---
type: is
id: is-01m3wx2hm1ezys1w50g5pk9eet
title: One rescoring pass over the 23 draft significance scores of imported results, by an independent review lane
kind: task
status: open
priority: 2
version: 7
delegate: null
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-01T23:33:56.992Z
updated_at: 2026-10-23T15:10:30.581Z
started_at: 2026-10-11T21:02:23.101Z
---
W2. T-037..T-055, T-056, T-057, T-061 and T-065 carry draft scores set by the registering lane. The process review lists pairs the rationales do not explain: T-062 (S3) vs T-051..T-053 (S4); T-061 (S2) vs T-022 (S5); T-065 (S3) vs T-011 (S2); T-063 (S1) vs T-016 (S3); T-044/T-046/T-056 (S3) vs T-019/T-020 (S4). Apply the three scoring rules of epistemics.md, record by as the review, and move the working rules now buried in rationales (T-020, T-042, T-015/T-032 precedents) into epistemics.md if the owner wants them as policy.

## Notes

2026-10-11, lane S of the intake pass (worktree branch worktree-agent-af3c94f7d89d86292, commit ca1439fca): the rescoring pass is done. Every draft `significance.by` (48 entries: T-037..T-055, T-056, T-057, T-058, T-059, T-061, T-064, T-065, T-068, T-070, T-073..T-079, T-081, T-087, T-117..T-127) now names docs/project/reviews/review-2026-10-11-significance-scores.md, with a rationale that states the comparison and scored 2026-10-11. Three scores changed: T-053 S4->S3 (third instance of T-052's technique; one score with T-062, T-066, T-067; the family is T-081's S4), T-063 S1->S3 (a corollary scores the claim it states, as T-002 and T-016 do), T-065 S3->S2 (an exact certificate of a reported packing, as T-011, T-098, T-101). T-062 rewritten at S3 to close the pair its 2 October review left here. The five pairs in this bead's description are resolved in the review's "The Five Pairs" table; the consistency pass over T-001..T-146 lists every remaining same-kind pair and its explanation (two residuals for the owner: T-023 vs T-031; T-088/T-089 on the kind side of the upper-bound line). The working rules (T-020 calibration, T-015/T-032 precedent, T-042 step rule, the upper-bound line, corollaries, families) are collected as one proposed paragraph under "Proposed for epistemics.md" in the review; epistemics.md itself was not edited, that is the owner's call. The three `by: issue #227 intake` truncations (think-nr59) are gone with this pass. RESULTS.md re-rendered (three rows). Checks from packing/: check_results, validate_schemas, check_rung_figures, check_prose_ceremony pass; packing-validate --records fails only on the two synopsis steps (document map stale; the glance rows for T-053, T-063, T-065 stale), which render_results_headline and the records lane's SYNOPSIS pass fix at the merge. Not pushed, no PR.

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): the proposed epistemics.md paragraph and the three residual pairs (T-023/T-031, T-088/T-089, T-152 vs T-150/T-088) are owner decisions on https://github.com/jlevy/squares/issues/543. Tracker https://github.com/jlevy/squares/issues/544.

2026-10-23 coord-intake-1023: asked the owner (in conversation) whether padding refinements below the record's printed precision are S1 or S2; the owner answered 'no preference'. The record keeps the line the 14 and 16 October reviews drew and #749 confirmed (S1 below printed precision); no entry moves. Left open for a future owner word.
