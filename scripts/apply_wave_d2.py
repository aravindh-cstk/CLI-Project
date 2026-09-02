#!/usr/bin/env python3
"""Wave D, tier 2a: the 67 missing Next Steps sections.

Every entry is sourced, and the bar is deliberately high enough to stop this
becoming padding. Early in the project the decision was made to mark Examples
Required rather than Recommended, because "a Recommended section is advisory
and would be skipped". The mirror-image failure is just as bad: filling 67
sections with the same two generic links to move a number down. So:

  * A doc gets a Next Steps section only if at least 2 sourced links survive.
    Docs below that are deferred with a reason, not padded.
  * Every link carries a hand-written description of what the target covers,
    because C1-06 requires one and because a bare link list is what the
    plugin-guide pass proved raises the error count rather than lowering it.
  * A target with no curated description is dropped rather than given a
    generated one.

Three sources, in priority order, capped at 4 links:

  1  CLI docs the body prose already links, outside Prerequisites. A human
     already judged those relevant, which is the most trustworthy signal
     available.
  2  The same page in the other version tree. Useful in both directions right
     now, with 2.0.0 recently GA.
  3  CLI Limitations for the same version, for command references and runbooks,
     which is the genuine "what this does not cover" page.

A fourth source, resolving referenced commands to the doc that documents them,
was tried and dropped. See the comment at the point of use: neither syntax
lines nor headings identify an owning doc reliably, and both produced
confidently wrong links.

Authentication, Install and Configure Regions are excluded on purpose. They are
prerequisites, not next steps, and CLI-C13 already puts them in every command
doc's Prerequisites section.

Usage:
  python3 scripts/apply_wave_d2.py            # dry run, prints every section
  python3 scripts/apply_wave_d2.py --verify   # dry run plus an HTTP check
  python3 scripts/apply_wave_d2.py --confirm  # write
"""

import collections
import glob
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.docs_html import Doc, JSON_DIR  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "docs", "markdown")
LINT = os.path.join(ROOT, "doc-standards", "scripts", "lint-doc.js")
HOST = "https://www.contentstack.com"
DEFERRED_REPORT = os.path.join(ROOT, "notes", "reports", "wave-d-next-steps.md")

# Prerequisite pages, never a next step.
PREREQ_SLUGS = {"install-the-cli", "cli-authentication", "configure-regions-in-the-cli"}

# Retired, never link.
RETIRED_SLUGS = {"create-custom-cli-commands"}

