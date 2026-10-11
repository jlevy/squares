---
type: is
id: is-01m12w4w0sg8bxn5kfp9fqzg51
title: "Composite: widen the light end of the shade ramps"
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-08-28T00:26:05.720Z
updated_at: 2026-10-06T08:29:04.344Z
closed_at: 2026-10-06T08:29:04.343Z
close_reason: "Done on main: sqpack/render/color.py has SHADE_LIGHT_SPREAD = 0.015, the lift this bead describes."
resolution: null
duplicate_of: null
---
The two darkest shades carry most of the atlas and were already right, so the ramp was widened only above them: each shade past the second lifts by 0.015. Right-angle family travel went 0.185 to 0.245 OkL, citron 0.183 to 0.226, with shade 0 and 1 byte-identical.
