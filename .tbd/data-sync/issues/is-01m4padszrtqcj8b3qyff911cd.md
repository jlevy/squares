---
type: is
id: is-01m4padszrtqcj8b3qyff911cd
title: "Stage 4 review of the 2026-10-11 upper-bound imports: third exact route and a mapped W2 review (#500, #501, #503, #504, #505, #506)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T20:28:18.295Z
updated_at: 2026-10-11T22:02:24.916Z
started_at: 2026-10-11T21:32:13.301Z
---
For each certificate the 2026-10-11 import lanes retain and replay on both maintained exact routes: devtools.check_half_angle_area decide-imports extended to the new packets (own readers, --upstream digests), controls, and a mapped review under docs/project/reviews/ in the form of review-2026-10-10-upper-bound-imports-476-481-483-484.md; verdict and per-count house table.

## Notes

2026-10-11, W2 review lane V1 for #503 and #504 (sub-agent, Claude Fable 5.1 at xhigh, a different model from the Opus import lane), worktree /home/user/squares/.claude/worktrees/agent-a10888f5a2fd13100, branch worktree-agent-a10888f5a2fd13100, cut from main 3a5a91a90 with the import lane's 7ad4fc95f merged (fast-forward). Not pushed.

Review: docs/project/reviews/review-2026-10-11-upper-bound-imports-503-504.md, mapped in docs/project/document-map.yaml (SYNOPSIS.md not re-rendered). Verdict accepted, finite feasibility only, for both certificates: PingYou Ltd's n207 (#503, 9dc93b6) and n153 (#504, bc328a7). Seven non-blocking findings: RV-1 #503's OpenAI Codex disclosure removed at the pin (0d8b9c1 and the first issue text had it; 9dc93b6 "Correct attribution in submission materials" removed it; #504 states nothing): the register should carry the first account and its removal on both entries and the author be asked; RV-2 the source ran both maintained routes itself at 5b0eb012 (native-replay.json), so the independently re-implemented relation rests on the routes' authorship predating the source and on the third route, which the source did not run; RV-3 no retained check binds a fact to its upstream bytes (RI-2), closed once here by --upstream for the certificate and the witness of each packet, and the packages' n70 parent held to T-146's n-070 by hand; RV-4 kernel controls gross (RI-3); RV-5 #504's lineage is by construction, not by pose; RV-6 no private-worker custody; RV-7 the n207 certificate's unread provenance.numerical_screen_side (14.885506208841678) is not SQUISH's side.

Replays reproduced here (from packing/, one worker, load 14-18 on 4 cores): pingyou-n207-certificate-2026-10-11 check --replay 3/3 jobs equal, exit 0, 134.8 s; pingyou-n153-certificate-2026-10-11 check --replay 3/3, 52.3 s; check-claims rebuilt equal, 7.4 s and 4.2 s (21:34:05Z to 21:37:24Z). Receipt totals as the packets print: 207: 3 jobs, 127,926 pair decisions, 54.66 route CPU s, 103.49 job wall s, longest 40.08; 153: 3 jobs, 69,768, 24.09, 70.27, 24.79. Kernel controls refuse at gap -1 and clearance -3.0 on both routes.

Third route: devtools.check_half_angle_area gained the #503/#504 roster (IMPORTS_503_504), its own pingyou-json reader (SQUISH's rows; note, dilation_exact, raw_side, provenance named and unread; any other field refused), its own witness-corners reader (centre = mean of corners, rotation = first edge on the unit circle, other edges its quarter turns), --upstream same_packing checks for a fact's pinned witness, and patch_lineage (LINEAGE), a credit measurement: parent squares reappearing in the child under a box symmetry and translation after the guard dilation is undone. Run: decide-imports --workers 1 --imports '#503' '#504' --upstream pingyou-n207-certificate-2026-10-11 DIR --upstream pingyou-n153-certificate-2026-10-11 DIR: #503 passed, 21,321 pairs (402 clipped), wall 1/20000000000, 0 wall contacts, least distance 1.000000e-10, 6/6 controls; #504 passed, 11,628 pairs (297 clipped), wall 1/10^13, 0 contacts, least distance 1.885826e-13, 6/6; no disagreement with the maintained inputs, margins, frozen claim records, register-plan claims or prints; 4 upstream checks pass (both certificates and both witnesses, fetched from raw.githubusercontent.com at the pins, all 15 files of the two scopes with the packets' digests); 59.4 s (65.4 s with start), 21:46:12Z to 21:47:17Z. Lineage against T-146's retained n-070 (which the packages' evidence/parents/n070.cert.json, d508ee05, equals pose for pose): #503 identity 69 within 1e-9 / 60 exact, and (x,y)->(L-y,L-x)+(6,6) 69/69, i.e. the source's 60+69 retained owners; #504 at most 31 within 1e-9 and 1 exact at lattice shifts: not a placement of the n70 by pose, as the source's own account (reclosed contacts, float solve) says. Metadata consistency read and not believed: (14+f)*d = S at 207; table side * guard = S at 153. Tests: packing/tests/test_check_half_angle_area.py 104 (12 new; the n207 decide and the lineage test marked slow), all pass; ruff and basedpyright clean on both files.

Significance: S3 confirmed for both (compared with T-136 S3, T-140 S3, T-146 S2); `by` to name the review. Rungs: each entry can take V3/C3 once registered with its confirming evidence (E-pingyou-503-exact-feasibility, E-pingyou-504-exact-feasibility; independent-implementation; verifiers V-sqpack-verify, V-check-rational-witness-independent, V-evand-arrangement-receipts, V-upper-bound-reports, V-check-half-angle-area, V-evand-exact-certificates; this review as independence_record and external_review). No V4/C4. Adoption per count (after private-worker custody): 153 -> #504 (then T-146, then T-136); 207 -> #503 (then T-136); replaces the first imports review's table at those two counts.

Validation: tests/test_check_half_angle_area.py 104 passed (138 s under load); ruff and basedpyright 0 findings on the two files; packing-validate --records (223 s) fails only on "synopsis agrees with the artifacts" (SYNOPSIS.md document map is stale: the new review is mapped and SYNOPSIS is left for the coordinator to re-render), every other step passes.

Not checked: reproduce.py (not run), the n153 table's origin in the n70, the degree-seven root and SymPy identity, the source's three checkers, the intermediate cycle-hit-153 control, derive --check from a checkout.
