---
name: spec-driven-coding
description: >-
  Run a lightweight spec-first workflow for any repository. Use when Codex
  should scaffold or maintain `code_copilot/`, create a change package, write
  `spec.md` and `tasks.md` before implementation, enforce Reverse Sync, and
  keep planning owned by this skill while execution skills such as TDD,
  debugging, verification, and review stay subordinate. Triggers include:
  set up spec-driven coding, create a change package, write the spec first,
  spec-first workflow, create spec and tasks, new feature with spec, refactor
  with spec, bugfix with spec, 修 bug 先写 spec, 先建 change package, 先写
  spec 再动代码, 大改动先做规格和任务拆分, 用 spec-driven coding 流程走,
  先出变更包, 先写 spec 和 tasks, 先建规格包, 先进入规格驱动, 先按
  spec-first 来做.
---

# Spec-Driven Coding

## What This Skill Owns

Use this skill when planning must live in files instead of chat memory.

This skill owns:

- `code_copilot/changes/<change>/change.toml`
- `spec.md`
- `tasks.md`
- `log.md`
- Reverse Sync when implementation drifts from plan

Execution-focused skills may help with testing, debugging, verification, and review, but they must not replace this planning system.

## Good Trigger Phrases

- "set up spec-driven coding"
- "create a change package"
- "write the spec first"
- "new feature with spec"
- "refactor with spec"
- "bugfix with spec"
- "用 spec-driven coding 流程走"
- "先出变更包"
- "先写 spec 和 tasks"
- "先建规格包"
- "先进入规格驱动"
- "修 bug 先写 spec"
- "大改动先做规格和任务拆分"

Short prompts:

- "建包"
- "写规"
- "开整"
- "续做"
- "校验"
- "收尾"

## Help Output

When the user asks for `$spec-driven-coding --help`, reply with a concise command list first instead of restating the whole workflow.

Routing rule:

- Treat `$spec-driven-coding --help`, `spec-driven-coding --help`, and close variants such as `帮我看下 spec-driven-coding help` as a help request
- For a help request, return help text only
- Do not initialize `code_copilot/`
- Do not create a change package
- Do not start planning or implementation
- Do not ask approval questions unless the user follows up with an execution command

Recommended help text:

```text
$spec-driven-coding --help

可用指令：
- 建包：为当前仓库初始化 `code_copilot/`
- 写规：创建 change 并起草 `spec.md` / `tasks.md`
- 续做：扫描现有 change，恢复当前上下文
- 开整：在已有 spec / tasks 基础上推进实现
- 校验：进入 `verifying` 并检查是否满足关闭条件
- 收尾：更新状态并关闭 change

常用完整触发词：
- 用 spec-driven coding 流程走
- 先出变更包
- 先写 spec 和 tasks
- 先建规格包
- 修 bug 先写 spec

工作规则：
- No Spec, No Code
- Spec is Truth
- `tasks.md` 是执行快照
- `log.md` 是会话日志
```

Command intent:

- `建包`: initialize `code_copilot/` for the current repository
- `写规`: create a change package and draft `spec.md` plus `tasks.md`
- `续做`: inspect existing changes and rebuild the current execution context
- `开整`: continue execution from approved spec and tasks
- `校验`: move the change into verification and run close-readiness checks
- `收尾`: update final status and close the change package

If the user gives one of the short commands directly, interpret it as the matching workflow stage above.

Preferred reply order:

1. Show the short command list
2. Show the common full trigger phrases
3. Show the working rules only if they add decision value
4. End by waiting for the user to choose a command

Do not expand into the full "Main Flow" section during `--help` unless the user explicitly asks for details.

## Main Flow

### 1. Initialize

Run once per repository:

```bash
python3 scripts/scaffold_package.py --target /path/to/repo --project-name my-app
```

This creates `code_copilot/` with `rules/`, `knowledge/`, `agents/`, and `changes/templates/`.

### 2. Create a Change

```bash
python3 scripts/create_change.py \
  --target /path/to/repo \
  --name add-bulk-import \
  --title "Add bulk import flow"
```

This creates:

- `change.toml`
- `spec.md`
- `tasks.md`
- `log.md`
- `decisions.md`
- `review.md`

### 3. Plan Before Code

Fill `spec.md`, then `tasks.md`.

Minimum `spec.md` contents:

- background and goal
- current code reality with file evidence
- functional change points
- API, data, and integration changes
- risks and review points
- verification strategy
- open questions

Minimum task rules:

- every task has a stable `Task ID`
- every task has `Goal`, `Files`, `Verification`, and `Expected outcome`
- use `Depends on` for real dependencies
- `Depends on` is enforced, not advisory

### 4. Approve and Execute

After the user confirms the plan:

```bash
python3 scripts/approve_change.py --target /path/to/repo --change add-bulk-import
python3 scripts/update_change_status.py --target /path/to/repo --change add-bulk-import --status in_progress --current-task T1
```

Useful helper:

```bash
python3 scripts/update_task_fields.py --target /path/to/repo --change add-bulk-import --task-id T1 --goal "Add request validation"
```

### 5. Validate and Close

```bash
python3 scripts/update_change_status.py --target /path/to/repo --change add-bulk-import --status verifying
python3 scripts/validate_change.py --target /path/to/repo --change add-bulk-import
python3 scripts/close_change.py --target /path/to/repo --change add-bulk-import
```

## Operating Rules

- No Spec, No Code
- Spec is Truth
- Reverse Sync before more implementation
- `tasks.md` is the execution snapshot
- `log.md` is the chronological session journal
- If `tasks.md` or `log.md` is stale, fix it before continuing

## Resume Work

Use:

```bash
python3 scripts/change_catchup.py --target /path/to/repo
python3 scripts/change_catchup.py --target /path/to/repo --change add-bulk-import
python3 scripts/change_catchup.py --target /path/to/repo --list
```

Read the reported `spec.md`, `tasks.md`, and `log.md` before relying on old chat history.

## Companion Skills

- UI-heavy work: `frontend-design`
- API and contract work: `api-design-principles`
- PostgreSQL schema work: `postgresql-table-design`
- New implementation: `test-driven-development`
- Bug investigation: `systematic-debugging`
- Finish gate: `verification-before-completion`
- Risky changes: `requesting-code-review`

## References

- `references/workflow.md` for the compact end-to-end flow
- `references/spec-checklists.md` for concrete spec review questions
- `references/task-splitting-examples.md` for example decompositions
- `references/stack-conventions.md` for adapting to real repository shapes
- `references/skill-routing.md` and `references/skill-decision-table.md` for companion-skill routing
- `references/superpowers-integration.md` for conflict rules when pairing with execution-only skills
- `references/中文说明.md` for the short Chinese reading version
