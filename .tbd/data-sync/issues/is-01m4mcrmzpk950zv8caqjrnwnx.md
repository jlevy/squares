---
type: is
id: is-01m4mcrmzpk950zv8caqjrnwnx
title: Bound the deployed-site audit job wall time
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-11T02:30:41.901Z
updated_at: 2026-10-11T02:31:09.238Z
started_at: 2026-10-11T02:31:09.234Z
---
The Pages verify-deployment job has no explicit wall timeout. The first audit of merged 6038 took 13m45s; its retry has exceeded 26 minutes while the inherited GitHub job default permits six hours. Add a conservative 30-minute job timeout covering setup and the complete live audit; preserve all verdicts, browser coverage, and per-request retries. Reuse the existing exact-deployed-revision workflow contract for focused verification. Report recovery options for running the patched checker against the existing deployment without redeploying; no dispatch or other GitHub mutation is authorized in this lane. This is a P2 CI resource and feedback boundary, not evidence of a production site defect.
