---
type: is
id: is-01m1zb00ss66pjnhm5rw9nawk1
title: "kpress: export the print-fonts wait and the print sans family from the package"
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-08T01:44:19.502Z
updated_at: 2026-09-08T01:44:30.822Z
---
PR #118 review S118-R2 and S118-R8. Two things this page needs from kpress live outside the kpress distribution:

1. `kpress.format.pdf._await_print_fonts` (with `_MARGIN_BOX_FONT_TOKENS`, `_MARGIN_BOX_SAMPLE` and `_PRINT_FONTS_READY_JS`) is private, so `packing/devtools/render_explainer_pdf.py` mirrors the margin-box step instead of calling it. The duplication is what let the step go missing in the first place.
2. The print sans family (`KPress Print Sans`) is exported only by `vendor/kpress/devtools/instance_sans.py`, repository content the wheel does not ship, so `packing/devtools/render_explainer.print_sans_family` and `packing/devtools/sans_instances.py` load it by path. A checkout that installed kpress as a wheel could not render the page at all.

Ask kpress for a public print-fonts wait and a family constant on `kpress.format`; then drop the mirrored block and read the family from the package, keeping the generator as the fallback.
