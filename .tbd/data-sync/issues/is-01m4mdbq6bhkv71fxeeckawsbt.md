---
type: is
id: is-01m4mdbq6bhkv71fxeeckawsbt
title: "Regularize every packing n = 1..324 with the adapted process, in pull requests after the #497 plan"
kind: task
status: in_progress
priority: 1
version: 10
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4jk4cae8514p87y79gsh17n
  - type: blocks
    target: is-01m4kbxmtaqt87tdw33cs19ah8
  - type: blocks
    target: is-01m4kbxna1xdmjd8nkka3wax60
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T02:41:06.762Z
updated_at: 2026-10-11T20:06:24.286Z
---
Owner request 2026-10-11 (epic think-cdud, item 4): adapt evand's search/regularize process as think-kl2v's assessment recommends and run it over every packing the record holds, n = 1..324, so the atlas and case drawings are clean and regular. A separate process, so a separate pull request stacked on PR #487 (gh stack; github-stacked-prs is granted), begun once the 2026-10-10 imports are in good shape; the owner checks it. Obligations: every regularized view exactly feasible at its stated side and verified over Q; no side, frontier value or evidence tier changed by a drawing; each regularization recorded with its typed credit and identity basis (the register's regularizations field for results, and the atlas layer's contract per the atlas bead); drawings labelled regularized; the existing gates (regularized atlas views match their index, re-derive exactly, drawings match their index) kept green and extended to the new process. Record the run cost in the bead. The wand125 confirmation runs (think-r333, think-i85v, think-nd7g) wait for this.

## Notes

2026-10-11: planned from think-kl2v's assessment (branch claude/regularization-2026-10-11, docs/project/research/research-2026-10-11-evand-regularization-assessment.md). Five slices: (1) witness to input at full precision and the exact-solve stage at the pin, with a receipt; (2) the regularizer stage (conservative, coincide, source orientation) and import through the evand-cert adapter, decided on three routes, identity and shade counts measured; (3) exact re-solve over Q of the tight contacts at the witness's side wherever rotations are rational, so side: same is literal; (4) the record: register results for solved views below the verified bound, index entries under think-k35c's contract otherwise; (5) drawings, gates and docs. Open owner questions (assessment's last section): 1 variant: conservative only, or upstream's best-choice with fewest at 14 counts; 2 may a fewest merge of determined groups be drawn as the same packing (recommended: no, alternates only); 3 do solved-to-smaller-side views (on the order of a hundred; about 73 where the verified bound is still the grid ceiling) become register results in this PR or a separate import; 4 side policy for irrational optima: status quo, reverse the 2026-10-02 ruling for labelled dilated views, or number-field views later (exact 45 degrees has no rational pose, so the Goebel family needs Q(sqrt 2)); 5 orientation: keep the source's (recommended) or adopt upstream's refit of 48; 6 taste tie-breaks from a gallery (symmetry vs contact at n = 10, the n = 26 diamond); 7 method credit with by: project and method naming Daniel's algorithm and pin; 8 retain the 80-digit KKT points (about 10 MB, OR-18) or only the receipt. Also: the atlas README's counts 55/87 are stale against the index's 68/74.

2026-10-11: the stacked layer is open as draft PR https://github.com/jlevy/squares/pull/497 (branch claude/regularization-2026-10-11, base claude/determined-rubin-yjfy2a), linked with PR #487 as GitHub stack #498. It holds the assessment only; work begins after #487 merges and the owner answers the assessment's eight questions.

2026-10-11 (correction, review A8): #497's base is main since #487 merged; #497 is the assessment and plan only (retitled).

2026-10-11, owner session (session_014Y3kYUK2wqLWoA4rqK1Wng), plan organized and execution begun. Owner directions: (1) make all fixes before proceeding; (2) vendor and pin the upstream regularization code and its inputs with proper credit, since we may fork it (supersedes the assessment's read-only attic recommendation); (3) run spikes on various n and show the result; (4) scope the end-to-end effort; (5) automated regularization followed by manual review and adjustment under a documented regularization policy.
Upstream pin: evand/square-packing 675a5eaa (search/regularize and search/exact byte-identical to the assessed 060c1a1 except posted_cert.py and 16 raw posted certificates).
Layout: #497 (claude/regularization-2026-10-11) = docs layer: review A fixes (think-t4q5), regularization policy (think-7f9y), effort scope. Stacked PR on claude/gifted-bell-57e62o = implementation: vendor/evand-regularize at 675a5ea (think-csds), devtools.regularize_evand driver = slices 1-2 (think-up3h), devtools.regularize_same_side exact re-solve = slice 3 (think-7hmc), spikes at n = 5, 10, 11, 17, 26, 37, 51, 70, 101, 129, 146, 200, 261, 292, 324 with a before/after gallery and the effort scope (think-ubr0).
Then: owner answers (Q3 first) with the spike gallery as evidence; slice 4 (record) and slice 5 (drawings and gates) and the full n = 1..324 run with manual review per the policy.

2026-10-11, owner: land in pieces and review quality across a few n before drawings change. Stack: (1) #497 assessment + policy; (2) #509 vendor at 675a5ea (claude/gifted-bell-57e62o); (3) tools: driver + same-side re-solve + gallery, no record/drawing change, reviewed with the spike gallery; (4) pilot: n = 10, 26, 70, 101, 129, 146, 200, 324 admitted after owner review, review records, gates; (5+) batches 1-108, 109-216, 217-324 each with gallery and review records. Outside the stack: #510 documentation-organization plan (think-xfuz); register-result import after owner question 3.

2026-10-11 (session_017JNnKDwL74rnktr9s8BdjP), stack state and repair. #497 had gone CONFLICTING against main after #502 (README reference table); merged main into claude/regularization-2026-10-11 (f5ca7f26c, both rows kept), then #497 into claude/gifted-bell-57e62o (34e74f68d; check_vendored_evand passes, 55 vendor-layer tests pass). The tools layer (stack item 3) was never pushed by the earlier session: the same-side module and its 12 tests were lost with that container. It is rebuilt on claude/busy-pascal-vgiccb, stacked on #509, as four lanes: same-side (Fable), driver (Opus), gallery (Opus), and a sourced history for the research doc (think-pwmi). Workflow entry: W7 pipeline-improvement.
