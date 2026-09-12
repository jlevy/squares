---
type: is
id: is-01m2b883ztxn7qazs98bndea6b
title: Build the maintained BC329 three-profile calibration coordinator
kind: task
status: open
priority: 1
version: 3
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
parent_id: is-01m2appdgg1p32xwgxptcqqb2x
created_at: 2026-09-12T16:47:12.378Z
updated_at: 2026-09-12T16:47:29.650Z
---
Run-sheet review F-2/F-3. Replace the one-off shell/Python timing, immediate-readback, and summary heredocs with a maintained devtools coordinator and tested receipt contract before any profile. Measure monotonic command wall time from immediately before subprocess launch until the top-level calibration command returns; retain exact commands, stdout, stderr, exit statuses, invocation identities and receipt digests; call strict producer/inventory readers; reconstruct counts, bytes and digests; atomically write and reread a duplicate-key-safe three-profile median/min-max summary. Preserve the narrower producer clocks and their scopes. Do not run a profile or BC329 until the tool and review pass.
