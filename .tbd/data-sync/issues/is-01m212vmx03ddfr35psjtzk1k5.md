---
type: is
id: is-01m212vmx03ddfr35psjtzk1k5
title: Prevent startup tooling from selecting a serial full push suite
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T18:00:36.498Z
updated_at: 2026-09-08T23:04:43.516Z
closed_at: 2026-09-08T23:04:43.515Z
close_reason: Integrated the shared parallel worker and change-reachable test policy. Final a10569d1 pre-push used three pytest workers and passed 45 checks with 1028 affected tests in135.15 seconds. Unrelated whole-suite fallback is no longer selected for the new startup and typography tool paths; broad selections preserve their intended coverage.
resolution: null
duplicate_of: null
---
The pre-push check at62e17793 expanded new startup/reporting paths into pytest -q tests -m not exhaustive_exact without parallelism and ran more than36minutes. Preserve coverage, identify missing reachability mapping or correct broad-suite execution, retain the interrupted receipt, and verify the repaired push path. Separate from KPress Python browser availability failure think-liv9.
