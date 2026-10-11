---
type: is
id: is-01m41yh02z23zwxq1ma1bvk8et
title: Run linear-control n82 (and n83 if missing) so T-076/T-073 carry a refused mutated control, as T-080 does
kind: task
status: open
priority: 3
version: 2
labels:
  - records
dependencies: []
created_at: 2026-10-03T22:35:31.295Z
updated_at: 2026-10-06T08:33:29.592Z
---
The complete replays of the linear n82 and n83 certificates are recorded (#327), but main holds no control.json for n82 or n83 (T-080's n101 has one). Run devtools.audit_wand125_linear linear-control n82 and n83 and record them; corrected the #294 closing note in place on 2026-10-03 21:40 (it had claimed a refused control for n82).

## Notes

2026-10-06 bead review: think-ve95 (under think-ntuu) was closed as a duplicate of this bead. It added one detail: add the n82/n83 control.json files beside receipts/n101/control.json with tests. On origin/main eb43ffe9a only packing/resources/web/wand125-linear-certificates-2026-10-02/receipts/n101/control.json exists.
