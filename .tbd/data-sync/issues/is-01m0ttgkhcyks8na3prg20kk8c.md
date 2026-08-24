---
type: is
id: is-01m0ttgkhcyks8na3prg20kk8c
title: Raise reusable Python modules to the tbd engineering quality floor
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
  - python
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T21:23:37.643Z
updated_at: 2026-08-24T21:23:37.643Z
---
Apply the loaded tbd Python and general engineering guidance to E2 and E3 code after its boundaries and tests are explicit. Keep Ruff and BasedPyright at zero warnings; use modern complete public types, absolute imports, Path, atomic durable writes, preserved exception context, explicit failure state, concise rationale-focused comments and docstrings, and no needless wrappers or duplicate implementations. Review every lint exception narrowly. Apply an appropriate lighter standard to E1 case code and do not generalize it without a second consumer. Acceptance: each changed module states its contract and maturity, relevant failures are tested, and all focused and full checks pass.
