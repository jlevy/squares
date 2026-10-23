---
type: is
id: is-01m4sce332y1xzh721zeyxrmet
title: "Put the T-153 reviews' questions to the author and post the #557 acknowledgement (owner's call)"
kind: task
status: open
priority: 2
version: 5
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4sce0tyvdb701rcxm7p6h4g
hold: null
hold_until: null
created_at: 2026-10-13T01:01:08.066Z
updated_at: 2026-10-23T06:16:09.033Z
started_at: 2026-10-14T01:30:14.468Z
---
The first review's section 8 lists eleven questions for the author; Q1 and Q3 concern file bindings outside the proof packet, and a mismatch found in answer would make the read defect-found and T-153 incomplete. K1 drafted an acknowledgement for https://github.com/jlevy/squares/issues/557 that has not been posted. Add the second review's questions (think-4j3n) when it lands. Posting is outward-facing: the owner decides when.

## Notes

Add the second review's questions (docs/project/reviews/review-2026-10-13-overbeck-n17-candidate-second.md, Questions for the Author) and SR-1..SR-9 alongside the first review's eleven questions.

2026-10-14: the consolidated share-back below covers all three reviews (first review §8, the second review's SR-1..SR-9 and questions, and the Fable mathematical-correctness review's findings and questions, deduplicated into 21 items). It replaces K1's acknowledgement draft, which lived in a session scratch that no longer exists. Post only on the owner's word, after the follow-up PR with the mathematical-correctness review merges.

Draft share-back for Marc Leonard Overbeck (GitHub Kleddamag), on https://github.com/jlevy/squares/issues/557 with an @Kleddamag mention, or as an issue on Kleddamag/the-seventeenth-square-candidate: the owner chooses where, and it is posted only on the owner's word (result-import.md, stage 7), after the follow-up pull request that adds the mathematical-correctness review has merged, so that every link resolves on `main`. It consolidates the questions of all three reviews (first review §8 Q1–Q11; second review SR-1..SR-9 and Q1–Q6; mathematical-correctness review findings 1–7 and Q1–Q4), deduplicated; the bracketed tags say where each came from and are removed before posting.

Drafted 2026-10-14.

---

@Kleddamag, thank you for publishing the verification edition, and for its known-issues and known-limits lists, which made it much easier to review.

**What we did.** We retained the edition at `653b9589` with release `large-files-v1` as digests, derived exact facts and receipts (no upstream bytes, since the licence does not yet allow reuse), and ran what we could:

- `check.py` passes on Linux here (CPython 3.12.3, SymPy 1.14.0, Node 22; levels 0–2, 7,118 files, 22,013 pins, 41 checks, about 810 s).
- 34 capture rows and three of the 13 trees reproduce with your code; the same 34 rows were decided again by an implementation written here, and the root was isolated independently. Everything agreed.
- The statement's F, G, rectangle and side map are this project's H-255 chart exactly, and L sits below n = 17's verified ceiling by about 1.0 × 10⁻²².

Three reviews then read the proof, each prompted separately:

- [The first review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-12-kleddamag-n17-candidate.md) read the statement, the five steps and the fifteen premises, and the three hardest places in detail (the class-row lemma, the root admission, and the hand-overs into the rigidity theorem).
- [The second review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-13-overbeck-n17-candidate-second.md) re-derived the normalized 52-row gate of `G20S_PHYSICAL` with its own code.
- [The third, a mathematical-correctness review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-13-overbeck-n17-mathematical-correctness.md), recomputed the root and the twenty decimals of L, the packing at side exactly L (every clearance, the 29 flush contacts and 22 tangencies by exact ideal membership), every literal geometric fact of §§3–6, the case partition, the admission of all eleven roots and the hand-overs of §8. It also checked the whole tree certificate `JQ` with a checker of its own, which reproduces the stored lower bound of the zero step exactly.

None found a false step or a blocking defect, and all three accept the proof as far as they read. What none of them did is rerun the 98 capture rows and the other twelve trees; those rest on your two checkers, whose acceptance rules the reviews found sound as specified. The result is registered as [T-153](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), under your name, as the first report of s(17) = L, at `V0`/`C1` (reported and read). n = 17 is recorded as reported proved, and the verified bounds move only on a complete replay.

**Questions and suggestions**, grouped, for a later version. None is blocking.

Admission (§7):

1. Could the admission geometry be written out in `PROOF.md` P073–P080 or a record bound to `ROOT_ADMISSION`, so that `adm.py` checks a text? That means the wall lemma, now only in the comment at `run_adm.py` lines 17–18; the lift rule ("some quarter-turn lift of the whole slot inside the root arc"); the label-12 cut at ρ with its precondition `a_lo > −ρ`; and a statement that the eleven root regions' direction specifications are the images of the class gates under those lifts, for the free-direction labels 3, 4, 15 and 17 in particular. The reviews re-derived all of it and found it correct. [K-Q4, SR-8, MR-1, MR-Q1]
2. The admission output records no margins, and the smallest is exactly 0 (label 1, every root), which is sound because gates and arcs are both closed. Printing every margin, and saying in the text that containment is of closed sets in closed sets, would make that visible. [MR-3]
3. Which file records the 136-pair separation of the eight off-wall profiles that P044 imports? Adding it to the public checks would close it. [SR-Q5, SR-8]

