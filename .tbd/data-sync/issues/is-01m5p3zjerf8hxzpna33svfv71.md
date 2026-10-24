---
type: is
id: is-01m5p3zjerf8hxzpna33svfv71
title: "Address PR #756 review B (B1-B4)"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-fix-756b-1024
labels: []
dependencies: []
parent_id: is-01m5nzjjyj7axr5vb1gvk4xwh9
hold: null
hold_until: null
created_at: 2026-10-24T04:51:22.200Z
updated_at: 2026-10-24T07:11:44.261Z
started_at: 2026-10-24T04:51:27.638Z
---

## Notes

2026-10-24 c-fix-756b-1024 (addressing review B of PR #756, https://github.com/jlevy/squares/pull/756#issuecomment-6379772274):
- Step 1 done. B1, B2 and B4 fixed in 891203621; re-pin 0a8435ccd; pushed 05:13Z. B3 fixed in the PR body. Dispositions posted: https://github.com/jlevy/squares/pull/756#issuecomment-6380267295 (marker review=B head=0a8435ccd2e609cdccc8bbb0fa7a6eefe4e1f5c1).
- B1: PR 574's algebraic certificates at 153 and 207 (T-174) are exact solves (`regularized_drawings.EXACT_SOLVES` now names counts per source; `exact_solve(by, n)`), and `case_note` refuses a source regularization at an owed count. Negative control first: the new tests failed before the fix, and `regularized_drawings --check` refused 153 on the committed records with the refusal in. Two case records regenerated; results.yaml unchanged.
- Deferred: think-xqpq (under think-ezt8), the vocabulary at T-174's 34 other houses and 12 houses of six other sources.
- Main moved (#745, #771, #750): merged origin/main 2c58b6373 at 5c12633e0 (conflicts site-urls.md and release.py only), re-pinned at 7399291de, pushed 05:23Z. Checks on the merge pass: site_urls (1396 rows), render_results, bound citations, composite figure, research tables, regularized_drawings, contributor_census --stale, select/adopt_houses, default_drawings --check and --check-state (56/228/29/7/4/0), flip_regularization, families, contact shades, check_release_impact, records tier (53 steps, 162 s, 2 jobs).
- Waiting: #757 to merge, then step 2 (merge, regenerate, check; expected 57/228/28/7/4/0) and step 3.
- Step 2 and 3 done. #757 landed (c5697c2f2): a trial merge of #757's head 21a0624cf (tree equal to main's after the merge) was resolved and checked first, then applied to the real merge 9e92fffd9 (tree a9c6df1aa, identical). 24 conflicts, resolved three ways or regenerated: ADOPTED 302 T-193 and 303 T-239; LATER_PASSES 2026-10-24 {204, 303}; SETTLED drops 303; SCREEN_FINDINGS (124, 1184, 302, 5110), reproduced by the screen at 303; index totals recomputed with atlas_totals; custody 70 houses, 200 inputs, 44 mutations. default_drawings: 57 / 228 / 28 / 7 owed / 4 / 0, as expected. 5eeedcf3e restored this branch's no-public-change records in release.py (the merge had taken #757's file whole); check_release_impact passes. 340 + 204 tests passed.
- Then merged #766 (5f8f005a3) at ecb953c89 and #769 (34eb8bb75) at daba8ac50, only the pin conflicting each time; all house and generator checks, stamp_landed --apply (nothing to stamp), check_release_impact and the records tier pass. Head 624926fdb pushed 07:02Z.
- Hosted green: 7399291de (Packing validation 40066058128), 5eeedcf3e (40069040138), dec383676 (40071590857). 624926fdb: run 40072590130 in progress at 07:11Z.
