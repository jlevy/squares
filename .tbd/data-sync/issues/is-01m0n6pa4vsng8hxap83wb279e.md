---
type: is
id: is-01m0n6pa4vsng8hxap83wb279e
title: Deepen the search and proof strategy catalogues
kind: epic
status: open
priority: 1
version: 24
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
child_order_hints:
  - is-01m0n6qt1c53c6wewq1gzsk61y
  - is-01m0n6qtbmb20b20rnmn4p0edw
  - is-01m0n6qtnwjm4s6ttbgr2exna9
  - is-01m0n6qv0an0wsfb2zx1qrnpes
  - is-01m0n6qvaj25fk1k4yfsbtxdgd
  - is-01m0n6qvmx0esjvsdv9k0y1023
  - is-01m0n6qvz95q40avq6wd328gtg
  - is-01m0n6qw9bg0rbmjk383mvfp5s
  - is-01m0n6qwqdwjvjex4thdhagfth
  - is-01m0n6qx2adncat8n1ttvtqfwt
  - is-01m0n6qxhezdwydjz0nz0yz0gz
  - is-01m0n6qy0fqqbx2s376e8tcsxy
  - is-01m0n6qyb5gxaan208sdavdqmp
  - is-01m0n6qyp87yn5a2mavs80107h
  - is-01m0n6qz11q26jgt0avv48jqe1
  - is-01m0n6qzbaatyq6pvgnfwxeewe
  - is-01m0n6qzp9wjabek8gakx67738
  - is-01m0n6r011nwv7x7mzt663n4qc
  - is-01m0n6r0bpvc0mcw2x9v048r5p
  - is-01m0n6r0pk99590k8b78zpja00
  - is-01m0n6r10yhz5naty77e606dyq
created_at: 2026-08-22T17:01:00.954Z
updated_at: 2026-08-22T22:13:45.613Z
---
The two catalogues are now structured and enforced:
- explorations/packing/frontier/search-strategies.yaml (20 entries, 4 families)
- explorations/packing/frontier/proof-strategies.yaml (30 entries, 6 families)
Both render into the report as generated tables via tools/render_tables.py.

What they already show: 10 of the 16 working proof strategies are one idea refined
(unavoidable point sets), while four genuinely different search families have each
produced records. The other ten-entry proof family -- the transversal and wider
packing-and-covering toolkit -- is almost entirely unapplied to s(n).

The child beads deepen individual families that are currently one row each. Adding to a
catalogue means editing the YAML and re-rendering, not editing the table.
