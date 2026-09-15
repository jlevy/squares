---
type: is
id: is-01m2h764pcbfwx0btxez85zdsq
title: Extract JavaScript from the explainer, print and math tools and their tests
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:05.578Z
updated_at: 2026-09-15T00:24:18.478Z
---
Extract every JavaScript string from the explainer, print and math tooling into probe files, with behaviour unchanged. About 1,700 lines in:

- `packing/devtools/`: `check_print_layout.py` (415 lines), `inspect_explainer_typography.py` (267), `check_math_loading.py` (236), `render_explainer_pdf.py` (206), `render_explainer.py` (105), `sans_instances.py` (86), `check_math_faces.py` (72), `compare_math_fonts.py` (50), `prepare_explainer_math.py` (25), `check_katex.py` (20), `check_scroll_restoration.py` (20), `check_published_site.py` (5) and `check_math_startup.py` (3);
- `packing/tests/`: `test_check_print_layout.py` (121) and `test_pdf_math_browser.py` (87).

Acceptance: these files leave the guard's allowlist; the render and print checks produce byte-identical output where they are deterministic; the affected tests pass; and each new probe is formatted and linted by Biome and type-checked.
