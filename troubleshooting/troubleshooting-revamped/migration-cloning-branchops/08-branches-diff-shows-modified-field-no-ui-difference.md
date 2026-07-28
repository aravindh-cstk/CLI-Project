# cm:branches:diff Shows a Field as Modified with No Visible UI Difference

Running cm:branches:diff to compare the prod and main branches showed a modification in a content type's URL field, but manually reviewing both branches in the UI showed no visible difference.

**Root cause**

`cm:branches:diff` only supports two `--format` values: `compact-text` (the default) and `detailed-text`. There is no "summary" format. With `compact-text`, the CLI only lists which content types or global fields were added, deleted, or modified. With `detailed-text`, the CLI fetches a per-field comparison for each modified item and renders the field-level differences, which is a finer-grained diff than the coarse added/deleted/modified list.

The CLI itself does not invent or compute any extra metadata comparison. It renders whatever field-level differences the comparison returns for that content type. So a field showing as modified in `detailed-text` with no visible UI difference means the comparison considered something about that field different, which can include non-visual properties such as field order or internal attributes that the standard schema UI doesn't render. Field reordering, or a difference in an internal attribute the comparison tracks but the schema UI doesn't display, can both produce this symptom.

**Resolution**

1. When `cm:branches:diff --format detailed-text` reports a change with no visible UI difference, treat it as a field-level difference in the comparison rather than a CLI defect.

2. If only the coarse list of added, deleted, or modified content types/global fields matters for your review, use the default `compact-text` format (or omit `--format` entirely) instead of `detailed-text`.

Understanding that `detailed-text` fetches and displays a per-field diff, while `compact-text` only lists which items changed, explains the discrepancy between the CLI diff output and the UI's schema view. The two real `--format` options are `compact-text` and `detailed-text`, there is no separate "summary" format.

*Source ticket: Case 53530*
