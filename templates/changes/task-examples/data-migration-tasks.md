# Task Example - Data Migration

## Task 1
- Goal: Add schema or data migration with rollback notes.
- Files: `migrations/...`, `db/...`
- Verification: Migration applies and rolls back cleanly in a test environment.

## Task 2
- Goal: Update read and write paths to match the new data shape.
- Files: `server/repositories/...`, `server/services/...`
- Verification: Old and new records behave correctly during rollout.

## Task 3
- Goal: Add rollout checks, monitoring notes, or cleanup tasks.
- Files: `code_copilot/changes/.../spec.md`, `ops/...`
- Verification: Rollout checklist covers drift, errors, and fallback signals.
