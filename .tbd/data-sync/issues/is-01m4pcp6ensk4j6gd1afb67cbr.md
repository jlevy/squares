---
type: is
id: is-01m4pcp6ensk4j6gd1afb67cbr
title: "Owner decisions from the regularization pilots: decision-table amendments (rows 4, 5, 7), variant, and the record changes before the full run"
kind: task
status: open
priority: 1
version: 4
labels:
  - regularization
dependencies:
  - type: blocks
    target: is-01m4mdbq6bhkv71fxeeckawsbt
  - type: blocks
    target: is-01m4pcp9t15wsdbwb9kdhw58eq
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T21:07:50.357Z
updated_at: 2026-10-11T21:23:08.934Z
---
From docs/project/research/research-2026-10-11-regularization-state-and-approach.md, Recommendations (pilots of 2026-10-11, gallery https://claude.ai/artifact/GGkxS3NBJzodZcJzaUb1qX). For the owner: (1) row 4: admit a view whose exact side equals the verified upper bound (relation 'bound'; n = 206's certificate side equals its T-098 bound exactly); (2) row 7: per-square regressions with no total falling go to review, not refusal (n = 295); (3) row 5: a view within 1e-9 of the witness with no turn is unchanged (n = 11 differs by 1e-33); (4) variant: conservative only (fewest at 129 loses 26 four-side squares and one-to-one identity); (5) adopt the register's lower exact certificates (T-146 and in-flight imports) as atlas witnesses first; (6) batch-register exact packings at printed sides below 14-decimal bounds (37, 87, 101, 200, 260 in the pilots; 17 waits on think-x4v4). Then amend docs/project/policies/regularization-policy.md and devtools.regularize_evand.classify.

## Notes

2026-10-11, owner (this session): (a) "I don't like the way you've marked things as refused when there's basically no candidate anyway" -> decided and applied: the policy (#497, 54aafcaa2) reports decisions as no view / no change / refused / held / review / alternate / admitted; refused only for a view that changes the drawing and fails an obligation; no change wherever nothing visible changes, whatever row matched (row 3 candidates still listed in the receipt). Driver (#511, 9d4f34aaf) and gallery follow; pilots reclassified: 4 admitted, 8 held, 1 refused (295), 9 no change, 3 no view. (b) Owner asked why n = 206 was refused when it looks much cleaner: answered that row 4 holds a view whose side is not the witness's, although 206's side equals its verified bound exactly and it passes every other check (no regression, one to one, max move 0.37). Amendment (1) here (relation 'bound') is what would admit it; still awaiting the owner's yes.
