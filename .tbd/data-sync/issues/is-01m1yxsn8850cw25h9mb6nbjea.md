---
type: is
id: is-01m1yxsn8850cw25h9mb6nbjea
title: Adopt kpress's mono face, box list marker and PT Serif quotes in the explainer
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T21:53:39.588Z
updated_at: 2026-09-07T21:53:39.588Z
---
When kpress lands its mono face (Source Code Pro static), the CSS-drawn list marker, and the retirement of LocalPunct: bump the gitlink, remove the shell's print-only prose override that dropped LocalPunct (explainer-shell.html near line 777, no longer needed once kpress does not borrow Georgia), check the mono size beside the prose in captions and body on screen and in the PDF with inspect_explainer_typography, re-render, and confirm the provenance guard passes with no Menlo or Georgia in the PDF. Record the PDF size before and after.
