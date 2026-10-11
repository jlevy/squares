---
type: is
id: is-01m3p04ndehpya7g3mbmmad36g
title: "W7: implement native exact rectangle-density coverage verifier"
kind: feature
status: in_progress
priority: 1
version: 18
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
child_order_hints:
  - is-01m3q3330ehfw8jkg6n2jjkz76
  - is-01m3q333efvqtrjzbncve0efps
  - is-01m3q3yck931awc12wrdfjtc8b
  - is-01m3q9nxx8t416wr59nsvcve5z
  - is-01m3qtxksrtmt2kc5qqnxf6t97
hold: null
hold_until: null
created_at: 2026-09-29T07:12:51.117Z
updated_at: 2026-10-06T08:29:23.234Z
started_at: 2026-09-29T07:14:10.458Z
---
W7 block in docs/project/specs/active/plan-2026-09-29-native-rectangle-verification.md. Exact rational common-core polygon subdivision and axis event sweep, source-distinct from verify.cpp; library, CLI, refusal controls, proof contract review. Analytic full-net control and bounded retained input probe required before first checkpoint. Full large-certificate independent confirmation remains separate.

## Notes

Initial native engine and strict admission implemented. Astra-max independent review found no unsound acceptance path; corrected rotated and axis counterexample receipt accounting, independently re-reviewed fix.12focused test cases pass incl exact asymmetric8image orbit mass1/8 and commoncore area21/250 with16vertex/corner inequalities; Ruff/typesclean. Complete201-angle analytic control; retained n11angle1/100nodes remains inconclusive46accepted9pending. Next: retain identicalpendingboxes then compare sum-per-rectangle-min4corner bound against commoncore under30s; certify>=1previouslyunresolvedbox without weakerbounds; never take minimum of totalcornercoverage. Full retained certificate remains open.

Astra-max bounded next-slice assessment, 2026-09-29

This assessment used existing source and retained receipts only. No new geometric experiment, certificate replay, Rust build, or acceptance claim was made. Existing notes, description, status, and delegation are preserved.

The retained native n11 receipt binds candidate SHA-256 8e3339eefb2fad81868f51e3f72cbc8487b40b66f9d8fbc711c1dbd5e5edeff4 and checker SHA-256 eee2f2b05f7cde370c9ce7e0fe0c1aeb04a526604886bd7c0b5bdeb6bded6b78. It checks only angle 1, threshold 1, with limits of 100 nodes, depth 20, and 30 seconds. It records 100 nodes, 46 accepted leaves, and 9 unresolved leaves. Under the reviewed binary traversal these counts imply 54 splits, 9 queued boxes, and no already depth-capped leaves. Reaching the node ceiling is a sufficient reason for stopping. The receipt does not retain exact pending boxes, bound deficits, elapsed time, or explicit stop causes, so it cannot establish the full-run cost or diagnose a geometric bottleneck. This is not a counterexample or an observed contract defect.

Narrow next slice: add diagnostic retention of every exact pending centre box, its angle and depth, and stop reason, bound to the same input, source and run settings. Keep diagnostics separate from acceptance and do not add resume trust in this slice. Compare the existing common-core bound with sum_R density(R) * min_v area(R intersect Q(v)), where v ranges over the four centre-box corners, on that identical frontier with a 30-second ceiling. For each convex rectangle, convexity plus the planar Brunn-Minkowski inequality justifies the corner minimum throughout the box; nonnegative densities justify summing these separate minima. Taking the minimum of total corner coverage is not justified. Each common-core intersection is contained in every corner intersection, so the proposed bound cannot be smaller mathematically. Retain exact old/new values and costs; useful first evidence closes at least one previously unresolved box while preserving all refusal and accounting controls. It remains partial evidence.

Proposed analytic control, not executed: n=58, L=4, B=1/2, one source rectangle [1/10,1/10,39/10,39/10] with weight 1444/25. Its coincident D4 images give constant density 4 and mass 1444/25 < 58. For cosine 3/5 and sine 4/5 over the local centre box [2,3]^2, every core is inside the support, so exact coverage and the per-rectangle corner bound are 1. The current common core is empty because both local halfwidths are -9/20, giving lower bound 0. This is a local proof-primitive control, not an assertion that this candidate passes full-domain verification. Also retain a regression that rejects replacing the sum of per-rectangle minima with a minimum of summed corner values.

Full independent acceptance still requires one bound input to pass exact mass/admission and all 201 required angles with zero unresolved work, plus a complete source-bound receipt and an executable replay command. Target 1 suffices for the packing obstruction; the candidate's stored rhs=1001/1000 is not a proof of coverage. An actual uniform positive coverage margin would make common-core subdivision converge in principle, but does not predict a practical node budget. After a complete run, register new exact-algebraic evidence scoped only to the certificate/count actually checked and retain the existing interval-certified source replay separately. A native n11 success must not promote the entire n11/n26/n29 composite or the unrelated T-057 row claim.

Final Astra-max next-step review selected think-gfpf: exactly two refinement levels on each of the 67 retained depth-capped boxes, unchanged common-core bound, 268 child evaluations and 30-second cooperative cap. Exact analytic control has parent 9/25 and each child 169/100. This experiment is predeclared but unexecuted. The queued depth-1 box prevents inferring full-angle cost from the 1000-node prefix.

The two-level diagnostic think-gfpf met its predeclared local criterion: 15 of 67 depth-capped parents close after all 268 children are evaluated. This is diagnostic evidence only; complete native external coverage remains think-aqne. Next: design and cost a whole-angle traversal without treating the 1000-node prefix as a full-angle cost estimate.

2026-09-29 upstream integration: wand125 provisional T-056/T-057 map to canonical T-058/T-059. Published Couzo/de Winter retain T-056/T-057. Historical notes and archived receipts retain their original labels; no evidence bytes or acceptance level changed.

2026-10-06 (bead review): think-ck07 was closed as a duplicate of this bead. Carried over from it: any conversion of rectangle densities to point masses must bound the transport error and pay it from actual coverage slack (placing rectangle mass at cell centres is unsound without that proof), and input admission must include think-c0xc's guards. Evidence: docs/project/reviews/review-2026-09-22-tokoharu-density-mathematics.md.
