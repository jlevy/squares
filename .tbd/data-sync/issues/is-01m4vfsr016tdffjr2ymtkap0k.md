---
type: is
id: is-01m4vfsr016tdffjr2ymtkap0k
title: Fable Max mathematical-correctness review of Overbeck's candidate, for sharing with the author
kind: task
status: open
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m4sce0tyvdb701rcxm7p6h4g
created_at: 2026-10-13T20:38:24.513Z
updated_at: 2026-10-14T02:11:31.924Z
---
Owner, 13 October: a strong Fable Max sub-agent for mathematical correctness on both n = 17 proofs, with full review docs to share back with the authors. Reviewer: tbd-strong-max on claude-fable-5-1, effort max, in /home/user/sq-math-overbeck; deliverable docs/project/reviews/review-2026-10-13-overbeck-n17-mathematical-correctness.md. Blind to the two earlier reviews until its findings are written; then compares.

## Notes

Done 14 October: docs/project/reviews/review-2026-10-13-overbeck-n17-mathematical-correctness.md (in /home/user/sq-math-overbeck, untracked; copy in the coordinator's scratchpad fable-reviews/). Verdict accepted; 3 minor findings, 4 notes, 4 questions for the author. Own code (scratchpad math-overbeck/): exact Krawczyk endpoint, Groebner ideal-membership proof of all 36 contacts of the upper construction, admission of all 11 roots, 194 literal checks over all 98 class files, an independent case partition, hand-overs, and the first independently implemented decision of a tree certificate (JQ, one-node checker; equals the stored zero_step_L exactly). Not reached: 98 capture rows, 12 trees, 17 finite rounds. Disclosure in its section 9: the second review's verdict sentence was seen before its own findings. Next: map into T-153, register its code with independence records (think-mlkx), draft the share-back to Overbeck with the T-153 questions (think-sdsl).

2026-10-14, writer lane on claude/stoic-clarke-jhfnru (local commits, not pushed): stored as docs/project/reviews/review-2026-10-13-overbeck-n17-mathematical-correctness.md, as written but for the reviewer line, which names the system family, tier and setting (a20a3e5af); listed in T-153 reviews with its section 9 disclosure in the reviewer text; T-153 stays V0/C1. Programs kept in the packet review-3/ (literal_checks.py: its eval of the source predicates replaced by a restricted parser at retention) and registered as V-overbeck-review3-* with the E-n017-overbeck-*-review3 entries; the second review's four gate programs registered as V-overbeck-review2-* with E-n017-overbeck-gate-review2 (f35ca0cbf, 2de5f92bf). Seven findings and four questions are for the author.
