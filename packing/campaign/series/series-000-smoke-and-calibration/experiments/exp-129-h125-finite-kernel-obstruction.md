---
title: exp-129 — one finite obstruction test for H125
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-129
  series: series-000
  title: Test the fixed biquadratic kernel family with exact finite objective evidence
  date: '2026-09-07'
  hypotheses: [H-125]
  tier: confirmatory
  subject:
    label: Fixed eleven-feature joint-D4 kernel family at side96/25, restricted to the five tight axis grids
    engine: Once-only finite LP proposer and independently implemented exact projected-PSD objective reader
    engine_commit: d6f0c403
    assurance: numerically-checked
    method: numerical-f64
    precision: {binary_bits: 64, rounding: nearest ties-to-even for binary64 LP inputs and output; exact Fraction construction and checking follow proposal}
    tolerance: No floating value or solver status accepts the claim. One bounded rationalization is followed by exact projected PSD; independent threshold comparison has zero tolerance.
    host_system: macOS arm64, project Python3.14.7 and locked SciPy, GNU coreutils timeout9.9; one proposer and at most one independent reader
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      The max authors froze independently, then swapped code for soundness review.
      Seventeen producer,55 independent-reader and three cross-implementation
      controls passed without constructing either scientific source. A lower-nine
      certificate is accepted only at its own threshold and refused at eleven;
      exact source, PSD, normalization, geometry, parsing and limit mutations
      remain required. The immutable engine push and committed protocol checks
      are pending at registration and must actually pass before invocation.
    candidate: >-
      Exactly the four wall-translated tight3x3 axis grids with origins in
      {1/2,L-5/2} squared, plus the centered tight3x3 grid, at L=96/25.
      Deduplicate and sort exact centers. Keep all source diagonals, every
      compatible unordered pair including touching, the eleven declared features
      and23 fixed necessary PSD directions. One HiGHS call,30-second solver
      limit and10000 iterations; one rationalization at denominator at most1000000,
      absolute dual magnitude at most2^32, then exact normalization and PSD.
    runs_per_condition: 1
    interleaved: false
    operator: Session097 coordinator under BC264 and think-rzdb; independent max mathematical admission
    commit: d6f0c403
    dirty: false
    entry_point: packing/devtools/kernel_axis_lp.py
    command: >-
      /usr/bin/time -p /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 60s
      env PYTHONPATH=src OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
      MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.kernel_axis_lp --target-five-grids
    budget: >-
      Exactly one producer child. Only its actual exit0 and a complete packet
      with exact bound>=11 authorize one independent reader. Each complete child
      receives TERM at60seconds and KILL up to2seconds later, including imports,
      construction, arithmetic and serialization. Two invoked children permit
      at most124seconds of timeout envelopes plus supervision/coordination overhead;
      this is not a strict60-second total completion promise. Launch producer by
      22:20UTC September7 and finish all scientific work by22:27UTC or preserve
      refusal/non-invocation. No retry, changed feature/source, extra LP,
      target-informed repair or continuum build.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-129-h125-finite-kernel-obstruction
  lease:
    expires: '2026-09-07T22:27:00Z'
  results: []
  verdict:
    decision: in-progress
    primary_criterion: An independently reconstructed exact projected-PSD objective certificate proves b>=11 for exactly H125's fixed family.
    reason: Prospective once-only protocol registered before either scientific source is constructed; actual passing engine/protocol checks, final protocol review and publication are still required.
---
# exp129 — One Finite Kernel-Family Obstruction Test

This is a prospective test of [H125](../../../hypotheses/H-125-biquadratic-two-pose-kernel.md),
not a positive kernel certificate or a packing-bound search.
No scientific source, solver target or target packet has been constructed at registration.
The [feature design and reader review](../results/agenda-027/bc-264-kernel-feature-design.md)
and [kernel contract and producer review](../results/agenda-027/bc-264-kernel-acceptance-review.md)
accept only this fixed finite refutational route.
The source-free build's75 controls do not measure H125.

## Admission Before Invocation

Engine `d6f0c403` contains the frozen producer, separate exact reader and three
source-free test files. It differs from code commit `5336a518` only in the rendered
session ledger. The first engine gate may therefore expose that corrected ledger
drift; an actual passing required gate on the executed immutable revision is still
required. The previous docs-only PR116 gate is not an instrument gate.

Before launching, record the completed independent protocol review, passing engine
push, passing checks of this committed prospective record, its publication on PR116,
and the actual engine/protocol revisions. `selftest_passed` refers to the completed
source-free controls, not pending whole-checkpoint validation.
The full gate remains a separate checkpoint obligation and may run asynchronously.
Any unsatisfied prerequisite at the launch cutoff means no invocation, zero scientific
wall time and an explicit blocked guard outcome. Do not borrow finalization time.

