---
type: is
id: is-01m3p532d6ggqg2a2wg1hyze6t
title: Frontier atlas page from SquarePackingCase/v2 records, n = 1..324, clean value rendering and thumbnails
kind: task
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies:
  - type: blocks
    target: is-01m3p5343njrazhtrtw46yr27c
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-29T08:39:21.766Z
updated_at: 2026-09-30T19:53:04.747Z
closed_at: 2026-09-30T05:04:30.626Z
close_reason: "Implemented by lanes A, D1 and D2 and integrated in 8c24872ae, 14cb1c051 and f268e9be0 (re-pin in cb738842d): register registered field, grouped_results and significance helpers, overview data layer, frontier atlas page, tutorial page, explainer nav/canonical/edition notice, Visualizer link, document-map summaries and reader-document cards, notable-sources registry, whole-credit and ai_assistance."
resolution: null
duplicate_of: null
---

## Notes

Reviewed design: thumbnails are generated from the rendering SVGs with ids, titles and descriptions stripped, served as separate lazy <img> files (the SVGs total 52 MB and share ids with the explainer); records validated through softschema since load_cases does not; a lower bound's relation comes from the register entry citing its evidence.

Audit 2026-09-30: also done on claude/overview-page-impl in 82805af95 (render_frontier_page.py). The close reason cites commits on origin/claude/optimistic-gauss-uzmcl2 (branch B), which is not part of that PR.
