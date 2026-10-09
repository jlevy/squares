---
type: is
id: is-01m4fdxy7dbpfged7eh7j24bt9
title: "Fix Pages layout shift: frontier.html 1280px dark CLS 0.209 and 390px font-settle CLS 0.25"
kind: task
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T04:14:51.629Z
updated_at: 2026-10-09T04:20:34.268Z
started_at: 2026-10-09T04:20:34.268Z
---
#448 Pages 37878589945 overview job: CLS 0.209 > 0.1. Original #449 4963448 Linux 390px light CLS 0.2512 while fonts settled. Find cause and fix in production; keep CLS 0.1.
