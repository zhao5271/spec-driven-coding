# Spec Checklists

Use these checklists when drafting or reviewing a concrete change package.

## API or Contract Changes

- Which producers and consumers are affected?
- Are request and response field changes backward compatible?
- Are validation failures distinct from business failures?
- Is pagination, filtering, sorting, or cursor behavior defined?
- Are empty, null, and default values explicit?

## Database or Migration Changes

- Which tables, collections, indexes, or files are affected?
- Is there a migration, backfill, or cleanup step?
- What is the rollback plan?
- Are read and write paths compatible during rollout?
- Is lock, performance, or data-correctness risk called out?

## Cache Changes

- What keys are added or changed?
- What are the TTL and invalidation triggers?
- What happens on cache miss or stale data?
- Can cache behavior hide or delay correctness bugs?

## Async or Worker Changes

- What triggers the job or event?
- What is the payload contract?
- What are retry, timeout, and idempotency expectations?
- How is failure surfaced to operators or users?
- What monitoring or status visibility is required?

## Frontend or Client Changes

- Which screens, states, or flows change?
- What are the loading, empty, validation, and error states?
- Are API contract changes reflected in the client mapping?
- What manual verification path proves the user flow works?

## Auth, Permission, or Sensitive Data Changes

- What boundary enforces access?
- What secrets or sensitive fields must never be logged?
- What roles or identities gain or lose access?
- What are the backward-compatibility and audit implications?

## Config, Rollout, or Operations Changes

- Which env vars, feature flags, or deployment files change?
- Can the feature be rolled back safely?
- What dashboards, logs, or alerts should be watched?
- Is there a staged rollout or migration window?
