# Superpowers Integration

Use this when `spec-driven-coding` is the main workflow and execution-only `superpowers` skills are assisting.

## Non-Negotiable Rules

- `spec-driven-coding` owns the planning system
- `spec.md` stays the plan of record
- `tasks.md` stays the execution checklist of record
- execution skills must not replace `code_copilot/changes/...`

## Allowed Pairings

- `test-driven-development`
- `systematic-debugging`
- `verification-before-completion`
- `requesting-code-review`

## Do Not Substitute

Do not replace this workflow with:

- another top-level rule system
- another task-plan location
- a parallel planning workflow outside `code_copilot/changes/...`

## Conflict Rule

If an execution skill suggests a path that differs from the written plan:

1. update `spec.md`
2. update `tasks.md`
3. continue implementation
