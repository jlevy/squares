---
type: is
id: is-01m4q7v1t6qmvrvzsf8qxn4dvq
title: "Grid slack: decide the third generator and its straightening threshold, then run it where grid regions still vary (PR #530)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels:
  - regularization
dependencies: []
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
hold: null
hold_until: null
created_at: 2026-10-12T05:02:20.998Z
updated_at: 2026-10-12T11:32:12.486Z
started_at: 2026-10-12T11:32:12.486Z
---
Owner note 2026-10-12: 'a lot of variation even on the grids, e.g. 302 and 303'. PR #530 (stacked on #511) adds devtools.census_drawing_regularity (house-renderer census: light/uneven/near-axis axis squares) and the prototype devtools.regularize_grid_slack (straighten near-axis squares under 0.5 deg, MILP translations keeping every witness contact, exact re-solve at s_W or U, both exact routes). 302: light 33->1, uneven 147->2, near-axis 9->0; 303: 12->7, 44->12, 1->0; 263 and 228 to ~0; 20 counts: light 149->93, uneven 472->240, near-axis 36->8, house sides 11,156->11,817. Owner decisions: (1) adopt it as the policy's third generator; (2) straightening threshold 0.5 deg or up to 5 deg (302 fully uniform at 5). Then: run over every count the census still ranks, taking the prototype per count only where no house/stage total falls against Evan Daniel's view; remaining unevenness at 290, 291, 171, 198, 126, 105 is forced.
