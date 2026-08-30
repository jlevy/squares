---
title: agenda-007 — twelve steered hours in four blocks, process first, each block a merged PR
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-007
  title: Twelve steered hours in four blocks, process first, each block a merged PR
  updated: '2026-08-30'
  status: completed
  objective: >-
    Spend twelve hours in four blocks of about three, in an order chosen so the blocks
    that make every later block cheaper run first. Blocks 1 and 3 are the loop itself:
    the pre-push tier is measured at 16.05s on this container and one step is all of it,
    so every checkpoint in this agenda pays that cost until it is fixed. Block 2 is the
    reader-facing tier, which the last run moved past without moving. Block 4 is the
    science, and it is deliberately last rather than deprioritised: it is the block whose
    question is open-ended, so it is the one that can absorb overrun without a
    commitment being cut short. This agenda owns the clock, the ordering, and what each
    block must leave behind. It does not own a scientific exit; agenda-005 BC-046 owns
    block 4's, and the gate-validation-speed spec owns the phase contracts for blocks 1
    and 3.
  items:
  - id: BC-077
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11, 29]
    state: complete
    priority: 0
    question: >-
      Can the pre-push record tier be made effectively instant without any verdict
      changing, and can the absence of a changed verdict be proved rather than asserted?
    hypotheses: []
    budget: >-
      about 150 minutes of work from the start of the run, in slices of 15 to 30 minutes
      each with a named output, plus a 30-minute checkpoint reserve
    entry: >-
      Phase 1 of plan-2026-08-29-gate-validation-speed is specified, measured and
      unstarted; its three beads are cut; and `--records` is measured on this container
      today at `16.05s` wall, of which `soft-schema validation` is `16.05s` on the
      critical path and every other step together is under four seconds
    exit: >-
      `jsonschema-rs` pinned and swapped with `e.path` renamed at the one call site; the
      exact grid replay moved out of the schema step into the step that owns exact
      geometry; `benchmarks/bench_schema_validation.py` repeatable per OR-1; a
      differential test standing in the suite that fails if the two validators ever
      disagree on the corpus or on generated mutations of it; the measured before and
      after recorded in D-370; and `--records` re-measured on the same container.
    artifacts:
    - docs/project/specs/active/plan-2026-08-29-gate-validation-speed.md
    - packing/benchmarks/bench_schema_validation.py
    bead: think-64bw
    depends_on: []
    workflows: [efficiency-loop]
    next_evidence: >-
      The differential verdict is the load-bearing measurement, not the timing. A
      validator two orders of magnitude faster that accepts one artifact the old one
      rejected is a soundness regression buying six seconds, and the corpus is 339
      artifacts against 23 schemas, so agreement on it is checkable rather than arguable.
      (Written before the block as "559 times faster" over "314 documents", from the
      spec's scratch-script figures; both are corrected above from the landed
      measurement.)
    note: >-
      Runs first, ahead of the documentation pass that agenda-006 puts before BC-075,
      because the spec itself says phase 1 can land before that block opens and because
      every checkpoint in this agenda pays the tier's cost until it is fixed. The
      dependency agenda-006 records is on the tier *contract*, which is block 3, and that
      ordering is preserved.

      Discharges the phase-1 half of agenda-006 BC-075, on its three cut beads:
      `think-64bw` swaps the validator, `think-p9of` moves the geometry, `think-2bk2`
      builds the benchmark and the differential test.

      Under-running is the failure mode that matters here, as it is in block 3. A tier
      that is merely slow is a disappointment; a validator that silently stops checking a
      keyword is a defect that makes every later gate run a lie, and it would be invisible
      in the timings that motivated the change.

      **Closed 2026-08-30.** The pre-push tier is `4.48s`, from `16.05s`, on the same
      container: `soft-schema validation` fell from `15.71s` to `4.48s` and the exact grid
      replay moved to `exact verification`, where it costs `3.6s` in a tier that does not
      contain it. 369 differential assertions stand in the suite and all pass.

      Two of the spec's claims did not survive being made reproducible, and both are
      corrected in `D-370` and in the spec rather than quietly dropped. The speedup is
      `83x` to `137x` across five runs over the real 339-artifact corpus, not the `559x` a
      scratch script reported over a 314-document subset -- a range rather than a point,
      because the Rust side is small enough that container noise moves it by half. And `error.message` is *not* byte-identical between the
      two libraries: they quote differently and systematically, so a consumer parsing that
      text would have broken silently. Nothing here parses it, which is the only reason the
      swap was safe rather than lucky.

      One scope decision worth naming: nine other modules still build a `jsonschema`
      validator, and none is on the pre-push tier. `think-gj9c` carries them, with the
      instruction to measure before swapping.
  - id: BC-078
    purpose: tool_validation
    owner_focus: process
    instances: [11, 29]
    state: complete
    priority: 0
    question: >-
      Do the reader-facing documents still describe the project the record describes?
    hypotheses: []
    budget: >-
      about 150 minutes of work, in slices of 15 to 30 minutes each covering one
      checklist section, plus a 30-minute checkpoint reserve
    entry: >-
      Block 1 has landed, so the checklist's own regeneration and check steps are cheap
      to run repeatedly; and the previous run closed eleven commitments that `README.md`
      and `TUTORIAL.md` never absorbed, because `check_synopsis` binds only the synopsis
    exit: >-
      The checklist in `campaign/documentation-pass.md` run over every root document and
      over the `n = 11` research report, with each drift either fixed or filed as a defect
      and no third option; the generated figures read against the sentences that introduce
      them, not merely regenerated clean; generated views regenerated; and an explicit
      statement of what was checked and what was left.
    artifacts:
    - packing/campaign/documentation-pass.md
    bead: think-eb29
    depends_on: [BC-077]
    workflows: [documentation-pass]
    next_evidence: >-
      W8 reconciles and does not author, so the measurable output is a disposition per
      checklist item rather than a word count. The sentences most at risk are the claim
      boundaries, because they are the ones that read as clutter: `reported` is not
      `verified`, `verified` is not the optimum, and a bound on a retained witness is not
      a bound on `s(n)`. D-367 is what that failure looks like, and it happened in the run
      that is asking for this pass.
    note: >-
      Discharges agenda-006 BC-074, unchanged in scope, on the same bead.

      A pass that quietly picks the more readable side of a disagreement is how a wrong
      claim becomes the tidy one, so a conflict the artifacts cannot settle leaves a
      defect rather than an edit.

      **Closed 2026-08-30. What was checked, and what was left.**

      Checked and corrected: `SYNOPSIS.md`, `TUTORIAL.md` and `README.md` all described the
      numeric-to-symbolic promotion route as unbuilt after every component of it had
      landed, and the synopsis paragraph contradicted itself two sentences later. That is
      `D-372`. `conventions.md`'s cadence table and `OR-3` both claimed seventy seconds for
      the pre-push tier that `BC-077` had taken to four; both restated from measurement,
      and `AGENTS.md` regenerated. The `n = 11` research report received a dated addendum
      for the three results this project established at that size after 2026-08-25 -- the
      exact route closing with a difference of exactly zero, the contact Jacobian at full
      rank with the earlier shortfall identified as `D-361`, and a cell certified with no
      float solver in the chain -- appended rather than rewritten, because it is a dated
      record.

      Checked and found current: `README.md`'s headline numbers, against the artifacts
      rather than against each other -- 27 papers, 13 web sources, 35 side lengths proved
      optimal, the `n = 11` gap of `0.088`, and `s(29) <= 5.93388579981302587863645209`.
      All three `TUTORIAL.md` witness commands run as printed. All six figure generators
      pass their own `--check`, and the atlas caption's badge counts reconcile with the
      frontier. `development.md`'s commands and flags all resolve.

      **The one that nearly went wrong is worth naming.** The first draft of the synopsis
      fix said what remained was "a decision, not a component", which was itself an
      overstatement in the opposite direction: the public `packing-witness promote
      --strategy interval-existence` still raises `checker-not-built`, and the `n = 29`
      certificate came from a case-specific driver. It was caught by checking which entry
      point actually produced the certificate rather than by rereading the prose, which is
      the whole argument for the runbook's ordering.

      Left, deliberately: nothing binds `README.md` or `TUTORIAL.md` to the artifacts the
      way `check_synopsis` binds the synopsis, and `D-372` argues that no checker can,
      because it would have to decide what a sentence claims. The cadence table is restated
      from measurement but not re-derived; `BC-079` owns that.
  - id: BC-079
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5, 11]
    state: complete
    priority: 0
    question: >-
      Are the gate's tiers the right tiers, and is the coordinator running them at the
      right times?
    hypotheses: []
    budget: >-
      about 150 minutes of work, in slices of 15 to 30 minutes each with a named output,
      plus a 30-minute checkpoint reserve; the measurement half is cheap and the retiering
      is a contract change
    entry: >-
      Block 1 has removed the noise that made the tier argument unarguable — one step
      being most of the tier hid what every other step costs — and block 2 has left a
      current reader-facing tier for the contract change to land in
    exit: >-
      A tier structure argued from what each step can catch and how often it can catch it,
      carrying a control that proves the new routing cannot run fewer steps than a change
      can reach; D-366 decided without dropping a control; the cadence table in
      `conventions.md` restated from measurement rather than from the impression it
      recorded last time; and this session's own agent logs rolled up so the coordinator
      half of the argument rests on measured minutes.
    artifacts:
    - docs/project/specs/active/plan-2026-08-29-gate-validation-speed.md
    - conventions.md
    bead: think-av72
    depends_on: [BC-077, BC-078]
    workflows: [efficiency-loop, process-review]
    next_evidence: >-
      The first-principles question is whether a step earns its slot. A check that has
      never failed on an edit-loop change is ceremony there however good it is at a
      boundary, and a check that can only fail after a regeneration belongs where
      regenerations happen. `--only` already runs three targeted steps in about four
      seconds against the tier that contains them, so the mechanism exists and the routing
      does not.
    note: >-
      Discharges the phase-2 half of agenda-006 BC-075, on its own bead `think-av72`.

      The coordinator is the half with the larger measured waste, and it is the half a
      tier change cannot fix. OR-3 has since been written for the general form of it; what
      this block owes is the measurement that says which of its clauses the timings
      actually support, and whether any of them is better enforced by tooling than by a
      rule an agent has to remember.

      A rule an agent reads and a tier that makes the rule unnecessary are different
      fixes, and this block is where they are told apart.

      **Closed 2026-08-30.** The answer to "are these the right tiers" was no, and the
      reason is one number: `--fast` measured `499s` with `fast behavioral tests` 94% of
      it, so the tier that catches everything which actually breaks was priced at the cost
      of the step that never has. `--edit` is that tier without the broad suite, measured
      at `32.9s`. The ladder is now `--records` at `4s`, `--edit` at `33s`, `--fast` at
      `499s`, and the full gate, and CI still runs `--fast` and the full gate on every
      push, so the split moved feedback latency and not coverage.

      Under-running was the failure mode to design against, and it is answered by making
      exclusion opt-*out*: a new step joins `--edit` unless explicitly marked `broad`, so
      forgetting the marker makes the tier slower rather than blinder. Three tests hold
      it -- the tiers nest as sets, every step is reachable from the full run, and the set
      of broad steps is asserted rather than assumed.

      `D-366` is decided by the second repair it named, a per-step budget, with no control
      dropped or retargeted. The verification run then improved the argument by
      contradicting its premise: 142 controls took `736s`, inside the `900s` cap the step
      was said to exceed, against `1268s` measured five days earlier at 137 controls. A
      spread of `1.7x` straddling the cap means the step fails *intermittently*, which is
      indistinguishable from the outside from a control that stopped firing -- a better
      case for a declared budget than the one this block started with.

      The coordinator half is now measured rather than argued. This session's rollup is
      retained at `campaign/resource-usage/5cd11e53-....yaml`: `233.6s` in `.gate-running`
      polling loops across three calls plus `245.6s` in three more waiting on tests, about
      17% of the session, and two gate runs started against trees that then changed
      underneath them and had to be discarded. `OR-3` already said not to do that; what it
      lacked was the price. It also records `585.6s` across 63 one-off code invocations,
      which is `OR-1`'s target measured for the first time.

      One thing this block did *not* settle: whether a reachability-scoped selector is
      worth building on top of the new tiers. At `33s` for the edit loop the answer is
      probably no, and that is a measurement rather than a decision, so `think-d0q7` stays
      where `BC-062` left it.
  - id: BC-080
    purpose: measurement_validation
    owner_focus: correctness
    instances: [3, 4, 5]
    state: complete
    priority: 1
    question: >-
      What relation should the atlas count, given that a connected optimal set produces
      many endpoint keys and the current store splits it?
    hypotheses: [H-032]
    budget: >-
      about 150 minutes of work, in slices of 15 to 30 minutes, opening with two W3 slices
      and entering W6 only if a criterion is frozen first, plus a 30-minute checkpoint
      reserve
    entry: >-
      The exact `n = 3` and `n = 4` quotient models are available as known answers, the
      `n = 5` face, sheet, obstruction and polytope results are retained, and the three
      process blocks ahead of this one have left the checkpoint cost small enough that a
      research slice can afford to close properly
    exit: >-
      A declared identity relation with a criterion that the exact `n = 3` sliding family
      and the exact `n = 4` point both satisfy, or a typed statement of which property the
      candidate relation cannot decide.
    artifacts:
    - packing/campaign/explorations/X-005-identity-relation-and-its-controls.md
    - packing/devtools/check_identity_relation.py
    - packing/tests/test_identity_relation.py
    bead: think-0yo9
    depends_on: [BC-079]
    workflows: [insight-iteration, research-loop]
    next_evidence: >-
      `distinct_basins` counts endpoint keys, not connected terminal components. The exact
      `n = 3` side-2 optimum contains a sliding family of centres, so one connected set
      produces many keys and the store splits it. Until D-034 is resolved the discovery
      curve cannot plateau, the census cannot saturate, and the rarity premise is
      untestable rather than untested.
    note: >-
      Discharges agenda-005 BC-046, unchanged in scope, on the same bead.

      This is the named next scientific transition in `SYNOPSIS.md`: from specialized
      `n = 5` local geometry to a defensible component relation, and explicitly not to a
      larger raw census. A bigger census built on a relation that splits one component
      into many keys measures the splitting, not the landscape.

      Last by design rather than by rank. Its question is the open-ended one, so it is the
      only block whose overrun costs a schedule rather than a commitment, and the three
      ahead of it each have a definite exit that a clock can be held against.

      **Closed 2026-08-30, and the exit clause's second branch is the one that fired.**
      A relation is declared: two endpoints are the same terminal component when their
      contact certificates agree, or when the strata those certificates name lie in one
      closure. It is the only one of four candidates that survives all four proved answers
      in `exp-014` and `exp-015`, and the `n = 3` artifact retains exactly what it needs,
      `closure(G) = [C, G, M]`, so the merge is read from the record rather than assumed.

      **But the acceptance rule this cell inherited could not have established that**, and
      that is `D-373`. It named the two quotient controls, both of which have component
      count one, so a relation that merges everything passes them -- and `side alone` is
      exactly that relation and is known wrong from `D-034`'s `n = 5` pair. Three of four
      candidates survive the rule as written. The labelled controls, whose proved answers
      are `2` and `24`, are what separate them. A criterion validated only on cases whose
      answer is one is validated against a constant.

      The two controls also turn out to isolate independent failures rather than duplicate
      one test: `n = 4` is pure symmetry with no connectivity anywhere, `n = 3` is pure
      connectivity inside a single orbit. `distinct_basins` is wrong on both counts and the
      errors compose, so it is a strict upper bound on the component count and not an
      estimate of it.

      Deliberately not claimed: this is not a component counter. The relation survives four
      proved answers and has not been shown to decide the general case, and the closure
      data it needs exists at `n = 3` only because an exhaustive classification produced it.
      `D-034` stays outstanding. What this removes is the possibility of closing it against
      a rule a merge-everything relation would have passed.

      Two gaps left with owners: `think-byc6` retains per-sample keys for `exp-015`, without
      which the relation the atlas uses today cannot be scored on the control that would
      most directly test it; and the next bounded question is whether `n = 5` can be given a
      discriminating control at all, since until one exists any `n = 5` identity claim is
      being validated against a constant in exactly the way `D-373` describes.
