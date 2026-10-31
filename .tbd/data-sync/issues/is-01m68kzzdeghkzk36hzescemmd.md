---
type: is
id: is-01m68kzzdeghkzk36hzescemmd
title: Register the candidates below the new houses at 130, 293 and 307 (regularizer solves and the 260 + L strip), then review and adopt; the 172 review-queue view to the owner
kind: task
status: in_progress
priority: 2
version: 8
delegate: bold-ritchie-l8
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m692kj815d0m141prdqx3c13
hold: null
hold_until: null
created_at: 2026-10-31T09:17:32.462Z
updated_at: 2026-10-31T17:38:10.875Z
started_at: 2026-10-31T11:48:22.244Z
---
Evan Daniel's regularizer (regularize_evand run, run adopt-2026-10-31-n130-307-evand, retained under packing/cases/regularized_drawings/think-3guf-2026-10-31/ on #852) solved two of the new witnesses the 31 October adoption wrote to exact KKT local minima below the house best packing's side:

- n = 130: below T-259's certificate (Polkovskyi's re-solve of Couzo's #843 packing) by 2.500e-13; strict modulo 29 exact flat motions.
- n = 307: below T-256's certificate (Couzo's #844 refinement of ntumlnoob's packing) by 3.752e-12; strict modulo 57 exact flat motions.

