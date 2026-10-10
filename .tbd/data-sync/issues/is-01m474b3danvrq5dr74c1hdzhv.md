---
type: is
id: is-01m474b3danvrq5dr74c1hdzhv
title: "Answer #375 (evand exact optima of 48 records): acknowledgement, verdict reply from the lane, then the reply from main and the close"
kind: task
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
created_at: 2026-10-05T22:53:21.706Z
updated_at: 2026-10-10T20:43:34.655Z
---
Replies owed on jlevy/squares#375. Posted 2026-10-05: the stage-1 acknowledgement (https://github.com/jlevy/squares/issues/375#issuecomment-6004562871). Lane F (think-t6ok) posts a verdict reply once its records are committed, stating only what the branch's records say and that they are not merged. After the merge: the reply from main with the merged T-id and rungs (check_requests --draft 375), recorded in packing/campaign/result-requests.yaml, and the close when nothing the author asked for is queued.

## Notes

2026-10-10, records lane R4 of the 2026-10-10 intake pass (think-fvz4): Evan Daniel's comment https://github.com/jlevy/squares/issues/375#issuecomment-6101883016 (20:31:42Z) withdraws S' at n = 17 as a separate submission and asks that the exact form from #419, at evand/square-packing 8c47162cec22f02791abfbf7dedb8094de91189a (search/exact/minpoly/data/n-17.minpoly.json.gz), be the n = 17 object, with its bookkeeping on #419 and #405; upper bound only, no optimality, no improvement on the register's 4.67553009360455. On the intake branch (not yet on main), in packing/campaign/result-requests.yaml, #375's n17-certificate is not_registered and no longer queued (withdrawn by the author), a new result n17-exact-form-2026-10-10 is queued under think-x4v4 (held with the n = 17 intake, nothing at 8c47162 retained or replayed), read_through is 2026-10-10T20:31:42Z, and #419 and #405 carry a note of the pointer.

The stage 7 draft for #375 in think-mtwe's notes must drop or reword its n = 17 part. The line that needs to change: "**What remains.** The n = 17 certificate is still held for the n = 17 work, under `think-00e3`, as the [8 October follow-up](https://github.com/jlevy/squares/issues/375#issuecomment-6065914616) says. A geometry replay of T-129 is optional and would not change any selected bound. This issue stays open while the n = 17 certificate is held, and a reply follows each change in the record." Its header line, "Ledger: not closeable (n17 hold).", needs the same change. The draft should acknowledge the withdrawal and say the exact form stays held with the n = 17 intake, not imported or replayed here; `check_requests --report` now lists "n17-exact-form-2026-10-10: an acknowledgement; not yet imported" among the replies due on #375.
