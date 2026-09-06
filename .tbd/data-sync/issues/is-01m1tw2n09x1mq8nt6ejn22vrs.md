---
type: is
id: is-01m1tw2n09x1mq8nt6ejn22vrs
title: Manage the fractional lane from T+2 to T+4
kind: task
status: in_progress
priority: 0
version: 7
delegate: /root/dilation_bound_promotion
labels:
  - fractional
  - research-slice
dependencies:
  - type: blocks
    target: is-01m1tw2pm3r1ppks7e434xxmwn
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T08:06:39.364Z
updated_at: 2026-09-06T11:48:51.402Z
---
Run the exact unused BC-232 leg 02 for its frozen 105-minute wall budget, supervise in slices no longer than 30 active minutes, preserve the four outputs and cumulative endpoints, and submit think-jeyp at T+4. Do not spend the final 30-minute leg.

## Notes

Released by ff9cfe30 against authorized pre-launch head da00905e. Original BC-232 leg 02 scientific process launched at 2026-09-06T11:36:42Z but died before an iteration; its empty original log is retained and the stem is terminal. Bounded recovery authorization and first gate receipt were pushed at 9a93b2ea. Fractional manager GO 2026-09-06T11:46:52Z. Recovery launched once at 2026-09-06T11:47:39Z in coordinator session 36339, uv PID 72209, Python PID 72291, with unchanged scientific inputs, fresh recovery-01 stem, 101-minute cap, 27,277 sites/3,495 orbits/13,000 rows, and cooperative stop. Shared active clock resumes from minute 121:44 at 11:47:39Z. Leg 03 remains forbidden before BC-220.