Rigidity (§8):

4. P110 needs the 52 normalized rows to be necessary for every 0 < R ≤ 1/5000, not only at the entry radius. `continuation/THEOREM.md` lines 87–89 states this; could P110 say so and cite it, together with the B6 prefix and the root-scale stop theorem (b ≥ −17/50000, b + z ≤ 3/125, z ≤ 1/40) by label? The edition's only text of the all-scale division also describes an earlier slider box and should be restated for the final domain. [K-Q2, MR-2, MR-Q2, SR-3, SR-Q3]
5. Does that proof cover the 152 separating alternatives individually, so that each pair's two retained alternatives are the only ones possible on the padded entry? [MR-Q2]
6. Which route is the one of record for `G20S_PHYSICAL`? `THEOREM_G20S.md` and the obligation's evidence still bind the box-wide route (eight rounds, ratio 0.859), which `PROOF.md` does not use. Could the two window trees `G20S` and `HW` also be listed as obligations of their own, with the `LOCAL_CERTIFICATE_IMPORT` dependency added? [K-Q3, SR-4, SR-9]
7. At P086, could the text say that the enlargement of the container from [0, L]² to [0, R]² applies to the eleven root trees only, and that the window trees run at S = L with S_floor = 4? Both facts are there, in P086 and P094. [MR-Q4]
8. Will a later version carry an independent builder of the normalized 244-row model, and a derivation of the finite second-order rows written independently of `uniform.py`? The continuation's independent check builds its rows with `import rigidity as kernel`, and the seventeen finite rounds' second builder mirrors the producer's formulas. The second review's row builder is one you are welcome to use. [SR-1, SR-Q1, SR-5, SR-Q6]

Files and bindings:

9. Where are the independent gate review's `check.py`, `bind.py`, `receipt.json` and `binding-receipt.json`, and which byte count of its `REVIEW.md` is right (7,817 in the manifest, 7,744 carried, same SHA-256)? [SR-2, SR-Q2]
10. `LABELS.tsv` binds `file:SELECTED_CLAUSES` to the `current-author-20261012i` copy and `file:C12_PROFILE_CAPACITY` into `public-edition-BK-20261011/revision-v4/`. Are the copies byte-identical, and is that binding intended? [K-Q1]
11. Where are the literal C7 and C8 target polygons bound, so that a reader can check the 19879/5000 and 647/125 containment from a carried file? [K-Q6]

Numbers and text:

12. P090 says 93 option splits of `JPA_v5`, and the stored report says 135; `KNOWN_ISSUES.md` gives `JG` 113 or 110 nodes. Which numbers are of record? [K-Q7, MR-7]
13. P057's upper quarter-turn gap, 974949/14197000000, is measured in the chart lifted by −π/2. In the gate's own chart it is 974949/14088170000. Both are positive; naming the chart would help. [MR-4]
14. `SPEC_v3.0.md` §11 names the terminal instance `box-relaxed`, which the proof does not use; the proof uses P095's sixteen-square entry. [MR-5]
15. `review-repair-O/F1_PROOF.md` line 5: reconcile "high-first" with the minimum score, or say that the two coincide when the low classes are empty. [K-Q5]
16. Were the `JQ` lists of options for the 33 undecided pairs produced by the same exclusion test the checker runs, or by a floating-point audit? (Soundness is unaffected, since the checker tests the precondition.) [MR-Q3]

Capture and tooling:

17. The public capture check takes `budget_units` from each certificate without recomputing capacities, and the surpluses are 0.5 to 23 units on budgets near 1.7 × 10¹⁰. All 98 budgets recomputed here match. Recomputing them in `check.py` would cost seconds. Were the certificates tuned to those surpluses on purpose, and does any depend on a boundary convention that the class-row lemma's limit argument does not cover? [SR-6, SR-Q4]
18. `recompute_slice.py` reports `SLICE RESULT: EQUAL` for a stored Node slice made with other checker bytes. Counting a checker-hash mismatch as a difference would close that. [SR-7]

Outside review and retention:

19. Could Guzhou0806's checker and his report on `JQ` and `JPG15p_v5` be published, or could this project obtain them? They are the only tree decisions by code written outside your project. [K-Q11]
20. Would you publish the RFC 3161 timestamps and the git objects of the sealed record, so that a reader can check the capture computation's comparison records? [K-Q10]
21. Is a licence that permits retaining the proof text and class files planned? We retain digests, receipts and derived exact facts only, which the current terms allow. [K-Q9]

The cheapest outside check that would close most of the remaining distance is a replay of the two window trees `G20S` and `HW` and one capture row with a checker not derived from yours. That is on our list, subject to budget.
