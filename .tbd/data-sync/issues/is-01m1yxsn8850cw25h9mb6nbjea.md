---
type: is
id: is-01m1yxsn8850cw25h9mb6nbjea
title: Adopt kpress's mono face, box list marker and PT Serif quotes in the explainer
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T21:53:39.588Z
updated_at: 2026-09-08T22:03:06.400Z
closed_at: 2026-09-08T22:03:06.388Z
close_reason: "Shipped: squares#134 merged to main on 2026-09-08 after a senior review (approve) and its fixes; the explainer takes kpress's mono face, its quote face and its box marker, and no host font draws any of the document's own text"
resolution: null
duplicate_of: null
---
When kpress lands its mono face (now Planetaire Mono Text at 0.87, kpr-v731, with the on/off setting kpr-…), the CSS-drawn list marker (kpr-2tmj) and the shipped quote face KPress Quotes (kpr-asj4): bump the gitlink, decide whether the explainer keeps the mono on (the page has 134 characters of code on three pages; the owner wants the option to turn it off for page weight through the standard setting, format.mono_font: system), remove the shell's print-only prose override that dropped LocalPunct (explainer-shell.html near line 777), check the mono size beside the prose in captions and body on screen and in the PDF with inspect_explainer_typography, extend the inliner to prune the mono faces when the setting is system, re-render, and confirm the provenance guard passes with no Menlo or Georgia in the PDF, removing its dated exceptions. Record the page and PDF sizes before and after.

## Notes

Squares PR #128 has merged and deployed the CSS list marker and shipped KPress Quotes face, and removed the old print-only prose override. Browser and PDF provenance checks passed. The mono portion remains open: Menlo and DejaVuSansMono remain documented host-font exceptions until KPress kpr-v731 and its configuration path ship. Do not close this issue based only on the completed marker and quote adoption.
