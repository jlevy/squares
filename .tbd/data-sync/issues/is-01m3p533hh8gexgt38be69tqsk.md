---
type: is
id: is-01m3p533hh8gexgt38be69tqsk
title: "Explainer and workbench: nav partial hidden in print, canonical URL, fragment forwarder, README/TUTORIAL links, #site-note"
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
created_at: 2026-09-29T08:39:22.929Z
updated_at: 2026-09-30T19:52:43.369Z
closed_at: 2026-09-30T05:04:30.632Z
close_reason: "Implemented by lanes A, D1 and D2 and integrated in 8c24872ae, 14cb1c051 and f268e9be0 (re-pin in cb738842d): register registered field, grouped_results and significance helpers, overview data layer, frontier atlas page, tutorial page, explainer nav/canonical/edition notice, Visualizer link, document-map summaries and reader-document cards, notable-sources registry, whole-credit and ai_assistance."
resolution: null
duplicate_of: null
---

## Notes

Reopened: Done only on claude/overview-page-impl, which was never pushed; the owner asked on 2026-09-30 that it be treated as lost. The decision is carried in the revised spec (plan-2026-09-29-github-pages-overview.md) and the work is to be redone.

Correction (2026-09-30 audit): the "treated as lost" reopen note above is wrong. claude/overview-page-impl was recovered, continued to a371c2f5f and is the branch of the overview PR. Done on it in dc25ee587 (nav on the explainer, explainer.html, forward.js, README and TUTORIAL links) and 9c3950749. The close reason cites commits on origin/claude/optimistic-gauss-uzmcl2 (branch B), which is not part of that PR.
