# Spec-Driven Coding

[![Repo](https://img.shields.io/badge/repo-spec--driven--coding-24292f?logo=github)](https://github.com/zhao5271/spec-driven-coding)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Codex](https://img.shields.io/badge/agent-Codex-10a37f)](README.md)
[![Bundle](https://img.shields.io/badge/bundle-8_skills-orange)](README.md)

Spec-first coding workflow for Codex, packaged as a ready-to-install bundle with the execution and domain companion skills most teams actually need.

This repository is for people who want:

- a real `spec.md -> tasks.md -> implementation -> reverse sync` workflow
- one install step instead of collecting multiple skills by hand
- execution discipline without letting another process framework take over the main plan

## Why

Most AI coding sessions fail for boring reasons:

- the plan only exists in chat history
- implementation starts before scope is stable
- debugging and validation happen too late
- different helper skills pull the workflow in different directions

This bundle fixes that by making one skill the workflow owner:

- `spec-driven-coding` owns the change package, `spec.md`, `tasks.md`, and Reverse Sync
- companion skills improve execution quality, not planning ownership

## Features

- Spec-first workflow for any repository
- Change-package scaffolding via `code_copilot/changes/<change-name>/`
- Explicit `spec.md`, `tasks.md`, and `log.md` flow
- Reverse Sync rules when code drifts from plan
- Bundled execution companions for TDD, debugging, verification, and review
- Bundled domain companions for frontend, API, and PostgreSQL work
- Portable bundle layout that installs into Codex with one script

## Included Skills

Main workflow:

- `spec-driven-coding`

Domain companions:

- `frontend-design`
- `api-design-principles`
- `postgresql-table-design`

Execution companions:

- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`

## 1-Minute Install

If you just want the fastest path:

```bash
git clone git@github.com:zhao5271/spec-driven-coding.git
cd spec-driven-coding
./install.sh
```

Then start with:

```text
用 $spec-driven-coding 为这个仓库初始化 code_copilot
```

or:

```text
Use $spec-driven-coding to scaffold code_copilot for this repo
```

## Install

Clone the repository:

```bash
git clone git@github.com:zhao5271/spec-driven-coding.git
cd spec-driven-coding
```

Install into the default Codex skills directory:

```bash
./install.sh
```

Default target:

```text
${CODEX_HOME:-$HOME/.codex}/skills
```

Install into a custom directory:

```bash
./install.sh --target /path/to/skills
```

Overwrite existing skill folders:

```bash
./install.sh --force
```

## Usage

### Recommended Pairings

New feature or refactor:

- `$spec-driven-coding`
- `$test-driven-development`
- `$verification-before-completion`

Bugfix:

- `$spec-driven-coding`
- `$systematic-debugging`
- `$verification-before-completion`

Large or risky change:

- `$spec-driven-coding`
- `$requesting-code-review`

### Shortest Prompt Cheat Sheet

Initialize a repository:

```text
用 $spec-driven-coding 为这个仓库初始化 code_copilot
```

```text
Use $spec-driven-coding to scaffold code_copilot for this repo
```

Start a new feature:

```text
用 $spec-driven-coding 先为“用户批量导入”创建 change package，再按 TDD 实现
```

```text
Use $spec-driven-coding to create a change package for "bulk user import", then implement it with TDD
```

Start a refactor:

```text
用 $spec-driven-coding 先写 spec 和 tasks，再重构这个模块
```

```text
Use $spec-driven-coding to write spec and tasks first, then refactor this module
```

Fix a bug:

```text
用 $spec-driven-coding 先建 change package，用 $systematic-debugging 排查这个 bug
```

```text
Use $spec-driven-coding to create a change package first, then use $systematic-debugging on this bug
```

Finish and verify:

```text
用 $verification-before-completion 检查这个 change 是否真的可以收尾
```

```text
Use $verification-before-completion before closing this change
```

Request review:

```text
这个改动比较大，用 $requesting-code-review 做一次复核
```

```text
This is a risky change. Use $requesting-code-review before merge
```

## Repository Layout

```text
spec-driven-coding/
├── install.sh
├── LICENSE
├── README.md
├── THIRD_PARTY_NOTICES.md
└── skills/
    ├── spec-driven-coding/
    ├── frontend-design/
    ├── api-design-principles/
    ├── postgresql-table-design/
    ├── test-driven-development/
    ├── systematic-debugging/
    ├── verification-before-completion/
    └── requesting-code-review/
```

## FAQ

### Is this only for one tech stack?

No. `spec-driven-coding` is intentionally generic. It works best when you record the real project constraints in the generated `rules/` files instead of forcing one framework's conventions onto every repo.

### Why bundle other skills instead of only shipping `spec-driven-coding`?

Because most users want the workflow and the minimum useful companions together:

- TDD for new implementation
- systematic debugging for diagnosis
- verification before claiming success
- review request for risky changes

Shipping them together makes the bundle usable immediately.

### Does this bundle let `superpowers` replace the main workflow?

No. The intended rule is the opposite:

- `spec-driven-coding` owns the planning system
- execution-only skills improve how you implement and validate

### Can I remove bundled skills I do not want?

Yes. The installer copies folders independently. You can delete any bundled skill directory before installation, or remove installed skills later.

## License Notes

This repository contains both original repository-authored files and bundled third-party skill copies.

- The repository-authored files in the root of this repository are licensed under the MIT License. See [LICENSE](LICENSE).
- Bundled third-party skill folders under `skills/` are not automatically relicensed by the root MIT license.
- Any bundled skill that already includes its own license file keeps that license file in place.
- For bundled third-party source notes and packaging-time provenance, see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

If you plan to republish or redistribute this repository, review the bundled third-party skills carefully and confirm that your redistribution terms match the upstream rights you actually have.
