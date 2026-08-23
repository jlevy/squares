---
type: is
id: is-01m0pd7gxn1a3cxzsrsgr1kt4t
title: Schema permits one round to name many hypotheses under one verdict
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T04:14:30.815Z
updated_at: 2026-08-23T04:14:30.815Z
---
experiment.schema.yaml has hypotheses: minItems 1 with no maximum, and a single verdict.decision. exp-006..009 named [H-002, H-019] and the verdict for H-002 was applied to H-019, so the ledger reported H-019 as refuted by the rounds whose data confirmed it. Instances fixed by splitting exp-010; the schema still permits it, so the next runner reproduces it. Fix: constrain to one hypothesis per round, or make verdicts per-hypothesis.
