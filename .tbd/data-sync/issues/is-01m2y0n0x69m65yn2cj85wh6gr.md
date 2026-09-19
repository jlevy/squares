---
type: is
id: is-01m2y0n0x69m65yn2cj85wh6gr
title: "PR199 review R2: keep threshold LP solver errors unresolved"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:40:00.804Z
updated_at: 2026-09-19T23:40:00.804Z
---
packing/devtools/produce_threshold_certificate.py:209-212 handles status1 but maps status4 and other unsuccessful outcomes to infeasible. Reproduced mocked HiGHS status4 on a feasible one-row matrix; resolve then emits scientific refusal. Only status2 can report solver infeasibility; preserve raw status/message, classify numerical/solver failures unresolved, and cover both initial and subsequent LP paths.
