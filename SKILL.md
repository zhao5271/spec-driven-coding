---
name: spec-driven-coding
description: >-
  Initialize and operate a lightweight Spec-driven coding workflow for any
  software repository. Use when Codex needs to scaffold or maintain
  `code_copilot/`, create reusable `rules/`, `knowledge/`, and
  `changes/templates/`, draft or update `spec.md` and `tasks.md` for a feature
  or bugfix, enforce Reverse Sync when implementation drifts from the plan,
  define the top-level coding workflow for a repository, or combine a
  spec-first process with execution-only companion skills such as TDD,
  debugging, verification, and code review without letting those skills replace
  the main planning flow. Trigger this skill for requests like: set up
  spec-driven coding, create a change package, write the spec first,
  spec-first workflow, create spec and tasks, new feature with spec, refactor
  with spec, bugfix with spec, 修 bug 先写 spec, 先建 change package, 先写
  spec 再动代码, or 大改动先做规格和任务拆分.
---

# Spec-Driven Coding

## Overview

Use this skill to keep coding work grounded in explicit specs instead of ad hoc chat memory. Start with a small reusable package, write the change down, split it into verifiable tasks, then code against the written plan.

This skill is the primary workflow owner. If other process-heavy skills are also available, keep this skill in charge of change-package structure, `spec.md`, `tasks.md`, and Reverse Sync.

Typical trigger phrases:

- "set up spec-driven coding"
- "create a change package"
- "write the spec first"
- "new feature with spec"
- "refactor with spec"
- "bugfix with spec"
- "先建 change package"
- "先写 spec 再动代码"
- "修 bug 先写 spec"
- "大改动先做规格和任务拆分"

## Workflow Decision Tree

1. Need to initialize a repository for Spec-driven coding?
   Run `scripts/scaffold_package.py`.

2. Need to start a real feature or bugfix?
   Run `scripts/create_change.py`, then fill `spec.md` and `tasks.md`.

3. Need help deciding what belongs in a spec?
   Read `references/workflow.md` and `references/spec-checklists.md`.

4. Need more concrete task breakdown examples?
   Read `references/task-splitting-examples.md`.

5. Need stack adaptation guidance instead of hardcoded defaults?
   Read `references/stack-conventions.md`.

6. Need to pull in the right companion skill for frontend, API, database, or Go-specialized work?
   Read `references/skill-routing.md` and `references/skill-decision-table.md`.

## Core Capabilities

### 1. Initialize the Minimal Execution Package

Create this structure inside the target repository:

```text
code_copilot/
├── agents/
├── rules/
├── knowledge/
└── changes/
    └── templates/
```

Run:

```bash
python3 scripts/scaffold_package.py \
  --target /path/to/repo \
  --project-name my-app \
  --runtime "python" \
  --backend "fastapi" \
  --frontend "react + vite" \
  --database "postgres" \
  --cache "redis"
```

Optional fields:

- `--identifier`: module name, package name, workspace name, or repo identifier
- `--async-stack`: queue, worker, stream, or job stack
- `--test-command`: default validation command for the repository

The script creates:

- `rules/project-context.md`
- `rules/coding-style.md`
- `rules/security.md`
- `rules/domain-rules.md`
- `rules/api-contracts.md`
- `rules/response-pattern.md`
- `rules/recommended-skills.md`
- `rules/skill-decision-table.md`
- `knowledge/index.md`
- `agents/copilot-prompt.md`
- `agents/execution-sop.md`
- `changes/templates/spec.md`
- `changes/templates/tasks.md`
- `changes/templates/log.md`
- `changes/templates/task-examples/api-endpoint-tasks.md`
- `changes/templates/task-examples/ui-flow-tasks.md`
- `changes/templates/task-examples/background-job-tasks.md`
- `changes/templates/task-examples/data-migration-tasks.md`
- `changes/templates/examples/api-change.md`
- `changes/templates/examples/ui-change.md`
- `changes/templates/examples/async-job-change.md`
- `changes/templates/examples/data-migration-change.md`

### 2. Create a New Change Package

Create a change directory before coding:

```bash
python3 scripts/create_change.py \
  --target /path/to/repo \
  --name add-bulk-import \
  --title "Add bulk import flow"
```

This creates:

- `code_copilot/changes/add-bulk-import/spec.md`
- `code_copilot/changes/add-bulk-import/tasks.md`
- `code_copilot/changes/add-bulk-import/log.md`

Then:

1. Fill `spec.md` with current facts and boundaries.
2. Split the work into atomic tasks in `tasks.md`.
3. Start implementation only after the user confirms the spec.

