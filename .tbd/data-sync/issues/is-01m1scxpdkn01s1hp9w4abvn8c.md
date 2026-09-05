---
type: is
id: is-01m1scxpdkn01s1hp9w4abvn8c
title: Publish a high-resolution atlas PNG for attachment and social sharing
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:22:33.907Z
updated_at: 2026-09-05T18:57:45.103Z
closed_at: 2026-09-05T18:57:45.103Z
close_reason: "Added known-best-1-100@2x.png at 4800x5792, 1.23 MiB, emitted by the same --update as the SVG, the 1x preview and the PDF and carrying the same source receipt. The 4096 target was measured and rejected: it is larger than the 2x export while carrying 27% fewer pixels, because a fractional scale invents antialiasing shades PNG cannot compress."
resolution: null
duplicate_of: null
---
The retained preview is 2400x2896 at 597 KB, the SVG's natural size. Add a second raster at roughly 4096 on the long edge, rendered by cairosvg from the same SVG so it matches the PDF by construction, carrying the same sha256 receipt and dimension guard the preview carries, drift-checked and mapped. File size to be measured and reported before it is committed: it is a binary in a repository, and it should be small enough to attach.
