---
type: is
id: is-01m5wmh5gpbjmk9safsg4qw245
title: Survey every asset's printed address
kind: task
status: in_progress
priority: 2
version: 4
delegate: claude-code@vm
labels: []
dependencies:
  - type: blocks
    target: is-01m5wmh6kad28vx7hxdmj224q0
parent_id: is-01m5wmghkt8vpnawbxzpbkm19e
hold: null
hold_until: null
created_at: 2026-10-26T17:36:02.582Z
updated_at: 2026-10-26T17:46:09.765Z
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

## Notes

## The survey, 26 October 2026

Two surfaces print an address. Nothing else does.

**1. The colophon, `render_overview.colophon_lines`.** Three quiet centred lines, the
first of which reads

> The Squares Project · github.com/jlevy/squares

It is the footer of every page of the site (`colophon_html`, passed to `kpress_page` as
`footer_html`) and, with its edition suppressed, the colophon of all four papers in both
their HTML and their printed PDFs (`render_n11_lower_bounds_explainer`,
`render_n11_optimality_review`, `render_packing_methods` pass `colophon_lines(edition="")`
into `COLOPHON` in each `*-shell.html`). A credits line with room for both: the site
belongs before the repository.

**2. The posters and their exports, `devtools/build_known_best_atlas.py`.** One constant,
`SUMMARY_REPOSITORY = "github.com/jlevy/squares"`, reaches the drawing four ways:

- `text_line("repository", SUMMARY_REPOSITORY, layout.repository_baseline)`, the corner
  layout's own line under the title. One address, so `squaremath.org`.
- `text_line("project-reference", f"{POSTER_CITATIONS} · {SUMMARY_REPOSITORY}", ...)`,
  the centred line of the non-corner layout: "The Squares Project ·
  github.com/jlevy/squares". A credits line with room for both.
- `SUMMARY_CITATIONS`, the summary's sentence: "Citations for all results are available
  in the Squares Project: github.com/jlevy/squares". One address in a sentence; the site
  is where a reader should be sent.
- The retained composite descriptions, each ending
  `f"{POSTER_CITATIONS}: {SUMMARY_REPOSITORY}."` These are prose a reviewer reads against
  the drawing, so they move with it.

**Carries no address, so needs no change.** The social card draws the project's name as
outlines and nothing else (`devtools/social_card.py`). The film and the retained video
spikes under `packing/atlas/known-best/video/` print no credit URL.
`devtools/render_composite_pdf.py` prints the poster SVG and adds no line of its own. The
workbench's shell carries the shared bar and the colophon, so it follows the colophon.

## What it costs

- The colophon is one line of Python and changes every page and the four paper PDFs. By
  `development.md`, a footer update keeps a paper's content edition and needs no release.
- Every poster line shifts the print layout: `check_print_layout` and the poster records
  hold measured baselines and ink bounds, and `_print_ink_bounds(SUMMARY_REPOSITORY, …)`
  reads the string's own width.
- A poster is a release asset. "Both infographic families and every advertised export
  advance together", and a printed-address correction is an ordinary correction, so the
  infographic family advances patch rather than taking a no-public-change record.
