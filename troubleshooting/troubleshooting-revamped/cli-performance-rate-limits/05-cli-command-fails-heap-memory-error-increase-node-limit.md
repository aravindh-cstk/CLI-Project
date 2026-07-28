# CLI Command Fails with Heap Memory Error: Increase the Node.js Memory Limit

A CLI operation failed with a heap memory error during execution.

**Root cause**

The CLI runs on Node.js and inherits standard Node.js memory behavior, including the default approximately 4GB V8 heap limit on 64-bit systems. Operations on large datasets can exceed this default limit.

**Resolution**

1. Increase the heap limit using the standard Node.js memory flag, either by invoking the CLI directly:

node --max-old-space-size=8192 <csdx-bin> ...

2. or by setting it as an environment variable before running the command:

NODE_OPTIONS=--max-old-space-size=8192

The CLI supports standard Node.js memory flags, and raising the heap limit resolves memory-related command failures for larger operations.

*Source ticket: Case 53727*
