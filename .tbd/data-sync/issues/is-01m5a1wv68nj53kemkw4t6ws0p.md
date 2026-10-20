---
type: is
id: is-01m5a1wv68nj53kemkw4t6ws0p
title: Correct Mac fine-net assurance prose and unavailable CPU reporting
kind: bug
status: open
priority: 1
version: 4
labels: []
dependencies: []
parent_id: is-01m5a0yx8cne1ka5wgnxtrq8e0
child_order_hints:
  - is-01m5a5aa6ystmc0mhcj61y941t
  - is-01m5a620ay3w1g886ktdczmkhp
  - is-01m5a76wv61fxeqx07z0m0wz5m
created_at: 2026-10-19T12:24:02.503Z
updated_at: 2026-10-19T13:56:54.757Z
---
Follow-up from independent Astra max correctness review think-m1ff, .codex/intake-resume-20261019/fine-net-mac-math-review.md. A1 High: packing/devtools/sqverify_fast_census.py evidence_entry hardcodes 4-core x86-64 Linux/container and the rectangle renderer also asserts Linux; derive platform/compiler/profile from preserved build/run evidence and omit unknown host facts before publishing Mac assurance. A2 Medium: packing/sqverify_fast/src/main.rs direction_cpu_seconds sums missing per-direction data to 0/-0.0 on Mac (lib.rs reads only Linux /proc); represent unavailability explicitly and preserve existing Linux receipts. Raw captures/controls may proceed on the qualified preserved binary with native output unchanged, separate unavailable annotation, capture wait4 aggregate CPU and /usr/bin/time -l aggregate timing for every full command. Neither finding is a mathematical blocker to that bounded raw route, but both block misleading assurance or cost claims. No source edit or new binary is authorized by this tracking record; a future fix must receive focused review/tests before publication.
