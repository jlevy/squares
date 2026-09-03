---
title: exp-059 — H-052 n = 17 fresh successor completion
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-059
  series: series-000
  title: Complete the H-052 chain from ordinal 170 in a fresh successor with a decidable result envelope
  date: '2026-09-03'
  hypotheses:
  - H-052
  tier: confirmatory
  subject:
    label: exact all-direction agreement for the retained n = 17 weighted certificate
    engine: sqpack n17 fresh successor certificate driver 0.1.0-preregistered
    engine_commit: 2f112f4c
    assurance: verified
    method: exact-algebraic
    host_system: linux x86_64 container, Python 3.14.7 exact-algebraic
    selftest_passed: true
  instance:
    axis: n
    point: 17
    role: target
  method:
    control: >-
      Byte-identical synthetic self-test receipts under normal and optimized Python over
      115 named guards on synthetic directions only: both ancestries verified and shown
      non-substitutable, the carried prefix anchored at the exp-052 genesis binding and
      terminating on the exp-056 boundary row, an incomplete chain, a changed retained
      row, a swapped ancestry, a noncanonical checkpoint, a wrong progress binding, a
      wrong previous-row hash, a wrong ordinal, a wrong stage, a missing summary, a wrong
      global minimum, a false precondition, a surviving mutation, a result overwrite, a
      path escape and a retained disagreement each refused, plus
      interrupted-versus-uninterrupted equivalence. No target direction is evaluated by
      any control.
    candidate: >-
      A successor driver that verifies the frozen exp-056 checkpoint, progress marker and
      binding as its immediate parent while separately verifying the frozen exp-052
      checkpoint, progress marker and binding as its carried-chain genesis; cross-checks
      that the genesis rows are a proper prefix of the parent's and that row 0 is
      anchored at the genesis binding hash; copies the 170 verified rows verbatim into a
      fresh exp-059 checkpoint; recomputes the interrupted ordinal 170 rather than
      promoting its payload-free marker; and continues to ordinal 180 by importing and
      calling the unchanged exp-049 accumulators through its own checkpoint machinery,
      appending one canonical hash-chained row per direction.
    runs_per_condition: 1
    interleaved: false
    operator: claude-opus-5
    commit: 2f112f4c
    dirty: true
    entry_point: cases/n17_weighted_certificate_successor/run.py
    command: >-
      ./.venv/bin/python3 -m cases.n17_weighted_certificate_successor.run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.json
      --checkpoint
      campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.checkpoint.json
      --progress
      campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.progress.json
    budget: >-
      Agenda-016 BC-148 gives the writer one fixed repository-wide process-exclusive
      lease, 2026-09-03T08:58:00Z through 2026-09-03T09:58:00Z. The process is launched
      by the coordinator, never by the lane, and stops at that boundary whatever its row
      count. Measured cost before the lease: 182.6 s for one real direction, and the
      eleven remaining directions carry 10.988 times that direction's event-cell count,
      so 33.4 minutes of accumulation and about 35 minutes in total. The first exact
      disagreement stops the process and is retained.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.json
  effort:
    timebox: >-
      One fixed repository-wide process-exclusive lease, 2026-09-03T08:58:00Z through
      2026-09-03T09:58:00Z, declared before the writer was launched. The process is
      launched by the coordinator, never by the lane.
    wall_seconds: 1991
    agent_minutes: 165
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Does a fresh successor's independently written exact accumulation agree with the
      source-faithful path on all 181 paired direction cells, both complete
      CertificateManifest summaries, every row minimum and the global minimum for the
      retained n = 17 certificate?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      The published result was re-validated from its bytes on disk: the file is exactly
      canonical, and validate_result re-derived the whole admission boundary, rebuilding
      all 181 hash-chain links from the two summaries alone and reproducing the emitted
      chain spine, the carried boundary 8947b38e at ordinal 169 and the last row hash
      60e58a70. Both 181-row summaries are identical, atom count 168, atom hash 37d35da0,
      direction hash cc789e1a, total weight 203/12, and every one of the 181 row minima
      is exactly 1/1, so the global minimum is 1/1.
  - shape: determination
    question: >-
      Did every declared instrument guard hold, so that agreement is decidable rather
      than merely observed?
    role: guard
    outcome: criterion_met
    checked_by: >-
      preconditions_pass, shrink_and_scaling.all_hold, all_mutations_rejected over the
      five frozen mutations, and all twelve frozen certificate invariants are true, so
      instrument_valid is true. Each was re-derived from the emitted fields rather than
      read: a record whose decision, instrument validity, precondition conjunction,
      mutation conjunction or invariant set is asserted rather than derived is refused.
      Before the run, 115 named guards passed with zero skips under byte-identical normal
      and optimized Python, and 39 focused tests passed.
  verdict:
    decision: accepted
    needs_review: true
    primary_criterion: >-
      Accept H-052 only if all 181 paired rows agree exactly, both 181-row
      CertificateManifest summaries agree on every atom and direction hash, total weight,
      row minimum and the global minimum, the shrink-and-scaling preconditions hold,
      every frozen mutation is rejected and the instrument is valid. A larger contiguous
      agreeing prefix is process evidence and moves no bound; the first exact
      disagreement is a retained result that may reject only after every instrument guard
      passes.
    reason: >-
      All 181 paired direction cells agree exactly, both complete certificate summaries
      are identical with global minimum 1/1, every instrument guard holds and the
      decision derives to accepted from the emitted evidence, so the registered
      criterion is met at its declared scope.
    commit: 2f112f4c+sha256-ab4dd8fe66b15e8f7
  complexity:
    lines_changed: 3696
    new_dependencies: []
    new_failure_modes:
    - >-
      The successor CLI has no path that assembles a terminal schema from an existing
      checkpoint. On a disagreement the driver raises after retaining the row, so that
      invocation would publish nothing and schema (b) would need a later assembly step.
      The gap did not fire on this round, which agreed on every cell, and it is recorded
      because that is the outcome in which an omission is least likely to be noticed.
    notes: >-
      One new package and one new test module, importing the hash-bound exact definitions
      from three frozen packages and editing none of them.
