---
type: is
id: is-01m3v5tssc8wzh51qyeqdsy056
title: "n = 11 optimality paper: citations link the build commit while every other site page links main"
kind: task
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T07:28:31.523Z
updated_at: 2026-10-01T11:20:55.784Z
closed_at: 2026-10-01T11:20:55.783Z
close_reason: "19f49c2f9 on jlevy/squares#261: the paper keeps its commit-pinned citations as the recorded exception (a dated review whose citations anchor into changing files); check_published_site requires each to name the deployed commit and exist in its tree; repo_links.py and paper-design.md record it."
resolution: null
duplicate_of: null
---
The paper renderer (render_n11_optimality_explainer) pins its repository links to the build commit by design; the site rule (think-eyrk, repo_links) is links on main. Decide and align, or record the exception in paper-design.md and check_published_site.
