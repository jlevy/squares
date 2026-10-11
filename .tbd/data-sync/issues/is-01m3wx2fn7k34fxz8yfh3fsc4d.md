---
type: is
id: is-01m3wx2fn7k34fxz8yfh3fsc4d
title: Hold a register entry scope to the scopes of its cited evidence, and extend the register coverage gate to upper bounds by others
kind: task
status: open
priority: 2
version: 1
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
created_at: 2026-10-01T23:33:54.982Z
updated_at: 2026-10-01T23:33:54.982Z
---
W7. check_results does not compare a result scope with its evidence scopes: T-045 claims s(32) >= 119/20 and cites one entry whose scope is 27, 28, 31. The coverage gate reads lower bounds only, so T-056, T-057 and T-065 are registered by convention. Add both checks with negative controls, and add the n = 32 evidence entry for T-045 from the retained replay receipt.
