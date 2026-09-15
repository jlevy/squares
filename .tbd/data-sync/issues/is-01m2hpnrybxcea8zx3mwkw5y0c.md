---
type: is
id: is-01m2hpnrybxcea8zx3mwkw5y0c
title: Generate or commit-stamp the counts documents copy by hand
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-15T04:54:46.474Z
updated_at: 2026-09-15T04:54:46.474Z
---
From the PR #125 review (`attic/reviews/pr125-review-7b06254c.md`, pinned `7b06254c`), non-blocking suggestion 6, "Hand-copied numbers": nearly every hand-copied number the review checked in READMEs, plans and the PR body had drifted (findings 27, 28, 31, 39). Generate them, or stamp each with the commit it was measured at.

The review round fixed the instances, not the class:

- dropped the count: `development.md`'s gate step count (6eb6a3df, D27) and README's two report counts (4b930870, D76);
- corrected it: TUTORIAL's strategy count (4b930870);
- stamped it: the spike README's sizes, stamped at `f3874426` (9baad048, D58).

The same drift has its own closed beads before this: think-aihj (copied no-regression count in SYNOPSIS), think-4b9m (gate step count), think-ojgc (SYNOPSIS rounds column), think-9muq and think-d3rx (this review). `packing/devtools/check_readme.py` already refuses numeric aggregates in README that `defects.yaml` owns, and `check_synopsis.py` reconciles SYNOPSIS; plans, package and spike READMEs, TUTORIAL and PR bodies have no such check.

Work: write the rule down (a count in prose is either rendered from its owner, checked by a drift check, or carries the commit it was measured at), and extend the existing checkers to the documents that repeat counts most (plans' status lines, `packages/workbench/README.md`, TUTORIAL). A PR body cannot be checked in CI; the address-pr-review procedure can say to regenerate its counts.
