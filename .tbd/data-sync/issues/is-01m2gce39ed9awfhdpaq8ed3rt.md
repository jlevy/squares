---
type: is
id: is-01m2gce39ed9awfhdpaq8ed3rt
title: "Stabilize and merge PR #167, audit recent merged stack, and plan next research"
kind: task
status: open
priority: 1
version: 5
labels: []
dependencies: []
child_order_hints:
  - is-01m2gbmjzt8366xpvsp05kmbp8
  - is-01m2gbmk4ayta3zjej4j2xgkz5
  - is-01m2gbq83nnn7vp64h679pyqzw
created_at: 2026-09-14T16:36:34.730Z
updated_at: 2026-09-14T19:23:26.461Z
---
Address the three PR #167 review findings, validate and merge the PR, audit the recent merged n=11/BC303 PR stack for unresolved state, and if stable produce the next research plan from the canonical handoff using the experiment-loop contract.

## Notes

PR167 merged to main as 80bcdbb0 after fixes ed68f644 and green fresh hosted required CI. Recent-stack audit: #156/#161-166 merged via 2f8865b6, #157 via 620e4731, #168 fixes included in the stack; code/hosted validation stable. Governance is not ready for a new target: think-uqa4, think-j007, think-088v, usage closeout, CI headroom, and H160/H162 pause-vs-run remain unresolved. Conditional next direction under think-gtax: Route A think-9y6q first, Route B think-ol1z second, Route C think-29ch third, Route D think-7n2w background only; preregister the bounded discriminator before execution.
