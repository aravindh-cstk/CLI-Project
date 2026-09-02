'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const { DocModel } = require('../lib/doc-model');

const { checkFrontMatter } = require('../checks/front-matter');
const { checkSectionStructure } = require('../checks/section-structure');
const { checkBannedPhrases } = require('../checks/banned-phrases');
const { checkEmDashSemicolon } = require('../checks/em-dash-semicolon');
const { checkTroubleshootingFormat } = require('../checks/troubleshooting-format');
const { checkNextStepsLinks } = require('../checks/next-steps-links');
const { checkAcronymFirstUse } = require('../checks/acronym-first-use');
const { checkCliSpecific } = require('../checks/cli-specific');

function loadFixture(name) {
  return DocModel.fromFile(path.join(__dirname, 'fixtures', name));
}

function ids(findings) {
  return findings.map((f) => f.ruleId);
}

test('clean feature doc produces no Tier 1 findings across all checks', () => {
  const doc = loadFixture('clean-feature-doc.md');
  const findings = [
    ...checkFrontMatter(doc, 'feature-doc'),
    ...checkSectionStructure(doc, 'feature-doc'),
    ...checkBannedPhrases(doc),
    ...checkEmDashSemicolon(doc),
    ...checkTroubleshootingFormat(doc),
    ...checkNextStepsLinks(doc),
  ];
  assert.deepEqual(findings, []);
});

test('broken feature doc: malformed front matter line is caught', () => {
  const doc = loadFixture('broken-feature-doc.md');
  const findings = checkFrontMatter(doc, 'feature-doc');
  assert.ok(ids(findings).includes('FM-02'));
  assert.ok(ids(findings).includes('FM-01'));
});

test('broken feature doc: Quick Start is flagged as forbidden for feature-doc', () => {
  const doc = loadFixture('broken-feature-doc.md');
  const findings = checkSectionStructure(doc, 'feature-doc');
  assert.ok(findings.some((f) => f.message.includes('Quick Start')));
});

test('broken feature doc: casual and marketing phrases are all caught', () => {
  const doc = loadFixture('broken-feature-doc.md');
  const findings = checkBannedPhrases(doc);
  const messages = findings.map((f) => f.message);
  assert.ok(messages.some((m) => m.includes('seamless')));
  assert.ok(messages.some((m) => m.includes('just')));
  assert.ok(messages.some((m) => m.includes('right away')));
  assert.ok(messages.some((m) => m.includes('powerful')));
});

test('broken feature doc: symptom-only Troubleshooting entry is caught', () => {
  const doc = loadFixture('broken-feature-doc.md');
  const findings = checkTroubleshootingFormat(doc);
  assert.ok(ids(findings).includes('C1-05'), 'expected C1-05 for an entry with no Root Cause label');
});

// common-rules.md mandates `**Root Cause**` (one cause) or `**Root Causes**` (several).
// The check previously demanded the literal `**Root Cause(s)**`, so a doc following the
// written standard failed a tier-1 check. All three spellings are accepted now.
test('Troubleshooting accepts Root Cause, Root Causes, and Root Cause(s)', () => {
  for (const label of ['**Root Cause**', '**Root Causes**', '**Root Cause(s)**']) {
    const doc = new DocModel('inline.md', [
      '---', 'title: t', 'description: d', 'url: /u', '---', '',
      '# T', '', '## Troubleshooting', '', '### It fails', '',
      label + ' The token is missing.', '', '**Resolution** Add the token.', '',
    ].join('\n'));
    assert.deepEqual(checkTroubleshootingFormat(doc), [], 'rejected ' + label);
  }
});

test('em dash and semicolon detector ignores code fences and inline code', () => {
  const doc = new DocModel('inline.md', [
    '---',
    'title: t',
    'description: d',
    'url: /u',
    '---',
    '',
    '# T',
    '',
    '## Overview',
    '',
    'Use `a; b` inline, that is fine.',
    '',
    '```js',
    'const x = 1; // fine in code',
    '```',
    '',
    'But this sentence has a semicolon; right here.',
  ].join('\n'));
  const findings = checkEmDashSemicolon(doc);
  assert.equal(findings.length, 1);
  assert.equal(findings[0].line, 17);
});

test('acronym check accepts a combined slash-separated expansion like (CI/CD)', () => {
  const doc = new DocModel('inline.md', [
    '---',
    'title: t',
    'description: d',
    'url: /u',
    '---',
    '',
    '# T',
    '',
    '## Overview',
    '',
    'Use in a continuous integration / continuous delivery (CI/CD) pipeline.',
  ].join('\n'));
  const findings = checkAcronymFirstUse(doc);
  assert.deepEqual(findings, []);
});

