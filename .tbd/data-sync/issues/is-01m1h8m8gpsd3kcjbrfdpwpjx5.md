---
type: is
id: is-01m1h8m8gpsd3kcjbrfdpwpjx5
title: Repair OR-10 negative-control drift after OR-10 became real
kind: bug
status: closed
priority: 1
version: 2
spec_path: packing/campaign/agendas/agenda-015-ten-hour-earned-routes-and-guard-repairs.md
labels: []
dependencies: []
parent_id: is-01m1g7btz9tbnfvpxdtkc0rqd1
created_at: 2026-09-02T14:33:34.997Z
updated_at: 2026-09-02T14:56:13.140Z
closed_at: 2026-09-02T14:56:13.139Z
close_reason: Fixed both synthetic rule IDs at OR-11; all three operating-rule negative controls fire for their intended reasons.
resolution: null
duplicate_of: null
---
The full BC-146 gate found that the 'new operating rule never reaches the summary' negative control still injects OR-10 after OR-10 became a real rule, so it fails contiguity instead of the expected summary-drift reason. Bump the synthetic rule to OR-11 and rerun the focused control.
