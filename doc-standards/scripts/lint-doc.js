#!/usr/bin/env node
'use strict';

const path = require('path');
const { DocModel } = require('./lib/doc-model');
const { buildReport, renderText } = require('./lib/report');

const { checkFrontMatter } = require('./checks/front-matter');
const { checkSectionStructure } = require('./checks/section-structure');
const { checkBannedPhrases } = require('./checks/banned-phrases');
const { checkEmDashSemicolon } = require('./checks/em-dash-semicolon');
const { checkQaHeaders } = require('./checks/qa-headers');
const { checkTroubleshootingFormat } = require('./checks/troubleshooting-format');
const { checkNextStepsLinks } = require('./checks/next-steps-links');
const { checkQuickReferenceTable } = require('./checks/quick-reference-table');
const { checkAcronymFirstUse } = require('./checks/acronym-first-use');
const { checkMigrationSpecific } = require('./checks/migration-specific');
const { checkGettingStartedSpecific } = require('./checks/getting-started-specific');
const { checkHeuristics } = require('./checks/heuristic-flags');
const { checkCalloutTaxonomy } = require('./checks/callout-taxonomy');
const { checkConditionalFraming } = require('./checks/conditional-framing');
const { checkHeadingUniformity } = require('./checks/heading-uniformity');
const { checkUnverifiedClaims } = require('./checks/unverified-claims');
const { checkCliSpecific } = require('./checks/cli-specific');

const VALID_TYPES = [
  'conceptual-guide',
  'feature-doc',
  'how-to-guide',
  'setup-guide',
  'kickstarter',
  'migration-guide',
  'getting-started',
  'cli-command-reference',
  'cli-task-runbook',
  'cli-module-reference',
];

const CHECKS = [
  checkFrontMatter,
  checkSectionStructure,
  checkBannedPhrases,
  checkEmDashSemicolon,
  checkQaHeaders,
  checkTroubleshootingFormat,
  checkNextStepsLinks,
  checkQuickReferenceTable,
  checkAcronymFirstUse,
  checkMigrationSpecific,
  checkGettingStartedSpecific,
  checkHeuristics,
  checkCalloutTaxonomy,
  checkConditionalFraming,
  checkHeadingUniformity,
  checkUnverifiedClaims,
  checkCliSpecific,
];

function parseArgs(argv) {
  const args = { file: null, type: null, format: 'text', tiers: [1, 2] };
  for (const arg of argv) {
    if (arg.startsWith('--type=')) {
      args.type = arg.slice('--type='.length);
    } else if (arg.startsWith('--format=')) {
      args.format = arg.slice('--format='.length);
    } else if (arg.startsWith('--tiers=')) {
      args.tiers = arg
        .slice('--tiers='.length)
        .split(',')
        .map((n) => parseInt(n.trim(), 10));
    } else if (!arg.startsWith('--')) {
      args.file = arg;
    }
  }
  return args;
}

/**
 * True when the doc documents the Contentstack CLI. The `csdx` binary name is the
 * reliable signal: it appears in every CLI doc that shows a command, and in no
 * SDK or CMS doc. Title text is the fallback for the lookup pages that show none.
 */
function isCliDoc(doc, titleText) {
  const body = doc.lines.join('\n');
  if (/\bcsdx\b/.test(body)) return true;
  return /\bcli\b/.test(titleText);
}

/**
 * Which type a CLI doc gets, or null to fall through to the product-wide branches.
 *
 * These tests key off the doc's SUBJECT, not its current structure. That is
 * deliberate. Typing a doc by the sections it already has would mean a doc that is
 * missing its `Commands` section gets typed as something that does not need one,
 * so the omission would never be reported. `Export Content Using the CLI | V1.x.x`
 * is the case in point: it documents `cm:stacks:export` under `## Export Command`
 * rather than `## Commands`, and it must still be linted as a command reference so
 * that the wrong heading shows up as a finding.
 *
 * Three of the six CLI archetypes reuse a product-wide type, so this returns those
 * names too rather than falling through, which keeps the mapping in one place.
 */
