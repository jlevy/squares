---
title: "H-149 \u2014 six fixed dots cover the selected wall tuple"
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-149
  kind: hypothesis
  claim: The original five sites D plus the exact saved exp149 centre cover every residual B-core avoiding
    the selected wall footprints for tuple (0,0,0,7), across all 361 retained directions.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: All 361 required directions have exact zero uncovered area
    direction: positive
    threshold: '0'
  instrument: packing/devtools/wall_owner_six_dot_cover.py
  instrument_ready: true
  regime: q=96/25, B=9977/10000, exact original D followed by exp149 centre, same exp146 four selected
    footprints and complete exp143 direction manifest.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: One 300-second external process plus two-second grace; shared 240-second internal guard
    after inputs.
  prereqs:
  - Admitted fixed six-dot source and synthetic controls; independent Astra Max source review.
  - Clean published prospective protocol; exact exp143, exp146 and exp149 bindings and replay.
  replication: false
  registered: '2026-09-09'
  notes: Chosen after exp150 refuted individual-owner exclusion of the saved escape. Accept only all 361
    zero deficits; first independently replayed strict escape refutes only this fixed six-dot cover. Partial
    or invalid remains unresolved. Old five-dot masks and dot-set symmetries are not inherited.
---
# H149: Can One Additional Dot Close This Branch?

The new site is fixed to the saved exp149 escape centre.
It hits that particular core and preserves every original dot hit, but the full cover
remains untested. Six dots would still contradict seven separated residual cores after
four distinct owners have been selected.
This is a conditional tuple exclusion, with global routing still open.

See the
[admitted design](../../cases/n11_five_dot_cover/after-exp150-decision-contract.md).
Source controls pass: 13 combined tests, clean Ruff and BasedPyright.
[Independent source admission](../../cases/n11_five_dot_cover/six-dot-source-admission.md)
is GO. Exp151 now refutes this fixed six-dot set: its first six directions are covered,
but owner-006 admits a replayed strict escape.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
