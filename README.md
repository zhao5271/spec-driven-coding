# Spec-Driven Coding Bundle

Spec-first coding workflow for Codex, bundled with the execution-only companion skills needed for feature work, debugging, verification, and review.

This repo is meant to be a publish-ready, open-the-box bundle:

- `spec-driven-coding` is the main workflow skill
- companion skills are bundled locally so users do not need to hunt them down one by one
- install is a single script

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

## What This Bundle Solves

Use this bundle when you want a spec-first workflow without letting other process-heavy skills take over the top-level plan.

The intended split is:

- `spec-driven-coding` owns `spec.md`, `tasks.md`, change packages, and Reverse Sync
- bundled execution skills improve how code gets implemented, debugged, verified, and reviewed

## Quick Start

Clone the repo, then install all bundled skills into Codex:

```bash
git clone <your-repo-url>
cd spec-driven-coding-bundle
./install.sh
```

Default install target:

```text
${CODEX_HOME:-$HOME/.codex}/skills
```

Install to a custom target:

```bash
./install.sh --target /path/to/skills
```

Overwrite an existing install:

```bash
./install.sh --force
```

## Shortest Prompt Cheat Sheet

These are the shortest prompts that still steer Codex into the intended workflow.

### Initialize a Repository

```text
用 $spec-driven-coding 为这个仓库初始化 code_copilot
```

```text
Use $spec-driven-coding to scaffold code_copilot for this repo
```

### Start a New Feature

```text
用 $spec-driven-coding 先为“用户批量导入”创建 change package，再按 TDD 实现
```

```text
Use $spec-driven-coding to create a change package for "bulk user import", then implement it with TDD
```

### Start a Refactor

```text
用 $spec-driven-coding 先写 spec 和 tasks，再重构这个模块
```

```text
Use $spec-driven-coding to write spec and tasks first, then refactor this module
```

### Fix a Bug

```text
用 $spec-driven-coding 先建 change package，用 $systematic-debugging 排查这个 bug
```

```text
Use $spec-driven-coding to create a change package first, then use $systematic-debugging on this bug
```

### Finish and Verify

```text
用 $verification-before-completion 检查这个 change 是否真的可以收尾
```

```text
Use $verification-before-completion before closing this change
```

### Ask for Review

```text
这个改动比较大，用 $requesting-code-review 做一次复核
```

```text
This is a risky change. Use $requesting-code-review before merge
```

## Recommended Usage Patterns

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

## Repository Layout

```text
spec-driven-coding-bundle/
├── install.sh
├── README.md
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

## Publishing Notes

- This bundle contains copied companion skills so users can install everything at once.
- The bundled `spec-driven-coding` copy has been made portable by removing machine-specific skill paths.
- If you publish this repo publicly, verify the redistribution terms of bundled third-party skills and preserve any upstream license files that are already included.
