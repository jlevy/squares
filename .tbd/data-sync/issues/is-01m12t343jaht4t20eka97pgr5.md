---
type: is
id: is-01m12t343jaht4t20eka97pgr5
title: Validation gate runs 6+ min against a documented 2 min budget
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-08-27T23:50:11.313Z
updated_at: 2026-08-27T23:50:11.313Z
---
conventions.md states the tiers as: focused under ~60s, checkpoint ~2 min, deep handoff ~5 min. The actual full gate wall time is 380-440s and the 'fast behavioral tests' step alone was 366-413s, so the fast tier is 6x its budget and the full gate exceeds the deep-handoff tier.

Root cause found and partly fixed: expensive pure builders were called repeatedly per process with no memoization.
- devtools/build_known_best_atlas.expected_outputs() rebuilds all 100 cases (~27s for _build_case alone, ~40s with rendering). tests/test_known_best_atlas.py called it 3x.
- devtools/build_prospective_atlas.expected_outputs() rebuilds the 101-case seed. tests/test_prospective_atlas_seed.py called it 2x; those two tests were 111s and 106s.

Both now memoize, with clear_build_caches() and an opt-in fixture for the negative-control tests that repoint a source root (the memo must not be read or left behind across a root swap). Measured: known-best file 63s -> 45s, prospective file 228s -> 113s, suite 366s -> ~250s.

Remaining, not yet addressed:
- One genuine first build still costs ~40s (known-best) and ~103s (prospective) per process. Every validate step that shells out to a builder pays it again, since the memo is per-process. Consider a content-addressed on-disk cache keyed by the source digests, or having the steps that need the same build share one process.
- tests/test_contact_assembly_labels.py::test_every_rich_d4_and_relabeling_image_has_one_label is 28.8s on its own.
- Decide whether the fast tier should be a genuinely fast subset, or the documented budget in conventions.md should be restated to match reality. Right now the docs and the gate disagree, which is how the drift went unnoticed.
