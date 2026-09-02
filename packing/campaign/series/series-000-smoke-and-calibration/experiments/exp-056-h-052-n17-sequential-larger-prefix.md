---
title: exp-056 — H-052 n = 17 sequential larger prefix
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-056
  series: series-000
  title: Continue the reviewed exp-052 chain from ordinal 33 in a parent-bound child chain
  date: '2026-09-02'
  hypotheses:
  - H-052
  tier: confirmatory
  subject:
    label: exact all-direction agreement for the retained n = 17 weighted certificate
    engine: sqpack n17 parent-bound child certificate driver 0.1.0-preregistered
    engine_commit: 11ce70ee
    assurance: verified
    method: exact-algebraic
    host_system: linux aarch64 container, Python 3.14
    selftest_passed: true
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: >-
      Byte-identical synthetic self-test receipts under normal and optimized Python over
      named guards on synthetic directions only: parent-verification refusal, chain
      continuity from the frozen parent row hash, tampered-row rejection, parent-path and
      resume-package write refusal, interrupted-versus-uninterrupted equivalence, result
      overwrite refusal, and a retained synthetic disagreement row. No target direction is
      evaluated by any control.
    candidate: >-
      A child driver that verifies the frozen exp-052 checkpoint, progress marker and
      package manifest, copies the reviewed 33 parent rows verbatim into a fresh exp-056
      checkpoint under a binding block naming the parent hashes, and then continues
      ordinals 33--180 by importing and calling the unchanged exp-052 accumulators and
      checkpoint machinery from `cases.n17_weighted_certificate_resume`, appending one
      canonical hash-chained row per direction.
    runs_per_condition: 1
    interleaved: false
    operator: claude-opus-5
    commit: 11ce70ee
    dirty: true
    entry_point: cases/n17_weighted_certificate_child/run.py
    command: >-
      uv run --frozen python -m cases.n17_weighted_certificate_child.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.json
      --checkpoint
      campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.checkpoint.json
      --progress
      campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.progress.json
    budget: >-
      Agenda-015 BC-137 gives the process both waves under coordinator observation. The
      process is launched by the coordinator, never by the lane, and stops at the
      agenda's 06:20 elapsed boundary, 2026-09-02T11:23:00Z on the wall clock, whatever
      its row count. Boundary observations use
      `--status` every 25 minutes; two consecutive boundaries without a new row is a typed
      no-progress stop; the first exact disagreement stops the process and is retained.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.json
  effort:
    timebox: >-
      The BC-137 wave-one and wave-two allocation ending at the agenda's fixed 06:20
      elapsed boundary, 2026-09-02T11:23:00Z on the wall clock; the checkpoint at that
      boundary is retained and never resumed inside this wall.
    stopped_by: timebox
  results: []
  lease:
    expires: '2026-09-02T11:23:00Z'
    host: claude-code-remote linux container, session-078
    pid: 20747
  verdict:
    decision: in-progress
    needs_review: true
    primary_criterion: >-
      Accept H-052 only if all 181 paired rows agree exactly and every frozen fixture,
      binding, chain, mutation and independence guard passes. A larger contiguous agreeing
      prefix is process evidence and moves no bound; the first exact disagreement is a
      retained result that may reject only after every instrument guard passes.
    reason: >-
      Registered before the process runs; no exp-056 result exists yet, so H-052 is
      neither accepted nor rejected by this round.
    commit: 11ce70ee
    resume_from: >-
      Frozen exp-052 parent checkpoint SHA-256
      db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8, parent progress
      SHA-256 08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af, parent
      last row hash
      9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6 and frozen package
      manifest 309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54. The child
      chain starts at ordinal 33 in the fresh exp-056 checkpoint and never rewrites an
      exp-052 path.
---
# Exp-056 — H-052 `n = 17` Sequential Larger Prefix

