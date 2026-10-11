---
type: is
id: is-01m4ehey13v9vk19xjacp842hy
title: "PR #456 review E3: render native frontier square roots correctly"
kind: bug
status: closed
priority: 1
version: 3
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4edy0gkgv91t6evhbzeyk58
hold: null
hold_until: null
created_at: 2026-10-08T19:57:19.767Z
updated_at: 2026-10-08T21:46:18.994Z
started_at: 2026-10-08T19:59:15.224Z
closed_at: 2026-10-08T21:46:18.992Z
close_reason: Fixed in e047331, independently reviewed in formal E5463107477 with disposition6069502067 and merged91ca9b8. Native structural math font restores actual hook and overbar; healthy and inherited-Sans-mutant paint controls pass screen/print on Chromium, Firefox and WebKit macOS. Exact-tree Linux frontend run37847037044/job113550357940 executes both paint tests and all207 site-layout tests with zero skips. Required PR packing/pages aggregates bothSUCCESS; final live rollout remains separately tracked in think-7wlz.
resolution: null
duplicate_of: null
---
BLOCKING High finding from fresh independent Astra MAX review: Chromium151 HTTPscreen/print paints n=5 as2+one-half times2 without square-root glyph or overbar, despite correct msqrt semantic markup. Structural/font checks falsely report359 readable/350 native roots/matching sans. Retained screenshots pr456-final-review-9tCYfs/chromium-http-nojs-{screen,print}-n5.png. Reviewer owns actual browser diagnosis/Firefox153/WebKit26.5 compatibility; independent Astra architecture advisor checks constructed-operator MATHfont versus reader-sans token fonts using primary sources. Require minimal production fix plus meaningful rendered-radical regression and all3engines/noJS/print/file-origin guards before candidate admission/CI/merge. No native candidate published; live site remainsKaTeX.
