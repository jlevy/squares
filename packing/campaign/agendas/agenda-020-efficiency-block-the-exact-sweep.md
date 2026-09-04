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
    own efficiency block. All four things W5 asks for at entry were already on record
    before any change: a measured baseline (the exact event-cell sweep that decides Condition 5
    at the retention gate fits atoms^2.00 and cost 5378 s on the largest retained
    certificate), a profile (one direction of that certificate spends 39.35 s in a
    dense Fraction grid against 2.29 s reducing the atoms to their reachable cells), a
    target (at least 10x, the operator's own figure being under 100 s for the n = 20
    decision), and a guard (the identical least covered mass on every retained
    certificate, with the Fraction sweep kept unchanged as the reference). The change
    is exact rather than approximate -- an integer difference array on the weights'
    common scale, reachable cells held as spans instead of expanded tuples, and the 181
    directions decided in parallel -- and is checked against the unchanged Fraction
    route cell for cell, never substituting for it. The measured result is 68x to
    roughly 183x depending on machine load, comfortably past the target, with no bound,
    verdict, or artifact changed and the interval route untouched as the independent
    second decision on every retained certificate. What moves is agenda-019's BC-190:
    its premise was that the retention gate was the dominant cost, and that premise is
    now gone; its baseline is the integer sweep. BC-191's row-generation and
    site-density costs are untouched and are now what binds.
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
      reference it is checked against, cell for cell?
    budget: >-
      Measured baseline, entry condition rather than the first task: the sweep fits
      atoms^2.00 over three paired runs on frozen bytes -- 1473 s at 1184 atoms
      (n = 17, 18), 4866 s at 2097 (n = 12), 5378 s at 2260 (n = 19, 20, 21) -- recorded
      in agenda-019's cost table and in frontier/results.yaml's T-017 and T-020
      next_rung. Profile, also entry rather than task: one direction of the n = 20
      certificate (2260 atoms; u = v = 4522 shared events; a 20,448,484-cell grid, of
      which 16,599,441 cells are reachable) spends 2.29 s in reduce_to_cells, almost
      all of it building that 16.6M-tuple list, against 39.35 s in the dense Fraction
      grid -- reproduced in this session directly from packing/cases/n20_fractional_certificate/certificate.json
      at direction index 37, which returns exactly those event and cell counts.
      Target: at least 10x, the operator's own figure being under 100 s for the n = 20
      decision. Guard: the identical least_cell_mass on every retained certificate, and
      minimum_covered_mass_fraction kept unchanged as the reference, held to the
      integer route cell for cell, direction by direction.
      Entered directly on the operator's direction, not from a pre-declared timebox.
      Three changes, each exact. weight_scale takes the lcm of the atom weights'
      denominators -- every retained certificate's weights are multiples of 1/200000,
      since rationalise rounds to that scale -- and minimum_covered_mass_integer runs
      the same difference-array sweep in int64 on that scale, two np.cumsum passes
      standing in for the two prefix sums the Fraction route takes one cell at a time;
      the scaled total is checked against 2**60 and minimum_covered_mass falls back to
      the Fraction route above it. reduce_to_spans holds the reachable cells as one
      (i, j0, j1) span per column instead of one tuple per cell, and reduce_to_cells is
      now defined as that expanded, so the two agree by construction rather than by a
      separate check. certificate.verify decides the 181 directions in a
      ProcessPoolExecutor, forked on Linux because Python 3.14's default forkserver
      re-imports the caller's __main__ and dies with a connection reset for a stdin
      caller; serial below 400 atoms; an explicit workers= always gets a pool; results
      ordered by direction so the first-attaining label does not depend on the
      schedule.
    entry: >-
      Agenda-019's cost table, frontier/results.yaml's T-017 and T-020 next_rung, and
      bead think-yrh5 already carry the baseline and the profile; the target and the
      guard were fixed before sweep.py or certificate.py changed.
    exit: >-
      A change with its equivalence guard intact, not a rejection. Measured on the same
      loaded box with the Fraction replay still running beside it: n = 17 (1184 atoms)
      in 21.8 s against 1473 s (68x), n = 20 (2260 atoms) in 38.7 s against 5378 s
      (139x), both returning the declared least covered mass. A later quiet-box replay
      of the retained command (python -m cases.n20_fractional_certificate), Fraction
      replay stopped, took 29.4 s wall (about 100 s CPU across four workers) and
      printed the same verdict -- least cell mass 50007/50000 at direction 0, VERIFIED:
      s(m) >= 24/5 for every m >= 19 -- against the 5378 s reference, about 183x; this
      session reproduced the identical printed values on a different, slower box.
      Equivalence: all 181 directions of the 373-atom n = 11 rung, Fraction against
      integer, value and witness, no mismatch, in 145 s. Tests:
      packing/tests/test_fractional_sweep_integer.py, 12 tests, 31.7 s (32.4 s
      reproduced in this session), covering the scale, full-net equivalence on a
      synthetic certificate at scale 231, six directions of the retained rung,
      spans-equal-cells, the overflow fallback with the limit patched down,
      parallel-equals-serial, and the n = 17 decision in the fast tier. The fast
      fractional suite as a whole -- 55 tests across test_fractional_certificate.py and
      test_fractional_interval.py, not exhaustive -- ran in 24 s where the same
      selection took 351 s that morning.
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
      Whether BC-191's row-generation and site-density costs, now the binding cost with
      the gate an order of magnitude cheaper, move by a comparable factor once measured
      the same way; and whether BC-190's premise -- that the generator's own
      accept/reject decision should move to the interval route -- still holds now that
      its baseline is the integer sweep rather than the Fraction one.
    outcomes:
    - scope: the exact event-cell sweep's Condition 5 decision at the retention gate
      classification: achieved
      result: >-
        The sweep now decides in int64 on the weights' common scale, holds reachable
        cells as spans, and runs the 181 directions in parallel; it returns the
        identical least covered mass the Fraction route returns, cell for cell, at 68x
        (n = 17) and 139x (n = 20) on a loaded box and roughly 183x on a quiet one --
        past the 10x target and the operator's under-100-s figure for n = 20 by a wide
        margin, with the Fraction route retained unchanged as the reference and the
        interval route untouched as the independent second decision.
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
      decision: checked-current
      reason: >-
        The New Results section reports T-017 through T-020 by bound and score; it
        never states the retention gate's cost, so there is nothing in it for the
        integer sweep to correct.
    - path: SYNOPSIS.md
      decision: checked-current
      reason: >-
        Grepped for 5378 and atoms^2: the only hit is the covering-value curve's
        quadratic fit at the five restricted optima, an unrelated claim. No sentence
        here states the sweep's cost, so none needed updating.
    - path: TUTORIAL.md
      decision: checked-current
      reason: >-
        Its uses of "sweep" are golden-section bracketing and the instance-cell
        glossary entry; neither names the event-cell sweep or its cost.
    - path: conventions.md
      decision: checked-current
      reason: >-
        Its one "sweep" reference is the hypothesis-to-experiment glossary entry for a
        parameter sweep; it does not describe the event-cell sweep or its cost.
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
        sweep.py decides Condition 5 in int64 on the weights' common scale, holds reachable
        cells as one span per column, and certificate.py's verify runs the 181
        directions in a process pool; the change is checked cell for cell against the
        unchanged Fraction route rather than replacing it.
      paths:
      - packing/src/sqpack/fractional/sweep.py
      - packing/src/sqpack/fractional/certificate.py
      - packing/tests/test_fractional_sweep_integer.py
    - name: record-sync
      result: >-
        Propagated the new gate cost into the results register, the block-close
        handoff, and the retarget exploration's cost section, and re-based agenda-019's
        BC-190 premise off the integer sweep rather than the Fraction one.
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
          Row generation is 79-94% of every round and untouched by this block; site
          density and the rationalisation scale are still unmeasured against the
          container side. With the gate an order of magnitude cheaper, this is now the
          binding cost.
      - bead: think-jgeg
        workflow: efficiency-loop
        priority: 0
        rationale: >-
          Re-based: its premise that the retention gate was the dominant cost is gone.
          The question left is whether the generator's own inner-loop accept/reject
          decision is worth moving to the interval route, measured against the integer
          sweep's baseline rather than the Fraction sweep's.
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
guard. All four were on record before this block touched a line of code.

