---
type: is
id: is-01m2dz8pw9m2wpsz4xgds5vtkz
title: "T1 reader: bind executing implementation revision separately from source revision"
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - bc303
  - admission
dependencies: []
parent_id: is-01m2b8wag8sa0p3mna22wmr3c6
hold: null
hold_until: null
created_at: 2026-09-13T18:07:57.832Z
updated_at: 2026-09-13T19:42:05.045Z
closed_at: 2026-09-13T19:42:05.045Z
close_reason: Isolated T1 reader repair 74ec773c passed 11 focused tests; independent Astra Max exact-head review accepted both source-row authentication and executing-reader provenance. It independently checked 377 source atoms, 17 retained-record mutations, and 10 provenance controls. No T1 campaign determination/global routing/new bound promoted; separate stacked PR remains think-uula.
resolution: null
duplicate_of: null
---
Independent Astra Max review found replay(repository) reports supplied input HEAD as implementation_revision even when the executing T1 tool bytes are from 88d54d85 and absent at the input HEAD. Bind actual running module bytes/path to their implementation commit and distinguish that from source-data commit. Add wrong-copy/revision mutation controls.
