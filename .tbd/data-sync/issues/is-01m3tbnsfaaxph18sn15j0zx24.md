---
type: is
id: is-01m3tbnsfaaxph18sn15j0zx24
title: "Site: more space above the homepage hero and above every page's title"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:51:24.392Z
updated_at: 2026-09-30T23:51:25.184Z
closed_at: 2026-09-30T23:51:25.183Z
close_reason: "Done in e500e7807 on claude/overview-page-impl (jlevy/squares#255): measured in the preview, the frontier title moves from 33px to 49px below the rule and the homepage hero to 41px."
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: a little more margin above the hero image on the main page, and more margin above the titles on each page. --site-page-top (site-nav.css) 2rem -> 3rem; the hero keeps --site-hero-lift 0.5rem, so it moves from 1.5rem to 2.5rem below the bar's rule; the explainer's hero reads the same token; print untouched.
