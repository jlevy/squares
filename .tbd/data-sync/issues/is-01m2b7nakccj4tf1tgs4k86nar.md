---
type: is
id: is-01m2b7nakccj4tf1tgs4k86nar
title: Search as a third mode, with its own controls and readout
kind: feature
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
created_at: 2026-09-12T16:36:56.555Z
updated_at: 2026-09-13T04:54:24.843Z
---
The third mode. One n, many runs, and a readout about the distribution rather than about one trajectory.

**What it has to show, because these are what the first night measured and none of them are visible today:**

- **How many of the runs are packings.** The single most important number, and the one whose absence made two rounds of benchmarking meaningless.
- **Best-of-k**, as a ladder, because a trial costs half a millisecond and the median is below the trivial grid at every n -- this method only exists as restarts.
- **The distribution**, not a single figure: best, median, worst on the `closed` scale where 1 is the record and 0 the trivial grid `ceil(sqrt(n))`.
- **The best arrangement found**, on the stage, so the owner can look at it rather than read about it.

**What it controls.** The trial count and seed range; which parameters vary between trials and over what values; and the parameters themselves -- the shake dial, the container inflation, the force law -- which Pack also has, because a search is many of Pack's runs.

**The finding it exists to make visible.** The shipped shake level is 3, chosen for how the animation looks. Below level 6 the best of a thousand valid runs never clears the trivial grid at any n; at 6 to 8 it reaches within half a per cent of the record at n = 5 and 10, and n = 11 clears the grid for the first time. A reader should be able to see that by moving one control.

Depends on think-r8kp: without the resolver the tab would display the same invalid numbers the harness did before its guard existed.

Do not fork the physics. A search run is `physics(index, style, mode)` at a different seed, and the mode's job is to ask for many of them and summarise, never to compute differently.

## Notes

2026-09-12 owner: defer Search until cleanup and standalone package phase complete. Actual dependencies now point to think-nals, not stale textual think-r8kp. Pack and Search must consume the same single-run kernel; the current benchmark instead exercises cached animation trajectories, so parity must be established first. Calibrate becomes a held-out/sweep preset within Search, not another engine or tab implementation. See updated plans/review.
