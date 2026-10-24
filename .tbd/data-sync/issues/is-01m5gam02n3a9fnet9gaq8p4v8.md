---
type: is
id: is-01m5gam02n3a9fnet9gaq8p4v8
title: "Owner decisions for #715 (and #666): counts above 1024, recipe-only rows, 335, hosting the bulk certificates"
kind: task
status: in_progress
priority: 1
version: 14
delegate: coord-intake-1021b
labels:
  - result-import
  - decision
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T22:51:56.373Z
updated_at: 2026-10-24T05:27:49.036Z
started_at: 2026-10-21T22:51:57.158Z
---
From the read-only triage of #715 (c-triage-715; full text: policy.md in the coordinator scratchpad triage-715/). No rule sets a ceiling above the n <= 324 horizon or mentions 1024, but the record holds nothing above 998, and #666's eight counts above 1024 wait on the same question.
D1. Track counts above 1024? Recommended: yes, no ceiling, rows recorded as reported (one answer covers #666).
D2. Do L-border/tiling rows with no certificate file of their own become rows? Recommended: yes, decided exactly from the recipe by a maintained checker; write the rule into the frontier README (4e4c8ce's deletion bounds wait on it too).
D3. Name a key reason to record 335 (#715's certificate is 1.84e-11 above Couzo's own 8 Oct decimal row)? Recommended: no; check the 8 Oct decimal poses exactly first; if they fail, propose a deferred-conflict correction.
D4. Host the certificates above 1024 (25-89 MB as Git stores them; OR-18)? Recommended: yes, a hosted-data manifest staged in the stage 2 PR; the owner publishes data/couzo-715-certificates-v1.
D5 (already open on #686): per-row credit beyond the horizon.
blocked_on: none

## Notes

2026-10-22 c-triage-1022b (read-only; coordinator scratchpad triage-1022b/residue-held.tsv).

**D2 also reaches below 1024.** The report-order walk of Couzo's history at 325 to 1024
holds 64 recipe bounds that no certificate file of their count stated when they were
published:

- `23aff0c`'s `upper_bounds.json`: 46 L-border and tiling constructions;
- Kevin Fang's `composites/table.csv` at `bef5c42` ("reproducible-only"): 17;
- `487b058`'s index: 1, at 327.

**Proposed D6.** Do index deletion bounds become rows? They are the bounds an index states
by deleting squares from the next count's certificate. There are 54 (`4e4c8ce` 39,
`23aff0c` 15); this is `think-yfoo`'s #627 C1 question.

- The runbook's claim table: "a consequence of another claim, such as monotonicity, at a
  count where the record holds no such value: its own entry only when it settles a case;
  otherwise the parent's scope covers it."
- Recommended: no rows, except where an issue claims the count, as #675 did at 992 and 995
  and #715 does at 743 and 985.

**D1.** Couzo's `5a299b4` index states 5,078 non-grid bounds above 1024: 282 certificates
and 4,796 constructions. #715 claims 1,112 of those counts. The certificate files cover
139 counts.

2026-10-22 c-triage-1022d (read-only; triage-732/README.md §4 and price.md D).

**#732 adds 5,078 rows above 1024**, at 1025–9913: 27,724,386 squares in 5.21 GB of
certificates at `Mishapolk/square-packing-records@814fbe9`.

- Census baselines: #715's print at 1,112 counts, the grid at 3,966.
- Against #715's prints: below at all 1,112, by less than 1e-12 at 66.
- #719's eight counts keep #719's sides.
- 3426's certificate is above its own grid side.
- **The issue proposes capping tracking at N = 10,000** (§7), a question for this decision.

**The price if A:**

- about 19 CPU-h on the positives, or 193 CPU-h with six controls (over the item cap: five
  or more items, or controls sampled);
- about 1.6 GB of derived facts, since there is no licence: a data release under OR-18
  (D4).

2026-10-23 c-lane-sweep-1023a.
- D4 premise for #732: the triage priced "about 1.6 GB of derived facts, since there is no licence". At 17cc220 (2026-10-22T20:15:36Z) Mishapolk added an MIT LICENSE, and his #719 comment 6350348588 says it covers every certificate, catalogue, manifest and tool. If A, the 5,078 certificates above 1024 (5.21 GB at 814fbe9) can be hosted as the files themselves in a data release (OR-18), not as derived facts.
- D5 evidence: the same comment says the 69 rows of #719 below the preceding report by less than 1e-9 are "precision continuous Newton/SQP quenches of the predecessor reported topologies", i.e. refinements of the reports before them, and that 447 is a new arrangement. No per-row parent list yet.
- #732's requests entry (claude/intake-bookkeeping-2026-10-23) queues its ask to cap tracking at N = 10,000 on this bead, with D1.

2026-10-23 (c-lane-couzo-residue-1022, review A of #730, A1 and A2): corrections to D2 and proposed D6, and what an answer that leaves holds out reopens.

**D2 and D6 describe 23aff0c's 61 holds wrongly.** The #730 history walk holds them, and `upper_bounds.json` at 23aff0c (pinned by digest in the couzo-issue670-2026-10-17 packet) states each one's construction. All 61 are classical constructions, not L-border/tiling recipes or deletions from a certificate:
- The 46 D2 holds are Göbel's squares (27, credited "Frits Göbel; family formulas generalized by David Ellsworth") and Friedman's off-centre family (19, citing this repository's `packing/cases/gobel_offcentre/packing.py`). 41 of the 46 are L-border extensions; 368, 543, 626, 752 and 849 are bare Friedman constructions.
- The 15 proposed-D6 holds (367, 406, 447, 541, 542, 588, 589, 638, 751, 847, 848, 906, 907, 967, 968) each delete one or two squares from Friedman's constructions at 368, 407, 448, 543, 590, 639, 752, 849, 908 and 969, not from a certificate.

So these 61 also wait on #613 (think-8krd): does a classical construction count as an earlier report? `beyond_horizon_replay.HISTORY_HELD` now names think-8krd beside think-f2io on both holds (`Held.also`) and says what each is (`Held.note`). `HELD_CLASSES` now reads:
- recipe: "a construction an index or table states with no certificate file of its own: an L-border, tiling or composite bound, or a classical construction (Göbel's squares, Friedman's off-centre family) or an L-border extension of one";
- consequence: "an index bound that deletes squares from a larger count's certificate or from a construction the index states".

The other D2/D6 holds fit as written:
- 4e4c8ce's 39 deletion bounds each delete from a 4e4c8ce certificate; for example, 743 deletes from best/n744.cert.
- bef5c42's 17 are composites.
- 487b058's 327 is an L-border extension.

**What an answer reopens (A2).** 131 history verdicts (126 not recorded, 5 undecided) and 2 of #719's were decided only against held publications. `beyond_horizon_replay` declares them (`HISTORY_RESTING`, `Resting`), and `check` holds them to the ledger (`resting_problems`). An answer that leaves a hold out of the record takes it out of the walk, so the walk is run again. `held-dependents` / `refusal_flips` reruns it by intake_ledger's rule from the frozen starts:
- **If D6 leaves deletion bounds out:** 9 of 5a299b4's certificates become records, at 406, 447, 588, 589, 638, 906, 907, 967 and 968. They are below everything else standing, and none has a row or a hold. (447 is also #719's walk.)
- **If D2 leaves recipes out:** 47 more become records:
  - 5a299b4 at 37 counts (407, 448, 457, 491, 533, 534, 580, 581, 590, 629, 630, 639, 677, 680, 681, 690, 730, 733, 734, 741, 785, 788, 789, 796, 842, 845, 846, 901, 904, 905, 908, 962, 965, 966, 969, 981, 982);
  - 5f3bdbf at 757, 813 and 871;
  - 487b058 at 812 and 930;
  - 43ac7d2's five undecideds at 812, 930, 931, 992 and 993.
- **Göbel and sub-print holds:** every step a rerun would record is above Göbel or a re-certification, so the same decision holds it again.

Either D2 or D6 answered "no rows" therefore means rerunning the history walk and writing those rows (with their replay), not only dropping the holds.

2026-10-23 coord-intake-1023: OWNER DECISION on D1 (in conversation, 23 October): YES, track counts above 1024 with no ceiling; rows recorded as reported, as below 1024. D4 follows as recommended (a hosted-data manifest, not Git blobs; OR-18) unless the owner says otherwise. Still open: D2, D3, D5, D6. Covers #666 (eight counts), #715, #719 (eight rows 1061-1568, think-9vr8) and #732 (5,078 files). Implementation owed: new bead(s) under think-ezt8.

2026-10-23 coord-intake-1023: OWNER DECISION on D2 (in conversation, 23 October): YES, recipe-only (L-border/tiling) rows become rows, decided exactly from the recipe by a checker this project maintains; the rule goes into the frontier README. Needs a recipe-checker PR (W7) before any recipe row is recorded. Still open: D3, D5, D6.

2026-10-23 c-addr-742-1023 (PR #742 review A, A6): what each answer would record in the
#732 walk beside #732's own claims. Leaving deletion bounds out (D6) records #732's 985,
eight of the author's 1851c2c files (367, 406, 541, 542, 588, 589, 638, 847), 8a488a1's file
at 848, and Couzo's 5a299b4 index at 8 counts. Leaving constructions with no certificate file
out (D2) records 24 of the 1851c2c files (368, 407, 448, 457, 533, 534, 543, 581, 590, 626,
630, 639, 677, 690, 730, 733, 734, 741, 785, 788, 789, 796, 845, 846), 8a488a1's at 849, and
5a299b4 at 37 counts. The author's files would need rows under a release that no walk
declares yet. Packet README, Held Back and Not Recorded.

2026-10-23 coord-intake-1023: OWNER DECISION on D6 (in conversation, 23 October): YES, a deletion bound (a side obtained by deleting a square from a published certificate at the next count) is an earlier report in report order; #732's 985 stays unrecorded. Applied by c-answers-1023 (PR #754) with the sub-print, withdrawn and Goebel answers. Still open: D3, D5.

2026-10-23 c-answers-1023 (PR https://github.com/jlevy/squares/pull/754, commit f590f81f4): OWNER DECISION on D6, relayed by coord-intake-1023 (23 October): a deletion bound, a side obtained by deleting squares from a published certificate at a larger count, IS an earlier report in report order. Applied on this bead's recommended terms ("no rows, except where an issue claims the count"), through 1024:
- 4e4c8ce's 39 index deletion bounds (each from a 4e4c8ce certificate) are a settled hold in the history, #719 and #732 walks (`beyond_horizon_replay.DELETION_ANSWER`, `Held.answer`): recorded in the walk, passed over by the chain, no row of their own, and no verdict rests on them. #732's 985 ties the bound and stays unrecorded; #715's restatements at 743 and 985 likewise. No row changes.
- 23aff0c's 15 deletions from Friedman's off-centre constructions are not deletions from a certificate, so they stay held with D2 (their parent constructions, which wait on the recipe checker) and think-zkxy.
- `held-dependents` now: leaving 23aff0c's deletions out would record 9 of 5a299b4's certificates (history walk) and, in #732's walk, 8 of the author's 1851c2c files, 8a488a1's 848 and 5a299b4 at 8 counts; nothing of #732's own.
- The exception is not applied: whether an issue's claim gives a deletion bound a row (743, superseded by #719's; 985, where the current row is couzo-verified-bounds-2026-10-14's of 14 October, 2.2e-10 above the bound, the one count to 1024 where a settled bound is the best side) is think-kzme. Rule text: result-import.md, Several Reports at One Count; frontier README. Rows above 1024 (#715's 158 deletions, #732's) are think-llit's.
- Still open here: D3, D5; D2's checker (W7).

2026-10-23 c-answers-1023 (PR https://github.com/jlevy/squares/pull/754, review A, A1 and A3): correction to my D6 note above, which stated the answer more broadly than it was given.

**The recorded answer** (corrected in place on 2026-10-23 by c-fix-754b-1023; see the note below): the owner selected the option labelled "Yes, an earlier report (Recommended)". The rest is the question the coordinator asked, not the owner's words. As coord-intake-1023 relayed them in its calls on review A of #754, the question was "a side obtained by deleting a square from a neighbour's certificate (e.g. Couzo's 985 from his 986)", and the selected option's description read "A published deletion bound counts like any stated bound; a later equal or higher side is not recorded".

**What #754 now applies:**
- Settled: 36 of 4e4c8ce's 39 index deletion bounds, each deleting one square from the next count's 4e4c8ce certificate (505 ... 989; 16 of them in #732's walk). Recorded in the walk, passed over by the chain; #732's 985 ties and is not recorded. `beyond_horizon_replay.DELETION_ANSWER`.
- Not settled: 751 (three squares from 754's certificate), 752 (two from 754's) and 927 (two from 929's), per certified_bounds.json at 4e4c8ce. They are beyond the answer's words and stay held on think-kzme. Each count's later steps are recorded below them, so no verdict rests on them.
- No row of their own is this bead's recommendation, not the owner's word. Whether the option's description, "counts like any stated bound" (the coordinator's words), gives a deletion bound a row is on think-kzme, along with the issue-claimed counts 743, 798, 855 and 985.
- No verdict or row changes from the earlier note. Rule text: result-import.md (Several Reports at One Count), the frontier README, and beyond_horizon_replay.HELD_CLASSES and DELETION_ANSWER.

2026-10-23 c-fix-754b-1023 (PR https://github.com/jlevy/squares/pull/754, review B, "Not verified": https://github.com/jlevy/squares/pull/754#issuecomment-6376229374). coord-intake-1023 confirmed how D6 was answered: it asked the owner a multiple-choice question in conversation, and the owner selected the option labelled "Yes, an earlier report (Recommended)". The question text and the option's description were written by the coordinator, not the owner. Changes:
- Corrected in place: the note above that called the question and the option's text "the recorded words", and its reference to "counts like any stated bound". No other note on this bead quotes the question or the description as the owner's.
- In #754 (commit 8775445cd): `result-import.md`, `beyond_horizon_replay.DELETION_ANSWER` and its comment, and the history and #732 walks' notes now quote only the selected label as the owner's answer and attribute the rest to the question the coordinator asked. `DELETION_ANSWER` states "a later equal or higher side is not recorded" as the consequence, not as the answer. No ledger.json, start or verdict changed.
- think-kzme's description and notes are corrected the same way.

2026-10-24 coord-intake-1023: D5 now includes Polkovskyi's request, in his #732 comment of 20:35:12Z on 23 October, for sole credit at 11 counts of the f1ceee4 release. His manifest calls all 138 refinements of Couzo's topology (127 under one wording, 11 under another). #769 records the request as queued and measures it pose by pose in `receipts/pose-identity.json`; it decides nothing. The owner's D5 answer, on how per-row credit beyond the corpus names a packing it refines, decides it.
