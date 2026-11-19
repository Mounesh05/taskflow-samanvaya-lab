# TaskFlow — SAMANVAYA Test Scenarios

## Scope

This repository is a nonproduction test application.
Use synthetic tasks and approved test accounts only.

## Scenario 1: Backend CRUD
Expected:
- Valid task creation succeeds.
- Invalid priority receives HTTP 422.
- Unknown task ID receives HTTP 404.

## Scenario 2: Python algorithms
Expected:
- Search is case-insensitive.
- Sorting orders priorities descending.
- Sorting preserves all tasks.
- Alternative correct sorting methods agree.

## Scenario 3: Frontend algorithms
Expected:
- Search returns matching tasks.
- Status summaries count tasks correctly.
- Sorting does not mutate input.

## Scenario 4: GitHub CI
Expected:
- Passing code produces successful checks.
- Failing tests make CI fail.
- Correcting a regression makes CI pass.

## Scenario 5: Real MongoDB
Expected:
- A task can be created.
- Its status can be updated.
- Stored data can be retrieved.

## Scenario 6: SAMANVAYA
Expected:
- GitHub project synchronization respects access.
- Code observations reference real source revisions.
- AI interpretations are distinguished from verified facts.
- Missing evidence is reported explicitly.
- Unauthorized users cannot access another project's reports.

## Important
CI results and AI claims must be checked against their
actual evidence. Do not assume that an AI recommendation
is correct merely because two agents agree.