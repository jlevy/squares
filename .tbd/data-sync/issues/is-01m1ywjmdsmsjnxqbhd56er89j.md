---
type: is
id: is-01m1ywjmdsmsjnxqbhd56er89j
title: Make Figure 5 formulas readable and controls clear
kind: bug
status: in_progress
priority: 1
version: 9
labels: []
dependencies: []
child_order_hints:
  - is-01m1yx70n68sarqckv3fqp9703
  - is-01m1yx70zbwfc3t6tfmjvp0rdh
  - is-01m1yxe8xmb8dp46wbgt4029nj
  - is-01m1yxysgf8x6nt839d27h0x4x
  - is-01m1yyjbrn5rm0ckr3243smmet
created_at: 2026-09-07T21:32:20.791Z
updated_at: 2026-09-07T22:07:09.075Z
---
W8 presentation edit with W7 interface repair as needed. Review full-size fractions, line wrapping, and every Figure5 control; stack panel below graphic at all widths per user; validate browser behavior and print; branch and PR fixes. Three independent audits cover semantics, typography, and regression coverage.

## Notes

All improvements are committed as 330b1abdc101b559da337325ed52fd50bc21bdba on codex/figure-5-controls and pushed to PR117: https://github.com/jlevy/squares/pull/117. Final pre-push validation passed all 45 steps in 213.16 seconds. Combined browser/layout/touch check passed in 18.24 seconds; 27 checker tests and 43 explainer tests passed. Independent math and code review accepted. PDF and desktop view inspected; final preview rebuilt at the committed revision. Hosted CI is running. Children track mobile handles, 23-year wording, initial pose, and verified deployment.
