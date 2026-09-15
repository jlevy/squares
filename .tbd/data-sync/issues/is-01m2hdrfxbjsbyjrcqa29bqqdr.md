---
type: is
id: is-01m2hdrfxbjsbyjrcqa29bqqdr
title: "Campaign records: resolve method.record everywhere, then check it; two small record-vs-data mismatches"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-15T02:18:58.346Z
updated_at: 2026-09-15T02:18:58.346Z
---
Found while addressing PR #125 review D26 (think-zhaq, fixed in a7c18798).

1. A check that `method.record` resolves was not added: it would fail on 18 existing experiment records (exp-040..057, exp-118, exp-129, exp-134, exp-158, exp-160), and on #155 exp-207 and exp-209 hold prose there rather than a path. packing/src/sqpack/campaign/runner.py (about :1375) writes record paths relative to packing/, against AGENTS.md's repository-relative rule. Repair those records and the runner, then add the resolving check to `packing-ledger check`.
2. SYNOPSIS.md gives H-202 "39.2m wall" where the ledger says 39.1m (left alone: adjacent to lane B's hunk on #155).
3. exp-205 says one seed left the grid at n = 50 in the both-factors arm; the committed data shows two (7.970317 and 7.929171).
