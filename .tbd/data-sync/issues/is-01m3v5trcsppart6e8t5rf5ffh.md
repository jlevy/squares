---
type: is
id: is-01m3v5trcsppart6e8t5rf5ffh
title: "n = 11 optimality paper page: two tables run past the article at phone width"
kind: bug
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:28:30.093Z
updated_at: 2026-10-01T11:20:54.931Z
closed_at: 2026-10-01T11:20:54.925Z
close_reason: "1b088f858 on jlevy/squares#261: the paper's tables keep to the column and scroll inside their own wrap; both fit the 358 px column at 390 (were 184 and 402 px over); preview_site --clips is clean on every page."
resolution: null
duplicate_of: null
---
Found 2026-10-01 by preview_site.clipped: n11-optimality/t-060-explainer.html has two tables running 135 px and 314 px past its article at 390 px, and 6 px at 768 with a scrollbar. The page came from jlevy/squares#259 with its own stylesheet (n11-optimality.css); jlevy/squares#261 (Codex) is editing the same paper. A full preview_site --shots or --clips run exits 1 on it until fixed.
