---
type: is
id: is-01m2cv8nnk623qmac1jbjkekt2
title: "PR #157 review DOC-01: a failed historical gate is recorded as passed"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:47.859Z
updated_at: 2026-09-13T07:38:47.859Z
---
packing/campaign/agent-sessions/session-127-weighted-five-site-atom-admission.md:160 declares 'full gate: fast at 6cb9eebd: passed' while the same declaration says one step failed. Commit 8eea95b3 confirms that failure and a later records-tier pass, not a passing rerun of the fast gate. Fix: correct the machine-consumed historical verdict to failed, preserve its observations, and record the later successful validation separately against its actual source and scope.
