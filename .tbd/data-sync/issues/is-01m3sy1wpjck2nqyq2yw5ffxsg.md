---
type: is
id: is-01m3sy1wpjck2nqyq2yw5ffxsg
title: "Site: every repository link on main, never at a commit hash, with a published-site check"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T19:53:20.840Z
updated_at: 2026-09-30T19:53:22.485Z
closed_at: 2026-09-30T19:53:22.482Z
close_reason: Done on claude/overview-page-impl in 8ffa5fba1.
resolution: null
duplicate_of: null
---
Sandbox id think-eyrk (never synced). devtools/repo_links.py names blob/main, tree/main or raw on main for every repository link; check_published_site fails a page linking a commit hash and checks linked paths against the deployed tree; a render-time test does the same. Generalizes think-eefp.
