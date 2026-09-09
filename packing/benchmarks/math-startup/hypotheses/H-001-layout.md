---
softschema:
  contract: squares.math-startup.hypothesis.v1
  schema: ../schemas/hypothesis.schema.yaml
  status: enforced
id: H-001
title: Reserved math bases prevent math-induced text movement
derived_from: [X-001]
registered: "2026-09-08T16:09:33Z"
widths: [1280, 390]
metric: anchor_max_local_displacement_px
criterion: geometry
maximum_math_box_displacement_px: 1
---
# Reserved Math Bases Prevent Math-Induced Text Movement

Measured per-base geometry in the original HTML keeps math from changing neighboring
text positions while fonts load.
Accept only when an independent delayed-font check observes both sides of reveal and
measures at most one CSS pixel of math-box movement at desktop and mobile widths in
Chromium, Firefox, and WebKit.
The tolerance permits subpixel rounding; it does not permit a different line break.

Normal-load anchor measurements at both widths describe what a reader experiences.
They are not sufficient by themselves: no observed pre-reveal frame could make an
unstable page appear stable.
Require the probe’s known-movement negative control, correct initial parameters,
preserved equation wrapping, and the existing no-swap, early-input, failure,
accessibility, and print checks.
Record any non-math source of remaining text movement separately rather than attributing
it to prepared boxes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
