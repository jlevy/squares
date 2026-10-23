---
type: is
id: is-01m5k1gznm6j706s8hjy1ka2zs
title: Use a Topics dropdown and consistent significance segments on News
kind: feature
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-components
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:10:43.763Z
updated_at: 2026-10-23T00:42:18.530Z
started_at: 2026-10-23T00:10:49.927Z
---
Implement only the News Topics/Tags filter as a colored dropdown multiselect, adapting the read-only Metabrowser chip-menu reference. Preserve news-topics/news-s URLs, history and hash restoration, S4/S5 default significance, and all-news access without scripts. Topics uses a compact All/one/+N summary, checked choices stay open, semantic topic colors, arrows/Home/End/Escape, outside dismissal and focus restoration. News significance remains inline segmented buttons, styled consistently with homepage Grid/Triangle; no significance dropdown. The later Results Archive significance-segments request is tracked separately by think-p39d. Reuse shared tokens, original menu chevron endpoints and reversed motion, light/dark styling and mobile fit. Parent owns builds/commit; plan updates coordinated with landings. Plan: docs/project/specs/active/plan-2026-10-22-site-navigation.md.

## Notes

Generic overview/filter-menu.js owns disclosure, native button focus/navigation, outside/Escape/Tab dismissal, viewport fit and All/None/one/+N summary; news-filters.js retains authoritative selection/history/hash state. Topics use shared colored chips, preserved checks and muted per-significance tallies. Significance stays the existing inline S3-S5 shared component, default S4/S5. Precise render_overview script wiring and check_site_scripts classification added; BROWSER directory remains declared renderer input. Purpose-based sans and Topics-only policy documented in paper-design.md. Desktop actual News contract passed96.53s; compatibility/News semantics16passed19.24s. Scoped types/Biome/Ruff clean. Browser contract caught selected lower-bound check contrast4.22:1 under generic hover ink; topic text/checks now retain body ink. Mobile contract then observed a hidden+inert discrete panel remain rendered under KPress tiny reduced-motion duration; added the same explicit zero-duration panel/chevron rule as navigation and a semantic zero-duration assertion. Failed mobile case rerunning69934; leave bead in progress until confirmed. Parent owns final rebuild and CI.
