---
type: is
id: is-01m24pyxdsrz809h9cp4bwtcmc
title: "PR139 R1: validate the corrected combined head with the full checkpoint"
kind: task
status: in_progress
priority: 1
version: 11
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
labels: []
dependencies:
  - type: blocks
    target: is-01m24nswnk9b76cq0hdgenfceq
parent_id: is-01m24nswnk9b76cq0hdgenfceq
created_at: 2026-09-10T03:49:38.352Z
updated_at: 2026-09-10T07:40:03.966Z
---
Fast34433755569 passed at58ee1782; deferred34433755622 skipped substantive lanes. After corrections freeze, run one full checkpoint, verify checkoutSHA/base/headparents and constituent results, and link evidence to PR139. PR147 full34430565799 already passed and must not be rerun. ReviewR1: https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994

## Notes

At published head0c4c41b40a6200918b5954a07ccf9647dc8bca5c, independent Sol audit confirms all62 fast receipts passed with actual clean synthetic checkout9e6a40f7629b46a8cece64bcd2346e0632b3c7b9, merging head into main1c1db463447cb08f8987d3355ba32a1c72ccd31a. Quick JUnit4823 tests, zero failures/errors/skips; certificate-page34449286960 passed same merge. Deferred34449352932 slow lane passed100 tests in858.98s; numeric, exhaustive and screen remain pending. Source list is73, fast62 plus full11, and the dispatched head-branch workflow names exactly those11 deferred checks. Audit retained under /private/tmp/pr139-0c4-ci-admission/; final report pending. The earlier local45-step push check passed4923 non-exhaustive tests in733.33s after correcting documented Cairo environment; it does not replace remaining full coverage. Automatic skipped34449286923 is not evidence. Final merge remains gated.
