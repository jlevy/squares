---
type: is
id: is-01m1mvbneqmacrwgm9s9hbczg5
title: "BC-180: measure and cut the gate's slowest step"
kind: task
status: open
priority: 2
version: 3
spec_path: packing/campaign/agendas/agenda-018-ten-hour-continuation-ladders-theorems-and-wave-two.md
labels:
  - packing
  - agenda-018
dependencies:
  - type: blocks
    target: is-01m1mvbpfv99crnn7gfte5epnd
parent_id: is-01m1mv6zm9cmtzc23nbzvfp4hs
created_at: 2026-09-03T23:58:39.574Z
updated_at: 2026-09-04T00:00:49.344Z
---
Lane D W5, 90 minutes, only after BC-178. Baseline fast behavioral tests (about 1210 s at 1607 tests) with the existing profile, find the two most expensive test modules, and cut wall time under an equivalence guard (identical test selection and outcomes) without touching a correctness check; record the measured delta or the rejection.
