---
softschema:
  contract: squares.math-startup.experiment.v1
  schema: ../schemas/experiment.schema.yaml
  status: enforced
id: exp-010
title: Protected queued math passes every registered font setting
kind: geometry
hypotheses: [H-004]
measurements:
  - runs/ci-34283695063/chromium-1280-custom-sans-print.json.gz
  - runs/ci-34283695063/chromium-1280-custom-sans-screen.json.gz
  - runs/ci-34283695063/chromium-1280-custom-serif-print.json.gz
  - runs/ci-34283695063/chromium-1280-custom-serif-screen-alternate-certificate.json.gz
  - runs/ci-34283695063/chromium-1280-custom-serif-screen-controls.json.gz
  - runs/ci-34283695063/chromium-1280-system-sans-print.json.gz
  - runs/ci-34283695063/chromium-1280-system-sans-screen.json.gz
  - runs/ci-34283695063/chromium-1280-system-serif-print.json.gz
  - runs/ci-34283695063/chromium-1280-system-serif-screen.json.gz
  - runs/ci-34283695063/chromium-390-custom-sans-screen.json.gz
  - runs/ci-34283695063/chromium-390-custom-serif-screen.json.gz
  - runs/ci-34283695063/chromium-390-system-sans-screen.json.gz
  - runs/ci-34283695063/chromium-390-system-serif-screen.json.gz
  - runs/ci-34283695063/firefox-1280-custom-sans-screen.json.gz
  - runs/ci-34283695063/firefox-1280-custom-serif-screen.json.gz
  - runs/ci-34283695063/firefox-1280-system-sans-screen.json.gz
  - runs/ci-34283695063/firefox-1280-system-serif-screen.json.gz
  - runs/ci-34283695063/firefox-390-custom-sans-screen.json.gz
  - runs/ci-34283695063/firefox-390-custom-serif-screen.json.gz
  - runs/ci-34283695063/firefox-390-system-sans-screen.json.gz
  - runs/ci-34283695063/firefox-390-system-serif-screen.json.gz
  - runs/ci-34283695063/webkit-1280-custom-sans-screen.json.gz
  - runs/ci-34283695063/webkit-1280-custom-serif-screen.json.gz
  - runs/ci-34283695063/webkit-1280-system-sans-screen.json.gz
  - runs/ci-34283695063/webkit-1280-system-serif-screen.json.gz
  - runs/ci-34283695063/webkit-390-custom-sans-screen.json.gz
  - runs/ci-34283695063/webkit-390-custom-serif-screen.json.gz
  - runs/ci-34283695063/webkit-390-system-sans-screen.json.gz
  - runs/ci-34283695063/webkit-390-system-serif-screen.json.gz
correctness: passed
judgment: All twenty-nine required observations pass with complete reservations, zero movement, and intrinsic width agreement within one pixel. The retained controls reject broken widths, missing reservations, font metrics, carrier struts, queue protection, print selection, and native fallback; accept the geometry correction for this exact source.
---
# Protected Queued Math Passes Every Registered Font Setting

[Pages dispatch 34283695063](https://github.com/jlevy/squares/actions/runs/34283695063)
checks the [candidate retained by exp-009](../fixtures/candidate-dab2a381.gz) at
`dab2a3818f661311b130ca2f2360ffad5627db65`. All twenty-nine reports identify that source
and a clean instrument checkout.
The matrix contains all four saved font settings at both registered widths in Chromium,
Firefox, and WebKit, all four Chromium print settings, and the alternate certificate.

Every screen observation retains 164 formulas and 261 reserved bases before and after
reveal. Every print observation retains 140 formulas and 223 bases.
All observations hold real math-font transfers and complete a hidden-to-visible
transition without missing reservations or changed line breaks.
The
[generated ledger](../ledger.md#exp-010-protected-queued-math-passes-every-registered-font-setting)
computes zero movement in every cell and final intrinsic width error below one pixel.

The
[default Chromium report](../runs/ci-34283695063/chromium-1280-custom-serif-screen-controls.json.gz)
retains rejected controls for hinted metrics, nonlinear scaling, removed widths,
consistently wrong widths, missing entire reservations, and an unreserved carrier strut.
Its queue check observes 153 unsubmitted formulas still hidden after the root watchdog
has expired, while thirteen actual font transfers remain held.
Removing their queue protection exposes those formulas and is rejected.
After release, no queue markers or unreadable math remain.
The host controls reject the intentionally wrong print certificate and broken native
fallback. Ordinary host checks also pass in Firefox and WebKit.

The [workflow receipt](../runs/ci-34283695063/pages-run.json.gz),
[Chromium build log](../runs/ci-34283695063/pages-build.log.gz),
[Firefox log](../runs/ci-34283695063/pages-firefox.log.gz), and
[WebKit log](../runs/ci-34283695063/pages-webkit.log.gz) retain the completed loading,
input, no-JavaScript, fallback, typography, reload, and export checks.
These results repair the incomplete and failed matrix in exp-008 without deleting that
earlier evidence or relaxing its tolerance.
Later main-branch integration is outside this frozen candidate and needs its own
correctness validation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
