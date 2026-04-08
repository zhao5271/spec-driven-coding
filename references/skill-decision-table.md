# Skill Decision Table

Use this table when deciding which companion skill to pull in.

| Work slice | Recommended skill | Why |
| --- | --- | --- |
| Page, component, styling, interaction | `frontend-design` | Better UI quality and stronger frontend execution |
| Backend API route, contract, pagination, errors | `api-design-principles` | Better API consistency and contract quality |
| PostgreSQL schema, indexes, constraints, JSONB, partitioning | `postgresql-table-design` | Better database correctness and performance design |
| New feature or refactor implementation after planning | `test-driven-development` | Stronger incremental implementation discipline |
| Bug investigation, flaky test, unexpected behavior | `systematic-debugging` | Better root-cause isolation before patching |
| Final completion gate before claiming success | `verification-before-completion` | Forces explicit verification evidence |
| Wide-scope or risky change that needs review | `requesting-code-review` | Adds an explicit review checkpoint before merge or handoff |
| Mixed feature across UI + API + DB | Start with this skill, then combine the matching companion skills | Keeps planning unified while allowing domain-specific depth |

## Fast Rules

- If the task changes how the user sees or interacts with a page, use `frontend-design`.
- If the task changes how the client calls or receives data, use `api-design-principles`.
- If the task changes tables, indexes, constraints, or SQL access paths, use `postgresql-table-design`.
- If the change package is ready and you are starting new implementation work, consider `test-driven-development`.
- If the current problem is primarily diagnostic, consider `systematic-debugging`.
- If you are about to declare completion, consider `verification-before-completion`.
- If the change is risky enough to merit an explicit review handoff, consider `requesting-code-review`.
