---
type: is
id: is-01m3527tsmve0wkq545bv4fq0z
title: "Round displayed upper bounds up, not to nearest: 51 open cases print a bound stronger than any on record"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels: []
dependencies: []
parent_id: is-01m33vv4hs6kbe1c349y8wsgsf
created_at: 2026-09-22T17:22:26.739Z
updated_at: 2026-09-22T17:22:26.739Z
---
Found by the citation-data lane (2026-09-22). packing/devtools/build_composite_figure_data.py rounds an upper bound's display to nearest, so in 51 of the 265 open cases the stage and the atlas print an upper bound below the stored one: n = 29 shows s(29) <= 5.933833 against 5.93383346..., a stronger bound than anything on record. Lower bounds are already truncated for exactly this reason; an upper bound must round up (outward) at the display precision. Fix the display rule at its source, regenerate composite-figure.json and everything drawn from it (the page, the atlas SVGs, the citation data's value fields) with their own generators, and add a test that no displayed upper bound is below its stored value and no displayed lower bound above its.
