---
type: is
id: is-01m24pyxdsrz809h9cp4bwtcmc
title: "PR139 R1: validate the corrected combined head with the full checkpoint"
kind: task
status: in_progress
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
labels: []
dependencies:
  - type: blocks
    target: is-01m24nswnk9b76cq0hdgenfceq
parent_id: is-01m24nswnk9b76cq0hdgenfceq
created_at: 2026-09-10T03:49:38.352Z
updated_at: 2026-09-10T07:00:39.476Z
---
Fast34433755569 passed at58ee1782; deferred34433755622 skipped substantive lanes. After corrections freeze, run one full checkpoint, verify checkoutSHA/base/headparents and constituent results, and link evidence to PR139. PR147 full34430565799 already passed and must not be rerun. ReviewR1: https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994

## Notes

The integrated working tree now includes all A6 numerical admissions, H157 corrections and the retained three-block plan. Final pre-push validation started at 2026-09-10T06:53:29Z against 6ed45816 with jobs 1 and inner_jobs 2; log /private/tmp/pr139-final-source-push.log and artifacts /private/tmp/pr139-final-source-push-artifacts/. The reachable-test process is actually using 10 workers, as recorded in its command receipt; do not infer its shape from the inner_jobs field. Prior d21 full coverage and the preparatory 44-step edit pass remain distinct. After the push, dispatch the PR head branch workflow and verify the actual head/base/merge checkout and full 73-step union before readiness and merge.
