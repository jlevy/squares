---
type: is
id: is-01m1sx5m1p5868jhwcdzfkvada
title: The mutation-snapshot cap has 0.9% headroom and the record keeps growing
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T23:06:30.837Z
updated_at: 2026-09-09T16:23:17.601Z
---
Measured 2026-09-05 after pruning packing/site/ and the link-preview card: the snapshot is 66,490,716 bytes against a 67,108,864 cap, 99.1% of it, 618,148 bytes of headroom. SNAPSHOT_MAX_BYTES' own comment says a guard with 2% headroom fires for the wrong reason; 0.9% is worse than the case it warns about, and the next committed artifact of any size trips it.

The cap has now been reached four times -- D-371 at 40 MiB, 2026-08-27 at 41,943,040 when the atlas SVG work landed, D-422 where 12 MB of the breach was bytecode the gate wrote into the tree it was measuring, and 2026-09-03 when the H-052 lane's solver state took it to 90,031,065. Each was answered by pruning or by raising, and the growth is the research record doing what it is supposed to do.

The comment names the durable fix and defers it: 'pruning what no control reads is the alternative to raising this again, and it belongs with the tier work rather than here.' The largest counted files under packing/ are chunk-components.json at 9,672,604, exp-042's result at 5,740,789, chunk-partitions.json at 5,220,955, bc-200-state-191-50.json at 2,545,923 and known-best-1-100.svg at 2,333,310 -- 25.5 MB in five files, over half the packing subtree's 48,054,972.

The composite SVG is the clearest candidate and was deliberately NOT taken here: it is named by no control (grep of controls.yaml gives zero) and is the same class as its PNG, PDF and 2x exports, all three already pruned. What stopped it is the second condition the existing entries state and check rather than assume -- 'read by nothing a control runs' -- which needs the controls that drive build_known_best_atlas --check and the deterministic SVG rendering step traced before the file is removed from a sandbox they run in. That trace is the work; the four large JSON results need the same one.

Also worth deciding rather than inheriting: the walk counts the working tree, not the git tree, which is why gitignored output could ever enter the number at all.

## Notes

2026-09-09, after the cap was raised from 128 to 160 MiB for T-026's registration.

The commit message for that raise says "nothing there is prunable". That is too strong,
and the measurement taken afterwards says so.

Excluding seven files from the snapshot -- `lane-a2-threshold-certificate-191-50-net360.json`
and the six largest lane A3 receipts, all under
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/` -- recovers
exactly 1,193,568 bytes and takes the tree to 133,930,591 bytes, under the OLD 128 MiB cap.

So a prune existed and was available at the moment of the breach. It was not taken, and
the reason is a real one rather than an oversight: those seven files are evidence, not
generated output. Every other prune this bead records (the composite SVG and its exports,
the bytecode of D-422, the site directory) removes something a renderer can rebuild.
These cannot be rebuilt without re-running the measurement, and removing them changes the
SOURCE SURFACE the controls exercise -- which is the second condition this bead already
insists on checking rather than assuming.

What this note buys: the next breach starts from a measured alternative instead of from
"nothing is prunable". Whoever hits it should decide explicitly between (a) raising again,
(b) pruning generated views after tracing the controls that read them, which is the work
this bead is about, and (c) pruning evidence files, which needs a policy on what the
record keeps rather than a size argument.

The 1,193,568 bytes are also the scale to keep in mind: it is under 1% of the tree, so
even taking the evidence prune buys roughly one more registration, not headroom.
