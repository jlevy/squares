---
type: is
id: is-01m24pyxdsrz809h9cp4bwtcmc
title: "PR139 R1: validate the corrected combined head with the full checkpoint"
kind: task
status: closed
priority: 1
version: 13
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
labels: []
dependencies:
  - type: blocks
    target: is-01m24nswnk9b76cq0hdgenfceq
parent_id: is-01m24nswnk9b76cq0hdgenfceq
created_at: 2026-09-10T03:49:38.352Z
updated_at: 2026-09-10T08:09:29.875Z
closed_at: 2026-09-10T08:09:29.874Z
close_reason: All73 declared checks passed on the exact final combined tree; source identities, raw artifacts and test-lane union admitted.
resolution: null
duplicate_of: null
---
Fast34433755569 passed at58ee1782; deferred34433755622 skipped substantive lanes. After corrections freeze, run one full checkpoint, verify checkoutSHA/base/headparents and constituent results, and link evidence to PR139. PR147 full34430565799 already passed and must not be rerun. ReviewR1: https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994

## Notes

Final source 0c4c41b40a6200918b5954a07ccf9647dc8bca5c: fast34449286919 and deferred34449352932 pass all73 distinct declared steps on clean synthetic merge9e6a40f7629b46a8cece64bcd2346e0632b3c7b9, base1c1db463447cb08f8987d3355ba32a1c72ccd31a. Head and merge tree6842862342321038ff7437dcda9827feb2c9d102. Four additional macOS repeats counted separately. Quick4823 + slow100 + exhaustive55 =4978 tests, zero failures/errors/skips; screen318 records. Numeric8 passed2390.94s, aggregate success; source-name union exact, no missing/extra. Receipt /private/tmp/pr139-0c4-ci-admission.md final addendum. Existing local prepush45/45 also passed. No timing baseline changes. Ready for guarded merge of the same head/base.
