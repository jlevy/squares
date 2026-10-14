---
type: is
id: is-01m4wcqv1wqhza9mbt42tvpkap
title: Simplify poster regularization credit and keep every n label gray
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4w9w2vc4p0j983wvvx8pybw
hold: null
hold_until: null
created_at: 2026-10-14T05:04:10.811Z
updated_at: 2026-10-14T07:21:25.542Z
started_at: 2026-10-14T05:11:36.430Z
closed_at: 2026-10-14T07:21:25.542Z
close_reason: Fixed, independently reviewed, and merged in regularization stack main9f48ccc80cee8dcf94c7cadbcaded01408f94fa2; exact-head Packing and Pages CI pass. Deployment tracked by parent think-azzv.
resolution: null
duplicate_of: null
---
User reviewed redrawn PDFs: replace granular regularized-count/tool credit with: Drawn packings are regularized for cleaner display using Squares Project rules, based on Daniel’s regularizer. Across both infographic PDFs and the web view, every large n number below a packing uses standard gray; red is reserved for the changed bound value, not n labels or s(n) prefixes. Regenerate both poster/export sets and verify web/print regression coverage.
