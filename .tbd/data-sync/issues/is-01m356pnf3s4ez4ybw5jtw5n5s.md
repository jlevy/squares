---
type: is
id: is-01m356pnf3s4ez4ybw5jtw5n5s
title: Avoid serial pre-push timeouts for broad documentation test selections
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-22T18:40:27.103Z
updated_at: 2026-09-22T18:56:16.121Z
---
PR #220 docs-only change to frontier README and publication runbook selected 61 test files. Default packing-validate --push --since origin/main on 10 CPUs uses 10 outer jobs, leaving pytest one worker; the reachable test step exhausted its 900s subset cap at 901.02s, while all other 50 steps passed (total 951.77s). The true-subset selector misses the automatic broad-fallback worker policy. Evaluate worker allocation for broad subsets after other steps finish; retain the same tests and timeout protection. Recovery run uses --jobs 2. Log /tmp/pr220-push.log on spud10; revision 30e742b6 plus docs fixes e560571f2.

## Notes

Correction: final selector report is 59 of 359 files. Isolated recovery: uv run --frozen --all-extras --group dev python -m devtools.reachable_tests --run --since origin/main -n 4 passed 1681 tests (4 warnings) in 498.38s on e560571f2. A whole --push --jobs 2 retry was interrupted to avoid repeating the already-passed floor. Keep the first run static/record successes and focused recovery together as coverage evidence.
