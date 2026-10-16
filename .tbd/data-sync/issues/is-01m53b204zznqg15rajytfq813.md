---
type: is
id: is-01m53b204zznqg15rajytfq813
title: "Stage 4 review of #622's s(29) certificate (T-195)"
kind: task
status: in_progress
priority: 2
version: 7
delegate: user-eb-review-622
labels:
  - result-import
dependencies: []
parent_id: is-01m50j15k23rw2vdmvyvs07rqt
hold: null
hold_until: null
created_at: 2026-10-16T21:49:27.583Z
updated_at: 2026-10-16T23:32:45.232Z
started_at: 2026-10-16T21:49:33.508Z
---
Stage 4 review (packing/campaign/result-import.md) of the s(29) exact rational certificate from jlevy/squares#622 (PingYou Ltd / BuddenPing), imported by records PR #661 (branch claude/intake-2026-10-16-n29-622) as packet pingyou-pr622-certificate-2026-10-15, replay evidence E-pingyou-622-exact-feasibility, per-count ledger upper-bounds-n29-20261016, register entry T-195. Independent exact-rational re-derivation of the certificate and both margins (T-155, T-174 at 29), the controls, provenance and credit, the rung, and adoption under the owner's house rule. Deliverable: docs/project/reviews/review-2026-10-16-pingyou-n29.md with programs in the packet's review/ directory; draft PR on #661's branch; a correctness review on #661. Worktree .claude/worktrees/review-622, branch claude/intake-2026-10-16-review-622.

## Notes

2026-10-16 22:15Z user-eb-review-622: claimed; worktree .claude/worktrees/review-622, branch claude/intake-2026-10-16-review-622 from #661 head 3f77449f4. Own release-asset download: 430,075 bytes, SHA-256 0dc9bcd1... (pin); tag -> 318ab94e (ls-remote). Clean-room checker review/programs/n29_exact_review.py (stdlib Fraction, python3.14 -I; producer's .py members and the replay's code unread): certificate ACCEPTED, 116 walls + 406 pairs over Q, 12 CPU s; one touching pair (23,24), 18 touching walls, least positive slack 1.04e-800. Controls: duplicate, outside, tight-pair (1e-3000), tight-box (1e-3000) all refused with exactly the expected violations. Derived fact facts/n-029.yaml.gz and native corners witness equal the certificate. Exact: T-155 - S = 1.566165818922113e-36; #574 N29 - S = 7.324826736065141e-90; S - Kingbird print = 0.919 ulp (inside only if the print is cut). Pushed 918b0bd30. Next: review #661's controls/records, write review doc + README, PR, GitHub review on #661.

2026-10-16 ~23:00Z user-eb-review-622: pushed c58edf873 (merged #661 head 4b3d413e5 at 166fc15f4). Added: identity (vs T-009 witness: 1-to-1 by index under y->L-y, 0 moved beyond 1e-9, max move 7.685e-20, max turn 3.3e-38; vs house 100-place facts 8.8e-100), T-009 Krawczyk box [..418, ..419] holds S (S-lo 1.08e-45) and shows the Kingbird print is a truncation; receipt re-decided (positive = certificate; controls change only sq1/sq0, refused for the right reason; routes' least gap/clearance equal mine); author's COMPARISON.json gains equal mine exactly. 10 outputs reproduce via uv (117 s). Findings drafted: rung declared before the exit (like #651 A2; hold blocked by check_standing reading the print as exact), identity measurable, controls gross (mine tight), relation label (T-174 precedent), activity/deferral name think-30n2. Next: README + review doc, document map/SYNOPSIS, validation, draft PR, GitHub review A on #661.

2026-10-16 ~23:35Z user-eb-review-622: review pushed 749fc640e (docs/project/reviews/review-2026-10-16-pingyou-n29.md, packet review/ with n29_exact_review.py, third_route.py, run_review.sh, 11 outputs). Draft PR https://github.com/jlevy/squares/pull/662 (base #661's branch), labels intake + S1. Verdict accepted, finite feasibility, no blocking defect. Coordinator items: third route run (30 s, passed, 6/6 controls) -> adoption prose may stand once the exit cites it; found_year must be 2025 (Schadt), not 2026; rung V3/C3 acceptable only if main never carries it without the review (check_requests already reads #622 closeable). Validation: records tier 52/52 (116 s), check_documentation ok, check_release_impact ok (no edition asked). Next: GitHub review A on #661.

2026-10-16 23:20Z user-eb-review-622: published review A (kind=correctness, event=COMMENT) on #661 at 893a7a0b9: https://github.com/jlevy/squares/pull/661#pullrequestreview-5554624342. Findings: A1 High (661 conflicts with main: 5 n11 claim docs, results.yaml, release.py; main cut v0.7.20 #644 and v0.7.21 #653, so 661's v0.7.20 must be re-cut, v0.7.22+; no Packing validation ran at 893a7a0), A2 Medium (rung before exit; acceptable only if main never shows it without the review; check_requests reads #622 closeable), A3 Medium (exit content owed), A4 Medium (independence label rests on routes the source ran; cite third route + clean-room checker), A5 Low (gross controls), A6 Low (identity measured), A7 Medium (adopt branch found_year 2026 -> 2025), A8 Low suggestion (T-009 box route for think-6gti), A9 Low (bead pointers). PR #662 (draft, base #661's branch) head 749fc640e; hosted CI running.

2026-10-16 23:35Z user-eb-review-622: done. PR #662 (draft, base #661's branch) head 9e740043d; hosted CI all green (15/15 non-skipped; Packing validation 38980731227, Certificate page 38980731237). Review A on #661 published. Local: records tier 52/52 at 9e740043d (105 s), check_documentation ok, check_release_impact ok, 622 tests 7 passed at 893a7a0. This bead can close when #662 merges (no structured record names it). Left with think-30n2 (lane N): A1 merge main + re-cut edition; the stage 4 exit (A2-A6, A9); adoption found_year 2025 (A7).
