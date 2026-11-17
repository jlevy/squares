---
type: is
id: is-01m5krs81bh3wc4ajwe73dc8hr
title: "Stage 4 mathematical review of T-232: wand125's s(31) >= 2391/400 fine-net certificate (no issue)"
kind: task
status: closed
priority: 1
version: 4
delegate: c-review-t232-math
labels:
  - result-import
  - validation
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T06:57:11.722Z
updated_at: 2026-10-24T08:26:43.151Z
started_at: 2026-10-23T06:57:22.296Z
closed_at: 2026-10-24T08:26:43.151Z
close_reason: "T-232's stage 4 review landed on main with #745 (af9c9e850): docs/project/reviews/review-2026-10-23-wand125-n31-fine-net.md and the packet's review/review-2026-10-23/; T-232 V3/C3. M-1 to M-3 and the questions moved to think-nq5g."
resolution: null
duplicate_of: null
---

## Notes

2026-10-23 c-review-t232-math (tbd-strong-max, maximum reasoning; stage 4 mathematical review of T-232 for think-wop1):
- Verdict: accept. The argument from mixed_n31_L59775 to s(31) >= 2391/400 (in fact >) is correct and complete; every premise holds in exact arithmetic. No blocking or major finding. Minor, all in the source's bundle: M-1 README line 15 names check2/control.jsonl.gz (the file is control-197_200.jsonl.gz); M-2 files-sha256.json line 2 gives the sealed README digest 3e302ff4, not the published 6dbab236; M-3 check2/receipt.json line 90 calls the check independent (it is this repository's sqverify_fast with one change). Notes N-1 to N-5; R-1 (the entry's pending-review clauses).
- Own clean-room exact checker (nothing of the source, the crate or devtools read before it ran): PREMISES_HOLD; NET_COVERS; geometry self-test PASS (18,000 cases each); capture VERIFIED at all 122 directions of a stratified seeded sample (96 strata + 28 named, incl. 0, 1, 2, 2071, 2072 and the source's 12 tightest), 2,842,868 nodes vs the source's 46,696,377, least capture found 1.000116 at direction 1841; mutants REFUTED with exact witnesses (99/100 at 5 directions, row 33 removed at 3, 0.999784 at 1841); source-log poses CONSISTENT (31 control witnesses equal the logged exact rationals); bound self-test PASS. About 2,270 CPU-s in all (0.63 CPU-h).
- Rungs: V0/C1 once the review is recorded (external_review informally-verified + reviews item); V3/C3 after the census at all 2,073 directions with CONTROLS_REFUSED, confirmed re-implemented sharing the producer's components, the clean-room sample beside it. Significance S3 confirmed; no News owed (optional draft).
- Deliverables, for the records lane to commit, under /tmp/claude-0/-home-user-squares/f8504540-2b5a-5f78-8968-eb4ffa4c4b64/scratchpad/review-t232/: docs/project/reviews/review-2026-10-23-wand125-n31-fine-net.md; packing/resources/web/wand125-fine-net-n31-2026-10-11/review/review-2026-10-23/ (programs, outputs, README); record-changes.md.
