---
type: is
id: is-01m4jr7mpcvv3wqm8280bt2x19
title: Keep website publication and frontend validation within their contracts
kind: bug
status: in_progress
priority: 1
version: 11
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T11:12:38.602Z
updated_at: 2026-10-10T14:42:03.319Z
started_at: 2026-10-10T11:13:19.000Z
---
Resolve PR 462 publication and frontend findings without relaxing existing contracts. Preserve script inventory refusal, native MathML readiness, stable Atlas geometry, 300 ms startup assertions, all browser checks and current effective PR hard ceiling. Retained fixes cover non-inherited Headroom clearance, concurrent browser-lane startup, canonical render setup and Atlas host reuse. Final hosted gates must pass before closure; full pre-merge checkpoint remains think-xio5.

## Notes

Final cf6cfa08d434a1d69ebf1fe69bf8352be3cd2098 is pushed to draft PR 462. Local frontend all four steps PASS in157.12s,405site+4HTTP+56floor, Astra reviewed. Hosted frontend38059936824/job114235952011:405functional PASS6skip390.21s,3HTTP startup FAIL318/327/302ms (unchanged300),1HTTP PASS; total415.57s exceeds effectivePR330s hard ceiling. Other checks passed. Prior72 frontend333.01 and413.41 were budget-only failures; scheduler832 passed296.39. No budgets changed. Astra investigating forced layout attributed to atlas-grid.js317.1ms; header collecting exact receipts and homepage evaluating workload. Implementation beads remain open pending finalgreen; full checkpoint think-xio5 remains separate.
