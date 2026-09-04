#!/usr/bin/env python3
"""Revert the 25 Next Steps sections Wave D tier 2a added (commit c9e72d3).

The docs owner decided Next Steps should not be a required CLI section: 16 CLI
docs already had a hand-written Next Steps section before this project touched
anything, and generating one for the rest turned out to read as padding rather
than as guidance. Those 16 pre-existing sections stay. Only the 25 this project
added are removed.

Does not blindly `git checkout` the pre-c9e72d3 JSON, because 14 of these 25
files were edited again by later waves (flag-table reshapes, Node.js fixes,
link fixes). A blind revert would also undo that later work. Instead each
file's current HTML is loaded and only the `Next Steps` H2 block (heading plus
everything up to the next H2) is removed, exactly the "drop" operation
apply_wave_b.py already uses.

Usage:
  python3 scripts/revert_wave_d2_next_steps.py            # dry run
  python3 scripts/revert_wave_d2_next_steps.py --confirm  # write
"""

import sys

sys.path.insert(0, "scripts/lib")
from docs_html import Doc, norm_text  # noqa: E402

TARGETS = [
    "docs/json/Version 1.x.x/CLI Advanced Operations/Change Master Locale.json",
    "docs/json/Version 1.x.x/CLI Advanced Operations/Entry Migration | V1.x.x.json",
    "docs/json/Version 1.x.x/CLI Advanced Operations/Update Missing Reference UIDs for Entries, Assets, and Extensions.json",
    "docs/json/Version 1.x.x/CLI Commands/Audit Plugin | V1.x.x.json",
    "docs/json/Version 1.x.x/CLI Commands/Bulk Publish and Unpublish Content | V1.x.x.json",
    "docs/json/Version 1.x.x/CLI Commands/CLI-Supported Features for Export, Import, and Clone Operations | V1.x.x.json",
    "docs/json/Version 1.x.x/CLI Commands/Cloning a Stack | V1.x.x.json",
    "docs/json/Version 1.x.x/CLI Commands/Compare and Merge Branches Using the CLI | V1.x.x.json",
    "docs/json/Version 1.x.x/CLI Commands/Overwrite Existing Content using CLI Import | V1.x.x.json",
    "docs/json/Version 1.x.x/Get Started with CLI/Configure Regions in the CLI | V1.x.x.json",
    "docs/json/Version 1.x.x/Migration Use Cases/Branches | Migration Use Cases | V1.x.x.json",
    "docs/json/Version 1.x.x/Migration Use Cases/Migrate Content Between Stacks Using the CLI | V1.x.x.json",
    "docs/json/Version 1.x.x/Miscellaneous/CLI Limitations | V1.x.x.json",
    "docs/json/Version 1.x.x/Miscellaneous/Contentstack CLI Configuration Reference.json",
    "docs/json/Version 2.x.x/CLI Advanced Operations V2/Change Master Locale.json",
    "docs/json/Version 2.x.x/CLI Advanced Operations V2/Entry Migration | V2.x.x.json",
    "docs/json/Version 2.x.x/CLI Advanced Operations V2/Update Missing Reference UIDs for Entries, Assets, and Extensions.json",
    "docs/json/Version 2.x.x/CLI Commands V2/CLI-Supported Features for Export, Import, and Clone Operations | V2.x.x.json",
    "docs/json/Version 2.x.x/CLI Commands V2/Cloning a Stack | V2.x.x.json",
    "docs/json/Version 2.x.x/CLI Commands V2/Compare and Merge Branches Using the CLI | V2.x.x.json",
    "docs/json/Version 2.x.x/CLI Commands V2/Export Content Using the CLI | V2.x.x.json",
    "docs/json/Version 2.x.x/CLI Commands V2/Import Content Using the CLI | V2.x.x.json",
    "docs/json/Version 2.x.x/CLI Commands V2/Overwrite Existing Content using CLI Import | V2.x.x.json",
    "docs/json/Version 2.x.x/CLI Migration Use Cases V2/Branches | Migration Use Cases | V2.x.x.json",
    "docs/json/Version 2.x.x/CLI Migration Use Cases V2/Migrate Content Between Stacks Using the CLI | V2.x.x.json",
]


def block(heading):
    out = [heading]
    node = heading.next_sibling
    while node is not None:
        name = getattr(node, "name", None)
        if name in ("h1", "h2"):
            break
        out.append(node)
        node = node.next_sibling
    return out


def main():
    confirm = "--confirm" in sys.argv
    print("LIVE RUN\n" if confirm else "DRY RUN, pass --confirm to write\n")

    written, skipped = 0, 0
    for rel in TARGETS:
        doc = Doc.load(rel)
        h2s = doc.soup.find_all("h2")
        target = None
        for h in h2s:
            if norm_text(h.get_text()) == "Next Steps":
                target = h
                break
        if target is None:
            print(f"  SKIP  (no Next Steps heading)  {doc.rel}")
            skipped += 1
            continue
        for node in block(target):
            node.extract()
        if doc.save(dry_run=not confirm):
            print(f"  {'wrote' if confirm else 'would write'}  {doc.rel}")
            written += 1
        else:
            print(f"  no change  {doc.rel}")

    print(f"\n{written} file(s) {'written' if confirm else 'would change'}, "
          f"{skipped} skipped.")


if __name__ == "__main__":
    main()
