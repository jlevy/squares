---
softschema:
  contract: squares.math-startup.exploration.v1
  schema: ../schemas/exploration.schema.yaml
  status: enforced
id: X-004
title: Hosted evidence separates font rounding and startup scheduling
proposes: [H-005]
---
# Hosted Evidence Separates Font Rounding and Startup Scheduling

The first hosted candidate fails geometry and the desktop speed criterion.
Its retained HTML reproduces the width errors on the Mac too; the failure is in
published reservations, rather than a Linux reader alone.
KaTeX’s default text-rendering policy permits Linux Chromium to round glyph advances.
Those measured pixels are not portable across platforms or changes in text size;
normalizing them into em units alone does not preserve their final width.
The host must request linear glyph positioning and validate the resulting preparation.
[Chromium’s font policy](https://github.com/chromium/chromium/blob/main/third_party/blink/renderer/platform/fonts/font_platform_data.cc)
explicitly enables subpixel positioning and disables hinting for geometric precision.

The held-transfer guard also released font responses serially.
That work could consume much of the runtime’s unchanged three-second recovery ceiling.
Release held responses concurrently and retain their timing; do not enlarge the runtime
deadline or the one-pixel geometry tolerance.
H-004 continues to own correctness of the repaired candidate.

The parameter trace shows a separate scheduling delay.
Hundreds of hydration calls issue font requests in one synchronous batch, after the
interactive certificate boots.
Individual waits are much shorter than the interval from navigation to the last font
promise resolving. Prioritize interactive panel mathematics and let readiness callbacks
and painting proceed between bounded batches.
Settlement must cover queued work as well as issued requests, so deferred heat maps and
PDF export still wait for the complete intended work.
H-005 uses a fresh comparison with the unchanged numerical and observer-cost criteria.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
