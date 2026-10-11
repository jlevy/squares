---
type: is
id: is-01m3tbfnx8y6phx0hhrypdqwkx
title: Render the separate T-060 paper with shared KPress typography and checked PDF output
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality.md
delegate: native_sol
labels: []
dependencies: []
parent_id: is-01m3qw1d6z2hnprytp2r49qe4f
created_at: 2026-09-30T23:48:04.135Z
updated_at: 2026-10-01T00:29:03.986Z
closed_at: 2026-10-01T00:29:03.974Z
close_reason: "PR259 at a3fd9510: reusable 264-line renderer emits offline HTML/Markdown and 16-page PDF; 135 math hosts render without errors. Dedicated hosted optimality job110160194859 passed real browser controls, source-bound figure tests, render/check and artifact upload. Parent think-08pw retains merge/deployment integration."
resolution: null
duplicate_of: null
---
Reuse the existing explainer design system without copying its certificate-specific runtime. Add a reproducible standalone HTML/Markdown/PDF build, source-bound figure insertion and focused rendering tests. Preserve the historical explainer. Verify rendered math, pagination and fonts.