---
# agenda-007 — Twelve Steered Hours in Four Blocks

**Date:** 2026-08-30

**Status:** Active. This is the current queue; `agenda-006` is its predecessor and
retains the record of the run that produced these commitments.

**Owns:** The clock, the ordering, and what each block must leave behind.

## The ordering, and why it is this one

The blocks are ordered by what makes the later blocks cheaper, not by importance.

**Blocks 1 and 3 are the loop itself.** The pre-push tier costs `16.05s` on this
container, and a single step — `soft-schema validation` — is the whole of it, with every
other record check together under four seconds.
Every checkpoint in this agenda pays that cost until it is fixed, and the four
checkpoints here are the point of the exercise.
Fixing it first is not tidying before the real work; it is the difference between a
checkpoint that is worth taking and one that gets skipped.

**Block 1 runs ahead of the documentation pass** that `agenda-006` schedules before
`BC-075`. That is a deliberate reordering and it is narrower than it looks: the
gate-validation-speed spec already says phase 1 can land before the block opens, and the
dependency `agenda-006` records is on the tier *contract*, which is block 3 and still
runs after the pass.

**Block 2 is the reader-facing tier.** The previous run closed eleven commitments.
`SYNOPSIS.md` carries their results because `check_synopsis` forces it to; `README.md`
and `TUTORIAL.md` do not, and nothing forces them.

