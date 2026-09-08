---
type: is
id: is-01m1ywjmdsmsjnxqbhd56er89j
title: Make Figure 5 formulas readable and controls clear
kind: bug
status: closed
priority: 1
version: 14
labels: []
dependencies: []
child_order_hints:
  - is-01m1yx70n68sarqckv3fqp9703
  - is-01m1yx70zbwfc3t6tfmjvp0rdh
  - is-01m1yxe8xmb8dp46wbgt4029nj
  - is-01m1yxysgf8x6nt839d27h0x4x
  - is-01m1yyjbrn5rm0ckr3243smmet
  - is-01m1yzd0n91ataqxvk8fbpdg7w
created_at: 2026-09-07T21:32:20.791Z
updated_at: 2026-09-07T22:34:53.160Z
closed_at: 2026-09-07T22:34:53.160Z
close_reason: Completed in PR117 at f4e4bd4a. All 45 local pre-push steps and all required hosted checks passed, including the paper build. Independent review accepted the changes; browser and PDF previews were regenerated, inspected, and reopened.
resolution: null
duplicate_of: null
---
W8 presentation edit with W7 interface repair as needed. Review full-size fractions, line wrapping, and every Figure5 control; stack panel below graphic at all widths per user; validate browser behavior and print; branch and PR fixes. Three independent audits cover semantics, typography, and regression coverage.

## Notes

Completed in PR117 at f4e4bd4afcd3df43f1dde8cf362a6218b45ca265. All required hosted checks passed (run 34166910598), and the hosted paper build passed (run 34166910543). Final local pre-push validation passed all 45 selected steps in 304.97 seconds; 43 explainer tests passed in 5.75 seconds. Independent code, mathematics, and timing-provenance reviews accepted. Figure 5 has full-size fractions, whole formula wrapping, below-graphic controls, precise actions, current shading, and a tilted left-side opening pose; both figures have tested tap/drag/keyboard rotation handles. The 23-year wording, T-022 parenthesis, revised opening sentence, and sourced verifier-timing footnote are included. Browser and final 15-page PDF reopened and visually checked. PR112 and PR115 prior deployments verified (26 live checks); this branch awaits PR117 merge.
