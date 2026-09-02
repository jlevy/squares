---
type: is
id: is-01m1gb24s8a7zjpkjyrmzbbb9m
title: BC-142 reachable-tests control proves only inclusion, not exact equivalence
kind: bug
status: open
priority: 0
version: 1
spec_path: packing/campaign/agendas/agenda-015-ten-hour-earned-routes-and-guard-repairs.md
labels:
  - agenda-015
  - validation
dependencies: []
parent_id: is-01m1g7be4072ykvwbkw6madgap
created_at: 2026-09-02T05:56:52.647Z
updated_at: 2026-09-02T05:56:52.647Z
---
BC-142 requires an equivalence control for the strict changed-module reachable-test set, but test_reachable_tests.py asserts only one inclusion, one exclusion, and non-identity with the full suite. At HEAD the selector returns 13/115, all 13 through broad walker markers; the changed-module closure is only the benchmark wrapper. Record BC-142 as partial and build a refusable exact-set equivalence contract before claiming 3/3.
