---
type: is
id: is-01m0v0z3ve6y0n6bc9e0ddwh1w
title: Migrate the exact n=3 quotient map onto the shared SVG spine
kind: task
status: open
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - known-answer
dependencies:
  - type: blocks
    target: is-01m0v0zahjq54tvtm1sxr0c9yx
  - type: blocks
    target: is-01m0v102z22dxytc6atqpnszdz
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:24.557Z
updated_at: 2026-08-24T23:16:56.417Z
---
Files: tools/check_small_n_moduli.py and atlas/n-003-optimal-moduli.svg. Rename svg_text to render_n3_moduli_svg and replace hand-built XML with shared svg.py helpers, number formatting, accessibility handling, and visual tokens while keeping the quotient layout domain-specific. Preserve the two labelled 12-cycles, unlabelled four-cycle, D4 x S3 interval, three packing glyphs, semantic IDs, active-signature/stabilizer distinctions, source description, and retained path. Update the golden only after deliberate diff review; done when the exact JSON model and SVG both replay byte for byte and existing negative controls still fire.
