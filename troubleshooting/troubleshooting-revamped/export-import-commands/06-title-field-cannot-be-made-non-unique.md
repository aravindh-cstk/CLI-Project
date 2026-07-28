# Title Field Cannot Be Made Non-Unique

The customer asked whether the title field on entries can be configured as non-unique.

**Root cause**

The title field is unique by default in Contentstack and is not configurable to allow non-unique values. The Contentstack platform enforces this behavior server-side as part of the content model constraints, not the CLI, so no CLI command, flag, or script can change or bypass it.

**Resolution**

No configuration change is available for this. If entries need a non-unique display label alongside a unique title, add a separate custom field for that purpose rather than trying to make the title field non-unique.

*Note: This exact question and answer also appears in similar_qs_CLI.csv, indicating it's a recurring question. It was verified against CLI.md directly and does not duplicate any published article there.*

*Source ticket: Case 43563*
