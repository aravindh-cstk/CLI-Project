# Wave E: what was deferred, and why

## The MOD1 heading renames

`MOD1a` asks a module reference to name each command or module with its real identifier verbatim, so `Export Module Limitations` would become `cm:stacks:export`. Not done, on purpose.

Renaming those headings rewrites 20 anchor ids on each CLI Limitations page, and three inbound links already point into those sections:

```
cli-limitations/v1#import-module-limitations
cli-limitations/v1#export-module-limitations
cli-limitations#bulk-publishunpublish-limitations
```

The third of those is already broken. The live page renders `bulk-publish-unpublish-limitations`, with a hyphen where the link has none, which is the clearest available proof that anchor ids are generated at render time and cannot be derived. Renaming headings before Wave F has re-baselined the anchors would break two working links in order to satisfy a naming rule.

The right order is Wave F first, then MOD1, with every rename verified against the re-rendered page.

## Splitting the cli-utilities API surface

`notes/others/cli-template-research.md` recommends lifting the `@contentstack/cli-utilities` API reference out of `Create Custom CLI Plugins for Contentstack | V2.x.x` into its own module reference. That creates a new page and therefore a new URL, so it needs a slug and a nav placement decision before it can be written.

## The Configuration Reference

It carries a trailing `Quick Reference Guide` holding performance-tuning JSON, which is not the index table `Quick Reference` means. Renaming it would satisfy the linter by mislabelling the content. Its remaining errors are almost entirely `CLI-01`: it is over 1,100 lines of option tables in a shape the standard does not recognise, and converting those tables is a job of its own.

## A broken in-page anchor found while building the tables

`CLI Limitations | V1.x.x` line 533 carries:

```
See [Asset Scan In-Queue Assets Are Not Retried](#asset-scan-in-queue-assets-are-not-retried)
```

No heading of that name exists anywhere on the page, at any level, and the link predates this wave. It resolves to nothing.

Left for Wave F, which is the link and anchor pass, but recorded here so it is not lost. The fix needs a person: either the section it points at was never written, or it lives on a different page and the link should carry that page's URL.

## The Node.js requirement was wrong, and this was the fix

Both CLI Limitations pages claimed `Node.js version 18.0.0 or above (recommended: 20.x or 22.x)`, in three places each: the Limitation line, the Impact line and the Workaround bullet. Checked against each published package's own `engines` field:

| Release | `engines.node` |
|---|---|
| 1.40.0 through 1.60.0 | `>=14.0.0` |
| 1.65.0 and 1.68.0 | `>=22.0.0` |
| 2.0.0 | `>=22.0.0` |

18 was never the floor for any release. This is user breaking rather than untidy: a reader on Node 18 or 20 follows the page, installs, and the CLI fails at runtime with the `EBADENGINE` behaviour the V1-to-V2 migration guide already warns about.

Fixing only the Limitation and Impact lines left `18.0.0+` standing three lines below the correction, in the Workaround bullet. All three places are corrected now, and the script that does it fixes all three so a re-run cannot reintroduce the mismatch.