**Baseline.** The exact event-cell sweep that decides Condition 5 at the retention gate
— every retained certificate’s least covered mass — was measured on three paired runs
against frozen bytes, the only comparison this record trusts:

| Atoms | Case | Time |
| ---: | --- | ---: |
| 1184 | `n = 17, 18` (side `459/100`) | `1473 s` |
| 2097 | `n = 12` (side `99/25`) | `4866 s` |
| 2260 | `n = 19, 20, 21` (side `24/5`) | `5378 s` |

Three points fit `atoms^2.00` over the range.
This table is agenda-019’s own, and the two extreme rows are also carried independently
in `frontier/results.yaml`’s `T-017` and `T-020` `next_rung` fields, so the baseline has
two citations rather than one.

**Profile.** Measured the same evening, one direction of the `n = 20` certificate (2260
atoms) with a `Fraction` replay of the whole verification running beside it in another
process. `reduce_to_cells` took `2.29 s`; the dense `Fraction` grid took `39.35 s`. This
session reproduced the shape of that split directly:
`packing/cases/n20_fractional_certificate/certificate.json` decoded and reduced at
direction index 37 gives `u = v = 4522` shared events, a `20,448,484`-cell dense grid,
and exactly `16,599,441` reachable cells — the same figure the commit that made this
change quotes. The grid was roughly 95% of the direction’s cost and the 16.6M-tuple cell
list was most of the rest.

