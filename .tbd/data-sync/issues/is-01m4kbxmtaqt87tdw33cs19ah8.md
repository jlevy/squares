---
type: is
id: is-01m4kbxmtaqt87tdw33cs19ah8
title: "Import wand125: s(28) >= 2297/400 and s(30) >= 2357/400 by fine-net check2 certificates (no issue)"
kind: task
status: in_progress
priority: 2
version: 15
delegate: bold-ritchie-l42
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
child_order_hints:
  - is-01m6kmn3kndnywx2z5anbp67tr
hold: null
hold_until: null
created_at: 2026-10-10T16:56:42.570Z
updated_at: 2026-11-04T17:45:59.902Z
started_at: 2026-11-04T15:03:02.888Z
---
Found by the 2026-10-10 evening reads (think-0nkn): wand125/square-packing 36b85b9 and ff9f269 add problems/square-lower-bounds/certificates/mixed_n28_L57425/ and mixed_n30_L58925/, check2 bundles on the 2,073-direction net (core 4999/5000, step 1/5002), reporting s(28) >= 2297/400 = 5.7425 (mass 2799999/100000; +3/400 over T-107's 1147/200; +1/400 over #446's unadopted 287/50) and s(30) >= 2357/400 = 5.8925 (mass 2999999/100000; +9/1000 over T-109's 11767/2000). Data: square-lower-bounds-v1 assets certificates__mixed_n28_L57425.tar.gz (627,191 B, SHA-256 7d0f910768d47fcdba6233334798487471db7ef2fe556400269c34c3116d3bf3) and certificates__mixed_n30_L58925.tar.gz (638,622 B, 0d11fe0554909e1457d70efa425c82344e622006590ac6ee58a481b69d1b61ba). Author: 772 s and 1790.3 s, 0.985 control at 32 directions. No issue reports them. Stages 1-3 as T-132 (#446 s(29)) did with devtools.fine_net_followup; full capture likely CPU-hours (owner budget).

## Notes

2026-10-10 stages 1-2 (intake sub-agent, branch worktree-agent-afd0e09abab917b31 from claude/determined-rubin-yjfy2a 1e642dc88): tool commit a7bf259c8, packet commit d8c795915 (packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/).

Pins: mixed_n28_L57425 at 36b85b9f37efa7cc5d4464805cfb0f2d21576267 (committed 2026-10-10T11:47:30Z) and mixed_n30_L58925 at ff9f2692afe7d1e65a51bb079b61b3710b97fc82 (14:12:31Z); both directories and the MIT LICENSE (blob bbfbff13) unchanged through head 27ed16885a3ac64c2a22c992f5375574ccf3ff16, whose five later commits change README tables only. Assets certificates__mixed_n28_L57425.tar.gz (627,191 B, 7d0f9107...3bf3, asset 627836167) and certificates__mixed_n30_L58925.tar.gz (638,622 B, 0d11fe05...61ba, asset 628141405) equal the API digest, SHA256SUMS lines 439 and 440, and ASSET.json; 11 documents each equal their commit blobs; each sealed bundle has 16 files matching all 15 files-sha256.json entries; verifier archive e495f9bf... as in the n29 and #446 packets.

Claims: s(28) >= 2297/400 (631 positive rectangles, mass 2799999/100000; +3/400 over T-107's 1147/200, +1/400 over #446's unadopted 287/50) and s(30) >= 2357/400 (463 rectangles, mass 2999999/100000; +9/1000 over T-109's 11767/2000), both core 4999/5000 on the 1/5002 net of 2,073 directions.

Premises (fine_net_followup premises): the narrow readers hold for both. audit_check2 holds n28 (EXACT_PREMISES_HOLD) and refuses n30 at its pre-publication receipt (fine-net-check2-receipt/v1 shape, verifier in place of build: KeyError 'build'), now recorded as CHECK2_READER_REFUSED; every earlier step passed and every listed file has the directory's digest. A reader change accepting the new shape (diff handed to the coordinator; audit_wand125_declared_net.py is outside this lane) makes n30 hold, with the existing 108 declared-net and follow-up tests passing. n30's pre-publication receipt is the check2 receipt's embedded run record (start 12:01:39Z, 1790.3 s, 12 threads, binary ec04d332...), and n28's repeats its check2 run (772 s against 771.6 s): one reported complete run each, where n29 had two.

Samples (sqverify-fast, source d97758bb, binary 567a0fd5, directions 0, 296, ..., 2072, one thread, two workers): 16/16 verified with the source's nodes and least bounds. n28: 21.19 CPU-s against the source's 33.05 (0.641); full capture 5,903 CPU-s, whole-net controls 5,911, total 3.28 CPU-hours, about 1.6 h wall at two workers. n30: 29.65 against 52.60 (0.564); 8,080 + 8,092 CPU-s, 4.49 CPU-hours, about 2.2 h. Both: about 7.8 CPU-hours; waits for an owner budget.

Register: two entries at V0/C0 (T-NN placeholders), pending adoption at n = 28 and 30; T-107 and T-109 keep both lanes; the #446 287/50 report stays. Proposed results, evidence, coverage, bibliography, resources README and n-028/n-030 open items handed to the coordinator. No issue asked, so no reply is owed.

2026-10-10 records lane R3: registered mixed_n28_L57425 as T-142 and mixed_n30_L58925 as T-143, both V0/C0 pending a complete capture and review (372dddf08); no case record changed (house adoption waits for jlevy/squares#403). Branch worktree-agent-a45d986d0210d7ec5 (records lane R3, merged into nothing yet).

2026-10-10 coordinator: the records branch was merged into claude/determined-rubin-yjfy2a at 4ce817db5 and is on draft PR https://github.com/jlevy/squares/pull/487 (CI on that branch is being driven to green); the ids are final once that PR merges to main. The stage 7 reply draft, where there is one, is in this bead or its answer bead.

2026-10-11: the owner set the budget in the session continuing PR #487: run the complete replay, its controls and its review here, on claude/determined-rubin-yjfy2a, before the merge (about 23 to 35 CPU-hours across think-r333, think-i85v and think-nd7g).

2026-10-11, later: the owner asked that PR #487 be validated, recorded and merged first, and that no expensive job start before then. The replay runs after the merge, under the budget above, in a follow-up stage 4 pull request from main; nothing has started.

2026-10-11, later still: the owner put the regularization of every packing (epic think-cdud, think-ux1v, a pull request stacked on PR #487) ahead of this run: clean graphics come first, and this bead now depends on think-ux1v. Order: PR #487 merges, then the regularization PR, then this replay.

2026-10-11 prep lane (nothing expensive ran): T-143 (n30) ready, smoke 5.8 CPU-s against 7.7, control samples at 0 and 1585 counted, revised 4.5 to 6.1 CPU-hours. T-142 (n28) census ready (smoke 4.5 CPU-s against 5.1, revised 3.3 to 4.5 CPU-hours) but its whole-net control is HELD: at the axis direction the 99/100 mutant's exact capture sits 2.15e-9 above the vertex sweep's certified bound, beyond the census's AXIS_ROUNDING of 1e-9 (CR-5 of the FC-1 re-check; n29's gap is 5.2e-10 and n30's 1.9e-10), so the control would write CONTROL_FAILED after 1.6 to 2.2 CPU-hours though the refusal is sound (exact capture below 1 at a centre inside the domain). Options for the owner and a review: widen AXIS_ROUNDING, derive it from the sweep's enclosure, or confirm with another control. Branch claude/wand125-confirmations-2026-10-11 (from claude/determined-rubin-yjfy2a 3ec95b418; commits 8ffbdbd1f..44eb6a017): runbook docs/project/specs/active/plan-2026-10-11-wand125-confirmations.md (mapped), --via release for proof bundles held only in release assets, devtools/retain_wand125_release.py, the census's MIXED_PACKETS, --evidence and --sweep-timeout, fine_net_followup control-sample. Total revised 23 to 31 CPU-hours, about 7 h wall in two lanes of two cores. Smoke receipts in the coordinator's scratch only. Owner questions pending: the n28 control's axis tolerance, and retaining the three check2 candidates in Git (as the 6 October check2 packet does, MIT; the nested verifier archive stays out).

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): the replay lane is https://github.com/jlevy/squares/issues/532 (T-142, T-143, T-144, with T-132). The owner questions on retaining the check2 candidates and on T-142's whole-net control tolerance are on https://github.com/jlevy/squares/issues/543. Tracker https://github.com/jlevy/squares/issues/544.

2026-10-31 bold-ritchie-l6 (stalled-bead triage of the 31 October intake pass, think-ztcy): Waits on think-ux1v, which the owner's order of 11 October puts first (in_progress, no update since 13 October, though #487, #497 to #549 and #518 have merged, so what remains of it needs checking), and on the replay tooling reaching main (claude/wand125-confirmations-2026-10-11 at 44eb6a0); then T-143's 4.5 to 6.1 and T-142's 3.3 to 4.5 CPU-hours, within the 40 CPU-hour item cap, with #543's two owner questions (check2 candidates in Git; T-142's control tolerance) open.

2026-11-04 bold-ritchie-l42 (intake lane L42, think-3guf; asked to run T-142's and T-143's census or control under the enclosure rule if priced at 15 CPU-hours or less, at two threads under nice -n 19): not run, and stopped here. What the two need, read today:
- Price: T-142's capture and whole-net control 3.28 to 4.5 CPU-hours (5,903 + 5,911 CPU-s from the 10 October eight-direction sample, revised up by the 11 October smoke run), T-143's 4.49 to 6.1 (8,080 + 8,092 CPU-s); together 7.8 to 10.6 CPU-hours, about 4 to 5.5 hours of wall at two threads. Within 15, and within the 40 CPU-hour item cap.
- No review reads either certificate (the 11 October final review read the record and premises only). result-import.md stage 4 and the declared-net checklist (review-2026-10-06-sqverify-fast-declared-net-soundness.md, For the Records Lane, item 7) need one before a census's evidence can be mapped, and check_results' verified_lane_review_problems refuses the verified lanes at n = 28 and 30 until a mapped review covers them: a census now would move no rung, as think-1lri found for T-132 (#889 deferred T-132's census for the same reason). That review is now think-4ul6.
- The release assets' members are not retained (pinned by size and digest only; #543 still asks the owner about keeping the three check2 candidates in Git, though think-r333 retained n29's on 2 November), and sqverify_fast_census lists no packet for them (MIXED_PACKETS, MIXED_ROOTS).
- This bead is still blocked by think-ux1v, the owner's order of 11 October (regularization before this replay).
- T-142's control tolerance question on #543 is moot: #892's enclosure rule judges its axis gap of 2.15e-9 (think-4uun). T-142's and T-143's next_rung and unfinished_confirmations now say so and name think-4ul6 (branch claude/bold-ritchie-xo28us-l42).
Order once unblocked: retain the two release assets' members, add the packet to the census, run think-4ul6's review, then the two censuses and controls (7.8 to 10.6 CPU-hours), --evidence with that review as the audit record, and the adoptions at n = 28 and 30. No reply is owed: no issue reported either.

2026-11-04 bold-ritchie-l42, later: on the coordinator's word (the owner's answer of 17 October to retain fine-net candidates where the census reads them; #543's checkbox is stale), both release assets' data members are retained (commit 7ccb06b3c on PR #903; check-retained 0 problems) and the census reads the packet. The coordinator has launched think-4ul6's review against 78729cfc2. Once it lands, the two censuses and controls (7.8 to 10.6 CPU-hours), the evidence with the review as audit_record and the adoptions at n = 28 and 30 go in a follow-up PR after #903, by the coordinator's decision. The think-ux1v ordering of 11 October is the coordinator's to clear with the owner.
