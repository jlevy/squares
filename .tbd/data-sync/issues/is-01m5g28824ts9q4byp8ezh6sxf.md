---
type: is
id: is-01m5g28824ts9q4byp8ezh6sxf
title: Diagnose hosted T-037 mobile layout shift
kind: bug
status: in_progress
priority: 1
version: 2
delegate: about_profiles_implementation
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T20:25:42.722Z
updated_at: 2026-10-21T20:25:51.879Z
started_at: 2026-10-21T20:25:51.879Z
---
Pages run 39669145614, overview job 119462390704 at head 7b566ae73, reports result/t-037.html at 390px in light and dark with CLS 0.103 above the unchanged 0.1 limit. Timing exceedances are empty. Inspect retained layout-shift sources, reproduce through existing repository rendering checks, and repair actual geometry if needed without relaxing thresholds. New head c3e8f1cc has only URL-date changes; CI is being monitored independently. No source commit or push before reporting evidence.
