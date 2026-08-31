---
type: is
id: is-01m0tyazqn3sgwvee1yfv2b3yf
title: Harden the D-199 repair regression contract
kind: task
status: open
priority: 2
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - testing
dependencies: []
parent_id: is-01m0twy8zcmaz9q79aph5qx8kd
created_at: 2026-08-24T22:30:27.828Z
updated_at: 2026-08-24T22:30:27.828Z
---
Senior review approved the D-199 correction but found two low-risk test gaps: the synthetic cascade does not inspect successive b_ub values, and the retained n=10 fixture intentionally requires an exact solver path. Add a direct assertion that RHS tightening is componentwise monotone and cumulative, and separate the version-bound diagnostic path from a portable contract asserting optimal outcome, original-row residual <=1e-10, solver calls within the cap, and monotone tightening.
