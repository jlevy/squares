---
type: is
id: is-01m5rtm3kqps82jfhxdeyxbkna
title: "New exact-side polynomial PR from current main, building on T-246; supersedes #403/#435 (#811)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: w-exact-sides-1025
labels:
  - project
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-25T06:05:32.663Z
updated_at: 2026-10-25T14:30:51.378Z
started_at: 2026-10-25T14:30:51.378Z
---
Owner decision 2026-10-25: #403/#435 are out of date (assessment in think-vt31). Start a fresh PR on current code and practice: main's polynomial notation (exact_sides.polynomial_text, root(p, low, high)), main's record coverage (derived facts in a register or view, not written onto records), one-record-per-line retained JSON; algebraic_source only if it still earns its place. Builds on Evan Daniel's s(29) registration (T-244, think-6gti). Lower priority: start only after the current result landings (T-243 n=12, T-244 s(29)) and the other outstanding intake items have merged. Run by its own sub-agent; the coordinator owns sequencing.
