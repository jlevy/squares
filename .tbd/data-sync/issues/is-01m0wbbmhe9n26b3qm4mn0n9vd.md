---
type: is
id: is-01m0wbbmhe9n26b3qm4mn0n9vd
title: Add retained record replay for H-042 incidence cores
kind: feature
status: open
priority: 2
version: 2
spec_path: packing/campaign/hypotheses/H-043-trump-incidence-rigidity-cores.md
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0sg2venckvcs3q1cr5v1qzc
created_at: 2026-08-25T11:37:15.053Z
updated_at: 2026-10-12T23:40:50.849Z
---
The pilot JSON contains exact stresses and deletion directions but the CLI only recomputes a result; it cannot load and independently replay a retained record. Before promoting the pilot to an experiment, add atomic record output, exact replay against rederived branch and provenance keys, tamper controls, and a maintained validation integration. D-290 tracks the durability gap.
