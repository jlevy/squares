---
type: is
id: is-01m1sx5m1p5868jhwcdzfkvada
title: The mutation-snapshot cap has 0.9% headroom and the record keeps growing
kind: task
status: open
priority: 1
version: 6
labels: []
dependencies: []
created_at: 2026-09-05T23:06:30.837Z
updated_at: 2026-09-22T19:46:18.161Z
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

2026-09-16: PR #189 measured the clean hosted mutation snapshot at 168,058,379 bytes, 286,219 bytes over the 160 MiB ceiling. This is tracked source growth, not cache drift; the Animate branch itself added only compact retained evidence plus maintained source. The ceiling was reset to 192 MiB, restoring about 32 MiB of operating headroom and bounding three portable workers at 576 MiB. The bead stays open for its durable generated-file dependency audit; the cap reset is not that audit.


2026-09-16 recovery: the 192 MiB reset above is undone on PR #188 (da2259fb). With c302b330's prune of the agenda 031-035 and exp-201/202 output roots, the merged snapshot is 144,637,123 bytes against 160 MiB. The durable generated-file dependency audit this bead owns is still outstanding; between 2026-09-09 (135,122,909 bytes) and 2026-09-16 (168,058,379 unpruned) the record grew about 33 MB, of which 23.2 MB was output roots now pruned, so the unprunable growth rate is closer to 10 MB/week and 22 MiB of headroom is a few weeks, not a standing margin.

2026-09-22, PR 218 (bead think-gatp). The composite-SVG candidate this bead nominated is
disproved, and the trace it asked for is done for that half.

Traced rather than inferred: no registered control drives `build_known_best_atlas --check`,
`render_composite_pdf --check`, or any atlas step. The two controls that name
`atlas/known-best/` reach the small contact JSONs at its top level, the `touches` glob
control matches paths without reading them, and the single full-suite control refuses at
collection before a test runs. So nothing a control runs reads either composite vector's
content.

But the prune still cannot pay, for a reason this bead did not anticipate. `README.md`
links both vectors inline -- `known-best-1-100.svg` on line 31, `known-best-1-324.svg` on
line 39 -- and the root README is one of the documents `linked_pruned_targets` scans.
`snapshot_source_bytes()` returns the identical 168,251,525 with the poster pruned, with
the n=1..100 vector pruned, and with both. The copy-back is load-bearing rather than
accounting noise: four controls run `devtools.check_readme`, which calls
`check_synopsis.check_links`, which refuses any relative link whose target does not exist.
Remove the copy-back and all four report a dead link instead of the refusal they rehearse.

Four exports already in `PRUNE` are inert for the same reason: `known-best-1-324.png`,
`known-best-1-100@2x.png`, `known-best-1-100.png` and `known-best-1-324.pdf` are all
linked from `README.md` and all copied straight back, 4,646,026 bytes that never leave a
snapshot.

So the bead narrows. Struck from its scope: the composite vectors, and any prune whose
target a checked document links inline. What remains is (a) the four large generated JSONs
-- `chunk-components.json`, `chunk-partitions.json`, `exp-042`'s result and
`translation-escape-screen.json`, 23.7 MB together -- which still need the same trace, and
(b) the structural fix this measurement newly identifies: a link scan that tolerates a
pruned target, or a placeholder for one, which is the only thing that would let the
composite vectors and the four inert exports actually leave the snapshot.

The 2026-09-22 breach itself was answered without any of that. Agenda 041's output root
joined `PRUNE` for a net 10,624,188 bytes -- the same retained-output class as agendas 031
and 033--035 -- taking the snapshot to 157,627,337 with the 160 MiB cap unchanged. Agendas
037, 038 and 040 were examined and excluded: tests and `devtools/check_class_record_claims.py`
read them from outside the record.

Do not close this bead on the strength of the above. Half its trace is done and the other
half is not.
