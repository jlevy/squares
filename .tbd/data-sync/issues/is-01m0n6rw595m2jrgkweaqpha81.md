---
type: is
id: is-01m0n6rw595m2jrgkweaqpha81
title: Keep the reports, corpus and generated tables consistent
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
created_at: 2026-08-22T17:02:24.937Z
updated_at: 2026-08-22T22:13:15.568Z
---
Standing maintenance. explorations/packing/test.sh is the guard and currently checks: exact verification of Trump's packing with negative controls; 100 frontier artifacts covering n = 1..100; soft-schema validation of both profiles; the six generated tables matching frontier/; and the strategy catalogues.

When a fact changes, edit the STRUCTURED source in frontier/ and re-run
tools/render_tables.py -- never edit a generated table in a report by hand, the drift
check will catch it. Re-run tools/validate_schemas.py after any schema change.
