---
type: is
id: is-01m4yrbj9wxd8hw5jndkmxa0fj
title: "Watch reads 2026-10-15: bengreff 0699398, BuddenPing 318ab94 and squares e96e9ea, evand 1038892, wand125 afdcaac, TheSnakeFang 078789a, franciscouzo b85dee2/487b058/4e4c8ce/58a7833, for intake-watch.yaml"
kind: task
status: closed
priority: 2
version: 10
delegate: user-eb-intake-residue
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-15T03:05:40.412Z
updated_at: 2026-10-16T05:47:05.300Z
started_at: 2026-10-15T03:06:07.321Z
closed_at: 2026-10-16T05:36:21.646Z
close_reason: "Its reads are on main (intake-watch.yaml at e2e018f32, via #627 in stack #632); no record names it as a deferral."
resolution: null
duplicate_of: null
---
The 15 October reads lane (think-mq0k, branch claude/wizardly-meitner-wqn4x3-reads-1015) read the watched heads the 02:30Z sweep at main 6964362b5 listed, by blobless clones, and re-read every head with git ls-remote at about 03:10Z (all unchanged). This bead holds the intake-watch.yaml reads the next records PR writes (this lane edits no record), and the read-only triage of the heads with nothing to import.

## Reads to write (packing/campaign/intake-watch.yaml, read_on 2026-10-15)

