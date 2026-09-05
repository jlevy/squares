---
type: is
id: is-01m1sp9zws6twqngzdsphwnbm7
title: Resume the retained 3.82 primal-dual state
kind: task
status: open
priority: 1
version: 3
labels:
  - research
dependencies:
  - type: blocks
    target: is-01m1sp9x74c7706vvea0w6ga08
parent_id: is-01m1sp7k7txpwp2y4pbhen30jv
created_at: 2026-09-05T21:06:34.008Z
updated_at: 2026-09-05T21:37:28.121Z
---
BC-232: resume the retained 3.82 cutting state from its warm JSON with run_fractional_cutting --warm, not the incompatible NPZ column-generation checkpoint. Apply the fixed four-CPU-hour shrinkage rule. If the row-converged primal drops below 11, require a tested rationalize/freeze bridge before treating it as an exact certificate.
