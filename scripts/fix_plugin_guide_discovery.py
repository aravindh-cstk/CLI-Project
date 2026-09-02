#!/usr/bin/env python3
"""Stop the Install pages telling readers the plugin guide does not exist.

Both Install pages carry this note, in the Namespaces section:

    Note: The guide to create your own plugin within csdx is yet to come. But,
    as our CLI is built using the oclif package, you can create your custom
    plugin by referring to oclif plugin documentation.

It is false in both versions. `Create Custom CLI Plugins for Contentstack` ships
as V2 (blt64294e11f81fe300) and V1 (blt4f27fd89adf6b6c1), both live on
production and both in the sidebar. The V2 one is V2-current: it pins
@contentstack/cli-command and cli-utilities at ~2.0.0 and uses @oclif/core v4.

The note did real damage. A developer looking for CLI 2.0.0 plugin information
read it, concluded Contentstack had no plugin docs, and built their plugin from
the source repo and oclif's own documentation instead. A sentence that states
the absence of a guide outlives the gap it describes, and steers readers away
from the guide that later ships.

Three edits, in descending order of what they cost a reader:

  WI-1  Replace the note on both Install pages. Separate CMS entries, so this is
        genuinely two edits rather than one shared one.
  WI-2  Add inbound prose links. Today zero of the 82 CLI docs link to either
        authoring guide, so discovery depends entirely on the sidebar and site
        search.
  WI-3  Fill the migration guide's plugin-author checklist, which has one item
        (bump Node to 22) while four more author-facing breaking changes sit
        documented in the authoring guide and absent from the checklist.

docs/markdown/ is generated from docs/json/ by scripts/json_to_markdown.py, so
editing a .md file achieves nothing. These edits go into
article_content[0].article_section.content, which is HTML.

Replacements are literal string matches on the stored HTML rather than a parsed
round-trip, so nothing outside the matched span can change. Following
scripts/fix_ga_changelog.py, a miss is reported and the write refused, so a
silent no-op is impossible.

Usage:
  python3 scripts/fix_plugin_guide_discovery.py            # dry run, shows the plan
  python3 scripts/fix_plugin_guide_discovery.py --confirm  # write
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(ROOT, "docs", "json")

INSTALL_V2 = "Version 2.x.x/Get Started with CLI V2/Install the CLI | V2.x.x.json"
INSTALL_V1 = "Version 1.x.x/Get Started with CLI/Install the CLI | V1.x.x.json"
MIGRATION = ("Version 2.x.x/Get Started with CLI V2/"
             "Migrate from Contentstack CLI V1 to V2 | V2.x.x.json")

EXPECTED_UID = {
    INSTALL_V2: "blt91a20a3ff7b6e05d",
    INSTALL_V1: "blt0756f65e7c6f9eed",
    MIGRATION: "blt05c442f72f396864",
}

PLUGINS_V2 = "/docs/headless-cms/create-custom-cli-plugins"
PLUGINS_V1 = "/docs/headless-cms/create-custom-cli-plugins/v1"
GUIDE_TITLE = "Create Custom CLI Plugins for Contentstack"


def c(text):
    return f'<span class="code">{text}</span>'


# --- WI-1: the false note --------------------------------------------------
# The two pages differ only in the <a> attribute order, which is why each is
# matched separately rather than through one shared pattern.

NOTE_V2_OLD = (
    '<p class="note"><strong>Note</strong>: The guide to create your own plugin '
    'within <span class="code">csdx</span> is yet to come. But, as our CLI is '
    'built using the oclif package, you can create your custom plugin by '
    'referring to <a href="https://oclif.io/docs/plugins" rel="noreferrer" '
    'target="_blank">oclif plugin documentation</a>.</p>'
)
NOTE_V1_OLD = (
    '<p class="note"><strong>Note</strong>: The guide to create your own plugin '
    'within <span class="code">csdx</span> is yet to come. But, as our CLI is '
    'built using the oclif package, you can create your custom plugin by '
    'referring to <a rel="noreferrer" href="https://oclif.io/docs/plugins" '
    'target="_blank">oclif plugin documentation</a>.</p>'
)


def note_new(guide_url):
    """The oclif pointer is kept and demoted rather than dropped. It is still
    useful, and removing it would lose information. The rewrite also brings the
    callout into CLI-C9 compliance, with the colon inside the bold."""
    return (
        '<p class="note"><strong>Note:</strong> To build your own plugin for '
        f'{c("csdx")}, see <a href="{guide_url}">{GUIDE_TITLE}</a>. The CLI is '
        'built on oclif, so the <a href="https://oclif.io/docs/plugins" '
        'rel="noreferrer" target="_blank">oclif plugin documentation</a> '
        'applies as well.</p>'
    )


# --- WI-2: inbound links ---------------------------------------------------
# The V1 page's section is `Next Step`, singular. A second bullet makes that
# ungrammatical, and CLI-C11 mandates the plural anyway. Nothing in the corpus
# links to #next-step, so the anchor change is safe.

# C1-06 requires a one-sentence description on every Next Steps link. The
# existing authentication bullet was already bare, so a bare new bullet would
# have doubled a tier-1 finding. Both carry a description, which takes these two
# docs below their previous error count rather than above it.
AUTH_DESC = ('log in and add a management token before running any command')
GUIDE_DESC = 'build and publish your own <span class="code">csdx</span> commands'


def next_steps(auth_url, guide_url, heading="Next Steps"):
    return (f'<h2>{heading}</h2><ul>'
            f'<li><a href="{auth_url}">CLI Authentication and Adding Tokens</a>: '
            f'{AUTH_DESC}.</li>'
            f'<li><a href="{guide_url}">{GUIDE_TITLE}</a>: {GUIDE_DESC}.</li></ul>')


NEXT_V2_OLD = ('<h2>Next Steps</h2><ul><li><a href="/docs/headless-cms/'
               'cli-authentication">CLI Authentication and Adding Tokens</a></li></ul>')
NEXT_V2_NEW = next_steps("/docs/headless-cms/cli-authentication", PLUGINS_V2)

NEXT_V1_OLD = ('<h2>Next Step</h2><ul><li><a href="/docs/headless-cms/'
               'cli-authentication/v1">CLI Authentication and Adding Tokens</a>'
               '</li></ul>')
NEXT_V1_NEW = next_steps("/docs/headless-cms/cli-authentication/v1", PLUGINS_V1)

# The migration guide's Next Steps calls the V2 URL "the V1 CLI". In a V1 to V2
# migration guide the reader wants V2, so the label is corrected rather than the
# link repointed. A plugins-guide row is added in the same replacement.
MIG_NEXT_OLD = (
    '<li><a href="/docs/headless-cms/install-the-cli">Contentstack CLI '
    'documentation</a>: reference documentation for the V1 CLI.</li>'
)
MIG_NEXT_NEW = (
    '<li><a href="/docs/headless-cms/install-the-cli">Contentstack CLI '
    'documentation</a>: reference documentation for the V2 CLI.</li>\n'
    f'<li><a href="{PLUGINS_V2}">{GUIDE_TITLE}</a>: the V2 plugin authoring '
    f'guide, updated for {c("@oclif/core")} v4.</li>'
)


# --- WI-3: the plugin-author checklist -------------------------------------
# Every item is sourced from diffing the V1 and V2 authoring guides, not
# inferred. The V1 guide pins @oclif/core ^3.0.0 with no Contentstack
# dependencies and points oclif.commands at ./src/commands. The V2 guide pins
# ^4.11.14, adds cli-command and cli-utilities at ~2.0.0, and requires
# ./lib/commands.

CHECKLIST_OLD = (
    '<h3>Custom Plugins (Plugin Authors Only)</h3>\n<ol>\n'
    '<li>Update <span class="code">engines.node</span> to '
    '<span class="code">&gt;=22.0.0</span> in your plugin\'s '
    '<span class="code">package.json</span>. (<a href="#nodejs-22">Node.js 22+</a>)'
    '</li>\n</ol>\n'
)
CHECKLIST_NEW = (
    '<h3>Custom Plugins (Plugin Authors Only)</h3>\n<ol>\n'
    '<li>Update <span class="code">engines.node</span> to '
    '<span class="code">&gt;=22.0.0</span> in your plugin\'s '
    '<span class="code">package.json</span>. (<a href="#nodejs-22">Node.js 22+</a>)'
    '</li>\n'
    f'<li>Update {c("@oclif/core")} from {c("^3.0.0")} to {c("^4.11.14")}.</li>\n'
    f'<li>Add {c("@contentstack/cli-command")} and '
    f'{c("@contentstack/cli-utilities")} at {c("~2.0.0")} to your dependencies. '
    f'Import {c("Command")} from {c("@contentstack/cli-command")}, and '
    f'{c("flags")} and {c("Args")} from {c("@contentstack/cli-utilities")}, so '
    'your plugin needs no direct dependency on '
    f'{c("@oclif/core")}.</li>\n'
    f'<li>Point {c("oclif.commands")} at {c("./lib/commands")}, the compiled '
    f'JavaScript output, rather than {c("./src/commands")}. A build step is now '
    'required before linking or installing, and pointing at TypeScript source '
    'makes command discovery fail.</li>\n'
    f'<li>Rewrite your tests if you use {c("@oclif/test")}. Version 4 removed '
    f'the chained {c("test.stdout().command().it()")} API entirely and now '
    f'exports only {c("runCommand")}, {c("captureOutput")} and {c("runHook")}. '
    f'The old API throws {c("TypeError: Cannot read properties of undefined")}.'
    '</li>\n</ol>\n'
    f'<p>For the full authoring workflow, see <a href="{PLUGINS_V2}">'
    f'{GUIDE_TITLE}</a>.</p>\n'
)


# --- The edit plan ---------------------------------------------------------
# (relative path, work item, label, old, new)
EDITS = [
    (INSTALL_V2, "WI-1", "replace the false plugin-guide note",
     NOTE_V2_OLD, note_new(PLUGINS_V2)),
    (INSTALL_V2, "WI-2", "link the plugin guide from Next Steps",
     NEXT_V2_OLD, NEXT_V2_NEW),

    (INSTALL_V1, "WI-1", "replace the false plugin-guide note, V1 target",
     NOTE_V1_OLD, note_new(PLUGINS_V1)),
    (INSTALL_V1, "WI-2", "link the V1 plugin guide, and Next Step to Next Steps",
     NEXT_V1_OLD, NEXT_V1_NEW),

    (MIGRATION, "WI-3", "fill the plugin-author checklist, 1 item to 5",
     CHECKLIST_OLD, CHECKLIST_NEW),
    (MIGRATION, "WI-2", "correct the V1 label and link the plugin guide",
     MIG_NEXT_OLD, MIG_NEXT_NEW),
]


def article_section(entry):
    for block in entry.get("article_content") or []:
        if "article_section" in block:
            return block["article_section"] or {}
    return {}


def main():
    confirm = "--confirm" in sys.argv
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    by_file = {}
    for rel, item, label, old, new in EDITS:
        by_file.setdefault(rel, []).append((item, label, old, new))

    loaded, missed = {}, []
    for rel, edits in by_file.items():
        path = os.path.join(JSON_DIR, rel)
        with open(path, encoding="utf-8") as fh:
            entry = json.load(fh)
        if entry.get("uid") != EXPECTED_UID[rel]:
            sys.exit(f"{rel}: uid is {entry.get('uid')!r}, expected "
                     f"{EXPECTED_UID[rel]!r}. Refusing to edit an unexpected entry.")
        section = article_section(entry)
        html = section.get("content") or ""
        before = len(html)

        print(f"{rel}\n  {entry['uid']}  v{entry.get('_version')}")
        for item, label, old, new in edits:
            if html.count(old) == 1:
                html = html.replace(old, new, 1)
                print(f"    {item}  {label}")
            else:
                n = html.count(old)
                print(f"    {item}  MISSED ({n} matches)  {label}")
                missed.append(f"{rel}: {item} {label}")
        print(f"    content {before} -> {len(html)} chars\n")
        loaded[rel] = (path, entry, section, html)

    if missed:
        print("Unmatched patterns:")
        for m in missed:
            print("  " + m)
        print("\nA miss means the stored HTML has changed since this was written. "
              "Re-read the entry rather than forcing the edit.")

    if not confirm:
        print("Dry run complete. Nothing written.")
        return 0
    if missed:
        sys.exit("Refusing to write with unmatched patterns.")

    for rel, (path, entry, section, html) in loaded.items():
        section["content"] = html
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(entry, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        print(f"wrote {rel}")

    print("\nRegenerating docs/markdown ...")
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts",
                                                 "json_to_markdown.py")], check=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
