---
type: is
id: is-01m5pjxq31vpw03t0emgwnvhfe
title: "Import franciscouzo: 126 upper bounds at 330-997 (106 certificate rows) and 831 L-border recipes above 1024, the live records since #763's pin, at 43f666c (no issue)"
kind: task
status: in_progress
priority: 2
version: 9
spec_path: docs/project/specs/active/plan-2026-10-24-rows-above-1024.md
delegate: c-import-gn29-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5raz24s6yh4tg8dsytsak84
hold: null
hold_until: null
created_at: 2026-10-24T09:12:30.049Z
updated_at: 2026-10-25T03:02:07.326Z
started_at: 2026-10-24T20:35:18.503Z
---

## Notes

2026-10-24 coord-intake-1024, from think-cncq's triage (c-triage-watch-1024; full verdicts in that bead's notes). 43f666c (pushed with 73eac5b and 1c17153 at 06:10:44Z on 24 October) lowers 957 counts in certified_bounds.json, every one below #763's 964ee2b side and every tree member. To 1024: 126 counts; 108 own-count certificates at 330-997, deletion 690 (from 691), 17 L-border recipes; 797 and 847 restate #763 by the print ruling; 106 certificate rows to record; recipes wait on the D2 checker (W7), 690 on think-kzme. Above 1024: 831 recipes on 14 of the new certificates, for think-llit's walk. Price 0.3-0.5 CPU-h (111 best/ files, 12.1 MB raw). Unclaimed by any issue: a report from its commit (owner, 2026-10-14). Author questions (Couzo, with the #763 acknowledgement): does #763 extend to these rows; who ran CT105's browser searches; does #763 still claim 303 (43f666c's README cedes it to pjmathematician's side-only leaderboard entry, 3.47e-11 above); should #763's 268 credit name Lavrentev; is Tymchishin the 304 finder.
blocked_on: think-ptkk, think-llit

2026-10-24 coord-intake-1024: depends on think-lyf9 (the 99 Kaggle-credited sides at 964ee2b, which come before 43f666c in report order; 46 overlap 43f666c's counts).

2026-10-25 c-import-gn29-1024 (import lane, W1 records; coordinator coord-intake-1024). Branch claude/intake-2026-10-24-couzo-43f666c (worktree /home/user/wt-gn29), from main 2ed0ea740. Draft PR https://github.com/jlevy/squares/pull/800 (labels intake, S2).

WHAT LANDED ON THE BRANCH
- Claims: devtools.couzo_43f666c_claims (receipts/claim-map.json, lowered): 957 lowered below 964ee2b, 126 at 330-997 (108 certificates, 690 deletion from 691, 17 recipes), 831 recipes above 1024; triage counts reproduced; every one credited to Couzo; credit lines Lavrentev v11 76, Tymchishin v3 40, kyleluecke 3, Tymchishin 22-3662 2, alexchilton 2, aqibrazadev 1, Polkovskyi 1, own 1.
- Packet couzo-43f666c-2026-10-24 pinned at 1c17153: 108 certificates + 4 indexes retained (factual data), 8 pinned by digest; check_added_blobs PASS 10.4 MB.
- Walk upper-bounds-couzo-43f666c-20261024 (starts frozen at main 2ed0ea740), with #763's 17 claims with no row on main and the push of 23:38:42Z read commit by commit (receipts/earlier-push.json; 8/12/14 sides, none recorded). Records 106 certificates + 16 recipes; 797, 847 restate #763 (fwa9); 367 NOT recorded, 3.83e-12 above 23aff0c's held deletion from Friedman's 368 (rests on think-zkxy) - changed vs the triage; 690 settled with no row by D6 (deletion_holds; kzme confirms). All 46 #795-shared counts unchanged (below the notebook rows).
- Replay: 106 verified both routes, 636 controls refused, 133.3 positive CPU s (2,125 s summed, 17m47s wall on 2 workers); all-pairs 330/691/997 agree (789,186 pairs, 261.5 CPU s); recipes 16 decided by construction_checker, 144 controls refused; all first at 43f666c; all below Goebel.
- Register: source couzo-43f666c-2026-10-24, 122 current rows; supersedes #763 72 (7 of them its new recipe rows), #795 notebook rows 46, f1ceee4 3, #732 1. Bibliography [Couzo 43f666c 2026-10-24] (credit ... Polkovskyi, Levy), atom E-couzo-43f666c-beyond-horizon-report, census spans, requests entry 43f666c-rows-325-1024 under #763, watch read for 1c17153 names the import.
- Credit by the source's lineage (credit line and seed_credit agree at all 122); previous_source kept as data, credits nothing (coordinator's reading rule, think-vm3m M-1).

