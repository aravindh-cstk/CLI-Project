# Recommended Order for Migrating Content Types Between Stacks

The customer asked for the correct order to follow when migrating content types and entries from one stack to another.

**Root cause**

Migrating modules out of order can cause dependency failures. Content types may reference Marketplace App configurations or global fields that don't yet exist in the target stack.

**Resolution**

1. When importing modules one at a time, follow this sequence: locales, environments, assets, taxonomies, extensions, Marketplace Apps, webhooks, global fields, content types, workflows, entries, labels, then custom roles.

2. Update and configure Marketplace Apps as needed once they're imported, since content types import right after them and may depend on their configuration.

3. Import global fields and content types next, then workflows, then entries, and finish with labels and custom roles.

`csdx cm:stacks:import` applies this order automatically when you run it without `--module`. If you import modules one at a time using `--module`, that automatic sequencing is skipped, so you need to follow this order yourself.

Following this order avoids dependency errors, and all modules migrate into the target stack correctly.

*Source ticket: Case 43220*
