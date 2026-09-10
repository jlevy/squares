---
type: is
id: is-01m24pyxdsrz809h9cp4bwtcmc
title: "PR139 R1: validate the corrected combined head with the full checkpoint"
kind: task
status: in_progress
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
labels: []
dependencies:
  - type: blocks
    target: is-01m24nswnk9b76cq0hdgenfceq
parent_id: is-01m24nswnk9b76cq0hdgenfceq
created_at: 2026-09-10T03:49:38.352Z
updated_at: 2026-09-10T07:20:54.670Z
---
Fast34433755569 passed at58ee1782; deferred34433755622 skipped substantive lanes. After corrections freeze, run one full checkpoint, verify checkoutSHA/base/headparents and constituent results, and link evidence to PR139. PR147 full34430565799 already passed and must not be rerun. ReviewR1: https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994

## Notes

Integrated PR139 commit 0c4c41b40a6200918b5954a07ccf9647dc8bca5c is published. Corrected pre-push run f45ce8f9608d4f6e9e5ccb9399b4ee5e passed all 45 selected steps in 733.33 s, including 4923 non-exhaustive tests. The preceding run failed atlas collection only because DYLD_FALLBACK_LIBRARY_PATH was omitted; corrected run uses /opt/homebrew/lib with unchanged source. Neither timing is a reference-shape baseline. Current fast CI is 34449286919; deferred checkpoint 34449352932 was dispatched from the PR head branch definition and is running. The automatic unlabelled deferred run 34449286923 skipped and is not evidence. Watch logs: /private/tmp/pr139-0c4-pr-checks-watch.log and /private/tmp/pr139-0c4-deferred-watch.log. Bind actual checked-out merge parents and the full 73-step union before marking ready and merging.