DRAFT AUTHOR QUESTIONS (next reply on #763, to Couzo; NOT posted)
Start: the triage's list (think-cncq), which the #763 import reply of 2026-10-24T13:37:28Z (issuecomment-6384882980) already asked as its questions 5 to 9, with no answer since. Couzo's 24 October answer on #672 (#790, think-mdfr) settles question 6: CT105 is the server behind his search web app, which only he runs, so its "browser searches" are his and the credit stands; say so and drop it. The rest stay open and are restated briefly.

Tell the author:
- 43f666c is recorded as a publication of its own, dated by the push of 2026-10-24T06:10:44Z: 106 certificates and 16 L-border recipes are rows; 797 and 847 restate #763's rows below the print; 367 is not recorded (3.83e-12 above 23aff0c's index bound at 367, Friedman's 368 less one square, which the record holds on think-zkxy); 690 has no row of its own by the owner's D6 answer. The 831 recipes above 1024 join the work above 1024 (think-llit).
- #763's 13 L-border recipes (365 444 487 632 733 734 737 788 789 845 910 966 970) are now rows, decided exactly by the record's construction checker from each recipe and its replayed parent; at 444, 487, 632, 733, 737, 788 and 845 43f666c's recipe supersedes them.
- Not to be said now: the brief asked to tell the author that 364, 450 and 874 are settled (think-yeol). The coordinator's later reading rule (stage 4 review of T-241/T-242, think-vm3m, M-1) found that #795's credits there read previous_source as the seed, which a separate lane corrects on main; the line waits for that correction.
- How the record credits 43f666c: by the lineage the source states, each entry's credit line ("refines the packing of ...") and its source_provenance.seed_credit, which agree at every one of the 122 rows (seed_credit is Couzo's own Kaggle push search at 412, his own row); previous_source is kept in the claim map as data and credits nothing.

Questions:
1. (still open, #763 question 5) Does #763 extend to 43f666c's 957 lowered bounds, or will they get an issue of their own? The record has taken them as the watched repository's publication from the push of 06:10:44Z.
2. (from think-lyf9's question 4) At 18 counts 43f666c is 5e-12 to 3e-11 below the notebook side 964ee2b published, and at the four counts measured (377, 405, 596, 984) it is the same packing. Is "Couzo after <author>" meant there as a new packing, or as a tighter certificate of theirs? The record follows the source's credit until you say.
3. (from the coordinator, after the #798 triage) At 377, 43f666c re-certifies 964ee2b's packing (every square within 1.7e-11) but moves its credit from kyleluecke to Kirill Tymchishin. Which is right?
4. (C1, from the coordinator's reading rule) What does your manifest's previous_source (and previous_reference.seed_credit) name: the record your catalogue held before at the count, or the packing a notebook or search started from? At 303, for example, source_provenance.seed_credit is Lavrentev while previous_source.credit is Evan Daniel (T-230). And which packing did each notebook run start from?
5. (new) Every recipe at or below 1024 in 43f666c and 964ee2b also has its full n-square expansion under certificates/parents/ at exactly its side, which the parents' manifest records. Are those expansions meant as the certificates of the recipes? The record decided each recipe from the recipe and its parent this time; the expansions agree with it.
6. (still open, #763 question 7) 43f666c's README no longer lists 303. Does #763 still claim 303?
7. (still open, #763 question 8) Should #763's 268 credit name Vladislav Lavrentev?
8. (still open, #763 question 9) Is Kirill Tymchishin the finder of the packing at 304?

LEFT
- 690's row: think-kzme. 367: think-zkxy. The 831 recipes above 1024: R3 (think-llit). Licences: think-m8f4.
- Recipe expansions under certificates/parents/ exist for all 30 recipes (A2 precedent would make them certificate rows); decided by the checker per the brief - coordinator's call.
- #798 re-chains at 376, 377, 416, 458, 502, 504 whichever merges second.

2026-10-25 coord-intake-1024: PR https://github.com/jlevy/squares/pull/800 (draft, intake, S2) at 41dd6da7e, CI green (40150051823, 40150051819). 122 rows (106 certificates, 16 recipes), #763's 13 recipes decided and recorded, 367 not recorded (think-zkxy), 690 settled by D6 (think-kzme). Senior review A by c-rev-800-1024 (think-fqs0) running. think-g2qy closes with the merge.

2026-10-25 coord-intake-1024: #800 MERGED as 4089f9587 at 03:01:36Z after review A (issuecomment-6392173409) and its dispositions (issuecomment-6392414804, head 82295bce6, CI green 40155651193/40155651191). #802 re-chains 376/377/416/458/502/504 next. The #763 follow-up for this import (author questions in gn29/author-questions.md: scope of #763, the 18 near-identical counts, 377's credit, recipe expansions, 303/268/304) is posted after the deploy, with C2 from think-hx0e.
