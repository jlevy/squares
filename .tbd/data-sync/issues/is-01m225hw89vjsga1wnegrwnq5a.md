---
type: is
id: is-01m225hw89vjsga1wnegrwnq5a
title: Build the solver workbench, and settle the research questions it raised
kind: epic
status: open
priority: 1
version: 14
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
child_order_hints:
  - is-01m225jsnny9dz3vjf9jadxy27
  - is-01m225jt70jcc6a00ms689cj93
  - is-01m225jtvtc6dh83035crary61
  - is-01m225kg4dcxk61r0qzysnavwf
  - is-01m225kgmgf8h55vzqxw7eanbd
  - is-01m225n07e60s99czgzrdra84z
  - is-01m225n0snadqqs76gd16xmhah
  - is-01m225n1a2spz8q429db3c5dv8
  - is-01m225nvxap6cynxrpds642e8b
  - is-01m225nwsd7kaj0vpk7ebye9bb
  - is-01m225nxnh5nz4vf17gsnzyh3n
  - is-01m225ps2ejkzyjc45g0xj6kyh
  - is-01m225psj2z0sx407k1ma5a4sp
created_at: 2026-09-09T04:06:56.519Z
updated_at: 2026-09-09T04:09:37.601Z
---
Phase 0 of the atlas video plan asked for a transitions spike and produced a solver workbench. Across thirteen revisions the prototype at packing/atlas/known-best/video/spikes/v2-transitions/ grew a fixed-timestep contact solver with an editable four-parameter force law and a draggable force-against-gap plot, a relationship graph that masks the attraction (every pair, per block, or the retained packing's own contact graph, which can also be drawn by hand on the stage), growth from a reduced starting size to unit squares, open-ended optimisation with squares draggable mid-run, an annealing dial, and three named modes.

This epic owns the instrument and its research questions. The atlas video plan (think-hsdj, docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md) keeps only the video artefacts: the frame record and player, the capture pipeline, the transition record and tween, and publication. That split is recorded in the plan's 'What Phase 0 became' section and in X-025.

The three modes are a choice on each of three axes. Scope: Pack takes one n, Animate takes a range, Calibrate would take a set split into cases tuned on and cases held back. Strategy: the force law, the relationship graph, growth, annealing, and which solver runs. Presentation: colour scheme, timing, motion phasing, desaturation. Calibrate is Pack's strategy panel with a loop and a results table around it, which is why it is cheap once Pack is right and why Pack is built first. The mode now called Animate was called Sweep until 2026-09-08; it was renamed because Calibrate is the mode that sweeps, over parameters, and two modes called sweep would be permanently ambiguous.

Measured facts the beads under this epic rest on, all from the committed spike notes at packing/atlas/known-best/video/spikes/v2-transitions/NOTES.md: the force law matters and has no single best setting (at n=17 the rigid law is the only setting that leaves the trivial grid, 4.756 against sticky's 4.988; at n=29 it reverses, rigid jamming at 6.402 against sticky's 5.986); growth finds nothing the plain settle does not (n=17 grown from 0.3 lands at 4.988, 6.7 per cent above the record); biasing toward a contact graph does not realise it and does worse than attracting every pair; and the page is not slow (120 fps headless at n=17 and n=272, worst frame 10 ms, 358 DOM nodes, 10.7 MB heap, every API call under 2 ms).

Research framing: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md, candidates C0a to C0d.
