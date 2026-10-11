---
type: is
id: is-01m3w47ygabsgm59xrhd5tr411
title: "Site footer: two lines, the project and repository, then the version stamp and 'Formatted and typeset with Flowmark and KPress'"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T16:19:59.612Z
updated_at: 2026-10-01T19:39:33.368Z
closed_at: 2026-10-01T19:39:33.365Z
close_reason: "c2647bd1d, merged into jlevy/squares#276: two lines, 'The Squares Project · github.com/jlevy/squares' (linked) and the live stamp · 'Formatted and typeset with Flowmark and KPress' (both linked), from one definition for the KPress pages and both papers; the workbench has no footer."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: change the footer to: line 1 'The Square Packing Project · github.com/jlevy/squares'; line 2 'v0.4.2-8ac5de · Formatted and typeset with Flowmark and KPress'. The version stamp is the live one (the release version and data revision, as the atlas stamp prints it), not the literal; it becomes v0.5.0-… with the version bump (think-pt1k). github.com/jlevy/squares links the repository; Flowmark and KPress link their projects. The same footer on every page that has one: the KPress pages, the two papers, the workbench.

## Notes

Done on claude/site-polish-4-home, commit c2647bd1d: two-line footer from one definition render_overview.colophon_lines on KPress pages, the explainer and the optimality paper (workbench is an application with no footer). Stamp is sqpack.release.PUBLICATION_EDITION. Both lines print in the PDFs; explainer PDF still 22 pages; release.py added to the optimality paper's declared inputs.
