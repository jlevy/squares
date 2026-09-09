---
type: is
id: is-01m23az2y5tqfaft2tmg4sn1zg
title: "X-024 slice A6: site separation on the threshold plateau duals with the depth-witness oracle"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T15:00:46.659Z
updated_at: 2026-09-09T15:00:46.659Z
---
From lane A3's F7 and S4 (packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-a3-threshold-loop-at-383-100.md). The threshold loop plateaus on the accepted 191/50 columns: 11.017916787 at 383/100, 11.000000000 at 153/40, and one round of two-of-three atom separation moves the 383/100 value by 3e-9. Both plateau duals are refused by the plateau reader at K2 -- depth 56217397/50000000 at a corner seam at 383/100, 548760309/500000000 at an interior meeting of the tilted pair at 153/40 -- so neither is a fractional packing of the plane and neither caps the method: the sites, not the atoms, are what these duals exploit. Three site rounds at 153/40 with the depth-witness oracle (the 300 deepest exact arrangement vertices per round, 2304 new sites in round 1) left the value at eleven and pushed the excess into a sliver 0.0006 wide where the right edges of wall squares at 0.26, 0.79, 1.58, 2.37 and 2.90 degrees interleave; the round-1 dual is 1/25-integral on its 35 heavy rows and sums to exactly eleven, and the reader refuses it at depth exactly 28/25. The slice is to close that sliver or to show it cannot be closed: place sites by the sliver's structure rather than vertex by vertex, or run the two-of-three generator directly on the retained 1/25-integral family (lane-a3-family-153-40-sites-round1-exact25.json) whose own K4 is unknown because the reader refuses a family above depth one. Retained inputs: the three duals, the exact-25 family, the reader verdicts and the three trajectories beside the lane report. Done when either a rows-complete value below eleven is frozen and decided by the two-route gate, or the plateau is shown to be a theorem about the method with its own sites, not an artefact of this site set.
