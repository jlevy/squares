---
type: is
id: is-01m5nzh8rq727n2q01ceqfwq2e
title: "Slow registry: charge or refuse an aliased pytest mark in _slow_marked (#745 review B4)"
kind: task
status: open
priority: 3
version: 2
labels:
  - validation
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T03:33:39.223Z
updated_at: 2026-10-24T03:48:35.124Z
---
PR #745 review B4 (suggestion, Low; https://github.com/jlevy/squares/pull/745#issuecomment-6379074892), deferred by c-final-745-1024.

`_slow_marked` in `packing/tests/test_module_boundaries.py` (the slow registry's scanner, about lines 1658-1715) recognizes `mark.slow` only through an attribute chain ending in `mark`. The reviewer's probes showed that `from pytest import mark as mk` with `@mk.slow`, and `getattr(pytest.mark, "slow")`, are neither charged to a test nor refused; by inspection `m = pytest.mark` with `@m.slow` is the same. Such a marker would defer a node to the slow lane without a measured cost in the registry, which is the gate failing open. The gap predates #745, and no such spelling exists in the tree today. In the other direction, `benchmark.slow` in a helper is refused, which fails closed.

Fix (pick one, the reviewer's options):
- resolve the module's `import`/`from` aliases of `pytest` and `pytest.mark` before matching;
- tighten the match to `pytest.mark` or a resolved alias;
- or, for ground truth, have the slow lane's collection check that every item with `get_closest_marker("slow")` belongs to a declared function.

Done when: each of the three spellings above, added to a scratch copy of a test module, is either charged to its test or refused by `test_the_slow_marker_is_declared_only_by_measured_nodes`, with a test for each (negative control first: the test fails on the current scanner), and the registry still matches all its entries.

Parent note: filed under think-5ewf (PR #745 review addressing) as the brief directed; re-parent it if think-5ewf closes first, so the bead tree check does not flag an open child under a closed parent.
