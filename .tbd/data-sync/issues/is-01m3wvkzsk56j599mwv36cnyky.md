---
type: is
id: is-01m3wvkzsk56j599mwv36cnyky
title: "The two papers share one structure: formats, credits, version and dates lines, and formatting"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T23:08:31.406Z
updated_at: 2026-10-02T00:00:59.081Z
closed_at: 2026-10-02T00:00:59.078Z
close_reason: "Merged as jlevy/squares#289 (merge f1575dbb7; commits 97e4069d5, 8cf99b715, f052e3033): devtools/paper_front.py writes both papers' formats row, credits, version and dates lines and both Markdown editions' fronts; devtools.paper_structure and tests/test_paper_structure.py hold every form axis equal. Four owner questions (review's version, its first-published day, repository line, 'Last revised' label) moved to think-cv22."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: about papers/n11-lower-bounds-explainer.html and papers/n11-optimality-review.html: 'formats, formatting, and all structure should be similar across these'. Both already serve HTML, Markdown and PDF with the same MD, PDF and GitHub chips, the same nav state, contents, footnotes and footer. Differences found on the live pages: the credits blocks differ in order and weight (the first paper: oversight, agents, a bold repository address, then 'First published … · Last revised …' and an edition line with a version-history link; the review: the original proof and its plain address, oversight, agents, 'Draft v0.1.0', then 'Original proof … · This review revised …', no version history); h1 treatment; and whatever a side-by-side audit finds in section structure, figure and table treatment, footnote and citation form, abstract or lead, Markdown and PDF editions (front matter, title block, page furniture). One component should produce both papers' title block, credits, formats row and closing; the owner's credits form for the review (names bold, addresses plain, version line plain, a break before the review's own credits) is the convention. Audit, align, test that the two cannot drift.