1. https://github.com/bengreff/s76-certificate, read_through 06993982e83dba37ca12121bd876396a15571fcb, bead think-osvq. One commit past the bengreff-s76-certificate-2026-10-14 packet's 1cb924f, of 14 October (08:16Z): the second route, zm_mixed.py alone over all 129,600 D4 roots at depth 24 (129,599 certified, 6 boxes left in one root R) and R alone at depth 34 (certified), with records/zm_full/, tools/check_full.py and verify.sh's --full-zm; 181 CPU-h at the source. The cover, the composite's records and the Lean are unchanged. New evidence for T-184, owned by think-osvq until a packet pins this commit; the records audit and prices are in its notes.
2. https://github.com/BuddenPing/square-packing-certificates, read_through 318ab94e821ba7280a68fa8ce2942c9ecdbda41d, no bead. Three commits of 12 October (UTC) change only README.md and SHA256SUMS: d68883c (22:40Z) indexes the #566 and #567 certificates of 18092df and 8f96ceb, 2030fd1 (22:59Z) the #568 and #569 certificates of 260aaf5, and 318ab94 (23:46Z, the head) replaces the first with the strengthened ones of 820b9ff and e70342d. Every indexed digest is one the pingyou-n105, n146, n261 and n272 refinement packets record; no certificate changes. Nothing to import.
3. https://github.com/BuddenPing/squares, read_through e96e9ea95c15c6ad3a9a547a8cb02760e721cfc4, no bead. A fork of this repository; its default branch is e96e9ea, the merge of jlevy/squares#507 (2026-10-12T23:07Z), an ancestor of jlevy/squares main, so it publishes nothing of its own there. Its other branch, codex/numerical-certificate-refinements at 4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde, is PR #574's head, which the pingyou-pr574-certificates-2026-10-13 packet pins (T-174). Nothing to import.
4. https://github.com/evand/square-packing, read_through 103889284ac06d28329bee6580fddf48d204f647, no bead. The 25 commits of 14 October (local time; 06:51Z to 15 October 00:26Z) from 73aa066 to 1038892 past the 622cd2e read. One adds a certificate: e006ce6 adds search/packer/candidates/tt2_n146.*, which #606 reports and the evand-n146-2026-10-14 packet retains at e006ce6 (think-rvv7; on claude/wizardly-meitner-wqn4x3-intake-1014b); 8cfc344 records the post. 1038892, the head, is TT2 at n = 110: the 18 "new" rows are the sub-11 minima of the two arms not in the 10 October as-of store (S 6, C 12); exactsolve certifies 6 directly, all among the store's 939 known exact minima (10.996923243 to 10.999651054); after exact/descend.py, 11 of the other 12 land on known minima, the best being the record minimum itself (10.99678339663159164, the case's verified side 10.996783396631591639612746267957 rounded up), and one (10.99692215) is still not jammed. None is below the record or any earlier report, and no certificate is committed (runs/ is untracked). The rest is the packer's development (B1 and B2 merges, near-miss queue, finisher, candidate automation, distinctness facts, jobs), the TT2 census and record metrics, night runs with no record at n <= 324 (about 128 CPU-h), M0's exact rebuild of #575's 176 (a tie), pk/pending.yaml pins of #596, #600 and #606, the records time-lapse video, handoffs and TODO triage. Nothing else to import.
5. https://github.com/wand125/square-packing, read_through afdcaac4ec2401cd4763cf6245c68539932865ba, no bead. Four commits of 15 October (JST; 2026-10-14T18:27Z to 19:05Z) past 1c661b7, the wand125-closed-form-source-hash-2026-10-14 packet's pin: eb22671 adds problems/cubes-in-cube, s3(9) = s3(10) = 2 + 1/sqrt(2) for unit cubes in a cube, by an 8-point lemma (every closed unit cube in [0, s]^3 holds a point of {1, s - 1}^3) checked by two interval branch-and-bound checkers, with Q(sqrt 2) packings; 3b6b671 lists it in the README; 7418838 and afdcaac add the site's paper, 3D view, results and theme #20. Three-dimensional cube packing is outside this record, which is squares in a square; the method is DS7's point-set argument in 3D and moves no square count. The earlier reads that name think-xzob stay. Nothing to import.
6. https://github.com/TheSnakeFang/squarepack-certs, read_through 078789a4cfd36f915f1bfbe76d742413d79b2965, no bead. The head is the pin of the fang-direct-certificates and fang-excess-theorem packets; the sweep flags d6b0122 and bef5c42 only for .gitignore, every other path they change being in the 078789a packets' scope. d6b0122 (12 October 19:08Z) copies Evan Daniel's MIT certificates into third_party/daniel/ as the B pieces of the composites: n-5 to n-273 from evand 29d0cee search/exact/batch/certs/ and hunt3_n308, n343, n344 from c013f43, each byte-identical to the upstream blob (Git blob ids compared here), with LICENSE, NOTICE and SOURCES.md, and third_party/fetch_unlicensed.sh, which downloads de Winter's unlicensed n211 record and Daniel's n-211.cert from pinned commits and checks their SHA-256 rather than redistributing them; .gitignore ignores that download directory. No claim of the author's own. bef5c42's composites are think-rn2y's import. Nothing else to import.
7. https://github.com/franciscouzo/square-packing, four reads:
   - read_through b85dee2b964e7f7fb9f765227e60c44cdcd3aa4d, no bead: the eight commits a7067d7 to b85dee2 past 337078c, whose certificates the #561, #583 and #586 packets retain at 0fa0e0d, 4596670 and b85dee2; the unretained paths are prose, reviews, the #561 publication drafts (added in e9eb44b, removed in 06d8db2), search code, found/ logs, known_best.json, decimal poses and drawings. Nothing to import.
   - read_through 487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d, bead think-nj7h: s(211) 9.29e-6 below #586 and 296 beyond-horizon certificates, until a packet pins it.
   - read_through 4e4c8ce23cb5e87f033021687010992c40575480, bead think-yfoo: the index for n < 1024, 341 beyond-horizon counts below 487b058 and #607 (its 237 is think-7j8o's packet; 43ac7d2 is #607's, think-qik6, packet on claude/wizardly-meitner-wqn4x3-intake-607).
   - read_through 58a783368d4b7e70bb800f0009ea9ca03e578739: the couzo-n237-2026-10-15 packet (this lane's branch) pins it for certificates/n237.cert; its other change, the Göbel square and strip bounds (gobel_bounds.json, GOBEL_COMPARISON.md, gobel_comparison.csv), are classical closed forms with no discovery claimed, equal inside the corpus to closed forms the record holds. Nothing else to import. If the packet has not landed when the read is written, name think-7j8o.

## Notes

## BuddenPing 318ab94: the 146 and 261 comparison, exact (packet claims files; script compare_146_261.py in the lane's scratch)

318ab94's index names the n146 certificate of 820b9ff (#566's update, T-168) and the n261 certificate of e70342d (#567's update, T-169), unchanged; it adds no certificate. In report order:

| n | Report | First committed | Exact side, truncated at 22 places | Against the previous row |
| --- | --- | --- | --- | --- |
| 146 | T-150, Barnett #505 | 2026-10-11 | 12.5837822039510462034570 | case house |
| 146 | 18092df, #566 as filed | 2026-10-12T22:37:38Z | 12.583782203950967 (print) | 8.0e-14 below T-150, superseded by the author |
| 146 | 820b9ff, #566 update, T-168 | 2026-10-12T23:41:08Z | 12.5837822039508342919134 | 2.119e-13 below T-150 |
| 146 | PR #574, T-174 | 2026-10-13T01:58:06Z | 12.5837822039508342919134 | 1.258e-79 below T-168 |
| 146 | #606, Evan Daniel tt2_n146 | 2026-10-14T21:50:35Z | 12.5837821901518603422925 | 1.380e-8 below T-174 |
| 261 | T-150, Barnett #505 | 2026-10-11 | 16.6787798753432077466977 | case house |
| 261 | 8f96ceb, #567 as filed | 2026-10-12T22:39:32Z | 16.678779875343112 (print) | 9.6e-14 below T-150, superseded |
| 261 | e70342d, #567 update, T-169 | 2026-10-12T23:44:55Z | 16.6787798753429098149372 | 2.979e-13 below T-150 |
| 261 | PR #574, T-174 | 2026-10-13T01:58:06Z | 16.6787798753429098149352 | 1.992e-21 below T-169 |

So 318ab94 publishes nothing new, and its sides are above the smallest report at both counts: T-174's at 261, #606's at 146 (T-174's 146 is 1.26e-79 below T-168's). Couzo's 4e4c8ce index holds #606's packing at 146 (regularized display view, credit Evan Daniel) and T-169's at 261 (credit BuddenPing), neither a new report.

2026-10-15, after the 487b058 import (think-nj7h): the couzo-verified-bounds-2026-10-14 packet on this branch pins 487b058 with a scope of the root README, upper_bounds.json, certificates/README.md, n211's files and the 296 beyond-horizon certificates and their metadata. Once it lands, the franciscouzo read through 487b058 needs no bead for those paths; its note should cover the changed paths outside the scope: lower_bounds.json, lower_bound_families.json and lower_bounds.py (the author's closed-form lower-bound index, which restates published bounds), expanded_comparisons.py, import_external.py, expanded_reference_bounds.json, known_best.json, the decimal packings and drawings it deletes or rewrites, and the 22 deleted certificates (superseded copies). Nothing in them to import. Until the packet lands, keep the read with bead think-nj7h.

