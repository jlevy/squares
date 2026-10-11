---
type: is
id: is-01m2aj2ewckram8ww4458w74hr
title: Calibrate the BC329 complete positive path before target registration
kind: task
status: closed
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
dependencies:
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
  - type: blocks
    target: is-01m26c1jahzgfckegz7fp9wcq7
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
child_order_hints:
  - is-01m2app5e71qnp9z5vfp9vppbp
  - is-01m2appdgg1p32xwgxptcqqb2x
  - is-01m2appm2nx1m700ky98ytzv4z
hold: null
hold_until: null
created_at: 2026-09-12T10:19:38.251Z
updated_at: 2026-10-06T08:40:12.052Z
closed_at: 2026-10-06T08:40:12.052Z
close_reason: "Superseded: calibrating BC329 before registration is moot. BC329's prospective endpoint 3.8267215 is below T-033's proved 3.8269975, so the packet could not move any bound even before T-060; its runner and calibration machinery is retained unexecuted on main via PR #156. s(11) is settled: T-060 (V3/C3) proves s(11) = T = 3.8770835..., packing/frontier/RESULTS.md on origin/main eb43ffe9a marks every earlier n11 lower bound 'superseded by T-060', and packing/campaign/ideas.md Orientation records n11 as settled with its older route premises historical. Its 'paused' hold (the owner's 2026-09-14 BC329/heavy-computation hold, think-zwlf) was cleared to close it: the hold's premise, a small n11 gain, no longer exists."
resolution: canceled
duplicate_of: null
---
After correctness repairs, run a target-free byte-bound positive fixture through raw sweep, normalized exact route, reflected interval route, dilation replay, publication, and independent per-direction readback. Retain wall/CPU clocks, direction counts, peak RSS, output bytes/files, worker count, source and implementation manifests, and deadline headroom on the intended host. Set the prospective scientific/external allowances from this measurement. The synthetic fixture must exercise the same serialization and route shapes without asking the BC329 scientific question; no target registration until an independent reader accepts the receipt.

## Notes

Astra xhigh target-free design review rejected the mocked unit fixtures as admission evidence. Selected design: a separate fixed-core-packet-calibration/v1 command and receipt that cannot emit or be read as scientific acceptance; one frozen analytically solved non-BC329 fixture; real generic raw/exact/interval/dilation kernels and strict row readers; 14,404 direction records at full shape; three fresh host runs; independently replayed receipt. Record requested and effective workers per route. RSS is a sampled process-group sum with shared-page/missed-peak limits, not exact physical peak. The easy fixture prices operational overhead only and cannot upper-bound BC329 compute time. Children think-zypf, think-vy5i and think-1mma own implementation, measurement and independent admission.

Paused: 2026-09-14 owner hold (think-zwlf): BC329's prospective gain is about 0.000274 over T-026 s(11) >= 3.8264474, and heavy computer-assisted work for very small improvements is paused while the program re-strategizes toward significant n=11 improvements or a much simpler proof. The runner, reader, verifier and run sheet land as retained, unexecuted machinery with PR #156 (think-j007). Resume only by an explicit owner decision.
