---
type: is
id: is-01m41erq0xx42rk5eft3hm207w
title: Audit and communicate every gap or error found in results reported by others (Evan Daniel, wand125, squarepacker, Queuingtheorydotcom, Nagamochi, Green, …)
kind: task
status: closed
priority: 1
version: 3
labels:
  - issues
dependencies: []
parent_id: is-01m41csdc2gp36ry5p6n7c2x2y
created_at: 2026-10-03T18:00:06.941Z
updated_at: 2026-10-03T18:49:16.167Z
closed_at: 2026-10-03T18:49:16.167Z
close_reason: null
resolution: null
duplicate_of: null
---
Owner 2026-10-03: summarize clearly whether any gaps or errors were identified in results reported by others, including Evan Daniel, and make sure those are commented on the issues. Strong-tier lane drafting scratchpad/gaps-errors-audit.md (classified E claim error / G proof gap / T tool defect / R reproducibility / N note, sourced) and one draft comment per issue with an @-mention. Coordinator reviews and posts; links to main paths, so post right after #292 lands.

## Notes

2026-10-03 18:40 Audit done (scratchpad/gaps-errors-audit.md, 9 drafts). Errors: Nagamochi Lemma 1 false (T-007, 242 case records cite it, 49 marked proved; PR #305 re-grounds, owner decision); Green DS7 Thm 9 (not unavoidable for k>=4 and k=2); wand125 T-058 ceiling (64/100 rows, corrected upstream, told on #246); wand125 comparison margins at n=83-87 slightly overstated (no bound affected). Gaps: Nagamochi Thms 1-2; Daniel's single-implementation premises (Valid7 now replayed + Lean built; ValidTilt9 not yet); Queuingtheorydotcom write-up (charge lemma omitted, two invariants too weak; checkers right, T-060 stands); Kleddamag/Guzhou0806 unargued prose steps (discharged here). Evan Daniel: no claim error. Final replies (disposition + findings + tag) being composed into scratchpad/final-replies/. Note: PR #305 assigns T-066..T-070 to other results; renumber at merge.