## 2026-10-15 records-1016 lane (think-mq0k), branch claude/wizardly-meitner-wqn4x3-records-1016, https://github.com/jlevy/squares/pull/616

All reads written to packing/campaign/intake-watch.yaml: bengreff s76 06993982 (think-osvq), BuddenPing square-packing-certificates 318ab94 and squares e96e9ea, evand 1038892, TheSnakeFang 078789a, franciscouzo b85dee2 (nothing to import; the paths the 02:30Z and 05:30Z sweeps flagged), 487b058 (packet pins it; out-of-scope paths hold nothing) and 58a7833 (think-yfoo), and wand125 through b57e667 (covers afdcaac). Close at merge.

2026-10-16 ~05:25Z, overnight coordinator user-eb (epic think-hg5s): ownership transferred to user-eb-intake-residue (bead think-mu5v) from claude-code@vm (last update 2026-10-15T09:15:52.197Z), because the sweep of 05:08Z reports this bead's blocker resolved and the owner asked tonight for the intake to continue. The lane resumes the work, closes the bead if it is done, or rewrites blocked_on.

2026-10-16 ~06:00Z user-eb-intake-residue (lane A, think-mu5v): resumed after the sweep of 05:08Z read #575, #596 and #586 (all closed 16 October) as this bead's waits. The work is done: every read this bead held is on main e2e018f32 in packing/campaign/intake-watch.yaml (bengreff/s76-certificate 0699398 with think-osvq; BuddenPing/square-packing-certificates 318ab94; BuddenPing/squares e96e9ea; evand 1038892; TheSnakeFang 078789a; franciscouzo b85dee2, 487b058 and 58a7833 with think-yfoo; wand125 through b57e667, which covers afdcaac), carried to main by #627 (which superseded #616) in stack #632. No record names this bead as a deferral (only a YAML comment in intake-watch.yaml). Closing.
blocked_on: none

Correction (user-eb-intake-residue, 2026-10-16T05:47Z by date -u): the '~06:xxZ' times in this lane's notes of 16 October are about an hour late; they were written between 05:30Z and 05:47Z. The site pages were read at about 05:35Z. No condition changes: every last reply named is still more than a day old.
