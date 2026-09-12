---
type: is
id: is-01m29gkhfkt1sv50caesct8q0x
title: One rule for how a number is written
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-12T00:34:46.373Z
updated_at: 2026-09-12T00:34:46.373Z
---
Owner, 2026-09-11: "if a value is truly an integer, don't write 3.00 for 3, just write 3. if it's a float, use 3 decimals on the diagram, 6 decimals on the formulas with an ellipsis."

One rule, applied everywhere a number is drawn, replacing the several that exist now. The page currently writes `fmt(v, 2)` in most places and the generator prints six-place values into the panel, so the same quantity can appear with two different precisions on one screen.

The rule:
- **An exact integer prints as an integer.** `4`, not `4.00`. This is visible today on the bar at every perfect square: n = 16 draws reference marks reading `4.00` and `5.00` when the values are exactly 4 and 5, and n = 16's record is exactly 4.
- **A non-integer on the diagram prints to three decimals.** The bar's reference decimals, the bound values above it, and any readout that is a diagram label rather than a stated fact.
- **A non-integer in a formula prints to six decimals with an ellipsis**, so the panel says `5.824445…` rather than implying the value terminates. The ellipsis is the honest part: these are algebraic numbers and a truncation without one reads as an exact decimal.

Two things to get right rather than assume:
- **"Truly an integer" is a question about the value, not the rendering.** A side of 4.000000001 is not 4, and the test has to be exact rather than a tolerance, or a bound that merely rounds to an integer will be printed as one.
- **The page and the generator both format numbers**, so the rule needs one implementation each side and they have to agree. `fmt` is the page's; the generator's is spread through the TeX builders.

Check the ellipsis glyph survives the font subset -- the panel's faces carry only what the page uses, and an earlier bug had a relation glyph fall through to a different face at a different size.
