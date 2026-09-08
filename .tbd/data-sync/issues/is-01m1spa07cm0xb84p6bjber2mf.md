---
type: is
id: is-01m1spa07cm0xb84p6bjber2mf
title: Test inset-margin seeding then release support
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@spud10.local
labels:
  - research
dependencies:
  - type: blocks
    target: is-01m1sp9x74c7706vvea0w6ga08
parent_id: is-01m1sp7k7txpwp2y4pbhen30jv
hold: null
hold_until: null
created_at: 2026-09-05T21:06:34.347Z
updated_at: 2026-09-06T05:37:18.226Z
started_at: 2026-09-06T03:21:56.565Z
closed_at: 2026-09-06T05:37:18.225Z
close_reason: "Exp-071/H-070 reached its preregistered terminal determination: the released inset seed and matched unseeded control produced byte-identical exact candidates, so the seeding hypothesis is rejected and no continuation opens."
resolution: null
duplicate_of: null
---
BC-233: run a 30-minute Massaccesi-style seed screen at the three declared rational margins. Convert Massaccesi's doubled margin M to the driver's one-sided --inset=M/2, then release all support restrictions and compare against an equal-budget unseeded control; retain a seed only if the released run wins.

## Notes

Official T+2 result: H-070/exp-071 rejected. All three exact inset screens were eligible; inset 1/2 was the unique screen minimum. The released seeded and unseeded control arms both exited 0, converged after eight rounds, and emitted byte-identical candidates of exact mass 11142893/1000000 (>11), so the preregistered strict-improvement criterion was missed and no exact lower-bound route opened. Terminal experiment record SHA-256 0cab80c891483ebc7150d5d4fc3c0a7de5958e74d04d8aec5f6a77453de201d9; complete twenty-output hash manifest is in results/agenda-025/bc-233-disposition.md. No successor launched; close at the coordinated landing checkpoint.
