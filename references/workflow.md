# Workflow

Use this workflow when operating the skill inside a real repository.

This workflow remains the top-level control plane even when you also use execution-only companion skills such as TDD, debugging, verification, or code review. Those skills may improve how you execute a task, but they must not replace the `code_copilot/changes/...` package, `spec.md`, or `tasks.md`.

Operating rule: create or update the change package first, then borrow execution-only skills to improve implementation quality.

## 1. Initialize

Run `scripts/scaffold_package.py` once per repository.

Goal:

- create a stable `code_copilot/` home
- put project rules in files instead of chat history
- make future changes reproducible

## 2. Research

Before drafting a spec:

- read the relevant code paths
- record exact file paths and function names
- identify backend, frontend, database, cache, async, or external integration impact

Do not let the model invent architecture.

## 3. Propose

Create a change package with `scripts/create_change.py`.

Then fill:

- `spec.md`
- `tasks.md`
- `log.md`

Use this order inside `spec.md`:

1. Background and goal
2. Current code reality
3. Functional change points
4. API, data, and integration changes
5. Risks
6. Verification strategy
7. Open questions

Do not move to execution while open questions still block the design.

## 4. Apply

Implement task by task.

For each task:

1. State the target files.
2. Make the code change.
3. Run verification.
4. Record findings in `log.md`.

Prefer evidence over confidence statements.

If you bring in execution-oriented companion skills:

- use TDD for new feature or refactor implementation
- use systematic debugging for bug investigation
- use verification before completion as the finish gate
- use code review requests for risky or wide-scope changes

Keep them subordinate to the written spec and task list.

## 5. Review

Review in two passes:

1. Spec compliance
   Check whether the code matches `spec.md`.
2. Code quality
   Check rules, error handling, tests, security, and maintainability.

## 6. Reverse Sync

If code and spec diverge:

1. Update `spec.md`
2. Update `tasks.md`
3. Resume coding

Never silently let the code drift away from the spec.

## 7. Archive and Distill

After completion:

- move durable lessons into `knowledge/`
- keep `rules/` lean and stable
- keep one-off implementation details in change logs only
