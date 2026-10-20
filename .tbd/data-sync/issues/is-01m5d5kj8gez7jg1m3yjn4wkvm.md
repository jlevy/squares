---
type: is
id: is-01m5d5kj8gez7jg1m3yjn4wkvm
title: "Import Evan Daniel: s(308) <= 17.997149121271 (#689)"
kind: task
status: open
priority: 1
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m5c0fwsxga70rszkjy1zbp2f
created_at: 2026-10-20T17:26:36.048Z
updated_at: 2026-10-20T18:49:14.920Z
---
Stage 1 to 3 import of jlevy/squares#689 (Evan Daniel, filed 2026-10-19T22:44:19Z), lane c-lane-evand-2 under think-eizi.

## Claim map
- Source: evand/square-packing at bc0708fc75c84cffd241e1901c71fbdd120542a3 (committed 2026-10-19T22:41:02Z), search/packer/candidates/s308_d308.cert, SHA-256 6a9c03318ee5a703313b5dcab02febbe6b520133ffea0a21ea2ecf0741c42a91, and its same-side regularized view s308_d308_regularized.cert, SHA-256 5e5af5a4833656743ae84c66dcaa6b2cd3d65d9e8308ff1323240f33520c2f03. Both digests match the issue. Head 1d2bb82 leaves the files unchanged.
- One claim: s(308) <= 3599429824254181747030632150463/(2 x 10^29) = 17.997149121270908735153160752315, printed 17.997149121271 (rounded up at 12 places). Register action: a new entry (the record holds no such value).
- Standing at 308: house T-174 (PingYou Ltd's refinement of Daniel's T-141 packing on Fang's two-wedge construction), exact side about 17.99826987952625588; T-141 and T-135 retained as history. No open report states a smaller side at 308 (open issues through #698 read on 2026-10-20).
- Source statements not decided here: KKT point, strict local minimum modulo 47 flat motions, no corner-corner MILP descent, 5 rattlers, 102 tilted squares; not a refinement of #489, not descended from #484 or #489; lineage from Chaoweeraprasit's #481 s(307) packing by one-square insertion and explorer moves.
- Ask: credit Nate Chaoweeraprasit's (itsnaka's) s(307) packing (#481) as the ultimate start.
- Credit note: think-a95t (the #673 consequences at 308, Kevin Fang's structured credit) concerns the present house; this packing names neither Fang nor #489 in its lineage.

## Validation plan (priced)
- Exact certification on the two maintained routes (sqpack.verify and devtools.check_rational_witness_independent) with the duplicate-square and outside-container controls, via devtools.upper_bound_reports certify: about 2 to 4 CPU-minutes, run in this lane.
- Stage 4 mathematical review (tbd-strong-max), run by the coordinator after the records PR opens. Then V3/C3 from the replay evidence and the review, adoption at 308 and regularization of the new house (both strong generators, about 5 to 25 CPU-minutes) in the stage 4 pull request.

## Notes

2026-10-20 (c-lane-evand-2): stages 1 to 3 done on claude/intake-2026-10-20-evand-308-154, draft PR https://github.com/jlevy/squares/pull/699 (head 34d72a95a; data commits 277bcd50a and the suite-a fix 938e5f573; hosted Packing validation run 39476391860 green). Packet packing/resources/web/evand-n308-2026-10-19 at bc0708f; digests match the issue. Both maintained exact routes accept the positive and refuse both controls (receipt retained). Registered as T-221, V0/C0, 1.12075825534714e-3 below T-174 at 308. n-308.md carries the pending-adoption paragraph (308 is HAND_MARKED). Credit ask queued on this bead until adoption. Reply draft: scratchpad/replies-new/689.md (post after merge; asks the author about the missing search/packer/dgen.py).
Next: stage 4 mathematical review (coordinator, with Fable), then V3/C3, adoption at 308 and regularization of the new house in the stage 4 PR. think-a95t (Fang's credit at 308) concerns the present house only.
