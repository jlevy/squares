---
type: is
id: is-01m25zrj5np9ywft00t8j8neaz
title: "N11 explainer: teach the T-025/T-026 lower-bound ladder"
kind: epic
status: open
priority: 1
version: 18
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - explainer
dependencies: []
parent_id: is-01m24sm7wm3s5eh8ke6vze7mw1
child_order_hints:
  - is-01m25zs0w1ctenbb2c5wt9q06v
  - is-01m25zs0xky60mnw0q1fvb5bfz
  - is-01m25zs0ygtqsqfx233fhjrxqf
  - is-01m26b9kjzhrxhsw4dm5atkax2
created_at: 2026-09-10T15:42:41.844Z
updated_at: 2026-09-11T06:56:48.371Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
Publish the v0.4.0 explainer for the strongest proved n=11 lower bound. Keep T-018 at 3.81 as the fully auditable visual proof, then define threshold atoms and the dilation argument that give T-025 at 3.82 and T-026 at C = 955000*sqrt(518400042893309449)/179696714646249. State the theorem as the ordinary lower bound s(11) >= C at V4/C5. Apply Practical Prose, regenerate every format, reconcile current main, and require local and hosted checks.

## Notes

Reopened because the earlier closure called T-026 a weak limit and treated endpoint fit as unresolved. That wording was mathematically misleading. PR #148 now contains standalone T-025/T-026 claim packets, exhaustive replays, mapped source-distinct review, the direct theorem s(11) >= C at V4/C5, and current-main reconciliation. Final pushed-head CI and browser review remain.
