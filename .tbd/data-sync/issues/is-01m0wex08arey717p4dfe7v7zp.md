---
type: is
id: is-01m0wex08arey717p4dfe7v7zp
title: Avoid host-Python diagnosis of Python 3.14 syntax
kind: bug
status: closed
priority: 0
version: 3
spec_path: explorations/packing/campaign/hypotheses/H-037-asymptotic-waste-exponent.md
labels:
  - packing
  - robustness
  - ci
dependencies: []
parent_id: is-01m0rvm4r4s2kf1d81dcscwm2c
created_at: 2026-08-25T12:39:09.833Z
updated_at: 2026-08-25T12:50:49.340Z
closed_at: 2026-08-25T12:50:49.339Z
close_reason: Retracted the false cache diagnosis, restored the Python 3.14/Ruff-canonical source, and verified the complete locked gate. D-307 preserves the measurement error.
resolution: null
duplicate_of: null
---
D-307. The older host python rejected parenthesis-free multiple exceptions that are valid in the repository's locked Python 3.14 target under PEP 758. This led to a false cached-bytecode diagnosis and an ill-targeted source change; Ruff caught it. Keep the formatter-canonical source, retract the cache claim, and use the locked uv/Ruff environment for language-version judgments.
