---
type: is
id: is-01m4x4x1kr1ms7wfp39h768m0d
title: Workbench check_frontend 'stage separator reload' reads the stage before the API is ready after reload
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-14T12:06:27.192Z
updated_at: 2026-10-14T12:06:27.192Z
---
Hosted CI on PR #597 at 8db1905d5 (run 38560177202, job 115839014427) failed 'workbench browser behavior in Chromium' in workbench_tools.check_frontend: the 'stage separator reload' probe's after-load phase read apiReady false, stageHeight 0 and valueMax 0, while the before-reload and after-ready phases read stageHeight 746 and valueMax 816 as expected. #597 changes only packing/devtools/check_requests.py, its tests and result-import.md, so the failure is a race in the probe (reading layout at load before the workbench API is ready), not that PR's. It was not seen in the last 30 failing Packing validation runs. Fix: have the probe wait for apiReady before asserting the restored separator, and add a negative control.
