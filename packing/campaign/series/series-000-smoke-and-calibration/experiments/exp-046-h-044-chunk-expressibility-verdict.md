---
title: exp-046 — the H-044 chunk-expressibility verdict at n <= 30
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-046
  series: series-000
  title: Score H-044's registered criterion against the frozen partition atlas
  date: '2026-08-31'
  hypotheses:
  - H-044
  tier: exploratory
  subject:
    label: chunk-expressibility of the standing records at n <= 30 under the frozen contract
    engine: devtools.score_h044 over chunk-partitions.json (census_known_best_chunks)
    assurance: numerically-checked
    method: numerical-f64
    precision: {binary_bits: 53, rounding: nearest}
    tolerance: >-
      the frozen contract's bands: exact contact residual 1e-9, near residual 1e-3,
      fitted angle 1e-6 radians; the scoring itself is integer counting over the
      stored atlas
    host_system: Linux x86_64, Claude Code remote container
    selftest_passed: false
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: >-
      The scorer re-derives every record's establishment from the stored per-F options
      (partitioned status, chunk count within six, free squares within two, off-frame
      chunks within two) and refuses to score if any derived row disagrees with the
      atlas's stored status; the recorded output must then replay byte-identically
      from the atlas under --check. Both controls passed on this run.
    candidate: >-
      The registered n <= 30 slice of the frozen partition atlas, scored per band
      against H-044's criterion (fraction established at K <= 6 with at most two
      free squares, threshold 4/5) under both readings the registered text
      supports: all 30 atlas records at n <= 30 (the claim's "standing-record
      poses ... with public full geometry"), and the 10 non-grid records, which
      are exactly H-044's own sweep points at n <= 30. Choosing between the
      readings is a preregistration-style decision held for the owner; the
      outcome does not depend on it.
    runs_per_condition: 1
    interleaved: false
    operator: claude-code-overnight-run
    entry_point: devtools/score_h044.py
    command: >-
      uv run --frozen python -m devtools.score_h044 --record
      campaign/series/series-000-smoke-and-calibration/results/exp-046-h-044-chunk-expressibility-verdict.json
      && uv run --frozen python -m devtools.score_h044 --check
      campaign/series/series-000-smoke-and-calibration/results/exp-046-h-044-chunk-expressibility-verdict.json
    budget: >-
      BC-100's 90-minute W3 block inside session-055; the scoring slice stopped well
      inside its 45-minute phase budget because the frozen atlas already carried the
      per-record evaluation and only the registered slice and its typed reasons were
      missing.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-046-h-044-chunk-expressibility-verdict.json
  effort:
    timebox: one 45-minute phase of session-055 (block 4 of the agenda-010 overnight run)
    wall_seconds: 1.1
    agent_minutes: 25
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Do at least 4/5 of the frozen-corpus records at n <= 30 admit a K <= 6 chunk
      decomposition with at most two free squares under the declared bands?
    role: outcome
    outcome: criterion_missed
  - shape: determination
    question: >-
      Does the scorer's independent re-derivation of every establishment agree with
      the atlas's stored statuses, and does the recorded score replay byte-identically
      from the atlas?
    role: guard
    outcome: criterion_met
  verdict:
    decision: unresolved
    needs_review: false
    primary_criterion: >-
      report criterion_met only when, per adjacency band, at least 4/5 of the atlas
      records at n <= 30 are established under the frozen contract (K <= 6, at most
      two free squares, at most two off-frame chunks, exact residual 1e-9 and near
      residual 1e-3 bands); report criterion_missed otherwise; hold the round
      unresolved with needs_review whenever the fraction lands near the threshold,
      per BC-100's registered exit.
    reason: >-
      The criterion is missed under both denominator readings the registered text
      supports, identically in the exact and near bands: 23/30 = 0.7667 over all
      atlas records at n <= 30, and 3/10 = 0.30 over the non-grid records that
      are H-044's own sweep points -- so the outcome is robust to the one
      preregistration-style ambiguity this round refuses to decide (which
      denominator the claim meant). All seven misses (n = 5, 11, 17, 18, 19, 28,
      29, every non-grid record but three) are typed no-partition results, fully
      determinate -- no n <= 30 record is search-capped or outside-budget. The
      decisive mechanism, verified against the stored components: the grammar's
      adjacency is the integer lattice step, and the tilted stratum's flush
      groups are tangentially slid -- Trump's n = 11 five-square group has all
      contact residuals exactly zero in the normal direction yet no integer
      lattice offsets, so it enters the universe as five singletons (the same
      mechanism at n = 17), and H-044's own worked decomposition of n = 11 needs
      three free squares against its own registered two. At n = 18, 19, 28, 29
      real shared-angle candidates form (sixteen to thirty-six) and no admissible
      set covers the squares within two free. Two frozen-contract decisions frame
      any review: singleton chunks are inadmissible (n = 5's four mutually
      non-adjacent corner squares can never group; admitting singletons provably
      flips n = 5 and lands the broad reading on 24/30 = 0.80 exactly, while
      moving the sweep reading only to 4/10), and sliding contact assemblies are
      outside the universe (a contact-relaxed grammar upper-bounds the broad
      reading at 26/30 = 0.8667, shape and off-frame budgets unchecked). Whether
      the remaining misses move under either relaxation needs one preregistered
      re-run of the census with the relaxed universe -- a follow-on, not
      tonight's decision. Either way the structural conclusion X-010 needs
      stands: the bar/L/rectangle lattice grammar as frozen expresses the grid
      stratum completely and the tilted stratum not at all, so a stage-1 pipeline
      built on it is a restricted-class instrument, exactly as block 2's
      repricing priced it. Tier is exploratory, not confirmatory, by H-044's own review
      amendment of 2026-08-26: the n = 1..100 corpus was inspected while the
      detector contract was being repaired, so it is calibration-only, and a
      confirmatory disposition needs a successor round on an unseen corpus frozen
      after the instrument and grammar -- this round supplies the instrument and
      the calibration number that successor will be judged against. Review
      resolution 2026-08-31 (session-060, BC-106): the hold is lifted with the
      decision standing at unresolved -- the criterion miss is determinate,
      byte-replayable, and robust to the one denominator ambiguity, so no
      near-threshold judgement is pending; and the round cannot dispose H-044 in
      either direction, because the ledger derives a hypothesis-level refutation
      from any rejected round regardless of tier while the registered amendment
      types this corpus calibration-only and the hypothesis undisposed. Nothing
      about this round awaits review.
    reopen_when: >-
      A successor round scores a corpus frozen after the instrument and grammar
      (the amendment's confirmatory path), or a preregistered re-run measures the
      two typed relaxations this round priced -- singleton admission (provably
      moves the broad reading to 24/30 exactly) and contact-relaxed sliding
      assemblies (upper-bounds it at 26/30).
---
# exp-046 — The H-044 Chunk-Expressibility Verdict at n <= 30

H-044 is the coverage prior for the whole stratified-enumeration design: a grammar that
cannot express the records it is meant to rediscover has no budget claim.
X-003 registered it refutation-first and search-free for exactly this moment — the
verdict lands before any enumerator is built, from retained geometry alone.

## What Was Measured

The frozen partition atlas already evaluated every standing record under the registered
contract (the census runs the deterministic exact-cover solver per record at every
free-square count; its schema pins `claim_status: calibration-no-verdict` by `const`, so
the atlas itself can never quietly become evidence).
This round adds the registered slice and nothing else: `devtools/score_h044.py`
re-derives each record’s establishment from the stored options, applies the n <= 30 cut
and the 4/5 threshold per band, types every miss, and emits a record that must replay
byte-identically from the atlas.

## The Number and What Sits Behind It

**Criterion missed under both readings of the registered denominator: 23/30 = 0.7667
over all records at n ≤ 30, and 3/10 = 0.30 over the non-grid records that are H-044’s
own sweep points — identically in both bands.** The registered text supports either
reading, and the outcome does not depend on it — which is why the review resolution
below needed no decision between them.
The twenty exact-grid records all establish (the grid is one rectangle chunk); three
non-grid records establish; the seven misses are the tilted stratum, every search
exhausting within seventeen states — a candidate-universe boundary, not a search-budget
one, and no `n ≤ 30` record is search-capped, so the slice is fully determinate under
the frozen cap.

The decisive mechanism is sharper than “tilted squares share no angle.”
Trump’s `n = 11` five-square group is flush — every internal contact residual is exactly
zero in the normal direction — and shares one fitted angle, but it is *tangentially
slid*: its members sit at no integer lattice offsets, and the grammar’s adjacency is the
lattice step.
So the group enters the universe as five singletons, and `n = 11` dies with
three candidates; `n = 17` misses by the same mechanism.
H-044’s own worked decomposition of `n = 11` — corner square, mirrored square, offset
square, an L of three, a five-square group — leaves **three** squares ungrouped, against
its own registered budget of two: the hypothesis’s headline instance is excluded by its
own criterion as written.
At `n = 18`, `19`, `28`, `29` the universe is real (sixteen to thirty-six candidates —
shared-angle diagonal strips do form chunks) and the failure is coverage: no admissible
chunk set covers the full square set within two free squares.

Two frozen-contract decisions are what a review would weigh, and both were made at
registration rather than tonight:

- **Singleton chunks are inadmissible** (candidate generation requires size >= 2). This
  alone decides `n = 5`: its four corner squares share the frame angle but touch
  nothing, so they can never group, and four ungrouped squares exceed the two-free
  budget regardless of the tilted center square.
  Admitting singletons provably flips `n = 5` (five singleton chunks, zero free) and
  lands the broad reading on 24/30 = 0.80 exactly, while moving the sweep reading only
  to 4/10 — which is one reason the round was initially held for review rather than
  closed.
- **Sliding contact assemblies and angle-class splits are outside the universe**, so
  every miss is typed as a limit of the grammar, never as a refutation of the record’s
  expressibility in some richer grammar.
  A contact-relaxed grammar upper-bounds the broad reading at 26/30 = 0.8667 — an upper
  bound only, with shape and off-frame budgets unchecked there.

Whether the other misses move under singleton admission or contact relaxation is not
decidable from the stored options — either relaxation changes the exact-cover instance —
so the honest answer is one preregistered re-run of the census with the relaxed
universe, and that follow-on is deliberately left outside this round.

## What This Buys the Program

Whatever the review decides about the threshold, the structural conclusion X-010’s Lane
B needs is now evidence-based rather than assumed: **the bar/L/rectangle grammar as
frozen expresses the grid stratum completely and the tilted stratum not at all.** A
stage-1 pipeline over this grammar is a restricted-class instrument — exactly the
honesty boundary block 2’s repricing (BC-095) priced, now confirmed from the geometry
side before any enumerator spent anything.
The typed remainder (what grammar extension would express the tilted stratum: sliding
assemblies, per-square angle classes, or nothing short of free-form) is the follow-on
question the registration deliberately left outside this round’s scope.

This round is exploratory by H-044’s own review amendment (2026-08-26): the n = 1..100
corpus was inspected during detector-contract repair and is calibration-only, so no
round on it can confirm H-044 — the registered confirmatory path is a successor on an
unseen corpus frozen after the instrument.
What this round contributes is that instrument, ready and replayed, and the calibration
number the successor is judged against.

Per the run’s unattended rules the verdict was recorded `unresolved` with `needs_review`
on the night of the round; the resolution below completes it.

## Review Resolution (2026-08-31)

Resolved in [session-060](../../../agent-sessions/session-060-verification-review.md)
under `BC-106`, applying the repository’s own rubric rather than deferring:

- **The measurement stands as verified computation.** Every establishment is re-derived
  from the stored options, every miss is a typed no-partition result under the frozen
  contract with no search cap reached, and the score replays byte-identically from the
  atlas (`--check`). Nothing in the number is a judgement call.
- **The near-threshold hold clause does not bind.** The registered criterion held the
  round for review “whenever the fraction lands near the threshold”; the miss is robust
  to the one preregistration ambiguity (23/30 and 3/10 under the two denominator
  readings, identically in both bands), so there is no marginal reading left to
  adjudicate.
- **The round cannot dispose H-044, by registration.** The 2026-08-26 amendment types
  this corpus calibration-only and the hypothesis undisposed; and the ledger derives a
  hypothesis-level refutation from any `rejected` round regardless of tier, so recording
  `rejected` here would report a disposition the registered contract forbids.
  The decision therefore stands `unresolved` with the review hold cleared, and
  `reopen_when` names the confirmatory successor and the two priced relaxations.

No `verified_*` field is implicated: the round’s claim is about grammar expressibility
of serialized geometry under tolerances, never a frontier bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
