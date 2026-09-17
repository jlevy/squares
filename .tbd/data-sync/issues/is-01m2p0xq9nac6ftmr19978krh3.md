---
type: is
id: is-01m2p0xq9nac6ftmr19978krh3
title: Run pre-registered stickiness and guidance sweeps on known packings
kind: task
status: open
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
refs:
  - kind: pr
    url: https://github.com/jlevy/squares/pull/190
    at: 2026-09-16T22:15:42.195Z
labels:
  - research
  - experiment
dependencies: []
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-16T21:10:50.420Z
updated_at: 2026-09-17T02:36:05.658Z
---
Use the durable experiment loop to run paired, interleaved seed sweeps over ordinary stickiness and each guidance tier. Start with known-answer controls spanning small, medium, crowded, symmetric, and multi-component contact structures; tune only on the declared calibration set and judge on held-out cases. Record every accepted, rejected, invalid, and no-effect round with median/range or stronger intervals, fixed budgets, exact engine commit/configuration, and generated ledger views. Only after the known controls recover high-quality valid packings may the campaign test open instances or claim search benefit.

## Notes

2026-09-16 reconciliation: this is the genuinely new deliverable retained from think-ejn6. It owns the first preregistered systematic sweep of ordinary stickiness and the graded guidance ladder. Open a truthful successor experiment series; do not append incomparable rounds to legacy series-000. Start with unguided baselines, paired/interleaved seeds, fixed work, known-answer calibration and held-out confirmation, retaining every invalid, rejected, and no-effect round.


2026-09-17 (PR #190 revision): this bead is the systematic guided sweep only. The unguided stickiness response curve moved to think-9hdg, whose held-out result fixes the stickiness level guided arms use; the partition freeze is think-05o4; guided Search receipts are think-10yz. It is a research consumer of Phase 5A, not a product gate (think-wln2 does not depend on it). No guided-vs-unguided comparison is admissible until think-gdkd declares the work currency and deciding statistic.
