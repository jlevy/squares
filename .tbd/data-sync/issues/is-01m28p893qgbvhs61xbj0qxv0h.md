---
type: is
id: is-01m28p893qgbvhs61xbj0qxv0h
title: "Phase 7: grade a physics configuration on the motion AND the outcome"
kind: feature
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T16:54:14.390Z
updated_at: 2026-09-11T20:11:53.847Z
closed_at: 2026-09-11T20:11:53.846Z
close_reason: "Built in 7e96fdfb: grade_motion.py reports outcome and motion separately and combines them with declared weights; six configurations ranked. The next steps it names (reduce wander, sweep the laws, move to devtools with Phase 6E, a grade floor in the gate) are follow-on work, not this bead."
resolution: null
duplicate_of: null
---
Built: atlas/known-best/video/spikes/v2-transitions/grade_motion.py, and recorded here because the METHOD is the deliverable, not the script.

A configuration graded only on where it ends up can thrash across the stage and still score well, because the lock-in carries whatever is left; one graded only on the journey can glide smoothly to somewhere wrong. So two families, reported separately and combined only at the end with the weights written down:

  outcome  residual, mean, turn   -- the run did not arrive and the lock-in is carrying it
  motion   wander                 -- a square straying from the line between its ends (thrashing, not travel)
  motion   jerk                   -- the worst single-frame step (a jump, not a glide)
  motion   overlap                -- squares passing through each other

At the shipped defaults over eight matched steps: residual 0.044 sides, turn 1.16 deg, wander 0.696, jerk 0.429, overlap 0.157, grade 0.292. THE OUTCOME HALF IS SOLVED AND THE MOTION HALF IS NOT, which the combined number alone would have hidden.

Ranking six configurations puts physics/anneal 0 first at 0.302 and every bodies setting last, and says the annealing dial buys nothing the grade values -- the shake was there to reach the record and the tightening phase now does that. That is the use: picking parameters against a number rather than an impression.

Next, in order: (1) reduce wander, which is now the dominant penalty -- the container's breath and the block matching are the two levers; (2) sweep the force law and the wall law through the grader the way the styles were swept; (3) move the grader to devtools with the rest (Phase 6E); (4) consider a grade floor in the gate once the number stops moving.
