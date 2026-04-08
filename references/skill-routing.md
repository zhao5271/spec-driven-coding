# Skill Routing

Use these companion skills to keep work specialized and consistent.

Keep this skill as the main workflow owner. Companion skills should deepen one work slice or improve execution quality, not create a second planning system.

## Frontend

Use `frontend-design` when the task includes:

- pages or components
- visual polish, layout, styling, or interaction
- forms, tables, dashboards, or admin UI

This is the default recommendation for UI-heavy implementation work.

## Backend API

Use `api-design-principles` when the task includes:

- REST API design or review
- request and response contract changes
- pagination, filtering, status codes, and error design
- API versioning or documentation decisions

This is the default recommendation for backend API design work.

## Database

Use `postgresql-table-design` when the task includes:

- PostgreSQL schema design
- table, index, foreign key, or constraint design
- JSONB, partitioning, or Postgres-specific performance patterns

If the project uses another database, adapt the design thinking carefully and avoid copying PostgreSQL-only features directly.

## Execution Discipline

Use these execution-only skills when the change package already exists and you want stronger implementation discipline:

- `test-driven-development` for new features or refactors
- `systematic-debugging` for bug investigation or flaky behavior
- `verification-before-completion` before claiming a fix or feature is complete
- `requesting-code-review` for broad, risky, or merge-sensitive changes

Do not use these to replace `spec.md`, `tasks.md`, or Reverse Sync.
