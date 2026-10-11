---
type: is
id: is-01m3sy1jyfdzhgbvrg0wjnyr8z
title: "Site: theme gear (System, Light, Dark) at the end of every page's nav"
kind: feature
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T19:53:10.862Z
updated_at: 2026-09-30T19:53:11.579Z
closed_at: 2026-09-30T19:53:11.578Z
close_reason: Done on claude/overview-page-impl in 282f05531, with 769393f68 (far right on wide screens) and 6b60a10fb (level with tab text).
resolution: null
duplicate_of: null
---
Sandbox id think-77xi (created in a cloud session, never synced; also think-kwlj). A gray gear ends the shared nav on every page, explainer included, opening a native-popover menu of System, Light and Dark. It uses kpress's kpress.theme preference and data-kpress-theme attributes, follows the OS in System and follows choices made in other pages; the explainer certificate canvas repaints on squares:themechange. overview/theme.js, site-nav.css, paper-design.md Theme control entry, tests.
