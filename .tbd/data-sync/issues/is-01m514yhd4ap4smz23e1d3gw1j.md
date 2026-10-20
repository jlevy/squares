---
type: is
id: is-01m514yhd4ap4smz23e1d3gw1j
title: "PR #636 A4: witness identity is weaker than stated; bind SETTLED to source.path and source.revision too"
kind: bug
status: closed
priority: 3
version: 3
delegate: ecstatic-edison-636-review-a
labels:
  - regularization
dependencies: []
parent_id: is-01m514y11gd146dzhmnf7ke508
hold: null
hold_until: null
created_at: 2026-10-16T01:24:13.860Z
updated_at: 2026-10-16T02:07:04.701Z
started_at: 2026-10-16T01:24:33.061Z
closed_at: 2026-10-16T02:07:04.701Z
close_reason: "Fixed (PR #636 A4) in 288a1a520: witness_identity, Settled and the record carry source path and revision; SETTLED binds key, path, revision, side; id check documented as row-to-count only. Test: test_the_state_follows_the_witness_as_it_identifies_itself (4 cases), test_a_row_out_of_place_fails_the_gate."
resolution: null
duplicate_of: null
---
Low. default_drawings.py:447-459,:481-485,:759-760. witness.id is per-n so the id comparison cannot fire on re-housing; SETTLED binds only (source.key, side). Fix: add source.path and source.revision (where present) to witness_identity and Settled; say what the id comparison checks. Review: https://github.com/jlevy/squares/pull/636#pullrequestreview-5541598868
