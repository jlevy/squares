---
type: is
id: is-01m1t7f9tt6fm2vmbvbsrjm19p
title: Repair PR 87 measured slow-test classification
kind: bug
status: closed
priority: 0
version: 2
labels: []
dependencies: []
parent_id: is-01m1t5yjssbd51cnnw2zwkqah6
created_at: 2026-09-06T02:06:33.805Z
updated_at: 2026-09-06T02:10:43.524Z
closed_at: 2026-09-06T02:10:43.522Z
close_reason: "Implemented in fd7c9d94: marked the measured 8.15s negative-control source-copy test slow and registered its hosted ownership; focused tests passed. Push-tier reached all checks except unrelated host cairo collection failure."
resolution: null
duplicate_of: null
---
On the exact PR 87 head, mark the measured 8.15-second negative-control source-copy test slow, register its hosted measurement in the slow-marker ownership test, run focused and fast validation, then update the PR 87 branch only if its remote head has not advanced.
