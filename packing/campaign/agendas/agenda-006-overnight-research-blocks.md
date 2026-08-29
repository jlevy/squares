---
title: agenda-006 — four bounded overnight blocks, each ending in a checkpoint that holds
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-006
  title: Four bounded overnight blocks, each ending in a checkpoint that holds
  updated: '2026-08-29'
  status: active
  objective: >-
    Schedule one unattended overnight run across three independent agenda-005 lanes, in
    blocks small enough that an interruption costs one block rather than the night. This
    agenda owns the clock, the ordering, and what a block must leave behind; it does not
    own a single scientific exit. Those stay with the agenda-005 commitments each block
    advances, so a block that stops early narrows the schedule and never a claim. The
    ordering is deliberate: the interval-certification lane runs first because it is the
    only one that can move a verified bound, and because session-035 left it declared and
    unstarted.
  items:
  - id: BC-052
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 10, 11, 29]
    state: complete
    priority: 0
    question: >-
      Can the interval-certification bridge be built as far as a Krawczyk operator and an
      interval separating-axis test that both refuse correctly, inside one 150-minute
      block, without any claim being made about n = 29?
    hypotheses: []
    budget: >-
      150 minutes from 2026-08-29T03:10Z, in slices of at most 30; a 20-minute
      finalization reserve inside that total
    entry: >-
      BC-047 is complete, so a refined n = 29 pose to 1000 declared digits already exists;
      the witness contract already names `interval-certified`; and PR 60 is merged so the
      block starts from a green main
    exit: >-
      Phases 1 and 2 of plan-2026-08-28-interval-certification are implemented with every
      control that spec names firing, or a typed statement of which conditioning stopped
      them. Either way the block ends committed, pushed, and carried by an open PR whose
      fast gate is green.
    artifacts:
    - src/sqpack/promote/interval.py
    - src/sqpack/promote/krawczyk.py
    - src/sqpack/promote/enclose.py
    - src/sqpack/promote/interval_verify.py
    - tests/test_promote_interval.py
    - tests/test_promote_krawczyk.py
    bead: think-pr0m
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      Session-035 closed with this as its declared next action, naming BC-045 and
      `think-75ll` and the spec's phases 1 and 2. Nothing has been built against it since,
      so the block starts exactly where that handoff points.
    note: >-
      A scheduling container. The scientific exit is owned by BC-045 in agenda-005 and by
      plan-2026-08-28-interval-certification; this item owns only the clock and the
      checkpoint. The uniqueness half of the Krawczyk verdict is the load-bearing part: a
      box holding two roots does not identify which pose was certified, so interior
      containment is checked rather than containment.
      Closed in session-036, inside the block clock. Phases 1 and 2 are built and every
      stage that can refuse was watched refusing; negative controls rise from 86 to 90 and
      the fast gate is green at 4m03s. The calibration against `sqpack.field` found two
      soundness bugs that inspection had not, both flattering: certificate endpoints were
      serialized by rounding to nearest, which lifted both ends of a box above the root it
      enclosed, and the operator reported its final iteration rather than the verdict it had
      proved, discarding a uniqueness result obtained two iterations earlier. The block's
      load-bearing result is a refusal: four unit squares packed exactly into a side-2
      container return six undecided pairs and zero separated, which is correct and is what
      a tolerance-based checker gets wrong. Nothing here certifies n = 29 and
      `verified_upper_bound` is untouched.
  - id: BC-053
    purpose: tool_validation
    owner_focus: correctness
    instances: [5, 10, 11, 29]
    state: complete
    priority: 0
    question: >-
      Does the checker agree with the exact route where the answer is already known, and
      what does it return at n = 29 — a certificate, or a typed refusal naming its cause?
    hypotheses: []
    budget: >-
      180 minutes from about 2026-08-29T05:40Z, in slices of at most 30; a 20-minute
      finalization reserve inside that total
    entry: >-
      BC-052 left a Krawczyk operator and an interval separating-axis test whose controls
      fire; origin/main has been merged at the start of this block
    exit: >-
      Phases 3 and 4 of the same spec: n = 5 and n = 10 certified in agreement with the
      exact route, n = 11 certified against Trump's published polynomial, a demonstrated
      refusal on a plausible-but-infeasible pose, and then whatever n = 29 actually
      returns. Any n = 29 success is recorded `unresolved` with `needs_review: true`; this
      runner may not accept it.
    artifacts:
    - src/sqpack/promote/relax.py
    - cases/kingbird29/layout.py
    - cases/kingbird29/certify_interval.py
    - tests/test_promote_relax.py
    - campaign/series/series-000-smoke-and-calibration/results/bc-053-n29-interval-certificate.json
    bead: think-9ida
    depends_on: [BC-052]
    workflows: [pipeline-improvement]
    next_evidence: >-
      Calibration is the test here and it is stronger than for the exact route, because
      n = 5, n = 10 and n = 11 have answers this implementation cannot influence. Agreeing
      with the exact route on valid input proves nothing about discrimination, which is
      why the refusal demonstration is part of the exit rather than a nicety.
    note: >-
      Advances BC-045. `verified_upper_bound` does not move in this block and no document
      may describe the reported n = 29 value as certified until a human accepts it. The
      bound move is a reviewed change through the evidence contract, never a search
      result written into the record.
      Unblocked by block 1. BC-052 delivered an operator whose controls fire and a verifier
      that refuses by name, which is this commitment's entry criterion, so the dependency is
      discharged rather than merely older. The schema decision phase 4 needs -- whether a
      fourth `scalar.kind` extends `Witness/v1` or forces a `v2` migration -- is taken in
      this block with calibration results in hand, not before them.
      Closed in session-037, slightly past the nominal boundary against block 4's slack.
      Phases 3 and 4 are built and calibrated. The route agrees with the exact one on
      n = 5, n = 10 and n = 11 -- strictly above each exact side and falling with the
      relaxation -- and proves an overlap of 1e-30 that a float check at 1e-9 accepts,
      which is the discrimination agreement alone cannot demonstrate. At n = 29 the chain
      completes: `s(29) <= 5.93383346267692918974379895098` at eps = 1e-20, all 406 pairs
      strictly separated, recorded `unresolved` with `needs_review: true` and promoting
      nothing. The strongest check was unplanned: verified unrelaxed, the 52 pairs the
      chain cannot decide are exactly the 52 contacts BC-042 extracted by a different
      route. D-356 records a control-harness limitation found on the way and reproduced on
      a clean tree.
  - id: BC-054
    purpose: tool_validation
    owner_focus: correctness
    instances: [11, 29]
    state: complete
    priority: 1
    question: >-
      Can the contact equations be assembled and closed from a frozen structure, and can
      the closed system then be solved exactly and discharged rather than trusted?
    hypotheses: []
    budget: >-
      180 minutes from about 2026-08-29T08:40Z, in slices of at most 30; a 20-minute
      finalization reserve inside that total
    entry: >-
      BC-042 froze the n = 29 contact structure with an empty ambiguity report, which is
      BC-043's entry criterion; BC-047 supplies the refinement BC-044 needs; origin/main
      has been merged at the start of this block
    exit: >-
      A reduced system in `s` and the distinct non-axis-aligned angles, closed by
      determinant conditions and reproducing the known n = 11 system — or a typed
      statement of which reduction the particular contact graph does not admit. Then, if
      the clock allows, BC-044's exact solve under its frozen margin rule.
    artifacts:
    - src/sqpack/promote/system.py
    - src/sqpack/promote/contacts.py
    - tests/test_promote_system.py
    - atlas/known-best/contact-structures.json
    bead: think-zm3f
    depends_on: []
    workflows: [pipeline-improvement]
    next_evidence: >-
      This is the unbuilt middle of the exact route: `promote/contacts.py` and
      `promote/refine.py` exist, and `promote/system.py` and `promote/solve.py` do not, so
      the pipeline currently runs from a structure straight to a refinement with no
      assembly between them.
    note: >-
      Advances BC-043 and then BC-044, both in agenda-005, which own their exits. This
      lane is independent of BC-052 and BC-053: the exact and interval routes are
      complements, and neither unblocks the other. X-004 found no integer relation through
      degree twenty below 10^22, so BC-044 may terminate in a refusal, and a refusal here
      is a result rather than a failure of the block.
      Closed in session-038, and it reached BC-043 rather than BC-044: the block clock went
      to three findings that each changed what assembly had to do. Contacts now identify
      which features meet -- typed from the intersection of their supports across every
      realising axis, because per-axis reading turns a corner-corner contact into two
      edge-edge ones that do not exist -- and assembly turns a structure into equations that
      vanish at the packing they came from, `4.44e-16` at n = 11. Counting rows is the wrong
      instrument: n = 11 is overdetermined by the count and four conditions short by the
      rank, so closure is sized by the shortfall. An angle class does not license an angle
      identity, which n = 29 showed with a residual of exactly pi. And seven n = 29 squares
      are reflected, which a centre-plus-rotation pose cannot represent, so assembly refuses
      them by name. Phase 4's exact solve was not reached.
  - id: BC-055
    purpose: tool_validation
    owner_focus: efficiency
    instances: [5]
    state: stopped
    priority: 1
    question: >-
      Can verification run only the steps a change can reach without ever running fewer
      than it should, and are the three packings the catalogue annotates "Rigid." actually
      rigid on evidence of our own?
    hypotheses: []
    budget: >-
      150 minutes from about 2026-08-29T11:40Z, split between the two lanes, in slices of
      at most 30; a 20-minute finalization reserve inside that total
    entry: >-
      A measured baseline for the gate exists — 4m15s for `--fast` on this container,
      recorded in block 1 — and origin/main has been merged at the start of this block
    exit: >-
      Either a reachability-scoped verification selector with a control proving it cannot
      under-run, measured against that baseline, or a measured rejection. Then a bounded
      n = 5 rigidity pass that produces our own evidence or names exactly what it would
      take.
    bead: think-ojlr
    depends_on: []
    workflows: [efficiency-loop, research-pass]
    next_evidence: >-
      The 4m15s baseline was measured on this container at the start of the run rather
      than assumed, and its breakdown is already known: 250.86s of fast behavioural tests
      against 40.38s of soft-schema validation and 30.29s of lint. Any selector that does
      not move the test figure has not moved the gate.
    note: >-
      Advances BC-051 and BC-049 in agenda-005. Deliberately last: both lanes are
      independent and bounded, so this is the block that can absorb overrun from the three
      ahead of it without any scientific commitment being cut short. Under-running the
      gate is the failure mode that matters; a selector that is merely slow is a
      disappointment, and one that skips a step a change can reach is a soundness defect.
      Not run, and recorded as stopped rather than left ready so the queue does not imply
      work that this run did not do. Blocks 2 and 3 each overran into the slack this cell
      was placed last to absorb, which is what the slack was for; the choice at the boundary
      was between a rushed efficiency change to the shared gate and a real endpoint check,
      and the endpoint check won. Nothing measured here is retracted: the 4m15s baseline
      stands and BC-051 and BC-049 remain ready in agenda-005.
  - id: BC-056
    purpose: tool_validation
    owner_focus: process
    instances: [5, 10, 11, 16, 29]
    state: ready
    priority: 0
    question: >-
      After a night of unattended work, does the whole record still hold together at the
      endpoints — gate, generated views, schemas, links, and the PR?
    hypotheses: []
    budget: 40 minutes from about 2026-08-29T14:10Z
    entry: >-
      The four blocks have reached terminal states, whatever those states are: BC-052,
      BC-053 and BC-054 complete, BC-055 stopped unrun
    exit: >-
      A full strict `packing-validate` receipt, every generated view regenerated from its
      source, a research-loop logbook entry covering the run, agenda and session artifacts
      reconciled with what actually happened, and a pushed PR whose checks are green.
      Blocks that stopped early are recorded as stopped with their exact limitation, never
      quietly dropped.
    bead: think-lo3p
    depends_on: [BC-052, BC-053, BC-054]
    workflows: [process-review]
    next_evidence: >-
      The strict gate is the only receipt that exercises the slow tiers, and no block
      above runs it; each runs the fast gate instead. So the run's one end-to-end check
      belongs here, where there is still clock left to repair what it finds.
    note: >-
      The endpoint check is a commitment rather than a courtesy: an unattended run that
      ends without one has produced work nobody has seen fail.
