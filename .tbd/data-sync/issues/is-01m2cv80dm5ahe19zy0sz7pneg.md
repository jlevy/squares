---
type: is
id: is-01m2cv80dm5ahe19zy0sz7pneg
title: "PR #157 review MATH-02: interval token cap is checked after allocation"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:26.100Z
updated_at: 2026-09-13T07:38:26.100Z
---
packing/src/sqpack/fractional/threshold_interval.py:169-180 expands token indices and rows before checking MAX_TOKENS_PER_ATOM. A compact oversized input can exhaust memory before refusal. Fix: preflight token totals, atom count and padded table dimensions before materialization, with a bounded sentinel control at 4097 tokens that refuses any attempted oversized expansion.
