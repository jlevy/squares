---
type: is
id: is-01m225kgmgf8h55vzqxw7eanbd
title: Benchmark solver steps per second under Node, with no browser
kind: task
status: in_progress
priority: 2
version: 3
spec_path: packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m225ps2ejkzyjc45g0xj6kyh
parent_id: is-01m225hw89vjsga1wnegrwnq5a
created_at: 2026-09-09T04:07:50.159Z
updated_at: 2026-09-09T04:09:45.044Z
---
In flight in the v2-transitions prototype as of 2026-09-08.

Measure the solver's throughput headlessly, in Node, with no browser and no rendering: steps per second as a function of n, and the cost per step broken down far enough to say what dominates. Report it as a tool that can be re-run, not as a number in a note (OR-1).

Why it is worth building rather than eyeballing. Everything Calibrate will do is thousands of settles with nobody watching, so steps per second at a given n is the quantity that prices the mode: it turns 'sweep the force law over these cases at these seeds' into a wall-clock estimate before anyone commits to it. Nothing today can produce that number without a browser in the loop, which measures the wrong thing.

The measurement that motivated it, and the trap it closes. Measured in the headless shell on 2026-09-08 the page is not slow: 120 frames per second at both n = 17 and n = 272, worst frame 10 ms, 358 DOM nodes, 10.7 MB heap, every API call under 2 ms. The sluggishness that prompted the investigation coincided with a five-minute load average of 116 caused by another session on the same host, not with the page. A browser-free benchmark separates solver cost from draw cost from host load, and would have answered that in one run.

The model test harness the atlas video plan already specifies runs the page's script in Node against a stub DOM, so the shape exists; this extends it to a timed loop rather than a correctness check.

Prototype: packing/atlas/known-best/video/spikes/v2-transitions/.
