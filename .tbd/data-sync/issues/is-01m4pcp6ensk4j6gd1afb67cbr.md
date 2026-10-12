---
type: is
id: is-01m4pcp6ensk4j6gd1afb67cbr
title: "Owner decisions from the regularization pilots: decision-table amendments (rows 4, 5, 7), variant, and the record changes before the full run"
kind: task
status: in_progress
priority: 1
version: 7
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4mdbq6bhkv71fxeeckawsbt
  - type: blocks
    target: is-01m4pcp9t15wsdbwb9kdhw58eq
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T21:07:50.357Z
updated_at: 2026-10-12T11:32:21.634Z
---
From docs/project/research/research-2026-10-11-regularization-state-and-approach.md, Recommendations (pilots of 2026-10-11, gallery https://claude.ai/artifact/GGkxS3NBJzodZcJzaUb1qX). For the owner: (1) row 4: admit a view whose exact side equals the verified upper bound (relation 'bound'; n = 206's certificate side equals its T-098 bound exactly); (2) row 7: per-square regressions with no total falling go to review, not refusal (n = 295); (3) row 5: a view within 1e-9 of the witness with no turn is unchanged (n = 11 differs by 1e-33); (4) variant: conservative only (fewest at 129 loses 26 four-side squares and one-to-one identity); (5) adopt the register's lower exact certificates (T-146 and in-flight imports) as atlas witnesses first; (6) batch-register exact packings at printed sides below 14-decimal bounds (37, 87, 101, 200, 260 in the pilots; 17 waits on think-x4v4). Then amend docs/project/policies/regularization-policy.md and devtools.regularize_evand.classify.

## Notes

2026-10-11, owner (this session): (a) "I don't like the way you've marked things as refused when there's basically no candidate anyway" -> decided and applied: the policy (#497, 54aafcaa2) reports decisions as no view / no change / refused / held / review / alternate / admitted; refused only for a view that changes the drawing and fails an obligation; no change wherever nothing visible changes, whatever row matched (row 3 candidates still listed in the receipt). Driver (#511, 9d4f34aaf) and gallery follow; pilots reclassified: 4 admitted, 8 held, 1 refused (295), 9 no change, 3 no view. (b) Owner asked why n = 206 was refused when it looks much cleaner: answered that row 4 holds a view whose side is not the witness's, although 206's side equals its verified bound exactly and it passes every other check (no regression, one to one, max move 0.37). Amendment (1) here (relation 'bound') is what would admit it; still awaiting the owner's yes.

2026-10-12, owner answers (this session), quoted: "q1 yes / q2 send to review yes, for trickier cases we can go to review in general / q3 yes / q4 as we do currently / q5 as recommended / q6 yes regularize and correct always". Recorded in the policy, section 9 Owner Decisions (#497, 016b38ecf): (1) a view at exactly the verified upper bound is a drawing frame, relation `bound`, decided by rows 5-10; (2) rows the rules cannot settle go to review: row 6 (no one-to-one pairing, unnamed turn) and row 7 where per-square counts fall but no house or stage total does; row 7 refuses only a falling total; (3) `conservative` only; (4) no change as now: no file written; (5) adopt T-146's certificates as witnesses after #403, RG-7 custody and the in-flight imports (think-cb34); (6) register every exact view below the bound, in batches (think-omqv). Driver applied on #511 (11d4fe3fc): side_relation, totals_fall, reclassify derives the relation; pilots reclassified: 206 held -> admitted, 295 refused -> review, nothing else moves. Closes when #497 and #511 merge.

2026-10-12: the overnight decisions made under the owner's standing instruction are recorded for confirmation in #497's policy section 10 (rotation tolerance, retry ladder, third generator, choice rule, contract and checks, regularized_drawings record, T-151).
