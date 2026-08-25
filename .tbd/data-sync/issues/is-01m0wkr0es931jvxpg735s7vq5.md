---
type: is
id: is-01m0wkr0es931jvxpg735s7vq5
title: Cancel detached validation process groups on interrupt
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/src/sqpack/cli/validate.py
delegate: validation_timeout_policy
labels:
  - packing
  - robustness
  - interruption
dependencies: []
parent_id: is-01m0vpakbh6fy8p18cxsmtydgd
created_at: 2026-08-25T14:03:49.081Z
updated_at: 2026-08-25T14:03:49.081Z
---
The first production-default timeout draft reintroduced D-295: every worker command entered a detached process group, so SIGINT reached only the main validator while ThreadPoolExecutor could wait up to the 600-second timeout. Add coordinated active-group termination/cancellation before executor shutdown, retain a bounded production-step SIGINT regression, record the recurrence, and do not land the default without it.