test('acronym check flags a bare acronym used before its expansion', () => {
  const doc = new DocModel('inline.md', [
    '---',
    'title: t',
    'description: d',
    'url: /u',
    '---',
    '',
    '# T',
    '',
    '## Overview',
    '',
    'This uses SSR for rendering.',
  ].join('\n'));
  const findings = checkAcronymFirstUse(doc);
  assert.ok(findings.some((f) => f.message.includes('SSR')));
});

test('bare link in Next Steps is caught, described link is not', () => {
  const doc = new DocModel('inline.md', [
    '---',
    'title: t',
    'description: d',
    'url: /u',
    '---',
    '',
    '# T',
    '',
    '## Next Steps',
    '',
    '- [Bare Link](https://example.com/bare)',
    '- [Described Link](https://example.com/described): explains the thing.',
  ].join('\n'));
  const findings = checkNextStepsLinks(doc);
  assert.equal(findings.length, 1);
  assert.ok(findings[0].message.includes('bare'));
});

test('clean CLI command reference produces no CLI findings', () => {
  const doc = loadFixture('clean-cli-command-reference.md');
  assert.deepEqual(checkCliSpecific(doc, 'cli-command-reference'), []);
  assert.deepEqual(checkSectionStructure(doc, 'cli-command-reference'), []);
});

test('broken CLI command reference: Prerequisites at H3 is reported as misleveled, not missing', () => {
  const doc = loadFixture('broken-cli-command-reference.md');
  const found = ids(checkCliSpecific(doc, 'cli-command-reference'));
  assert.ok(found.includes('CLI-03'), 'expected CLI-03 for Prerequisites at H3');
  assert.ok(!found.includes('CLI-02'), 'must not also report Prerequisites as absent');
});

test('broken CLI command reference: wrong flag-table columns, H4 headings, buried install, bare fences', () => {
  const doc = loadFixture('broken-cli-command-reference.md');
  const found = ids(checkCliSpecific(doc, 'cli-command-reference'));
  assert.ok(found.includes('CLI-01'), 'expected CLI-01 for Flag/Short Flag/Description columns');
  assert.ok(found.includes('CLI-05'), 'expected CLI-05 for the H4 headings');
  assert.ok(found.includes('CLI-07'), 'expected CLI-07 for plugins:install with no Installation section');
  assert.ok(found.includes('CLI-06'), 'expected CLI-06 for the untagged code fence');
});

test('CLI-05 flags every H4, including command facets, which were previously exempt', () => {
  const doc = loadFixture('broken-cli-command-reference.md');
  const depth = checkCliSpecific(doc, 'cli-command-reference').filter((f) => f.ruleId === 'CLI-05');
  // `gadget:list` is a command id, `Flags` is a facet. The facet exemption is gone,
  // because a facet at H4 is just as unlinkable as a command at H4.
  assert.equal(depth.length, 2, 'expected both H4 headings to be reported');
  assert.ok(depth.some((f) => f.message.includes('gadget:list')));
  assert.ok(depth.some((f) => f.message.includes('Flags')));
  assert.ok(depth.every((f) => f.message.includes('bold lead-in')), 'message must name the fix');
});

test('CLI-05 still fires on a CLI doc that carries a non-CLI type', () => {
  // The V1-to-V2 migration guide is typed `migration-guide` but is rendered by the
  // same platform, so its 43 H4s are just as unlinkable. Without the isCli flag
  // this doc is never checked, which is the regression this test guards.
  const doc = loadFixture('broken-cli-command-reference.md');
  const found = ids(checkCliSpecific(doc, 'migration-guide', true));
  assert.ok(found.includes('CLI-05'), 'expected CLI-05 on a CLI doc typed migration-guide');
  assert.ok(!found.includes('CLI-01'), 'type-scoped checks must stay off for a non-CLI type');
  assert.ok(!found.includes('CLI-03'), 'type-scoped checks must stay off for a non-CLI type');
});

test('CLI checks stay silent on a non-CLI doc with a non-CLI type', () => {
  const doc = loadFixture('broken-cli-command-reference.md');
  assert.deepEqual(checkCliSpecific(doc, 'feature-doc', false), []);
  assert.deepEqual(checkCliSpecific(doc, 'how-to-guide', false), []);
});

test('module reference is exempt from the Prerequisites requirement', () => {
  const doc = new DocModel('inline.md', [
    '---', 'title: "X"', 'description: "Y"', 'url: "/z"', '---', '',
    '# CLI Limitations', '', '## Overview', '', 'What this indexes.', '',
  ].join('\n'));
  const found = ids(checkCliSpecific(doc, 'cli-module-reference'));
  assert.ok(!found.includes('CLI-02'), 'module reference must not be asked for Prerequisites');
});

