# Task Example - Background Job

## Task 1
- Goal: Add job creation entry point and payload validation.
- Files: `server/routes/...`, `server/jobs/...`
- Verification: Job creation returns a stable job identifier.

## Task 2
- Goal: Implement worker-side execution, retries, and status updates.
- Files: `worker/...`, `server/services/...`
- Verification: Success and failure paths update job status correctly.

## Task 3
- Goal: Add operator or user-facing visibility for job progress.
- Files: `web/src/pages/...`, `server/routes/...`
- Verification: Users can see progress and completion state.
