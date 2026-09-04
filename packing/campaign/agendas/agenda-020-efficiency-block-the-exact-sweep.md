---
title: "agenda-020 — efficiency block: the exact event-cell sweep decides in integers"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-020
  title: "Efficiency Block — the Exact Event-Cell Sweep Decides in Integers"
  updated: '2026-09-04'
  status: completed
  objective: >-
    A one-block W5 efficiency-loop commitment, entered directly on the operator's
    direction rather than drawn from agenda-019's queued candidates, and recorded here
    after the fact at the operator's further direction to track and capture it as its
    own efficiency block. The entry record contained operator-reported timing baselines,
    a one-direction profile, a tenfold target, and an equivalence guard; it did not retain
    raw timings, machine state, or a controlled benchmark. The implementation now uses
    an exact integer difference array on the weights' minimal common denominator, stores
    reachable cells as spans, and runs directions through an affinity- and memory-bounded
    process pool. Integration review restored an independent legacy cell/Fraction
    reduction, made the public integer helper enforce its overflow preconditions, and
    removed an unsafe forced-fork context. Retained tests compare the independent routes
    on a small full net and selected directions of a retained rung; full retained
    certificates are still decided by the exact route and by the method-distinct interval
    route. Pre-integration speed reports are planning evidence, not a benchmark for the
    corrected implementation. No bound, verdict, or certificate artifact changed.
  items:
  - id: BC-196
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11, 12, 17, 18, 19, 20, 21]
    state: complete
    priority: 0
    question: >-
      Can the exact event-cell sweep that decides Condition 5 at the retention gate be made at
      least ten times faster without changing what it decides -- the same least
      covered mass on every retained certificate, with the Fraction sweep still the
      reference it is checked against on declared guard cases?
    budget: >-
      Operator-reported baseline, entry condition rather than a retained benchmark: the
      former Fraction sweep took 1473 s at 1184 atoms
      (n = 17, 18), 4866 s at 2097 (n = 12), 5378 s at 2260 (n = 19, 20, 21) -- recorded
      in agenda-019's cost table and in frontier/results.yaml's T-017 and T-020
      next_rung. The three-point least-squares exponent is 2.04; 2.00 is only the
      1184-to-2260 endpoint slope. No raw timing transcript, machine description, or load
      trace is retained. Profile, also an operator report: one direction of the n = 20
      certificate (2260 atoms; u = v = 4522 shared events; a 20,448,484-cell grid, of
      which 16,599,441 cells are reachable) spends 2.29 s in reduce_to_cells, almost
      all of it building that 16.6M-tuple list, against 39.35 s in the dense Fraction
      grid. The deterministic event and cell counts are reproducible from
      packing/cases/n20_fractional_certificate/certificate.json at direction index 37;
      the timings are not retained measurements.
      Target: at least 10x, the operator's own figure being under 100 s for the n = 20
      decision. Guard: identical values and witnesses between independently implemented
      span/integer and cell/Fraction reductions on a tractable full net and selected
      retained directions; serial/parallel agreement; every retained certificate still
      accepted by the exact route and the method-distinct interval route.
      Entered directly on the operator's direction, not from a pre-declared timebox.
      Three changes, each exact. weight_scale takes the lcm of the atom weights'
      denominators, which divides the generator's configured rationalisation scale, and
      minimum_covered_mass_integer runs the same difference-array sweep in int64 on that
      minimal scale, two np.cumsum passes
      standing in for the two prefix sums the Fraction route takes one cell at a time;
      the public helper checks nonnegativity, scale integrality, and the 2**60 scaled-total
      limit itself, while minimum_covered_mass falls back to Fraction above that limit.
      reduce_to_spans holds one (i, j0, j1) span per column; reduce_to_cells independently
      retains the legacy geometry as a reference. certificate.verify uses Python's safe
      platform-default process context, runs serially for a non-importable main module or
      below 400 atoms, and caps worker multiplicity by affinity, a fixed maximum, and a
      concurrent-grid memory budget. One supported grid may exceed that parallelism
      budget but is never multiplied. Results stay in direction order.
    entry: >-
      Agenda-019's cost table, frontier/results.yaml's T-017 and T-020 next_rung, and
      bead think-yrh5 already carry the baseline and the profile; the target and the
      guard were fixed before sweep.py or certificate.py changed.
    exit: >-
      A corrected exact implementation with retained safety and equivalence controls.
      Before the integration hardening, operator reports gave 21.8 s at 1184 atoms and
      38.7 s or 29.4 s at 2260, returning the declared least covered masses; those runs
      used the uncapped four-worker implementation and are not benchmarks for current
      defaults. The original all-181-direction comparison of the 373-atom n = 11 rung
      shared its geometry implementation, so it controlled arithmetic but not geometry.
      Current retained tests compare independent geometry at one retained direction,
      independent values and witnesses on six retained directions and every direction of
      a small synthetic net, overflow refusal through the public helper, serial/parallel
      equality, safe stdin fallback, bounded worker allocation, and a full n = 17 exact
      decision. Final validation and its exact test counts belong in the stacked review.
    bead: think-yrh5
    workflows: [efficiency-loop]
    depends_on: []
    artifacts:
    - packing/src/sqpack/fractional/sweep.py
    - packing/src/sqpack/fractional/certificate.py
    - packing/tests/test_fractional_sweep_integer.py
    - packing/frontier/results.yaml
    - packing/campaign/explorations/X-013-where-the-certificate-should-go-next.md
    - docs/project/handoff-2026-09-04-block-close.md
    next_evidence: >-
      Whether BC-191's row-generation and site-density costs dominate after a controlled
      end-to-end measurement; and whether BC-190's premise -- that the generator's own
      accept/reject decision should move to the interval route -- still holds now that
      its baseline is the integer sweep rather than the Fraction one.
    outcomes:
    - scope: the exact event-cell sweep's Condition 5 decision at the retention gate
      classification: achieved
      result: >-
        The sweep now decides in int64 on the weights' minimal common scale, holds
        reachable cells as spans, and uses a bounded process pool. Its result is checked
        against an independently retained cell/Fraction reference on tractable nets and
        selected retained directions, while the interval route remains the method-distinct
        full-certificate confirmation. Historical pre-cap speed reports exceeded the
        target, but the corrected implementation still needs a retained benchmark before
        that performance claim can be promoted.
      evidence:
      - packing/src/sqpack/fractional/sweep.py
      - packing/src/sqpack/fractional/certificate.py
      - packing/tests/test_fractional_sweep_integer.py
      - packing/frontier/results.yaml (T-017 and T-020 next_rung)
      - commit d8733ad0
      disposition: retire-success
      follow_up: null
  closeout:
    documentation_review:
    - path: README.md
      decision: updated
      reason: >-
        The stacked review bounded the n = 12 priority and fixed-net ceiling claims to
        the retained corpus and the current direction net.
    - path: SYNOPSIS.md
      decision: checked-current
      reason: >-
        Grepped for 5378 and atoms^2: the only hit is the covering-value curve's
        quadratic fit at the five restricted optima, an unrelated claim. No sentence
        here states the sweep's cost, so none needed updating.
    - path: TUTORIAL.md
      decision: updated
      reason: >-
        The stacked review added an atoms-and-weights explanation, the five proof
        conditions, and a link to the minimal checker and visual.
    - path: conventions.md
      decision: updated
      reason: >-
        The notation rule now reserves C0--C5 for epistemic confirmation levels and
        names mathematical hypotheses Condition 1, Condition 2, and so on.
    - path: development.md
      decision: checked-current
      reason: >-
        Its "sweep" reference is the unrelated n = 29 arbitrary-precision digit sweep;
        the event-cell sweep's cost is not mentioned here.
    - path: operating-rules.md
      decision: checked-current
      reason: >-
        Carries the operating rules (OR-1 through OR-11) rather than a per-instrument
        cost claim; nothing here names the sweep or its cost.
    changes:
    - name: integer-event-cell-sweep
      result: >-
        sweep.py decides Condition 5 in int64 on the weights' minimal common scale and
        holds reachable cells as one span per column. certificate.py uses a bounded
        process pool. An independently retained legacy cell/Fraction route supplies the
        internal reference on declared guard cases.
      paths:
      - packing/src/sqpack/fractional/sweep.py
      - packing/src/sqpack/fractional/certificate.py
      - packing/tests/test_fractional_sweep_integer.py
    - name: record-sync
      result: >-
        Propagated the implementation change and its evidence boundary into the results
        register, handoff, and retarget exploration. Agenda-019's BC-190 now begins by
        measuring the integer and interval routes instead of assuming either dominates.
      paths:
      - packing/frontier/results.yaml
      - packing/frontier/RESULTS.md
      - docs/project/handoff-2026-09-04-block-close.md
      - packing/campaign/agendas/agenda-019-efficiency-first-retarget-and-deep-strategy.md
      - packing/campaign/explorations/X-013-where-the-certificate-should-go-next.md
      - packing/campaign/ledger.md
    validation:
    - scope: schema-validation
      status: passed
      evidence: >-
        uv run --frozen --all-extras --group dev python -m devtools.validate_schemas
        from packing/, reported verbatim in the closing session.
    - scope: agenda-map-render
      status: passed
      evidence: >-
        uv run --frozen --all-extras --group dev python -m devtools.render_agenda_map
        --check from packing/, reported verbatim in the closing session.
    - scope: documentation-check
      status: passed
      evidence: >-
        uv run --frozen --all-extras --group dev python -m devtools.check_documentation
        from packing/, reported verbatim in the closing session.
    replanning:
      candidates:
      - bead: think-ji0r
        workflow: efficiency-loop
        priority: 0
        rationale: >-
          Operator reports put row generation at 79-94% of observed rounds; site density
          and the rationalisation scale remain unmeasured against container side. A
          controlled end-to-end run must determine whether this is now the binding cost.
      - bead: think-jgeg
        workflow: efficiency-loop
        priority: 0
        rationale: >-
          Re-based: the former Fraction-sweep baseline is obsolete. The question left is
          whether the generator's inner-loop decision is worth moving to the interval
          route, measured against the corrected integer sweep.
      - bead: think-9pfw
        workflow: insight-iteration
        priority: 1
        rationale: >-
          Turns the reach table's ranking into a priced target list; still blocked on
          BC-191 to price its candidates honestly.
      - bead: think-48p0
        workflow: research-loop
        priority: 1
        rationale: >-
          The first high-prize case above a perfect square, with a cost model recorded
          before the run; still blocked on a target and a priced cost model from
          BC-191 and BC-192.
      selected:
        bead: think-ji0r
        workflow: efficiency-loop
        rationale: >-
          Row generation's cost as a function of container side is what every later
          commitment needs priced, and it is the one candidate whose measurement this
          block did not already change the terms of.
      operator_input:
        status: confirmed
        note: >-
          The operator directed this block directly -- it should be at least 10x
          faster -- and asked for it to be tracked and captured as its own efficiency
          block rather than folded silently into agenda-019's BC-190; this record is
          that capture, filed after the work rather than before it.
