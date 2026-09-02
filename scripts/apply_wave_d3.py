#!/usr/bin/env python3
"""Wave D, tier 2b: Examples sections for 8 V2 command references.

32 docs had no Examples section. 8 get one here. The other 24 are deferred, and
the reasons matter more than the count, because three of them are correctness
traps rather than effort problems.

Why only 8:

  V1 docs are excluded outright. The only verified flag data available is
  notes/reports/flag-inventory.json, generated from the oclif.manifest.json
  inside each published 2.0.0 tarball. Writing 2.0.0 examples onto a V1 page is
  exactly the defect CLI-C11 exists to stop: cm:stacks:migration --config kept
  its name and changed its meaning between the versions, and short flags were
  removed across six plugins. A V1 reader copying a 2.0.0 example gets a
  command that fails, or worse, one that silently does something else.

  Query-based Export is excluded even though it qualifies on every other test,
  because it is one CMS entry shown in both version trees. Adding 2.0.0
  examples would put them on the V1 page too.

  CLI for Launch, Apps CLI Plugin and Configure MFA Secret are excluded as
  mis-scoped. The accuracy report's scoping picks the most-mentioned command
  with a published manifest, which for those three is auth:login, because their
  real subjects (launch:*, app:*) publish no manifest and MFA has no command of
  its own. auth:login ships exactly three flags, none of them related to MFA,
  Launch or Marketplace apps.

  The rest document several commands each, so a single Examples section cannot
  be scoped from the flag data alone.

Every flag in every example below is checked against the inventory before
anything is written, and the script refuses to write on a single unknown flag.
That check is the point: it means no example can claim a flag the released
binary does not have.

What is NOT claimed: that a given combination is the best way to do a task.
Each example states what its flags do, drawn from the manifest's own
descriptions, and nothing more.

Usage:
  python3 scripts/apply_wave_d3.py            # dry run, prints every example
  python3 scripts/apply_wave_d3.py --confirm  # write
"""

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.docs_html import Doc, JSON_DIR  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY = os.path.join(ROOT, "notes", "reports", "flag-inventory.json")
REPORT = os.path.join(ROOT, "notes", "reports", "wave-d-examples.md")

# (uid, rel json path, command)
TARGETS = [
    ("bltb61fca77fed848a6", "Version 2.x.x/CLI Commands V2/Cloning a Stack | V2.x.x.json",
     "cm:stacks:clone"),
    ("blt66365ee2f36e0315",
     "Version 2.x.x/CLI Commands V2/Configure CLI Logging Preferences | V2.x.x.json",
     "config:set:log"),
    ("bltc7a1129f3ee45ffd",
     "Version 2.x.x/Miscellaneous V2/Configure Rate Limits in the CLI | V2.x.x.json",
     "config:set:rate-limit"),
    ("blt267c4988aa1389a5",
     "Version 2.x.x/Get Started with CLI V2/Configure Regions in the CLI | V2.x.x.json",
     "config:set:region"),
    ("blt2fe395869b399af0",
     "Version 2.x.x/CLI Commands V2/Export Content Using the CLI | V2.x.x.json",
     "cm:stacks:export"),
    ("blt1215a1f9bbcc9900",
     "Version 2.x.x/CLI Commands V2/Import Content Using the CLI | V2.x.x.json",
     "cm:stacks:import"),
    ("blt25e29bfc7ef93e50",
     "Version 2.x.x/Content Migration Commands V2/Export Content to CSV File Using the CLI | V2.x.x.json",
     "cm:export-to-csv"),
    ("blt9f703f1d6c0405d9",
     "Version 2.x.x/Content Migration Commands V2/Import Content Using the Seed Command | V2.x.x.json",
     "cm:stacks:seed"),
]

