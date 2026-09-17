---
type: is
id: is-01m2gxkzqdxb01e2h4tpkvczw7
title: Register the guidance ladder's hypotheses before the first round
kind: task
status: open
priority: 1
version: 11
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2p0xq9nac6ftmr19978krh3
  - type: blocks
    target: is-01m2pkfjyz4vn6cb3xvxhz61jc
  - type: blocks
    target: is-01m2pkfk9z36garp9891702grd
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-14T21:36:53.481Z
updated_at: 2026-09-17T03:16:19.804Z
---
Register the ladder's hypotheses before any round, per the experiment loop, with the instrument marked not ready until the extraction and kernel mechanics exist. Freeze or revise every planned registration default in the annealing plan's "Planned registration defaults" section first: seed-derived relabelling at grid and random starts, per-tier controls and eligibility, deciding versus reported arms, the work currency with compensation slots and realized work ratio, the deciding statistic, the replacements for accept-rule clauses 3 and 4, and the calibration selection rule. Candidates, each stated so it can fail under that deciding statistic (median block-best valid side below every deciding comparator's with non-overlapping ranges, over at least five paired blocks on every eligible held-out cell):

1. Merging near-flush groups into rigid blocks, contracting, then releasing gives a lower block-best valid side on the eligible held-out cells than either held welds or no welds, at equal work.
2. Structure used as a start gives a lower block-best valid side than the same structure held as constraints on every eligible held-out cell in the test set.
3. The true contact graph gives a lower block-best valid side than the unguided arm and a rewired graph of the same size; if it beats the unguided arm but not the rewired graph, the gain is from added forces, not from structure.
4. The least informative rung that beats the unguided arm is ordered by the record's remaining degrees of freedom, not by n.
5. Mechanism hypothesis, which cannot accept a search claim: an aligning torque is necessary for any contact-graph rung to realise its flush contacts.

Ids come from the integrated record at registration time, after checking parallel PRs, per conventions.md.

## Notes

2026-09-16 requirement transfer from duplicate think-1han: preregister the fixed guidance metric vector before measuring: packing validity, valid best side and known-result gap, component/contact/face recovery, false contacts, exact work and operational runtime (the continuity guard was dropped for Search rounds in the ecb44f8f revision), seed spread, and deterministic provenance. Recovery metrics are explanatory and cannot accept a search claim without valid-side improvement.


2026-09-17 (PR #190 approving review of 8eda51f1, design nits for registration): decide whether the compensation-slot multiplier is fixed per cell rather than per contrast, arm and setting, now that the work-only pilot covers every frozen cell (a held-out n that scales differently could otherwise leave the band); and state what an invalid calibration comparison does to the selection of the setting carried forward.
