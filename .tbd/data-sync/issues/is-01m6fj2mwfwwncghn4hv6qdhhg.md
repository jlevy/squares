---
type: is
id: is-01m6fj2mwfwwncghn4hv6qdhhg
title: "Import Özden: s(94) >= 1993/200 by dilating Hosono's mixed_n94_L995 on a 600-direction net (#890)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l33
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m6fjg22q3p76p8eet2wp4jv0
hold: null
hold_until: null
created_at: 2026-11-03T01:58:43.855Z
updated_at: 2026-11-03T02:06:03.350Z
started_at: 2026-11-03T01:58:48.827Z
---
Import of jlevy/squares#890 (opened 2026-11-03T01:20:31Z by kenaznia-doga, an AI agent account posting for Doğa Özden): s(94) >= 1993/200 = 9.965, above the verified 199/20 of T-091 (Hosono, mixed_n94_L995).

## Claim map
- Source: kenaznia-doga/s94-lower-bound@9d76ad5549e99e952c899462b36d2bd765517969 (one commit, 2026-11-03T01:19:36Z; tree 1ef6aeda). Certificate certificate/n94_L9965.json.gz (format M, proof_net step 83/120000, last 599 = 600 directions; L = 1993/200, B = 19884161/19900000; 853 orbits, mass 9399999/100000). Stated digests: JSON text b8b03ee8...749c, .gz 116c8342...16f8; Hosono's candidate.json at wand125/square-packing-bounds@797bdf6e 64d81953...0667a.
- Claims in the release: (1) s(94) >= 1993/200 [register: a new lower-bound entry; T-091 keeps its claim, superseded at n = 94 once adopted]; (2) n = 31 negative note: Hosono's 2391/400 measure dilated to 2989/500 is refused (not a bound; recorded in the packet only); (3) the route's ceiling 99500/9977 (an observation, no claim).
- Consequence: s(95) >= s(94) >= 1993/200 settles nothing (n = 95 and 96 are proved = 10, T-191).
- Who else holds the value: nobody; the record's best at n = 94 is 199/20 (T-091, V3/C3).

## Validation plan (priced)
- Replay: this repository's sqverify-fast (reviewed source d97758bb, binary 567a0fd5) through devtools.sqverify_fast_census over all 600 declared-net directions from the retained bytes: about 7,900 CPU-s (the author's receipt; 2.2 CPU-h) at two threads; then the whole-net control (99/100 mutant at every direction, near-threshold mutant), and per-direction comparison with the author's two receipts.
- Producer relation: the author ran this repository's unmodified sqverify-fast, so the replay is same-implementation (reproduced with the producer's code). The author's second checker (Codex, exact-integer) is retained, not run.
- Review: a separately prompted stage 4 mathematical review (tbd-strong-max) is needed before the verified lane moves (declared-net review's records-lane item 7; verified_lane_review_problems).

Answer bead: this bead.
