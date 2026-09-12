---
type: is
id: is-01m2b7na7psnnn1j62g1yjdtta
title: The page can tell a packing from an overlap, and resolve one into the other
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
created_at: 2026-09-12T16:36:56.180Z
updated_at: 2026-09-12T16:36:56.180Z
---
**The foundational chunk, and it is worth doing even if the Search tab never ships.**

The page draws arrangements that are not packings and has no way to say so. Measured over 15,000 blind runs: every one ends with squares inside each other by 0.03 to 0.12 of a unit side. The page's gap bar already half-knows -- it computes a total overlap, calls the frame `valid: false` and hides its pointer -- but it has no notion of the container a *valid* version of that arrangement would need, so a run that ends overlapping has no honest number at all.

Two things move into the page, both already written and measured in `packing/devtools/bench_annealing.py`:

1. **A separating-axis test over the current poses**, giving the deepest pairwise overlap rather than a sum. The sum cannot distinguish one bad pair from many slight ones, and the deepest is what decides validity.
2. **A resolver**: push overlapping squares apart along each pair's minimum-penetration axis, angles held, until none overlap; then report the container the separated arrangement needs. It is a projection, never an improvement -- the resolved side is always at least the raw one, and the difference is how much of the raw result was overlap.

Both are cheap: 15 to 56 sweeps, sub-millisecond at these n.

**What it changes beyond the search.** The gap bar can show the honest side for any frame rather than hiding its pointer; a free or blind run can end on a packing rather than near one; and the owner can see, on the stage, the difference between what the physics produced and what it is worth.

**The control that must come with it.** The snapped trajectory ends on the record's own poses by construction and scores 5.5e-7 to 1.0e-6 of overlap. Any implementation that does not pass that control is wrong, and the checker should assert it.

Measured numbers this must reproduce, from the harness: blind runs at n = 5, 11, 17 score 8.4e-2, 3.5e-2, 8.6e-2 deepest overlap; resolving makes 120 of 120 valid.