---
# Agenda 020 — Efficiency Block: the Exact Event-Cell Sweep Decides in Integers

## Workflow Entry Point

This agenda is complete.
It records a single W5 `efficiency-loop` block that the operator directed and that ran
to completion the same evening agenda-019 was drafted, before agenda-019 opened.
Nothing here is queued; it exists so the block has its own commitment, its own bead, and
its own outcome rather than living only as a paragraph inside agenda-019’s handoff
section.

## What W5 asks for at entry, and how each was met

[`packing/campaign/README.md`](../README.md) requires four things before a W5 slice may
open: a measured baseline, a profile, a target metric, and an equivalence or validity
guard. All four were reported before this block touched a line of code.

The record is weaker than that first sentence once “measured” is read as “independently
reproducible.” Its timings are operator reports with no raw transcript, machine
description, or load trace.
They justified an optimization experiment; they do not support a benchmark-quality
performance claim.

**Baseline.** The former Fraction event-cell sweep that decides **Condition 5** had
three reported timings on frozen certificates:

| Atoms | Case | Time |
| ---: | --- | ---: |
| 1184 | `n = 17, 18` (side `459/100`) | `1473 s` |
| 2097 | `n = 12` (side `99/25`) | `4866 s` |
| 2260 | `n = 19, 20, 21` (side `24/5`) | `5378 s` |

