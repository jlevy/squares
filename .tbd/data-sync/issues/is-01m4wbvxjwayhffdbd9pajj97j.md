---
type: is
id: is-01m4wbvxjwayhffdbd9pajj97j
title: "Import BuddenPing: s(207) <= 14.880960371559, refining T-147 (#503 comment)"
kind: task
status: in_progress
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T04:48:55.899Z
updated_at: 2026-10-14T17:59:44.662Z
started_at: 2026-10-14T04:49:01.109Z
---
https://github.com/jlevy/squares/issues/503#issuecomment-6133755143 (BuddenPing, 2026-10-12T22:25Z) and the issue body's dated update. BuddenPing/square-packing-certificates 10418630bfb00853a539ad7ad9908b2d746147c0, n207.cert.json and pingyou-n207-rational.yaml; a coordinate refinement of T-147; credit PingYou Ltd. Intake lane pingyou of 2026-10-14.

## Notes

## 2026-10-14 intake lane pingyou (stages 1, 2 and the stage 4 replay)

Branch `claude/wizardly-meitner-wqn4x3-intake-1014-pingyou`, commit `680123806` (pushed; no PR). Packet `packing/resources/web/pingyou-n207-refinement-2026-10-12/`. Resumed after a container restart: the predecessor lane's packet, declaration and first five receipts were kept and checked; n272 and n261 were certified and all seven replayed again here.

### Stage 1 triage

- **Read:** the comment of 2026-10-12T22:25Z on #503 (closed), with the dated update atop the body; read through the owner's reply of 2026-10-14T04:42Z.
- **Pin:** BuddenPing/square-packing-certificates `10418630bfb00853a539ad7ad9908b2d746147c0`, committed 2026-10-12T22:24:32Z (tree `7920d484`); every file of the scope has the same blob at the head 318ab94 (2026-10-12T23:46:52Z) at retrieval 2026-10-14T04:47Z.
- **Claim:** s(207) <= 3720240092889639048018577779/250000000000000000000000000 as printed; exact side 14.880960371558556192074311116, rounded up at 16 places 14.8809603715585562. First committed 2026-10-12T22:24:32Z.
- **Other claims of the release:** none at other counts in this scope. Later, outside it: PR #574 (BuddenPing/squares head 4c319c2, open) and the GitHub releases at tags data/pingyou-* on 318ab94 state smaller certificates at all seven of this pass's PingYou counts; an import of their own, not owned here (see the packet README).
- **Licence:** none (no licence file at the pin; GitHub detects none; the release READMEs grant nothing for the source's own files). Derived-only custody: no upstream byte retained.
- **Register action:** a new entry (a later release that improves an earlier entry's value): T-147 keeps its claim, and the case record decides which is current.
- **Who else holds the value (frozen in acquisition/claims.json at main aeef99ef0):** case T-147 (PingYou Ltd), below by 1.485e-09; T-098 (#375) below by 1.299e-02; T-116 (#422) below by 7.032e-03; T-127 (#438) below by 7.032e-03; T-136 (#481) below by 4.546e-03; #573 above by 5.562e-13; #593 above by 5.559e-13; PR #574 above by 2.977e-12; smallest: PR #574. Open PRs #585 (regularized-drawing credit), #587 (T-156 at 290) and #591 (regularized view by default) state no side at this count.
- **Credit:** Credit PingYou Ltd (https://github.com/BuddenPing/square-packing-certificates) with the n207 assembly and this refinement of its certificate, as the source asks: two differently placed patches of Ryan Xu's n70 construction (ry-xu, issue 432), taken from Evan Daniel's exact n70 certificate, with upright grids of 42 and 36 squares. The source names SQUISH's n207 (issue 481) only as its earlier comparison.
- **AI assistance:** the issue and comments state nothing about AI assistance; no pinned file states anything about AI assistance (scanned, packages included); the standing statement on record is the author's #503 answer of 2026-10-12T17:57Z for the n207 and n153 solutions: 'Both solutions were AI assisted by "PY", an unreleased agentic AI offering by PingYou Ltd.'
- **Validation plan and price:** both maintained exact routes (sqpack exact_verify and check_rational_witness_independent) through devtools.upper_bound_reports, a positive and two controls, --workers 1; measured 10-16 s per job (7 route CPU s). No source program needs to run. Stage 4 review and a third route (check_half_angle_area) remain.

### Stage 2 and the stage 4 replay

- Packet written by acquire_source; fact derived and held to the source's witness. certify --workers 1 45 s wall: 3 jobs, 1 positive passes both routes, 2 controls refused by both; 127,926 pair decisions, 21.96 route CPU s, longest job 15.77 s; a fresh check --replay 38 s wall, equal to the retained rows.
- register-plan (printed, nothing written; full output kept in the lane's scratch): T-NNN at V0/C0, scope [207], proposed significance 2, published 2026-10-12, evidence E-pingyou-503-refinement-report, credit 'PingYou Ltd after Xu, Daniel, Levy', lineage builds-on-project, source key [PingYou n207 refinement 2026-10-12]. Shared records not edited.

### Draft acknowledgement (not posted)

@BuddenPing, thank you. We have the refined n207 certificate from your comment of 12 October, pinned at 1041863 (n207.cert.json, SHA-256 94dc19ce…). We retain it as derived exact facts beside T-147's, and this project's two maintained exact routes have decided it with both controls; it is the same assembly as T-147's, and smaller by the 1.4851194398617480221170501178639e-9 you state. A review and the registration follow; T-147 keeps its own claim, and the case record will say which is current. PR #574 states further n207 certificates; it is a separate import.

Posted (stage 1 acknowledgement, 2026-10-14): https://github.com/jlevy/squares/issues/503#issuecomment-6162867217

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): T-166 at 207, V0/C0, regularizing T-147.

Renumbered on 14 October at review A3 of #602 (records PR, branch claude/wizardly-meitner-wqn4x3-records-1014): Kevin Fang's theorem, T-178 above, is now T-163, at Theorem 1's first commit (6028f31, 12 October); T-163 to T-177 above are now T-164 to T-178. T-179 to T-184 keep their ids.