**Target.** At least `10×`, with the operator’s own figure — under `100 s` for the
`n = 20` decision — as the number this block was actually held to.

**Guard.** The identical `least_cell_mass` on every retained certificate, and
`minimum_covered_mass_fraction` kept unchanged as the reference rather than replaced,
held to the integer route cell for cell, direction by direction.
This is the guard [`decide_certificate.py`](../../devtools/decide_certificate.py)
already enforces at the retention gate — deciding a rung only when the frozen bytes are
accepted, and agree, by two routes that fail differently — extended here to a second
internal check between the sweep’s own two implementations.

## The change

Three exact changes, read directly from
[`sweep.py`](../../src/sqpack/fractional/sweep.py) and
[`certificate.py`](../../src/sqpack/fractional/certificate.py) rather than restated from
memory.

`weight_scale` takes the least common multiple of the atom weights’ denominators.
Every retained certificate’s weights are multiples of `1/200000`, because the
generator’s `rationalise` step rounds each orbit to that scale already, so the scale
this function finds for a retained certificate is the scale it was built at.
`minimum_covered_mass_integer` then runs the same difference-array sweep
`minimum_covered_mass_fraction` always ran, but in `int64` on that scale: two
`np.add.at`/`np.subtract.at` passes build the signed difference array, and two
`np.cumsum` passes stand in for the two prefix sums the `Fraction` route takes one cell
at a time. The scaled total mass is checked against `2**60` before the integer route
runs, and `minimum_covered_mass` falls back to the `Fraction` route above that limit — a
decline rather than a risked wraparound.

`reduce_to_spans` holds the reachable cells as one `(i, j0, j1)` span per column instead
of one tuple per cell.
`reduce_to_cells` is now *defined* as that same span reduction, expanded — not computed
separately and checked for agreement after the fact — so the two cannot drift apart from
each other; a test exists (`test_the_span_reduction_is_the_ cell_reduction_folded`) but
it is confirming construction, not substituting for it.

