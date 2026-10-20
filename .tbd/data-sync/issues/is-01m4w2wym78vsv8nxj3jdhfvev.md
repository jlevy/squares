---
type: is
id: is-01m4w2wym78vsv8nxj3jdhfvev
title: Record the hosted checks-tier cost of the default-pictures step
kind: chore
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-14T02:12:12.551Z
updated_at: 2026-10-14T02:12:12.551Z
---
PR #591 (formal stack 498, layer 11) adds the step "default pictures improve on their house drawings" (packing/src/sqpack/cli/validate.py) with fast=True and records=True, so it also runs in the hosted checks tier. Its cost is so far quoted only locally: 5.3 s standalone at four workers, and 21-34 s inside --records under load (review A, finding A8). Once the cascade lands and pull-request CI runs the layer, read the checks-tier wall with devtools.read_tier_walls and record it in packing/devtools/gate-budgets.yaml under the checks tier, attributing the rise to this step if max_unattributed_rise requires it. Done when gate-budgets.yaml carries a hosted reading that includes the step and check_gate_budgets passes.