The least-squares log-log exponent of those three reports is `2.04`; `2.00` is only the
1184-to-2260 endpoint slope.
Repetition of the same reports in Agenda 019 and `frontier/results.yaml` is provenance,
not independent support.

**Profile.** One direction of the 2260-atom certificate reportedly spent `2.29 s`
constructing reachable cells and `39.35 s` in the dense Fraction grid.
The structural part is reproducible: direction 37 has 4522 events on each axis, a
20,448,484-entry dense grid, and 16,599,441 reachable cells.
The timing split remains an operator report.

**Target.** At least `10×`, with the operator’s own figure — under `100 s` for the
`n = 20` decision — as the number this block was actually held to.

**Guard.** The merged implementation retains two internal paths: span geometry with
integer arithmetic, and the independently implemented legacy cell geometry with Fraction
arithmetic. Tests compare values and witnesses on every direction of a small net and six
directions of a retained 373-atom rung, and compare the two geometries directly at one
retained direction. Serial and parallel schedules must agree.
At the retention gate, every full certificate still has to agree with the
method-distinct interval decision.

## The change

The implementation has three exact changes, read directly from
[`sweep.py`](../../src/sqpack/fractional/sweep.py) and
[`certificate.py`](../../src/sqpack/fractional/certificate.py) rather than restated from
memory.

