---
type: is
id: is-01m292qr3ayhe4zxrnmcjz9vb4
title: The bar's lower-bound numeral was set in the panel's serif
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T20:32:24.168Z
updated_at: 2026-09-11T20:33:09.406Z
closed_at: 2026-09-11T20:33:09.405Z
close_reason: "Fixed: the bar's number modifiers are is-lower and is-record, so the panel's bare .lower rule cannot reach into the plot. Measured after: both numerals Source Sans 3, 26 px, weight 700."
resolution: null
duplicate_of: null
---
The gap bar's two numerals are meant to be one face and one size, scarlet for the proved lower bound and green for the best known upper bound. The lower one came out in a 48 px serif and the upper in a 26 px sans.

Cause: the SVG text carried class="gapbar-num lower", and the facts panel below has a bare `.lower` rule -- position, 48 px, var(--serif) -- for its lower-bound line. A bare class selector reaches into an SVG as readily as into a div; `.gapbar-num` and `.lower` have the same specificity for font-family, and `.lower` is later in the sheet, so it won. Only `fill` survived from the bar's own rule, which is why the number was the right colour in the wrong face.

This is the second time the page has been bitten by a bare class name shared between the plot and the panel: the `gap-open` rect is named around the same trap.

Fixed: the bar's modifiers are `is-lower` and `is-record`, with a comment naming the collision. Measured after: both numerals Source Sans 3, 26 px, weight 700, #a3123f and #17794a.
