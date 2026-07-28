---
uid: "blt4f27fd89adf6b6c1"
seo_title: "Create Custom CLI Plugins for Contentstack | Contentstack"
seo_description: "Learn how to build, test, and publish custom CLI plugins for Contentstack using oclif. Covers setup, development workflow, and best practices."
---

# Create Custom CLI Plugins for Contentstack

This guide explains how to develop an external plugin for [Contentstack CLI](https://www.contentstack.com/docs/headless-cms/install-the-cli), including requirements, project structure, best practices, testing, publishing steps, and key internal behaviors to consider.

## Introduction

The Contentstack CLI supports modular extensibility through external plugins.

These plugins offer the following capabilities:

- Extend CLI functionality with custom commands.
- Allow global (system-wide) or local (project-specific) installation.
- Integrate with the [oclif framework](https://oclif.io/) for structured command development.

**Example plugin**: `@contentstack/apps-cli`

## Prerequisites

- [Node.js version 22.x and above](https://nodejs.org/en/download/)
- [Contentstack account](https://www.contentstack.com/login/)
- Familiarity with the oclif CLI framework (recommended)
- Contentstack CLI [installed](/docs/headless-cms/install-the-cli)

## Plugin Structure

A well-organized plugin should follow the recommended directory layout:

```
my-plugin/
├── src/
│   └── commands/
│       └── mycommand.ts
├── test/
│   └── commands/
│       └── mycommand.test.ts
├── .eslintrc.js
├── package.json
├── tsconfig.json
├── README.md
└── oclif.manifest.json
```

> **Note:** Use namespacing to prefix all commands to avoid collision. For example, use `csdx myplugin:do` instead of `csdx do`.

## Creating a Plugin

Use oclif's generator to create your plugin:

```
npx oclif generate myplugin
cd myplugin
```

The generator prompts you with the following questions:

1. **Select a module type**: Choose `ESM` or `CommonJS`.
2. **NPM package name**: Example: `@contentstack/myplugin` or `myplugin`
3. **Command bin name the CLI will export**: Example: `myplugin` (this is the binary name, not the full command namespace)
4. **Description**: Example: `A new CLI generated with oclif`
5. **Author**: Example: `Contentstack` or your organization name
6. **License**: Default: `MIT`
7. **Who is the GitHub owner of repository**: Example: `@contentstack`
8. **What is the GitHub name of repository**: Example: `myplugin`
9. **Select a package manager**: Choose: `npm`, `yarn`, or `pnpm`

After answering these prompts, the generator creates the plugin structure in your current directory.

### Configure package.json

Modify the generated `package.json` to include the necessary oclif configuration:

```
{
  "name": "myplugin",
  "version": "1.0.0",
  "oclif": {
    "plugins": [],
    "commands": "./src/commands"
  },
  "dependencies": {
    "@oclif/core": "^3.0.0"
  }
}
```

### Move to plugin-directory

```
cd <plugin-directory>
// Example:
cd ./myplugin
```

### Generate a command

```
npx oclif generate command myplugin:do
```

This creates `src/commands/myplugin/do.ts`.

### Build the plugin

Before linking or using your plugin, you must build it to compile TypeScript to JavaScript:

```
npm run build
```

This command compiles your TypeScript commands from `src/commands/` to `dist/commands/`.

During development, oclif reads from `src`. When published, the CLI loads compiled commands from `dist` (based on your build settings).

### Generate the manifest

After building the plugin, generate the oclif manifest file by running the following command:

```
npx oclif manifest
```

This command creates the `oclif.manifest.json` file, which is required for the CLI to discover your commands.

## Plugin Registration and Linking

When developing a plugin locally, you must link it to the Contentstack CLI for testing:

```
cd <plugin-directory>
csdx plugins:link
```

This sets up the plugin within the `csdx` namespace, allowing you to use your custom commands directly.

### Verify the Setup

Test that your plugin is properly linked by running the following command:

```
csdx myplugin:do
```

You should see your plugin's output in the terminal.

### Development Workflow

During development, you can use the development mode, which automatically transpiles TypeScript as you make changes.

Alternatively, run the plugin directly using Node.js:

```
node bin/run myplugin:do
```

> **Tip:** After making changes to your plugin, rebuild and regenerate the manifest, then test with `csdx myplugin:do` to ensure everything works correctly.

## Commands and Flags

Each command in your plugin must follow the `oclif` command structure:

### Command Structure

- `static description` - Help text displayed in the CLI
- `static flags` - CLI options and arguments
- `async run()` - Main command logic

### Example Command

```
import {Command, Flags} from '@oclif/core'

export default class MyCommand extends Command {
  static description = 'Performs operations with Contentstack'
  
  static flags = {
    stack: Flags.string({
      char: 's',
      description: 'Stack API key',
      required: true,
    }),
    help: Flags.help({char: 'h'}),
  }

  async run() {
    const {flags} = await this.parse(MyCommand)
    this.log(`Working with stack: ${flags.stack}`)
  }
}
```

## Testing

### Testing Setup

Use `@oclif/test` with Mocha or Jest for testing your commands.

### Example Test

```
import {expect, test} from '@oclif/test'

describe('myplugin:do', () => {
  test
    .stdout()
    .command(['myplugin:do', '--stack', 'dummy_key'])
    .it('runs myplugin:do', ctx => {
      expect(ctx.stdout).to.contain('Working with stack: dummy_key')
    })
})
```

**Run Tests**

```
npm test
```

## Testing Workflows

### Production Testing

To simulate the end-user experience, follow these steps to test your published plugin:

1. [**Install the Contentstack CLI globally**](/docs/headless-cms/install-the-cli):

   ```
   npm i -g @contentstack/cli
   ```

2. [**Set the region**](/docs/headless-cms/configure-regions-in-the-cli#set-region):

   ```
   csdx config:set:region <region-name>
   ```

3. [**Authenticate**](/docs/headless-cms/cli-authentication#authentication):

   ```
   csdx login
   ```

4. **Install your published plugin**:

   ```
   csdx plugins:install @contentstack/myplugin
   ```

5. **Test the plugin command**:

   ```
   csdx myplugin:do --help
   ```

### Development Testing

Test your plugin during development:

1. **Install the Contentstack CLI globally**:

   ```
   npm i -g @contentstack/cli
   ```

2. **Set the region**:

   ```
   csdx config:set:region <region-name>
   ```

3. **Authenticate**:

   ```
   csdx login
   ```

4. **Link your local plugin**:

   ```
   csdx plugins:link <plugin-local-path>
   ```

5. **Test the plugin command**:

   ```
   csdx myplugin:do --help
   ```

## Important Considerations

### Region and Authentication

Core plugins handle region and authentication automatically. Before using any command, ensure the user has configured the region and completed authentication.

1. [**Set the region**](/docs/headless-cms/configure-regions-in-the-cli#set-region):

   ```
   csdx config:set:region <region-name>
   ```

2. [**Authenticate**](/docs/headless-cms/cli-authentication#authentication):

   ```
   csdx login
   ```

### Contentstack CLI Features

The `@contentstack/cli` package provides additional features that plugins can leverage:

| Feature | Description |
| --- | --- |
| `cdaHost`, `cmaHost`, `region` | Region-aware endpoints |
| `authToken`, `email`, `region`, `config` | Auto-loaded from CSDX config |
| `utilities` | Common helpers for I/O, logging, formatting, etc. |
| Shared base command classes | Consistent CLI behavior |

### Publishing the Plugin

1. Publish your plugin package to npm:

   ```
   npm publish
   ```

2. Install via CLI:

   ```
   csdx plugins:install @contentstack/myplugin
   ```

Once installed, users can use your custom plugin to execute tasks.

## Best Practices

### Do's

| Practice | Description |
| --- | --- |
| Use namespacing | Prefix commands like `myplugin:action` to avoid collisions. |
| Follow oclif standards | Maintain command/flag conventions for consistency. |
| Use proper CLI feedback | Use `this.log`, `this.error`, `ux.prompt` for user interaction. |
| Validate inputs | Check required flags/args early in your command logic. |
| Add tests | Include basic tests for every command. |
| Document commands | Add descriptions, usage, and examples. |
| Use Contentstack SDKs | Prefer official [SDKs](/docs/developers/sdks) like `contentstack-management`. |
| Respect user configs | Use `~/.csdx/config.json` when needed. |
| Log errors gracefully | Use clear error messages and helpful hints. |

### Don'ts

| Practice | Reason |
| --- | --- |
| Don't overwrite global configs | Avoid altering shared state. |
| Don't hardcode values | Make plugins configurable. |
| Don't break existing flows | Avoid side effects in CLI. |
| Don't ignore security | Never log sensitive information. |
| Don't bypass CLI output patterns | Ensure UX consistency. |

## Uninstall a Plugin

To uninstall a plugin, perform the following steps:

1. **List the installed plugins**:

   ```
   csdx plugins:list
   ```

2. **Uninstall a specific plugin**:

   ```
   csdx plugins:uninstall <plugin_name>
   ```

> **Note:** This command **does not delete** the plugin's code folder from your local machine. It only removes the plugin from the CLI's plugin registry.

## Update a Plugin

To update an installed plugin, run the following command:

```
csdx plugins:update
```

## Remove All User Installed Plugins

To remove all user-installed plugins, run the following command:

```
csdx plugins:reset
```

## Display Installation Properties of a Plugin

To display the installation properties of a plugin, run the following commands:

```
cd <plugin-directory>
csdx plugins:inspect
```

## Available Methods and Utilities

When building your plugin, you have access to various methods and utilities from both `oclif` and the Contentstack CLI. Here are the most commonly used ones:

### Basic oclif Command Methods

These methods are available directly in the `Command` class:

```
// Logging
this.log('Message')                    // Print a message
this.error('Error message')           // Print an error and exit
this.warn('Warning message')           // Print a warning

// Exit handling
this.exit(code)                       // Exit with code (0 = success)
this.error('Message', {exit: 1})      // Error and exit with code

// Configuration access
this.config.bin                        // CLI binary name
this.config.version                    // CLI version
```

### Contentstack CLI Utilities

> **Note:** `@contentstack/cli-utilities` is optional and only required if you plan to use Contentstack-specific utilities such as `cliux`, `configHandler`, or `managementSDKClient`. Skip this if you're building a simple plugin that doesn't interact with Contentstack APIs.

To use Contentstack CLI utilities, install the following package:

```
npm install @contentstack/cli-utilities
```

This ensures your plugin works correctly when published and installed via `csdx plugins:install`.

**User Interface (cliux)**

```
import { cliux } from '@contentstack/cli-utilities'

// Printing messages
cliux.print('Message')                 // Print message
cliux.print('Message', {color: 'cyan'}) // Print with color
cliux.success('Success message')       // Print success message
cliux.error('Error message')           // Print error message
cliux.warning('Warning message')       // Print warning message
cliux.info('Info message')             // Print info message

// User prompts
const answer = await cliux.inquire({
  type: 'input',
  name: 'value',
  message: 'Enter a value:',
  default: 'default-value'
})

const confirmed = await cliux.confirm('Are you sure?')

// Loading indicators
cliux.loader('Processing...')          // Show loading spinner
```

**Configuration Access (configHandler)**

```
import { configHandler } from '@contentstack/cli-utilities'

// Get configuration values
const email = configHandler.get('email')
const region = configHandler.get('region')  // Returns { name, cma, cda }
const config = configHandler.get('config')   // Full config object

// Set configuration values
configHandler.set('key', 'value')

// Check authentication
import { isAuthenticated } from '@contentstack/cli-utilities'
if (isAuthenticated()) {
  // User is logged in
}
```

**Management SDK Client**

```
import { managementSDKClient } from '@contentstack/cli-utilities'

// Get authenticated SDK client
const region = configHandler.get('region')
const client = await managementSDKClient({ host: region.cma })

// Use the client
const stack = await client.stack({ api_key: 'your-api-key' })
const entries = await stack.contentType('content_type_uid').entry().query().find()
```

**Essential Helper Functions**

```
import { 
  isAuthenticated,
  formatError,
  validatePath,
  sanitizePath
} from '@contentstack/cli-utilities'

// Check authentication
if (isAuthenticated()) {
  // User is logged in
}

// Format Contentstack API errors
try {
  // API call
} catch (error) {
  const formattedError = formatError(error)
  cliux.error(formattedError)
}

// Path validation and sanitization
if (validatePath('/some/path')) {
  const cleanPath = sanitizePath('../../../some/path') // Removes directory traversal
}
```

**Logger Service**

The logger automatically initializes with the log path determined by the following priority:

1. Environment variable: `CS_CLI_LOG_PATH` (highest priority)
2. User config: `log.path` from CLI config (set via `csdx config:set:log --path <path>`)

```
import { log, handleAndLogError, getLogPath } from '@contentstack/cli-utilities'

// Get the current log path (useful for debugging)
const logPath = getLogPath()
console.log(`Logs are being written to: ${logPath}`)

// Simple logging (uses singleton logger, automatically initializes)
log.info('Info message')
log.success('Success message')
log.warn('Warning message')
log.debug('Debug message', { context: 'additional data' })

// Structured error logging
log.logError({
  type: 'API_ERROR',
  message: 'Failed to fetch entries',
  error: error,
  context: { stackApiKey: 'your-key' },
  meta: { additionalInfo: 'value' }
})

// Error handling with classification
try {
  // Your code
} catch (error) {
  handleAndLogError(error, { command: 'myplugin:do' }, 'Custom error message')
}
```

**Configuring Log Path**

Users can configure the log path using the CLI logging preference as follows:

```
csdx config:set:log --path /path/to/logs
```

Or set the environment variable:

```
export CS_CLI_LOG_PATH=/path/to/logs
```

### Complete Example: Using Utilities

Here's a complete example showing how to use these utilities together:

```
import {Command, Flags} from '@oclif/core'
import { 
  cliux, 
  configHandler, 
  isAuthenticated,
  managementSDKClient 
} from '@contentstack/cli-utilities'

export default class MyCommand extends Command {
  static description = 'Fetches entries from Contentstack'
  
  static flags = {
    'content-type': Flags.string({
      char: 'c',
      description: 'Content type UID',
      required: true,
    }),
    'stack-api-key': Flags.string({
      char: 's',
      description: 'Stack API key',
      required: true,
    }),
  }

  async run() {
    const {flags} = await this.parse(MyCommand)
    
    // Check authentication
    if (!isAuthenticated()) {
      cliux.error('Please login first: csdx login')
      this.exit(1)
    }
    
    // Get region configuration
    const region = configHandler.get('region')
    if (!region) {
      cliux.error('Please set a region: csdx config:set:region <region>')
      this.exit(1)
    }
    
    cliux.info(`Using region: ${region.name}`)
    
    try {
      // Get authenticated client
      const client = await managementSDKClient({ host: region.cma })
      const stack = client.stack({ api_key: flags['stack-api-key'] })
      
      // Show loading indicator
      cliux.loader('Fetching entries...')
      
      // Fetch entries
      const entries = await stack
        .contentType(flags['content-type'])
        .entry()
        .query()
        .find()
      
      cliux.success(`Found ${entries.items.length} entries`)
      
      // Display results
      entries.items.forEach((entry: any) => {
        cliux.print(`- ${entry.title} (${entry.uid})`)
      })
      
    } catch (error: any) {
      cliux.error(`Error: ${error.message}`)
      this.exit(1)
    }
  }
}
```

### Quick Reference: Essential Utilities

Here's a quick reference of essential utilities from `@contentstack/cli-utilities`:

| Utility | Import | Purpose |
| --- | --- | --- |
| User Interface | `cliux` | Print messages, prompts, confirmations |
| Configuration | `configHandler` | Access CLI config (`authToken`, `email`, `region`) |
| Authentication | `isAuthenticated` | Check if the user is logged in |
| Management SDK | `managementSDKClient` | Contentstack Management API client |
| Error Handling | `formatError` | Format Contentstack API errors |
| Path Utilities | `validatePath`, `sanitizePath` | Validate and sanitize file paths |
| Logging | `LoggerService` | Logging for your plugin |

## Troubleshooting

### Command Not Found After Linking

If your command isn't recognized after linking:

1. Verify that the build completed successfully:

   ```
   npm run build
   ```

2. Regenerate the manifest:

   ```
   npx oclif manifest
   ```

3. Check that the command exists in the `dist/commands/` directory:

   ```
   ls dist/commands/myplugin/
   ```

4. Relink the plugin:

   ```
   csdx plugins:uninstall myplugin
   csdx plugins:link
   ```

### ESM Module Warnings

You may see a warning as given below:

`Warning: @contentstack/myplugin is a linked ESM module and cannot be auto-transpiled.`

This warning is expected. The plugin loads compiled code from the `dist/` directory. Ensure to build your plugin before linking.

### Changes Not Reflecting

If your changes aren't showing up:

1. Rebuild the plugin:

   ```
   npm run build
   ```

2. Regenerate the manifest:

   ```
   npx oclif manifest
   ```

3. Relink if necessary:

   ```
   csdx plugins:link
   ```

### Authentication or Region Errors

If you get authentication or region errors:

1. Verify you're logged in:

   ```
   csdx login
   ```

2. Check your region:

   ```
   csdx config:get:region
   ```

3. Set region if required:

   ```
   csdx config:set:region <region-name>
   ```

### Plugin Installation Issues

If installation fails:

1. Verify that the package is published on npm.

2. Check that the package name matches:

   ```
   csdx plugins:install @contentstack/myplugin
   ```

3. Ensure that the package has the correct `oclif.manifest.json` file (generated during `npm publish`).
