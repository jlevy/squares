---
type: is
id: is-01m1mv95j3zcxpvpckwjxwf8gn
title: "BC-161: certify the first n = 12-specific lower bound (H-061)"
kind: task
status: open
priority: 0
version: 5
spec_path: packing/campaign/agendas/agenda-017-six-hour-generator-rigidity-ceilings-and-w9-block.md
labels:
  - packing
  - agenda-017
dependencies:
  - type: blocks
    target: is-01m1mv96kjz5ap9yv61k9w1r5d
parent_id: is-01m1mv6ykrged0hs7msmak2e5v
created_at: 2026-09-03T23:57:17.763Z
updated_at: 2026-09-04T00:28:07.463Z
---
Lane A W6, 105 minutes after BC-160's freeze. Run the frozen generator at n = 12 and side 19/5 on the registered site ladder (grid 29 plus at most two column-generation refinements) with 181 directions and B = 9973/10000 (effective unit-square side 38000/9973); the survey sized a separation sweep at ten to thirty seconds on four cores and generation at ten to ninety minutes, kill line at a restricted optimum of 12 - 1/500. Rationalise and verify exactly on two accumulation paths, one repair iteration then a typed stop. Freeze exp-060 with certificate bytes, hashes, direction list, per-direction minima, the V(G, K) ladder and dual, receipts under normal and -O Python, and the claim boundary. The side never moves after results; a converged dual reaching twelve at B = 1 is recorded as an exact ceiling that rejects H-061 as registered and is a theorem about the method. needs_review true until BC-162.
