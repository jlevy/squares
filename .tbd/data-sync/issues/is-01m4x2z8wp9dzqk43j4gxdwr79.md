---
type: is
id: is-01m4x2z8wp9dzqk43j4gxdwr79
title: "Import wand125: the independent checker cfcheck for the closed form (problems/closed-form/indep-checker at 746e2c5), intervals 1 and 34 (#600)"
kind: task
status: in_progress
priority: 2
version: 7
delegate: serene-hopper
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
child_order_hints:
  - is-01m4xpw83n12s71g17jgfd8msr
hold: null
hold_until: null
created_at: 2026-10-14T11:32:43.030Z
updated_at: 2026-10-14T17:22:39.518Z
started_at: 2026-10-14T11:32:48.901Z
---
746e2c5 (2026-10-14T10:38:27Z), after think-tsox's 9a28a84 pin, adds cfcheck under problems/closed-form/indep-checker/: a Rust checker written from SPEC.md only, the author says sharing no code with replay4d, which accepted every leaf of intervals 1 and 34 (91,044 roots, 3,138,681 leaves, 0 refusals). New evidence for the closed-form claim (#600): a later-revision packet, a priced or run replay of intervals 1 and 34 here, and an evidence-update plan for the records lane (session 01UXZs37jGv5vqVGADH7Gkn8).

## Notes

2026-10-14, intake lane wand125-cfcheck (writer sub-agent of squares-43), branch lane/wand125-cfcheck, commit c7bfaa32d on 10a8e0b4b; not pushed.

Stage 1. Pin 746e2c5ac7a7f534996dd50a5e1fd9f1d8836a8d (2026-10-14T10:38:27Z, tree d2ba54e9), the child of the 9a28a84 pin. It adds problems/closed-form/indep-checker/ (32 files) and changes problems/closed-form/README.md; nothing else in the tree changes (the folder's other 25 files are byte-identical, pinned by acquire_source against the 9a28a84 packet). Triage row: new evidence about a registered entry: no new entry, source retained at 746e2c5, evidence update.

Stage 2. Packet packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/ (34 retained, 26 pinned, acquire_source --check PACKET_MATCHES_ITS_CONTRACT); key [wand125 cfcheck 2026-10-14] in bibliography.yaml and resources/README.md; MIT; credit wand125, lineage independent; README names Codex, commit names Claude Opus 5.5, issue #600 names Claude and Codex for both checkers.

Independence. Source: "Written from SPEC.md and the published bundles only; shares no code with the original checkers (replay4d, seam4d_core, validate_family.py), which were not read." Found (comparison/shared_code.py): 0 shared files, lines, comments, local crates or arithmetic kernel; longest plain run 34 tokens (baselines 15-18); renamed overlap 1.16% of 25-token windows (baselines 0.05-0.15%), every run of 30+ tokens traced to a procedure SPEC.md states step by step (6.2 tiling, 5.11 B4U frontier with the 2/3 resample and 60/2000 limits, 5.4 sampling loop, 5.11 edge quadratic, 4 half-angle normals) or to idioms; positive control found. SPEC.md is the producer's own description of its checker's procedures, and the reviewer (Hosono) wrote the producer's code: independent implementation of the producer's specification; clean room as stated, not checkable.

Stage 4, a stated sample (receipts/): build from the retained copy, rustc 1.97.0, locked crates, 42 tests pass. Premises in full on intervals 1 and 34, none refused; 2,909 leaves accepted (1,320 on interval 1 top.rec, the smallest record; 1,001 and 773 per-kind samples); 3 re-sealed mutants refused (duplicate root; CORE1:Tx relabelled CORE; masses x 99/100). 42.9 CPU-minutes. Price of the complete two-interval replay: 288.45 worker-hours at the source's rates (242.02 recorded + 46.43 resumed), about 320-650 CPU-hours here; all 136 records by cfcheck about 9,900 worker-hours. Interval 34 carries only the record's 33 proved counts m^2-1, -2, -3 (m = 8..18); interval 1 carries none.

Evidence-update plan for the records lane: packing/resources/web/wand125-closed-form-cfcheck-2026-10-14/evidence-plan.md (E-wand125-closed-form-cfcheck-report, E-wand125-closed-form-cfcheck-sample, V-wand125-cfcheck). No rung moves.

Gate: packing-validate --edit, 2 steps failed, both identical on clean 10a8e0b4b (branch is 50 commits behind origin/main): published URL registry (t-157..t-160, t-037, n-264) and synopsis release impact.

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): cfcheck's evidence on T-180: E-wand125-closed-form-cfcheck-report, E-wand125-closed-form-cfcheck-sample and V-wand125-cfcheck; no rung moves.

## Validation backlog (2026-10-14, owner's cap: hold anything > 40 CPU-h)

The complete cfcheck replay of intervals 1 and 34 is its own bead, think-o4kf: 320-650 CPU-h (288.45 worker-h at the source), HELD; a proposed subset is the two top.rec records, about 12-13 CPU-h. The whole backlog is think-lh7d.
