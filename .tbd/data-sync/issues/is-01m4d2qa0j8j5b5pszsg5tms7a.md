---
type: is
id: is-01m4d2qa0j8j5b5pszsg5tms7a
title: Export a compact web index and lazy exact-value payloads
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-web-export
labels: []
dependencies: []
parent_id: is-01m4d2n7hjcxy6nh0wkvy8bpmj
hold: null
hold_until: null
created_at: 2026-10-08T06:20:31.121Z
updated_at: 2026-10-08T07:53:39.028Z
started_at: 2026-10-08T06:20:37.159Z
closed_at: 2026-10-08T07:53:39.027Z
close_reason: null
resolution: null
duplicate_of: null
---
Own render_exact_side_values.py, new devtools/exact_catalogue.py and their Python tests. Preserve full render()/Markdown/PDF mathematics; publish compact canonical web view, complete archive HTML, lazy entry metadata and coefficient-string payloads. No record admission changes; root owns docs/CI/metrics and sole commits.

## Notes

Delivered in 6900cb94207eeea589dbcf3cb8c75a45eabbb633 and PR435. Deterministic index plus per-entry metadata and exact descending integer-string vectors; complete HTML/Markdown/PDF remain separate archives. Exporter refuses unsafe/symlink payload paths and detects missing/stale/extra files. Renderer/export/control selection passed locally; coordinator final focused web selection passed 57 tests, and clean-head real archives rendered and passed --check. Parent think-mo36 owns remaining hosted integration.
