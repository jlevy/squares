---
type: is
id: is-01m1vzcaw7nt6mevfa15cbm51x
title: Preview explainer typography, PDF layout, and reading guide
kind: task
status: open
priority: 2
version: 9
labels: []
dependencies: []
created_at: 2026-09-06T18:23:36.838Z
updated_at: 2026-09-06T19:50:48.673Z
---

## Notes

Local explainer preview is updated across prose, typography, credits, Further Reading, and print layout. Current scale: measure 40, H2 1.2, sans light/regular 430, medium 550, bold 680, with overrides together in explainer-shell.html. Credits and body both measure 18px screen and 12pt print; the typography diagnostic supports CSS selector filtering. The framework phrase links to the repository; redundant open-source and README sentences were removed. Further Reading groups project elements, framework, agent tools, and document tools with Burns/Massaccesi attribution. Moved the results count before the atlas sentence and clarified This lower bound; joined verification into the proof paragraph. Credits say Human oversight; the weaker-certificate parenthetical explains its value for illustration in one sentence; the final apparent-novelty/priority sentence was removed from the footnote. Updated the comparison test for the revised explanation. Fixed Figure 3: certificate labels now descend from the largest bound, so longer leaders remain left of the labels above them. Reviewed enlarged before/after PDF crops; both labels are clear, and only page 4 differs from the previously reviewed render. HTML and PDF rebuilt; 43 explainer tests and Ruff pass. Earlier BasedPyright and print layout checks passed. PDF remains 14 pages with clean breaks. Also fixed Markdown credit date extraction, revision-pinned document links, and URL-fragment handling. Changes remain uncommitted for user inspection.
