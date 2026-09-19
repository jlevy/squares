---
type: is
id: is-01m2y0qgmwq94dk9ykh5kdhn3v
title: "PR199 review R8: reject unsupported piercing direction angles"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:41:22.458Z
updated_at: 2026-09-19T23:41:22.458Z
---
integral_piercing.py:528-530 only checks positive angle_limit, though centre_domain assumes nonnegative cosine and sine. L2 B1 sites[(1,1)], direction_steps2, angle_limit2 produces rows[[0]], infeasible and killed_coarse_net; angle_limit1/2 yields[[1]] feasible. The centre pierces every closed unit square in the2x2 container. Reject angle_limit>1 before using first-quadrant geometry (or generalize with absolute projections), test invalid ranges. Defaults and retained certificates unaffected.
