---
type: is
id: is-01m57xnbtbzmgefz6bdm37xje9
title: "W2 #668: replay all retained de Winter certificates and source checker controls"
kind: task
status: closed
priority: 2
version: 7
delegate: c-lane-692
labels:
  - result-import
dependencies: []
parent_id: is-01m5733s8sp4ftvztm0sndswpb
hold: null
hold_until: null
created_at: 2026-10-18T16:31:34.218Z
updated_at: 2026-10-23T05:32:42.611Z
started_at: 2026-10-18T16:31:48.125Z
closed_at: 2026-10-23T05:32:42.611Z
close_reason: "Tracker audit 2026-10-23 (c-audit-c-1023, think-lrg9), checked by coord-intake-1023: DONE. Replay on both maintained routes integrated as E-de-winter-668-upper-exact-feasibility (result-requests #668 notes), 7c801b596 on main, T-196 V3/C3 (#704); the record states no run of the source's verify_all.py exists, which the rung does not need"
resolution: null
duplicate_of: null
---
Stage 4 source replay lane for GitHub #668, n=227,229,260. Owner: Codex de_winter_668_replay. Read retained verify_all.py and all three imported source validators before any execution; run unmodified retained entrypoints for all three complete certificates with Python 3.14.7, standard library and no network, explicit external TMPDIR/CARGO_TARGET_DIR/UV_CACHE_DIR, in isolated external scratch after root releases the #665 heavy slot. Price: expected 15-45 seconds serial; conservative 180-second total wall ceiling covering three complete verify_all.py runs, at least two geometric mutant refusals for each of the three accepted checker implementations at each count, binding checks, receipt serialization and interpreter startup. Basis: 716 squares and 85,427 unordered pairs per route (256,281 pair-route decisions); source clipping receipts report 0.651s/0.711s/0.489s for the three witnesses; two other source routes use exact rational SAT with AABB pruning. Wall ceiling is an estimate, not a measurement. Retain source digests, complete logs and mutant receipts; add a durable test; register all deciding verifier programs and Stage4 evidence once Stage3 allocates IDs. Do not inspect the separate Astra independent checker/review until the source receipt is sealed. Independence disclosure: tbd show of parent exposed its older static mathematical audit; this lane does not claim context-free mathematical review. Do not run before slot release, raise rungs prematurely, merge or message the author. Eventual replay branch to be coordinated with root; no provisional T ID. blocked_on: jlevy/squares#665

## Notes

2026-10-19 20:55Z lane-new: taken over from the 19 October handoff (#684) with its import beads. The earlier replay and review outputs were left on the Mac and are not in Git; this lane re-runs the replays here (devtools.upper_bound_reports certify / check --replay) and has the stage 4 review written by a separate reviewer session.

2026-10-20 lane-new: replay done on claude/intake-2026-10-20-de-winter-668 7c801b596: upper_bound_reports certify (9 jobs, 425 route CPU-s, 490 job wall s) and check --replay both pass; receipt retained in the packet.
