---
type: is
id: is-01m5ndg7em7x0s0p5wehyfd90e
title: "PR #754 follow-up review B"
kind: task
status: closed
priority: 2
version: 5
delegate: c-rev-754b-1023
labels: []
dependencies: []
parent_id: is-01m5mqf45jawcpz1vnqkvvqm2g
child_order_hints:
  - is-01m5nfdtfyjpee1131zzb9g0w9
hold: null
hold_until: null
created_at: 2026-10-23T22:18:30.739Z
updated_at: 2026-10-24T01:26:51.013Z
started_at: 2026-10-23T22:18:44.276Z
closed_at: 2026-10-24T01:26:51.012Z
close_reason: "Fixed in #754 merged at 0bbb0a2c4 (head d4f73323b; review A dispositions 6372591445, review B dispositions 6377099959; CI green: 40048767717, 40048767835, 40048765054)"
resolution: null
duplicate_of: null
---

## Notes

2026-10-23 c-rev-754b-1023: follow-up review B (round 2) of PR #754 published at head 2cc420a4f: https://github.com/jlevy/squares/pull/754#issuecomment-6376229374

Verdict: approve once B1 is fixed or deferred. Nothing in the record is wrong. No Blocker or High findings.
- B1 (Medium): A2's restatement half has no disposition. The restatement answer is still opt-in per ledger, and no check covers a ledger read from 23 October that lists neither ruling. Exposure: the 66 sub-1e-12 counts above 1024 that think-llit will walk.
- B2 (Low): #732's `check --tree` is 311 of 390 lines of Göbel-only noise. The frozen-before exception is missing from the runbook, and `tree_drift` has no test.
- B3 (Low): the refusal above 1073 refuses the whole import, receipt or gather; tell think-llit.
- B4 (suggestion): think-q920's companion (think-v022) is stale, and think-v022 is still open.

Checked:
- A1, A3 to A6 and A9 are fixed; A7 and A8 are justified deferrals.
- A2's rules 1 to 4 hold, with GOEBEL_FROM = 2026-10-23. Its three negative controls fail against c3f5dc604^.
- The 1073 reach matches a build of the families to 5000.
- No ledger.json, starts.yaml, claims.json or register row changed since review A.
- The #732 walk with a Göbel member in every start gives a byte-identical ledger.json, and nothing in CI or make intake reads the drift. Keep the date.

Tests: 747 passed. Replay check, ledger check and render --check all OK on the 12 walks. Ruff is clean.
