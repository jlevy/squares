---
type: is
id: is-01m163ed1rmq5egbj2dxjp9zda
title: Atlas SVG coordinate precision is inherited, not pinned
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-29T06:31:21.399Z
updated_at: 2026-08-29T06:31:21.399Z
---
`format_svg_number` renders a `ScalarSource` at whatever precision the shared exact field happens to be refined to, so the generated atlas SVG's coordinates carry 27 digits in a fresh process and 50 after any caller has run `field.refine_to(40)`. That makes `known-best-1-100.svg` non-reproducible and `test_known_best_composite_png_is_derived_from_current_svg` a check that passes only by test ordering. Reproduce: `pytest tests/test_promote_system.py tests/test_known_best_atlas.py -p no:randomly` fails; either module alone passes. Fix is to quantise at the emission site, which re-hashes every stored SVG and PNG receipt in the repo, so it needs its own slice. See D-359.
