---
type: is
id: is-01m0wbd5gxv2nf80fmz816wptv
title: Replace tautological H-042 provenance controls with exact mappings
kind: bug
status: open
priority: 2
version: 1
spec_path: explorations/packing/campaign/hypotheses/H-042-trump-incidence-rigidity-cores.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0sg2venckvcs3q1cr5v1qzc
created_at: 2026-08-25T11:38:05.212Z
updated_at: 2026-08-25T11:38:05.212Z
---
Order-10 audit found source_row_labels_are_complete only compares a list to itself, while contact_feature_aliases_are_complete proves nonemptiness and a product count rather than exact alias identities, uniqueness, and raw-selection mapping. Rename count-only facts and add mutation-capable exact provenance assertions before promotion. D-293 owns the testing gap.
