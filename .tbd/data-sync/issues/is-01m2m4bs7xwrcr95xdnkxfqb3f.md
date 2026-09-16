---
type: is
id: is-01m2m4bs7xwrcr95xdnkxfqb3f
title: "PR #178 review R2: the API-exposure assertion is unreachable through the tool"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4brc46s3a2pqbaqthnyz7
created_at: 2026-09-16T03:32:28.028Z
updated_at: 2026-09-16T03:32:28.028Z
---
packages/workbench/tools/workbench_tools/check_candidate.py:746 and :1629. main() reaches browser_checks only when the static half is clean; ten stale static failures under think-tn0j. Recorded so the change closing tn0j re-runs the tool end to end. (PR #178, review 5218208269)
