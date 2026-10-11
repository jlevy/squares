---
type: is
id: is-01m4mcrmzpk950zv8caqjrnwnx
title: Bound the deployed-site audit job wall time
kind: bug
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-11T02:30:41.901Z
updated_at: 2026-10-11T02:33:37.045Z
started_at: 2026-10-11T02:31:09.234Z
---
The Pages verify-deployment job has no explicit wall timeout. The first audit of merged 6038 took 13m45s; its retry has exceeded 26 minutes while the inherited GitHub job default permits six hours. Add a conservative 30-minute job timeout covering setup and the complete live audit; preserve all verdicts, browser coverage, and per-request retries. Reuse the existing exact-deployed-revision workflow contract for focused verification. Report recovery options for running the patched checker against the existing deployment without redeploying; no dispatch or other GitHub mutation is authorized in this lane. This is a P2 CI resource and feedback boundary, not evidence of a production site defect.

## Notes

Implemented and source-frozen: .github/workflows/pages.yml adds timeout-minutes: 30 only to verify-deployment. The existing exact-deployed-revision contract asserts the ceiling and retains site URL, commit, dependency and browser coverage assertions. Three focused workflow tests passed in 14.66s; Ruff check, Ruff format check and scoped diff check passed. Receipt: /Users/levy/.codex/visualizations/2026/10/08/01a11dc7-6f9d-7060-be5c-4cff21839702/website-cleanups/audit-timeout-focused.log. No checker retry, verdict, browser or publication behavior changed. New evidence from coordinator: attempt 2 completed with 25 GitHub 503 failures, checker 27m36s and job 28m22s, versus initial audit 13m45s; retain the conservative 30-minute explicit job boundary, not a speed claim. Workflow comment describes the failure boundary without privileging one timing. Existing workflow_dispatch has only PDF diagnostic options and no audit-only route: main dispatch rebuilds/deploys, branch dispatch skips deploy and verification. The patched checker CLI can audit existing deployed 6038 with explicit --site and --commit from the corresponding source checkout; an old-job rerun keeps its old source. Hosted patched-checker recovery without redeploy would require a separately designed audit-only entry point. No dispatch, rerun, commit, staging or GitHub mutation performed. Keep this bead in progress pending independent review, integration and hosted evidence.
