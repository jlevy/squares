---
type: is
id: is-01m32qeknv12pway8h3kmdmfwq
title: "Main's merge cadence outran its validation wall: six merges, no completed run (D-466 live)"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m32fgxn7yh0skf12a0zxnres
created_at: 2026-09-21T19:35:25.627Z
updated_at: 2026-09-21T19:35:25.627Z
---
Observed 2026-09-21 19:35Z. This is D-466's documented pattern happening on main, not a hypothetical.

Packing validation runs on main, newest first:
  c2cc1cf6  in progress   (PR 216, 19:34)
  a7d68c00  CANCELLED     (PR 215, 19:20)
  87a3e0cb  CANCELLED     (PR 214, 19:01)
  beee2e0f  CANCELLED     (PR 213, 18:59)
  e0a27db9  CANCELLED     (PR 212, 18:56)
  6eb69761  in progress since 18:33  (PR 211) -- over an hour, never finished
  9fe9999d  success       (17:41)  <-- the last completed run on main

So main has had NO completed validation run since 9fe9999d at 17:41Z, across six merges. The workflow cancels a run when a newer push arrives, and eleven merges landed faster than the tier's own wall, so each cancelled its predecessor. OR-14 already states this exactly: 'a push cadence faster than the tier's own wall produces no completed run at all -- three runs on one branch were cancelled that way before the pattern was seen.'

Every one of those PRs was green on its own merge ref before landing, so this is not evidence of a defect in the merged code. It IS evidence that post-merge verification on main silently stopped reporting for two hours while looking, at a glance, like ordinary activity: a cancelled run is not a red one.

This is OR-17's fourth obligation seen from the other side. That rule says a gate must never re-decide a tree it has already decided; the converse hole is that a gate can be prevented from deciding ANY tree by a merge cadence it cannot keep up with, and nothing notices.

Two things to decide:
1. Whether main's validation should use a concurrency group that queues rather than cancels, so every merged tree is eventually decided, or whether per-merge verification on main is simply not worth its wall given every PR is gated pre-merge.
2. Whether anything should report 'main has no completed run newer than X'. Today nothing does, which is why this needed a person to notice.
