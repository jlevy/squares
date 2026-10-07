---
type: is
id: is-01m3z64sddkyk2qq5vep420mqf
title: Selector finish stage, re-search the 90 flags, then F1 rank-2 residue sweep (lane S2)
kind: task
status: closed
priority: 1
version: 10
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: null
hold_until: null
created_at: 2026-10-02T20:50:56.556Z
updated_at: 2026-10-07T06:23:10.673Z
started_at: 2026-10-03T22:35:32.305Z
closed_at: 2026-10-05T10:04:21.819Z
close_reason: H1 landed on the session branch at 6bfd419ec/0fab37ef4 (census reads the recheck receipt; tests pin 87 flags/2,197 orbits at exp-250 and 86 flags after s182-k1)
resolution: null
duplicate_of: null
---
Session 168. Q1's residue survey (0e110249) found the selector's L-BFGS-B descent stops at maxiter 600 and polishes only below 1e-4, so flags between 1e-4 and 1e-2 may be false. S2 is adding a finish stage (long descent) to devtools/select_n17_sub_patterns.py, re-searching all 90 flags (arity-6/7/8 receipts) and running the full arity-8 sweep with --restrict-to-survivors 8 (Q1 found an arity-8 north-wall class removing 539 orbits deferred by the missing-pairs subset). Next: commit tool, tests and receipts; recompute projections.

## Notes

2026-10-03 05:25 UTC. Float-search speedup integrated 7581197f2: random-first stage, exact witness cache, early stop, vectorised penalty; verdict-equivalent on 1,608 classes (one old false flag now placed, mask 983968). Placed 4.5x, chunk 1.7x, full queue 26.4 -> 15.6 CPU-hours. Sweep restarted with --levers combined-fast from chunk 59. At 05:05: 29,500 of 423,756 classes, 49 flags, greedy cover 889 of 2,264 residue orbits (39%) in 26 picks; queue 1 done (14 flags), queue 2 hit rate 0.98%. Top flags: south-wall a8 539 orbits (stalls at 64 bins; adaptive rows next), a9 122 orbits pen 9.3e-3 and a9 66 orbits pen 1.3e-2 (queued for K2 at 64 bins). Next for S2: resume-from-screen (exact) and a compiled penalty (numba or extension), numbers first.

2026-10-03 evening. The resume lever landed (73a68676d, lever set combined-fast-resume). The full budget continues from the screen's checkpoint, verdict-identical on all 21 of 27 chunk-61 classes that reached the full budget, and saves 11.5% of CPU on flagged classes (about 10.7% of a chunk like 61). The live sweep stays paused at chunk 61 (SIGSTOP, pid 900; its timeout ends about 14:49 UTC on 2026-10-04). At about an hour a chunk over 848 chunks, the bottleneck is certifying the flags it finds, not the sweep.

2026-10-05 (PR 347 status survey). The title's first two parts are done: the finish stage, and the 90-flag recheck (16ea38d81: 89 still flagged, 1 placed). Left: point the census's flag list at the recheck (it still projects 88 classes and 2,189 orbits; 87 and 2,197 once corrected; the recheck receipt's schema n17-sub-pattern-recheck/v1 is not the selector's, so the census cannot read it as is), and resume the residue-universe sweep, paused at chunk 61 of 848, whose process passed its timeout on 2026-10-04 at about 14:49 UTC.
