# Spec-Driven Coding

`spec-driven-coding` is a spec-first workflow for Codex that keeps planning in files instead of chat memory.

Use it when you want a repeatable flow like:

`spec.md -> tasks.md -> implementation -> verification`

It is designed to help you:

- initialize a repository with a reusable `code_copilot/` workflow package
- create a change package before coding
- keep `spec.md` and `tasks.md` as the source of truth during execution
- recover context cleanly when a session resumes

## Quick Start

Install the main skill from GitHub:

```bash
npx skills add zhao5271/spec-driven-coding -g -y
```

Install the full bundle from this repository:

```bash
git clone git@github.com:zhao5271/spec-driven-coding.git
cd spec-driven-coding
./install.sh
```

Choose the root skill install if you only want the main workflow.

Choose the bundle install if you also want the companion skills included in this repository.

## First Prompt

Initialize a repository:

```text
用 $spec-driven-coding 为这个仓库初始化 code_copilot
```

Start a new change:

```text
用 $spec-driven-coding 先为“用户批量导入”创建 change package，再写 spec 和 tasks
```

Ask for help:

```text
$spec-driven-coding --help
```

## Workflow Cheatsheet

The short command sequence is:

`建包 -> 写规 -> 开整 -> 续做 -> 校验 -> 收尾`

- `建包`: initialize `code_copilot/` for the current repository
- `写规`: create a change and draft `spec.md` and `tasks.md`
- `开整`: continue implementation from the approved plan
- `续做`: scan existing changes and recover execution context
- `校验`: move the change into verification and check close readiness
- `收尾`: close the change package

## What This Creates

When you initialize a repository, the workflow creates a `code_copilot/` package with:

- `rules/` for stable project rules
- `knowledge/` for durable project knowledge
- `agents/` for reusable execution guidance
- `changes/templates/` for change-package templates

When you start a real feature or bugfix, the workflow creates:

- `change.toml`
- `spec.md`
- `tasks.md`
- `log.md`
- `decisions.md`
- `review.md`

The working rule is simple:

- no spec before code
- `spec.md` is the plan
- `tasks.md` is the execution snapshot
- `log.md` is the chronological record

## Included Skills

Main workflow:

- `spec-driven-coding`

Companion skills in the full bundle:

- `frontend-design` for UI-heavy work
- `api-design-principles` for API and contract work
- `postgresql-table-design` for PostgreSQL schema work
- `test-driven-development` for new implementation and refactors
- `systematic-debugging` for bug investigation
- `verification-before-completion` for finish-gate validation
- `requesting-code-review` for risky changes

## Core Scripts

The root skill ships these workflow scripts:

```bash
python3 scripts/scaffold_package.py --target /path/to/repo --project-name my-app
python3 scripts/create_change.py --target /path/to/repo --name add-bulk-import --title "Add bulk import flow"
python3 scripts/approve_change.py --target /path/to/repo --change add-bulk-import
python3 scripts/update_change_status.py --target /path/to/repo --change add-bulk-import --status in_progress --current-task T1
python3 scripts/change_catchup.py --target /path/to/repo --change add-bulk-import
python3 scripts/validate_change.py --target /path/to/repo --change add-bulk-import
python3 scripts/close_change.py --target /path/to/repo --change add-bulk-import
```

## Install Options

Two supported ways to use this project:

- `npx skills add zhao5271/spec-driven-coding -g -y`
  This installs the root workflow skill from GitHub.
- `git clone ... && ./install.sh`
  This installs the full bundle, including companion skills.

If you want a pinned release, use a Git tag or a specific repository revision in your own install workflow.

More detail is in [references/public-install-and-release.md](references/public-install-and-release.md).

## FAQ

### Does this require a specific tech stack?

No. The workflow is intentionally generic. It works best when you record the real stack details in the generated `rules/` files.

### Do I need the full bundle?

No. If you only want the main planning workflow, install the root skill. Use the full bundle if you want the companion skills ready to go.

### Can I use it with other execution-focused skills?

Yes. That is the intended model. `spec-driven-coding` owns planning, while execution-focused skills improve testing, debugging, verification, or review.

### What should I type first?

Usually one of these:

```text
用 $spec-driven-coding 为这个仓库初始化 code_copilot
```

```text
用 $spec-driven-coding 先写 spec 和 tasks，再开始改这个功能
```

### Where can I read more?

- `references/workflow.md`
- `references/spec-checklists.md`
- `references/task-splitting-examples.md`
- `references/stack-conventions.md`
- `references/skill-routing.md`
- `references/skill-decision-table.md`
- `references/superpowers-integration.md`
- `references/中文说明.md`
