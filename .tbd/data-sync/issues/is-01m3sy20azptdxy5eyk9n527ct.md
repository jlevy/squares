---
type: is
id: is-01m3sy20azptdxy5eyk9n527ct
title: Site pages share the explainer's text layout and math pipeline, with a contents rail
kind: feature
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T19:53:24.573Z
updated_at: 2026-09-30T19:53:26.142Z
closed_at: 2026-09-30T19:53:26.141Z
close_reason: Done on claude/overview-page-impl in 60091c2e2, 7b06e5852, 13501d66a, ea7882790 and d700c2fcc.
resolution: null
duplicate_of: null
---
No bead was ever created (the rail fix was sandbox think-zr1a). templates/paper-type.css carries the explainer's text tokens to the doc pages; overview/math.js typesets through the explainer's KaTeX bundle in batches; devtools.measure_site_pages is the reusable load and typography measurement (synopsis DOMContentLoaded about 14 s to 1.1 s). Doc and report pages centre the reading column beside kpress's contents rail, whose scroll-spy now works.
