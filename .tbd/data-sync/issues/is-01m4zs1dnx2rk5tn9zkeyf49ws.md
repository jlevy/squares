---
type: is
id: is-01m4zs1dnx2rk5tn9zkeyf49ws
title: "D2: bound deferred proof lookup time before cold execution"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zq0njqcj232mhnhc0nwfa3
hold: null
hold_until: null
created_at: 2026-10-15T12:36:51.004Z
updated_at: 2026-10-15T12:37:27.197Z
started_at: 2026-10-15T12:37:27.195Z
---
Seniorreviewofunpublishedcandidate:fourserialAPIreadswith60srequesttimeoutandnostepdeadlinecanadd240sbeforecoldfallback. Addsmalltotalnewlookupdeadline(e.g1min), keepoutcomeempty-outputnormalcommandfallback andexistingfastreusebehavior unchanged. Testtimeoutpresenceandfailurefallback; neverextendscientificcommanddeadline.
