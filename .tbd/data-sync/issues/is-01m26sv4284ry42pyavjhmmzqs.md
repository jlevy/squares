---
type: is
id: is-01m26sv4284ry42pyavjhmmzqs
title: Clarify T-026 as a proved lower bound across the explainer and reader docs
kind: task
status: in_progress
priority: 1
version: 7
labels: []
dependencies: []
child_order_hints:
  - is-01m27258dy9wympsk083fspbm0
  - is-01m2729rgwe9tf9kk6m8hv5242
  - is-01m27341tgrm865t7htkcacdf5
created_at: 2026-09-10T23:18:28.662Z
updated_at: 2026-09-11T02:00:38.479Z
---
Revise PR148 after the merged n=11 stack so the headline states s(11) >= 3.826447410572939744... directly, replaces misleading 'weak limit' theorem language with dilation-limit proof terminology, and explains the result's V4/C4 evidence status consistently in the explainer, tutorial, README, synopsis, and result register. Regenerate derived views and pass local and hosted validation before merge readiness.

## Notes

PR #148 states the exact theorem first, retains the complete T-018 worked assurance example, derives T-025 and T-026 directly, and reconciles V4/C4 terminology across reader docs. Final editorial requests are implemented locally: one-line title block with no subtitle, exact bound named L, the top edition links to Version History at the end, GPT 5.6 Sol/GPT-6 Astra credits, seven-place public decimals, and concrete threshold-atom prose. The Pages failure is isolated to check_math_faces.py re-rendering a displayed formula with KaTeX's inline default. Preserving displayMode makes the exact theorem agree under serif/sans and screen/print: the live check reports zero findings; the checker self-test and 86 focused explainer/math-loading tests pass. The acknowledgment target exists in the stamped commit; think-sqa3 remains open until a pushed-head GitHub URL is verified. T-025/T-026 standalone claim-document implementation is in flight under think-yb21.
