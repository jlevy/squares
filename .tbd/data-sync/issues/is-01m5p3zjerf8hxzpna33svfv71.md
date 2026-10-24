---
type: is
id: is-01m5p3zjerf8hxzpna33svfv71
title: "Address PR #756 review B (B1-B4)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-fix-756b-1024
labels: []
dependencies: []
parent_id: is-01m5nzjjyj7axr5vb1gvk4xwh9
hold: null
hold_until: null
created_at: 2026-10-24T04:51:22.200Z
updated_at: 2026-10-24T05:23:38.768Z
started_at: 2026-10-24T04:51:27.638Z
---

## Notes

2026-10-24 c-fix-756b-1024 (addressing review B of PR #756, https://github.com/jlevy/squares/pull/756#issuecomment-6379772274):
- Step 1 done. B1, B2 and B4 fixed in 891203621; re-pin 0a8435ccd; pushed 05:13Z. B3 fixed in the PR body. Dispositions posted: https://github.com/jlevy/squares/pull/756#issuecomment-6380267295 (marker review=B head=0a8435ccd2e609cdccc8bbb0fa7a6eefe4e1f5c1).
- B1: PR 574's algebraic certificates at 153 and 207 (T-174) are exact solves (`regularized_drawings.EXACT_SOLVES` now names counts per source; `exact_solve(by, n)`), and `case_note` refuses a source regularization at an owed count. Negative control first: the new tests failed before the fix, and `regularized_drawings --check` refused 153 on the committed records with the refusal in. Two case records regenerated; results.yaml unchanged.
- Deferred: think-xqpq (under think-ezt8), the vocabulary at T-174's 34 other houses and 12 houses of six other sources.
- Main moved (#745, #771, #750): merged origin/main 2c58b6373 at 5c12633e0 (conflicts site-urls.md and release.py only), re-pinned at 7399291de, pushed 05:23Z. Checks on the merge pass: site_urls (1396 rows), render_results, bound citations, composite figure, research tables, regularized_drawings, contributor_census --stale, select/adopt_houses, default_drawings --check and --check-state (56/228/29/7/4/0), flip_regularization, families, contact shades, check_release_impact, records tier (53 steps, 162 s, 2 jobs).
- Waiting: #757 to merge, then step 2 (merge, regenerate, check; expected 57/228/28/7/4/0) and step 3.
