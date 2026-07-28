# UI JSON Import Creates Only One Entry Even with Multiple Records in the File

The customer tried to import 500+ entries of the same content type using a single JSON file through the Contentstack UI's entry import option, but only one empty entry was created.

**Root cause**

This is expected behavior, not a bug. The Contentstack UI entry importer supports only a single entry per JSON file. It is not designed for bulk multi-record import.

**Resolution**

1. For bulk entry creation, use the Content Management API to programmatically create entries. This is the preferred approach for scalability.

2. Alternatively, use the Contentstack CLI, which supports bulk import through a structured export/import format.

Bulk entry creation succeeds using either the Content Management API or the CLI. The UI's JSON importer remains limited to one entry per file by design.

*Source ticket: Case 56501*
