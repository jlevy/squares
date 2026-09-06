# BC-251 Scalar Readiness Audit

BC-251 / H-093, readiness child `think-zuq5`, 2026-09-06. This is a read-only source
audit within the coordinator’s `19:57:28–20:12:28 UTC` allocation.
No control command, optimization, target experiment, or full source replay was run.
Local `origin/main` still names `c14451f5`; the reviewed, open PR 100 head is
`237d9386`. Its code was read through Git and was not imported.

H-093 remains instrument-blocked until the fixes land and the focused controls below
pass on that landed code.
This audit found no additional blocking soundness defect in the bounded seed, cutting,
and bridge path review.
It does not commission the instrument or authorize the scalar probe.

## Required Landed Controls

PR 100’s changes cover the large-input screen failure, intermediate cutting depth, and
float-identical vertices that erase a thin overlap.
The last defect matters even at small coordinates: its regression uses
`epsilon = 1/10^20` in a side-four container and requires screened separation and exact
vertex enumeration to return depth `2`, not `1`. The regression is
`test_float_identical_vertices_cannot_erase_a_thin_overlap` in
[the cutting tests](../../../../../tests/test_fractional_cutting.py); it is absent on
the currently recorded main revision.

After landing, run this single focused test command from `packing/`. It includes the
thin-overlap regression, bounded-screen and exact-fallback controls, the exact seed
maps, the driver’s safe crossing and artifacts, and the bridge’s positive and refusal
cases. These are existing or PR-100 controls, not another test search.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m pytest -q \
  tests/test_fractional_ceiling.py tests/test_fractional_cutting.py \
  tests/test_run_fractional_colgen.py::test_seed_sites_are_carried_to_the_new_side_by_the_map_named \
  tests/test_run_fractional_cutting.py tests/test_freeze_cutting_primal.py
```

The [bridge positive](../../../../../tests/test_freeze_cutting_primal.py) creates a
small terminal state at `L = 2`, `B = 2/3` on a two-direction net, freezes a covering
candidate with total in `[9,12)`, and requires the exact sweep to accept it.
Its companions refuse total at least `n`, missing row convergence, and output overwrite.
The [driver crossing control](../../../../../tests/test_run_fractional_cutting.py)
separately checks all four output artifacts and passes its stopped state into the
bridge. Neither optimizes the H-093 target.

One zero-iteration integration control then exercises the actual retained seed through
the production driver, at its original side rather than `61/16`:

```bash
scalar_readiness_dir=$(mktemp -d /private/tmp/squares-bc251-readiness.XXXXXX)
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 381/100 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 0 --iterations 0 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 --stop-on-covering-below-n \
  --seed-certificate cases/n11_fractional_certificate/certificate.json --seed-map scale \
  --json "$scalar_readiness_dir/seed-control-summary.json"
jq -e '.settings.seed_sites == 1121 and .settings.outer_side == "381/100"
  and .settings.seed_map == "scale" and (.iterations | length) == 0
  and .frozen == null' "$scalar_readiness_dir/seed-control-summary.json"
```

Expected: the summary records all `1,121` seed sites, no iteration, and no frozen
family. No state or covering candidate is expected from a zero-iteration control.
The retained source declares `L = 381/100`, `B = 9977/10000`, 180 steps, total
`434547/40000`, and minimum `4001/4000`; this audit read its metadata, not its coverage.
Seeding uses only coordinates, so the source’s old weights and verdict are not imported
as evidence at another side.
The changed-side scale map is already covered by the unit test; for the eventual target
its exact scale factor is `1525/1524`.

## Assumptions Outside PR 100

- Use the
  [continuation addendum’s scalar command](../../../../../../docs/project/handoff-2026-09-06-post-381-t2-t10-continuation.md#scalar-6116-launch),
  which includes `--stop-on-covering-below-n`. The older command in Agenda 025 omits
  that flag. Do not silently drop the safe crossing when restoring readiness.
- A row-converged LP value is a numerical proposal.
  The bridge snaps rows, re-solves, and rationalizes; its null-minimum candidate still
  needs declaration, production sweep plus interval agreement, and the standalone
  `--unpinned` decision.
  PR 100 does not make floating row convergence or a finite-site optimum a theorem.
- A state stores direction indices, not its direction net.
  The bridge must receive the frozen `207107/500000`, 180-step net, `n = 11`, and the
  correct terminal state; its stored side and core side must match the intended
  instance. The bridge reads the state twice, so it must not race an active cutting
  writer. These are existing handoff preconditions, not a request for another checksum
  layer.
- The 150-minute process limit and 1,200-second bridge row-generation deadline are
  cooperative. Final solves, separation, verification, serialization, and startup or
  teardown are not all stopped by those clocks.
  Preserve the coordinator’s process handle, fresh output paths, tail accounting, and
  terminal-state boundary.
- The interpolation between the 3.81 certificate mass and the 3.82 restricted LP value
  motivates a probe only; it supplies no slope bound or existence prediction with a
  certified error. A timeout or finite-site optimum above eleven leaves H-093 open.
  An exact depth-at-most-one family of weight at least eleven addresses only the frozen
  scalar language; the unit-square packing question remains separate.

These are the minimal controls recommended before the coordinator lifts the identified
readiness hold after landed-code review.
They do not start the 150-minute invocation, revive BC-232, change H-093’s criterion, or
authorize further BC-231 implementation.
No additional useful read-only audit remains in this selected slice.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
