---
type: is
id: is-01m2cv8kt14nnbtwmm0v89fnmc
title: "PR #157 review READ-04: replay hashes bytes it may not have parsed"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:45.953Z
updated_at: 2026-09-13T08:41:09.136Z
closed_at: 2026-09-13T08:41:09.136Z
close_reason: "Fixed: Snapshot (replay_weighted_atom_source.py:65) holds path, digest and record from a single read_bytes (_snapshot, line 80), so the reported digest is the sha256 of the bytes actually parsed. Verified at the reviewed head: raising a declared count from 1 to 999 inside the parse/hash window gave reproduced=True with reader.sha256 c88a3478 (the CHANGED bytes) while the parse had used d00a6237; a plain replay of those bytes fails with 'declared token total 7, exact token total 1004'. Same on the family side: family.sha256 2eaf24ac bound to bytes that fail with 'family declares total_weight 11, its placements sum to 4039/4'. After: reported digest is d00a6237 = sha256 of the parsed bytes, and differs from the sha256 of the bytes on disk. Controls test_an_input_changed_mid_replay_cannot_be_digest_bound[reader] and [family] monkeypatch recomputed to rewrite the file inside the REAL window, so this is an executed race rather than an argument from source; both fail pre-fix."
resolution: null
duplicate_of: null
---
packing/devtools/replay_weighted_atom_source.py:191-223 parses each path, recomputes, then rereads the paths for their digests. Changing a declared charge from 1 to 999 during recomputation yields reproduced=True bound to the changed bytes, which then fail a normal replay. Fix: read each input once and parse/hash the same immutable byte snapshot; controls for both changing inputs.
