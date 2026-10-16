---
type: is
id: is-01m4sx9mxbv509zbb1tyvjkz0z
title: Draw 301 from the grid-slack view at a 1-degree threshold (admits cleanly; the 0.5-degree view sits in review)
kind: task
status: closed
priority: 1
version: 4
delegate: user-eb-reg-leftovers
labels:
  - regularization
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-13T05:55:48.266Z
updated_at: 2026-10-16T09:57:48.982Z
started_at: 2026-10-16T05:22:36.549Z
closed_at: 2026-10-16T09:57:48.982Z
close_reason: "Verified 2026-10-16 by lane D (user-eb-reg-leftovers): 301 is drawn from Evan Daniel's view at U (0/0/0 light/uneven/near-axis, 8 classes), better than the 1-degree grid view (14 classes, 4.6e-12 above U); at 270 and 305 neither strong generator improves on the drawn views (runs evand-regularize-leftovers-1016, grid-slack leftovers 0.5/1/5 deg). No record names these beads."
resolution: null
duplicate_of: null
---
Measured on 13 October 2026 at stack 498's top (a98d40319), scratch only (session 01RXar8v4JCumHp9eHemRgSA; outputs not retained):
- 301's drawing (axis tool) is irregular by rotation, not position: 110 grid squares tilted 0.03-0.68 deg in 39 angle classes (98 under 0.5 deg, 12 at 0.53-0.68 deg), centres on the lattice within 0.03. Census: light 25, uneven 89, near-axis 98, variation 187 (worst in the atlas). The axis tool's snap tolerance (1e-4 rad) leaves them; 22 more are rotation-blocked (it never translates).
- grid-slack at 0.5 deg: row 7 (review): 9 squares' stage counts fall, all pairs of a square left at 0.53-0.68 deg beside one straightened from 0.26-0.48 deg; an artefact of the 0.5 deg threshold equalling the stage rule's 0.5 deg tolerance. Leaves 12 off-hue squares, 3 light.
- grid-slack at 1 deg (byte-identical to 5 deg at 301): row 10 admit, same side, both exact routes, one-to-one, 110 named turns (max 0.68 deg), max move 0.44 (rattler 258 into its corner), census light 0, uneven 0, near-axis 0.
- Evan Daniel's view at 301: row 6 review (re-angles 35 band squares up to 1.34 deg; bound side).
- Elsewhere (13 counts with a square tilted 0.5-2 deg): 1 deg also finishes 267; 5 deg also rescues 176 (row 10, L16 U62 -> L3 U36) and finishes 146, 172, 199, but re-poses ~3 deg squares at 176 and 306; 175 and 270 get worse at 5 deg (the choice rule rejects them).
Do: once the owner chooses, run regularize_grid_slack --n 301 --near-axis-degrees 1 (or the chosen global threshold) and admit through layer --grid-run; recorded parameters cover a per-count value.

## Notes

2026-10-16 ~08:05Z user-eb-reg-leftovers (lane D of the intake pass, branch claude/intake-2026-10-16-regularize-leftovers): VERIFIED, the ask is met, and by a better view than the one proposed here. Since 13 October (2b24ab73c) 301 is drawn from Evan Daniel's exact view at the verified upper bound U (run evand-regularize-bound-1013-n301; state regularized in packing/atlas/known-best/default-drawings.json, both exact routes): light/uneven/near-axis 0/0/0, 8 angle classes, 8 hues, house/stage sides 1001/1007, against the axis tool's 25/89/98 this bead measured. Grid-slack was re-run tonight on the same witness at 0.5, 1 and 5 degrees (grid-slack-leftovers-deg05-1016 / -deg1-1016 / -deg5-1016): at 1 and 5 degrees it draws 0/0/0 but 14 classes and hues and 997/1001 sides, at the decimal witness's side 4.58e-12 above U (owner's question 13: a drawn view must be at most U) and row 7 refuse; at 0.5 degrees 3/42/0. regularize_select over the runs (0 chosen) keeps the drawn view. Nothing left to run. No record names think-co6o, so it can close now; the atlas README paragraph of 16 October that cites the re-run lands with this lane's PR. Coordinator: please close (I have not).
