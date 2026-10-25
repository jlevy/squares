---
type: is
id: is-01m5raz24s6yh4tg8dsytsak84
title: "PR #800 (merge): senior review A of the 43f666c import and #763's recipe rows"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-24-rows-above-1024.md
delegate: c-rev-800-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5pjxq31vpw03t0emgwnvhfe
hold: null
hold_until: null
created_at: 2026-10-25T01:31:54.392Z
updated_at: 2026-10-25T01:55:34.876Z
started_at: 2026-10-25T01:32:00.361Z
closed_at: 2026-10-25T01:55:34.876Z
close_reason: "Review A of #800 posted (issuecomment-6392173409): approve once A1 has a disposition; 1 Medium, 6 Low, 1 suggestion; addressed by c-import-gn29-1024."
resolution: null
duplicate_of: null
---
Review A (senior, round 1) of https://github.com/jlevy/squares/pull/800 at 41dd6da7e (base 755ef426b): 122 rows (106 certificates, 16 recipes) from 43f666c, #763's 13 recipes decided by W7's checker and recorded, 127 supersessions, 367 and 690 not recorded.

## Notes

2026-10-25 c-rev-800-1024 (senior reviewer, strong tier; coordinator coord-intake-1024). Review A (senior, round 1) of PR #800 published as a PR comment at head 41dd6da7e, base 755ef426b: https://github.com/jlevy/squares/pull/800#issuecomment-6392173409
Verdict: approve once A1 has a disposition. 0 Blocker, 0 High, 1 Medium, 6 Low, 1 suggestion.
- A1 Medium: the 13 #763 recipe rows join couzo-issue763-2026-10-23, landed 2026-10-24 (landings.yaml:271); Recently Added dates them a day early; stamp_landed.py:208 and overview_sections.py:1563 assume a source's rows land in one merge. Rows also carry bead think-ptkk, not think-g2qy.
- A2 Low: plan :341/:200 say frozen walks keep RECIPE holds / ISSUE_763 unchanged.
- A3 Low: D2 text ("no certificate file of its own") vs the 29 recipes' parents/ expansions (all 29 matched in parents/manifest.json at 1c17153); #795 A2 precedent differs; record the rule.
- A4 Low: "credit and seed credit agree at every row" true at 106, not 122 (recipes have no seed_credit).
- A5 Low: earlier_issue/earlier_push generic in shape, #763-specific in content.
- A6 Low: RECIPES_763 unused; tautological test.
- A7 Low: PR body omits the ledger's owner items (29 first-commit-before-report, 133 publication-dependent).
- A8 suggestion: unit test recipe_first_commits on a temp git repo.
Independently re-derived: 957/126/831 and 108/1/17; 122 rows + 690, 797/847 restate, 367 above (3.827e-12); exact margins at 330 367 377 412 444 459 487 632 683 690 691 733 737 792 797 845 847 997; 127 + 7 supersessions; 11 recipes decided by own Fraction checker; all 108 retained certificates feasible; recipe dating (efef7d1 365/970, 964ee2b others, 43f666c all 17); blobs first at 43f666c; push times via activity API. Scratch: scratchpad/rev-800/.
