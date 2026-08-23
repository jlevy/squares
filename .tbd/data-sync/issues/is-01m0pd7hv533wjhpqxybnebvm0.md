---
type: is
id: is-01m0pd7hv533wjhpqxybnebvm0
title: Polished tier has a declared noise floor of ~1e-11; nothing may be promoted from it
kind: task
status: open
priority: 2
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T04:14:31.781Z
updated_at: 2026-08-23T04:14:31.781Z
---
The LP post-check accepts constraint violations up to LP_FEASIBLE_EPS=1e-9 and HiGHS floors primal feasibility at 1e-10, so a polished side can be wrong by ~1e-11. Eight recorded rounds carry small NEGATIVE gaps to the analytic value at exactly that scale. Contained by tier discipline (only exact may claim a record), not eliminated. Keep the floor declared wherever polished numbers are quoted, and route any promotion through sqpack.verify.
