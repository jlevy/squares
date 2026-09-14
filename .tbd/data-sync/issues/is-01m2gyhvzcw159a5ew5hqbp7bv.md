---
type: is
id: is-01m2gyhvzcw159a5ew5hqbp7bv
title: Even space above and below the headline
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2gyhqfmr0xpcjsr34na3acq
created_at: 2026-09-14T21:53:12.656Z
updated_at: 2026-09-14T22:16:22.981Z
closed_at: 2026-09-14T22:16:22.980Z
close_reason: "Fixed in c94054c4. In this codebase the box is the container drawing: #packing-svg is 971 tall rather than 940, which puts the drawn floor at 942.9. The headline ink runs 989 to 1034, leaving 46.1 px above and 46.0 px below, measured in pixels at n = 1, 17 and 100. The stage stays 1920 x 1080 for 1080p capture, and check_workbench.py measures the gaps from a capture screenshot."
resolution: null
duplicate_of: null
---
Owner, 2026-09-14: "Make the box overall a little bigger, so the space above and below the n = <> is even."

Measured on the built page (stage coordinates, 2026-09-14): the container's drawn floor is at 913.2 at every n, and the headline row sits at `bottom: 12px`, 972 to 1068, so the numeral's ink is much closer to the stage's bottom edge than to the container above it.

Constraint: the stage is 1920 x 1080 because `capture_video.py` maps it one page pixel to one video pixel (`STAGE_HEIGHT = 1080`). "Bigger" therefore means either growing the stage's height and teaching capture a new frame height, or keeping 1080 and fitting the drawing so the headline sits midway between the container floor and the stage floor. Measure the ink with pixels, not boxes, and choose the option that keeps capture exact; state which in the commit.

Accept: the gap from the container floor to the top of the headline ink equals the gap from the bottom of the ink to the stage edge within 2 px, at n = 1, 17 and 324.
