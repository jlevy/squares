---
type: is
id: is-01m46vexyyvrwth1swj4kb18nm
title: Independently re-implement the Lemma 4.10 box labelling of Ryu's k^2 - M(k) >= 0.033 log k (review RF-1)
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-05T20:18:10.014Z
updated_at: 2026-10-05T20:18:10.014Z
---
Ryu's preprint (jlevy/squares#368, packet packing/resources/web/squarepacker-k2-minus-c-2026-10-05, recorded in packing/frontier/asymptotic-waste-bounds.yaml) rests its constant 0.033 and the k >= 10^13 formula on Lemma 4.10: 78,673 boxes each labelled infeasible, no side pair, or E_II + W_I + sum D_i* <= 9. On 2026-10-05 (think-8nv9) the source's own verify_leaves2.py re-verified every box here (reproduced with the producer's code), and three coverage programs found no gap. The labelling has one implementation, which shares the search's cell grid, float prefilter, split rule and float point count max_points (review docs/project/reviews/review-2026-10-05-squarepacker-k2-minus-c.md, RF-1 and RF-2). Write an independent labeller from the proof of Lemma 4.10 (the disc model, without reading verify_leaves*.py or bnb*.py), with an exact or ball-arithmetic point count, run it on the retained box lists, and record it as a second route. Without it the analytic Lemma 4.9 still gives 0.027.
