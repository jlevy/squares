---
type: is
id: is-01m3tbnwrhjvangr6m4searpkb
title: Standalone math headlines on cards and popovers are set in the serif
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:51:27.760Z
updated_at: 2026-10-01T04:50:45.849Z
closed_at: 2026-10-01T04:50:45.848Z
close_reason: Done in f7cb5c0b0 on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. headline_math_face marks a headline serif only when it is all math; atlas and case popover titles are serif, worded headlines are sans.
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: a headline that is math standing alone, for example n = 11 as a heading, is set in the serif on cards and in popovers. Popover values and case titles already carry data-math-face=serif (e984d68ac; host_math_init.js honours it); extend it to card headlines and any other heading whose whole content is math, with a test.
