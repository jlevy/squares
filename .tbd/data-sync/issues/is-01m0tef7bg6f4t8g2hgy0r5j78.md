---
type: is
id: is-01m0tef7bg6f4t8g2hgy0r5j78
title: Retain independently invalid basin events instead of crashing the batch
kind: bug
status: open
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0t4phe1905yy2jk7czp1391
created_at: 2026-08-24T17:53:09.473Z
updated_at: 2026-08-24T18:00:59.393Z
---
D-183. Exp-026 n=6 seed 3 reached make_event, failed the independent sqpack validity screen, and validate_event raised before run() could append the fourth record. The partial JSONL contains only seeds 0-2, violating the preregistered retain-every-stop contract and making unattended batches censor precisely the failures needed for diagnosis. Acceptance: BasinEvent/v3 can retain a finite endpoint whose independent screen is invalid; its admissibility is false and promotion_blockers includes an exact independent-validity token; replay derives and checks that state; a mutation cannot forge admissibility or omit the blocker; run() writes the record before continuing; exp-026 resumes seed 3 without rerunning seeds 0-2; focused and normal gates pass.

## Notes

2026-08-24 implementation checkpoint a3be8e4 pushed. BasinEvent/v3 now derives independent_validity_failure, forces admissibility false, retains the event, and rejects forged admissibility or omitted blockers; v2 remains strict. Exp-026 remains a blocked three-row artifact under da6bac3. Full 30-step gate passes in 78s. Still open until a separately preregistered four-seed n=6 replication proves run-path retention.
