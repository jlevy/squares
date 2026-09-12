---
type: is
id: is-01m29krxcs3exnz8e3zznsq84b
title: Seven hypotheses about why the annealing does or does not find a packing
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
created_at: 2026-09-12T01:30:08.151Z
updated_at: 2026-09-12T01:56:47.845Z
---
**Written before the sweeps, so the sweep tests them rather than generating them.** A hypothesis found in the data after the fact is a description of the data.

Each of these is a statement the harness can return true or false on, with the measurement that would do it. Ordered by how much they would change the method if true.

**H1. The annealing cannot find n = 11 at all, at any parameters.** n = 11 has a tilted square at 45 degrees and an irrational side; the blind run's grid drop has no reason to propose a tilt. If true, the honest conclusion is that this is not a search and should not be sold as one, and the effort goes to the animation instead. Measure: 1000 trials at the shipped defaults; success rate zero within tolerance.

**H2. Success is dominated by the initial drop, not by the annealing.** The blind run places the new square in the emptiest cell of a coarse grid. If the answer is decided there, the annealing schedule is decoration. Measure: hold the schedule fixed, vary only the drop (grid resolution, random placement, best-of-k); compare the spread of success rates against the spread from varying the schedule with the drop fixed.

**H3. The jiggle's decay exponent matters more than its amplitude.** The shake decays as (1 - tau)^1.5. Classical annealing says the SCHEDULE is what determines whether a search escapes local minima, and amplitude only sets the scale. Measure: a two-dimensional sweep of amplitude and exponent; if true, success varies along the exponent axis and is flat along the amplitude one over a wide band.

**H4. The contraction is too fast to be a search.** The walls close on the record's side over the move, and the clock only runs while the deepest overlap is within tolerance. A search needs time at each temperature; a monotone squeeze may be a quench. Measure: success rate against the number of steps, holding everything else; a search improves with steps, a quench plateaus early.

**H5. The tolerance for "found it" is doing more work than the parameters.** A tolerance of 1e-3 on the side and one of 1e-5 may rank parameter sets differently. Measure: rank the same sweep at three tolerances and compare the orderings.

**H6. n = 17 is easier than n = 11 for the annealing, despite being larger.** n = 17's record is a grid-like arrangement with one tilted block; n = 11's is not. If true, "hard for the annealing" tracks the arrangement's structure rather than n, which is the more useful predictor. Measure: success rates for n in {5, 10, 11, 17, 26, 29} at fixed parameters, against a structural feature of each record -- number of tilted squares, or the contact graph's regularity.

**H7. Deterministic replay is already broken.** The run is meant to be reproducible from its seed. If two runs with the same seed and parameters ever differ, every number above is noise. Measure this FIRST, and treat a failure as a blocker rather than a finding.

H7 is the one to run before any of the others.

## Notes

H7 answered before the harness was built, and in a stronger form than it was asked: replay is deterministic because THERE IS NOTHING TO VARY. Every generator in the page is seeded from n alone -- the cached simulator's shake from n, the live optimiser's from n and the start kind, the random start's poses from n -- so a given (n, parameters) has exactly one blind trial and it is the same one every time.

That is the right property for an animation and it makes a success rate impossible. think-45fh is the consequence: give the run a seed, defaulting to today's behaviour bit-for-bit, before anything else in this epic.

The other six hypotheses stand as written, but H1 (can it find n = 11 at all) now needs restating: at one trial per n the honest question is not a rate but whether the single trial lands, and a rate only becomes meaningful once seeds exist.