**Block 4 is the science, and it is last.** Its question is the open-ended one, so it is
the block that can absorb overrun without a commitment being cut short.
The three ahead of it each have a definite exit a clock can be held against.

## Slice discipline

A block is 150 minutes of work plus a 30-minute checkpoint, and the work is spent in
slices of 15 to 30 minutes.
Thirty minutes is a ceiling and not a quota: a slice closes when its named output
exists, which is often sooner.

The rule exists because the failure it prevents is the one that actually happens.
An unbounded slice does not announce itself — it reads as progress right up to the point
where three hours have gone into a sub-problem nobody scheduled, and the block ends with
a deep answer to a question that was not the block’s. A slice with a named output fails
loudly instead: at the 30-minute mark either the output exists or it does not, and if it
does not, the next decision is made deliberately rather than drifted into.

So each slice is declared before it starts, with one named output and one check.
At its end the coordinator does one of three things, and never a fourth:

- **Close it.** The output exists; record it and take the next slice.
- **Renew it once.** The output is close and the reason it is not done is known and
  bounded. Say the new fact that justifies another clock, per the phase-boundary rule.
- **Cut it.** Record what was reached, file what was not as a bead or a defect, and move
  to the next slice. A cut slice that leaves a bead is a result; a slice that silently
  runs long is not.

