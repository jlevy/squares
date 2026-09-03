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
    host_system: linux aarch64 container to macOS arm64 bridge, Python 3.14 exact-algebraic
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
    operator: claude-opus-5 then openai-codex-max-equivalent coordinator
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
      One fixed elapsed lease from the registered 2026-09-02T05:27:00Z launch through
      the agenda's 06:20 elapsed boundary, 2026-09-02T11:23:00Z on the wall clock. The
      lease includes the interrupted host handoff because its hard stop did not move;
      the checkpoint at that boundary is retained and never resumed inside this wall.
    wall_seconds: 21360
    stopped_by: timebox
  results:
  - shape: determination
    question: >-
      Did the sole preregistered continuation finish all 181 paired directions inside
      its fixed two-wave lease while preserving a replayable terminal artifact?
    role: cost
    outcome: criterion_missed
    checked_by: >-
      Post-interrupt status replay validated 170 contiguous agreeing rows, ordinals
      0--169, and the chained ordinal-170 independent-start marker; 17 focused controls
      pass, normal and optimized 36-guard self-tests are byte-identical, and the
      canonical result path remains absent.
  verdict:
    decision: unresolved
    needs_review: false
    primary_criterion: >-
      Accept H-052 only if all 181 paired rows agree exactly and every frozen fixture,
      binding, chain, mutation and independence guard passes. A larger contiguous agreeing
      prefix is process evidence and moves no bound; the first exact disagreement is a
      retained result that may reject only after every instrument guard passes.
    reason: >-
      The fixed 11:23Z timebox ended before all 181 paired rows completed. The retained
      170-row prefix is valid process evidence, every completed pair agrees exactly and
      the interrupted ordinal was not appended, but a prefix does not satisfy H-052's
      all-direction criterion. No canonical result exists, so H-052 remains neither
      accepted nor rejected and the terminal decision stays review-pending for BC-145.
    commit: 11ce70ee+sha256-f45227508b28f377
    resume_from: >-
      Canonical child checkpoint SHA-256
      0d39a7e734e8afc62fda914fda4ec8b5e9b2e48ea1b1d8b197dc08e27e7a35d4 contains the
      validated contiguous prefix through ordinal 169, whose last row hash is
      8947b38e0351048c3a67d914f2b8449185686d920913f5a2404898bdeca4c0b6. Canonical
      progress SHA-256 0875f31fbf7391cfa40349812ca38a786069830a28f1c8d92ffd4ab33ecfe93c
      records ordinal 170 at independent_started, chained to that row. Any continuation
      requires a newly preregistered round that replays the frozen parent and child
      bindings and resumes at ordinal 170; exp-056 itself must not be rerun.
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

The child driver binds `campaign/series/series-000-smoke-and-calibration/results/` as
its only writable output root and refuses every lexical or resolved-path escape, every
path carrying the `exp-052` slug, and every path under
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
`uv run --frozen python -m cases.n17_weighted_certificate_child.run --status campaign/series/series-000-smoke-and-calibration/results/exp-056-h-052-n17-sequential-larger-prefix.checkpoint.json`,
which reports the row count, last ordinal, last row hash and agreement state without
loading the retained fixture.

## Claim Boundary

This round can produce a larger contiguous agreeing prefix or all 181 pairs.
Agreement alone moves no bound: it does not adopt the retained certificate as a frontier
result, does not decide H-052 on a prefix, and does not open any `n = 17--19`
lower-bound transition, which needs the separate adoption gate.
The first exact disagreement is a retained result, not a failure.

## Stopped-By Rules

The process stops, retains its checkpoint and records why when any of these holds:

1. **Boundary stop.** The fixed 2026-09-02T11:23:00Z wall arrives, whatever the row
   count.
2. **No progress.** Two consecutive 25-minute boundary observations show no new row.
3. **Disagreement.** A direction’s two manifests differ exactly; the row is kept and the
   process stops.
4. **Drift.** A frozen input, parent hash, package manifest or chain link fails
   verification, in which case nothing is written at all.

Correction, 2026-09-02: the registration prose previously rendered the elapsed `06:20`
boundary as `06:20Z`. The frontmatter and agenda both bind elapsed `06:20` to `11:23Z`;
only the prose timestamp was wrong, and this correction changes no criterion, budget or
evidence.

## Terminal Outcome

BC-137 stopped at the fixed 11:23Z boundary after one authorized interrupt.
The retained checkpoint contains 170 contiguous rows through ordinal 169; all completed
pairs agree exactly and the chain verifies.
The progress marker records ordinal 170 at `independent_started`, so the interrupted
calculation was not promoted to a partial row.

Seventeen focused tests pass after the interrupt.
Normal and optimized self-tests each report 36 guards, zero skips and receipt hash
`612349379b70ccddfa5bd4f5265a747caca768c5b9a9627b4057e69a5791f894`. The canonical result
remains absent. This is an unresolved timebox outcome and process-cost measurement, not
an H-052 decision or a packing-bound transition.
BC-145 must independently replay the frozen checkpoint, absence boundary and one named
interruption mutation before `needs_review` can clear.

## Interrupted and Resumed Handoff

The registered writer began as Linux/Claude PID 20747 with a lease through `11:23Z`.
After the coordinator host handoff, the recovery checkout could observe neither that
process nor any exp-056 output path.
The owner confirmed that a matched Claude-to-Codex and Linux-to-macOS handoff is a
continuation when the exact inputs, instrument bytes, checkpoint chain, criteria, and
guard receipts still match.

At `05:40Z` the coordinator started the literal registered command on macOS under Codex.
It reproduced the 33 frozen parent rows and completed one agreeing child row at ordinal
33\. The coordinator paused on a provenance question, then resumed the same checkpoint
after the owner clarified the bridge rule.
The pause changed no scientific input or result.

At the `05:53Z` observation, the resumed checkpoint had 34 rows and last row hash
`dd34a2f7df3d78e5a89babb3f31f6658d96d3dd63f259777503c15e00f467e01`, and SHA-256
`06c0cc6eed7050e9183ebfd8837342ff7ade570331781112f391f031ceeceec2`. Its progress marker
was at ordinal 34, stage `independent_started`, with SHA-256
`90c5890a93c45103e9ba7d9d2c335edc111825450d59e62233a34110af0b5b32`. The canonical result
was absent at resumption.
Those hashes preserve the handoff observation; the live checkpoint and progress files
continue to advance under the lease.
The round still requires all 181 paired rows to decide H-052, and the fixed `11:23Z`
boundary did not move.

## Start and Immutability

The child chain starts at ordinal 33. Ordinals 0--32 are the reviewed parent rows,
copied verbatim with their original hashes and re-verified against the parent binding
genesis, so the retained parent evidence is carried rather than recomputed.
Exp-052’s record, result, checkpoint and progress paths are never written, and the
exp-052 package is imported, never edited.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
