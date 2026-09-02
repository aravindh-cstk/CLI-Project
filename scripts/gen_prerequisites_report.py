#!/usr/bin/env python3
"""WI-5: check each CLI doc's Prerequisites against what the code actually requires.

Read-only. Reads the GA state from the `v2.0.0` git tag rather than from the working
tree, because the working tree sits on branch v2-dev behind the GA release. Nothing
is checked out and no branch is changed.

Usage:
  python3 scripts/gen_prerequisites_report.py
"""

import collections
import glob
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "docs", "markdown")
CORE = os.path.join(ROOT, "repo", "cli-core")
PLUGINS = os.path.join(ROOT, "repo", "cli-plugins")
OUT = os.path.join(ROOT, "notes", "reports", "cli-prerequisites-report.md")
GA_TAG = "v2.0.0"


def git_show(repo, ref, path):
    p = subprocess.run(["git", "-C", repo, "show", f"{ref}:{path}"],
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def git_ls(repo, ref, pattern):
    p = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", ref],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return []
    return [l for l in p.stdout.splitlines() if re.search(pattern, l)]


def bundled_at_ga():
    src = git_show(CORE, GA_TAG, "packages/contentstack/package.json")
    d = json.loads(src)
    return d["version"], d["engines"]["node"], set(
        p for p in d["oclif"]["plugins"] if p.startswith("@contentstack/")
    )


def command_inventory():
    """command id -> npm package name, from the GA tag for core and the working tree
    for the plugins monorepo, which carries no v2.0.0 tag."""
    inv = {}

    def add(files, pkg_json_getter, repo_label):
        for f in files:
            m = re.match(r"packages/([^/]+)/src/commands/(.+)\.ts$", f)
            if not m:
                continue
            pkg_dir, cmd_path = m.group(1), m.group(2)
            if cmd_path.endswith("/index"):
                cmd_path = cmd_path[: -len("/index")]
            cmd = cmd_path.replace("/", ":")
            name = pkg_json_getter(pkg_dir)
            if name:
                inv[cmd] = (name, repo_label)

    core_files = git_ls(CORE, GA_TAG, r"packages/[^/]+/src/commands/.*\.ts$")

    def core_pkg(pkg_dir):
        src = git_show(CORE, GA_TAG, f"packages/{pkg_dir}/package.json")
        return json.loads(src)["name"] if src else None

    add(core_files, core_pkg, "cli-core@" + GA_TAG)

    plug_files = [
        os.path.relpath(p, PLUGINS)
        for p in glob.glob(PLUGINS + "/packages/*/src/commands/**/*.ts", recursive=True)
    ]

    def plug_pkg(pkg_dir):
        pj = os.path.join(PLUGINS, "packages", pkg_dir, "package.json")
        if not os.path.exists(pj):
            return None
        return json.load(open(pj))["name"]

    add(plug_files, plug_pkg, "cli-plugins working tree")
    return inv


def doc_commands(path, inv):
    """Commands a doc documents.

    Single-word command ids need a command context to count. The inventory holds ids
    like `app`, `tsgen`, and `plugins`, and a bare word-boundary search for `app`
    matches the English word in any doc that mentions an app, which produced 12 false
    "missing install step" findings on the first run. So a colon-bearing id is
    unambiguous and matched bare, while a single-word id must appear either after
    `csdx` or inside backticks.
    """
    text = open(path, encoding="utf-8").read()
    found = []
    for cmd in sorted(inv, key=len, reverse=True):
        esc = re.escape(cmd)
        if ":" in cmd:
            hit = re.search(r"\b" + esc + r"\b", text)
        else:
            hit = re.search(r"csdx\s+" + esc + r"\b", text) or re.search(
                r"`" + esc + r"(\s[^`]*)?`", text
            )
        if not hit:
            continue
        # Skip an id that is only a prefix of a longer id already recorded.
        if any(cmd != o and o.startswith(cmd + ":") for o in found):
            continue
        found.append(cmd)
    return found


def prereq_block(path):
    """The Prerequisites section's bullet text, and the heading level it sits at."""
    lines = open(path, encoding="utf-8").read().split("\n")
    level, start = None, None
    for i, l in enumerate(lines):
        m = re.match(r"^(#{2,6})\s+Prerequisites?\s*$", l.strip())
        if m:
            level, start = len(m.group(1)), i
            break
    if start is None:
        return None, None, []
    items = []
    for l in lines[start + 1:]:
        if re.match(r"^#{1,6}\s", l):
            break
        if re.match(r"^\s*[-*]\s+", l):
            items.append(l.strip())
    return level, start + 1, items


def main():
    ga_version, ga_node, bundled = bundled_at_ga()
    inv = command_inventory()
    files = sorted(
        f for f in glob.glob(MD + "/**/*.md", recursive=True)
        if "/Version 2" in f
    )

    rows = []
    for f in files:
        cmds = doc_commands(f, inv)
        pkgs = sorted({inv[c][0] for c in cmds})
        external = sorted(p for p in pkgs if p not in bundled)
        body = open(f, encoding="utf-8").read()
        level, line, items = prereq_block(f)
        says_install = bool(re.search(r"\bplugins:install\b", body))
        joined = " ".join(items).lower()
        rows.append({
            "file": os.path.relpath(f, MD),
            "cmds": cmds, "pkgs": pkgs, "external": external,
            "level": level, "line": line, "items": items,
            "says_install": says_install,
            "has_login": "cli-authentication" in joined or "authenticated" in joined,
            "has_install": "install-the-cli" in joined or "installed" in joined,
            "has_region": "region" in joined,
            "has_account": "login" in joined and "contentstack" in joined,
        })

    L = []
    A = L.append
    A("# CLI Prerequisites Accuracy Report")
    A("")
    A("WI-5 of the CLI Structure Review. Checks each V2 doc's Prerequisites against what "
      "the code actually requires, rather than against what the prose already claims.")
    A("")
    A("Reproduce with:")
    A("")
    A("```bash")
    A("python3 scripts/gen_prerequisites_report.py")
    A("```")
    A("")
    A("## Versions this was checked against")
    A("")
    A("| Fact | Value | Source |")
    A("|---|---|---|")
    A(f"| V2 GA version | **{ga_version}** | `v2.0.0` git tag, `packages/contentstack/package.json` |")
    A("| V2 GA release date | **2026-08-13** | `changelog/2.x/cli-2.0.0.md` |")
    A(f"| Node requirement | **{ga_node}** | same `package.json`, `engines.node` |")
    A("| Latest V1 | **1.66.0**, released 2026-07-27 | `changelog/1.x/cli-1.66.0.md` |")
    A("")
    A("**On the source used.** The working trees for `repo/cli-core` and "
      "`repo/cli-plugins` sit on branch `v2-dev` at 2026-08-05 and 2026-07-25, both behind "
      "the 2026-08-13 GA release. Rather than pull and hope, core facts here are read "
      "from the `v2.0.0` tag, which is exact. Nothing was checked out and no branch was "
      "changed. The plugins monorepo carries no `v2.0.0` tag, so its command inventory "
      "comes from the working tree, and every flag-level claim below is cross-checked "
      "against `changelog/2.x/cli-2.0.0.md` instead.")
    A("")
    A("---")
    A("")
    A("## The baseline every command doc needs")
    A("")
    A("From `repo/cli-core/packages/contentstack-command/src/index.ts`, the base class "
      "every command extends:")
    A("")
    A("- It throws `You are not logged in. Run the command: $ csdx auth:login` when no "
      "email is configured.")
    A("- It exits when no region is configured, printing "
      "`Error: Region not configured. Please set the region with command "
      "$ csdx config:set:region`.")
    A("")
    A("So the minimum for **every** doc that runs a command is four items: a Contentstack "
      "account, the CLI installed, an authenticated session, and a configured region. A "
      "command taking `--alias` needs a fifth, a management token added with "
      "`csdx auth:tokens:add`.")
    A("")
    A("Region is the one most often missing. It is not optional for non-North-America "
      "stacks, and `common-rules.md` is explicit that a conditional requirement like this "
      "is Mandatory stated conditionally, never Optional.")
    A("")
    A("---")
    A("")
    A("## Bundled versus external plugins at GA")
    A("")
    A("This is the highest-value finding in the report, and it is mechanically decidable. "
      "A doc for a bundled plugin must not tell the reader to install anything. A doc for "
      "an external plugin must, or the command fails as `command not found`.")
    A("")
    A(f"**Bundled at GA ({len(bundled)} Contentstack plugins),** from `oclif.plugins`:")
    A("")
    for p in sorted(bundled):
        A(f"- `{p}`")
    A("")
    A("**External, requiring `csdx plugins:install`:**")
    A("")
    seen_ext = sorted({p for r in rows for p in r["external"]})
    for p in seen_ext:
        A(f"- `{p}`")
    A("")
    A("The GA changelog confirms two of these moved out of the bundle at GA rather than "
      "having always been external: `@contentstack/cli-launch` "
      "(\"Made the `launch` plugin opt-in, it is no longer bundled\") and "
      "`@contentstack/cli-cm-migrate-rte` (\"Made the RTE migration available as a "
      "separate, opt-in plugin\"). GA also added a guided install prompt for both instead "
      "of a bare `command not found`, which is itself documentable behavior that no doc "
      "currently mentions.")
    A("")
    A("---")
    A("")
    A("## Findings")
    A("")

    missing_pre = [r for r in rows if r["level"] is None]
    wrong_level = [r for r in rows if r["level"] and r["level"] != 2]
    ext_no_install = [r for r in rows if r["external"] and not r["says_install"]]
    bundled_says_install = [
        r for r in rows if not r["external"] and r["says_install"] and r["pkgs"]
    ]
    no_region = [r for r in rows if r["items"] and not r["has_region"]]

    A("### No Prerequisites section at any level")
    A("")
    if missing_pre:
        A("| Doc | Commands it documents |")
        A("|---|---|")
        for r in missing_pre:
            A("| `%s` | %s |" % (
                r["file"].replace("|", "\\|").replace(".md", ""),
                ", ".join("`%s`" % c for c in r["cmds"][:4]) or "none"))
        A("")
        A("A doc with no commands and no Prerequisites is defensible: it runs nothing. A "
          "doc that documents a command and has no Prerequisites is not, because the base "
          "class will reject the reader before the command starts.")
    else:
        A("None.")
    A("")

    A("### Prerequisites present but not at H2")
    A("")
    if wrong_level:
        A("| Doc | Level | Line |")
        A("|---|---|---|")
        for r in wrong_level:
            A("| `%s` | H%d | %d |" % (
                r["file"].replace("|", "\\|").replace(".md", ""), r["level"], r["line"]))
        A("")
        A("These are nested under another section. The section-order check reads H2 text "
          "only, so these register as absent rather than as misplaced, and the two need "
          "different fixes. At H4 the heading also gets no anchor id and no navigation "
          "entry.")
    else:
        A("None.")
    A("")

    A("### External plugin documented with no install instruction")
    A("")
    if ext_no_install:
        A("| Doc | External package | Needs |")
        A("|---|---|---|")
        for r in ext_no_install:
            A("| `%s` | %s | `csdx plugins:install %s` |" % (
                r["file"].replace("|", "\\|").replace(".md", ""),
                ", ".join("`%s`" % p for p in r["external"]),
                r["external"][0]))
        A("")
        A("Each of these documents a command that is not in the GA bundle, without telling "
          "the reader to install it. A reader following the doc gets `command not found`.")
        A("")
        A("The `Contentstack CLI Configuration Reference` case is the softest of these. It "
          "is a module reference, and MOD3 deliberately gives that type no Prerequisites "
          "or Installation section. The right fix is not to add an install step to the "
          "reference, it is to make the `cm:stacks:export-query` entry link to "
          "`Query-based Export`, which carries the install step.")
    else:
        A("None.")
    A("")
    A("### Verified non-findings")
    A("")
    A("Recorded so they are not re-raised. Each looks like a defect and is not.")
    A("")
    A("- **`CLI for CS Assets | V2.x.x` needs no `plugins:install`.** "
      "`@contentstack/cli-asset-management` is absent from the GA bundle and is an oclif "
      "package, so it looks external. It ships no commands of its own: its `src/` holds "
      "`export`, `import`, `import-setup`, and `query-export` library code that the "
      "bundled export and import plugins consume. The GA changelog matches, recording "
      "\"Added AM 2.0 export support\" under `cli-cm-export` rather than a new command "
      "namespace. The doc correctly drives AM 2.0 through `cm:stacks:export` and "
      "`cm:stacks:import`, both bundled. This doc is also the strongest Prerequisites "
      "section in the corpus, with Mandatory and Optional subsections and a specific, "
      "verifiable list.")
    A("- **The five external plugin docs already carry their install step.** "
      "`Apps CLI Plugin`, `Content Type Plugin`, `Regex Validate Plugin`, "
      "`Generate Typescript Typings with TSGen Plugin`, and `CLI for Launch` each "
      "reference `csdx plugins:install`. `CLI for Launch` matters most, because the "
      "changelog shows `launch` only left the bundle at GA, so that doc has kept pace.")
    A("")

    A("### Bundled plugin with a spurious install instruction")
    A("")
    if bundled_says_install:
        A("| Doc | Bundled packages |")
        A("|---|---|")
        for r in bundled_says_install:
            A("| `%s` | %s |" % (
                r["file"].replace("|", "\\|").replace(".md", ""),
                ", ".join("`%s`" % p for p in r["pkgs"][:3])))
        A("")
        A("These mention `plugins:install` while documenting only bundled commands. Verify "
          "each one: some legitimately reference installing a different plugin, which is "
          "fine, and the rest are telling readers to install something they already have.")
    else:
        A("None.")
    A("")

    A("### Prerequisites that omit region configuration")
    A("")
    if no_region:
        A(f"{len(no_region)} docs have a Prerequisites list that never mentions region.")
        A("")
        A("| Doc | Items | Has account | Has install | Has auth |")
        A("|---|---|---|---|---|")
        for r in no_region:
            A("| `%s` | %d | %s | %s | %s |" % (
                r["file"].replace("|", "\\|").replace(".md", ""), len(r["items"]),
                "yes" if r["has_account"] else "no",
                "yes" if r["has_install"] else "no",
                "yes" if r["has_login"] else "no"))
        A("")
        A("The base class exits without a configured region, so for any reader on a "
          "non-North-America stack this is a blocking requirement that the doc does not "
          "state. State it conditionally rather than marking it Optional.")
    else:
        A("None.")
    A("")
    A("---")
    A("")
    A("## GA changes the docs have not caught up with")
    A("")
    A("From `changelog/2.x/cli-2.0.0.md`. These are content-accuracy findings rather than "
      "prerequisites, and each names the doc to check.")
    A("")
    A("| GA change | Doc to check |")
    A("|---|---|")
    A("| Short flags removed in favour of long-form only, across export, import, tsgen "
      "(`-o`, `-p`, `-d`), content-type, migration, external-migrate | `Export Content "
      "Using the CLI` still documents a `Short Flag` column with `-k` and `-a`. Check each "
      "of the six. Note `apps-cli` went the other way and **added** `-k` |")
    A("| `--api-version` removed from `cm:stacks:bulk-entries` and "
      "`cm:stacks:bulk-taxonomies` | `Bulk Operations in CLI` |")
    A("| tsgen `--token-alias` renamed to `--alias` | `Generate Typescript Typings with "
      "TSGen Plugin` |")
    A("| New `auth:tokens:list` command and `auth:tokens` namespace | `CLI Authentication "
      "and Adding Tokens` |")
    A("| New `--cs-assets` and `--auth-api` flags on `config:set:region` | `Configure "
      "Regions in the CLI` |")
    A("| New `--skip-taxonomy-publish` on import, and taxonomies now auto-republish after "
      "import | `Import Content Using the CLI` |")
    A("| Export output is now a flat directory, global fields export one file per item, "
      "content type schema JSON export removed, main branch exported by default when "
      "`--branch` is empty | `Export Content Using the CLI` |")
    A("| New command `cm:stacks:bulk-taxonomies` | No doc owns it. Check `Bulk Operations "
      "in CLI` |")
    A("| `@contentstack/cli-asset-management` reached 1.0.0 at GA (AM 2.0: spaces, "
      "workspaces, fields, asset types, OAuth) | `CLI for CS Assets` |")
    A("")
    A("---")
    A("")
    A("## Commands with no owning doc")
    A("")
    documented = set()
    for r in rows:
        documented.update(r["cmds"])
    orphan_cmds = sorted(set(inv) - documented)
    A(f"{len(orphan_cmds)} of {len(inv)} known commands are not mentioned in any V2 doc.")
    A("")
    A("| Command | Package |")
    A("|---|---|")
    for c in orphan_cmds:
        A(f"| `{c}` | `{inv[c][0]}` |")
    A("")
    A("---")
    A("")
    A("## Per-doc detail")
    A("")
    A("| Doc | Prereq level | Items | Commands | External packages |")
    A("|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: x["file"]):
        A("| `%s` | %s | %d | %d | %s |" % (
            r["file"].replace("|", "\\|").replace(".md", ""),
            ("H%d" % r["level"]) if r["level"] else "**none**",
            len(r["items"]), len(r["cmds"]),
            ", ".join("`%s`" % p for p in r["external"]) or "none"))
    A("")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(L) + "\n")
    print("wrote", OUT)
    print("GA", ga_version, "node", ga_node, "| bundled", len(bundled),
          "| commands known", len(inv))
    print("docs:", len(rows), "| no prereq:", len(missing_pre),
          "| wrong level:", len(wrong_level),
          "| external-no-install:", len(ext_no_install),
          "| no region:", len(no_region),
          "| undocumented commands:", len(orphan_cmds))


if __name__ == "__main__":
    main()
