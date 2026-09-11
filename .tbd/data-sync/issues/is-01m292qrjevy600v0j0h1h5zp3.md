---
type: is
id: is-01m292qrjevy600v0j0h1h5zp3
title: Bound arrows were cut in half, and the rail's ends were the scale's ends
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T20:32:24.653Z
updated_at: 2026-09-11T20:33:09.742Z
closed_at: 2026-09-11T20:33:09.741Z
close_reason: "Fixed: the rail runs end to end, the scale's ends are quiet ticks inset 34 units, and the plot gained 8 units of headroom. Measured after: nothing clipped at any of 13 sampled n."
resolution: null
duplicate_of: null
---
Two faults in the gap bar's geometry, with one fix.

The scale ran from sqrt(n) at x=0 to sqrt(n)+1 at x=680, and the arrows are 22 units wide centred on their value, so an arrow at either extreme was half outside the viewBox and clipped. Every perfect square n put both arrows there, since the record equals sqrt(n) exactly.

And the rail's two ends WERE the scale's two ends, which reads as a box with hard sides rather than as a scale.

Fixed: the rail runs the full width of the column and the scale's ends are quiet ticks inset 34 units from each end, so sqrt(n) and sqrt(n)+1 are marks ON the bar. An arrow at either extreme now has room to be drawn whole. The plot's viewBox also gained 8 units of headroom, which the upper numeral's em box was overrunning by one pixel.

Measured after: at n in {2,4,5,9,10,11,16,17,26,29,100,110,272} every arrow and every numeral lies inside the plot. Cut: 0.
