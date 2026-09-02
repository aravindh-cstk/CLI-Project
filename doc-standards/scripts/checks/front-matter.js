'use strict';

const { makeFinding } = require('../lib/report');

const BASE_REQUIRED_KEYS = ['title', 'description', 'url'];

// Docs generated from the CMS carry the mirror's own front matter shape, written by
// scripts/json_to_markdown.py: uid, seo_title, seo_description. Those three satisfy
// the same requirement as title, description, url, so a mirrored doc must not be
// reported as missing all three. Detected by the presence of `uid`, which authored
// front matter never carries.
const MIRROR_KEYS = { title: 'seo_title', description: 'seo_description', url: 'uid' };

function isCmsMirror(fm) {
  return 'uid' in fm.keys && !('title' in fm.keys);
}

/** Tier 1: required front matter keys present, malformed key:value lines, version field for migration guides. */
function checkFrontMatter(doc, docType) {
  const findings = [];
  const fm = doc.frontMatter;

  if (!fm.present) {
    findings.push(
      makeFinding({
        tier: 1,
        ruleId: 'FM-01',
        checkId: 'front-matter',
        message: 'No YAML front matter block found at the top of the document.',
        line: 1,
      })
    );
    return findings;
  }

  for (const malformed of fm.malformedLines) {
    findings.push(
      makeFinding({
        tier: 1,
        ruleId: 'FM-02',
        checkId: 'front-matter',
        line: malformed.line,
        message: `Malformed front matter line, not a valid "key: value" pair: ${JSON.stringify(malformed.text)}`,
      })
    );
  }

  const requiredKeys = [...BASE_REQUIRED_KEYS];
  if (docType === 'migration-guide') requiredKeys.push('version');

  const mirror = isCmsMirror(fm);
  for (const key of requiredKeys) {
    if (key in fm.keys) continue;
    // A mirrored doc satisfies the requirement through its equivalent key.
    if (mirror && MIRROR_KEYS[key] && MIRROR_KEYS[key] in fm.keys) continue;
    findings.push(
      makeFinding({
        tier: 1,
        ruleId: key === 'version' ? 'MIG-02' : 'FM-01',
        checkId: 'front-matter',
        line: fm.startLine,
        message: mirror
          ? `Missing required front matter key "${key}" (or its mirror equivalent "${MIRROR_KEYS[key] || key}").`
          : `Missing required front matter key "${key}".`,
      })
    );
  }

  return findings;
}

module.exports = { checkFrontMatter };