Run from the clean immutable engine checkout's `packing/` directory, with its `src`
first on `PYTHONPATH` and the locked project interpreter supplying dependencies.
Do not run from the coordinator's changing worktree or import an archived executable.
The complete fixed source must be reconstructed by each actually invoked scientific
process. Those two constructions are the separately admitted producer and reader,
not permission for an additional source probe or exploratory solve.

## Output and Process Contract

Resolve the declared repository-relative result directory against
`/Users/levy/wrk/github/squares`, not the immutable engine checkout's working directory.
This is the same root used by the reader's absolute input path below.
Exclusively create that result directory with `mkdir`, without `-p`; an
existing directory refuses launch. Use shell no-clobber mode for every output stream.
The directory is a live attempt record, not an atomically published claim of completion.
Retain producer stdout in `producer.json`, stderr and external wall/user/system time
in `producer.log`, and the actual tool exit in the outcome record.
Empty or partial output remains evidence. Never truncate or regenerate it.
There are no repository-integrity hash manifests.

The producer command is fixed in the frontmatter. It calls HiGHS once and attempts
one bounded rationalization. Its internal30-second limit excludes startup and tail;
the external60-second TERM and two-second KILL grace cover the entire child.
Use the fixed one-thread environment for both calls. No loop, second solve, changed
denominator or source expansion follows a numerical or exact-check failure.

Only if the producer actually exits zero and its intact seven-key packet has a
canonical rational `bound >= 11` may the independent reader run once:

```bash
/usr/bin/time -p /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 60s \
  env PYTHONPATH=src OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /Users/levy/wrk/github/squares/packing/.venv/bin/python3 \
  -m devtools.check_kernel_axis_lp \
  --input /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-129-h125-finite-kernel-obstruction/producer.json
```

Keep its stdout in `verification.json` and stderr/timing in `verification.log`, also
with exclusive creation. Do not create reader output paths unless the reader runs.
Checking retained producer bytes to decide this trigger is not a new source or solver
invocation; it cannot supply mathematical acceptance in place of the independent reader.

The packet limit is2MiB, with at most45 exact poses and990 positive-weight pairs.
Source rationals have128-bit limits; certificate rationals4096-bit limits.
The producer refuses4096-bit intermediate growth; the reader permits at most32768 bits.
These arithmetic limits supplement, not replace, the whole-child supervision.

## Exact Acceptance and Terminal Disposition

Acceptance requires actual reader exit zero and all of these positive predicates:
`status=verified_objective_bound`, `source=five-tight-axis-grids-v1`, `side=96/25`,
`minimum_bound=11`, exact `bound >= 11`, literal `projected_psd_verified=true`,
literal `scientific_family_refuted=true` and literal `new_packing_bound=false`.
Require complete source, pose/pair counts and projected-rank metadata consistent with
the fixed instrument; the reader reconstructs all geometry and matrices itself.
`pose_count` must equal the length of the packet's complete `poses` inventory;
`pair_count` must equal `len(beta)`, its positive sparse proof support, not the number
of compatible rows considered by the proposer. `projected_ranks` contains the exact
ranks of the reconstructed $4\times4$ and $2\times2$ blocks, respectively.
Unknown or missing acceptance fields prevent promotion.

The reader checks $\alpha\ge0$, $\sum\alpha=1$, positive sparse compatible-pair
weights $\beta$, and exact PSD of the reconstructed invariant matrices and scalars.
The full vector-block trace is retained. Hence every kernel in H125 obeys
$b\ge1+\sum\beta\ge11$. Record H125 as rejected and the obstruction question as
`criterion_met` only after that independent acceptance; then the outcome assurance
may become `verified` with `exact-algebraic` method. Preserve the numerical proposer
provenance in this protocol and the retained receipt.

A producer packet below eleven, outer-LP feasibility, solver failure or failed
rationalization leaves H125 unresolved. It supplies no PSD candidate, LP-optimality
claim or positive continuum certificate. Do not invoke the reader for a bound below
eleven. Any timeout, malformed packet or reader refusal also remains unresolved;
retain the actual stage, exit, partial output and wall/user/system times.
Remove the lease and record every terminal outcome. A timebox outcome names these
retained artifacts in `resume_from` while explicitly prohibiting an unchanged retry.

No outcome here rejects H114 as a whole, establishes Trump optimality, certifies a
candidate kernel, improves the published lower bound or permits feature expansion.
BC264's next decision must compare this family-scoped result with the retained
alternative agendas rather than automatically raising degree.

The complete22:00:19 UTC ownership audit found exp129 absent from landed main
`a5e9dbfd` and every open PR inventory/body, with no competing reservation.
This round allocates only exp129 under existing H125, BC264 and Session097.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
