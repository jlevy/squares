---
type: is
id: is-01m4yby40b4wk2yevnnphcrkmp
title: Rebalance the type floor in broad local push checks
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
created_at: 2026-10-14T23:28:36.865Z
updated_at: 2026-10-14T23:28:36.865Z
---
Observed final prepush at7b802c723: after66of68checks completed by60s, the type floor remained active through180s; a process snapshot showed one BasedPyright Node process at124.2%CPU and about3.8GiB RSS. Source _type_floor sizes threads from cpus-minus-outer-jobs+1, so implicit10outer slots reserve onlyone type thread even after sibling floor work drains. The quick-test exclusive phase started around184s. Investigate a bounded allocation/scheduling fix using existing machinery, retain complete zero-finding coverage and host memory bounds, measure actual inclusive floor/push cost, and avoid a new framework or changing CI obligations. Standalone hosted typecheck already uses its own allocation; this observation is a local scheduling issue, not proof of a hosted regression. Follow stabilization.
