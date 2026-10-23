---
type: is
id: is-01m5k7rrfx0m41eja3qmnfercc
title: Records tier misses assess_frontier_rigidity --check, which an adoption can make stale (#731 went red in hosted validate after a green local records tier)
kind: bug
status: open
priority: 2
version: 1
labels:
  - validation
dependencies: []
created_at: 2026-10-23T01:59:50.013Z
updated_at: 2026-10-23T01:59:50.013Z
---
#731 adopted T-230 at 303 and passed packing-validate --records (52/52) locally, but hosted validate failed on 'frontier rigidity assessed here' (assess_frontier_rigidity --check: stale rigidity blocks for n = [303]), fixed by --update in 260a0cef0. A records change that moves a retained witness can stale a rigidity block, so the step belongs in the records tier (development.md validation tiers; OR-13). Add it, or make adopt_houses re-derive the block itself, with a test.
