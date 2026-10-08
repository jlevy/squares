---
type: is
id: is-01m4ehey13v9vk19xjacp842hy
title: "PR #456 review E3: render native frontier square roots correctly"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4edy0gkgv91t6evhbzeyk58
hold: null
hold_until: null
created_at: 2026-10-08T19:57:19.767Z
updated_at: 2026-10-08T19:59:15.226Z
started_at: 2026-10-08T19:59:15.224Z
---
BLOCKING High finding from fresh independent Astra MAX review: Chromium151 HTTPscreen/print paints n=5 as2+one-half times2 without square-root glyph or overbar, despite correct msqrt semantic markup. Structural/font checks falsely report359 readable/350 native roots/matching sans. Retained screenshots pr456-final-review-9tCYfs/chromium-http-nojs-{screen,print}-n5.png. Reviewer owns actual browser diagnosis/Firefox153/WebKit26.5 compatibility; independent Astra architecture advisor checks constructed-operator MATHfont versus reader-sans token fonts using primary sources. Require minimal production fix plus meaningful rendered-radical regression and all3engines/noJS/print/file-origin guards before candidate admission/CI/merge. No native candidate published; live site remainsKaTeX.
