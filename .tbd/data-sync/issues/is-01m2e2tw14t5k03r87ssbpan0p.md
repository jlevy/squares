---
type: is
id: is-01m2e2tw14t5k03r87ssbpan0p
title: "R3: snapshot must admit all coordinator-required top-level logs"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2dzxxp9raxnvx21zk6mawes
created_at: 2026-09-13T19:10:18.646Z
updated_at: 2026-09-13T19:10:18.646Z
---
Independent exact-head review at verifier repair 0874e912 found snapshot now demands only summary plus three run records, while the maintained coordinator writes eighteen top-level stdout/stderr log files across its three runs. Reproduce with a target-free synthetic coordinator-shaped root, define the exact allowed top-level artifact set, reject extras, and preserve valid coordinator output. No positive profile or BC329 target.
