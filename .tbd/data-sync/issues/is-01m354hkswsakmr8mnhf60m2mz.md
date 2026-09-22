---
type: is
id: is-01m354hkswsakmr8mnhf60m2mz
title: Make the grid-fill speed-up a setting, and default it to 4x
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T18:02:44.411Z
updated_at: 2026-09-22T19:22:13.863Z
closed_at: 2026-09-22T19:22:13.848Z
close_reason: "Done in a6995399f: grid fill speed is a control, 1 to 8 in halves, default 4, carried on the API, in a capture's commands and in its receipt; a cut that asks for a factor the page declines is refused. Re-priced: n=2..100 153.39 s, n=2..324 542.02 s."
resolution: null
duplicate_of: null
---
The owner (2026-09-22): the speed-up for the fast steps (the grid fills that finish each square's last row) should be a settable factor, defaulting to 4x instead of 3x. Today it is the constant SIMPLE_TRANSITION_SPEED = 3 in packages/workbench/src/animation/timeline.ts, reported by the page as continuous().simpleSpeed and checked by check_animation_editor's census, which already reads the page's own factor rather than assuming one. Make it a control beside the page's other timing settings, with a setter and getter on the API, carried in the capture's commands and receipt, and default 4. It shortens every range that holds a grid fill: n = 1..100 is 159.65 s at 3x, and the 55 still steps in it take 26.41 s, so 4x saves about 6.6 s. Re-price the cuts afterwards with capture_video --price-against and record the new lengths in the delivery spec.
