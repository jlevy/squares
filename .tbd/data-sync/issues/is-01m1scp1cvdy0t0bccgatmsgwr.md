---
type: is
id: is-01m1scp1cvdy0t0bccgatmsgwr
title: Pages path filter omits known-best-1-100.svg, the file the page actually embeds
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:18:23.003Z
updated_at: 2026-09-05T21:38:52.884Z
closed_at: 2026-09-05T21:38:52.884Z
close_reason: D-458. Four render inputs had drifted out of the Pages filter, the composite SVG among them. RENDER_INPUTS declares them beside the outputs and test_the_pages_filter_covers_every_render_input holds the workflow to it, checked by deleting the SVG entry.
resolution: null
duplicate_of: null
---
The Certificate page workflow triggers on packing/atlas/known-best/known-best-1-100.png and .pdf but not the .svg that Figure 1 loads. Safe today only by construction: the PNG carries a tEXt receipt of the SVG's sha256 and the PDF is derived from it, so the SVG cannot move alone. That is an accident of the build, not a stated invariant, and the filter should name the file it depends on.
