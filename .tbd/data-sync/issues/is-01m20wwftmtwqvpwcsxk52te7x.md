---
type: is
id: is-01m20wwftmtwqvpwcsxk52te7x
title: Show the default certificate figures in the initial published HTML
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: null
created_at: 2026-09-08T16:16:12.615Z
updated_at: 2026-10-06T08:49:52.149Z
closed_at: 2026-10-06T08:49:52.148Z
close_reason: "Done: packing/devtools/templates/n11-lower-bounds-explainer-shell.html on origin/main (lines 43-44) displays the default certificate's .cert-figure in the initial HTML even while hidden and hides only the non-default ones; its parent think-qcmi is closed."
resolution: null
duplicate_of: null
---
Normal startup instrumentation found every .cert-figure hidden until bottom-script show(), so the first readable prose frame omits all figures and later inserts the selected certificate into document flow. Generate the default selected certificate as visible in the original HTML and preserve selection through prepared-math extraction and runtime initialization. Keep nonselected certificate figures hidden; test the no-JS initial layout and certificate picker transitions. Assigned to the Squares startup implementation slice; separate from per-formula intrinsic width changes.
