---
type: is
id: is-01m5ssz55ej9kv490x6skjj90m
title: "Import #804's 297: Hyukdong Kim's degree-21 exact side of T-174's packing, with its exact configuration (s297-exact-configuration.zip e08b5d0a, CC0)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: coord-n12-1025
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-25T15:13:20.558Z
updated_at: 2026-10-31T18:59:12.011Z
started_at: 2026-10-25T15:44:28.505Z
---
From read-only triage w-triage-1025b, 2026-10-25 ~15:20Z (findings: coordinator scratchpad triage-1025b.md). HyukdongKim on #804, comments 6397363927 (12:00:41Z) and 6397593690 (12:23:57Z): s(297) <= S*, the only real root of an irreducible degree-21 polynomial, claimed 3.36e-90 below T-174's certificate, with an exact configuration s297-exact-configuration.zip (SHA-256 e08b5d0a...47a7) under CC0, reported VALID on verify_exact.py. Checked here with SymPy: degree 21, irreducible, one real root matching the print, T-174 exact side minus root = +3.3591e-90 (decides nothing). Nothing else reports 297 below T-174. Disposition: a new register entry, a sibling of T-244 (next free id after main's T-246 is T-247; reserve before registering), decided on both exact routes (~2-8 CPU-h; needs an owner budget or the cap), sharing think-4rzl's tooling; draft S2. The attachment could not be fetched from this session (proxy blocks user-attachments). Coordinate with think-4rzl (c-decide-4rzl-1025), which edits the same #804 entry, packet and T-244 evidence.

## Notes

2026-10-31 coordinator (intake think-3guf): this bead now owns a queued ask on #804 (jlevy/squares#864, merged 737d8311e): take in Kim's s297-exact-configuration.zip (CC0; public copy HyukdongKim/square-packing-exact-sides f480441e), source issuecomment-6415293035; the public copy unblocks route B at 297. #804 cannot close while the ask is queued.
