# Wave D: what was deferred, and why

Wave D had 259 missing-section findings. This records the ones that are not mechanical, so the gap stays a known quantity.

The rule throughout: **omit rather than invent.** A fabricated root cause or a guessed section boundary reads exactly as authoritative as a real one, and the reader cannot tell the difference. A visible hole that the linter keeps reporting is the better outcome.

## Commands and Steps for Execution

| Doc | Section | Why it needs a person |
|---|---|---|
| Compare and Merge Branches Using the CLI, both versions | `Commands` | Five h2 sections named `Steps to ...` cover ten commands between them. Mapping each command to its own h3 is the restructure CMD1 asks for, and it needs someone who knows which command belongs to which step. |
| Generate Typescript Typings with TSGen Plugin, both versions | `Commands` | Carries `Usage` and `Options` rather than a command section. Whether Commands should absorb both, or `Usage` alone becomes Commands with `Options` as its flag table, is an editorial call. |
| Query-based Export, both versions | `Commands` | Has Overview, Prerequisites, Installation, Query Format and Limitations and documents no command section at all. This is missing content, not a missing heading. |
| Bootstrap Starter Apps, both versions | `Steps for Execution` | The band holds four procedure sections plus `Supported Starter Apps`, which is reference material. Wrapping all five under Steps for Execution would file reference content as a step. |
| Create Custom CLI Plugins for Contentstack, both versions | `Steps for Execution` | Twelve h2 sections spanning build, test, publish and plugin management. cli-template-research.md already recommends splitting the cli-utilities API surface out of this doc, so its structure is a Wave E decision. |
| Branches, Migration Use Cases, both versions | `Steps for Execution` | Two h2 sections, each a separate use case with its own procedure. One Steps for Execution spine would have to merge two independent walkthroughs. |
| Migrate Selected Content Using the Query Export Plugin | `Steps for Execution` | Interleaves procedure sections with `Query Format` and `Export Output Structure` reference sections, so the spine is not contiguous. |
| Create Custom CLI Commands | `Steps for Execution` | Being retired. Its step one is `csdx plugins:create`, which has never shipped. Release blt709e2fb5f57c8659 unpublishes it, pending approval. |

## Troubleshooting and Limitations

97 findings, and the least sourceable work in the wave. The cloned plugin sources yield 18 thrown error messages and roughly 120 error call sites in total, spread across 47 docs that need a Troubleshooting section. Some docs have two or three sourceable failures. Some have none.

Each section must use `**Root Cause**` or `**Root Causes**` per `sdk-templates/common-rules.md`, which `checks/troubleshooting-format.js` enforces correctly now that its literal `**Root Cause(s)**` requirement is fixed.

## Next Steps and Examples

99 findings, and the most sourceable. `Next Steps` needs a link plus a one-sentence description per entry, which `C1-06` requires and which the plugin-guide pass showed is worth doing properly: adding bare links there raised the error count until the descriptions went in. Targets come from `cli-url-map.csv` and every one must return 200 before it ships. `Examples` draws on the 58 commands and 360 flags in `notes/reports/flag-inventory.json`.

