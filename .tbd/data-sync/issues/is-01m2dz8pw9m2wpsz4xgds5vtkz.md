---
type: is
id: is-01m2dz8pw9m2wpsz4xgds5vtkz
title: "T1 reader: bind executing implementation revision separately from source revision"
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - bc303
  - admission
dependencies: []
parent_id: is-01m2b8wag8sa0p3mna22wmr3c6
hold: blocked
hold_until: null
created_at: 2026-09-13T18:07:57.832Z
updated_at: 2026-09-13T18:13:47.335Z
---
Independent Astra Max review found replay(repository) reports supplied input HEAD as implementation_revision even when the executing T1 tool bytes are from 88d54d85 and absent at the input HEAD. Bind actual running module bytes/path to their implementation commit and distinguish that from source-data commit. Add wrong-copy/revision mutation controls.
