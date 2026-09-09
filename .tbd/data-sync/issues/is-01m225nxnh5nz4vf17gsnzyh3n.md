---
type: is
id: is-01m225nxnh5nz4vf17gsnzyh3n
title: Stop the rigidity slider reaching settings the fixed timestep cannot hold
kind: bug
status: open
priority: 2
version: 2
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m225ps2ejkzyjc45g0xj6kyh
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:09:09.037Z
updated_at: 2026-09-09T04:09:45.051Z
---
Known defect in the v2-transitions prototype, recorded in revision 11 and deferred deliberately.

The integrator runs at a fixed 1/120 s timestep. Below a knee of about a hundredth of a side the force law is stiffer than that timestep holds: measured at rigidity 0.004 with repulsion 4000, n = 17 ends needing a side of 6.82 around a box of 5.34 with a 0.21 overlap -- squares thrown out of the container. The slider still reaches there, because 'the hardest setting is effectively rigid' was the request, and the readout reports the overlap honestly. The rigid preset stops at 0.01, which is measured stable.

The notes name it a trap for anyone who has not read that section, and it is: the failure is silent in the sense that matters, because a run that throws squares out still produces a number.

Fixing it is a choice, not a patch, and the choice should be recorded. The candidates: substep the integrator so the stiff end is integrable (which changes the cost model the steps-per-second benchmark measures); clamp the slider at the measured stable bound and say why; or keep the reach and gate the run, refusing to report a side when the deepest overlap exceeds a threshold. The third preserves the request and closes the trap, and it is the smallest.

This matters more once anything sweeps the law automatically: candidate C0b's sweep would visit the unstable region with nobody watching, and every configuration there would contribute a number that means nothing.

Prototype: packing/atlas/known-best/video/spikes/v2-transitions/. Notes: NOTES.md, revision 11, 'One force law' and 'What reads badly'.