# command -> [(lead-in sentence, command line)]
# Placeholders follow CLI-C6: single angle brackets, upper snake case.
EXAMPLES = {
    "cm:stacks:clone": [
        ("Clone both structure and content into a brand new stack, naming it as you go.",
         "csdx cm:stacks:clone --source-stack-api-key <SOURCE_API_KEY> "
         "--stack-name <NEW_STACK_NAME> --type a"),
        ("Clone into an existing destination stack using saved management token aliases "
         "rather than API keys.",
         "csdx cm:stacks:clone --source-management-token-alias <SOURCE_ALIAS> "
         "--destination-management-token-alias <DEST_ALIAS>"),
        ("Clone one branch into another, skipping the audit fix that otherwise runs "
         "during the import half of the operation.",
         "csdx cm:stacks:clone --source-stack-api-key <SOURCE_API_KEY> "
         "--destination-stack-api-key <DEST_API_KEY> --source-branch <SOURCE_BRANCH> "
         "--target-branch <TARGET_BRANCH> --skip-audit"),
    ],
    "config:set:log": [
        ("Turn on console logging, which replaces the progress bar view.",
         "csdx config:set:log --show-console-logs"),
        ("Raise the log level and send log files to a directory of your choosing.",
         "csdx config:set:log --level debug --path <LOG_DIRECTORY>"),
    ],
    "config:set:rate-limit": [
        ("Set the utilization percentage for an organization, which governs how much of "
         "the available rate limit the CLI will consume.",
         "csdx config:set:rate-limit --org <ORG_UID> --utilize 70"),
        ("Set utilization for named limits only, passing the limit names separated by "
         "commas.",
         "csdx config:set:rate-limit --org <ORG_UID> --limit-name getRateLimit,bulkLimit "
         "--utilize 60,80"),
        ("Reset an organization back to the default rate limit.",
         "csdx config:set:rate-limit --org <ORG_UID> --default"),
    ],
    "config:set:region": [
        ("Point every API at a custom host in one command by naming the region. Adding "
         "--name is what makes the CLI treat the other hosts as a named region rather "
         "than individual overrides.",
         "csdx config:set:region --name <REGION_NAME> --cma <CMA_HOST> --cda <CDA_HOST> "
         "--ui-host <UI_HOST>"),
        ("Override only the Launch and Developer Hub hosts, leaving the rest of the "
         "region as it is.",
         "csdx config:set:region --launch <LAUNCH_HOST> "
         "--developer-hub <DEVELOPER_HUB_HOST>"),
    ],
    "cm:stacks:export": [
        ("Export an entire stack to a directory, authenticating with a management token "
         "alias.",
         "csdx cm:stacks:export --alias <MANAGEMENT_TOKEN_ALIAS> --data-dir <EXPORT_PATH>"),
        ("Export a single module rather than the whole stack.",
         "csdx cm:stacks:export --stack-api-key <STACK_API_KEY> --data-dir <EXPORT_PATH> "
         "--module content-types"),
        ("Export named content types from a specific branch, and skip the Marketplace "
         "prompts so the command can run unattended.",
         "csdx cm:stacks:export --alias <MANAGEMENT_TOKEN_ALIAS> --data-dir <EXPORT_PATH> "
         "--branch <BRANCH_NAME> --content-types blog_post author --yes"),
    ],
    "cm:stacks:import": [
        ("Import a previously exported directory into a target stack.",
         "csdx cm:stacks:import --alias <MANAGEMENT_TOKEN_ALIAS> --data-dir <EXPORT_PATH>"),
        ("Import one module and replace the copy already in the target stack.",
         "csdx cm:stacks:import --stack-api-key <STACK_API_KEY> --data-dir <EXPORT_PATH> "
         "--module entries --replace-existing"),
        ("Import into a branch without publishing assets, and skip the audit fix, which "
         "shortens a large import.",
         "csdx cm:stacks:import --alias <MANAGEMENT_TOKEN_ALIAS> --data-dir <EXPORT_PATH> "
         "--branch <BRANCH_NAME> --skip-assets-publish --skip-audit"),
    ],
    "cm:export-to-csv": [
        ("Export the entries of one content type in one locale.",
         "csdx cm:export-to-csv --action entries --alias <MANAGEMENT_TOKEN_ALIAS> "
         "--content-type blog_post --locale en-us"),
        ("Export the users of an organization, naming the organization so the CSV "
         "filename reflects it.",
         "csdx cm:export-to-csv --action users --org <ORG_UID> --org-name <ORG_NAME>"),
        ("Export taxonomy terms with a semicolon delimiter, which suits spreadsheets "
         "configured for it.",
         "csdx cm:export-to-csv --action taxonomies --stack-api-key <STACK_API_KEY> "
         "--taxonomy-uid <TAXONOMY_UID> --delimiter \";\""),
    ],
    "cm:stacks:seed": [
        ("Seed a new stack in an organization from the default starter repository.",
         "csdx cm:stacks:seed --org <ORG_UID> --stack-name <NEW_STACK_NAME>"),
        ("Seed from a specific GitHub repository into an existing stack.",
         "csdx cm:stacks:seed --repo <GITHUB_ORG>/<REPO_NAME> "
         "--stack-api-key <STACK_API_KEY>"),
        ("Seed without the confirmation prompt, for use in a script.",
         "csdx cm:stacks:seed --org <ORG_UID> --stack-name <NEW_STACK_NAME> --yes"),
    ],
}


def flags_used(line):
    return set(re.findall(r"--([a-z][a-z0-9-]*)", line))


