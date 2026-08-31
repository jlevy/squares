---
type: is
id: is-01m0vcbwn74ygpnxetkk4eyvpr
title: Correct stale BC-010 deep-gate diagnosis
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
labels:
  - packing
  - bookkeeping
  - pr22
dependencies: []
parent_id: is-01m0vbg75b3j30f9eq2j678b9j
created_at: 2026-08-25T02:35:37.509Z
updated_at: 2026-08-25T02:44:52.034Z
closed_at: 2026-08-25T02:44:52.033Z
close_reason: Replaced BC-010's superseded n=4/n=10 diagnosis with the D-199/D-203 state, logged D-219, preserved the unchanged golden and no-retry precondition, and validated the agenda under the packing schema and normal focused checks.
resolution: null
duplicate_of: null
---
BC-010 still says n=4 and n=10 drift under D-126/D-162 after D-199 restored n=10 at both pool widths and D-203 isolated only n=4 seed 0. Correct the current note without changing the experiment order or verdict, validate the agenda, and record the error in the packing defect log.

## Notes

Bounded factual correction delegated: replace only the stale BC-010 ending, Flowmark the file, validate agenda/frontmatter, and record as next available defect id. No experiment order, hypothesis, threshold, or mathematical verdict changes.
