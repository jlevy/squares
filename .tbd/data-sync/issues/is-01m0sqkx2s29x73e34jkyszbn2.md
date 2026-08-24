---
type: is
id: is-01m0sqkx2s29x73e34jkyszbn2
title: Complete H-010 with Figure 14 unavoidability and correct D-091
kind: bug
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
created_at: 2026-08-24T11:13:45.560Z
updated_at: 2026-08-24T11:28:43.060Z
---
Validity recurrence of D-091. The 12-point Figure 14 set really is unavoidable; that fact is necessary but insufficient because the published proof also localizes one avoiding box and forces it to contain all three A points. Current H-010 omits the Figure 14 certificate and falsely says the standalone statement does not exist. Acceptance: a source-faithful five-node proof DAG certifies Figure 13 localization, the representative exceptional region, same-box A1/A2/A3 forcing, Figure 14 unavoidability, and the 3+9 counting contradiction; D-091 and living summaries state exactly what was missing.

## Notes

2026-08-24: D-091, H-010, synopsis, and master review now state all five nodes and restore genuine Figure 14 unavoidability. Keep open until exp-016 independently replays and mutation-tests every node.