Replanning happens at slice boundaries only, and only forward.
Mid-slice replanning is how the ceiling stops being a ceiling.

## What a block must leave behind

Every block closes the same way, and a block that cannot is a block that stopped early
rather than finished:

- Its declared exit met, or a typed statement of what it reached instead.
- A pull request, reviewed and merged, so the next block starts from a green `main`.
- `packing-validate --records` before the push, per `OR-3`, with the slower tiers
  running concurrently rather than after.
- Its agenda cell moved off `ready`, and the `agenda-006` or `agenda-005` commitment it
  discharges moved with it.
- An `OR-7` documentation-guidelines pass, if the block produced a new document or a
  substantial rewrite.

## What this agenda does not own

Any scientific exit.
`BC-046` in [agenda-005](agenda-005-symbolic-promotion-and-identity.md) owns block 4’s
criterion, and
[the gate-validation-speed spec](../../../docs/project/specs/active/plan-2026-08-29-gate-validation-speed.md)
owns the phase contracts for blocks 1 and 3. This agenda owns when work starts, when it
must stop, and what it must leave behind.

Nor does it own a promotion.
Under-running the gate is the failure mode both efficiency blocks are written against: a
tier that is merely slow is a disappointment, and a tier that skips a step a change can
reach is a soundness defect.
Any retiering carries a control proving it cannot.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
