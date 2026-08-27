---
type: is
id: is-01m1135hb7cm4gneyhbvmvws88
title: Replay El Moumni's n=7 proof as a source-faithful lower-bound control
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels:
  - packing
  - proof-control
  - focus-correctness
dependencies: []
parent_id: is-01m0qxpddtqxy7sbsdk90kbqm1
hold: blocked
hold_until: null
created_at: 2026-08-27T07:50:18.726Z
updated_at: 2026-08-27T09:28:03.265Z
---
Build an independent, source-faithful replay of El Moumni's 1999 s(7)=3 argument before using automated unavoidable-set synthesis on open cases. Acceptance: encode Proposition 1's center-containment condition, Proposition 2's parallel-line intersection bound, and the three symmetry cases for a hypothetical side 3-alpha; adversarially perturb at least one threshold or case route and require rejection; compare the resulting certificate with the retained published scan. Preserve the strict boundary: this is a published n=7 lower-bound replay, not evidence for n=11, not whole-class automation, and not packing feasibility for any generated scaffold. The n=15 Proposition 3 substitution may be a second control only after the n=7 route is independently replayable.

## Notes

2026-08-27 retained-scan audit stopped with typed blocker source_formula_blocked. D-344 records printed page 287's impossible |pr| = 2 sqrt(2) - 4 - epsilon; the coordinate-derived candidate 3 sqrt(2) - 4 - sqrt(2) epsilon remains a source-distinct, unadopted repair. D-345 records Theorem 1's dropped min(B,1) branch. cases/small_n/el_moumni7.py now proves the source-distinct two-branch Case 1 arithmetic exactly in Q(sqrt(2)) and focused tests reject the unbranched substitution, deleted third contribution, printed negative length, and inexact inputs. The complete source-faithful replay remains blocked: independently derive and audit the Figure 4 coordinates and downstream inequalities, then encode Proposition 1 and Cases 2-3 before any full-theorem verdict. No n=15, n=11, geometry, feasibility, or generic proof-automation claim.
