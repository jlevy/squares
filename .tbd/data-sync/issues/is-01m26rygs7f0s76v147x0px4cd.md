---
type: is
id: is-01m26rygs7f0s76v147x0px4cd
title: Reconcile PR149 onto the current v0.4.0 explainer stack and restore CI
kind: task
status: in_progress
priority: 1
version: 14
delegate: root integration lane
labels: []
dependencies: []
child_order_hints:
  - is-01m27m104h8xe13rsy1rn70r2k
  - is-01m27nzye5x8zqy5zhkmkeqy8s
  - is-01m2ad93c4a71sg21qx5jgcqpm
  - is-01m2ad9avdatjwfznq7zwqjget
created_at: 2026-09-10T23:02:51.417Z
updated_at: 2026-09-12T08:56:21.134Z
---
PR #149's page-render diagnostic work is currently red only because it predates the session-099 terminal repair in PR #150, and it also modifies the same explainer/PDF surface now advanced by PR #148. Reconcile it onto the current v0.4.0 explainer head, resolve the page-count and generated-artifact context rather than carrying a 17-page assumption, run focused PDF/page tests and the required pre-push gate, push the author branch, retarget it as a clean stack layer above PR #148, update its cost/validation/body, and require all hosted checks to pass. Preserve D-490's measured host-specific evidence and do not claim the underlying nondeterminism cause is solved.

## Notes

PR149 has two concurrent candidate fixes that must be combined without overwriting author work: remote b6a81495 ties exposure and exemptions to the same observation; local 88615a56 pauses the page root watchdog only during artificial geometry setup and proves the hook fired. Astra adjudication recommends both and rejects the former causal wording about carrier CSS and final glyph layout. Child think-6ogd owns integration and D-491 correction; dependent think-o96l owns fresh exact-head validation, push, hosted CI, full checkpoint, PR metadata, and bead sync. The local pre-push on 88615a56 is evidence for that pre-merge head only.