---
# agenda-006 — four bounded overnight blocks

One unattended run, 2026-08-29, from about `03:10Z` to about `14:50Z`. The blocks are
sized so that an interruption costs one block rather than the night, and so that the
lane most likely to move a verified bound runs while the clock is longest.

## The schedule

| Block | Clock | Advances | Lane |
| --- | --- | --- | --- |
| `BC-052` | `03:10Z`, 150 min | BC-045, spec phases 1–2 | Interval certification |
| `BC-053` | `05:40Z`, 180 min | BC-045, spec phases 3–4 | Interval certification |
| `BC-054` | `08:40Z`, 180 min | BC-043, then BC-044 | Exact promotion |
| `BC-055` | `11:40Z`, 150 min | BC-051 and BC-049 | Efficiency and rigidity |
| `BC-056` | `14:10Z`, 40 min | — | Endpoint check |

Start times are nominal.
A block that finishes early starts the next one early; a block that overruns eats into
BC-055, which is placed last precisely because it can absorb that without cutting a
scientific commitment short.
No block may borrow from BC-056.

## What every block owes, regardless of what it found

1. **Merge `origin/main` first**, from block 2 onward.
   Another agent is landing cleanups in parallel, and a block that starts from a stale
   base pays for it at the checkpoint rather than at the start.
