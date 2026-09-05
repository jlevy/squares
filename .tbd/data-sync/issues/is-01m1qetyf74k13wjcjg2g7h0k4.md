---
type: is
id: is-01m1qetyf74k13wjcjg2g7h0k4
title: "Markdown article: convert the prose, math and footnotes from the HTML template"
kind: task
status: closed
priority: 1
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1qekyhf4hjcavbdm3xya0bt
created_at: 2026-09-05T00:17:32.134Z
updated_at: 2026-09-05T00:41:24.293Z
closed_at: 2026-09-05T00:41:24.292Z
close_reason: "certificate_page.md written from the template: 465 lines, 78 math spans whole under flowmark 0.4.0 and idempotent, kpress renders it with 8 headings, 6 figures, 69+9 math elements and 3 notes; word-level fidelity against the template clean."
resolution: null
duplicate_of: null
---
Create packing/devtools/templates/certificate_page.md: Markdown with $…$ math, [^n] footnotes, {.class} attrs, ::: boxed-text; figures as raw HTML blocks with <span class="tex"> math; the same placeholders and BEGIN/END markers; flowmark-clean and idempotent; every math span whole. Delegated.
