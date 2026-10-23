---
type: is
id: is-01m5ghbpszw0r22b4wm95vgkfr
title: "Decide #715's 30 sub-print re-certifications of Couzo's 4e4c8ce certificates (2.4e-23 to 3.2e-23 below, same print)"
kind: task
status: in_progress
priority: 1
version: 8
delegate: c-lane-715-import
labels:
  - result-import
  - decision
dependencies: []
parent_id: is-01m5g8xj3hqca5wcen9f71dtnd
hold: null
hold_until: null
created_at: 2026-10-22T00:49:44.766Z
updated_at: 2026-10-23T01:52:17.076Z
started_at: 2026-10-22T00:49:56.222Z
---
Issue #715 (franciscouzo/square-packing 6b7391de) restates 64 counts at or below 1024 that the triage read as certificates first published at 02f9690, f311f08, a7067d7 and 4e4c8ce (9 to 15 October). At the pin, 30 of them are not byte-identical: the explicit certificates certificates/nN.cert, first committed at 5a299b4 (2026-10-20) and pushed with the pin at 2026-10-21T22:56:37Z after the issue, are exact L-border re-materializations of the same packings whose sides are below the 4e4c8ce certificates' by 2.37e-23 to 3.18e-23. Both round up to the same 12-place print. Counts: 535, 582, 591, 631, 633, 640, 682, 684, 691, 695, 735, 737, 742, 745, 790, 791, 797, 798, 799, 854, 855, 856, 857, 909, 913, 915, 916, 970, 975, 977.

By the ledger rule with exact sides, each would be recorded after the 4e4c8ce publication as a refinement of Couzo's own packing; by the issue's prints it is undecided. The lane's brief says to stop on a row whose newness depends on rounding, so nothing is recorded for these counts. The certificates are retained and replayed in packing/resources/web/couzo-issue715-2026-10-21 (receipts/filtered-exact-replay.json; receipts/earlier-publications.json gives each margin), and the 22 October ledger (packing/campaign/issue-intake/upper-bounds-20261022) leaves them undecided against the 4e4c8ce publication.

Decision wanted (coordinator or owner): record these 30 as #715's rows (a 30-row addition to the packet's claims record and source-coverage.yaml, superseding 487b058's rows now and 4e4c8ce's when think-yfoo lands), or leave them to think-yfoo's 4e4c8ce import as restatements.
blocked_on: none

## Notes

2026-10-22 c-triage-1022b (read-only; coordinator scratchpad triage-1022b/residue-held.tsv).

**The question is wider than #715's 30.** A report-order walk of Couzo's whole history at
325 to 1024 finds 44 more publications in the same class. Each is below the side it beats
by under 1e-12, and both round up to one 12-place print:

- **`5a299b4`: 31.**
  - 11 files: 327, 332, 372, 414, 451, 494, 539, 540, 587, 632 and 683.
  - 20 index L-border constructions: 326, 329, 334, 363, 366, 371, 402, 405, 443, 446,
    486, 531, 578, 627, 678, 731, 786, 843, 902 and 963.
- **`23aff0c`: 10**, at 325, 333, 362, 401, 442, 456, 485, 499, 530 and 577.
- **`4e4c8ce`: 3**, at 327, 332 and 542.

**What follows from them.**

- #719's ledger records two of them (366 and 372, both `5a299b4`'s) as reports.
- The source's own `submissions/2026-10-20/README.md` says "Differences within 1e-10 are
  treated as rounding" and "a tighter witness does not establish a new arrangement".
- **One answer should cover all 74.** The plan holds them all and records the earlier
  certificate as the row (couzo-residue-plan.md, O1). Recommended: restatements, not new
  rows.
- **In the corpus.** 18 of `4e4c8ce`'s certificates are below today's case lanes by
  1.6e-31 to 2.4e-12, but none is below an exact side the register already states. They
  are not this question.

2026-10-22 c-triage-1022d (read-only; triage-732/README.md §§2–3).

- **At 325–1024, #732 adds one row in the class: 499.** It is 8.66e-13 below #719's row,
  and both print 22.881306218113.
- **The precedents conflict.** #722 recorded #719's 631 (2.73e-13 below Couzo's, same
  print, kept at 16 places). #730's `SUB_PRINT` holds the class.
- **In the corpus, the class is larger.** At 42 counts whose house is Kingbird's,
  Mishapolk's files (published at `1851c2c`, #719's pin) are below the house's verified
  side by 1.35e-36 to 7.23e-15. Each is within one unit of the reported print's 14th place
  and the same arrangement.
  - The house rule's exception (T-195) would record them, if asked and validated.
  - The author has not asked: #719's question 4.
  - Adoption would cost 3.5 to 17.5 CPU-h.

2026-10-23 c-lane-sweep-1023a. Mishapolk's answer 4 on #719 (comment 6350348588, 2026-10-22T20:15:57Z): "We leave the recording of these 34 sub-12th-decimal quenches to maintainer discretion under the repository's threshold conventions." Not a claim: by the claim table ("below the standing bound and asking for no work") they stay pinned by digest in the mishapolk-issue719-2026-10-22 packet. Whether the record takes the class anyway (the house rule's T-195 exception, 3.5 to 17.5 CPU-h for the 42 in-corpus files at 814fbe9 per the #732 triage) stays the owner's question here; #719's entry notes it (claude/intake-bookkeeping-2026-10-23).

2026-10-23 (c-lane-couzo-residue-1022, review A of #730, A2): 9 history verdicts rest only on sub-print holds (`HISTORY_RESTING`): 5a299b4 at 325, 333, 362, 401, 442, 485, 530 and 577, and 23aff0c at 327. #719's 366 rests on one in #719's walk. The history walk holds 74 sub-print re-certifications (think-fwa9). A rerun without them records 8 steps, each itself a re-certification below the 12-place print, so this decision holds it again (`refusal_flips`, `held-dependents`). Any answer that leaves held publications out of the record still means rerunning the history walk (`beyond_horizon_replay`; see think-f2io's note of today).

2026-10-23 (c-lane-couzo-residue-1022, review A of #730, round 2, A6): a correction to this morning's note. The #719 walk now holds #715's re-certifications at the 19 counts it records them, as the history walk does (`Held(SUB_PRINT, "think-fwa9")`, no longer `Awaiting`), since they wait on this decision and not on an import. In that walk 5a299b4's not-recorded verdicts at those 19 counts (535, 582, 591, 631, 633, 640, 682, 684, 691, 695, 735, 737, 742, 745, 790, 791, 797, 798, 799) rest on them alone, beside #719's 366. `HISTORY_RESTING` and the #719 walk's `resting` declare them, and `check` holds them. A rerun without the sub-print holds records each of the 19 again as a re-certification below the 12-place print, so this decision holds it again; no row is at risk. Across both walks, 9 + 19 + 1 verdicts rest on sub-print holds.
