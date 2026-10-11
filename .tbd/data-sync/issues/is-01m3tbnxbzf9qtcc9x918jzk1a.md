---
type: is
id: is-01m3tbnxbzf9qtcc9x918jzk1a
title: Math inside sans text is sans math on every site surface
kind: bug
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:51:28.382Z
updated_at: 2026-10-01T04:50:46.273Z
closed_at: 2026-10-01T04:50:46.271Z
close_reason: "Done in 2d59db74f on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. measure_site_pages math over 20 pages at two widths: no formula is set serif inside sans text; tests/test_site_math_faces.py walks the pages with a negative control."
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: math within a sans context is sans math. think-g63b (4cfb962e6) set math in the face of the text around it via host_math_init.js isSansContext; audit every sans context on the built site (cards and their notes, chips, tables, popovers, nav, captions, the Visualize and case pages) in the preview, list any formula still typeset in the serif inside sans text, and fix the face detection or markup so none remains; add a check that walks the pages.
