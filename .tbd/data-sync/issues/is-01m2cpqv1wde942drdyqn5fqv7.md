---
type: is
id: is-01m2cpqv1wde942drdyqn5fqv7
title: Bind the deployed PDF receipt to the served explainer HTML
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2cge1zdgenaswpf8nmd9fmv
created_at: 2026-09-13T06:19:42.011Z
updated_at: 2026-09-13T06:19:42.011Z
---
The final deployment review found check_published_site only checks PDF format/page count, so an old 22-page PDF can pass beside a new HTML edition. Validate its single canonical trailing sqpack-source-html-sha256 receipt against the fetched HTML bytes; retain negative controls for missing, malformed, duplicate, and wrong-source receipts. This is a staleness check, not a tamper guarantee.
