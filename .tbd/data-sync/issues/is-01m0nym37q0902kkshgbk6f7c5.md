---
type: is
id: is-01m0nym37q0902kkshgbk6f7c5
title: "PoseBox scalar and hits_all_poses(): the proof-lane hook"
kind: task
status: open
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0nym0701fv1qq9fbqq9qz0w
created_at: 2026-08-22T23:59:14.167Z
updated_at: 2026-08-25T03:03:40.763Z
---
Interval over a box of (x,y,theta). Instantiating the same predicate at this scalar turns 'do these two squares overlap' into 'can any square with pose in this box avoid all these points' -- the unavoidable-set decision, in the same code. One worked example, no proof attempt.

## Notes

2026-08-24 ownership boundary: this bead owns the PoseBox unavoidable-set proof hook. General interval existence certification for imported packing witnesses belongs to frontier-assurance bead think-75ll; the two use cases must not be planned as one duplicate deliverable.
