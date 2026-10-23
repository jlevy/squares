---
type: is
id: is-01m5k1gznm6j706s8hjy1ka2zs
title: Use a Topics dropdown and consistent significance segments on News
kind: feature
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-components
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:10:43.763Z
updated_at: 2026-10-23T00:12:35.138Z
started_at: 2026-10-23T00:10:49.927Z
---
Implement only the News Topics/Tags filter as a colored dropdown multiselect, adapting the read-only Metabrowser chip-menu reference. Preserve news-topics/news-s URLs, history and hash restoration, S4/S5 default significance, and all-news access without scripts. Topics uses a compact All/one/+N summary, checked choices stay open, semantic topic colors, arrows/Home/End/Escape, outside dismissal and focus restoration. Significance remains inline segmented buttons, styled consistently with the homepage Grid/Triangle component. Do not add a significance dropdown or alter Results single-threshold semantics. Reuse shared tokens, original menu chevron endpoints and reversed motion, light/dark styling and mobile fit. Parent owns builds/commit; plan updates coordinated with landings. Plan: docs/project/specs/active/plan-2026-10-22-site-navigation.md.
