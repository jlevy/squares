---
type: is
id: is-01m1tw2n09x1mq8nt6ejn22vrs
title: Manage the fractional lane from T+2 to T+4
kind: task
status: in_progress
priority: 0
version: 6
delegate: /root/dilation_bound_promotion
labels:
  - fractional
  - research-slice
dependencies:
  - type: blocks
    target: is-01m1tw2pm3r1ppks7e434xxmwn
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T08:06:39.364Z
updated_at: 2026-09-06T11:38:31.514Z
---
Run the exact unused BC-232 leg 02 for its frozen 105-minute wall budget, supervise in slices no longer than 30 active minutes, preserve the four outputs and cumulative endpoints, and submit think-jeyp at T+4. Do not spend the final 30-minute leg.

## Notes

Released by ff9cfe30 against authorized pre-launch head da00905e. Manager restart 2026-09-06T11:35:26Z; BC-232 leg 02 launched exactly once at 11:36:42Z, session 27576, uv PID 64895, Python 3.14.7 PID 64896, 27,277 sites/3,495 orbits/13,000 rows, cooperative stop enabled. First receipt: results/agenda-025/bc-232-leg-02-microreceipt-001.md. Leg 03 remains forbidden before BC-220.
