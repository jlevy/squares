# Review Packets: Agenda 013 Second Wave

**Date:** 2026-09-01

**Author:** Codex, for the project maintainers

**Status:** Frozen BC-119 packet set for BC-120 independent review

These three packets reconcile agenda-013’s first- and second-wave decisions for n = 17,
n = 68 and n = 50. They are review instructions, not new experiments.
Reviewers must judge the retained evidence without repairing it, retrieving a target or
weakening a claim boundary.

## Frozen Revision and Common Contract

The evidence revision is `529b6729155458c940999cd11074f05ae9f1ce3d`. Every scientific
source, experiment, result, checkpoint, progress marker, test and lane session named
below is read from that revision.
Later commits may add review and state records only; any change to a listed evidence
path invalidates the packet.

Each reviewer works read-only against one lane that the reviewer did not author.
Run Python only from `packing/` with `uv run --frozen`. Mutations use pytest temporary
paths or an operating-system temporary directory and must not alter a retained artifact.
Reviewers do not run n = 17 target accumulation, make an n = 68 network or parent/child
request, interpret n = 50 geometry, or create a registered result.

For each experiment, report one of:

- **pass:** the exact decision, evidence boundary and limitation reproduce;
- **bounded caveat:** the outcome reproduces, but a material frozen limitation prevents
  review clearance;
- **discrepancy:** retained evidence contradicts the recorded decision or boundary; or
- **cannot-reproduce:** the named replay cannot be completed at the frozen revision.

A pass grants BC-121 permission to change only that experiment’s `needs_review` field
from `true` to `false`. It does not change the decision, hypothesis, frontier or
instrument state.
Any other determination leaves `needs_review: true`. Each response uses
the four campaign fields: **Artifact, Result, Guard, Next**.

Before a lane replay, confirm that
`git diff --exit-code 529b6729 -- <listed evidence paths>` is empty.
The packet’s hashes are SHA-256 values of bytes at the full frozen revision, not claims
about later working-tree bytes.

## Packet A: n = 17 / H-052

### Decisions under review

| Experiment | Frozen decision | Evidence status | Proposed BC-121 transition |
| --- | --- | --- | --- |
| exp-049 | `unresolved`, `needs_review: true` | One 3,920-second process ended at the timebox with exit 130; result and checkpoint absent | Clear review only if the no-result process decision and boundary pass |
| exp-052 | `unresolved`, `needs_review: true` | One 4,456-second process retained 33/181 contiguous agreeing rows and ordinal-33 progress; result absent | Clear review only if the checkpoint/progress replay and incomplete-result boundary pass |

H-052 remains scientifically unresolved under either pass.
The 33-row prefix is process and resumability evidence, not a sample-based H-052 result.
No frontier transition is proposed.

### Frozen bytes

| Artifact | SHA-256 |
| --- | --- |
| exp-049 record | `f8bbb64a561198c07cfc80548014d090f5b6a9baf27e619017544979854abb92` |
| exp-052 record | `bd4881bc218b59267e25f4c161c2947a445e8d509d31502fbcde63c3b0edefa1` |
| exp-052 checkpoint | `db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8` |
| exp-052 progress marker | `08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af` |
| session-068 | `7d88fd733f35e276db7a98ef652ee8303a06db29c777a9f616e774f6b6135a72` |
| resumable driver | `3e5284fd56fd33f7b767954164128e9d43f5efad09eae4666035c3ef32c63f54` |
| focused test | `4226ab0cb5f9e46256b5fc47d5bc493dfbb6ef77354e9e7a61d624ba4db76a53` |

The frozen scientific-package manifest is
`309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54`. The normal/optimized
self-test receipt is `beaf5b2b9bcaa0b95ff053c8f6e0aa955d075d21d877460c52b779a68d60ca60`.

### Required replay and guard

1. Confirm the exp-049 result is absent and that its record says no checkpoint or
   partial canonical record exists.
   Do not rerun exp-049.

2. Confirm the exp-052 result is absent and recompute the checkpoint, progress, driver
   and focused-test hashes.

