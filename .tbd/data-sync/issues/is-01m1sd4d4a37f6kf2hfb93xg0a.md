---
type: is
id: is-01m1sd4d4a37f6kf2hfb93xg0a
title: "BC-215: stop re-running expensive gate work whose inputs have not changed"
kind: task
status: open
priority: 0
version: 5
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
created_at: 2026-09-05T18:26:13.770Z
updated_at: 2026-09-06T21:15:42.806Z
---

## Notes

W5 Phase 3 includes explained exhaustive-family planning before any skip, a complete code/data/fixture and test-node census, trusted reusable receipts, end-of-run source checks, and complete fresh-plus-reused coverage. See docs/project/reviews/review-2026-09-06-change-scoped-exhaustive-validation.md for the PR94–96 timing evidence, focused contract obligations, invalidation fixtures and project/upstream documentation matrix. The landed first slice repairs repository-relative configuration and limit-tool invalidation; automatic family selection and reuse are not enabled.

Retain the concrete n=40 duplicate: exhaustive test_the_record_round_trips and the named assessor --check both recompute assess(). Preserve both until the coverage union plus cheap CLI equality, drift, missing-input and read-only fixtures justify eliminating one execution. Bounded pytest scheduling also needs a total-work comparison, not only lower elapsed time. Final PR98 exhaustive timing is 21m14s job / 1251.16s pytest for the same 55 identities; the dominant n=40 case takes 192.64s. Prior 26m56s and 20m56s observations are source-bound and host variation prevents a causal worker-speedup claim.

New measured queue case: main validation 34057826143 for merged 8743cb0d was created 2026-09-06T20:23:13Z; its first jobs started 20:36:10Z, 12m57s later. Workflow-level concurrency serializes push/refs/heads/main with cancellation disabled. Predecessor 34057077924 on PR100's 6a064e3b had already failed the old OR-16 control; its exhaustive job finished naturally at 20:36:08 before the new run began. No cancellation was performed. The fresh main tree combines PR100 mathematical changes with PR98, so the successful PR98 checkpoint on older base c14451f5 does not certify it. Evaluate a policy that preserves required per-tree/final coverage while letting immediate feedback proceed independently of serialized deep audits, and handles known failing superseded runs without claiming cancelled evidence as a pass.

Keep queue time, setup, execution, critical-path latency and total runner work separate. This is already required by the W5 spec and prepared upstream testing-and-CI-performance guide. The parallel review's reported reachable-push observations (642s/685s on its actual pre-integration sources) are another feedback-cost case to reproduce before changing scope. Complete the documentation matrix and workflow/selector negative controls together with any rollout.

Final main 34057826143 passed on 8743cb0d: validate 20m23s, exhaustive 22m48s and macOS 1m47s. All 66 default checkpoint steps and case/control evidence were verified. The workflow took 35m46s from creation to completion, including the measured 12m57s pre-job delay. Within the main gate, controls and slow tests started at +15.110s, quick tests at +766.039s, and n=40 at +987.010s, finishing last at +1205.601s. These timings expose a bounded scheduling candidate in addition to queue admission; they do not isolate why those delays occur. Measure changes against complete coverage and total-work requirements. Main artifact links and detailed source-specific results are in PR98; audits are /tmp/pr98-main-validate-artifact-audit.json and /tmp/pr98-main-exhaustive-macos-artifact-audit.json.
