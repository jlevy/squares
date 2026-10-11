---
type: is
id: is-01m3sy222x8d5h4f0j7mg2fft3
title: Workbench carries the site nav, gear and theme; case 11 as the nav mark and favicon on every page
kind: feature
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T19:53:26.360Z
updated_at: 2026-09-30T19:53:27.899Z
closed_at: 2026-09-30T19:53:27.897Z
close_reason: Done on claude/overview-page-impl in 3e8274909, 426f0f5aa and 995dd96c8.
resolution: null
duplicate_of: null
---
No bead was ever created for the workbench nav (the nav mark was sandbox think-7n2m). render_overview.nav_shell gives the workbench the shared nav partial, kpress tokens, site-nav.css, the pre-paint theme bootstrap and theme.js; build_site places them. The nav home link leads with the case 11 drawing, alone below 50rem; every page carries the favicon.