Exp-052 stopped at its declared timebox with a reviewed 33-row prefix and no result.
This round changes only where the sequential process starts.
It reuses the admitted exp-052 driver without editing it, and it does not change H-052’s
all-direction agreement criterion.

## Frozen Bindings

| Binding | Value |
| --- | --- |
| Parent checkpoint SHA-256 | `db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8` |
| Parent progress SHA-256 | `08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af` |
| Parent last row hash | `9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6` |
| Parent binding hash | `2446fa39e154800410b9b5cc19f19aed7cc0c797d116f7ece1c97a2c7c0b4d1a` |
| Frozen package manifest | `309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54` |
| Unchanged resume driver | `cases/n17_weighted_certificate_resume/run.py` |

Every one of those is verified before the child driver opens a chain, and a mismatch in
any of them refuses the run before a single direction is evaluated.

## Fresh Paths

The result, checkpoint and progress paths share the `exp-056` slug and were absent at
preregistration:

- `campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.json`
- `campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.checkpoint.json`
- `campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.progress.json`

The child driver binds `campaign/series/series-000-smoke-and-calibration/results/` as its
only writable output root and refuses every lexical or resolved-path escape, every path
carrying the `exp-052` slug, and every path under
`cases/n17_weighted_certificate_resume`. A checkpoint is process evidence, not a result,
and a progress marker can never stand in for a completed paired row.

## Instrument Hashes

Recorded at registration, before the process was launched:

| Artifact | SHA-256 |
| --- | --- |
| `packing/cases/n17_weighted_certificate_child/run.py` | `f45227508b28f37759df836db08dbad2031d600ef2b1ac087b73f8322b156b05` |
| `packing/cases/n17_weighted_certificate_child/__init__.py` | `ce25d0c6f97d463833260561fdc06b9434c3a9539d3aee9aabd7a98a268778fb` |
| `packing/tests/test_n17_weighted_certificate_child.py` | `3aa7c0b1816d3545dbf7e77e4fa31f3dc58d5ab727ffb5ad25f64c3049ee137a` |
| Unchanged `packing/cases/n17_weighted_certificate_resume/run.py` | `3e5284fd56fd33f7b767954164128e9d43f5efad09eae4666035c3ef32c63f54` |
| Self-test receipt, normal and optimized | `9d6cbdc83ad83bf5234b872d67931b7003a038fa870ebc426133368e8e43a28e` |
| Self-test guard inventory | `612349379b70ccddfa5bd4f5265a747caca768c5b9a9627b4057e69a5791f894` |

Thirty-six named guards pass with zero skips over synthetic directions only.
Boundary observation uses
`uv run --frozen python -m cases.n17_weighted_certificate_child.run --status
campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.checkpoint.json`,
which reports the row count, last ordinal, last row hash and agreement state without
loading the retained fixture.

## Claim Boundary

This round can produce a larger contiguous agreeing prefix or all 181 pairs.
Agreement alone moves no bound: it does not adopt the retained certificate as a frontier
result, does not decide H-052 on a prefix, and does not open any `n = 17--19` lower-bound
transition, which needs the separate adoption gate.
The first exact disagreement is a retained result, not a failure.

## Stopped-By Rules

The process stops, retains its checkpoint and records why when any of these holds:

1. **Boundary stop.** The fixed 2026-09-02T06:20:00Z wall arrives, whatever the row count.
2. **No progress.** Two consecutive 25-minute boundary observations show no new row.
3. **Disagreement.** A direction's two manifests differ exactly; the row is kept and the
   process stops.
4. **Drift.** A frozen input, parent hash, package manifest or chain link fails
   verification, in which case nothing is written at all.

## Start and Immutability

The child chain starts at ordinal 33.
Ordinals 0--32 are the reviewed parent rows, copied verbatim with their original hashes
and re-verified against the parent binding genesis, so the retained parent evidence is
carried rather than recomputed.
Exp-052's record, result, checkpoint and progress paths are never written, and the
exp-052 package is imported, never edited.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
