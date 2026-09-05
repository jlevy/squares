---
type: is
id: is-01m1sejpasjx7c237xkty0vd9g
title: Remove non-scaling-stroke from the shared packing renderer and the T-018 visual
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T18:51:30.520Z
updated_at: 2026-09-05T18:51:30.520Z
---
D-457 removed vector-effect=non-scaling-stroke from the composite atlas. The same attribute is still emitted by sqpack/render/style.py presentation_attributes, sqpack/render/packing.py and devtools/render_t018_proof_visual.py. It is inert under cairosvg (measured identical at scale 1, 2 and 4) and wrong under any browser, which resolves it against display size. Removing it touches every retained case rendering, so it is its own change with its own regeneration and drift check.