---
# Exp-059 — H-052 `n = 17` Fresh Successor Completion

Exp-056 stopped at its fixed timebox with 170 contiguous agreeing rows and no result.
Its retained chain is valid, but its child assembler cannot decide H-052: it omits both
181-row `CertificateManifest` summaries, the global minima, the shrink-and-scaling
preconditions, the mutation map, `all_mutations_rejected` and `instrument_valid`.

This round repairs that result boundary in a fresh successor **before** it computes the
remaining eleven directions.
It changes no mathematical input and no criterion.

## Two Ancestries, Neither Substitutable

The successor records exp-056 as its **immediate parent checkpoint** and exp-052 as its
**carried-chain genesis**, in two separate binding blocks that each carry their own
literal role. One cannot stand in for the other.

| Binding | Immediate parent | Carried-chain genesis |
| --- | --- | --- |
| Role | `immediate-parent-checkpoint` | `carried-chain-genesis` |
| Experiment | exp-056 | exp-052 |
| Checkpoint SHA-256 | `0d39a7e7…` | `db5c1569…` |
| Progress SHA-256 | `0875f31f…` | `08e301b0…` |
| Binding hash | `18ec64b4…` | `2446fa39…` |
| Last row hash | `8947b38e…` at ordinal 169 | `9badcc57…` at ordinal 32 |
| Rows | 170 | 33 |
| Marker | ordinal 170, `independent_started` | ordinal 33, `independent_started` |

The two are cross-checked against each other rather than merely verified side by side.
Row 0’s `previous_row_hash` must equal the genesis binding hash, which is what makes
exp-052 the genesis rather than just an ancestor; row 32’s hash must equal the genesis
last row hash; the parent’s first 33 rows must reproduce the genesis rows exactly; and
the genesis must be a *proper* prefix.
A mismatch in any of them refuses the run before a single direction is evaluated.

Verification of the immediate parent is read-only.
It never constructs a writable store over the frozen paths, so no code path in it can
publish, truncate or resume the retained artifact.
It also requires exp-056’s declared result path to still be absent.

## Ordinal 170 Is Recomputed, Not Promoted

Exp-056’s marker sits at ordinal 170 in stage `independent_started`. A progress marker
carries no payload, so nothing about that interrupted calculation is retained and
nothing about it may be inherited.
The successor recomputes ordinal 170 from both accumulators, and `append_pair` refuses
any ordinal below the first new one.

