---
type: is
id: is-01m25zrj5np9ywft00t8j8neaz
title: "N11 explainer: teach the T-025/T-026 lower-bound ladder"
kind: epic
status: open
priority: 1
version: 14
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
updated_at: 2026-09-10T19:46:38.010Z
---
Add a documentation block alongside the three scientific blocks to bring the public
explainer up to the merged T-025/T-026 result. The block is editorial and does not
consume or extend a scientific target budget. It belongs to the existing explainer
line under think-3od5 while this bead coordinates it with the post-PR139 overnight
session.

Begin with a source-bound complexity audit of the current Markdown article and
renderer. Decide prospectively between two architectures: retain the simple
weighted-point certificate as the teaching spine and add the threshold/dilation
extension, or rebuild the whole article around the tighter certificate. The decision
must compare the number of new concepts, figure and renderer changes, independent
verification surface, obsolete claims, and effect on the reader's proof arc.

The article must state the current result exactly: T-026 is the weak lower limit
955000*sqrt(518400042893309449)/179696714646249 =
3.826447410572939744..., with endpoint fit unresolved. T-025 is the exact excluded
endpoint 191/50 using point and two-of-three threshold atoms. The exact upper
construction remains 3.877083590022814.... Preserve the distinction between the
simple point-only certificate, the threshold certificate, and the dilation argument.
Do not turn A6, owner restrictions, or private overnight work into a theorem.

Apply Practical Prose, regenerate the explainer from its Markdown source, run its
focused tests and PDF/page checks, and obtain an independent mathematical/prose review
before readiness. If the overnight research changes the standing bound, update only
after its theorem and certificate gates pass. The exact V3 plan source remains pending
under think-i1fr, so this block must not claim V3 alignment.

## Notes

Architecture and implementation are complete on codex/n11-explainer-current-bound. Draft PR #148 is pushed at 35484ebd and titled “docs: publish the v0.4.0 n=11 lower-bound explainer.” It retains T-018 as the visual, first-principles spine; states T-025 at 191/50 and T-026 as the weak limit 3.826447410572939744… with the endpoint unresolved; defines the advanced terms before use; and adds the missing T-025/T-026 tutorial evidence row.

The v0.4.0 release metadata drives the current version, date, exactly two rendered history entries, atlas stamps, and generated claim stamps. History dates record the first Git commit carrying each label: v0.4.0 on September 10, 2026 at 35484ebd, and the 3.81-result v0.3.0 on September 8, 2026 at ce3b1ab5. All directly affected checks pass, including 135 focused tests, static analysis, prepared HTML/Markdown drift, deterministic 20-page PDF/font validation, and the complete 324-case atlas gate. Hosted checks are running. Retarget PR #148 from main to codex/n11-daytime-strategy after that branch is published, then require stacked hosted checks before readiness. No unmerged research claim is used by the explainer.
