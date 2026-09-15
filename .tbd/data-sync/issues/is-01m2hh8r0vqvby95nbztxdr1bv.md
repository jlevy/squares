---
type: is
id: is-01m2hh8r0vqvby95nbztxdr1bv
title: Seeking the last instant of a physical step throws a drain RangeError
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:16.665Z
updated_at: 2026-09-15T03:32:54.340Z
closed_at: 2026-09-15T03:32:54.339Z
close_reason: "Fixed on PR #160 in db6ec77a: smootherstep is clamped to one; check_animate_view seeks 1,323 grid instants, ends included, under three styles and three annealing levels."
resolution: null
duplicate_of: null
---
Found 2026-09-14 by lane D-page while writing the Animate checks (and by the legacy-checker inventory); not a review finding.

Seeking the last instant of a physical step threw `RangeError: scene drain must be between zero and one` instead of drawing: `smootherstep` in `packages/workbench/src/application.js` guarded 0 and 1 but not the polynomial just below 1, which rounds to 1 + 2^-52, and the physical styles pass the resulting drain to the painter unclamped (the tween clamps). Hit at annealing 10 under physics or bodies at `duration() * 48 / 48` of the steps into 10, 17 and 26, and at `seek(2.4)` of the step into 17 at the default level.
