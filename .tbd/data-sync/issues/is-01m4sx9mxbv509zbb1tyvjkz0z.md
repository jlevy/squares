---
type: is
id: is-01m4sx9mxbv509zbb1tyvjkz0z
title: Draw 301 from the grid-slack view at a 1-degree threshold (admits cleanly; the 0.5-degree view sits in review)
kind: task
status: in_progress
priority: 1
version: 2
delegate: user-eb-reg-leftovers
labels:
  - regularization
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-13T05:55:48.266Z
updated_at: 2026-10-16T05:22:36.549Z
started_at: 2026-10-16T05:22:36.549Z
---
Measured on 13 October 2026 at stack 498's top (a98d40319), scratch only (session 01RXar8v4JCumHp9eHemRgSA; outputs not retained):
- 301's drawing (axis tool) is irregular by rotation, not position: 110 grid squares tilted 0.03-0.68 deg in 39 angle classes (98 under 0.5 deg, 12 at 0.53-0.68 deg), centres on the lattice within 0.03. Census: light 25, uneven 89, near-axis 98, variation 187 (worst in the atlas). The axis tool's snap tolerance (1e-4 rad) leaves them; 22 more are rotation-blocked (it never translates).
- grid-slack at 0.5 deg: row 7 (review): 9 squares' stage counts fall, all pairs of a square left at 0.53-0.68 deg beside one straightened from 0.26-0.48 deg; an artefact of the 0.5 deg threshold equalling the stage rule's 0.5 deg tolerance. Leaves 12 off-hue squares, 3 light.
- grid-slack at 1 deg (byte-identical to 5 deg at 301): row 10 admit, same side, both exact routes, one-to-one, 110 named turns (max 0.68 deg), max move 0.44 (rattler 258 into its corner), census light 0, uneven 0, near-axis 0.
- Evan Daniel's view at 301: row 6 review (re-angles 35 band squares up to 1.34 deg; bound side).
- Elsewhere (13 counts with a square tilted 0.5-2 deg): 1 deg also finishes 267; 5 deg also rescues 176 (row 10, L16 U62 -> L3 U36) and finishes 146, 172, 199, but re-poses ~3 deg squares at 176 and 306; 175 and 270 get worse at 5 deg (the choice rule rejects them).
Do: once the owner chooses, run regularize_grid_slack --n 301 --near-axis-degrees 1 (or the chosen global threshold) and admit through layer --grid-run; recorded parameters cover a per-count value.
