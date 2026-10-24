---
type: is
id: is-01m5qf8dnze8hms5gg949fgfep
title: "wait_for_run_artifact: retry a transient 5xx instead of failing the Pages job"
kind: bug
status: open
priority: 2
version: 1
labels:
  - infrastructure
dependencies: []
created_at: 2026-10-24T17:27:40.991Z
updated_at: 2026-10-24T17:27:40.991Z
---
On 24 October 2026, PR #793's Certificate page run 40113441337 failed nine jobs over two attempts with 'artifact join failed: gh: Server Error (HTTP 502)': packing/devtools/wait_for_run_artifact.py retries only explicit quota responses (RateLimitError), so a single transient 5xx from the GitHub API fails the job before anything of the branch runs, and pages-required then fails. Other branches' runs at the same hour succeeded. Retry a 5xx (and a gh timeout) with backoff within the existing deadline, keeping a 4xx other than quota a failure, with tests on the injected api callable. Found by c-w7-1024 while addressing #793's round 1.
