---
type: is
id: is-01m5b11wcmc6cxqp03q00w348p
title: Regularize 155, 229, 236 and 271 after the 19 October evand adoption (T-197, T-199, T-218, T-219)
kind: task
status: in_progress
priority: 2
version: 5
delegate: c-lane-692
labels:
  - regularization
dependencies: []
parent_id: is-01m54ahn4m3hkpas6fz13bjhpd
hold: null
hold_until: null
created_at: 2026-10-19T21:28:33.428Z
updated_at: 2026-10-20T02:06:45.936Z
started_at: 2026-10-19T21:28:46.377Z
---
Both strong generators (grid-slack at 0.5, 1 and 5 degrees; Evan Daniel's driver) and regularize_select on the four counts the 19 October adoption re-houses, in the adoption's PR (claude/intake-2026-10-19-evand-singles), per result-import.md 'Adopt a House, Then Regularize It'. Priced by adopt_houses at 20 to 100 CPU-minutes. Runs under scratchpad lnew/runs, retained evidence under packing/cases/regularized_drawings/<this bead>-2026-10-19/.

## Notes

2026-10-20 lane-new: PR #692 opened (head f76d57a40, base 028bc72ec) with records, adoption at 155/229/236/271, regularization (think-ip1p), explainer v0.4.9 and site v0.7.36. packing-validate --records passes 52 steps at the head; --push is running. Senior review requested via the coordinator. Stage 7 reply waits for the merge and check_published_site.

2026-10-20 lane-new: PR #692 head e877e19ad. The first CI run at f76d57a40 found adoption follow-ups: sweeps checkout, censuses, translation screen, PR 574 claims, n-155 closed form, bibliography Levy suffix, test golden counts. They are fixed in 9b0c82d82 and a8222aad4. main b16ddeb0a (#691) is merged and the worker snapshot pruned of the 229 review SVG. v0.7.36 is re-cut last. --records passes 52/52.
