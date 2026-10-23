---
type: is
id: is-01m5msteea766hp8844fdw7wg7
title: "PR #754 A2: the Göbel answer is opt-in per walk; readers of the record still take the grid beyond 324, so 369 and 376 read at 20 (Medium)"
kind: bug
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m5mstad6tr1k9t825pe62ptr
created_at: 2026-10-23T16:34:34.058Z
updated_at: 2026-10-23T19:03:52.818Z
---
Review A of PR #754 (https://github.com/jlevy/squares/pull/754#issuecomment-6369572454); see the review for file:line references and the suggested fix.

## Notes

2026-10-23 c-answers-1023 (PR https://github.com/jlevy/squares/pull/754 at 7226721f1): escalated to coord-intake-1023, not implemented.

A2 escalation (think-v022, open): Göbel's construction as the standing side beyond 324 in every reader. These readers cannot take it without a design choice.

1. upper_bound_reports._row (packing/devtools/upper_bound_reports.py:1614). It builds `candidates` from the grid, earlier reports and the house. Its claims.json records are frozen and rebuilt by `check` for comparison, in 15 packets with beyond-horizon claims, all read before 23 October. Adding Göbel changes every frozen record. Options:
   (a) date-gate on the declaration's read_on >= 2026-10-23, so older packets keep their reading of the day;
   (b) rewrite the 15 frozen records.
   Recommend (a): it is the walks' rule, since rulings are dated and older ledgers are unchanged.
2. beyond_horizon_replay._standing (packing/devtools/beyond_horizon_replay.py:1860). It reads those frozen records, so it follows 1.
3. intake_ledger.beyond_member and tree_members (packing/devtools/intake_ledger.py:1141, 1278): fresh starts. Göbel is feasible to n = 1073, the retained program's reach, but past 1073 a start must either refuse or fall back to the grid. `recomputed()` must still reproduce the frozen grid members of older ledgers. Recommend: a Göbel member at 325 to 1073 for starts frozen on or after 23 October, and refusal beyond 1073 until think-llit.
4. cases/asymptotic/fang_excess_inventory.read_record (:393). TABLE = range(15, 73) reaches n = 5184 against a Göbel reach of 1073, and adding a construction changes what the research artifact measures: recorded rows, not best known sides. It already lost 369 and 376 through current_beyond_horizon's NOT_CURRENT. This needs a coordinator or owner call: a separate Göbel column, or leave it on recorded rows.

2026-10-23 c-answers-1023: fixed in c3f5dc604, on coord-intake-1023's decisions. PR #754 head 2cc420a4f, CI green. Rules 1 to 3 are dated at intake_ledger.GOEBEL_FROM (2026-10-23): claim_row, standing_sides, and tree_members with construction_member. Rule 4, the Fang inventory, stays on recorded rows and is deferred to think-a75a. No recorded verdict or row changes. Reply: https://github.com/jlevy/squares/pull/754#issuecomment-6372591445
