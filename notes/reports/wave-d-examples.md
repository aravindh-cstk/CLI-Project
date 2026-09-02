# Wave D: the Examples pass

32 docs had no Examples section. 8 got one. 24 are deferred, and three of the reasons are correctness traps rather than effort.

## Why V1 docs get nothing here

The only verified flag data is `notes/reports/flag-inventory.json`, built from the `oclif.manifest.json` inside each published **2.0.0** tarball. Writing a 2.0.0 example onto a V1 page is the defect `CLI-C11` exists to stop. `cm:stacks:migration --config` kept its name and changed its meaning between the versions, and short flags were removed across six plugins, so a V1 reader copying a 2.0.0 line gets a command that fails or, worse, one that quietly does something else.

## The three that look eligible and are not

| Doc | Why |
|---|---|
| `Query-based Export` | One CMS entry shown in both version trees, so 2.0.0 examples would land on the V1 page as well. |
| `CLI for Launch`, both versions | The accuracy report scopes it to `auth:login`, because `launch:*` publishes no manifest. `auth:login` ships three flags and none of them concerns Launch. |
| `Apps CLI Plugin | V2.x.x` | Same scoping artifact. Its subject is `app:*`, which publishes no manifest. |
| `Configure MFA Secret Using CLI | V2.x.x` | MFA has no command of its own. The doc sets `CONTENTSTACK_MFA_SECRET` and then runs `auth:login`, so an Examples section would repeat its Commands section. |

## The rest

Each documents several commands, so one Examples section cannot be scoped from flag data alone: `Audit Plugin` (4 commands), `Compare and Merge Branches` (8 in V1, 10 in V2), `CLI Authentication and Adding Tokens` (6 and 7), `Configure Early Access` (3), `Configure Proxy Settings` (3), and `Bulk Publish and Unpublish Content`, whose commands publish no manifest.

## What the 8 sections do and do not claim

Every flag in every example is checked against the inventory before anything is written, and the script refuses to write on a single unknown flag. So no example can name a flag the released binary does not have.

What is **not** claimed is that a combination is the best way to do a task. Each example states what its flags do, drawn from the manifest's own descriptions, and stops there.

