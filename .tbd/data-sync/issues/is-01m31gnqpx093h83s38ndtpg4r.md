---
type: is
id: is-01m31gnqpx093h83s38ndtpg4r
title: "X-040: mark refuted claims in the lane-2 and lane-3 tables"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:17:44.667Z
updated_at: 2026-09-21T08:17:44.667Z
---
PR 204 review finding F1 (High). Only the lane-1 table at X-040:132 carries a Lane verdict column. X-040:157 labels the stressed-optimum reduction 'Derived here' - defined at :72-73 as checked by its reviewer - while :251 records R2's finding that the stress theorem is false as stated. Same pattern at :158 (D3 shrunk ceilings hold only for m=4; :259 refutes m=5,6) and :182-183/:188 (n=45 listed as one-spare; :276 records R3's correction and BC-366 retires it). Those tables exist so a later lane can pick a mechanism off them. Fix: give lanes 2 and 3 the verdict column lane 1 already has.
