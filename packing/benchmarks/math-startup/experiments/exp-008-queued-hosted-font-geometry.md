---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-008
title: Linear geometry passes screen checks but fails hosted print
kind: geometry
hypotheses: [H-004]
measurements:
  - runs/ci-34274946315/chromium-1280-custom-sans-print.json.gz
  - runs/ci-34274946315/chromium-1280-custom-sans-screen.json.gz
  - runs/ci-34274946315/chromium-1280-custom-serif-print.json.gz
  - runs/ci-34274946315/chromium-1280-custom-serif-screen-alternate-certificate.json.gz
  - runs/ci-34274946315/chromium-1280-custom-serif-screen-controls.json.gz
  - runs/ci-34274946315/chromium-1280-system-sans-print.json.gz
  - runs/ci-34274946315/chromium-1280-system-sans-screen.json.gz
  - runs/ci-34274946315/chromium-1280-system-serif-print.json.gz
  - runs/ci-34274946315/chromium-1280-system-serif-screen.json.gz
  - runs/ci-34274946315/chromium-390-custom-sans-screen.json.gz
  - runs/ci-34274946315/chromium-390-custom-serif-screen.json.gz
  - runs/ci-34274946315/chromium-390-system-sans-screen.json.gz
  - runs/ci-34274946315/chromium-390-system-serif-screen.json.gz
  - runs/ci-34274946315/firefox-1280-custom-sans-screen.json.gz
  - runs/ci-34274946315/firefox-1280-custom-serif-screen.json.gz
  - runs/ci-34274946315/firefox-1280-system-sans-screen.json.gz
  - runs/ci-34274946315/firefox-1280-system-serif-screen.json.gz
  - runs/ci-34274946315/firefox-390-custom-sans-screen.json.gz
  - runs/ci-34274946315/firefox-390-custom-serif-screen.json.gz
  - runs/ci-34274946315/firefox-390-system-sans-screen.json.gz
  - runs/ci-34274946315/firefox-390-system-serif-screen.json.gz
correctness: failed
judgment: All sixteen completed screen settings and the alternate certificate pass, but three Chromium print settings move beyond one pixel. WebKit stops at an earlier first-exposure failure, so eight required screen cells are missing. Preserve all twenty-one reports without inferring absent passes.
---
# Linear Geometry Passes Screen Checks but Fails Hosted Print

[Pages dispatch 34274946315](https://github.com/jlevy/squares/actions/runs/34274946315)
uses the same [prepared candidate](../fixtures/candidate-d122d19c.html.gz) at
`d122d19cffb1b59c86ce57a02838f0c70438e978` as exp-007. All twenty-one available reports
identify that source and a clean instrument checkout.

Chromium and Firefox complete every screen setting at both widths.
Each observation retains 164 formulas and 261 reserved bases before and after reveal.
Chromium’s alternate certificate also passes.
All four print settings retain 140 formulas and 223 bases, but custom-serif moves by up
to 29.953 pixels and both system settings by 7.0625 pixels.
Only custom-sans print passes.
Final intrinsic width agreement remains within one pixel; the failed observations
concern vertical positions and baselines.

The default Chromium report retains rejected hinted-metric, nonlinear-scaling,
removed-width, stable-wrong-width and missing-reservation controls.
Its host controls also reject the intentionally wrong print certificate and broken
native fallback. These controls do not waive the measured print failures.

The [WebKit log](../runs/ci-34274946315/pages-webkit-failed.log.gz) records the earlier
first-exposure failure.
Its eight geometry cells never run, and the artifact upload reports no geometry files.
The complete H-004 matrix is therefore both failed and incomplete.
The [evaluation](../runs/ci-34274946315/evaluation.json.gz) retains every available
finding and the reporter’s missing-coverage result.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
