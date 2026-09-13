---
type: is
id: is-01m2cv8kt14nnbtwmm0v89fnmc
title: "PR #157 review READ-04: replay hashes bytes it may not have parsed"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:45.953Z
updated_at: 2026-09-13T07:38:45.953Z
---
packing/devtools/replay_weighted_atom_source.py:191-223 parses each path, recomputes, then rereads the paths for their digests. Changing a declared charge from 1 to 999 during recomputation yields reproduced=True bound to the changed bytes, which then fail a normal replay. Fix: read each input once and parse/hash the same immutable byte snapshot; controls for both changing inputs.
