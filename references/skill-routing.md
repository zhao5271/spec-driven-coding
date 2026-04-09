# Skill Routing

Use this file when you want a short explanation of which companion skill fits a work slice.

Keep `spec-driven-coding` as the workflow owner. Companion skills help one slice of work or improve execution quality; they do not replace `change.toml`, `spec.md`, `tasks.md`, or Reverse Sync.

## Domain Routing

### Frontend

Use `frontend-design` for:

- pages and components
- layout, styling, and interaction
- forms, tables, dashboards, and admin UI

### Backend API

Use `api-design-principles` for:

- request or response contract work
- REST API design or review
- pagination, filtering, and error-response design

### Database

Use `postgresql-table-design` for:

- schema and index design
- constraints and foreign keys
- PostgreSQL-specific patterns such as JSONB and partitioning

## Execution Routing

Use these only after a change package exists:

- `test-driven-development` for new implementation or refactor work
- `systematic-debugging` for diagnosis and flaky behavior
- `verification-before-completion` before claiming completion
- `requesting-code-review` for risky or wide-scope changes

## Routing Rule

If multiple domains are involved, keep planning here and pull in only the companion skills that match the current slice.
