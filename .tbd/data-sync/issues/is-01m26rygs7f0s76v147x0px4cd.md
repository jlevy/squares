---
type: is
id: is-01m26rygs7f0s76v147x0px4cd
title: Reconcile PR149 onto the current v0.4.0 explainer stack and restore CI
kind: task
status: in_progress
priority: 1
version: 2
delegate: root integration lane
labels: []
dependencies: []
created_at: 2026-09-10T23:02:51.417Z
updated_at: 2026-09-10T23:02:57.100Z
---
PR #149's page-render diagnostic work is currently red only because it predates the session-099 terminal repair in PR #150, and it also modifies the same explainer/PDF surface now advanced by PR #148. Reconcile it onto the current v0.4.0 explainer head, resolve the page-count and generated-artifact context rather than carrying a 17-page assumption, run focused PDF/page tests and the required pre-push gate, push the author branch, retarget it as a clean stack layer above PR #148, update its cost/validation/body, and require all hosted checks to pass. Preserve D-490's measured host-specific evidence and do not claim the underlying nondeterminism cause is solved.
