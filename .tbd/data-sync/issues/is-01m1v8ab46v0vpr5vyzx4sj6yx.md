---
type: is
id: is-01m1v8ab46v0vpr5vyzx4sj6yx
title: Recover BC-232 leg 02 after the manager exec session died
kind: bug
status: closed
priority: 0
version: 4
labels:
  - release-blocker
  - fractional
  - operations
dependencies:
  - type: blocks
    target: is-01m1tw2n09x1mq8nt6ejn22vrs
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T11:40:34.309Z
updated_at: 2026-09-06T11:48:48.618Z
closed_at: 2026-09-06T11:48:48.617Z
close_reason: Audited fresh-stem recovery launched once from pushed head 9a93b2ea; operational release blocker resolved.
resolution: null
duplicate_of: null
---
BC-232 leg 02 launched once at 2026-09-06T11:36:42Z as manager exec session 27576 (uv PID 64895, Python PID 64896), but the process did not survive the manager turn. At coordinator detection 11:39:49Z both PIDs were absent, the original leg-02 log existed at zero bytes, and the state, summary, family, and two bridge outputs were absent. Preserve that stem as a terminal technical failure and pause the shared clock at active minute 121m44s. Before recovery, retain a coordinator authorization packet on a fresh bc-232-leg-02-recovery-01 stem, prove every recovery output absent, cap the replacement at 101 minutes so launch-to-detection plus recovery cannot exceed the original 105-minute process allocation, re-run local focused/edit checks if code or contracts change, commit/push, and obtain a fresh manager acknowledgement. No rerun on the original stem and no leg 03.

## Notes

Recovery authorization committed and pushed at 9a93b2ea0b34701304e311aa080ddd31d3c70e88. Fractional manager returned GO at 2026-09-06T11:46:52Z after exact-head, warm-hash, fresh-path, process, argv, and wall-budget checks. The first sandboxed invocation never initialized uv or the scientific runner and created no output; per the environment escalation rule, the identical command was relaunched outside the restricted sandbox. The scientific recovery began once at 2026-09-06T11:47:39Z in coordinator session 36339 as uv PID 72209 and Python 3.14.7 PID 72291. Initial reconstruction reports 27,277 sites, 3,495 orbits, 13,000 rows, minutes 101, and cooperative stop enabled. No second scientific recovery is authorized.
