---
type: is
id: is-01m4d6q7agj2kx3sg7gnx2f8dp
title: Remove repeated full-corpus setup from site contract tests
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
created_at: 2026-10-08T07:30:22.667Z
updated_at: 2026-10-08T07:30:22.667Z
---
C12: Hosted complete104 run37739282088 and ordinaryPR0f suiteD reproduce redundant real forwarder rebuilding during59 negative variants, with45.85/47.07s call time; complete-site metadata and amended-result tests also trigger whole-corpus setup in calls. Use immutable actual module fixtures, fresh per-variant dictionaries/lists, retained actualchecker/admissions and allnegatives. Preserve12s complete-gate limit,45s PRhardbackstop, all104steps and full-stepbudgets. No mutable production cache or scientific custody cache.