The decision table held both at row 3 (register first), and the selection lists them as register candidates and never admits them (regularization-process.md, "Register Candidates"). Each is a smaller packing: register them as one batch result through the import runbook's stages 3 and 4 (devtools.register_regularized_bounds, as T-155), crediting the packings' finders (Couzo at both, after PR #574's finders at 130 and ntumlnoob at 307) and Daniel's regularizer, check whether any earlier certificate or the next count's ceiling already states each side (first_certified_in), take them through a stage 4 review, then adopt them under the house rule with both regularizations.

## Validation
- Claim: s(130) and s(307) at the regularizer's solved sides, 2.500e-13 and 3.752e-12 below the houses of 31 October; the run's solve/witness.cert at each count.
- Run: register_regularized_bounds, the maintained exact routes, a stage 4 review, then the adoption and its regularization.
- Cost: minutes of CPU for the replay; the review a lane of its own; the regularization 5 to 25 CPU-minutes a count by the runbook's receipts; an estimate, not a receipt.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Depends on: #852 merging (it holds the run and the new houses).
- Done when: the batch result is registered, reviewed and adopted at both counts, or the record says why a side proves no new bound.

## Notes

2026-10-31 (bold-ritchie-l2; A3 and A8 of the senior review of #852, https://github.com/jlevy/squares/pull/852#pullrequestreview-5722530514):
- A third register candidate, at 293: the committed s260_1028.cert (T-257's house at 260) plus one axis-aligned L strip of 16 + 16 + 1 squares in [S, S+1]x[0, S+1] U [0, S+1]x[S, S+1] proves s(293) <= 8816991251060941991251052624833/(5*10^29) = 17.6339825021218840..., 8.98e-13 below the adopted 293 house (T-257's s293_1028.cert) and across its 12-place print (...122 against ...123). The reviewer built it and the maintained independent route accepted it (42,778 pairs; scratchpad/rev9-scripts/lstep_293.py). Credit Evan Daniel (his 260, as his 293 is his 260 plus an L). Register with the 130 and 307 regularizer solves, review, then adopt. A scan of L steps into and out of the eight re-housed counts found no other improvement.
- For the owner's section 5 review (regularization policy), not a candidate: Evan Daniel's same-side view at 172 (run evand-regularize-adopt-2026-10-31-n130-307-evand) went to review at row 7, "2 per-square counts fell while no total did". It draws 0 uneven and 0 near-axis squares, 4 angle classes and 4 hues; the drawn grid-slack view has 21 classes and 20 hues. result-import.md sends such a view to the owner; the count is settled on its current drawing and the view waits in the review queue (receipt review_queue: [172]).

2026-10-31 bold-ritchie-l8 (lane L8 of the 31 October intake, epic think-3guf), branch claude/bold-ritchie-xo28us-l8:

- **Triage, exact** (devtools.register_candidates think-ruu2-2026-10-31 table, against main e482345fe's witnesses): 307 is 3.752e-12 below T-256 and its 12-place print differs (...685 against ...689); 293 (T-257's s260_1028.cert plus one L strip, s_260 + 1) is 8.980e-13 below T-257 and its print differs (...122 against ...123). Neither is a restatement by think-fwa9's words, so both are new results. 130 is 2.500e-13 below T-259 at the SAME print (11.902430645983). By the ruling's words that is a sub-print re-certification, but the record applies the ruling beyond the corpus only (think-ikku RV-1), and no answer says whether it reaches this project's own regularized views; T-155 registered such sides before the ruling. So it is HELD at registration for the owner. Neither next count's ceiling (131, 294, 308) is at or below its side, and no retained certificate states any of the three sides.
- **Registered**: T-261 (307), T-262 (293) and T-263 (130, held), each V3/C3 from the replay, with no review listed. Evidence: E-register-candidates-2026-10-31-views (130, 307; same-implementation, the run's own checkers) and E-register-candidates-2026-10-31-l-strip-293, both under citation deferrals naming think-4z8z. The case records at 130 and 307 gain the generated "not drawn, registered as T-26x" sentence (devtools.regularized_drawings); no case lane moves.
- **Retained**: packing/cases/register_candidates/think-ruu2-2026-10-31/: views/n-130.yaml.gz and n-307.yaml.gz, copied from the coordinator's run directory only after their Git blobs (8a991c28, 6030dd50) and sides matched the retained run reports; 293 is rebuilt from the #845 packet's 260 certificate through its custody wherever it is read.
- **Credit choice for the review**: measured against T-257's 293 certificate, nearest centres pair the L-strip packing one to one under no box symmetry (measure/identity-n293.json), so T-262 carries no regularizations item. It credits Daniel through builds_on ([Daniel issue 845 2026-10-29]). 307 and 130 are regularizations of T-256 and T-259 (one to one under the identity).
- **Adoption is held** (coordinator, 31 October: the review lane rv-ruu2 is running on all three). Besides the review, adopting a project-made certificate needs select_houses and upper_bound_houses to read it: select_houses reads entry["attribution"], which a project result lacks, and upper_bound_houses writes houses only from import packets. That slice is think-4z8z (new, child of this bead). When the review returns, list it on T-261 and T-262 only. T-263 waits for the owner.
- **Owner question** (to carry with think-ikku RV-1): does the 23 October restatement ruling reach (a) counts inside the corpus and (b) this project's own regularized views below a house within its 12-place print? 130 is the one live case; T-155's 26 sub-print same-side views predate the ruling.

2026-10-31 bold-ritchie-l8, after the stage 4 review (supersedes the adoption plan in the note above). The review (bold-ritchie-rv-ruu2, tbd-strong-max) is mapped at docs/project/reviews/review-2026-10-31-project-candidates-130-293-307.md, with its code, receipts and run inputs in packing/cases/register_candidates/think-ruu2-2026-10-31/review/.

- **Verdict**: all three valid; none a new arrangement. Each is its house's own packing with less padding (RV-2); uniform contraction of the house removes 87% of the margin at 130 and 94% at 307, and at 293 it overshoots.
- **Coordinator's decision (31 October)**: do not adopt. T-261 (307), T-262 (293) and T-263 (130) are registered at S1, V3 with C held at C1 (below the stage 4 exit, so select_houses takes none), with the review listed (accepted) and credits per the review: 130 Couzo's packing as T-259 credits it; 307 ntumlnoob's refined by Couzo; 293 Daniel's packing and construction (builds_on, exact re-assembly only, no regularizer).
- **Certificates (RV-5)**: the run's solve certificates at 130 and 307 (9d4b4c29..., f5474910...) and the review's written 293 with the house's own strip placement, a column of 17 flush top plus a row of 16 (10eac4aa...), held pose for pose to T-257's 260 plus the strip. The drawn views are no longer registered; they are kept only as the review's inputs.
- **Owner questions**: RV-3 (all three: is such a re-certification a new result at any print, only across it, or at none? The review recommends none); RV-4 (293: is s_260 + 1 already #845's own report via its recipe?); think-ikku RV-1 (130). think-4z8z (adoption plumbing) applies only if the answers keep any of them.

2026-10-31 bold-ritchie-l8, after review A of #861 (A1 blocking): **held unregistered.** The coordinator chose review A's option (a), which is the stage 4 review's own proposal: none of the three candidates is registered until the owner answers RV-3 (all), RV-4 (293) and think-ikku's RV-1 (130). Removed from #861 (commit 6454ae2e7): T-261 to T-263, the four E-register-candidates-2026-10-31-* evidence entries and their deferrals, the census rows, and the review's two route verifiers (V-ruu2-review-route-sat/-area), which wait with the evidence. Kept: the package packing/cases/register_candidates/think-ruu2-2026-10-31/ (certificates n-130/n-293/n-307.cert, the receipts on both maintained routes and the sharp controls, measure/, the review's code, out/ and inputs/), the mapped review record with a dated disposition note, V-register-candidates (text corrected: the 293 certificate was written by the review lane, whose routes share qio.py with the builder, so they are not clean-room there), and the tool and its tests. The earlier notes' T-261/T-262/T-263 numbers no longer exist; T-261 is now #545's grade-C claim. The select_houses KeyError that registration would expose, review A's A8 credit point at 293, and the registration order are on think-4z8z. This bead stays open for the owner's answers.
