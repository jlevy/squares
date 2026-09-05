---
type: is
id: is-01m1sj3bd92ye5hrffxr5cw530
title: "Print: a page break can land right after a section heading"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T19:53:02.121Z
updated_at: 2026-09-05T19:53:02.121Z
---
Headings need break-after: avoid (and orphans/widows handling) so a heading is never the last thing on a page. This belongs in kpress's print stylesheet rather than in the explainer's shell; kpress is vendored at vendor/kpress on branch squares/page-fixes, so the fix is a PR there. Check whether kpress already sets it and, if so, why it is not taking effect for this page.
