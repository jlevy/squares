---
type: is
id: is-01m5wmh5gpbjmk9safsg4qw245
title: Survey every asset's printed address
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m5wmh6kad28vx7hxdmj224q0
parent_id: is-01m5wmghkt8vpnawbxzpbkm19e
hold: null
hold_until: null
created_at: 2026-10-26T17:36:02.582Z
updated_at: 2026-10-26T17:36:26.494Z
started_at: 2026-10-26T17:36:26.494Z
---
One pass over every asset a reader can hold or download, naming the line it carries and
whether that line has room for one address or two. The answer is a table, and the next
two beads are written from it.

Where to look:

- `devtools/build_known_best_atlas.py`: `SUMMARY_REPOSITORY`, `SUMMARY_CITATIONS`,
  `POSTER_CITATIONS`, `POSTER_DIAGRAM_CREDIT`, the `project-reference`, `citations`,
  `repository`, `credit` and `release-stamp` text lines, and the retained composite
  descriptions that describe them.
- `devtools/render_composite_pdf.py` and the composite PDF names in
  `sqpack.known_best`.
- The four papers' fronts (`devtools/paper_front.py`, each `render_*` module) and their
  printed PDFs.
- `devtools/atlas_print_font.py` and `devtools/check_print_layout.py`, for what a changed
  line costs in layout.
- `devtools/social_card.py`, the film's credits (`sqpack/motion_lab`, the retained video
  spikes), and `packages/workbench`.
- `README.md`'s poster captions and `docs/project/guides/`, for what the prose says each
  asset carries.

Record for each: the asset, the file and symbol that writes the line, the line as it
reads now, whether it is one address or a credits line, and what the print layout holds
about it.
