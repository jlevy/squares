---
type: is
id: is-01m32tnmps6qw5h8tde5xq9zmw
title: Set the stage legend as sentences with math and colour swatches
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-21T20:31:41.784Z
updated_at: 2026-09-21T20:31:41.784Z
---
Refinements to the legend added at the foot of the facts column (think-kgx1), from the owner's review:

- `s(n)` must be set as mathematics, not as plain text. The build already renders one-off expressions through the vendored KaTeX at build time -- `build_candidate.py:1263` does exactly this for `\\sqrt{n}` and `\\sqrt{n} + 1` -- so `s(n)` goes the same way rather than being faked in the text face.
- Each line is a sentence: initial capital and a full stop.
- The lines carry colour swatches, as the composite figure's own legend does: four swatches before the tilt-angle line and a shade ramp before the full-side-contacts line. See `packing/atlas/known-best/known-best-1-324.svg`, whose swatches are 19 px squares with a hairline black stroke.

The swatches must come from the page's own palette -- `DATA.colour.palette` and `DATA.colour.shades`, which the builder fills from `sqpack.render` -- and not from the SVG's hexes copied across, or the legend will say one thing while the picture says another the moment the palette moves.

This means the legend is built in script from the corpus rather than written as static markup in the template.
