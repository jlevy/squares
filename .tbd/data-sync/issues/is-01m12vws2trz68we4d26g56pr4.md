---
type: is
id: is-01m12vws2trz68we4d26g56pr4
title: n=11 rigid flag regressed from true to null
kind: bug
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T00:21:40.569Z
updated_at: 2026-08-28T01:26:20.485Z
---
frontier/n-011.md records reported_upper_bound.rigid: null. Three retained sources say the packing is rigid: resources/web/kingbird-squares-in-squares.md:80, resources/papers/friedman-ds7-packing-unit-squares-in-squares.md:71 ('This packing is also rigid'), and resources/papers/kingbird-square-11-provenance.svg:21. The repo's own research doc records both at docs/project/research/research-2026-08-22-packing-11-unit-squares.md:184.

The v1 record had rigid: true; commit c80d7e6 flipped it to null and was the only record changed. Restore it, and add an audit so the flag is checked against the catalogue rather than only migrated forward (devtools/migrate_frontier_v2.py:352 is the sole code that touches the field).
