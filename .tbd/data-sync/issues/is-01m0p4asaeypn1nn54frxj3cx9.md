---
type: is
id: is-01m0p4asaeypn1nn54frxj3cx9
title: "Phase 2: the proposer interface"
kind: epic
status: open
priority: 1
version: 15
spec_path: docs/project/specs/paused/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0p4ath0k0w56dkyy7ryerwp
  - type: blocks
    target: is-01m0p4bvjsw40qb2e41ycygyqr
child_order_hints:
  - is-01m0p4askv3n2t3je7mefnhmsd
  - is-01m0p4asxdaenzfkx53j4vh6qs
  - is-01m0p4at6z9sdaabcqmave9t9d
created_at: 2026-08-23T01:39:00.557Z
updated_at: 2026-10-12T23:50:44.017Z
---
Epic. One contract: (n, pair_test_budget, keyed_rng, seeds?) -> configurations. A proposer never quenches, canonicalizes, decides validity, or writes the atlas, so a new strategy cannot change what a basin means and two proposers are comparable by construction. Thin by design. The existing sqsearch binary is adapted behind it via its JSONL output - no rewrite, because JSONL is 1.4% of a quench.
