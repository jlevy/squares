---
type: is
id: is-01m12t343jaht4t20eka97pgr5
title: Validation gate runs 6+ min against a documented 2 min budget
kind: bug
status: open
priority: 1
version: 5
labels: []
dependencies: []
created_at: 2026-08-27T23:50:11.313Z
updated_at: 2026-09-07T22:52:45.133Z
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

## Notes

Related September7 repair on PR110: original03ff2102 passed correctness but failed the checks runtime band twice at150.31s/150.24s. VE004 admits the early-start scheduling hint after six complete48-check local observations: control median93.18s, candidate71.84s,22.9% reduction with nonoverlapping ranges on frozen1dfdb8fb/ed595fb6. Original VE003 missing-map setup failure remains retained. Hosted repairs d915dfa9 and ecd4a035 passed every required check in runs34158723317/34159929517. Full66 ed595fb6 passed1616.00s. No verifier arithmetic, thresholds or worker counts changed. The original publication obligation closed under think-oli1; broader validation costs remain open.

Upstream integration checkpoint September7: published1b953c95 passed every required check in34166050586; checks48 took133.94s within the unchanged band. The local full dbd60231, same implementation as1b apart from two Markdown files, hit900s quick/n40 timeouts,1800s slow timeout and three120s negative-control timeouts. Independent process inspection observed several heavy validation/test runs in other worktrees. This is evidence of overlapping load, not a quantified causal attribution or a performance comparison. Prior ed595fb6 used the same Python3.14.7,10CPU,jobs10/inner3 settings and caps; its quick329.16s/n40250.51s/slow715.60s/controls402.20s/full1616.00s are retained context.

Recoveries preserve the failed original status and all original caps/assertions. The three controls passed serially in38.296s,37.724s and26.409s. Isolated n40 on clean dbd60231 passed623.683s on September7 at22:45:40UTC, jobs2/inner1, inside900s. Hosted suite source equivalence is independently verified and covers3456 quick tests in121.72s; it does not cover the separate slow lane or prove native macOS runtime success. Slow replay and exhaustive completion remain pending under think-dwq8. Evidence is retained in attic/agenda-028-overnight/upstream-reconciliation-dbd60231 and PR110; no budget edit or claim of a new speedup follows from these recoveries.
