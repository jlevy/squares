---
type: is
id: is-01m25zrj5np9ywft00t8j8neaz
title: "N11 explainer: teach the T-025/T-026 lower-bound ladder"
kind: epic
status: open
priority: 1
version: 12
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - explainer
dependencies: []
parent_id: is-01m24sm7wm3s5eh8ke6vze7mw1
child_order_hints:
  - is-01m25zs0w1ctenbb2c5wt9q06v
  - is-01m25zs0xky60mnw0q1fvb5bfz
  - is-01m25zs0ygtqsqfx233fhjrxqf
created_at: 2026-09-10T15:42:41.844Z
updated_at: 2026-09-10T17:58:09.321Z
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

Architecture and implementation are complete on codex/n11-explainer-current-bound. PR #148 is at 277f8b1a. The independent mathematical and prose audit is complete under think-0zc1: T-018 remains the visual teaching spine; T-025 and T-026 are stated at their exact scopes; endpoint certificate, weak limit, core, trace, and charge are now defined; the rational-density step is written out; and the point-only generator section is scoped explicitly. Local validation passed: 70 focused tests, Ruff, BasedPyright, prepared-render replay, deterministic 20-page PDF, print layout and its self-check, and desktop/mobile typography checks. The PR is still based on main because codex/n11-daytime-strategy is not yet published remotely. Retarget PR #148 to that branch once it exists, then require hosted CI to pass before marking ready. No unmerged scientific claim is used by the explainer.
