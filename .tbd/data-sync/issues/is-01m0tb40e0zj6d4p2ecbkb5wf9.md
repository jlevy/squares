---
type: is
id: is-01m0tb40e0zj6d4p2ecbkb5wf9
title: Diagnose the retained n4 seed3 post-check rejection
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
created_at: 2026-08-24T16:54:36.223Z
updated_at: 2026-08-24T16:56:53.169Z
---
D-171. BasinEvent/v3 n=4 seed 3 reaches one fixed-point evaluation whose successful HiGHS result still violates pair row 16 by 4.209e-10 after the single D-164 bounded repair. The producer correctly stops and retains one unsettled evaluation, leaving the four-seed positive-control cell only 3/4 admissible. Acceptance: retain the exact event and failing cell evidence; classify whether the second result reflects cell-boundary ambiguity, solver tolerance, or an incorrect row; preregister any bounded remedy; preserve the 1e-10 screen and independent validity; never promote the current stop.

## Notes

2026-08-24 exp-023 retained at 94b67a5. Seed 3 stops at side 2.0218239546404626 after one of 3,866 fixed-point evaluations remains unsettled: successful HiGHS result, bounded one-row retry already used, pair row 16 residual 4.209e-10. Event remains independently valid but scientifically inadmissible with both derived blockers. Seeds 0-2 reach proved side 2 and are admissible. Next 30m slice must retain the exact failing fixed cell and classify boundary ambiguity vs solver artifact vs row error before any remedy; keep the 1e-10 screen and one-remedy cap.
