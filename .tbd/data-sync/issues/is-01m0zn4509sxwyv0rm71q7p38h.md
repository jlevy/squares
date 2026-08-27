---
type: is
id: is-01m0zn4509sxwyv0rm71q7p38h
title: Align PR 45 source and generated hashes with repository hash policy
kind: bug
status: closed
priority: 2
version: 3
labels:
  - packing
  - pr-45-review
dependencies: []
created_at: 2026-08-26T18:25:38.824Z
updated_at: 2026-08-27T01:32:22.341Z
closed_at: 2026-08-27T01:32:22.340Z
close_reason: Co-committed integrity hashes were removed under repository policy while upstream UnitSquare trust evidence remains; deterministic replay, strict, and final-head CI are green.
resolution: null
duplicate_of: null
---
development.md says Git is the integrity boundary for co-committed sources/goldens and forbids adjacent SHA-256 fields/checksum controls absent an independently supplied trust boundary or a separately named content-identity purpose. PR #45 adds self-hashes for committed Kingbird sources, manifests, renderings, witnesses, profiles, and source maps, and describes the corpus as hash-checked. Retain upstream-declared UnitSquare hashes where they cross a real trust boundary; remove the co-committed integrity checks or explicitly redesign/name legitimate dedup/cache identities in accordance with policy.

## Notes

Implemented in the reviewed PR 45 draft candidate: removed co-committed local integrity hashes, retained only upstream-declared UnitSquare SVG hashes and explicitly named witness parent-content identities, with Git plus deterministic replay as the co-committed integrity boundary. Schema/generator/profile checks pass. Leave open until fresh strict and CI receipts complete integration.
