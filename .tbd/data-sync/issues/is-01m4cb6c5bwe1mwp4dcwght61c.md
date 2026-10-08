---
type: is
id: is-01m4cb6c5bwe1mwp4dcwght61c
title: "PR #427 A8 — Medium: source-sensitive behavioral contracts were not brought forward with the import."
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
hold: null
hold_until: null
created_at: 2026-10-07T23:29:19.019Z
updated_at: 2026-10-08T00:20:40.447Z
started_at: 2026-10-08T00:20:36.049Z
closed_at: 2026-10-08T00:20:40.447Z
close_reason: Source fixes9ff422a/6c615115 at f1d7 are independently reviewed E/F/G/H with0newfindings and hosted final-head CI30SUCCESS26documentedSKIP. Focused379+190+3+11owner checks passed; selected broad assertions completed with original capability failure retained and unchanged supported profiler/heavy completions. Actual broad allowance1800 is unchanged. These source findings are fixed; parent422 intake/confirmation/deployment remain open until atomic stack merge and publication.
resolution: null
duplicate_of: null
---
Review https://github.com/jlevy/squares/pull/427#pullrequestreview-5449633758 head83748.

**A8 — Medium: source-sensitive behavioral contracts were not brought forward with the
import.** Actual suites A, B, C and D also fail retained motion/source rosters and
population assertions in `packing/tests/test_validation_cli.py:2721`,
`test_translation_escape_screen.py`, `test_chunk_taxonomy.py` and
`test_known_best_atlas.py:182`. `test_verified_upper_bound_contract.py:679` identifies
the new adapter and its tests as undeclared ceiling consumers, while `:591` requires the
per-case ceiling paragraph to name `s(88)` rather than generic `s(n)`. Its
trailing-bound roster likewise predates this import.
The current prose expresses the right inequality; these failures expose an incomplete
migration of the repository’s behavioral contracts.

**Fix:** after refreshing the owning data producers, derive and review the new corpus
expectations, update the exact changed rosters/counts, declare both new consumers with
their ceiling-only meaning, and render the required per-case wording.
Preserve the complete prior-scope tests and meaningful semantic assertions.
Run all four actual behavioral shards; do not skip the failing cases or relax thresholds
to make the import pass.

## Design assessment

A separate immutable second-update layer is appropriate: it avoids extending the
original release or first-update scope, and routes all selected geometry through the
existing exact witness producer.
The explicit report end marker gives redrafting a stable boundary; preservation tests
protect earlier proofs and hand-authored n=88 lower-bound prose.
Full-data comparison independently confirms all 324 verified upper, verified lower and
reported lower lanes, 315 unselected witnesses and manifest entries, and 65 earlier
packet/proof files are preserved.

`update_selected` rebuilds canonical composite metadata before later scope checks and
writes outputs atomically per file rather than transactionally across the complete set.
That limitation does not explain these failures and does not invalidate the promised
preservation of unselected geometry.
The relevant repair is a complete dependent-output refresh, not an unrelated transaction
redesign.

## Documentation

The packet, frontier, result register and source coverage correctly describe T-116 as
V0/C0/S3. Exact visualization checks do not promote this result or imply optimality or
rigidity. Preserve that distinction through repairs.
Update the PR’s validation account once the failed sweeps and pending full gate are
resolved.
