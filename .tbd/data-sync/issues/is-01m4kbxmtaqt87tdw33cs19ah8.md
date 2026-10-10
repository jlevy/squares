---
type: is
id: is-01m4kbxmtaqt87tdw33cs19ah8
title: "Import wand125: s(28) >= 2297/400 and s(30) >= 2357/400 by fine-net check2 certificates (no issue)"
kind: task
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:56:42.570Z
updated_at: 2026-10-10T17:45:33.950Z
---
Found by the 2026-10-10 evening reads (think-0nkn): wand125/square-packing 36b85b9 and ff9f269 add problems/square-lower-bounds/certificates/mixed_n28_L57425/ and mixed_n30_L58925/, check2 bundles on the 2,073-direction net (core 4999/5000, step 1/5002), reporting s(28) >= 2297/400 = 5.7425 (mass 2799999/100000; +3/400 over T-107's 1147/200; +1/400 over #446's unadopted 287/50) and s(30) >= 2357/400 = 5.8925 (mass 2999999/100000; +9/1000 over T-109's 11767/2000). Data: square-lower-bounds-v1 assets certificates__mixed_n28_L57425.tar.gz (627,191 B, SHA-256 7d0f910768d47fcdba6233334798487471db7ef2fe556400269c34c3116d3bf3) and certificates__mixed_n30_L58925.tar.gz (638,622 B, 0d11fe0554909e1457d70efa425c82344e622006590ac6ee58a481b69d1b61ba). Author: 772 s and 1790.3 s, 0.985 control at 32 directions. No issue reports them. Stages 1-3 as T-132 (#446 s(29)) did with devtools.fine_net_followup; full capture likely CPU-hours (owner budget).

## Notes

2026-10-10 stages 1-2 (intake sub-agent, branch worktree-agent-afd0e09abab917b31 from claude/determined-rubin-yjfy2a 1e642dc88): tool commit a7bf259c8, packet commit d8c795915 (packing/resources/web/wand125-fine-net-n28-n30-2026-10-10/).

Pins: mixed_n28_L57425 at 36b85b9f37efa7cc5d4464805cfb0f2d21576267 (committed 2026-10-10T11:47:30Z) and mixed_n30_L58925 at ff9f2692afe7d1e65a51bb079b61b3710b97fc82 (14:12:31Z); both directories and the MIT LICENSE (blob bbfbff13) unchanged through head 27ed16885a3ac64c2a22c992f5375574ccf3ff16, whose five later commits change README tables only. Assets certificates__mixed_n28_L57425.tar.gz (627,191 B, 7d0f9107...3bf3, asset 627836167) and certificates__mixed_n30_L58925.tar.gz (638,622 B, 0d11fe05...61ba, asset 628141405) equal the API digest, SHA256SUMS lines 439 and 440, and ASSET.json; 11 documents each equal their commit blobs; each sealed bundle has 16 files matching all 15 files-sha256.json entries; verifier archive e495f9bf... as in the n29 and #446 packets.

Claims: s(28) >= 2297/400 (631 positive rectangles, mass 2799999/100000; +3/400 over T-107's 1147/200, +1/400 over #446's unadopted 287/50) and s(30) >= 2357/400 (463 rectangles, mass 2999999/100000; +9/1000 over T-109's 11767/2000), both core 4999/5000 on the 1/5002 net of 2,073 directions.

Premises (fine_net_followup premises): the narrow readers hold for both. audit_check2 holds n28 (EXACT_PREMISES_HOLD) and refuses n30 at its pre-publication receipt (fine-net-check2-receipt/v1 shape, verifier in place of build: KeyError 'build'), now recorded as CHECK2_READER_REFUSED; every earlier step passed and every listed file has the directory's digest. A reader change accepting the new shape (diff handed to the coordinator; audit_wand125_declared_net.py is outside this lane) makes n30 hold, with the existing 108 declared-net and follow-up tests passing. n30's pre-publication receipt is the check2 receipt's embedded run record (start 12:01:39Z, 1790.3 s, 12 threads, binary ec04d332...), and n28's repeats its check2 run (772 s against 771.6 s): one reported complete run each, where n29 had two.

Samples (sqverify-fast, source d97758bb, binary 567a0fd5, directions 0, 296, ..., 2072, one thread, two workers): 16/16 verified with the source's nodes and least bounds. n28: 21.19 CPU-s against the source's 33.05 (0.641); full capture 5,903 CPU-s, whole-net controls 5,911, total 3.28 CPU-hours, about 1.6 h wall at two workers. n30: 29.65 against 52.60 (0.564); 8,080 + 8,092 CPU-s, 4.49 CPU-hours, about 2.2 h. Both: about 7.8 CPU-hours; waits for an owner budget.

Register: two entries at V0/C0 (T-NN placeholders), pending adoption at n = 28 and 30; T-107 and T-109 keep both lanes; the #446 287/50 report stays. Proposed results, evidence, coverage, bibliography, resources README and n-028/n-030 open items handed to the coordinator. No issue asked, so no reply is owed.