## Fresh Paths

The result, checkpoint and progress paths share the `exp-059` slug and were absent at
preregistration:

- `campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.json`
- `campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.checkpoint.json`
- `campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.progress.json`

The successor binds `campaign/series/series-000-smoke-and-calibration/results/` as its
only writable output root and refuses every lexical or resolved-path escape, every path
carrying the `exp-052` or `exp-056` slug, and every path resolving inside
`cases/n17_weighted_certificate`, `cases/n17_weighted_certificate_resume` or
`cases/n17_weighted_certificate_child`.

BC-147 found that the exp-056 child driver’s own forbidden set named only `exp-052` and
the resume package, so it would have accepted an exp-056 output path.
The successor closes that gap by name, and a refusal test pins it.

## Two Terminal Schemas

Exactly two shapes may be published, and the assembler routes to one of them or refuses.

**Complete agreement** requires both 181-row `CertificateManifest` summaries — atom and
direction hashes, total weight, every one of the 181 row minima, and the global minimum
— plus the explicit `global_minimum` comparison and `exact_manifest_agreement`. The
validator rebuilds the entire 181-link hash chain from the two summaries alone, anchored
at the genesis binding hash, and requires it to reproduce the emitted chain spine, the
carried boundary `8947b38e…` at ordinal 169, and the last row hash.
An altered manifest therefore cannot survive: it breaks the chain that must still
terminate on exp-056’s verified boundary.

**Early disagreement** requires the verified contiguous prefix through the discrepant
pair, the discrepant pair’s exact payload with both manifests and its named differing
fields, the first-disagreement decision, and six **explicit absences**, each with a
reason: the suffix rows, both full certificate manifests, the row minima, the global
minimum and manifest-level agreement.
Declaring an absence while the field is present is refused, and so is carrying either
full summary.

Both schemas carry the shrink-and-scaling preconditions, every frozen mutation result,
`all_mutations_rejected` and `instrument_valid`. The decision is **derived** from those
fields rather than asserted beside them: the assembler builds the record without the six
decision-bearing fields, canonicalizes it, and only then derives each one from what was
emitted. The validator re-derives all six from the record alone and refuses on any
mismatch.

## Instrument Hashes

Recorded at registration, before the process was launched:

| Artifact | SHA-256 |
| --- | --- |
| `packing/cases/n17_weighted_certificate_successor/run.py` | `ab4dd8fe66b15e8f7c9837c4a3fede7234f702892addaf818bbacff1a763a553` |
| `packing/cases/n17_weighted_certificate_successor/__init__.py` | `03e0569fdb03e5df8f5a35cdb050d519c77ccfe240922c604260a9be1d9280c3` |
| `packing/tests/test_n17_weighted_certificate_successor.py` | `dbe1032fc95149e72f33666ecb587dcca55c8ab1279ae1c388850f16d68e9d9b` |
| Unchanged `packing/cases/n17_weighted_certificate_resume/run.py` | `3e5284fd56fd33f7b767954164128e9d43f5efad09eae4666035c3ef32c63f54` |
| Unchanged `packing/cases/n17_weighted_certificate_child/run.py` | `f45227508b28f37759df836db08dbad2031d600ef2b1ac087b73f8322b156b05` |
| Frozen package manifest | `309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54` |
| Successor binding hash | `f7c93f057a4b82910fcf9b1906fb0c70b0f3ba71e8050c76771651b3a1de34fc` |
| Self-test guard inventory | `0109332aaa375e1808457ab51be4c1792c5e3f973a6905e28ccdd063cb270013` |
| Self-test stdout, normal and optimized | `875722ceea9ce17dc7c4fd1a109f3a06b4b11d5803effa1cd284f2f9d045888c` |

One hundred and fifteen named guards pass with zero skips over synthetic directions
only, and the normal and optimized receipts are byte-identical.
Boundary observation uses
`./.venv/bin/python3 -m cases.n17_weighted_certificate_successor.run --status campaign/series/series-000-smoke-and-calibration/results/exp-059-h-052-n17-fresh-successor-completion.checkpoint.json`,
which reports the row count, both ancestry ids, the first new ordinal, the last row hash
and the agreement state without loading the retained fixture.