3. Use the frozen `CheckpointStore.load` and `read_progress` path with the production
   binding already serialized in the checkpoint.
   It must return 33 contiguous rows, ordinals 0--32, exact agreement on every pair,
   last-row hash `9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6`, and
   progress ordinal 33 at `independent_started` chained to that row.

4. Run:

   ```text
   uv run --frozen --all-extras --group dev pytest -q tests/test_n17_weighted_certificate_resume.py
   uv run --frozen python -m cases.n17_weighted_certificate_resume.run --selftest
   ```

5. The required mutation is `test_changed_row_hash_is_rejected`; it must reject a
   changed row hash in a temporary checkpoint.
   Also confirm that the production `--record` command is not invoked, because that
   would resume target work rather than review retained evidence.

### Required boundary determination

Pass exp-049 only if the reviewer reproduces its executed no-result timebox and agrees
that it neither accepts nor rejects H-052. Pass exp-052 only if the exact retained
prefix replays and the reviewer agrees that 148 directions plus the frozen precondition
and mutation decisions remain unevaluated.
A row-count, chain, progress, hash, agreement or absence mismatch is a discrepancy.
Inability to exercise the retained loader is cannot-reproduce.

## Packet B: n = 68 / H-053

### Decisions under review

| Experiment | Frozen decision | Evidence status | Proposed BC-121 transition |
| --- | --- | --- | --- |
| exp-047 | `blocked`, `needs_review: true` | Target-blind numerical prototype failed outward interval-enclosure and complete-runner admission; no target access | Clear review only if the premeasurement refusal and no-target boundary pass |
| exp-051 | `blocked`, `needs_review: true` | Exact proof/verifier and injected runner controls pass, but the literal registered `--record` command exits 2 because the CLI has no production adapter; no target access | Clear review only if the literal-command refusal and boundary pass |

Neither experiment rejects H-053 or says anything about the n = 68 child’s feasibility,
gain or contacts. H-053 remains unresolved and instrument-unready.
No frontier transition is proposed.

### Frozen bytes

| Artifact | SHA-256 |
| --- | --- |
| exp-047 record | `b893023fca00e6c5f6958aa03a14ec8742b9500cab2527479d047dd205d10538` |
| exp-051 record | `e77c1252627e64291c753969609504baf2db7d7f885bd3c2fa1250d937478e6b` |
| session-069 | `7026e3fe1d26e10255a4023d688ad8c2e708dbbc2cade5707571e0cc448ff659` |
| proof producer and runner | `3d91046ad9d4ea7b3a7e2f3e7f1ca02aec7cd7118d2291a50f622e8541020029` |
| independent verifier | `1533210f9d8e17cbdfa822da59187d280fc4ab063816644825c50d7b8b24552f` |
| focused test | `7cc3a7f59d74e78648966af0ecf88443abfe99432213d30bcb33dee568f3f3c8` |

The exp-051 result path must be absent before and after review.

### Required replay and guard

1. Establish result-path absence, then invoke the literal registered command exactly:

   ```text
   uv run --frozen python -m cases.unitsquare_precision.refusal.run --record campaign/series/series-000-smoke-and-calibration/results/exp-051-h-053-n68-refusal-localization.json
   ```

   It must exit 2 in argument parsing, expose only `--selftest` and `--runner-selftest`,
   leave the result absent and make no network or target access.

2. Run both target-blind self-tests and the focused suite:

   ```text
   uv run --frozen python -m cases.unitsquare_precision.refusal.run --selftest
   uv run --frozen python -m cases.unitsquare_precision.refusal.run --runner-selftest
   uv run --frozen --all-extras --group dev pytest -q tests/test_unitsquare_precision.py
   ```

3. The required mutation is `test_refusal_independent_verifier_rejects_named_mutations`.
   At least one parameterized source-binding, cover, corner-image, wall-sign or
   pair-sign mutation must reject.

4. Inspect exp-047’s precision block and confirm that fixed binary64 tolerances and
   heuristic radii are explicitly not outward interval certificates.

### Required boundary determination

Pass exp-047 only if its interval-enclosure/runner refusal reproduces as an instrument
guard before target access.
Pass exp-051 only if the literal command reproduces exit 2 while the exact synthetic
proof residue still passes its independent verifier.
A target read, result creation, CLI behavior change or claim that either refusal rejects
H-053 is a discrepancy.
Do not write the missing adapter during review.

