---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: in_progress
priority: 2
version: 13
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-upstream-1015
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-15T18:02:51.502Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

2026-10-15 continuation: git fetch --all completed; origin/main31eaf6333c5d5b6b3d111241768cdd3d30982588 has289 commits beyond HEAD8270752fe, merge-base37e6757ed. PR578 remains open, local gh-stack absent and remote formal-stack API empty. Worktree clean; merge NOT started because required external /Volumes/spud-ext1 scratch fell from95MiB to32MiB free. User asked to free severalGB or supply another mounted external volume; do not use internal scratch. Read-only review:87 overlapping paths; preserve published upstream site release history throughv0.7.7 and choose fresh profiles edition instead of branch proposedv0.7.0. Preserve branch render_changelog profile target mapping with upstream News rewrite/filters/anchors/parser/headings. Preserve upstream explanations navigation remap plus profile empty-current support. Normalize new curated wand125 person labels to Hosono in fine-net n37/n39/n44 and linear n145 sources and Greff credit, preserving identifiers/URLs/archive. Reconcile census, generated result/citation/URL views and independent paper release dispositions after merge. Previous integration at8270752fe had hosted31passed27skipped; this new merge has no validation yet.