## Pre-Writer Confirmations

Two checks were run against the real retained data before the lease, and both are
reproducible:

1. Recomputing retained ordinal 169 from scratch on this host, through the successor’s
   own accumulators, reproduced the retained row hash
   `8947b38e0351048c3a67d914f2b8449185686d920913f5a2404898bdeca4c0b6` exactly.
2. Feeding the 170 retained source and independent manifests to the same chain-rebuild
   the complete-agreement validator uses, anchored at the exp-052 genesis binding hash,
   reproduced **every one of the 170 retained row hashes**, terminating on that same
   boundary.

The second is the stronger of the two: the mechanism that will decide agreement is
already known to agree with the frozen chain on real data, not only on synthetic
directions.

## Terminal Outcome

The writer ran once, inside its declared lease, from 2026-09-03T08:59:33Z to
2026-09-03T09:32:44Z — 1991 seconds against a 3600-second lease and a 2100-second
estimate. It recomputed ordinal 170 and continued to ordinal 180, appending eleven new
rows to the 170 carried ones.

|  |  |
| --- | --- |
| Terminal schema | `complete-agreement` |
| Decision | `accepted`, derived from the emitted evidence |
| `instrument_valid` | true |
| Rows | 181, all agreeing; `first_disagreement_ordinal` null |
| Result SHA-256 | `438dfc1ffc3f5ac2c8b83bc03014aa52e616da95b4a3b276f22326d36dee2d0a` |
| Checkpoint SHA-256 | `bb45ed2a1bd01b26ec4af3a137f5f51ce6a9ad1f8ccc744b76db936e62d1d28c` |
| Last row hash | `60e58a70c49fe6be879230c6305e59695364016ecdf1ba5ac3a305c12f5cb9a6` |
| Carried boundary | `8947b38e…` at ordinal 169 |

Both 181-row summaries are byte-identical.
Atom count 168, atom hash `37d35da0…`, direction count 181, direction hash `cc789e1a…`,
total weight `203/12`. Every one of the 181 row minima is exactly `1/1`, so the global
minimum is `1/1` — the frozen expectation `576/576`. All twelve certificate invariants,
all five mutation rejections, the precondition conjunction and the shrink-and-scaling
conjunction hold, and the progress marker was removed at the final reconciliation.

The published result was then re-validated from its bytes on disk by a separate process:
the file is exactly canonical, and `validate_result` re-derived the entire admission
boundary, rebuilding all 181 hash-chain links from the two summaries alone.
The four frozen ancestor digests are unchanged, the frozen package still computes to
`309ec241…`, and neither exp-052 nor exp-056 ever acquired a result file.

## Named Instrument Limitation

The successor’s CLI has no path that assembles a terminal schema from an existing
checkpoint.
Schema (b) is built, validated and covered by ten named guards plus a focused
control, but on a disagreement the driver raises before `run_target` reaches its
assembly call, so that invocation would retain the discrepant row and publish nothing;
schema (b) would need a later assembly step reading the retained checkpoint.
This is a wiring omission in the command-line layer, not a defect in the assembler.

It did not fire on this round, which agreed on every cell.
It is recorded because the all-agree outcome is exactly the one in which such an
omission is least likely to be noticed and most likely to mislead a later reader about
what the instrument can do.

## Claim Boundary

This round can produce all 181 exact pairs or the first exact disagreement.
Agreement alone moves no bound: it establishes implementation agreement for one fixed
certificate, and it is neither an independent proof method, nor adoption of the retained
`4.5058` as a reviewed lower bound, nor any cross-`n` or LP-generalization claim.
A disagreement rejects the agreement claim only, at H-052’s registered scope, and leaves
the mathematical lower bound for independent adjudication.
The separate adoption gate remains untouched either way.

## Stopped-By Rules

The process stops, retains its checkpoint and records why when any of these holds:

1. **Boundary stop.** The fixed 2026-09-03T09:58:00Z lease boundary arrives, whatever
   the row count.
2. **Disagreement.** A direction’s two manifests differ exactly; the row is kept and the
   process stops.
3. **Drift.** A frozen input, ancestry hash, package manifest or chain link fails
   verification, in which case nothing is written at all.

A time-limited partial chain is process evidence, not a negative result, and
`assemble_result` refuses to publish one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
