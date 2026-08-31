---
type: is
id: is-01m188m2r2n9ydb4een5atsv6r
title: Swap the remaining jsonschema call sites to jsonschema-rs
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-08-30T02:40:19.201Z
updated_at: 2026-08-30T02:40:19.201Z
---
BC-077 swapped devtools/validate_schemas.py, which was the step on the pre-push critical path. Nine other modules still construct jsonschema.Draft202012Validator: src/sqpack/campaign/ledger.py, src/sqpack/witness.py, devtools/check_atlas.py, devtools/screen_translation_escape.py, devtools/price_contact_enumeration.py, devtools/generate_contact_full_cell_control.py, devtools/profile_known_best_chunks.py, devtools/generate_contact_structures.py, devtools/render_known_best_contact_overlays.py, devtools/build_contact_scaffold_atlas.py.

Deliberately out of BC-077's scope: none of them is on the pre-push tier, and widening the swap would have widened what the differential test had to cover in the same change. tests/test_schema_validator_equivalence.py already proves the two libraries agree over the whole corpus, so the remaining swaps are mechanical -- rename e.path to e.instance_path at each call site.

Measure before doing it. The point is speed, and a call site that validates one small document does not need it.
