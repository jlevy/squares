---
type: is
id: is-01m2evbgakwhyytm7h5m8y0mst
title: Investigate simultaneous SIGTERM of concurrent local validation gates
kind: bug
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - validation
dependencies: []
parent_id: is-01m2eddtqbpv11d9g5yk0s8cv0
created_at: 2026-09-14T02:18:49.554Z
updated_at: 2026-09-14T19:20:02.372Z
---
At 2026-09-14 about 02:18 UTC, H162 full gate (clean f58 head, running exhaustive_exact) and X032 unsandboxed pre-push gate (clean 646 head, jobs8, reachable tests) both exited 143 simultaneously. Redirected logs remained empty because validators had not flushed; there is no verdict for either run. Cause is unknown: do not infer a research or test failure or assume a specific process-group bug. Reproduce or inspect process/session supervision, then use isolated one-gate-at-a-time reruns; record exact receipts and remediation if a genuine harness defect is found.

## Notes

2026-09-14 PR167 follow-up: an exact-head clean full gate was not SIGTERM'd, but saturated its 3600s ceiling while other host validation workloads were active. Exhaustive exact completed green; unrelated atlas/screen/negative-control/fast/slow/dilation lanes timed out or flaked. Controlled reruns cleared all functional failures; only the fast-suite 12s timing guard remained host-load-sensitive on different passing tests. Fresh hosted required CI was fully green.