### 3. Draft Good Specs

Use this minimum structure in `spec.md`:

- Background and goal
- Current code reality with file-path evidence
- Functional changes
- API, data, and integration changes
- Risks and review points
- Test and verification strategy
- Open questions

Read `references/spec-checklists.md` when the change touches:

- public APIs or client contracts
- database schema or migrations
- cache, jobs, queues, or async workers
- frontend pages, forms, or state flows
- authentication, authorization, or sensitive data
- deployment, config, or rollout behavior

### 4. Split Work into Atomic Tasks

Keep tasks small and verifiable:

- Prefer one task per clear intent.
- Prefer 3 to 5 files per task.
- Name concrete files, entry points, and target functions.
- Attach one verification method per task.

Good task names:

- Add request schema and boundary validation
- Implement service branch for retry-safe import
- Add repository query and migration for status index
- Update client request mapping and result rendering

Avoid vague task names:

- Finish backend
- Handle everything in worker
- Complete frontend updates

### 5. Enforce Reverse Sync

When implementation diverges from the plan:

1. Stop coding.
2. Update `spec.md` first.
3. Update `tasks.md` if the execution path changed.
4. Resume implementation only after the written plan matches reality.

Treat these as hard rules:

- No Spec, No Code
- Spec is Truth
- Reverse Sync

### 6. Adapt to Repository Reality

This skill is intentionally generic. Do not force one stack's conventions onto another repository.

Always record the real project constraints in `rules/project-context.md`:

- runtime and package layout
- backend and frontend entry points
- shared contracts and generated clients
- test, build, and migration commands
- deployment, config, and secret boundaries

Put stable domain rules in `rules/` and durable business knowledge in `knowledge/`. Keep one-off implementation details inside each change log.

## Companion Skills

Use companion skills deliberately based on the work slice.

- Use `frontend-design` for pages, components, styling, interaction, and UI-heavy changes.
- Use `api-design-principles` for API design, contract review, pagination, filtering, and error responses.
- Use `postgresql-table-design` for PostgreSQL schema, indexing, constraints, and JSONB or partitioning design.

### Execution Pairing With Superpowers

Use this skill as the top-level workflow and only borrow execution-focused skills from `superpowers`.

Approved pairings:

- New feature or refactor: `test-driven-development` plus `verification-before-completion`
- Bug investigation or flaky behavior: `systematic-debugging` plus `verification-before-completion`
- Large change or risky merge candidate: `requesting-code-review`

Keep responsibilities split like this:

- `spec-driven-coding` owns change-package creation, spec boundaries, task decomposition, and Reverse Sync
- Execution-focused companion skills own testing discipline, debugging method, validation rigor, and review requests

Do not let `superpowers` replace the main plan:

- Do not use `using-superpowers` as the top-level rule system
- Do not maintain two planning systems in parallel, such as `code_copilot/changes/...` and `docs/superpowers/plans/...`
- Do not let `writing-plans` replace `code_copilot/changes/<change-name>/tasks.md`

If instructions conflict, prefer this skill's document locations and change-management rules. `spec.md` remains the single source of truth.

Read `references/superpowers-integration.md` when you need the fuller pairing guide, conflict rules, or scenario recipes.

## Execution Recipes

Use these default operating sequences unless the repository has a better established workflow:

### New Feature or Refactor

1. Create the change package with `scripts/create_change.py`
2. Write or update `spec.md`
3. Split the work in `tasks.md`
4. Implement with `test-driven-development`
5. Verify with `verification-before-completion`

### Bugfix

1. Create or update the change package
2. Record the current understanding and failure shape in `spec.md`
3. Update `tasks.md` with the investigation and fix path
4. Investigate with `systematic-debugging`
5. Verify with `verification-before-completion`

### Large or High-Risk Change

1. Keep the change package current
2. Finish implementation against the written tasks
3. Request review with `requesting-code-review`
4. If review changes the plan, update `spec.md` and `tasks.md` before continuing

## References

- Read `references/workflow.md` for the end-to-end operating model.
- Read `references/spec-checklists.md` when drafting or reviewing a concrete change package.
- Read `references/stack-conventions.md` when adapting the workflow to an existing runtime, framework, and repo layout.
- Read `references/task-splitting-examples.md` when you need more concrete task decomposition.
- Read `references/skill-routing.md` when you need to choose the right companion skill.
- Read `references/skill-decision-table.md` when you want the compact routing view.
- Read `references/superpowers-integration.md` when combining this skill with execution-focused `superpowers` skills.
- Read `references/中文说明.md` when you want a longer Chinese reading version.
