---
type: is
id: is-01m2b80wrktzpknr73k8s3vkwm
title: Reconcile annealing difficulty claims with retained per-cell evidence
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
created_at: 2026-09-12T16:43:15.602Z
updated_at: 2026-09-13T04:52:34.585Z
---
X-028 §3a closes with: "there is a difficulty gradient after all, and it runs opposite to §2's: the search works where there are few squares and fails where there are many." Re-reading the same data by disjoint blocks, that is not what it says.

| n | gap to the grid | best-of-1000, blocks clearing the grid | verdict |
| ---: | ---: | ---: | --- |
| 5 | 10.82% | 34/39 | works |
| 10 | 7.90% | 5/5 | works |
| 11 | 3.17% | 1/5 at shake 6, 13/16 at shake 8 | parameter-dependent |
| 17 | 6.94% | 0/5 | fails |
| 26 | 6.74% | 5/5 | **works, and it is the largest n measured** |
| 29 | 1.12% | 0/5 | fails |

n = 26 clears the grid in every block of a thousand and is bigger than both instances the campaign calls hard. Size is not the variable.

What the three failures share is not their n. **n = 11 and n = 29 have the two smallest gaps in the set** -- 3.17% and 1.12% -- so there is almost no room between the record and the trivial grid, and `closed` is a harsh scale there: at n = 29 the whole gap is 0.066 of a side. n = 17's gap is ordinary at 6.94%, which leaves it genuinely unexplained.

**And n = 17 is confounded.** It has only ever been run at shake 6, the level at which n = 11 also fails and at which n = 11 turns around when moved to 8. Nothing has measured n = 17 at the level where the method starts working. Until that run exists, "the search fails at n = 17" is a statement about one parameter setting.

Two repairs, one cheap and one editorial:
- run n = 17, 26 and 29 at shake 8 and 10, which is minutes;
- correct §3a in place -- annotate, do not rewrite -- to say the gradient claim did not survive the block analysis.

## Notes

2026-09-12 review correction: the prior note that n17 only ran at shake6 is false; summaries contain n17 shake8 inflate cells but all are unresolved. exp-208 declares deeper resolved runs not substantiated by the retained per-cell summaries. Resolve commands vs completed runs, sample counts and guard versions before a dated X-028 annotation. Do not present the pasted disjoint-block numbers as independently verified; raw trials are absent. Existing claim that n26 is largest measured is also inaccurate (n29 exists). Keep gap-normalized and absolute excess side by side and avoid a causal size claim.