def main():
    confirm = "--confirm" in sys.argv
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    ga = json.load(open(INVENTORY, encoding="utf-8"))["commands"]

    # Hard gate. Every flag in every example must exist on that command in the
    # published 2.0.0 manifest, or nothing is written at all.
    bad = []
    for cmd, examples in EXAMPLES.items():
        if cmd not in ga:
            bad.append(f"{cmd}: not in the inventory")
            continue
        known = set(ga[cmd]["flags"])
        for _lead, line in examples:
            if not line.startswith(f"csdx {cmd} "):
                bad.append(f"{cmd}: example does not invoke it: {line[:60]}")
            for flag in sorted(flags_used(line) - known):
                bad.append(f"{cmd}: --{flag} does not exist on this command")
    if bad:
        print("FLAG CHECK FAILED, nothing will be written:")
        for b in bad:
            print("  " + b)
        return 1
    total = sum(len(v) for v in EXAMPLES.values())
    print(f"flag check passed: {total} examples, every flag verified against the "
          f"published 2.0.0 manifests\n")

    written = 0
    for uid, rel, cmd in TARGETS:
        path = os.path.join(JSON_DIR, rel)
        if not os.path.exists(path):
            print(f"MISSING {rel}")
            continue
        doc = Doc.load(path)
        if doc.entry.get("uid") != uid:
            print(f"SKIP {rel}: uid is {doc.entry.get('uid')}, expected {uid}")
            continue
        if doc.find_heading("Examples", level=2):
            print(f"SKIP {rel.split('/')[-1][:52]}: already has an Examples section")
            continue

        print(f"{rel.split('/')[-1][:56]}  ({uid})  {cmd}")
        for lead, line in EXAMPLES[cmd]:
            print(f"    {line[:104]}")

        if not confirm:
            continue
        heading = doc.soup.new_tag("h2")
        heading.string = "Examples"
        anchor = doc.find_heading("Troubleshooting", level=2) or \
            doc.find_heading("Limitations", level=2) or \
            doc.find_heading("Next Steps", level=2)
        nodes = [heading]
        for lead, line in EXAMPLES[cmd]:
            p = doc.soup.new_tag("p")
            p.string = lead
            pre = doc.soup.new_tag("pre")
            pre.string = line
            nodes += [p, pre]
        if anchor is not None:
            for node in nodes:
                anchor.insert_before(node)
        else:
            for node in nodes:
                doc.soup.append(node)
        if doc.save():
            written += 1

    lines = ["# Wave D: the Examples pass", "",
             "32 docs had no Examples section. 8 got one. 24 are deferred, and three "
             "of the reasons are correctness traps rather than effort.", "",
             "## Why V1 docs get nothing here", "",
             "The only verified flag data is `notes/reports/flag-inventory.json`, built "
             "from the `oclif.manifest.json` inside each published **2.0.0** tarball. "
             "Writing a 2.0.0 example onto a V1 page is the defect `CLI-C11` exists to "
             "stop. `cm:stacks:migration --config` kept its name and changed its "
             "meaning between the versions, and short flags were removed across six "
             "plugins, so a V1 reader copying a 2.0.0 line gets a command that fails "
             "or, worse, one that quietly does something else.", "",
             "## The three that look eligible and are not", "",
             "| Doc | Why |", "|---|---|",
             "| `Query-based Export` | One CMS entry shown in both version trees, so "
             "2.0.0 examples would land on the V1 page as well. |",
             "| `CLI for Launch`, both versions | The accuracy report scopes it to "
             "`auth:login`, because `launch:*` publishes no manifest. `auth:login` "
             "ships three flags and none of them concerns Launch. |",
             "| `Apps CLI Plugin | V2.x.x` | Same scoping artifact. Its subject is "
             "`app:*`, which publishes no manifest. |",
             "| `Configure MFA Secret Using CLI | V2.x.x` | MFA has no command of its "
             "own. The doc sets `CONTENTSTACK_MFA_SECRET` and then runs `auth:login`, "
             "so an Examples section would repeat its Commands section. |", "",
             "## The rest", "",
             "Each documents several commands, so one Examples section cannot be scoped "
             "from flag data alone: `Audit Plugin` (4 commands), `Compare and Merge "
             "Branches` (8 in V1, 10 in V2), `CLI Authentication and Adding Tokens` "
             "(6 and 7), `Configure Early Access` (3), `Configure Proxy Settings` (3), "
             "and `Bulk Publish and Unpublish Content`, whose commands publish no "
             "manifest.", "",
             "## What the 8 sections do and do not claim", "",
             "Every flag in every example is checked against the inventory before "
             "anything is written, and the script refuses to write on a single unknown "
             "flag. So no example can name a flag the released binary does not have.", "",
             "What is **not** claimed is that a combination is the best way to do a "
             "task. Each example states what its flags do, drawn from the manifest's "
             "own descriptions, and stops there.", ""]
    if confirm:
        open(REPORT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print(f"\nwrote {os.path.relpath(REPORT, ROOT)}")
    if not confirm:
        print("\nDry run complete. Nothing written.")
        return 0
    print(f"\nwrote {written} json files. Regenerating docs/markdown ...")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "json_to_markdown.py")],
                   check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
