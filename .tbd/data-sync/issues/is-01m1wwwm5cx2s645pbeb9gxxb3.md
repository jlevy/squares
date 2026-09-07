---
type: is
id: is-01m1wwwm5cx2s645pbeb9gxxb3
title: Archive the un-retained Burns n = 17 assets in a dated packet
kind: task
status: open
priority: 2
version: 1
labels:
  - sources
  - n17
dependencies: []
parent_id: is-01m1wwrjmnkeq6xgkwcz4ha3zs
created_at: 2026-09-07T02:59:19.340Z
updated_at: 2026-09-07T02:59:19.340Z
---
The archive under packing/resources/web/n17-lower-bounds-2026/ holds the lower-bound post, note, verifier and the near-record post HTML, but not: (1) the Part 1 intro post https://sam-burns.com/posts/n17-square-packing-problem-intro/ (2026-08-05; states the ML search method and links Squarl); (2) the near-record post's linked data file https://sam-burns.com/downloads/n17-square-packing/alternative-packing-rounded-coordinates.json (format squarl_n17_blog_rounded_coordinates_v1: 17 centres and angles, W = 4.677648294965133, the q and W quintics; the author marks it illustration, not a certificate); (3) the five matplotlib SVG figures of the near-record post, which carry the drawn square polygons; (4) the two post PNGs. SHA-256 prefixes fetched 2026-09-07: burns-part1.html: d26b7ce8913a... alt-coords.json: 40622c8b03e1... 01-alternative-packing.svg: 68e7e4f5115a... 02-record-vs-alternative.svg: 297fde8414c9... 03-four-searches-one-topology.svg: 3a6dd9114b2d... 04-contact-certificates.svg: 6744ac052d09... 05-angle-balance.svg: 7c499769b628... n17-lower-bound.png: 6de7aecf2db7... optimal-n17-square-packing.png: 370c0cf29786... . Also record the Squarl repository https://github.com/sam-bee/squarl (MIT, single squashed commit 016dff98 of 2026-08-05, 3.4 MB Go/CUDA RL library; docs/final-search-closeout.md reports the final nine-hour search did not beat Bidwell, best strict width 4.675530095599908; data/world-record.json is a float32 Bidwell reconstruction from Ellsworth's SVG, not new data) in the archive index row for [Burns--Massaccesi n17]. Put the new files in a new dated directory and add an index row; do NOT reword packing/resources/web/n17-lower-bounds-2026/README.md, which is a frozen input of the resumable n = 17 replay (SHA-256 b48c0c31...).