`certificate.verify` decides the 181 directions of a certificate in a
`ProcessPoolExecutor`, using the `fork` start method on Linux rather than the platform
default. Python 3.14 defaults to `forkserver`, which re-imports the caller’s `__main__`;
a caller invoked from stdin has none, and the pool died with a connection reset — this
was hit while making the change and is the reason the code names the fork context
explicitly rather than leaving the default in place.
Below 400 atoms the loop runs serially in-process, since starting a pool costs more than
the milliseconds it would save; an explicit `workers=` argument always gets a pool
regardless of atom count, so a small certificate can still be used to compare the two
schedules. Results are returned ordered by direction whichever way they ran, so the
reduction that follows — first direction attaining the minimum wins — does not depend on
the schedule, and `test_the_parallel_direction_loop_matches_the_serial_one` checks
exactly that.

## The measurement

Measured on the same loaded box, with the `Fraction` replay of the whole verification
still running beside it in another process: `n = 17` (1184 atoms) decided in `21.8 s`
against the `1473 s` baseline (`68×`), and `n = 20` (2260 atoms) in `38.7 s` against
`5378 s` (`139×`), both returning the declared least covered mass.
A later replay of the retained command, `python -m cases.n20_fractional_certificate`,
with the `Fraction` replay stopped so the box was quiet, took `29.4 s` wall (about
`100 s` of CPU spread across four workers) and printed the same verdict —
`least cell mass 50007/50000 at direction 0` and
`VERIFIED: s(m) >= 24/5 for every m >= 19` — against the `5378 s` reference, about
`183×`. This session re-ran the same replay on a different, slower sandbox and
reproduced the identical printed values, though not the same wall time; the two boxes
disagree on the constant and agree on everything the certificate actually claims, which
is the only agreement that matters.

Equivalence, the correctness argument and not merely a speed claim: all 181 directions
of the 373-atom `n = 11` rung, `Fraction` against integer, value and witness cell both,
no mismatch, in 145 s. `packing/tests/test_fractional_sweep_integer.py` holds this and
eleven further checks — the scale is the correct lcm, the two routes agree on every
direction of a small synthetic net at scale 231, six directions of the retained `n = 11`
rung including both ends, `reduce_to_cells` is exactly the spans expanded, the overflow
fallback declines correctly with the limit patched down, the parallel schedule matches
the serial one, and the `n = 17` certificate verifies in the fast tier at its declared
value — 12 tests in `31.7 s` (`32.4 s` reproduced in this session).
The wider fast fractional suite — `test_fractional_certificate.py` and
`test_fractional_interval.py`, 55 tests, not the exhaustive tier — ran in `24 s` where
the same selection took `351 s` that morning, which is the fast tier’s own
before-and-after rather than a claim about this file alone.

## What this changes, and what it does not

Agenda-019’s `BC-190` asked whether the generator’s own accept-or-reject decision should
move to the interval route, on the premise that the retention gate’s exact sweep was the
dominant cost. That premise is gone: the gate is now an order of magnitude cheaper, and
`BC-190`’s question is about the generator’s inner loop rather than the gate, with the
integer sweep as its baseline rather than the `Fraction` sweep it was drafted against.
`BC-191` — row generation at 79–94% of every round, site density untuned against the
container side, the untuned-grid `8.8×` — is untouched by this block and is now what
binds a run. `BC-192` and `BC-194` are unaffected directly; both remain blocked on
`BC-191` pricing what a run at a larger side actually costs.

What did not change: no bound moved, no verdict changed, no certificate’s total mass or
declared least covered mass differs from what it was before this block, and the interval
route — the independent second decision at the retention gate — was not touched.
Retention is exactly as strict as it was: `devtools.decide_certificate` still refuses a
candidate unless both routes accept it and agree on the value, and this block added a
second such check inside the sweep itself rather than relaxing the first.

Selected next: `BC-191` (`think-ji0r`), because the cost that used to sit behind an
hours-long gate now sits in a search whose own cost as a function of container side has
never been measured, and every later commitment in agenda-019 is blocked on that number.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