# One curated description per target, keyed by the version-agnostic slug. A
# target absent from this map is dropped rather than described generically.
DESC = {
    "apps-cli-plugin": "manage Marketplace apps and their installations from the command line",
    "asset-scanning-in-cli": "scan assets for malware as part of an import or export",
    "bulk-operations-in-cli": "publish or unpublish entries and assets in bulk",
    "cli-audit-plugin": "audit exported data for reference and field problems before importing it",
    "cli-bootstrap-starter-apps": "bootstrap a starter app wired to a new stack",
    "cli-branches-migration-use-cases": "worked branch migration scenarios, including field renames",
    "cli-bulk-publish-and-unpublish-content": "publish or unpublish entries and assets in bulk",
    "cli-change-master-locale": "change a stack's master locale after content already exists",
    "cli-cloning-a-stack": "copy a stack's structure and content with a single clone command",
    "cli-content-type-plugin": "inspect, compare and diagram content types from the command line",
    "cli-entry-migration": "migrate entries between stacks with field-level control",
    "cli-export-content-to-csv-file": "export entries, assets or users to CSV",
    "cli-for-cs-assets": "the CS Assets commands, which use the cs-assets REST API rather than the Content Management API",
    "cli-for-launch": "deploy and manage Launch projects from the command line",
    "cli-import-content-using-the-seed-command": "seed a stack from a starter repository in one command",
    "cli-limitations": "the coverage gaps and known constraints across CLI commands",
    "cli-migrate-and-overwrite-content-in-the-same-stack": "overwrite content in place rather than importing into a fresh stack",
    "cli-migrate-content-from-html-rte-to-json-rte": "convert HTML RTE fields to JSON RTE",
    "cli-migrate-selected-content-types-using-the-query-export-plugin": "export only the content types a query matches",
    "cli-query-based-export": "export only the entries a query matches",
    "cli-regex-validate-plugin": "validate the regex patterns set on content type fields",
    "cli-supported-features-for-export-import-and-clone-operations": "which modules export, import and clone cover, module by module",
    "cli-tsgen-plugin": "generate TypeScript typings from your content types",
    "cli-update-missing-reference-uids": "repair entries, assets and extensions whose reference UIDs are missing",
    "cli-useful-plugins": "community plugins that extend the CLI",
    "cli-v1-to-v2-migration-guide": "what changed at 2.0.0, flag by flag, and how to upgrade",
    "compare-and-merge-branches-using-the-cli": "compare and merge content model changes between branches",
    "configure-cli-logging-preferences": "switch between progress bars and console logs",
    "configure-early-access-program-in-the-cli": "turn on early access features for a plugin",
    "configure-mfa-secret-using-cli": "store an MFA secret so scripted logins do not prompt",
    "configure-proxy-settings-in-cli": "route CLI traffic through a corporate proxy",
    "configure-rate-limits-in-the-cli": "raise or lower the API rate limits the CLI applies",
    "contentstack-cli-configuration-reference": "every configuration key the plugins accept, and how overlapping sources resolve",
    "create-custom-cli-plugins": "build and publish your own csdx commands",
    "export-content-using-the-cli": "export stack content to disk before importing it elsewhere",
    "import-content-using-the-cli": "import exported content into a target stack",
    "migrate-content-between-stacks-using-the-cli": "the end-to-end stack-to-stack migration procedure",
    "migrate-your-content-using-the-cli-migration-command": "run scripted content model changes with the migration command",
    "overwrite-existing-content-using-cli-import": "overwrite existing entries and assets during an import",
    "uninstall-cli-plugins": "remove a plugin you no longer need",
}


def slug_of(url):
    return re.sub(r"^/headless-cms/", "", url).replace("/v1", "").replace("/v0", "")


def clean_title(title):
    title = re.sub(r"^\[Contentstack Command-line Interface \(CLI\)\] - ", "", title)
    title = re.sub(r"^\[Command Line Interface\] - ", "", title)
    return re.sub(r"\s*\|\s*V[012]\.x\.x\s*$", "", title).strip()


def http_ok(url):
    """Fetch the page a written href actually points at.

    Entry urls in index.json are stored without the /docs prefix, while the
    hrefs written into the content include it. Verifying the bare url made every
    single target look like a 404, which would have deferred all 67 docs and
    looked like a corpus problem rather than a missing prefix.
    """
    req = urllib.request.Request(HOST + "/docs" + url,
                                 headers={"User-Agent": "Mozilla/5.0"}, method="GET")
    try:
        return urllib.request.urlopen(req, timeout=45).getcode()
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception:
        return None


def gather():
    """(missing docs, types, command ownership, mentions) from the linter and corpus."""
    missing, types = [], {}
    owns, mentions = collections.defaultdict(set), collections.defaultdict(set)
    files = [f for f in sorted(glob.glob(MD + "/**/*.md", recursive=True))
             if "/Version 1" in f or "/Version 2" in f]
    for f in files:
        rel = os.path.relpath(f, MD)
        text = open(f, encoding="utf-8").read()
        for m in re.finditer(r"csdx\s+([a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)+)", text):
            mentions[rel].add(m.group(1))
        for m in re.finditer(r"^csdx\s+([a-z][a-z0-9-]*(?::[a-z][a-z0-9-]*)+)\s*(\[OPTIONS\]|$)",
                             text, re.M):
            owns[rel].add(m.group(1))
        proc = subprocess.run(["node", LINT, f, "--format=json"], capture_output=True,
                              text=True, cwd=os.path.dirname(LINT))
        if not proc.stdout.strip():
            sys.exit(f"linter produced no output for {rel}. Pass absolute paths.")
        data = json.loads(proc.stdout)
        types[rel] = data.get("type")
        if any('Required section "Next Steps" is missing' in x.get("message", "")
               for x in data.get("automatedFindings", [])):
            missing.append(rel)
    return missing, types, owns, mentions