test('CMS-mirror front matter satisfies the title, description, url requirement', () => {
  const doc = new DocModel('mirror.md', [
    '---', 'uid: "blt123"', 'seo_title: "T | Contentstack"', 'seo_description: "D"', '---', '',
    '# T', '',
  ].join('\n'));
  assert.deepEqual(ids(checkFrontMatter(doc, 'cli-command-reference')), []);
});

test('authored front matter still requires title, description, url', () => {
  const doc = new DocModel('authored.md', [
    '---', 'description: "D"', '---', '', '# T', '',
  ].join('\n'));
  const found = ids(checkFrontMatter(doc, 'cli-command-reference'));
  assert.ok(found.filter((x) => x === 'FM-01').length >= 2, 'expected missing title and url');
});

// CLI-16. The note below is the exact sentence that shipped on both Install the
// CLI pages while Create Custom CLI Plugins for Contentstack was live in both
// versions. A developer read it, concluded there were no plugin docs, and built
// their plugin from oclif's own documentation instead.
test('CLI-16 catches a doc claiming its own documentation does not exist', () => {
  const doc = new DocModel('install.md', [
    '---', 'uid: "blt123"', 'seo_title: "T"', 'seo_description: "D"', '---', '',
    '# Install the CLI', '', '## Namespaces', '',
    '> **Note**: The guide to create your own plugin within `csdx` is yet to come.',
    'But, as our CLI is built using the oclif package, you can create your custom',
    'plugin by referring to [oclif plugin documentation](https://oclif.io/docs/plugins).',
    '',
  ].join('\n'));
  const findings = checkBannedPhrases(doc);
  assert.ok(ids(findings).includes('CLI-16'), 'expected CLI-16 on "yet to come"');
});

test('CLI-16 does not fire on the corrected note, and ignores code fences', () => {
  const doc = new DocModel('fixed.md', [
    '---', 'uid: "blt123"', 'seo_title: "T"', 'seo_description: "D"', '---', '',
    '# Install the CLI', '', '## Namespaces', '',
    '> **Note:** To build your own plugin for `csdx`, see',
    '[Create Custom CLI Plugins for Contentstack](/docs/headless-cms/create-custom-cli-plugins).',
    '',
    '```', 'echo "coming soon"', '```', '',
  ].join('\n'));
  assert.ok(!ids(checkBannedPhrases(doc)).includes('CLI-16'));
});

// CLI-17. The check that did not exist. Nine absolute docs links sat in the
// corpus because the word "relative" appeared once in the whole standard, inside
// C2-04, and no check anywhere tested for a URL scheme at all.
const { checkInternalLinkForm } = require('../checks/internal-link-form');

test('CLI-17 catches an absolute link to the docs site and names the relative form', () => {
  const doc = new DocModel('abs.md', [
    '---', 'uid: "blt1"', 'seo_title: "T"', 'seo_description: "D"', '---', '',
    '# T', '', '## Overview', '',
    'See [Contentstack CLI](https://www.contentstack.com/docs/headless-cms/install-the-cli).',
    '',
  ].join('\n'));
  const findings = checkInternalLinkForm(doc);
  assert.ok(ids(findings).includes('CLI-17'));
  assert.match(findings[0].message, /\/docs\/headless-cms\/install-the-cli/);
});

test('CLI-17 leaves relative docs links, the login app, and third parties alone', () => {
  const doc = new DocModel('ok.md', [
    '---', 'uid: "blt1"', 'seo_title: "T"', 'seo_description: "D"', '---', '',
    '# T', '', '## Overview', '',
    '- [Install the CLI](/docs/headless-cms/install-the-cli): relative, correct.',
    '- [Contentstack account](https://www.contentstack.com/login): the app, not the docs.',
    '- [oclif](https://oclif.io/docs/plugins): third party.',
    '- [This section](#overview): a bare fragment.',
    '',
  ].join('\n'));
  assert.deepEqual(ids(checkInternalLinkForm(doc)), []);
});

test('CLI-17 ignores an absolute docs URL inside a code fence', () => {
  const doc = new DocModel('fence.md', [
    '---', 'uid: "blt1"', 'seo_title: "T"', 'seo_description: "D"', '---', '',
    '# T', '', '## Overview', '',
    '```', 'curl https://www.contentstack.com/docs/headless-cms/install-the-cli', '```',
    '',
  ].join('\n'));
  assert.deepEqual(ids(checkInternalLinkForm(doc)), []);
});
