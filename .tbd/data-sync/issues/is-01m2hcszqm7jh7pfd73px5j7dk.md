---
type: is
id: is-01m2hcszqm7jh7pfd73px5j7dk
title: "PR #125 review D24: basin-hopping seeds use per-process hash(); wall-clock bound unrecorded"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:18.739Z
updated_at: 2026-09-15T02:15:45.798Z
closed_at: 2026-09-15T02:15:45.797Z
close_reason: "Fixed in 5193a361: seeds derived with zlib.crc32 and recorded in meta.json with the derivation and quench bound; exp-204 Limits records the replay limit (salted hash, wall-clock bound reached by 408/500 and 485/500 quenches)."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F23 (Medium); triage row D24.

packing/devtools/run_basin_hopping.py (:202) seeds with hash(condition) % 251; str hashing is randomised per process (132, 200, 6 under PYTHONHASHSEED 0, 1, 2), so exp-204's per-seed ranges cannot be re-run. The 5 s wall-clock quench bound is a second unrecorded source of nondeterminism. Fix: stable derivation, derived seed and time bound in meta.json, replay-limit note in exp-204.
