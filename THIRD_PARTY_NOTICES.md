# Third-Party Notices

This repository bundles several skill directories that were copied from an existing local Codex/agent skill installation at packaging time.

The purpose of this file is transparency:

- where each bundled skill came from during packaging
- whether an explicit license file was present in the bundled copy
- which items should be reviewed before redistribution

## Packaging-Time Source Notes

| Bundled skill | Packaging-time local source | Included license file in bundle | Notes |
| --- | --- | --- | --- |
| `frontend-design` | `~/.agents/skills/frontend-design` | Yes | `skills/frontend-design/LICENSE.txt` is preserved in this repo. |
| `api-design-principles` | `~/.agents/skills/api-design-principles` | No separate license file found in copied directory | Review upstream rights before broader redistribution. |
| `postgresql-table-design` | `~/.agents/skills/postgresql-table-design` | No separate license file found in copied directory | Review upstream rights before broader redistribution. |
| `test-driven-development` | `~/.agents/skills/test-driven-development` | No separate license file found in copied directory | Review upstream rights before broader redistribution. |
| `systematic-debugging` | `~/.agents/skills/systematic-debugging` | No separate license file found in copied directory | Review upstream rights before broader redistribution. |
| `verification-before-completion` | `~/.agents/skills/verification-before-completion` | No separate license file found in copied directory | Review upstream rights before broader redistribution. |
| `requesting-code-review` | `~/.agents/skills/requesting-code-review` | No separate license file found in copied directory | Review upstream rights before broader redistribution. |

## Repository-Owned Skill

| Skill | Notes |
| --- | --- |
| `spec-driven-coding` | This bundled copy is maintained in this repository and was adapted into a portable, publishable bundle form. |

## Important Boundary

The root [LICENSE](LICENSE) covers repository-authored root files such as:

- `README.md`
- `install.sh`
- this notice file
- repository-level packaging glue

It does not automatically overwrite or replace any separate terms that may apply to bundled third-party skill directories.

If you publish or redistribute this repository further, verify the upstream license status of each bundled third-party skill before assuming the root MIT license covers those copies.
