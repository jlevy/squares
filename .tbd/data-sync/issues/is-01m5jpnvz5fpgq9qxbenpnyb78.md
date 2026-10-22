---
type: is
id: is-01m5jpnvz5fpgq9qxbenpnyb78
title: "validate.py: align --push docstring and help text with the draft-PR gate (#724 review A2)"
kind: task
status: open
priority: 3
version: 1
labels:
  - process
dependencies: []
created_at: 2026-10-22T21:01:09.477Z
updated_at: 2026-10-22T21:01:09.477Z
---
PR #724 review A2 (nit): packing/src/sqpack/cli/validate.py still calls --push 'the pre-push floor' (lines ~7572 and ~7906). After #724 the draft-PR rule is the edit or records tier plus the directly affected tests, with hosted CI as the full gate; --push is optional. Reword on the next edit to that file; it enforces nothing.
