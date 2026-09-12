---
type: is
id: is-01m29gs5z48h1ztmc5h659hd6b
title: The bar spans whole integers, so it stops sliding under the reader
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-12T00:37:51.188Z
updated_at: 2026-09-12T00:37:51.188Z
---
Owner, 2026-09-11: "expand the entire bar to be the nearest integers below sqrt(n) and above sqrt(n) + 1, and include sqrt(n) and sqrt(n) + 1 as well, so then it's a little clearer how they fit together. This will also mean that the bar doesn't change quite as often, so it's easier to stay oriented."

The span becomes `[floor(sqrt(n)), ceil(sqrt(n) + 1)]` instead of `[sqrt(n), sqrt(n) + 1]`, with `sqrt(n)` and `sqrt(n) + 1` staying as marks INSIDE it rather than being its ends.

**The second reason is the better one.** The bar is a scale a reader is meant to hold in their head across a sweep, and today its two ends move with every n -- at n = 26 it runs 5.10 to 6.10, at n = 27 it runs 5.20 to 6.20, so nothing on it is ever twice in the same place. With integer ends it runs 5 to 7 for every n from 17 to 35, and the bar stops sliding under the reader.

What follows, and each wants deciding rather than assuming:

- **The span is no longer one unit wide**, so `GAPBAR.span` stops being a constant. It is 2 units when `sqrt(n)` is not an integer (floor to ceil of a value one apart) and 2 when it is. Work out whether it is ever 3 before writing the mapping.
- **More integers fall inside**, so the reference marks go from two or three to three or four. The drawing loop already handles any number of them; the labels may need collision handling they have not needed yet.
- **The open band gets proportionally narrower**, since the gap between the bounds is unchanged while the span roughly doubles. Check it is still legible at the n where the gap is smallest before committing to the wider span.
- **`gapbarX` and the inset both change meaning.** The inset exists so a mark at an end is not clipped; with integer ends the extremes may now be empty, in which case the inset can shrink or go.

Same-size rule applies to the new marks: ink at 400, same size as the bounds, the scale's own ends included -- see the commit that set that.
