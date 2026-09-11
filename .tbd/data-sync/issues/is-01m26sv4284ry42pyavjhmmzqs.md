---
type: is
id: is-01m26sv4284ry42pyavjhmmzqs
title: Clarify T-026 as a proved lower bound across the explainer and reader docs
kind: task
status: in_progress
priority: 1
version: 4
labels: []
dependencies: []
child_order_hints:
  - is-01m27258dy9wympsk083fspbm0
created_at: 2026-09-10T23:18:28.662Z
updated_at: 2026-09-11T01:43:49.436Z
---
Revise PR148 after the merged n=11 stack so the headline states s(11) >= 3.826447410572939744... directly, replaces misleading 'weak limit' theorem language with dilation-limit proof terminology, and explains the result's V4/C4 evidence status consistently in the explainer, tutorial, README, synopsis, and result register. Regenerate derived views and pass local and hosted validation before merge readiness.

## Notes

PR #148 now states the exact theorem first, retains the complete T-018 worked assurance example, derives T-025 and T-026 directly, and reconciles V4/C4 terminology across reader docs. Final editorial requests are implemented at local head 916833c5: one-line title block with no subtitle, exact bound named L instead of L-star, top edition label linked to Version History at the end, and concrete threshold-atom prose replacing abstract charge/load-bearing language in progress. Focused explainer suite passes 58 tests; canonical render/check passes; default-browser preview opened. Previous hosted Pages build failed its math-face metric check on the newly introduced displayed exact theorem; this is the remaining tracked blocker, now being reproduced and fixed before push. Required pre-push gate is running.
