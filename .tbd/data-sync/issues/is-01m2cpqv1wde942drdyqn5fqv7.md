---
type: is
id: is-01m2cpqv1wde942drdyqn5fqv7
title: Bind the deployed PDF receipt to the served explainer HTML
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2cge1zdgenaswpf8nmd9fmv
created_at: 2026-09-13T06:19:42.011Z
updated_at: 2026-09-13T07:07:21.769Z
closed_at: 2026-09-13T07:07:21.769Z
close_reason: Implemented and independently reviewed in PR149 8d0a3ff2, inherited unchanged by PR156 52e4ab65. Exact stored PDF bytes and source receipt are validated; visible raw TeX, queued math and render errors are refused before export; live PDF receipts bind to fetched HTML. All six real browser controls and final artifact checks pass in both final-head Pages workflows (34743959872 and 34743978490). Full affected local gates and final hosted packing checks pass. Raw mismatch evidence is uploaded with seven-day retention; download before rerunning because GitHub can discard earlier-attempt artifacts. The intermittent PDF root cause remains separate under think-ptit.
resolution: null
duplicate_of: null
---
The final deployment review found check_published_site only checks PDF format/page count, so an old 22-page PDF can pass beside a new HTML edition. Validate its single canonical trailing sqpack-source-html-sha256 receipt against the fetched HTML bytes; retain negative controls for missing, malformed, duplicate, and wrong-source receipts. This is a staleness check, not a tamper guarantee.
