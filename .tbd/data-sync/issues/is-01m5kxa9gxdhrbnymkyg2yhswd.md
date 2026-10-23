---
type: is
id: is-01m5kxa9gxdhrbnymkyg2yhswd
title: "PR #747 (merge): close settled intake issues at stage 7; awaiting-author questions"
kind: task
status: in_progress
priority: 1
version: 8
delegate: c-addr-747-1023
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T08:16:24.605Z
updated_at: 2026-10-23T18:31:47.318Z
started_at: 2026-10-23T08:16:33.602Z
---

## Notes

2026-10-23 c-addr-747-1023: review A (https://github.com/jlevy/squares/pull/747#issuecomment-6360911091) addressed on claude/intake-2026-10-23-close-issues. Merged origin/main #749 (9c56ecb4c); 712bbbd0a A1 owner hold (held: by/since/note; #557 #565 #570 #574 held citing think-5ip2), A5 closed-on-GitHub step, A9 awaited >14 days listed for a decision, A3 narrowed admission test; cdefdcdba A4 READMEs, A6 bare child env/stdin/cwd, A7 malformed rows reported, A8 sharp-near-wall control, receipts re-run (40 invocations, all controls refused); 1a5fe2b2c A2 three same-implementation evidence entries beside T-197..T-199 (no rung moves), A3 #670 withdrawn, #470 measured (measure/identity.json: 12 of 16 earlier packings refined; Gupta via T-128 at 180, Daniel via T-130 at 270, credit updated) and withdrawn, #672 kept; ef43bf583 re-pin. No deferrals. Per-finding beads were not created: the lane rules allow new beads only for deferrals. #470 and #670 are closeable on the record for the coordinator to close after merge.

2026-10-23 c-addr-747-1023: hosted shard C at ef43bf583 failed test_the_writer_rebuilds_every_adopted_record_from_its_prior_state (the adoption writer carries T-197's evidence into n=155's verified bound); fixed in 3bd3e6f49, re-pinned b6cc2b5db. Hosted CI green at b6cc2b5db: Packing validation 39981269619, Certificate page 39981269426, Branch mergeability 39981261856. Disposition reply https://github.com/jlevy/squares/pull/747#issuecomment-6369092386. PR left draft for the coordinator.


2026-10-23 c-rev2-747-1023: review B (follow-up, round 2) at b6cc2b5db, https://github.com/jlevy/squares/pull/747#issuecomment-6369595230. Verdict: approve with changes; no Blocker or High. A1-A9 dispositions hold (A1 as mechanism: the four held issues are never a close step; A2: three same-implementation entries, no rung moves vs c7300e28e or main). Findings: B1 (Medium) the held note claims an owner instruction and a 23 Oct start the beads do not hold (think-sdsl/mxhc 13 Oct, think-wnsv 15 Oct, think-l3oo 16 Oct reserve them for the owner; think-ezt8 lists them as an open owner question); B2 (Medium) T-138 note, #470 withdrawal note, README and PR body say every earlier register packing was measured and none pairs at 132/302/303, but identity.py compared nine entries (T-056, T-092, T-113, T-116 not compared there); B3 (Low) "earlier packings refined" where 10 of 12 sides are above the paired packing; B4 (Low) epistemics.md:750-752 and check_requests.py:23-25, :998 keep the old admission test; B5, B6 (Low suggestions). Credit line and contributor entries follow attribution.md and go no further. Reruns: identity.py byte-identical (10.4 CPU s); source-checker replay into scratch equal to receipts (40 invocations); 152 + 48 tests pass; check_results, check_release_impact, check_requests, intake_sweep --offline as expected.

2026-10-23 c-addr-747-1023: review B (https://github.com/jlevy/squares/pull/747#issuecomment-6369595230) addressed. Merged origin/main #752 (77d233ba0) and #751 (b78e851a4). 5e4ef6902: B1 held gains basis (owner-instruction | recorded-reservation) and beads; the four notes cite the reservation beads (think-sdsl, think-mxhc, think-wnsv, think-rfce, think-9v2k, think-l3oo, think-5ip2, think-ezt8) and say no owner instruction is recorded; B4 epistemics and check_requests wording; B5 intake_comments --out refuses a held issue; B6 invariant test. 41369ce5e: B2 readers for T-056, T-092, T-113, T-116, T-117; identity.json now 56 pairs over 13 entries (T-129 not readable): 302 = SQUISH T-116, 303 = SQUISH T-113, 14 of 16 pair, only 132 none; B3 four refined (103, 258, 302, 303), ten at a larger side. b11316bd3 no-change record vs main 05e95db36; 1814f4ea7 re-pin. No deferrals.

2026-10-23 c-addr-747-1023: merged origin/main #748 (777577956) and #746 (e2540728c); no-change record re-measured against cc91ee1b8 (e50c01aa6); pin 777577956. Head e50c01aa6, hosted CI green: Packing validation 40001829429, Certificate page 40001829729, Branch mergeability 40001822681. Review B dispositions https://github.com/jlevy/squares/pull/747#issuecomment-6372002362. PR left draft.
