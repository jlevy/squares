---
type: is
id: is-01m4mngjp5bgapdhqt3nt33ge4
title: "Size the --push behavioral cap for narrow selections that approach the whole suite (PR #496 F3)"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T05:03:34.596Z
updated_at: 2026-10-12T23:38:57.728Z
closed_at: 2026-10-12T23:38:57.728Z
close_reason: "Duplicate of think-ri5z (PR #496 review F3), which PR #507 and the website development-loop plan name as the owner."
resolution: duplicate
duplicate_of: is-01m4mth1gzbfvd0qzhfbexx891
---
Deferred from PR #496 review F, finding F3 (Low, pre-existing): https://github.com/jlevy/squares/pull/496#pullrequestreview-5481911429
packing/src/sqpack/cli/validate.py:5891 gives any narrow reachable-test selection the shared 900 s FAST_SUITE_BUDGET_SECONDS cap, while the whole-suite fallback gets 1,800 s.
F3's measurements at PR #496 head aca9a0784: the 12-path change selects 555 of 742 test files; .github/workflows/pages.yml alone selects 554 (the one-line timeout-minutes edit pulls in every Pages workflow input); each other single path selects 111 to 137; the earlier ten-path snapshot selected 155, and that 155-file --push run timed out at the 900 s cap (1,275.28 s total wall). Base and head select the same files for the same paths; selection and the cap are unchanged by PR #496.
Decide, with a measurement, whether a narrow selection above some fraction of the suite takes the whole-suite budget, or a budget scaled by the selected fraction. Review C's 'do not increase the unchanged 900-second guard' applied to PR #496 only. Related: think-oe1g (comment-only workflow edits select the whole suite).
Waits on: a measured per-file cost model for the reachable selection (think-ht59 scope), not on PR #496.