def body_links(rel):
    """CLI doc URLs the body prose links, with the Prerequisites block removed."""
    text = open(os.path.join(MD, rel), encoding="utf-8").read()
    text = re.sub(r"^## Prerequisites.*?(?=^## )", "", text, flags=re.S | re.M)
    out = []
    for m in re.finditer(r"\]\((/docs(/headless-cms/[^)#]*))", text):
        out.append(m.group(2).rstrip("/"))
    return out


def main():
    confirm = "--confirm" in sys.argv
    verify = "--verify" in sys.argv or confirm
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    index = json.load(open(os.path.join(JSON_DIR, "index.json"), encoding="utf-8"))
    by_md = {e["markdown"]: e for e in index["entries"]}
    by_url = {}
    for e in index["entries"]:
        by_url.setdefault(e["url"], e)

    missing, types, owns, mentions = gather()

    cmd_owner = collections.defaultdict(list)
    for rel, cmds in owns.items():
        for cmd in cmds:
            cmd_owner[cmd].append(rel)

    def stem(title):
        return clean_title(title)
    stems = collections.defaultdict(list)
    for e in index["entries"]:
        stems[stem(e["title"])].append(e)

    plans, deferred = [], []
    for rel in missing:
        entry = by_md.get(rel)
        if entry is None:
            deferred.append((rel, "not in index.json"))
            continue
        is_v1 = rel.startswith("Version 1")
        picks, seen_urls = [], {entry["url"]}

        def add(target_entry, why, desc=None):
            """Dedupe on URL, not slug. A V1 and a V2 page share their slug and
            differ only by the /v1 suffix, so deduping on slug silently blocked
            every cross-version link."""
            slug = slug_of(target_entry["url"])
            if slug in PREREQ_SLUGS or slug in RETIRED_SLUGS:
                return
            # Keep the reader in their own version tree where a counterpart exists.
            if is_v1 and not target_entry["url"].endswith("/v1"):
                alt = [x for x in stems[stem(target_entry["title"])]
                       if x["url"].endswith("/v1")]
                if alt:
                    target_entry = alt[0]
            text = desc or DESC.get(slug)
            if text is None or target_entry["url"] in seen_urls:
                return
            seen_urls.add(target_entry["url"])
            picks.append((target_entry, text, why))

        # Command-to-doc ownership was tried as the first and strongest source
        # and then dropped, because it cannot be derived reliably from the
        # corpus. Matching a `csdx <cmd> [OPTIONS]` syntax line makes the CS
        # Assets page look like the owner of auth:login and the Configuration
        # Reference look like the owner of cm:stacks:export, since both quote
        # those commands in examples. Matching headings instead is worse: the
        # V1-to-V2 migration guide has a heading per command, so it comes out
        # owning almost the entire surface. Both produced confidently wrong
        # links, which is worse than a shorter Next Steps section.
        # 1. body prose links
        for url in body_links(rel):
            target = by_url.get(url)
            if target:
                add(target, "linked in the body")
        # 2. For a V1 reader the useful forward step is the upgrade guide, not
        #    the V2 copy of the same page. Linking the V2 copy would send them
        #    to flags their installed CLI does not have.
        if is_v1:
            guide = by_url.get("/headless-cms/cli-v1-to-v2-migration-guide")
            if guide:
                add(guide, "how to upgrade")
        # 3. CLI Limitations
        if types.get(rel) in ("cli-command-reference", "cli-task-runbook"):
            lim = by_url.get("/headless-cms/cli-limitations/v1" if is_v1
                             else "/headless-cms/cli-limitations")
            if lim:
                add(lim, "coverage gaps")

        picks = picks[:4]
        # Two bars, not one. At least 2 links, AND at least one of them specific
        # to this doc. "How to upgrade" plus "coverage gaps" is true and
        # relevant, but it is the same pair on every page, so on its own it is
        # padding dressed as a section. A doc that cannot offer one specific
        # onward link is deferred for a person to write.
        specific = [p for p in picks if p[2] == "linked in the body"]
        if len(picks) < 2 or not specific:
            why = ("no onward link specific to this doc, only the generic upgrade "
                   "and limitations pair" if len(picks) >= 2
                   else f"only {len(picks)} sourced link(s) with a curated description")
            deferred.append((rel, why))
            continue
        plans.append((rel, entry, picks))

    checked = {}
    if verify:
        for _rel, _entry, picks in plans:
            for target, _d, _w in picks:
                checked.setdefault(target["url"], None)
        print(f"verifying {len(checked)} distinct link targets over HTTP ...")
        for url in list(checked):
            checked[url] = http_ok(url)
        bad = {u: c for u, c in checked.items() if c != 200}
        if bad:
            print("NOT 200, these will not be written:")
            for u, c in bad.items():
                print(f"   {c}  {u}")
        else:
            print("all 200\n")

    written = 0
    for rel, entry, picks in plans:
        picks = [p for p in picks if not verify or checked.get(p[0]["url"]) == 200]
        if len(picks) < 2:
            deferred.append((rel, "links did not resolve over HTTP"))
            continue
        print(f"{rel.split('/')[-1][:58]}  ({entry['uid']})")
        for target, desc, why in picks:
            print(f"    - {clean_title(target['title'])[:44]:46s} [{why}]")
        if not confirm:
            continue
        path = os.path.join(JSON_DIR, entry["json"])
        doc = Doc.load(path)
        if doc.find_heading("Next Steps", level=2):
            continue
        heading = doc.soup.new_tag("h2")
        heading.string = "Next Steps"
        ul = doc.soup.new_tag("ul")
        for target, desc, _why in picks:
            li = doc.soup.new_tag("li")
            a = doc.soup.new_tag("a", href="/docs" + target["url"])
            a.string = clean_title(target["title"])
            li.append(a)
            li.append(f": {desc}.")
            ul.append(li)
        doc.soup.append(heading)
        doc.soup.append(ul)
        if doc.save():
            written += 1

    lines = ["# Wave D: the Next Steps pass", "",
             f"{len(missing)} docs had no Next Steps section. "
             f"{len(plans)} got one. {len(deferred)} were deferred.", "",
             "**Every entry is sourced and every description is hand written.** A "
             "doc gets a section only when at least 2 sourced links survive, and a "
             "link target with no curated description is dropped rather than given "
             "a generated one. Filling 67 sections with the same two generic links "
             "would move the error count without helping a reader, which is the "
             "mirror image of skipping the section entirely.", "",
             "Authentication, Install the CLI and Configure Regions are excluded on "
             "purpose. They are prerequisites, not next steps, and CLI-C13 already "
             "puts them in every command doc's Prerequisites section.", "",
             "## Deferred", "", "| Doc | Why |", "|---|---|"]
    for rel, why in deferred:
        lines.append(f"| `{rel}` | {why} |")
    lines.append("")
    if confirm:
        open(DEFERRED_REPORT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print(f"\nwrote {os.path.relpath(DEFERRED_REPORT, ROOT)}")

    print(f"\nplanned {len(plans)}, deferred {len(deferred)}")
    if not confirm:
        print("Dry run complete. Nothing written.")
        return 0
    print(f"wrote {written} json files. Regenerating docs/markdown ...")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "json_to_markdown.py")],
                   check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
