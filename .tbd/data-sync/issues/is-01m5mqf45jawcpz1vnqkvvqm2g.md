---
type: is
id: is-01m5mqf45jawcpz1vnqkvvqm2g
title: "PR #754 (merge): owner answers in the walks (restatements, withdrawn files, Göbel, D6)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: c-sync-754-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5ndg7em7x0s0p5wehyfd90e
hold: null
hold_until: null
created_at: 2026-10-23T15:53:25.937Z
updated_at: 2026-10-24T01:05:35.981Z
started_at: 2026-10-23T15:53:27.712Z
---

## Notes

2026-10-23 c-rev-754-1023: review A (senior engineering review, round 1) of PR #754, posted as a PR comment.

- Review: https://github.com/jlevy/squares/pull/754#issuecomment-6369572454
- Marker: `<!-- tbd:review v=1 id=A kind=senior pr=754 round=1 head=41c43051c6f799374a32c105945a9afd2ef2df18 base=c1115c0956104e40571d26de439c91917911d554 -->`
- Verdict: approve once A1 is settled. Nothing in the record is wrong:
  - only 369 and 376 lose their current row, and only nine rows change;
  - Göbel's sides are exact through 1073;
  - the nine older ledgers are byte-identical;
  - think-oqjd, think-zkxy and think-kzme stay undecided.
- Findings:
  - A1 (Medium): D6 is written as "deleting squares from a published certificate at a larger count". The recorded words are "a square … at the next count". 751 (3 squares from 754), 752 (2 from 754) and 927 (2 from 929) are settled outside those words. "No row of its own" comes from the recommendation, not from the recorded "YES". Nothing rests on the three bounds. The coordinator should confirm the owner's words, or the branch should narrow the text.
  - A2 (Medium): the rulings are opt-in per walk, and the default baseline beyond 324 is still the grid. Every reader of current rows, the next ledger and the importer included, now sees 369 and 376 at 20. No check requires the rulings in a new ledger.
  - A3 (Low): the restatement rule is quoted as the owner's words, but the words are the lane's.
  - A4 (Low): constructions are never restated, which no answer set. `goebel_form` returns None at 1074 to 1100 without a word.
  - A5 (Low): wrong text at 798 and 855, where the 4e4c8ce side is a deletion bound with no row. think-kzme may also need 798 and 855. "by his answer" in source-coverage.yaml:8756 should name the owner.
  - A6 (Low): #613's ask is marked done, but no defect is recorded and the baseline exists only per walk.
  - Suggestions A7 to A9.
- Blocker/High: none.
- Dedicated reviews: correctness applies by the area list, since the branch changes a persisted register format and a rule with exact numerics. Security and performance do not apply.
- Tests at 41c43051c:
  - pytest -n 2 on seven files: 349 passed;
  - render --check and check on all 12 walks: OK;
  - beyond_horizon_replay check: OK;
  - check_source_coverage: reconciled;
  - ruff: clean;
  - reviewer scripts: verdict and register diffs, an exact Göbel recheck, and the reruns.
