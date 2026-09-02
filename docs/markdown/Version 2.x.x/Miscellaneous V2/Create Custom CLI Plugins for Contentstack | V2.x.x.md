---
uid: "blt64294e11f81fe300"
seo_title: "Create Custom CLI Plugins for Contentstack | Contentstack"
seo_description: "Learn how to build, test, and publish custom CLI plugins for Contentstack using oclif. Covers setup, development workflow, and best practices."
---

# Creating Custom CLI Plugins for Contentstack

## Overview

Build an external plugin that extends the Contentstack CLI with custom commands, using the oclif framework together with Contentstack CLI utilities for authentication, configuration, and API access.

The Contentstack CLI supports modular extensibility via external plugins, which:

- Extend CLI functionality with custom commands
- Can be installed globally or locally
- Are built using the [oclif framework](https://oclif.io/)

**Reference plugin:** `@contentstack/apps-cli`

## Prerequisites

Before you start, ensure the following:

- **Node.js version 22 or above**
- **Contentstack account** ([Sign up](https://www.contentstack.com/login) if you don't have one)
- **Familiarity with the oclif CLI framework** (recommended)
- **Contentstack CLI installed globally:**

```
npm install -g @contentstack/cli
```

## Plugin Structure

A well-organized plugin follows this recommended directory layout:

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

> **Note:** Use namespacing to prefix all commands to avoid collision, e.g., `csdx myplugin:do` instead of `csdx do`.

## Creating a Plugin

Use oclif's generator to create your plugin:

```
npx oclif generate myplugin
cd myplugin
```

The generator will prompt you with the following questions (shown in the order they appear):

1. **Select a module type** - Choose `ESM` or `CommonJS`
2. **NPM package name** - Example `@contentstack/myplugin` or `myplugin`
3. **Command bin name the CLI will export** - Example: `myplugin` (this is the binary name, not the full command namespace)
4. **Description** - Example: `A new CLI generated with oclif`
5. **Author** - Example: `Contentstack` or your organization name
6. **License** - Default: `MIT`
7. **Who is the GitHub owner of repository** `(https://github.com/OWNER/repo)` - Example: `@contentstack`
8. **What is the GitHub name of repository** `(https://github.com/owner/REPO)` - Example: `myplugin`
9. **Select a package manager** - Choose: `npm`, `yarn`, or `pnpm`

After answering these prompts, the generator will create the plugin structure in your current directory.

### Configure package.json

Modify the generated `package.json` to include the necessary oclif configuration:

```
{
  "name": "myplugin",
  "version": "1.0.0",
  "oclif": {
    "commands": "./lib/commands",
    "bin": "csdx"
  },
  "dependencies": {
    "@contentstack/cli-command": "~2.0.0",
    "@contentstack/cli-utilities": "~2.0.0",
    "@oclif/core": "^4.11.14"
  }
}
```

> **Note:** `oclif.commands` must point to `./lib/commands` (the compiled JavaScript output), not `./src/commands`. Pointing to TypeScript source will cause command discovery to fail when the plugin is linked or installed.

### Move to Plugin-Directory

```
cd <plugin-directory>
# Example: cd ./myplugin
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

This compiles your TypeScript commands from `src/commands/` to `lib/commands/`.

### Generate the manifest

After building, generate the oclif manifest file:

```
npx oclif manifest
```

This creates `oclif.manifest.json`, which is required for the CLI to discover your commands.

## Plugin Registration and Linking

When developing a plugin locally, you need to link it to the Contentstack CLI for testing:

```
cd <plugin-directory>
csdx plugins:link .
```

This sets up the plugin within the `csdx` namespace, allowing you to use your custom commands directly.

### Verify the setup

Test that your plugin is properly linked:

```
csdx myplugin:do --help
```

You should see your command's help output in the terminal.

### Development Workflow

During development, you can run the plugin directly using Node.js:

```
# Production mode (compiled JS from lib/)
node bin/run.js myplugin:do

# Development mode (TypeScript via ts-node, no build step needed)
node bin/dev.js myplugin:do
```

> **Tip:** After making changes to your plugin, rebuild and regenerate the manifest, then test with `csdx myplugin:do` to ensure everything works correctly.

## Commands and Flags

Each command in your plugin should follow the oclif command structure:

### Command Structure

- `static description` - Help text displayed in the CLI
- `static args` - Positional arguments (optional)
- `static flags` - Named CLI flags/options
- `async run()` - Main command logic

### Example Command

```
import { Command } from '@contentstack/cli-command'
import { Args, flags } from '@contentstack/cli-utilities'

export default class MyCommand extends Command {
  static description = 'Does something cool with Contentstack'

  // Positional arguments — import Args from @contentstack/cli-utilities
  static args = {
    environment: Args.string({
      description: 'Environment name',
      required: true,
    }),
  }

  static flags = {
    'stack-api-key': flags.string({
      char: 's',
      description: 'Stack API key',
      required: true,
    }),
  }

  async run() {
    const { args: cmdArgs, flags: cmdFlags } = await this.parse(MyCommand)
    // All base Command class properties are available automatically:
    this.log(`Stack: ${cmdFlags['stack-api-key']}, Env: ${cmdArgs.environment}`)
    this.log(`CMA: ${this.cmaAPIUrl}, Region: ${this.region.name}`)
  }
}
```

> **Note:** Import `Command` from `@contentstack/cli-command` (not `@oclif/core`). Import `flags` (lowercase) and `Args` from `@contentstack/cli-utilities`. `flags` and `Args` are re-exported from `@oclif/core`, they are not Contentstack-specific, but importing them from `@contentstack/cli-utilities` is the recommended approach so your plugin does not need a direct `@oclif/core` dependency.

## Testing

### Testing Setup

Use `@oclif/test` with Mocha and `sinon` for testing your commands.

> **Note:** `@oclif/test` v4 (which aligns with `@oclif/core` v4) removed the old chained `test.stdout().command().it()` API entirely. The package now exports only `runCommand`, `captureOutput`, and `runHook`. Using the old API will throw `TypeError: Cannot read properties of undefined`.

**Example Test**

```
import { expect } from 'chai'
import { describe, it, afterEach } from 'mocha'
import { stub, restore } from 'sinon'
import MyCommand from '../../../src/commands/myplugin/do'

describe('myplugin:do', () => {
  afterEach(() => restore())

  it('runs with required flag', async () => {
    const runStub = stub(MyCommand.prototype, 'run').resolves()
    await MyCommand.run(['--stack-api-key', 'dummy_key'])
    expect(runStub.calledOnce).to.be.true
  })
})
```

**Run Tests**

```
npm test
```

### Testing Workflows

**Production Testing**

Test your published plugin as end users would:

1. **Install the Contentstack CLI globally:**

   ```
   npm i -g @contentstack/cli
   ```

2. **Set the region:**

   ```
   csdx config:set:region <region-name>
   ```

3. **Authenticate:**

   ```
   csdx auth:login
   ```

4. **Install your published plugin:**

   ```
   csdx plugins:install @contentstack/myplugin
   ```

5. **Test the plugin command:**

   ```
   csdx myplugin:do --help
   ```

**Development Testing**

Test your plugin during development:

1. **Install the Contentstack CLI globally:**

   ```
   npm i -g @contentstack/cli
   ```

2. **Set the region:**

   ```
   csdx config:set:region <region-name>
   ```

3. **Authenticate:**

   ```
   csdx auth:login
   ```

4. **Link your local plugin:**

   ```
   csdx plugins:link <plugin-local-path>
   ```

5. **Test the plugin command:**

   ```
   csdx myplugin:do --help
   ```

## Important Considerations

### Region and Authentication

> **Note:** Core plugins handle region and authentication automatically. Before using any command, ensure the user has configured the **region** and completed **authentication**.

1. **Set the region:**

   ```
   csdx config:set:region <region-name>
   ```

   For more information, see [Configure Regions](/docs/headless-cms/configure-regions-in-the-cli).

2. **Authenticate:**

   ```
   csdx auth:login
   ```

   For more information, see [CLI Authentication](/docs/headless-cms/cli-authentication).

### Contentstack CLI Features

The `@contentstack/cli-command` base `Command` class exposes the following properties automatically, with no manual config lookup needed. Properties use two API abbreviations: Content Management API (CMA) and Content Delivery API (CDA).

| Property | Type | Description |
| --- | --- | --- |
| `this.region` | `{ name, cma, cda, uiHost, ... }` | Full region object |
| `this.cmaHost` | `string` | CMA hostname, protocol stripped (`api.contentstack.io`) |
| `this.cdaHost` | `string` | CDA hostname, protocol stripped (`cdn.contentstack.io`) |
| `this.cmaAPIUrl` | `string` | Full CMA URL with `https://` (`https://api.contentstack.io`) |
| `this.cdaAPIUrl` | `string` | Full CDA URL with `https://` |
| `this.uiHost` | `string` | App UI URL (`https://app.contentstack.com`) |
| `this.email` | `string` | Logged-in user's email. Throws `CLIError` if not logged in |
| `this.rateLimit` | `number` | User-configured rate limit (default: `5`) |
| `this.getToken(alias)` | `function` | Look up a stored management token by alias |
| `this.deliveryAPIClient` | `contentstack` SDK | Contentstack Delivery SDK, ready to initialize |
| `this.developerHubUrl` | `string` | Developer Hub API URL |
| `this.launchHubUrl` | `string` | Launch Hub API URL |
| `this.personalizeUrl` | `string` | Personalize API URL |
| `this.composableStudioUrl` | `string` | Composable Studio URL |
| `this.context` | `object` | oclif config context |

## Publishing the Plugin

### Publish to npm

1. **Publish your plugin package to npm:**

   ```
   npm publish
   ```

2. **Install via CLI:**

   ```
   csdx plugins:install @contentstack/myplugin
   ```

Once installed, users can use your custom plugin to execute tasks.

## Best Practices

### Do's

| Practice | Description |
| --- | --- |
| **Use namespacing** | Prefix commands like `myplugin:action` to avoid collisions |
| **Follow oclif standards** | Maintain command/flag conventions for consistency |
| **Use proper CLI feedback** | Use `this.log`, `this.error`, `ux.prompt` for user interaction |
| **Validate inputs** | Check required flags/args early in your command logic |
| **Add tests** | Include basic tests for every command |
| **Document commands** | Add descriptions, usage, and examples |
| **Use Contentstack SDKs** | Prefer official SDKs like `contentstack-management` |
| **Respect user configs** | Use `~/.csdx/config.json` when needed |
| **Log errors gracefully** | Use clear error messages and helpful hints |

### Don'ts

| Practice | Reason |
| --- | --- |
| **Don't overwrite global configs** | Avoid altering shared state |
| **Don't hardcode values** | Make plugins configurable |
| **Don't break existing flows** | Avoid side effects in CLI |
| **Don't ignore security** | Never log sensitive information |
| **Don't bypass CLI output patterns** | Ensure UX consistency |

## Managing Installed Plugins

### Uninstalling a Plugin

If you need to uninstall a plugin:

1. **List installed plugins:**

   ```
   csdx plugins
   ```

2. **Uninstall a specific plugin:**

   ```
   csdx plugins:uninstall <plugin_name>
   ```

> **Note:** This command will not delete the plugin's code folder from your local machine, only remove it from the CLI's plugin registry.

### Updating a Plugin

If you need to update an installed plugin:

```
csdx plugins:update
```

### Resetting All Plugins

To remove all user-installed plugins:

```
csdx plugins:reset
```

### Inspecting a Plugin

To display the installation properties of a plugin:

```
cd <plugin-directory>
csdx plugins:inspect
```

## Available Methods and Utilities

### Basic oclif Command Methods

```
this.log('Message')               // Print a message
this.error('Error message')       // Print an error and exit
this.warn('Warning message')      // Print a warning
this.exit(0)                      // Exit with code
this.config.bin                   // CLI binary name ('csdx')
this.config.version               // CLI version
```

### Contentstack CLI Utilities (`@contentstack/cli-utilities`)

> **Note:** Only needed if you want Contentstack-specific utilities (`cliux`, `managementSDKClient`, etc.). Simple plugins that don't interact with Contentstack APIs can skip this.

```
npm install @contentstack/cli-utilities
```

**User Interface (cliux)**

```
import { cliux } from '@contentstack/cli-utilities'

// Print messages
cliux.print('Message')
cliux.print('Info', { color: 'cyan' })           // cyan = info style
cliux.print('Warning', { color: 'yellow' })      // yellow = warning style
cliux.print('Bold text', { bold: true })
cliux.success('Done!')                           // green
cliux.error('Something failed')                  // red

// Note: cliux.info() and cliux.warning() do NOT exist — use cliux.print() with color

// Spinner — cliux.loader() is a TOGGLE: first call starts, second call stops
cliux.loader('Processing...')   // start
// ... do work ...
cliux.loader()                  // stop — never forget this or the spinner hangs

// loaderV2 — returns an Ora instance for more control
const spinner = cliux.loaderV2('Fetching...')  // start, returns Ora
// ... do work ...
cliux.loaderV2('Done', spinner)                // set text and stop

// Table output — value = data key, alias = display header
cliux.table(
  [
    { value: 'title', alias: 'Title' },
    { value: 'uid',   alias: 'UID' },
  ],
  entries.map((e: any) => ({ title: e.title, uid: e.uid })),
)

// Progress bar — returns a cli-progress SingleBar
const bar = cliux.progress({ format: 'Writing |{bar}| {value}/{total}' })
bar.start(total, 0)
bar.increment()
bar.stop()

// Prompts
const answer = await cliux.inquire({ type: 'input', name: 'value', message: 'Enter value:' })
const confirmed = await cliux.confirm('Are you sure?')
```

**Structured Errors (CLIError)**

Use `CLIError` instead of `cliux.error()` + `this.exit()` to throw a clean, structured CLI error:

```
import { CLIError } from '@contentstack/cli-utilities'

if (!isAuthenticated()) {
  throw new CLIError('Please login first: csdx auth:login')
}
```

**Positional Arguments (Args)**

```
import { Args, flags } from '@contentstack/cli-utilities'

static args = {
  environment: Args.string({ description: 'Environment name', required: true }),
  uid: Args.string({ description: 'Entry UID' }),
}

async run() {
  const { args: cmdArgs } = await this.parse(MyCommand)
  this.log(cmdArgs.environment)
}
```

**Configuration Access (configHandler)**

```
import { configHandler } from '@contentstack/cli-utilities'

const email  = configHandler.get('email')
const region = configHandler.get('region')    // { name, cma, cda, uiHost, ... }
const token  = configHandler.get('authtoken')

configHandler.set('myKey', 'value')
```

**Authentication**

```
import { isAuthenticated, isManagementTokenValid } from '@contentstack/cli-utilities'

// Check if user is logged in (reads authtoken/oauthAccessToken from config)
if (!isAuthenticated()) {
  throw new CLIError('Please login first: csdx auth:login')
}

// Validate a stored management token before using it in a long operation
const { token } = this.getToken(alias)
const result = await isManagementTokenValid(stackApiKey, token)
if (result.valid !== true) {
  throw new CLIError(`Token invalid: ${result.message}`)
}
```

**Management SDK Client**

```
import { managementSDKClient } from '@contentstack/cli-utilities'

// Always use this.cmaHost from the base Command class — it's already region-aware
const client = await managementSDKClient({ host: this.cmaHost })
const stack  = client.stack({ api_key: cmdFlags['stack-api-key'] })
const result = await stack.contentType('blog_post').entry().query().find()
```

**Direct HTTP Client (HttpClient)**

For calls that don't go through the management SDK (custom endpoints, third-party APIs):

```
import { HttpClient, configHandler } from '@contentstack/cli-utilities'

const httpClient = new HttpClient({
  headers: {
    api_key:   cmdFlags['stack-api-key'],
    authtoken: configHandler.get('authtoken'),
  },
})

const response = await httpClient.get(`${this.cmaAPIUrl}/v3/stacks`)
const stack = response?.data?.stack
```

`HttpClient` handles proxy configuration, retry logic, and Open Authorization (OAuth) headers automatically.

**File System Utility (FsUtility)**

For chunked streaming reads and writes of large datasets, used by all import/export plugins:

```
import { FsUtility } from '@contentstack/cli-utilities'

const fsUtil = new FsUtility({
  basePath:            './exports/entries',
  moduleName:          'entries',
  fileExt:             'json',
  createDirIfNotExist: true,
})

// Write entries in chunks (auto-creates UUID-named chunk files + index)
for (const entry of entries) {
  fsUtil.writeIntoFile([entry] as any, { keyName: 'uid', mapKeyVal: true })
}
```

**Progress Tracking (CLIProgressManager + SummaryManager)**

`CLIProgressManager` is the standard way to track progress in complex multi-module operations (used by import/export plugins). It handles spinners, progress bars, and per-module success/failure counts.

Use the static factory `createSimple` for a single-module progress bar. The constructor auto-starts the spinner or progress bar, there is no separate `start()` call. Use `tick()` to record each item result, and `complete()` to finalize:

```
import { CLIProgressManager } from '@contentstack/cli-utilities'

// createSimple(moduleName, total) — auto-starts on construction
const manager = CLIProgressManager.createSimple('entries', entries.length)

for (const entry of entries) {
  try {
    await processEntry(entry)
    manager.tick(true, entry.uid)           // success
  } catch (err: any) {
    manager.tick(false, entry.uid, err.message)  // failure
  }
}

// complete() stops the bar and triggers summary callbacks
manager.complete(manager.getFailureCount() === 0)
```

For multi-module operations with a shared summary (used by import/export):

```
import { CLIProgressManager } from '@contentstack/cli-utilities'

// Initialize a global summary before creating any managers
CLIProgressManager.initializeGlobalSummary('export', 'main', 'EXPORT CONTENT')

const entriesManager    = CLIProgressManager.createSimple('entries', entries.length)
const assetsManager     = CLIProgressManager.createSimple('assets', assets.length)

for (const entry of entries) {
  entriesManager.tick(true, entry.uid)
}
entriesManager.complete(true)

for (const asset of assets) {
  assetsManager.tick(true, asset.uid)
}
assetsManager.complete(true)

// Print final success/failure counts for all modules
CLIProgressManager.printGlobalSummary()
```

`SummaryManager` is used internally by `CLIProgressManager`, so you rarely need it directly. Access the shared instance via the static method:

```
const hasFailed = CLIProgressManager.hasFailures()  // true if any module had failures
CLIProgressManager.printGlobalSummary()             // print all module counts
CLIProgressManager.clearGlobalSummary()             // reset for a new run
```

**Reading Content Type Schemas (readContentTypeSchemas / readGlobalFieldSchemas)**

For plugins that work with exported content type or global field schema files:

```
import { readContentTypeSchemas, readGlobalFieldSchemas } from '@contentstack/cli-utilities'

// Read all CT schema JSON files from a directory
const contentTypes = readContentTypeSchemas('./exports/content_types')

// Read all global field schema files (excludes schema.json, __master.json, etc.)
const globalFields = readGlobalFieldSchemas('./exports/global_fields')
```

**Chalk (loadChalk / getChalk)**

Chalk 5 is ESM-only. Use the built-in compatibility layer rather than requiring chalk directly:

```
import { loadChalk, getChalk } from '@contentstack/cli-utilities'

// During CLI init / command setup — loads and caches chalk
await loadChalk()

// After loadChalk() has been called — get the cached instance
const chalk = getChalk()
cliux.print(chalk.bold.cyan('Bold cyan text'))
```

**Helper Utilities**

```
import {
  formatError,
  validatePath,
  sanitizePath,
  pathValidator,
  redactObject,
  generateUid,
  generateShortUid,
  formatDate,
  formatTime,
  isManagementTokenValid,
  getAuthenticationMethod,
  validateUids,
  validateFileName,
  escapeRegExp,
} from '@contentstack/cli-utilities'

// Format Contentstack API errors into a clean message string
try { /* API call */ } catch (error) {
  throw new CLIError(formatError(error))
}

// Path validation — rejects paths with special chars (*,$,%,#,<>,{},!,&,?)
if (!validatePath(cmdFlags.output)) throw new CLIError('Invalid path')

// Path sanitization — strips directory traversal (../) and normalises slashes
const safe = sanitizePath(path.resolve(cmdFlags.output))

// Path normalization — resolves against cwd and strips traversal
const normalized = pathValidator('./relative/path')

// Redact sensitive keys before logging
// Strips: authtoken, token, api_key, management token, delivery token, password, secret, email
const safePayload = redactObject({ apiKey: 'bltXXX', authtoken: 'csXXX', email: 'user@example.com', data: 'ok' })
// => { apiKey: '[REDACTED]', authtoken: '[REDACTED]', email: '[REDACTED]', data: 'ok' }

// UUID generation
const uid      = generateUid()       // UUID v4
const shortUid = generateShortUid()  // short UUID

// Date/time formatting (produces YYYYMMDD and HHMMSS strings)
const now  = new Date()
const date = formatDate(now)   // '20260813'
const time = formatTime(now)   // '183916'

// Auth method detection
const method = getAuthenticationMethod()  // 'OAuth' | 'Basic Auth' | ''

// UID and filename validation
validateUids('blt123abc')      // true/false — alphanumeric only
validateFileName('export.json') // true/false — alphanumeric, dash, underscore, dot
escapeRegExp('a.b*c')          // 'a\\.b\\*c'
```

**Logger Service**

```
import { log, handleAndLogError, getLogPath, getSessionLogPath } from '@contentstack/cli-utilities'

const logPath     = getLogPath()        // base log path for the current run
const sessionPath = getSessionLogPath() // session-specific log file path

log.info('Info message')
log.success('Success message')
log.warn('Warning message')
log.debug('Debug message', { context: 'extra data' })
log.logError({
  type:    'API_ERROR',
  message: 'Failed to fetch entries',
  error:   error,
  context: { stackApiKey: 'bltXXX' },
})

try {
  // your code
} catch (error) {
  handleAndLogError(error, { command: 'myplugin:do' }, 'Custom error message')
}
```

Configure log path:

```
csdx config:set:log --path /path/to/logs
# or
export CS_CLI_LOG_PATH=/path/to/logs
```

### Complete Example

A production-quality command using all major utilities:

```
import { Command } from '@contentstack/cli-command'
import {
  Args,
  flags,
  cliux,
  CLIError,
  isAuthenticated,
  managementSDKClient,
  redactObject,
  generateUid,
  formatDate,
  formatTime,
  configHandler,
} from '@contentstack/cli-utilities'

export default class MyCommand extends Command {
  static description = 'Fetch and display entries from a content type'

  static examples = ['csdx myplugin:do blog_post --stack-api-key <key>']

  static args = {
    'content-type': Args.string({ description: 'Content type UID', required: true }),
  }

  static flags = {
    'stack-api-key': flags.string({ char: 's', description: 'Stack API key', required: true }),
    alias: flags.string({ char: 'a', description: 'Management token alias' }),
  }

  async run() {
    const { args: cmdArgs, flags: cmdFlags } = await this.parse(MyCommand)

    if (!isAuthenticated()) {
      throw new CLIError('Please login first: csdx auth:login')
    }

    const requestId = generateUid()
    const now       = new Date()

    // All base Command class properties — available automatically
    cliux.print(`Region:      ${this.region.name}`, { color: 'cyan' })
    cliux.print(`CMA URL:     ${this.cmaAPIUrl}`, { color: 'cyan' })
    cliux.print(`CDA URL:     ${this.cdaAPIUrl}`, { color: 'cyan' })
    cliux.print(`UI host:     ${this.uiHost}`, { color: 'cyan' })
    cliux.print(`Rate limit:  ${this.rateLimit} req/s`, { color: 'cyan' })
    cliux.print(`Request ID:  ${requestId} — ${formatDate(now)}_${formatTime(now)}`, { color: 'cyan' })

    // loaderV2: start spinner, returns Ora instance
    const spinner = cliux.loaderV2(`Fetching entries from '${cmdArgs['content-type']}'...`)

    try {
      const client = await managementSDKClient({ host: this.cmaHost })
      const stack  = client.stack({ api_key: cmdFlags['stack-api-key'] })
      const result = await stack.contentType(cmdArgs['content-type']).entry().query().find()

      cliux.loaderV2('Done', spinner)  // stop spinner
      cliux.success(`Found ${result.items.length} entries`)

      // cliux.table(): value = data key, alias = column header
      cliux.table(
        [
          { value: 'title',      alias: 'Title' },
          { value: 'uid',        alias: 'UID' },
          { value: 'locale',     alias: 'Locale' },
          { value: 'created_at', alias: 'Created' },
        ],
        result.items.map((e: any) => ({
          title:      e.title || '(no title)',
          uid:        e.uid,
          locale:     e.locale || 'en-us',
          created_at: e.created_at?.substring(0, 10) || '-',
        })),
      )

      // redactObject strips sensitive keys before logging
      const safeLog = redactObject({
        requestId,
        stackApiKey: cmdFlags['stack-api-key'],
        authtoken:   configHandler.get('authtoken'),
        entries:     result.items.length,
      })
      cliux.print(JSON.stringify(safeLog, null, 2))

    } catch (error: any) {
      cliux.loaderV2('', spinner)  // always stop spinner on error
      throw new CLIError(error.errorMessage || error.message)
    }
  }
}
```

### Utilities Quick Reference

For the full list of base `Command` properties available on `this` (`this.region`, `this.cmaHost`, `this.cdaHost`, and the rest), see [Contentstack CLI Features](#contentstack-cli-features) above.

**@contentstack/cli-utilities: All Exports**

| Export | Purpose |
| --- | --- |
| `cliux` | `print`, `success`, `error`, `loader` (toggle), `loaderV2` (Ora), `table`, `progress`, `inquire`, `confirm` |
| `CLIError` | Throw a structured CLI error |
| `flags` | Flag definitions (`flags.string`, `flags.boolean`, `flags.integer`, ...) |
| `Args` | Positional argument definitions (`Args.string`, `Args.integer`, ...) |
| `configHandler` | Read/write CLI config (`get`, `set`) |
| `isAuthenticated` | Returns `true` if logged in |
| `isManagementTokenValid` | Validates a management token against the API |
| `getAuthenticationMethod` | Returns `'OAuth'` \| `'Basic Auth'` \| `''` |
| `managementSDKClient` | Authenticated CMA SDK client |
| `HttpClient` | Direct HTTP client with proxy/retry support |
| `FsUtility` | Chunked file read/write for large datasets |
| `CLIProgressManager` | Full progress tracking: spinner, bar, success/failure counts |
| `SummaryManager` | Per-module operation summary |
| `readContentTypeSchemas` | Read content type JSON files from a directory |
| `readGlobalFieldSchemas` | Read global field JSON files from a directory |
| `marketplaceSDKClient` | Contentstack Marketplace SDK client |
| `formatError` | Parse and format Contentstack API errors |
| `validatePath` | Reject paths with special chars |
| `sanitizePath` | Remove `../` traversal, normalise slashes |
| `pathValidator` | Resolve path against cwd, strip traversal |
| `redactObject` | Strip sensitive keys (`authtoken`, `api_key`, `token`, etc.) before logging |
| `generateUid` | UUID v4 |
| `generateShortUid` | Short UUID |
| `formatDate` | `Date` → `'YYYYMMDD'` |
| `formatTime` | `Date` → `'HHMMSS'` |
| `validateUids` | Validate alphanumeric UID |
| `validateFileName` | Validate filename characters |
| `escapeRegExp` | Escape special chars for use in RegExp |
| `loadChalk` / `getChalk` | Chalk 5 ESM compatibility layer |
| `log` | Singleton logger (`info`, `success`, `warn`, `debug`, `logError`) |
| `handleAndLogError` | Classify and log an error |
| `getLogPath` | Base log directory path |
| `getSessionLogPath` | Session-specific log file path |
| `LoggerService` | Logger class for custom logger instances |
| `CLITable` | Table rendering class |
| `NodeCrypto` | Encryption/decryption utility |
| `messageHandler` | i18n key→string resolution |
| `authHandler` | Authentication handler |
| `managementSDKInitiator` | Low-level SDK initiator |
| `ContentstackClient`, `ContentstackConfig` | TypeScript types for management SDK |

## Troubleshooting

### Command Not Found After Linking

**Root Cause(s)**: The plugin was linked before it was built, or the oclif manifest is stale, so the CLI has no record of the command.

**Resolution**:

1. **Verify the build completed successfully:**

   ```
   npm run build
   ```

2. **Regenerate the manifest:**

   ```
   npx oclif manifest
   ```

3. **Check that the command exists in** `lib/commands/`**:**

   ```
   ls lib/commands/myplugin/
   ```

4. **Relink the plugin:**

   ```
   csdx plugins:uninstall myplugin
   csdx plugins:link .
   ```

### ESM Module Warnings

**Root Cause(s)**: oclif cannot auto-transpile a linked ESM plugin, so it prints a warning like the one below even though the plugin runs fine from its compiled output:

```
Warning: @contentstack/myplugin is a linked ESM module and cannot be auto-transpiled.
```

**Resolution**: No action is needed if you've already built the plugin. The plugin runs from the compiled code in the `lib/` directory, not from the warning's source. Build your plugin before linking to avoid the warning altogether.

### Changes Not Reflecting

**Root Cause(s)**: The linked plugin still points at a previous build, since linking does not automatically rebuild or refresh the plugin's compiled output.

**Resolution**:

1. Rebuild the plugin: `npm run build`
2. Regenerate the manifest: `npx oclif manifest`
3. Relink if necessary: `csdx plugins:link .`

### Authentication or Region Errors

**Root Cause(s)**: The CLI has no active session, or no region configured, for the account being used.

**Resolution**:

1. Verify you're logged in: `csdx auth:login`
2. Check your region: `csdx config:get:region`
3. Set region if needed: `csdx config:set:region <region-name>`

### Plugin Installation Issues

**Root Cause(s)**:

- The package isn't published on npm.
- The package name in the install command doesn't match the published name.
- The package is missing a valid `oclif.manifest.json` file.

**Resolution**:

1. Verify the package is published on npm.
2. Check the package name matches: `csdx plugins:install @contentstack/myplugin`.
3. Ensure the package has the correct `oclif.manifest.json` file (generated during `npm publish`).

## Next Steps

- [CLI Authentication](/docs/headless-cms/cli-authentication): set up and verify authentication for the Contentstack CLI before publishing or testing your plugin.
- [Configure Regions](/docs/headless-cms/configure-regions-in-the-cli): point the CLI at the correct Contentstack region for your organization.
- `@contentstack/apps-cli`: review a real, published plugin for command structure and namespacing conventions.
