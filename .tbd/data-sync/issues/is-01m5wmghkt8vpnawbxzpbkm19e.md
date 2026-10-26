---
type: is
id: is-01m5wmghkt8vpnawbxzpbkm19e
title: Assets and PDFs carry squaremath.org, with the repository beside it in a credits line
kind: epic
status: in_progress
priority: 2
version: 5
delegate: claude-code@vm
labels: []
dependencies: []
child_order_hints:
  - is-01m5wmh5gpbjmk9safsg4qw245
  - is-01m5wmh6kad28vx7hxdmj224q0
  - is-01m5wmh7vpm45bwrkkr7963679
hold: null
hold_until: null
created_at: 2026-10-26T17:35:42.202Z
updated_at: 2026-10-26T17:36:26.475Z
started_at: 2026-10-26T17:36:26.475Z
---
The owner, 26 October 2026: update every asset, the PDFs included, to link to
squaremath.org where there is room for one URL, and to squaremath.org and
github.com/jlevy/squares where a credits line has room for both.

Today the printed assets name the repository alone. `build_known_best_atlas` holds
`SUMMARY_REPOSITORY = "github.com/jlevy/squares"` and prints it four ways: the posters'
own `repository` line under the title, the centred `project-reference` line
("The Squares Project · github.com/jlevy/squares"), the citations sentence in the
retained composite descriptions, and the summary's citations line. `render_overview`
holds `SITE_URL = "https://squaremath.org/"`, which the pages already use.

Scope to settle before editing, one bead each:

1. The survey: every asset a reader can hold or download, and the line each carries --
   the two poster families and their exports, the composite atlas PDFs, the four paper
   PDFs and their fronts, the film, the social card and the atlas print.
2. The rule, written once: one URL means squaremath.org; a credits line with room for
   both names the site first and the repository second. A constant pair rather than four
   literals.
3. The redraw, with the retained descriptions and the print-layout checks moved with it.

Two things make this larger than a string change:

- Every drawn line shifts the print layout. `check_print_layout` and the poster records
  hold the measured baselines and ink bounds, and the retained composite descriptions in
  `build_known_best_atlas` are prose a reviewer reads against the drawing.
- A poster is a release asset. `development.md`, "Release assets are drawn at their
  component's version bump", and the release-impact gate makes the infographic family a
  candidate: both infographic families and every advertised export advance together, so
  this needs a version decision rather than a no-public-change record.

Not on the Changelog branch (PR #837), which is navigation and reader text and carries a
no-public-change record for the papers. This is its own pull request.
