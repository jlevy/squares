---
type: is
id: is-01m5j10qmw6d55ghhfxg9ekww1
title: Migrate generated site URLs and validate legacy profile links
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-implementation
labels: []
dependencies:
  - type: blocks
    target: is-01m5j10r3f4dms3f0mgkphr7fe
parent_id: is-01m5j0rns0p8gq9rrn3wnns7p1
hold: null
hold_until: null
created_at: 2026-10-22T14:42:36.827Z
updated_at: 2026-10-22T16:01:28.843Z
started_at: 2026-10-22T15:44:53.762Z
---
Implement canonical squaremath.org site URLs, explicit legacy profile aliases, live changelog targets, and regressions per plan. Include the required site release-impact disposition for published SYNOPSIS.md/development.md documentation inputs; pre-push reports these pending at current v0.9.0. Preserve github.com/jlevy/squares repository links in PDFs. Plan and guide staged on codex/squaremath-domain.

## Notes

Implemented on codex/squaremath-domain, latest commit 82b48dc29. Sol implementation and compatibility review plus Astra senior review complete; only low plan-status issue fixed. Focused suites: 64 changelog/profile tests, 30 profile/date tests, 133 site metadata/URL/news/profile tests; PDF absolute-link Node test passes. Complete external preview builds and assembled local publication audit passes 7333/7333. Required pre-push gate still running; earlier failures (Ruff formatting, URL registry date drift, prior-main changelog hostname validation) fixed and committed. Owner verified domain; no repository cname or routing changes yet.
