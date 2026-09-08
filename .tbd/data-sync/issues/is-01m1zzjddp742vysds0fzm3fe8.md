---
type: is
id: is-01m1zzjddp742vysds0fzm3fe8
title: Debug font loading, sans math, and related explainer rendering; integrate fixes and CI
kind: task
status: closed
priority: 1
version: 11
labels: []
dependencies: []
child_order_hints:
  - is-01m1zzsrn7qbfgpnhx90mnvdc4
  - is-01m1zzss1fezvthwvd2xzcnb1m
  - is-01m1zzssc6t2mn96vsjt7cn7xz
  - is-01m1zzsspkf31ysgtq60kwqy2p
  - is-01m202z7qaaz5116n2096jkcjd
  - is-01m204vpqppwzxg5br84yr98cr
created_at: 2026-09-08T07:43:53.780Z
updated_at: 2026-09-08T10:53:01.857Z
closed_at: 2026-09-08T10:53:01.856Z
close_reason: "Reviewed recent font PRs with three subagents, reproduced and fixed font swapping, sans caption adoption, fallback/metric errors, print readiness, browser guard gaps, and CI failures. KPress #59/#60 and Squares #128 are merged; the live v0.2.4-33cd4760 page and PDF pass retained rendering checks. All pre-merge and post-merge CI passed. Audit children are closed; existing subsetting, mono-adoption, and CI performance follow-ups remain separately tracked."
resolution: null
duplicate_of: null
---
W7 pipeline-improvement. User requests review of recent font PRs, reproduce transient math font swapping and serif math in sans captions, inspect other related rendering defects, track fixes as beads, implement in squares or KPress at the cleanest boundary, validate CI and merge correctly. Three bounded delegates review PR history, KPress pipeline, caption behavior; coordinator owns reproduction, integration, records, and merges.

## Notes

Implemented and merged in Squares PR #128 at 33cd47606dae223664f117945631440aa5c8ece9,
with KPress PRs #59 and #60 pinned at 7b20ae702acf37020e6132265c8faa0ba74e4465. Shared
rendering now selects matching serif, sans, or stock font metrics and waits for every
face needed by the formula before exposing it.
Article math and dynamic figure readouts use the same rendering boundary.
Native MathML and raw TeX remain readable when enhancement is unavailable.

Pre-merge fast validation, the complete deferred complement, and Pages passed on the
exact source tree later merged to main.
The post-merge Pages run also passed, including Chromium, Firefox, WebKit, reproducible
PDF, print layout, typography, and actual-font checks:
https://github.com/jlevy/squares/actions/runs/34214731528.

The deployed public page reports v0.2.4-33cd4760. All three live delayed-font probes
passed with no findings; each held 36 font-load promises, retained four early slider
targets, exposed no intermediate math, and verified 124 native formulas plus five
raw-TeX fallbacks without JavaScript.
The actual-face probe verified 199 formulas, including 80 sans instances: Source Sans
caption/readout letters and digits, PT Serif prose, and KPress Print Sans caption digits
in print, with matching metric geometry.
Desktop and mobile captures and all seven figure-caption PDF pages were visually
reviewed. Required-font failures, missing composite declarations, nested stock opt-outs,
and deliberately broken loading controls are covered by retained regressions.

Live evidence is retained in /tmp/squares-font-live-chromium.json,
/tmp/squares-font-live-firefox.json, /tmp/squares-font-live-webkit.json,
/tmp/squares-font-live-faces.json, and /tmp/squares-font-live/. Reusable checkers are
packing/devtools/check_math_loading.py and packing/devtools/check_math_faces.py.
The original PR #128 page at c1dab812 fails the loading probe.
Font subsetting and remaining mono adoption remain open under think-f8q9 and think-9r58.

The deployed PDF was downloaded separately and checked with the retained font_findings
and provenance audit.
It is a tagged, 17-page, 804,701-byte PDF carrying v0.2.4-33cd4760, with no font
findings and only DejaVuSansMono reported under the documented kpr-v731 exception.
The public PDF was also visually spot-checked.
Its byte size differs from the macOS local export because the hosted renderer and
allowed atlas/mono faces differ; this is not a font-size improvement measurement.

Full post-merge numerical CI passed on 33cd4760 in run 34214731500, with all five
applicable jobs successful: https://github.com/jlevy/squares/actions/runs/34214731500.
The main merge contains both original CI repair heads from PRs #122 and #123, and GitHub
marks those PRs merged as well as #128. The checkout is clean.
All work in this rendering audit is implemented, merged, deployed, and verified.
CI performance follow-up remains on think-ph9v, alongside the separate font subsetting
and mono-adoption follow-ups.
