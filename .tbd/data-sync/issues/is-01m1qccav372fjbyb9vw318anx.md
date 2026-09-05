---
type: is
id: is-01m1qccav372fjbyb9vw318anx
title: "F7 and F29: interval-route masses scaled and summed in Python integers, refused at 2^62; no overflow warnings from a restricted search"
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:36.131Z
updated_at: 2026-09-05T00:24:41.738Z
closed_at: 2026-09-05T00:24:41.738Z
close_reason: "Ported as commit 'interval: masses scaled and summed in Python integers, refused at 2^62' on claude/port-pr80-findings; box budget and atom cap split to think-05dc."
resolution: null
duplicate_of: null
---
Same discipline the integer sweep applies at 2^60. Port with their positive-weight 2^63 + 1 regression.
