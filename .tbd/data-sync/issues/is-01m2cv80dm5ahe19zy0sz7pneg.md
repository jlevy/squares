---
type: is
id: is-01m2cv80dm5ahe19zy0sz7pneg
title: "PR #157 review MATH-02: interval token cap is checked after allocation"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:26.100Z
updated_at: 2026-09-13T08:11:09.490Z
closed_at: 2026-09-13T08:11:09.490Z
close_reason: "Fixed: threshold_interval.py:165-192 decides the per-atom token cap, the atom count and the padded table dimensions from DECLARED numbers (row_widths from token_count, never token_sites) before index/rows exist. Only the distinct-site cap stays after materialization, and it bounds data the certificate already carries. Verified with tracemalloc peak during the refused call: 4097 tokens 67,008 -> 1,147 bytes; 2,000,000 tokens 33,129,464 -> 910 bytes (was linear in the declared count, so ~16GB at 1e9). Sentinel test patches token_sites to raise on access: it fired before the fix, and after the fix IntervalInputError arrives with the expansion never attempted. Existing match= controls unchanged."
resolution: null
duplicate_of: null
---
packing/src/sqpack/fractional/threshold_interval.py:169-180 expands token indices and rows before checking MAX_TOKENS_PER_ATOM. A compact oversized input can exhaust memory before refusal. Fix: preflight token totals, atom count and padded table dimensions before materialization, with a bounded sentinel control at 4097 tokens that refuses any attempted oversized expansion.
