---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-003
title: Prepared publication across browsers and print
kind: geometry
hypotheses: [H-001]
measurements:
  - runs/geometry-chromium-1280.json.gz
  - runs/geometry-chromium-390.json.gz
  - runs/geometry-firefox-1280.json.gz
  - runs/geometry-firefox-390.json.gz
  - runs/geometry-webkit-1280.json.gz
  - runs/geometry-webkit-390.json.gz
  - runs/geometry-chromium-1280-print.json.gz
  - runs/geometry-chromium-390-print.json.gz
  - runs/geometry-chromium-1280-alternate.json.gz
correctness: passed
judgment: Accept the reserved initial geometry; all registered browser/width cells retain their layout across real font arrival, with unchanged wrapping and rejected fault controls.
---
# Prepared Publication Across Browsers and Print

All checks consume the same prepared artifact built from Squares `dc2eb681` and KPress
`345b9eb`. A second complete preparation reproduced the HTML byte for byte.
The reports retain the original source identity, Git state, browser version, viewport,
media, process arguments, before/after boxes, and complete diagnostic findings.
The browser comparisons use different font advances during the hold, so a matching
fallback font cannot conceal an ineffective width reservation.
These observations use the default custom-serif setting.
They do not cover saved sans or system settings; the later integration review found
reservation loss in those contexts and tracked its correction separately as
`think-fatc`.

The desktop Chromium report retains both geometry negative controls: removing the
reserved width changes positions, while adding a consistently wrong width preserves
positions but disagrees with the final glyphs.
Both are rejected. It also retains the old print-visibility and native-fallback host
branches as rejected controls.
Print geometry and the initially hidden alternate certificate pass separately.

The independent loading probe passes in [Chromium](../runs/loading-chromium.json.gz),
[Firefox](../runs/loading-firefox.json.gz), and
[WebKit](../runs/loading-webkit.json.gz).
Each report retains four rejected controls: early exposure, dropped early input, an
unavailable later font family, and clipped no-JavaScript fallback.
These correctness probes deliberately perturb readiness; they provide no normal-load
latency claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