function detectCliDocType(doc, titleText) {
  const h2 = doc.topLevelSections().map((s) => s.text.trim());

  // Docs with no H2 at all cannot satisfy any Section Order table. `Useful Plugins`
  // and `Uninstall CLI Plugins` are the two, both 12 to 26 line stubs whose content
  // is already covered elsewhere. They are reported as retire candidates instead.
  if (h2.length === 0) return null;

  // Reuses of product-wide types.
  if (/^install the cli\b/.test(titleText)) return 'setup-guide';
  if (/\basset scanning\b|\bcs assets\b/.test(titleText)) return 'feature-doc';

  // Lookup pages. Subject test only: these have no Commands section by definition,
  // and their Prerequisites, where one exists, is nested at H3 under another H2.
  if (/\blimitations\b|\bconfiguration reference\b|\bsupported features\b/.test(titleText)) {
    return 'cli-module-reference';
  }

  // A title that opens with an imperative operation names a procedure, so it is a
  // runbook whatever else the page contains. This runs before the plugin test
  // because `Migrate Selected Content Using the Query Export Plugin` is a runbook
  // that merely mentions a plugin in its title.
  if (/^(migrate|change|update|overwrite|restore|bootstrap|creat(e|ing) custom)\b/.test(titleText)) {
    return 'cli-task-runbook';
  }
  if (/\bmigration use cases\b|\bstarter apps\b/.test(titleText)) return 'cli-task-runbook';

  // A doc named after a plugin documents that plugin's command surface, even when
  // it carries a step list. `Generate Typescript Typings with TSGen Plugin`
  // documents the single `tsgen` command and its flags, and its `Steps for
  // execution` H2 is a usage walkthrough rather than a procedure spine. This test
  // precedes the spine test for that reason.
  if (/\bplugin\b/.test(titleText)) return 'cli-command-reference';

  // Procedure spine, for the runbooks whose title gives nothing away.
  const hasSpine =
    h2.some((t) => /^steps? for execution$/i.test(t)) ||
    h2.filter((t) => /^step \d+\s*:/i.test(t)).length >= 2;
  if (hasSpine) return 'cli-task-runbook';

  return 'cli-command-reference';
}

/**
 * `isCliDoc` against a doc alone, without going through type detection.
 *
 * Needed because CLI-C1 (headings stop at H3) binds on subject rather than on
 * type: a CLI doc typed `migration-guide` or `feature-doc` is still rendered by
 * the same platform, so its H4s are still unlinkable. The check loop passes this
 * to `checkCliSpecific` so those docs are not skipped.
 */
function docIsCli(doc) {
  const titleHeading = doc.headings.find((h) => h.level === 1);
  return isCliDoc(doc, titleHeading ? titleHeading.text.toLowerCase() : '');
}

/** Doc-type detection, mirroring ~/.claude/commands/revamp-doc.md Step 1's priority order. */
function detectDocType(doc) {
  const overviewSection = doc.findSection(['Overview']);
  const overviewText = overviewSection ? doc.sectionOwnBody(overviewSection).toLowerCase() : '';
  const titleHeading = doc.headings.find((h) => h.level === 1);
  const titleText = titleHeading ? titleHeading.text.toLowerCase() : '';
  const hasRoutingTable = Boolean(doc.findSection(['Role-Based Routing Table']));
  const hasQuickStart = Boolean(doc.findSection(['Quick Start']));

  if (titleText.startsWith('get started with') || (hasRoutingTable && hasQuickStart)) {
    return 'getting-started';
  }
  const hasMigrationStructure = Boolean(doc.findSection(['Type Mapping Reference', 'Pre-Upgrade Checklist']));

  // CLI types are resolved before the migration and feature-doc branches below,
  // both of which would otherwise swallow them. The migration branch matches any
  // title containing "migrat", which captures the 9 runbooks named "Migrate ...",
  // and the feature-doc branch matches any doc with a Commands section or the word
  // "command" or "plugin" in its title, which captures 43 of the 82 CLI docs.
  // A doc carrying genuine migration structure still falls through to
  // migration-guide, so the V1-to-V2 guide keeps its own type.
  if (isCliDoc(doc, titleText) && !hasMigrationStructure) {
    const cliType = detectCliDocType(doc, titleText);
    if (cliType) return cliType;
  }

  if (/\bmigrat|upgrad/.test(titleText) || hasMigrationStructure) {
    return 'migration-guide';
  }
  if (/^(fetch|configure|add|create|delete|update|list|generate|validate|compare)\b/.test(titleText)) {
    return 'how-to-guide';
  }
  if (/\binstall|configur.*(environment|sdk|runtime)/.test(overviewText)) {
    return 'setup-guide';
  }
  if (/\bclone|starter|kickstart/.test(overviewText) || /\bclone|starter|kickstart/.test(titleText)) {
    return 'kickstarter';
  }
  if (doc.findSection(['Commands', 'Command Reference']) || /\bplugin|command\b/.test(titleText)) {
    return 'feature-doc';
  }
  return 'conceptual-guide';
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.file) {
    console.error('Usage: lint-doc.js <file> [--type=doc-type] [--format=text|json] [--tiers=1,2]');
    process.exit(2);
  }

  const filePath = path.resolve(args.file);
  const doc = DocModel.fromFile(filePath);

  const docType = args.type || detectDocType(doc);
  if (!VALID_TYPES.includes(docType)) {
    console.error(`Unknown doc type "${docType}". Valid types: ${VALID_TYPES.join(', ')}`);
    process.exit(2);
  }

  const isCli = docIsCli(doc);
  let findings = [];
  for (const check of CHECKS) {
    findings = findings.concat(check(doc, docType, isCli));
  }
  findings = findings.filter((f) => args.tiers.includes(f.tier));

  const report = buildReport(args.file, docType, findings);

  if (args.format === 'json') {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(renderText(report));
  }

  process.exit(report.summary.errors > 0 ? 1 : 0);
}

main();
