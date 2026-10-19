---
type: is
id: is-01m5a64brz6pm3wwgg00fenn5a
title: Resolve PR665 composite slow-call timeout after empty-roster fixture correction
kind: task
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m5a4zqkgk1vqa1q1n1ncbdec
child_order_hints:
  - is-01m5a77w7n1728q66fvwxbkpxf
  - is-01m5a7yneh0jt7ha8jd5gevy9k
created_at: 2026-10-19T13:38:03.166Z
updated_at: 2026-10-19T14:09:53.616Z
---
Unresolved separate timing issue from run39256144591 at tested d4f629b0f52508513beed9a79a508396e14053cc tree d478e0c89ca1e7048d4bf9f857fab931d6da9c64 equal frozen3f20a458. Composite node tests/test_known_best_atlas.py::test_known_best_composite_contains_every_case_and_square on gw1 started13:05:46.152963Z, setup passed13:05:46.153559Z; no call/finish through command end13:29:13.564064Z, lower bound1407.410s. Successful calls at same worker/order20:933.047s in39244113905 and1025.915s in39239208628. Test body and atlas builder unchanged, but37 adopted witnesses/source routes changed and adopted build_witness re-runs exact_verify; no per-case or in-call telemetry identifies the cause. Do not call this host variance or a hang without evidence. Root next action is narrow test-fixture correction, fresh review, hosted full rerun at changed head; ordinary1800-second cap stays, no unchanged-head rerun, timeout increase, skip or heavy local work under W44 hold. Inspect hosted corrected-head timing; if still incomplete, obtain bounded per-case/stack telemetry through a reviewable diagnostic change. Keep strict production empty-roster rejection.
