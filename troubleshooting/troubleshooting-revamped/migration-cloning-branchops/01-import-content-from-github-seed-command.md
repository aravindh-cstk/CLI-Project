# Import Content from a GitHub Repository Using the CLI Seed Command

The customer wanted to import content directly from a GitHub repository into Contentstack and asked for the correct method.

**Root cause**

The Seed command (`csdx cm:stacks:seed`) does not import arbitrary content from a GitHub repository. It only imports content that is already in Contentstack's exported stack format and placed inside a folder named `stack` in the repository, with a GitHub Release created for that repository. The command downloads the latest release's tarball through the public GitHub API and extracts it, then runs it through the same import logic used by `cm:stacks:import`.

The command reaches the GitHub REST API without an authentication header, so it can only access public repositories. It does not support private repositories or personal access tokens. It also fails if the repository has no `stack` folder or no published GitHub Release, even when the exported content itself is otherwise valid.

**Resolution**

1. Export the source stack with `csdx cm:stacks:export` (for example `csdx cm:stacks:export -A` or `csdx cm:stacks:export -a "management token"`).

2. Create a public GitHub repository and, inside it, a folder named `stack`. Commit the exported content into that `stack` folder.

3. Create a GitHub Release on that repository. The Seed command downloads and extracts the latest release, not just the latest commit on the default branch.

4. Run `csdx cm:stacks:seed --repo "account/repository"` to import the content into the target stack. Use `--stack-api-key` to seed into an existing stack, or `--org` and `--stack-name` to create a new one.

Content from the GitHub repository imports successfully into the target stack once it follows this `stack`-folder-plus-release structure and the repository is public.

*Source ticket: Case 40919*
