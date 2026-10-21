---
type: is
id: is-01m5ebp20t3d4dbxzdx3t5d9sk
title: Align profile list bullets with KPress conventions
kind: bug
status: closed
priority: 2
version: 4
delegate: profiles-bullet-fix
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T04:32:03.608Z
updated_at: 2026-10-21T04:35:58.148Z
started_at: 2026-10-21T04:32:14.234Z
closed_at: 2026-10-21T04:35:58.147Z
close_reason: KPress-native list alignment restored, validated and reflected in local preview.
resolution: null
duplicate_of: null
---

## Notes

Fixed site-contributor.css: removed directory item padding so KPress controls marker/text alignment; reset first item start margin for multicolumn alignment; account icon row now suppresses pseudo bullets and resets list/item margins. Independent design review no blockers. Biome and static CSS checks pass. New content-addressed asset site-contributor.1e680e9ceb1e775d.css published through SiteAssets/write_assets and583 HTML references refreshed atomically; old asset retained. Served preview http://127.0.0.1:8790/profiles/index.html . Local uncommitted changes in external worktree; no push/deploy.
