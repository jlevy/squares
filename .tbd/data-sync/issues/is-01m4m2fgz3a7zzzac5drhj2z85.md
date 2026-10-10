---
type: is
id: is-01m4m2fgz3a7zzzac5drhj2z85
title: Reconcile upstream paper metadata with the current website organization
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T23:30:57.122Z
updated_at: 2026-10-10T23:36:38.736Z
started_at: 2026-10-10T23:31:09.102Z
---
Resolve only overview_sections.py, papers-article.md, and test_overview.py conflicts while consolidating origin/main8fc983414 into the website branch. Preserve Home/Visuals/Row default, immutable full-poster card assets and author credits; adopt upstream shared canonical Title Case paper records/descriptions and methods-survey figures/link prose. Keep PDFs on Papers, current navigation and Results routes. Stage these three resolutions only; final merge/CI belongs to root.

## Notes

Resolved and staged only overview_sections.py, papers-article.md and test_overview.py for the in-progress merge of8fc98341411ecf22bd045cef96ca6fe0946a615e into774d2dbb466a4b932b44a8cc5490a2dc23599feb. Shared PaperRecord titles and PAPER_DESCRIPTIONS adopted; one comprehension includes all4papers, TUTORIAL_TITLE shared. Mannaseh Ahmed credit, current Papers PDF section/footer, Home/Visuals/Row/image code preserved. Methods link uses upstream title/path placeholders and names its actual retained-record figures. Existing introductory/card tests migrated to the current credited bullet prose; two Papers-only tests use existing Papers fixture instead of full-site preparation. Initial selection6PASS/1author-link-selector failure; corrected exact nine-link oracle plus two changed prose tests3PASS4.68s. Types0/0/0; Ruff/format/staged diffcheckPASS. All133 overview helper function ASTs equal website HEAD. No browser/full gate/commit/push; final merge and CI belong to root. Keep open pending final exact-head CI.
