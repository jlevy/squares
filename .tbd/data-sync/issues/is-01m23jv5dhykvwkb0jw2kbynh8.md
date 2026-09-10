---
type: is
id: is-01m23jv5dhykvwkb0jw2kbynh8
title: "Physics with memory: repel from local optima already visited"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T17:18:26.734Z
updated_at: 2026-09-09T17:18:26.734Z
---
Idea from the 2026-09-09 session. Map out the local optima a search keeps falling into, then place a repulsive term on those specific configurations, so a run that approaches an already-explored minimum is pushed away from it. Physics with memory about where it has been.

This is metadynamics (Laio and Parrinello, 2002) and its well-tempered variant: a history-dependent bias built from Gaussians deposited at visited points in a collective-variable space, used to fill basins so the dynamics escapes them. Neither the 2026-09-08 annealing survey nor the 2026-09-09 simulation survey covers it, which is a real gap in both -- the closest thing either records is basin hopping (H-137), which restarts from a perturbed incumbent rather than remembering where it has been.

Three things have to be decided before it can be built, and the third is the hard one:

1. The collective variable. Repelling in the raw 3n-dimensional pose space is useless because the squares are interchangeable -- a relabelled copy of a visited optimum is a different point there and would not be repelled. The variable has to be permutation-invariant. Candidates already in this repository: the contact-graph signature, the angle-class census, the chunk taxonomy (atlas/known-best/chunk-partitions.json). X-025 line ~1101 already lists these as candidates for a configuration distance and notes that no distance exists here yet.
2. Where the bias enters. In the projection search it cannot be a force, since there is no potential -- it would have to be a perturbation applied at restart, or an extra constraint set that excludes a neighbourhood of a visited point.
3. Whether the local optima are even distinguishable. exp-139 measured that the trivial grid traps every mechanism tried; if the other basins are as few and as flat, a memory buys little.

Entry points: devtools/sweep_structure_hints.py has the rung ladder this would sit at the top of (rung 5, 'additional memory constraints'), and devtools/known_structure.py extracts the structural signatures a collective variable could be built from.
