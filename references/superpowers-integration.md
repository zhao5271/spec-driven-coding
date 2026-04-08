# Superpowers Integration

Use this reference when `spec-driven-coding` is the main workflow and `superpowers` skills are only allowed to enhance execution.

## Core Rule

- `spec-driven-coding` owns the top-level workflow
- `spec.md` is the only plan of record
- `tasks.md` is the execution checklist of record
- `superpowers` may improve execution quality but must not replace the planning system

## Approved Superpowers Skills

- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`

These are execution aids, not workflow owners.

## Disallowed Workflow Substitutions

Do not use these as replacements for this skill's main structure:

- `using-superpowers` as the top-level rule system
- `writing-plans` as the source of implementation tasks
- `docs/superpowers/plans/...` as a parallel plan location when `code_copilot/changes/...` already exists

## Conflict Resolution

If `spec-driven-coding` and a `superpowers` skill disagree:

1. Keep `code_copilot/changes/<change-name>/spec.md` as the canonical plan
2. Keep `code_copilot/changes/<change-name>/tasks.md` as the canonical task list
3. Use the `superpowers` skill only for execution technique
4. If implementation drifts, perform Reverse Sync here first, then continue

## Recommended Pairings

### New Feature or Refactor

- Main workflow: `spec-driven-coding`
- Execution support: `test-driven-development`
- Finish gate: `verification-before-completion`

Suggested sequence:

1. Create the change package
2. Confirm scope and boundaries in `spec.md`
3. Break down work in `tasks.md`
4. Implement task-by-task with TDD
5. Run final verification before claiming completion

### Bugfix

- Main workflow: `spec-driven-coding`
- Investigation support: `systematic-debugging`
- Finish gate: `verification-before-completion`

Suggested sequence:

1. Capture the observed failure and suspected scope in `spec.md`
2. Add investigation and fix tasks to `tasks.md`
3. Debug systematically before patching
4. Update the written plan if the root cause differs from the original theory
5. Verify before claiming the bug is fixed

### Large or Risky Change

- Main workflow: `spec-driven-coding`
- Review support: `requesting-code-review`

Suggested sequence:

1. Keep spec and tasks current during implementation
2. Finish the intended task set
3. Request code review
4. If review changes scope or design, update the spec before further coding

## Practical Rules

- No Spec, No Code
- Spec is Truth
- Reverse Sync before resuming implementation
- One planning system per change
- `superpowers` improves execution quality, not planning ownership
