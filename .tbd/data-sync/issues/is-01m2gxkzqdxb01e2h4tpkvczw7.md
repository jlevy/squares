---
type: is
id: is-01m2gxkzqdxb01e2h4tpkvczw7
title: Register the guidance ladder's hypotheses before the first round
kind: task
status: open
priority: 1
version: 8
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
updated_at: 2026-09-17T02:35:20.894Z
---
Register the ladder's hypotheses before any round, per the experiment loop, with the instrument marked not ready until the extraction and kernel mechanics exist. Candidates, each stated so it can fail:

1. Merging near-flush groups into rigid blocks, contracting, then releasing reaches the n = 29 record at a higher valid rate than either held welds or no welds, at equal work.
2. Structure used as a start beats the same structure held as constraints at every n in the test set.
3. The true contact graph beats a rewired graph of the same size; if it does not, the gain is from constraining, not from structure.
4. The smallest successful rung is ordered by the record's remaining degrees of freedom, not by n.
5. An aligning torque is necessary for any contact-graph rung to realise its flush contacts.

Ids come from the integrated record at registration time, after checking parallel PRs, per conventions.md.

## Notes

2026-09-16 requirement transfer from duplicate think-1han: preregister the fixed guidance metric vector before measuring: packing validity, valid best side and known-result gap, component/contact/face recovery, false contacts, continuity guards, exact work/runtime, seed spread, and deterministic provenance. Recovery metrics are explanatory and cannot accept a search claim without valid-side improvement.
