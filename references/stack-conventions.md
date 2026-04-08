# Stack Conventions

This skill is intentionally generic. Use this guide to adapt the workflow to the real repository instead of forcing one preferred stack.

## What to Record Early

Put these facts in `rules/project-context.md` as soon as they are known:

- primary runtime or language
- package, app, or workspace layout
- main server or job entry points
- frontend, mobile, or consumer app locations
- database, migration, and schema ownership
- build, test, lint, and deployment commands

## How to Adapt the Templates

- Replace placeholder paths with real paths from the repository.
- Replace generic API language with the repo's real contract style.
- Replace database notes with the repo's real storage model.
- Replace test commands with the commands that actually exist.

## Common Repository Shapes

### Backend service only

Focus on:

- entry points
- API or event contracts
- persistence rules
- deployment and observability

### Frontend app only

Focus on:

- page and component ownership
- state management boundaries
- API client conventions
- test and build commands

### Fullstack monorepo

Focus on:

- shared contracts
- frontend and backend release coupling
- migration sequencing
- end-to-end verification paths

### Worker or data pipeline

Focus on:

- job triggers
- payload contracts
- retries, timeouts, and idempotency
- operator visibility and failure recovery

## Specialize When It Helps

If the repo clearly matches an existing opinionated skill, use that skill instead of stretching this one too far.
