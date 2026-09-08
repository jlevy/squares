---
softschema:
  contract: squares.math-startup.hypothesis.v1
  schema: ../schemas/hypothesis.schema.yaml
  status: enforced
id: H-004
title: Every saved font setting retains complete initial math geometry
derived_from: [X-003]
registered: "2026-09-08T18:46:14Z"
widths: [1280, 390]
metric: math_box_displacement_px
criterion: geometry
maximum_math_box_displacement_px: 1
font_contexts: [custom-serif, custom-sans, system-serif, system-sans]
---
# Every Saved Font Setting Retains Complete Initial Math Geometry

The default-only geometry result does not establish stability for other saved font
settings. Integration review found that hydration discarded mismatched reservations, and
that surviving caption boxes could conceal the missing prose boxes.
The correction prepares each supported context and selects it through CSS before paint.

Require all four saved setting combinations at both registered widths in Chromium,
Firefox, and WebKit.
Each run must hold actual math-font transfers, observe reveal, retain line breaks, and
stay within one CSS pixel of its initial geometry and final intrinsic widths.
Every visible formula base must have a reservation before and after reveal.
Missing coverage invalidates a run even when surviving boxes do not move.

Require rejected controls for a removed width, a consistently wrong width, and an entire
reservation removed before discovery.
Check all four settings in Chromium print mode, plus the existing alternate-certificate,
failure, no-JavaScript, first-exposure, and early-input behavior.
This is a correctness extension; it makes no latency claim and does not change H-003’s
acceptance rule.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