2. **Run `tbd sync`**, so bead state is not the thing that drifts overnight.
3. **Commit, push, and update the PR.** A checkpoint that exists only in the working
   tree is not a checkpoint; the container is ephemeral.
4. **Run the fast gate** and leave it green, or leave the failure named.
5. **Record the result where it belongs** — an experiment for a measurement,
   `defects.yaml` for an actual error, the owning bead for work state — and never in
   this agenda, which holds the schedule and nothing else.

A negative or refused result satisfies these just as a positive one does.
The run has no target it is allowed to reach by loosening something.

## Why this order

The interval route is first because it is the only lane here that can move
`verified_upper_bound`, and because it is the one session-035 left declared and
unstarted. It is also the tractable half of the promotion problem: it certifies a root
without needing the minimal polynomial that X-004 could not find.

The exact route is third because it is genuinely independent — neither route unblocks
the other — and because its likeliest outcome is a typed refusal, which is worth having
but is not worth the longest clock.

The efficiency and rigidity lanes are last because they are the two that can be cut
short without leaving a scientific question half-answered.

## What this agenda does not own

Every scientific exit.
BC-045, BC-043, BC-044, BC-051 and BC-049 in
[agenda-005](agenda-005-symbolic-promotion-and-identity.md) own their criteria, and the
specs own their phase contracts.
This agenda owns when work starts, when it must stop, and what it must leave behind.

The accept rule is untouched, and the one clause that is a judgment rather than
arithmetic stays out of reach: an unattended runner may decline a marginal result and
may not accept one. Anything at `n = 29` that passes is recorded `unresolved` with
`needs_review: true`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
