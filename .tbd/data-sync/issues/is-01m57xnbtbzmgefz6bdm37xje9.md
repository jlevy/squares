---
type: is
id: is-01m57xnbtbzmgefz6bdm37xje9
title: "W2 #668: replay all retained de Winter certificates and source checker controls"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m5733s8sp4ftvztm0sndswpb
created_at: 2026-10-18T16:31:34.218Z
updated_at: 2026-10-18T16:31:34.218Z
---
Stage 4 source replay lane for GitHub #668, n=227,229,260. Owner: Codex de_winter_668_replay. Read retained verify_all.py and all three imported source validators before any execution; run unmodified retained entrypoints for all three complete certificates with Python 3.14.7, standard library and no network, explicit external TMPDIR/CARGO_TARGET_DIR/UV_CACHE_DIR, in isolated external scratch after root releases the #665 heavy slot. Price: expected 15-45 seconds serial; conservative 180-second total wall ceiling covering three complete verify_all.py runs, at least two geometric mutant refusals for each of the three accepted checker implementations at each count, binding checks, receipt serialization and interpreter startup. Basis: 716 squares and 85,427 unordered pairs per route (256,281 pair-route decisions); source clipping receipts report 0.651s/0.711s/0.489s for the three witnesses; two other source routes use exact rational SAT with AABB pruning. Wall ceiling is an estimate, not a measurement. Retain source digests, complete logs and mutant receipts; add a durable test; register all deciding verifier programs and Stage4 evidence once Stage3 allocates IDs. Do not inspect the separate Astra independent checker/review until the source receipt is sealed. Independence disclosure: tbd show of parent exposed its older static mathematical audit; this lane does not claim context-free mathematical review. Do not run before slot release, raise rungs prematurely, merge or message the author. Eventual replay branch to be coordinated with root; no provisional T ID. blocked_on: jlevy/squares#665
