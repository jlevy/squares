---
type: is
id: is-01m1vzcaw7nt6mevfa15cbm51x
title: Preview explainer typography, PDF layout, and reading guide
kind: task
status: open
priority: 2
version: 8
labels: []
dependencies: []
created_at: 2026-09-06T18:23:36.838Z
updated_at: 2026-09-06T19:46:13.202Z
---

## Notes

Local explainer preview is updated across prose, typography, credits, Further Reading, and print layout. Current scale: measure 40, H2 1.2, sans light/regular 430, medium 550, bold 680, with overrides together in explainer-shell.html. Credits and body both measure 18px screen and 12pt print; the typography diagnostic supports CSS selector filtering. The framework phrase links to the repository; redundant open-source and README sentences were removed. Further Reading groups project elements, framework, agent tools, and document tools with Burns/Massaccesi attribution. Moved the results count before the atlas sentence and clarified This lower bound; joined verification into the proof paragraph. Latest edits: credits say Human oversight; the weaker-certificate parenthetical is one sentence explaining its value for illustration; the final apparent-novelty/priority sentence was removed from the footnote. Updated the existing comparison test for the revised explanation. Markdown formatted, HTML and PDF rebuilt, 43 explainer tests and Ruff pass. Earlier BasedPyright and the print layout check passed. The latest PDF has 14 pages; changed pages 1, 4, and 14 were visually reviewed, and all other pages match the previously reviewed render. Paragraphs, equation/list introductions, boxes, captions, and reading groups stay together. Also fixed Markdown credit date extraction, revision-pinned document links, and URL-fragment handling. Changes remain uncommitted for user inspection.
