# Spec-Driven Coding

Spec-first coding workflow for Codex.

Use it when you want planning to live in files instead of chat memory:

- `change.toml` for machine-readable change state
- `spec.md` for the plan
- `tasks.md` for the execution snapshot
- `log.md` for chronological progress

## 30-Second Start

Remember this line:

`建包 -> 写规 -> 开做 -> 续做 -> 校验 -> 收尾`

Meaning:

- `建包`: create the change package
- `写规`: write or refine `spec.md`
- `开做`: move into execution with approved plan
- `续做`: resume with `change_catchup.py`
- `校验`: run `validate_change.py`
- `收尾`: close with `close_change.py`

## Quick Start

Install the main skill:

```bash
npx skills add zhao5271/spec-driven-coding -g -y
```

Or install the full bundle:

```bash
git clone git@github.com:zhao5271/spec-driven-coding.git
cd spec-driven-coding
./install.sh
```

## Fastest Way To Use It

Initialize a repository:

```text
用 $spec-driven-coding 为这个仓库初始化 code_copilot
```

Core commands:

```bash
python3 scripts/create_change.py --target /path/to/repo --name add-bulk-import --title "Add bulk import flow"
python3 scripts/update_task_fields.py --target /path/to/repo --change add-bulk-import --task-id T1 --goal "Add request validation"
python3 scripts/approve_change.py --target /path/to/repo --change add-bulk-import
python3 scripts/update_change_status.py --target /path/to/repo --change add-bulk-import --status in_progress --current-task T1
python3 scripts/validate_change.py --target /path/to/repo --change add-bulk-import
python3 scripts/close_change.py --target /path/to/repo --change add-bulk-import
```

`Depends on` in `tasks.md` is enforced. If `T2` depends on `T1`, `T2` cannot start until `T1` is `done`.

## Mnemonic

Use these short prompts:

- `建包`
- `写规`
- `开做`
- `续做`
- `校验`
- `收尾`

Meaning:

- `建包`: create the change package
- `写规`: write or refine `spec.md`
- `开做`: move from planning into execution
- `续做`: resume with `change_catchup.py`
- `校验`: run `validate_change.py`
- `收尾`: close with `close_change.py`

## Execution Order

1. `create_change.py`
2. fill `spec.md` and `tasks.md`
3. `approve_change.py`
4. `update_change_status.py --status in_progress --current-task T1`
5. implement and verify
6. `update_change_status.py --status verifying`
7. `validate_change.py`
8. `close_change.py`

## What Gets Created

Each change package contains:

- `change.toml`
- `spec.md`
- `tasks.md`
- `log.md`
- `decisions.md`
- `review.md`

## Included Skills

Main workflow:

- `spec-driven-coding`

Companions:

- `frontend-design`
- `api-design-principles`
- `postgresql-table-design`
- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`

## Repository Layout

```text
spec-driven-coding/
├── SKILL.md
├── agents/
├── references/
├── scripts/
├── templates/
└── skills/
```

## References

- `references/workflow.md`
- `references/spec-checklists.md`
- `references/task-splitting-examples.md`
- `references/stack-conventions.md`
- `references/skill-routing.md`
- `references/skill-decision-table.md`
- `references/superpowers-integration.md`
- `references/中文说明.md`