## Packet C: n = 50 / H-054

### Decisions under review

| Experiment | Frozen decision | Evidence status | Proposed BC-121 transition |
| --- | --- | --- | --- |
| exp-048 | `unresolved`, `needs_review: true` | E1 source/provenance dependency stopped before reconstruction, with no result | Clear review only if the premeasurement refusal and no-geometry boundary pass |
| exp-050 | `unresolved`, `needs_review: true` | Executed ordered E1 reason 3, `attribution-unbound`, with zero cells; immutable result exists | Known producer-runner binding gap requires at least `bounded caveat`; leave review pending unless the reviewer disproves that materiality |

Neither experiment reconstructs n = 50, verifies the `53/7` pose, dispositions H-054 or
supports work on n = 39 or n = 54. H-054 remains unresolved and instrument-unready.
No frontier transition is proposed.

### Frozen bytes

| Artifact | SHA-256 |
| --- | --- |
| exp-048 record | `6b336d391489a23cd844b64049a00a4f49928be8799db6e579a8dcc32c8d24ae` |
| exp-050 record | `7a72174c29a8a12e39e13443a0885b97b29ba5387f81baa824508582bfdbd212` |
| exp-050 result | `ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02` |
| session-070 | `bc69821b25060d37d2f6bfa0ccfb46051921a3d950d8a217d632ac01f457f68e` |
| intake module | `fed71cf825906bd09f3711ec0a465dce0e4aecb91a1128f3a9d792e59c7c8d0c` |
| producer runner | `52baeb1b6ad52aa504498ba21aeb6b3d361aaaec2461c76904a357d8d95cf29d` |
| independent verifier | `b43e5c99ca657ed168b8d57188abe24c3796e845b47ce73d37c23870f972c77e` |
| independent test | `99fd0f29eb18b014bccbf02682fdac7944c0186e9a6ea11c709d30ca009769a7` |

The result binds four input hashes but does not bind the producer-runner hash listed
above. That omission is a packet fact, not an instruction to edit exp-050.

### Required replay and guard

1. Confirm the exp-048 result path is absent and that its source-cell admission stopped
   before reconstruction.

2. Run the immutable-result verifier and independent suite:

   ```text
   uv run --frozen python -m cases.n050_exact.verify_source_semantics_result --result campaign/series/series-000-smoke-and-calibration/results/exp-050-h-054-n50-source-semantics-e1-localization.json
   uv run --frozen --all-extras --group dev pytest -q tests/test_n050_exact_independent.py
   ```

   The replay must report reason index 3, `attribution-unbound`, zero cells, four bound
   artifacts, 171 retained n = 19 pair facts, zero skips and `needs_review: true`.

3. The required mutation is
   `test_independent_missing_semantics_control_refuses_before_cells`; it must return
   reason 4 with zero cells.
   The changed-result and duplicate-key mutations must also reject in the complete
   focused suite.

4. Run the literal registered exp-050 command against the existing result.
   It must exit nonzero with `result already exists`, and the result SHA-256 must remain
   unchanged.

5. Inspect the immutable result and verifier for the producer-runner digest.
   Confirm whether its absence means the durable record cannot prove
   refusal-before-evaluation under a later mutated, unbound runner, even though current
   code orders the check correctly.

### Required boundary determination

Pass exp-048 only if the evidence establishes a premeasurement source-semantics
dependency and no geometry work.
For exp-050, reproduce the executed E1 result and then judge the frozen
producer-provenance omission.
The expected determination is `bounded caveat`: retained bytes support the reason-3
refusal, but do not durably bind the runner whose ordering is part of the claim.
A different determination must name exact contrary evidence.
Review does not rerun n = 19 geometry and cannot promote n = 50.

## Coordinator Reconciliation Rule

BC-120 records all six experiment determinations separately.
A lane-level pass cannot hide a caveat on one experiment.
BC-121 applies only explicitly cleared `needs_review` transitions and otherwise
preserves the frozen decision verbatim.
Source or result repairs become newly registered future work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
