---
type: is
id: is-01m225nwsd7kaj0vpk7ebye9bb
title: "Carry identity on a second channel: 42 greens do not hold 324 squares"
kind: bug
status: open
priority: 2
version: 1
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies: []
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:09:08.140Z
updated_at: 2026-09-09T04:09:08.140Z
---
Known defect in the v2-transitions prototype, recorded in revision 12 and deferred.

Identity colouring is the default scheme: each square takes one colour of its own, keyed by the persistent identity the pool tracks, and keeps it for a whole session and across a step from one n to the next. The palette is generated rather than tabulated, from a staggered lattice over the green band between citron OkLCh (0.799, 0.124, 109.4 degrees) and teal (0.662, 0.119, 174.6 degrees), nine rows of rising lightness with the two palest rows carrying four and three slots because hue separation scales with chroma. That is 42 entries.

42 repeats 7.7 times over 324 squares, so at large n two squares eight apart in identity are the same colour and identity colouring quietly stops being an identity -- which is the one thing it promises.

The band is the constraint: greens alone do not hold 324 distinguishable colours, and widening past teal and citron stops being greens. A second channel -- the stroke, a mark, a shape -- is the way out and none was tried. This also bears on the atlas video: the video plan's open question on Version 2 colour now lists identity colouring as a third answer, and 324 is exactly its range, so the ceiling is the video's too.

A related note from the same revision: the identity scheme still desaturates while moving, so the promise holds only of a resting frame unless the drain is turned off. That is revision 6's motion cue and a separate feature; decide whether the two can coexist.

Prototype: packing/atlas/known-best/video/spikes/v2-transitions/. Notes: NOTES.md, revision 12, 'Three colour schemes' and 'What reads badly'. Video plan: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md, Open Questions.
