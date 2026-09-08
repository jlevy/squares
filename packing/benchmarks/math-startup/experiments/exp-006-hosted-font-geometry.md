---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-006
title: First hosted saved-setting geometry matrix
kind: geometry
hypotheses: [H-004]
measurements:
  - runs/ci-34270137119/firefox-1280-custom-sans-screen.json.gz
  - runs/ci-34270137119/firefox-1280-custom-serif-screen.json.gz
  - runs/ci-34270137119/firefox-1280-system-sans-screen.json.gz
  - runs/ci-34270137119/firefox-1280-system-serif-screen.json.gz
  - runs/ci-34270137119/firefox-390-custom-sans-screen.json.gz
  - runs/ci-34270137119/firefox-390-custom-serif-screen.json.gz
  - runs/ci-34270137119/firefox-390-system-sans-screen.json.gz
  - runs/ci-34270137119/firefox-390-system-serif-screen.json.gz
  - runs/ci-34270137119/webkit-1280-custom-sans-screen.json.gz
  - runs/ci-34270137119/webkit-1280-custom-serif-screen.json.gz
  - runs/ci-34270137119/webkit-1280-system-sans-screen.json.gz
  - runs/ci-34270137119/webkit-1280-system-serif-screen.json.gz
  - runs/ci-34270137119/webkit-390-custom-sans-screen.json.gz
  - runs/ci-34270137119/webkit-390-custom-serif-screen.json.gz
  - runs/ci-34270137119/webkit-390-system-sans-screen.json.gz
  - runs/ci-34270137119/webkit-390-system-serif-screen.json.gz
correctness: failed
judgment: The partial hosted matrix reports real width errors and WebKit formula loss; Chromium geometry was blocked by an earlier interaction-check failure. Missing cells and failed observations remain failures, not inferred passes.
---
# First Hosted Saved-Setting Geometry Matrix

[Pages dispatch 34270137119](https://github.com/jlevy/squares/actions/runs/34270137119)
tested the prepared `25e66d7b` artifact in Firefox and WebKit across all eight screen
settings per browser.
Chromium’s earlier print interaction check counted inactive MathML variants, so its
thirteen geometry observations never ran.
The [failed build log](../runs/pages-34270137119-build-failed.log.gz) is retained.
The complete H-004 requirement is twenty-nine observations, including the alternate
certificate, and this partial matrix cannot satisfy it.

All sixteen available reports retain width failures.
Firefox preserves formula counts; some WebKit settings lose formulas when hydration
falls back. Replaying the exact published HTML on the Mac also reproduces width errors.
The [follow-up investigation](../explorations/X-004-hosted-rendering.md) separates
platform-dependent glyph rounding from the guard’s serial response-release delay.
Neither finding authorizes a looser tolerance or a longer runtime deadline.

The interaction check now filters semantic fractions by the selected font variant.
Its [complete local replay](../runs/print-layout-25e-active-variants.json.gz) against
the unchanged CI HTML passes with the corrected instrument; its
[overflow and bullet controls](../runs/print-layout-25e-controls.log.gz) also pass.
These instrument repairs do not erase the original CI failure or establish correctness
of the pending rebuilt publication.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
