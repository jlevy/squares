---
type: is
id: is-01m4fhtf47sdkk0ffx4b5x5jpx
title: Unadopted better results render as superseded (T-128, T-130)
kind: bug
status: closed
priority: 1
version: 8
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T05:22:52.167Z
updated_at: 2026-10-09T19:13:59.858Z
started_at: 2026-10-09T05:23:17.911Z
closed_at: 2026-10-09T19:13:59.858Z
close_reason: Fixed and merged in stack 430 (main d3860c97a)
resolution: null
duplicate_of: null
---
render_recent_results.standing marks any result no case lane rests on as SUPERSEDED, so T-128 (#460) reads 'recorded, superseded by T-098, T-115, T-125 and T-127' and T-130 (#469) 'superseded by T-119 and T-125' although their reported sides are strictly smaller than the held bounds. Correct status should say reported/pending adoption. Fix at #460, the lowest layer where it manifests.

## Notes

Fixed at #460 657147e79 + re-pin 61359c972: superseded means replaced (cases hold a bound at least as good as each stated bound; ties stay superseded); new standing 'pending adoption' (status renders 'recorded', no mark) where a stated bound is strictly better than the case record in a lane the entry can hold (C0/C1 -> reported lane only), via check_standing.improvements() exact comparison; mixed cases pending as a whole, superseded per-case in site chains; T-128 claim states its eight exact sides; guard test requires unadopted imports to state sides. Docs: epistemics.md Status, result-import.md Stage 3 rule 'The claim states each bound it reports', article template, paper-design. Upward: T-129 sides patch at #463 (integrator), T-130 sides patch at #469 (#469 agent); re-render RESULTS.md/headline and re-pin per layer.

Round-2 review (R) of 657147e79: R1 High T-121..T-123 still mislabeled superseded by T-098 (algebraic alpha_n sides unreadable; guard exception locks it in); R2 Med latent irrational case bounds compared via printed decimal; R3 Low direction vs kind; R4 Low problems() pending branch not independent; R5 Low docs; R6 Low superseding() names worse lanes. Sent to the label agent for fix on #460. R7 (f3f1f822f message says seven, records eight replies) goes in #466 PR body.

Round-2 addressed on #460 (head 4291ed6e6, hosted Packing 37895864439 + Pages 37895864484 green): 7d2135863 CI fixes (guard declared in DECLARED_CONSUMERS; filter expectation keeps PENDING_ADOPTION rows visible under hide-superseded); 072b99d1f R2 span() interval comparison for closed-form bounds (+-1 unit last printed place; overlap = tie); 3ef945cba R3 KIND_DIRECTIONS; d636d850a R4 independent citing() check; 2e3dd84f6 R6 lane-precise superseding(); 43d08e879 R1 T-120..T-123 claims state cut sides (T-120 superseded by T-125; T-121..T-123 pending adoption) and guard asserts unplaced == []; bfe5bbf4b + 4291ed6e6 R5 docs (math-markup fix); 60f0e1278 re-pin to 43d08e87. Upward: test_result_status expected set at #463+ drop T-121..T-123, keep T-120/T-129; re-render and re-pin each layer.
