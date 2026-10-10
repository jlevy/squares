---
type: is
id: is-01m4jkkfsrfyg2sqvp66cznkgm
title: "Stage 4-5: independently review and adopt the pending upper-bound reports (T-128, T-130, T-131 and the 2026-10-10 imports), choosing one house per count"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:51:43.927Z
updated_at: 2026-10-10T13:46:44.398Z
started_at: 2026-10-10T09:52:52.837Z
---
The register holds rational upper-bound reports by others at V0/C0 whose next_rung is an independent review of the retained replay and a selected-house decision: T-128 (Couzo, eight), T-130 (Couzo, five), T-131 (Daniel, n = 132), and this pass's #470, #476, #481, #483 and #484 once registered. Several counts now carry more than one candidate (132: T-098 house, T-131, #476, #470; 237, 263, 270, 303: #476 and #481; 267: #470, #476). For each count: the smallest certificate whose complete two-route replay passed, a mapped W2 review of that replay (think-mt6e's rule: verified lane only on a replay here and a mapped review), the earlier house kept as history, and the case record's reported and verified ceilings moved together. Mirror the Gupta adoption (PR #448, #459: confirm_gupta_records.py). Coordinate with PR #403 / #435, which own canonical exact-value integration on the case records.

## Notes

2026-10-10, W2 review lane (sub-agent, Claude Opus 5.5), commit 4708077f3 on worktree-agent-a96d05b94bf14e20a, cut from claude/determined-rubin-yjfy2a at b0486a547.

Review: docs/project/reviews/review-2026-10-10-couzo-daniel-refinement-replays.md, mapped in docs/project/document-map.yaml (SYNOPSIS.md not re-rendered). Verdict accepted, finite feasibility only, for T-128 (8 certificates), T-130 (5), T-131 (n132) and Daniel's equal-side hunt1_n155 (evidence update to T-128). Six non-blocking findings: RD-1 T-128's module has no replay of its retained receipt (certify overwrites it); RD-2 the kernel's duplicate/outside controls are gross (gap -1, 3.0-15.8 units outside), not sharp; RD-3 both maintained routes read one parse and half-angle map; RD-4 at T-128/T-130 V-sqpack-verify is the producer's copied verify.py; RD-5 no private-worker custody at T-130/T-131 (needed before a house moves, not for the rung); RD-6 #481 (131, 270) and #476 (132, 270) are smaller.

Replays reproduced here (from packing/, two workers at most): T-128 24/24 jobs equal to their retained rows via `python -m devtools.check_half_angle_area replay-t128 --workers 2`, 339.0 s; T-130 15/15 via `python -m devtools.couzo_followup_reports check --replay`, 130.5 s; T-131 6/6 via `python -m devtools.evand_hunt_reports check --replay`, 38.5 s; `evand_hunt_reports check-claims` rebuilt equal, 0.5 s.

Third route: packing/devtools/check_half_angle_area.py with packing/tests/test_check_half_angle_area.py (25 tests, 3.4 s). Own literal reader, half-extent containment, circumscribed-disc rule then exact clipped-intersection area; shares only Fraction with the maintained routes. `decide --workers 2`: 15 certificates, 213,064 pairs (5,241 clipped), 90 controls all at their required outcomes (incl. side at far-wall contact accepted, 1e-40 past refused, closest pair in contact accepted, pushed 1e-30 refused), no disagreement with the maintained inputs, wall clearances (exactly 1/(2*10^20) at all 15), separating-axis gaps (least Euclidean distance >= gap), register claim decimals or receipt totals; 37.0 s.

Rungs: T-128, T-130 and T-131 can each take V3/C3 once confirming evidence (E-couzo-451-exact-feasibility, E-couzo-460-followup-exact-feasibility, E-evand-465-record-hunt-exact-feasibility; relationship independent-implementation), verifier V-check-half-angle-area and the reviews entry land. No V4/C4 (one AI review, no human oversight).

Adoption per count: T-130 at 84, 86, 105, 175; T-128 at 108, 127, 155 (Couzo's; Daniel's equal side as confirmation), 180, 228, 306; 131 -> #481 (fallback T-128); 132 -> #476 (fallback T-131); 270 -> #481 (then #476, then T-130). Hold the current houses at 131, 132 and 270 until those imports have their own two-route replay and mapped review. T-128's n105 stays verified, not selected.

Validation: --edit failed only on the stale SYNOPSIS document map (expected) and a basedpyright exit 247 with no output under load ~17 on 4 cores; basedpyright rerun alone: 0 errors, 0 warnings, 0 notes (255.8 s). --records failed only on the stale SYNOPSIS document map.

2026-10-10 13:45Z (coordinator): house adoption, i.e. moving case records' reported and verified ceilings, is deferred until jlevy/squares#403 lands: that open PR rewrites all 324 packing/frontier/n-NNN.md case records, including every count this round touches, so adoption now would collide with it. Register-level work proceeds tonight: the W2 review (docs/project/reviews/review-2026-10-10-couzo-daniel-refinement-replays.md, accepted, RD-1 to RD-6 non-blocking) supports V3/C3 for T-128, T-130 and T-131, and the new imports (#476, #481, #483, #484) are registered as reported without case-record edits, as T-131 was. The per-count house table in the review's notes (84, 86, 105, 175: T-130; 108, 127, 155, 180, 228, 306: T-128; 131 and 270: #481; 132: #476) is the adoption plan once #403 merges; RD-5 (private-worker custody for T-130 and T-131) precedes any house move.
