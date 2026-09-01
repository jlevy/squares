---
type: is
id: is-01m1dqc43wtym6hsxmbnqca2k8
title: "BC-115: productize the weighted-certificate lane after two consumers exist"
kind: task
status: open
priority: 2
version: 2
spec_path: packing/campaign/agendas/agenda-012-weighted-proof-precision-bridge-and-cross-scale-controls.md
labels:
  - packing
  - agenda-012
dependencies: []
parent_id: is-01m1dbej7kqs8r1hwfmx5w3v3n
hold: blocked
hold_until: null
created_at: 2026-09-01T05:34:19.258Z
updated_at: 2026-09-01T05:42:59.061Z
---
Blocked on BC-112 and a named second fixed-certificate consumer. Build a generic exact certificate reader/checker with two retained consumers, migrate the n=17 fixture without changing its result, repair the inclusive-endpoint defect in the float LP candidate generator, and add mutations that separate generator failure from exact-certificate failure. This tool block cannot adjudicate H-006 or H-034 and cannot move a frontier claim.

## Notes

Manual blocker: BC-112 must be terminal and a second fixed-certificate consumer must be named in the agenda before this hold is removed. The dependency edge alone is insufficient; do not let BC-112 completion auto-advertise productization.
