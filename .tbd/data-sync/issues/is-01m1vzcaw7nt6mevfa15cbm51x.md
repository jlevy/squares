---
type: is
id: is-01m1vzcaw7nt6mevfa15cbm51x
title: Preview explainer typography, PDF layout, and reading guide
kind: task
status: open
priority: 2
version: 11
labels: []
dependencies: []
created_at: 2026-09-06T18:23:36.838Z
updated_at: 2026-09-06T20:14:50.150Z
---

## Notes

Local preview includes the requested prose, credit, Further Reading, Figure 3 label, typography, and print-layout edits. Current typography: measure 40, H2 scale 1.2, sans base 18.5px against 18px serif prose, regular/light 410, medium 550, bold 680. Sans overrides stay together locally; print preserves the size ratio and uses 1.32 caption/footnote leading. Print now resets normal and muted text roles to solid black across KPress scopes, including theme/palette selectors; page numbers are black too. This covers prose, captions, figure labels, footnotes, and colophon while preserving the screen styling and colored links. HTML and PDF rebuilt. All 43 explainer tests pass; git diff --check passes. The 14-page PDF has identical text and line/page breaks to the previously reviewed version. Visually checked the updated Figure 3/captions and Further Reading/footnotes/colophon. Previous font and print-layout audits passed, as did Ruff and BasedPyright for code changes. The diagnostic supports selector filtering. All changes remain uncommitted for user inspection.
