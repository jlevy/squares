---
type: is
id: is-01m0wmn0zw88qedq2hjv6asdxs
title: Relax interrupt-test wall ceiling above measured suite jitter
kind: bug
status: open
priority: 2
version: 1
spec_path: explorations/packing/tests/test_validation_cli.py
delegate: codex-root
labels:
  - packing
  - validity
  - testing
dependencies: []
parent_id: is-01m0vpakbh6fy8p18cxsmtydgd
created_at: 2026-08-25T14:19:39.899Z
updated_at: 2026-08-25T14:19:39.899Z
---
The first SIGINT regression required wall <3s. It passed alone in about 2.5s but took 3.008s in the full focused file despite satisfying process-death and leak checks and staying far below its 10s command deadline. Use a 5s ceiling that still distinguishes coordinated cleanup from waiting for the command deadline; retain all semantic survivor assertions.
