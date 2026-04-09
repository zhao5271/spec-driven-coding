#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def write_file(path: Path, content: str, force: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return f"skip {path}"
    path.write_text(content, encoding="utf-8")
    return f"write {path}"


def copy_template_tree(src: Path, dst: Path, force: bool) -> list[str]:
    outputs: list[str] = []
    if not src.exists():
        return outputs
    for template in sorted(src.rglob("*")):
        if template.is_dir():
            continue
        target = dst / template.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            outputs.append(f"skip {target}")
            continue
        target.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
        outputs.append(f"write {target}")
    return outputs


def value_or_todo(value: str) -> str:
    return value or "TODO"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a minimal Spec-driven coding package for any repository."
    )
    parser.add_argument("--target", required=True, help="Target repository path")
    parser.add_argument("--project-name", required=True, help="Human-readable project name")
    parser.add_argument(
        "--identifier",
        default="",
        help="Module, package, workspace, or repository identifier",
    )
    parser.add_argument(
        "--runtime",
        default="",
        help="Primary runtime or language, e.g. go, python, node, java",
    )
    parser.add_argument(
        "--backend",
        default="",
        help="Backend stack, e.g. gin, fastapi, spring boot, rails",
    )
    parser.add_argument(
        "--frontend",
        default="",
        help="Frontend stack, e.g. react + next.js, vue3 + vite",
    )
    parser.add_argument(
        "--database",
        default="",
        help="Primary database, e.g. postgres, mysql, sqlite",
    )
    parser.add_argument("--cache", default="", help="Primary cache, e.g. redis")
    parser.add_argument(
        "--async-stack",
        default="",
        help="Queue, worker, or async stack, e.g. celery, sidekiq, kafka",
    )
    parser.add_argument(
        "--test-command",
        default="",
        help="Default test or verification command for the repository",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    repo = Path(args.target).expanduser().resolve()
    root = repo / "code_copilot"

    files = {
        root / "rules" / "project-context.md": f"""# Project Context

- Project name: {args.project_name}
- Identifier: {value_or_todo(args.identifier)}
- Runtime or language: {value_or_todo(args.runtime)}
- Backend stack: {value_or_todo(args.backend)}
- Frontend stack: {value_or_todo(args.frontend)}
- Primary database: {value_or_todo(args.database)}
- Cache: {value_or_todo(args.cache)}
- Async stack: {value_or_todo(args.async_stack)}
- Default test command: {value_or_todo(args.test_command)}

## Directory Notes

- Describe the real entry points here.
- Describe where handlers, services, jobs, repositories, or controllers live.
- Describe where the frontend application or clients live.
- Describe where migrations, schemas, configs, and deployment files live.
- Describe shared contracts, generated clients, or SDKs here.

## Suggested Mapping

- App entry points:
- Domain modules:
- API layer:
- Persistence layer:
- Jobs, queues, or async workers:
- UI, mobile, or client apps:
- Build, test, and deployment files:
""",
        root / "rules" / "coding-style.md": """# Coding Style

- Keep boundary code thin and business logic explicit.
- Prefer small functions with clear ownership.
- Wrap or annotate errors when they cross boundaries.
- Add tests for changed behavior, not only happy paths.
- Keep naming aligned across API, storage, and client layers.
- Prefer reversible changes over wide untracked edits.
""",
        root / "rules" / "security.md": """# Security

- Do not hardcode secrets, tokens, or private keys.
- Do not log sensitive user data or secrets.
- Validate external input at the boundary layer.
- Highlight auth, money, permissions, and destructive operations for manual review.
- Record rollout, fallback, and incident-sensitive changes explicitly.
""",
        root / "rules" / "domain-rules.md": """# Domain Rules

- Record business rules that the model should not guess.
- Record state-machine boundaries here.
- Record idempotency, retry, timeout, and compensation rules here.
- Record API, event, and client contract conventions here.
- Record cache keys, TTLs, and invalidation rules here when relevant.

## Suggested Sections

### Contract Rules

- Request and response field naming
- Error code and message rules
- Pagination, filtering, or event payload conventions

### Data Rules

- Ownership of tables, collections, or files
- Transaction or consistency boundaries
- Schema constraints and migration safety notes

### Async Rules

- Retry policy
- Idempotency keys
- Dead-letter or failure handling

### Frontend or Client Rules

- API wrapper location
- State ownership
- Form, table, and enum mapping conventions
""",
        root / "rules" / "api-contracts.md": """# API Contracts

## Recommended Response Envelope

- `code`: business status code when the repository uses one
- `message`: readable status message
- `data`: payload object, list, or result envelope
- `requestId`: request trace identifier when available

## Common Pagination Fields

- `page`
- `pageSize`
- `total`
- `list`

## Contract Stability Rules

- Keep field names stable across producers and consumers.
- Distinguish validation failures from business errors.
- Record null, empty-list, and default-value behavior explicitly.
- Define versioning or compatibility expectations before changing public contracts.
""",
        root / "rules" / "response-pattern.md": """# Response Pattern

Document the repository's stable response and result shapes here.

## Suggested JSON Response Shape

```json
{
  "code": 0,
  "message": "ok",
  "data": {},
  "requestId": "trace-123"
}
```

## Suggested Pagination Shape

```json
{
  "page": 1,
  "pageSize": 20,
  "total": 200,
  "list": []
}
```

If the repository already has a different stable standard, record that standard instead of forcing this example.
""",
        root / "rules" / "recommended-skills.md": """# Recommended Skills Routing

Use these companion skills when the change crosses specific domains.

## Frontend Work

Use `frontend-design` when the task involves:

- pages or components
- visual design, layout, styling, or interaction
- forms, tables, dashboards, or admin UI

## Backend API Work

Use `api-design-principles` when the task involves:

- REST API design
- request or response contract changes
- pagination, filtering, or error-response design
- API review before implementation

## Database Work

Use `postgresql-table-design` when the task involves:

- PostgreSQL table or index design
- constraints, foreign keys, or schema review
- JSONB, partitioning, or Postgres-specific performance design

## Execution Discipline

Use these execution-only skills after a change package exists:

- New feature or refactor:
  `test-driven-development`
- Bug investigation or flaky behavior:
  `systematic-debugging`
- Final completion gate:
  `verification-before-completion`
- Explicit review handoff:
  `requesting-code-review`

Do not let these replace `spec.md`, `tasks.md`, or Reverse Sync.
""",
        root / "rules" / "skill-decision-table.md": """# Skill Decision Table

## Quick Routing

- Frontend page, component, styling, interaction:
  `frontend-design`
- Backend API, contract, pagination, error response:
  `api-design-principles`
- PostgreSQL schema, indexes, constraints:
  `postgresql-table-design`
- New feature or refactor implementation:
  `test-driven-development`
- Bug investigation or flaky behavior:
  `systematic-debugging`
- Final verification before claiming success:
  `verification-before-completion`
- Risky or wide-scope change needing review:
  `requesting-code-review`

## Mixed Work

- Frontend + backend API:
  Use `frontend-design` and `api-design-principles` together.
- Backend API + database:
  Use `api-design-principles` and `postgresql-table-design` together.
- Fullstack feature:
  Start with this skill, then route sub-parts by domain.
""",
        root / "knowledge" / "index.md": """# Knowledge Index

- Add stable domain knowledge here first.
- Split into topic files only after real accumulation.

## Suggested Topics

- business state rules
- integration edge cases
- cache invalidation rules
- migration pitfalls
- async retry and idempotency rules
- recurring UI or workflow pitfalls
""",
        root / "agents" / "copilot-prompt.md": """# Copilot Prompt

You are an engineering partner operating under a Spec-driven workflow.

Always:

1. Read `rules/` first.
2. Check whether a change package already exists.
3. Use spec and tasks as the source of truth.
4. Stop and ask when facts are missing.
5. Update docs first when implementation diverges from the plan.
6. Route UI-heavy work to `frontend-design`.
7. Route API contract work to `api-design-principles`.
8. Route PostgreSQL schema work to `postgresql-table-design`.
9. Use `test-driven-development` for new feature and refactor implementation after planning.
10. Use `systematic-debugging` for bug investigation before patching.
11. Use `verification-before-completion` before claiming completion.
12. Use `requesting-code-review` for risky changes that need an explicit review checkpoint.
13. Before each meaningful implementation slice, update `Current task` and mark the matching task `in_progress`.
14. After each meaningful implementation or verification slice, immediately refresh `Next task`, `Blockers`, resume fields, and `log.md`.
15. Treat stale `tasks.md` or `log.md` as a process bug and fix them before continuing.
""",
        root / "agents" / "execution-sop.md": """# Spec-Driven Execution SOP

Operating rule: create or update the change package first, then borrow execution-only skills for implementation discipline.

Operating mode: light-auto. Progress updates happen during execution, not as an end-of-session cleanup task.

## Step 1

Read `rules/`, `knowledge/`, and any existing change package first.

## Step 2

Write or update `spec.md` with real file-path evidence.

## Step 3

Split the work into atomic tasks in `tasks.md`.

## Step 4

Route the work to the right companion skill:

- Frontend: `frontend-design`
- Backend API: `api-design-principles`
- PostgreSQL: `postgresql-table-design`

Add execution discipline when appropriate:

- New feature or refactor: `test-driven-development`
- Bug investigation: `systematic-debugging`
- Final completion gate: `verification-before-completion`
- Review checkpoint: `requesting-code-review`

## Step 5

Implement task by task.

For every meaningful work slice:

1. Update `Current task` and task status before coding.
2. Make the code change.
3. Run verification.
4. Immediately update `Next task`, `Blockers`, and the resume checklist in `tasks.md`.
5. Immediately append the result to `log.md`.

## Step 6

If implementation diverges from the plan, update `spec.md` and `tasks.md` first.

## Step 7

Review spec compliance, code quality, and verification evidence before closing the change.

Before any completion claim, make sure `tasks.md` and `log.md` already reflect the final known state.
""",
    }

    outputs = [write_file(path, content, args.force) for path, content in files.items()]
    template_root = Path(__file__).resolve().parent.parent / "templates" / "changes"
    outputs.extend(copy_template_tree(template_root, root / "changes" / "templates", args.force))
    print("\n".join(outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
