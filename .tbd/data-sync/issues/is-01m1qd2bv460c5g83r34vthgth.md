---
type: is
id: is-01m1qd2bv460c5g83r34vthgth
title: "Certificate page: footnote hover previews do not appear"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - explainer
  - pr-79
  - kpress
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-04T23:46:38.050Z
updated_at: 2026-09-05T00:04:03.786Z
closed_at: 2026-09-05T00:04:03.785Z
close_reason: Commit 387c3508, verified in the browser.
resolution: null
duplicate_of: null
---
Review feedback on PR #79. The footnotes use kpress's markup but the previews are kpress's tooltips.js, an ES module over overlay.js, viewport.js and runtime.js, which the self-contained page does not load. Bundle those modules into the page from the kpress distribution (as KaTeX already is), call initKpressTooltips for footnotes after boot, and verify the preview appears on hover. think-vnph asks kpress for a standalone bundle so this local bundling can go.
