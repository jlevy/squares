---
type: is
id: is-01m0n6rw595m2jrgkweaqpha81
title: Keep the reports, corpus and generated tables consistent
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
created_at: 2026-08-22T17:02:24.937Z
updated_at: 2026-10-06T08:32:21.944Z
closed_at: 2026-10-06T08:32:21.944Z
close_reason: |
  Superseded (bead review 2026-10-06, origin/main eb43ffe9a): Standing maintenance whose guard (explorations/packing/test.sh, tools/render_tables.py) no longer exists; the same consistency is enforced by packing-validate's records tier on origin/main (devtools/render_research_tables.py drift check, devtools/validate_schemas.py)
resolution: canceled
duplicate_of: null
---
Standing maintenance. explorations/packing/test.sh is the guard and currently checks: exact verification of Trump's packing with negative controls; 100 frontier artifacts covering n = 1..100; soft-schema validation of both profiles; the six generated tables matching frontier/; and the strategy catalogues.

When a fact changes, edit the STRUCTURED source in frontier/ and re-run
tools/render_tables.py -- never edit a generated table in a report by hand, the drift
check will catch it. Re-run tools/validate_schemas.py after any schema change.
