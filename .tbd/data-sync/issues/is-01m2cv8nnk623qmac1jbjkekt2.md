---
type: is
id: is-01m2cv8nnk623qmac1jbjkekt2
title: "PR #157 review DOC-01: a failed historical gate is recorded as passed"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:47.859Z
updated_at: 2026-09-13T08:17:13.153Z
closed_at: 2026-09-13T08:17:13.153Z
close_reason: "Fixed: session-127 line 160-162 verdict corrected to failed, observations retained. git show 8eea95b3 confirms the review: its own message says 'Its only failing step was the absence of this declaration', plus a separate clean --records run at 85.77s -- a records-tier pass, not a passing rerun of the fast tier. CI has NO check runs at 6cb9eebd at all, so the commit's 'ALL CHECKS PASSED' banner could not be carried forward as a verdict. Complication the finding did not mention: check_session_gate.py:331 refuses a terminal session whose only declaration does not certify, and certification_pending is allowed only when stopped, so flipping the verdict alone would have made the record machine-invalid. Resolved by declaring the run that actually passed -- hosted run 34719110436 at 8eea95b3 with packing-required, validate, suite, geometry and sweeps all success, which packing-validation.yml:137-139 states are a partition of --fast. Corpus precedent for a failed/passed pair in one record: session-106:237-238, session-105:308-310. A dated correction records the withdrawal and that 'additions over that commit are records only' is no longer true (99afa2d3, 8ebb9876, e6b954cb). check_session_gate now exits 0 over 39 certified terminal sessions."
resolution: null
duplicate_of: null
---
packing/campaign/agent-sessions/session-127-weighted-five-site-atom-admission.md:160 declares 'full gate: fast at 6cb9eebd: passed' while the same declaration says one step failed. Commit 8eea95b3 confirms that failure and a later records-tier pass, not a passing rerun of the fast gate. Fix: correct the machine-consumed historical verdict to failed, preserve its observations, and record the later successful validation separately against its actual source and scope.
