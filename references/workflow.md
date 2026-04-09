# Workflow

Use this when operating `spec-driven-coding` inside a real repository.

## Core Rule

`spec-driven-coding` owns the planning system:

- `change.toml`
- `spec.md`
- `tasks.md`
- `log.md`

Execution-only skills may help, but they must not replace this structure.

## End-to-End Flow

### 1. Initialize

Run once per repository:

```bash
python3 scripts/scaffold_package.py --target /path/to/repo --project-name my-app
```

### 2. Research

Before drafting a spec:

- read the relevant code paths
- record real file paths and entry points
- identify API, database, cache, async, or UI impact

### 3. Create and Plan

Create a change package:

```bash
python3 scripts/create_change.py --target /path/to/repo --name add-bulk-import --title "Add bulk import flow"
```

Then fill:

- `spec.md`
- `tasks.md`
- `log.md`

After the user confirms the plan:

```bash
python3 scripts/approve_change.py --target /path/to/repo --change add-bulk-import
```

### 4. Execute

Move into implementation:

```bash
python3 scripts/update_change_status.py --target /path/to/repo --change add-bulk-import --status in_progress --current-task T1
```

Useful helper:

```bash
python3 scripts/update_task_fields.py --target /path/to/repo --change add-bulk-import --task-id T1 --goal "Add request validation"
```

Rules:

- `Task ID` is required
- `Depends on` is enforced
- do not start a task until its dependencies are `done`
- update `tasks.md` and `log.md` during execution, not afterward

### 5. Verify and Close

```bash
python3 scripts/update_change_status.py --target /path/to/repo --change add-bulk-import --status verifying
python3 scripts/validate_change.py --target /path/to/repo --change add-bulk-import
python3 scripts/close_change.py --target /path/to/repo --change add-bulk-import
```

### 6. Reverse Sync

If implementation drifts from the plan:

1. update `spec.md`
2. update `tasks.md`
3. continue coding

## Resume

```bash
python3 scripts/change_catchup.py --target /path/to/repo
python3 scripts/change_catchup.py --target /path/to/repo --change add-bulk-import
python3 scripts/change_catchup.py --target /path/to/repo --list
```

Read the reported files before relying on old chat history.
