---
type: is
id: is-01m2b883ztxn7qazs98bndea6b
title: Build the maintained BC329 three-profile calibration coordinator
kind: task
status: in_progress
priority: 1
version: 18
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh implementation; independent operational review
labels:
  - n11
  - calibration
  - tooling
dependencies:
  - type: blocks
    target: is-01m2b884n0ms50xp93q6aaps1g
  - type: blocks
    target: is-01m2appdgg1p32xwgxptcqqb2x
  - type: blocks
    target: is-01m2cv85q2ajjgsnx7076ta8cp
parent_id: is-01m2appdgg1p32xwgxptcqqb2x
child_order_hints:
  - is-01m2dzapemsrp1hn26art77r69
  - is-01m2dzaptz5wh3hmv24dsqx72f
  - is-01m2dzaq79t4tthvy0z800752y
  - is-01m2e3ehdf6s735hrnswcxd2xg
hold: null
hold_until: null
created_at: 2026-09-12T16:47:12.378Z
updated_at: 2026-09-13T19:27:40.751Z
---
Run-sheet review F-2/F-3. Replace the one-off shell/Python timing, immediate-readback, and summary heredocs with a maintained devtools coordinator and tested receipt contract before any profile. Measure monotonic command wall time from immediately before subprocess launch until the top-level calibration command returns; retain exact commands, stdout, stderr, exit statuses, invocation identities and receipt digests; call strict producer/inventory readers; reconstruct counts, bytes and digests; atomically write and reread a duplicate-key-safe three-profile median/min-max summary. Preserve the narrower producer clocks and their scopes. Do not run a profile or BC329 until the tool and review pass.

## Notes

Earlier independent review at fc3e314d refused inverted raw/exact task chronology, disjoint phase time, and unsafe second result.json read; prior auto-review had then blocked source edits. The user subsequently authorized tracking and doing these tasks. Isolated 4b8d333a repaired all three, integrated as dbbf8495; 132 focused tests passed with one unrelated process-group EPERM. Independent exact-head review accepted their targeted controls but REFUSED strict receipt admission on derived infinite deadlines (think-0osz) and uncaught finite phase-sum OverflowError (think-dgfk). Sol max isolated repair underway, followed by independent rereview. Durable report docs/project/reviews/review-2026-09-13-n11-bc329-coordinator-final.md. No positive profile/BC329 target.
