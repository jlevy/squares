---
type: is
id: is-01m0tef7bg6f4t8g2hgy0r5j78
title: Retain independently invalid basin events instead of crashing the batch
kind: bug
status: open
priority: 0
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0t4phe1905yy2jk7czp1391
created_at: 2026-08-24T17:53:09.473Z
updated_at: 2026-08-24T18:03:14.801Z
---
D-183. Exp-026 n=6 seed 3 reached make_event, failed the independent sqpack validity screen, and validate_event raised before run() could append the fourth record. The partial JSONL contains only seeds 0-2, violating the preregistered retain-every-stop contract and making unattended batches censor precisely the failures needed for diagnosis. Acceptance: BasinEvent/v3 can retain a finite endpoint whose independent screen is invalid; its admissibility is false and promotion_blockers includes an exact independent-validity token; replay derives and checks that state; a mutation cannot forge admissibility or omit the blocker; run() writes the record before continuing; exp-026 resumes seed 3 without rerunning seeds 0-2; focused and normal gates pass.

## Notes

2026-08-24 D-183 repair replication preregistered and pushed as exp-027 at 6e6eb16, engine a3be8e4. Same n=6 seeds 0-3 and 10s budget; criterion is four retained replayable outcomes, with seed 3 remaining visibly non-admissible if its independent screen still fails.
