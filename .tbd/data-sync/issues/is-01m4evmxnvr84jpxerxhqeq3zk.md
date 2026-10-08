---
type: is
id: is-01m4evmxnvr84jpxerxhqeq3zk
title: Bind the n=211 reflection lineage to its actual selected source
kind: bug
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T22:55:21.785Z
updated_at: 2026-10-08T23:09:11.518Z
started_at: 2026-10-08T22:55:31.318Z
---
Independent review of think-c7io found that a numerical n211 witness could be reflected with a fixed de Winter lineage even after a future selected-source change. Bind the registered reflection to the expected retained source path/key or derive a truthful generic parent. Reject mismatched parents before applying or recording the transformation. Add a focused mismatch regression and preserve current valid reflection behavior, exact verification and motion replays. Hold canonical record refresh until this provenance guard is reviewed and verified.

## Notes

Fixed the registered n211 reflection guard to require the exact retained de Winter parent path and key, including already-transformed reads. Mismatch regression passes; scientific replay and independent source/record review confirm honest raw-certificate false / ancestor-certificate true lineage. The other 323 cases and immutable parents are unchanged. Integrated validation remains in think-142l.
