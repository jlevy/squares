---
type: is
id: is-01m76qshvdpy2hnjdk3y4karqw
title: "Flaky CI: tests/test_site_atlas_views.py::test_viewport_size_prepaints_without_motion_and_keeps_explicit_choices crashes its xdist worker (60 s faulthandler timeout) on starved runners; failed frontend on #965 (job 130893681261) and #964 head 67f40d9f0"
kind: bug
status: closed
priority: 1
version: 3
delegate: bold-ritchie-l123
labels:
  - validation
dependencies: []
hold: null
hold_until: null
created_at: 2026-11-12T02:01:09.228Z
updated_at: 2026-11-12T04:33:01.345Z
started_at: 2026-11-12T02:01:32.378Z
closed_at: 2026-11-12T04:33:01.345Z
close_reason: "Fixed by #968 (merged bc152e8b4): the faulthandler_timeout C watchdog replaced by devtools.stack_watchdog (a GIL-holding Python-thread dump) plus a ban scan; D-523."
resolution: null
duplicate_of: null
---
