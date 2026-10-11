---
type: is
id: is-01m3syx8zc50xfnq7dxp05xg4p
title: "epistemics.md: say whether recorded geometric executions satisfy V4's replay predicate"
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-30T20:08:18.155Z
updated_at: 2026-10-06T08:28:50.781Z
closed_at: 2026-10-06T08:28:50.780Z
close_reason: "Done on main: epistemics.md (99b043acd) now says a recorded execution performed here, receipt retained and hash-bound, is a replay at C3/C4, while C5 needs a fresh end-to-end replay. The ladders were redefined and T-060 re-rated to V3/C3."
resolution: null
duplicate_of: null
---
T-060 is V4 on evidence E-n011-global-optimality-independent with replay_status passed, but its certificate records geometry_rerun: false and the inventory does not prove the executions' occurrence; a fresh end-to-end replay cannot run from the repository (about 2.3 GB of LFS inputs outside Git; child checkers pin parent receipts; think-e2ot). epistemics.md does not say whether recorded executions count as replay command plus passing replay status. Owner decision; then either state it in epistemics.md and check_results, or make think-e2ot the path that earns V4. Found by the 2026-09-30 epistemics audit.
