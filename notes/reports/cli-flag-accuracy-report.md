# CLI Flag Accuracy Report

What the V2 docs say about flags, checked against what CLI 2.0.0 ships.

Ground truth is the `oclif.manifest.json` inside each published npm tarball, collected by `scripts/gen_flag_inventory.py`. The local repo is not used: `repo/cli-plugins` sits on `v2-dev` with no `v2.0.0` tag, and its export plugin is still at `2.0.0-beta.24`.

Reproduce with:

```bash
python3 scripts/gen_flag_inventory.py
python3 scripts/gen_flag_accuracy_report.py
```

## Summary

| Finding | Count | What it costs a reader |
|---|---|---|
| `GHOST` | 0 | Copies a flag that does not exist. The command fails. |
| `FOREIGN` | 0 | Table mixes another command's flags in without saying so. |
| `SWAPPED` | 0 | Uses a real flag for the wrong purpose. Fails in a way that looks like their mistake. |
| `MISSING` | 0 | Cannot discover a flag the command supports. |

10 docs were tied to a single command and checked. 9 could not be scoped to one command. 0 document a plugin that publishes no manifest, so no GA flag data exists for them.

---

## The defect class this report cannot catch

Every check here compares flag **names**. One defect class escapes that entirely: a flag that keeps its name and changes its meaning.

`cm:stacks:migration --config` is the only instance in the CLI surface. In V1 it took inline configuration. In 2.0.0 it takes the path of a JSON configuration file, and inline configuration moved to the new `--inline-config` flag. A name diff sees no change, and neither does a reader: a V1 script passing inline values still parses, and GA reads the string as a file path rather than failing.

It was found by diffing flag **descriptions** between the last 1.x manifest and 2.0.0, not by diffing names. Re-run that comparison after any major version, because it is the only thing that surfaces this class. CLI-C11 states the rule.

---

## Findings

---

## Coverage

| Doc | Scoped to | Flags documented | Flags at GA |
|---|---|---|---|
| `Version 2.x.x/CLI Commands V2/Audit Plugin \| V2.x.x.md` | `documents 4 commands, not scoped` | - | - |
| `Version 2.x.x/CLI Commands V2/Bulk Operations in CLI \| V2.x.x.md` | `documents 3 commands, not scoped` | - | - |
| `Version 2.x.x/CLI Commands V2/CLI-Supported Features for Export, Import, and Clone Operations \| V2.x.x.md` | `documents 4 commands, not scoped` | - | - |
| `Version 2.x.x/CLI Commands V2/Cloning a Stack \| V2.x.x.md` | `cm:stacks:clone` | 14 | 14 |
| `Version 2.x.x/CLI Commands V2/Compare and Merge Branches Using the CLI \| V2.x.x.md` | `documents 10 commands, not scoped` | - | - |
| `Version 2.x.x/CLI Commands V2/Configure CLI Logging Preferences \| V2.x.x.md` | `config:set:log` | 3 | 3 |
| `Version 2.x.x/CLI Commands V2/Configure Early Access in the CLI \| V2.x.x.md` | `documents 3 commands, not scoped` | - | - |
| `Version 2.x.x/CLI Commands V2/Content Type Plugin \| V2.x.x.md` | `documents 10 commands, not scoped` | - | - |
| `Version 2.x.x/CLI Commands V2/Export Content Using the CLI \| V2.x.x.md` | `cm:stacks:export` | 10 | 11 |
| `Version 2.x.x/CLI Commands V2/Import Content Using the CLI \| V2.x.x.md` | `cm:stacks:import` | 18 | 18 |
| `Version 2.x.x/CLI Commands V2/Overwrite Existing Content using CLI Import \| V2.x.x.md` | `documents 2 commands, not scoped` | - | - |
| `Version 2.x.x/Content Migration Commands V2/Export Content to CSV File Using the CLI \| V2.x.x.md` | `cm:export-to-csv` | 14 | 14 |
| `Version 2.x.x/Content Migration Commands V2/Import Content Using the Seed Command \| V2.x.x.md` | `cm:stacks:seed` | 6 | 7 |
| `Version 2.x.x/Content Migration Commands V2/Migrate your Content using the CLI Migration Command \| V2.x.x.md` | `cm:stacks:migration` | 7 | 7 |
| `Version 2.x.x/Get Started with CLI V2/CLI Authentication and Adding Tokens \| V2.x.x.md` | `documents 7 commands, not scoped` | - | - |
| `Version 2.x.x/Get Started with CLI V2/Configure Regions in the CLI \| V2.x.x.md` | `config:set:region` | 10 | 10 |
| `Version 2.x.x/Get Started with CLI V2/Migrate from Contentstack CLI V1 to V2 \| V2.x.x.md` | `documents 31 commands, not scoped` | - | - |
| `Version 2.x.x/Miscellaneous V2/Bootstrap Starter Apps \| V2.x.x.md` | `cm:bootstrap` | 8 | 8 |
| `Version 2.x.x/Miscellaneous V2/Configure Rate Limits in the CLI \| V2.x.x.md` | `config:set:rate-limit` | 4 | 4 |