`weight_scale` takes the least common multiple of the atom weights’ denominators.
That minimal denominator divides the generator’s configured rationalisation scale; it
need not equal it after factors cancel.
`minimum_covered_mass_integer` then runs the same difference-array sweep
`minimum_covered_mass_fraction` ran, but in `int64` on that scale: two
`np.add.at`/`np.subtract.at` passes build the signed difference array, and two
`np.cumsum` passes stand in for the two prefix sums the `Fraction` route takes one cell
at a time. The public integer entry point checks nonnegative weights, scale integrality,
and a conservative `2**60` bound before allocating `int64`; the dispatcher falls back to
Fraction above the bound.

`reduce_to_spans` holds the reachable cells as one `(i, j0, j1)` span per column instead
of one tuple per cell.
`reduce_to_cells` independently retains the legacy reduction.
This independence matters: the source-branch test expanded spans through the same
implementation and could not catch a shared geometry bug; the stacked integration
restored a genuine cross-check.

`certificate.verify` decides the 181 directions of a certificate in a
`ProcessPoolExecutor` using Python’s platform-default start method.
It never forces `fork` from library code.
A non-importable `__main__` such as `<stdin>` takes the serial path; ordinary parallel
callers must use the standard guarded script entry point.
The worker count is capped by process affinity, a fixed maximum, and a conservative
concurrent-grid budget.
One supported grid may exceed that parallelism budget, in which case it runs alone.
Small certificates run serially by default.
Results return in net order, so scheduling cannot change the first direction attaining
the minimum.

## The measurement

Before the safety integration, operator reports gave `21.8 s` at 1184 atoms and `38.7 s`
or `29.4 s` at 2260, all returning the declared exact least mass.
The latter report used four workers; the corrected 2260-atom default is constrained by
the aggregate grid budget and therefore is not the same configuration.
Ratios of `68×`, `139×`, and `183×` against the old cross-run reports are useful
planning observations, not controlled benchmarks.

The original all-181-direction comparison on the 373-atom rung also predated the
restored independent geometry, so it controlled arithmetic under shared geometry.
The integrated tests are stronger per compared direction and deliberately smaller in
retained scope. The current implementation’s performance remains to be measured under a
recorded environment after all safety corrections.

## What this changes, and what it does not

Agenda-019’s `BC-190` asked whether the generator’s own accept-or-reject decision should
move to the interval route, on the premise that the retention gate’s exact sweep was the
dominant cost.
The optimization invalidates the old baseline but does not establish a new
end-to-end bottleneck.
`BC-190` must compare the interval route against the current integer sweep, not the
former Fraction sweep.
`BC-191` — row generation at 79–94% of every round, site density untuned against the
container side, and the single reported untuned-grid `8.8×` contrast — is untouched.
Controlled measurement must determine whether it now binds.
`BC-192` and `BC-194` remain blocked on a prospective cost model.

What did not change: no bound moved, no verdict changed, no certificate’s total mass or
declared least covered mass differs from what it was before this block, and the interval
route — the independent second decision at the retention gate — was not touched.
Retention is exactly as strict as it was: `devtools.decide_certificate` still refuses a
candidate unless both method-distinct routes accept it and agree on the value.
The integer path changes the exact route’s implementation, not the theorem or its
evidence threshold.

Selected next is `BC-191` (`think-ji0r`), paired with the rebased `BC-190`, because the
search and decision costs as functions of side have not been measured under the current
implementation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
