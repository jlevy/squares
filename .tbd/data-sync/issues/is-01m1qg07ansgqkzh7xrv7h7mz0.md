---
type: is
id: is-01m1qg07ansgqkzh7xrv7h7mz0
title: "Certificate page: the all-100 known-best composite is the opening section's figure; figures renumber 1–7"
kind: task
status: open
priority: 2
version: 5
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1qekyhf4hjcavbdm3xya0bt
created_at: 2026-09-05T00:37:53.620Z
updated_at: 2026-09-05T00:40:49.441Z
---
Review direction on PR #79: the atlas composite of every known-best packing n = 1…100 becomes Figure 1 in 'The Square Packing Problem'; Trump 2, number line 3, atoms 4, prover 5, shrink 6, coarsening 7. Not inlined and not a data URI: the page deploys to GitHub Pages, so the renderer copies packing/atlas/known-best/known-best-1-100.png (2400×2676, 484 KB) and known-best-1-100.pdf (75 KB, vector) into the site directory beside index.html, and the figure is <img src="known-best-1-100.png"> hotlinked to known-best-1-100.pdf. Relative paths pass the CI self-containment check (it rejects only http(s) assets) and work from file://. pages.yml's paths filter should list the atlas composite so a change rebuilds the page. Figure renumbering in the Markdown and the JS comments.

## Notes

Caption for the composite figure: 'The best known packings of 1 through 100 unit squares, from the project's atlas: each cell is the tightest arrangement on record for that n, drawn from the retained witness. The full results, with every witness and its provenance, are in the GitHub repository, and the composite is available as a PDF.' — with 'GitHub repository' linked to packing/atlas/known-best/ on main and 'PDF' to known-best-1-100.pdf, and the image itself hotlinked to the PDF.
