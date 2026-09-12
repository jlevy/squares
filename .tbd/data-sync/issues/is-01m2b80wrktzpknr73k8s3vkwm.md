---
type: is
id: is-01m2b80wrktzpknr73k8s3vkwm
title: The difficulty gradient claim did not survive; n=26 works and n=17 is confounded
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies: []
created_at: 2026-09-12T16:43:15.602Z
updated_at: 2026-09-12T16:43:15.602Z
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
