---
title: session-042 — agenda-006 block 8, the exact route answers at n = 11 and refuses at n = 29
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-042
  title: Recover a minimal polynomial under the frozen margin rule, and record what n = 29 returns
  date: '2026-08-29'
  started_at: '2026-08-29T00:25:46-07:00'
  deadline_at: '2026-08-29T01:25:46-07:00'
  goal: >-
    Close agenda-006 block 8 by building the minimal-polynomial step under the promotion
    spec's frozen margin rule, calibrating it against Trump's published degree-eight
    polynomial at n = 11, and running it at n = 29 -- recording whatever comes back,
    including a refusal.
  workflow_phases:
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: work
    focus: correctness
    commitment: BC-060
    bead: think-ovp7
    objective: >-
      Build `promote/solve.py` implementing the three-clause margin rule, and calibrate it
      by recovering a polynomial that is already published.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 30
    started_at: '2026-08-29T00:25:46-07:00'
    deadline_at: '2026-08-29T00:55:46-07:00'
    expected_output: >-
      Trump's degree-eight polynomial recovered from digits alone, with every number the
      rule consumed recorded alongside the verdict.
    validation_command: >-
      uv run --frozen --group dev python -m pytest tests/test_promote_solve.py -q
    kill_condition: >-
      Stop if a clause is relaxed to make a candidate pass. The rule is the deliverable;
      a search that accepts is worth nothing without one that refuses.
    fallback: >-
      Record which clause the known answer fails and why, rather than shipping a rule
      calibrated to accept it.
    outcome: >-
      Recovered exactly, and discharged. Degree eight, coefficients identical to Trump's
      1979 publication, irreducible over Q, two real roots, and exactly one isolating
      interval containing the refined value.
    evidence:
    - >-
      'The rule as built: `C` is the largest coefficient the relation *actually carries*,
      not the search''s `maxcoeff` bound, and `B = (d+1) log10(C)` with `M = 200`. For
      Trump''s polynomial `C = 12420`, so `B = 36.85` and the relation must vanish below
      `10^-237`. It vanishes at `4.99e-338`, and re-evaluated at `2B + 2M` it keeps
      falling to `3.38e-412` -- clause 2, which is what a relation fitted to its digits
      cannot do.'
    - >-
      'It came back negated on the first run, and that is why the module normalises. An
      integer relation is determined only up to a unit and a common factor, so `pslq` may
      return `-p` or `2p` as readily as `p`, and a caller comparing against a published
      polynomial would see a spurious mismatch. Canonical form is primitive with a
      positive leading term.'
    - >-
      'Fitting is not minimality, so a `discharge` step follows the rule. Any multiple of
      the minimal polynomial vanishes just as well; irreducibility over Q is what makes
      the degree the *value''s* degree, and an isolating interval containing the refined
      value is what says which of the roots the packing is. The square of Trump''s
      polynomial is refused by name.'
    - >-
      'What `discharge` does **not** do is rebuild the packing from the field and
      re-verify it. That needs an exact solve of every pose unknown rather than the side
      alone, and calling this the whole round trip would overstate it. Named in the
      docstring rather than left for a reader to discover.'
    stop_reason: criterion
    next_action: >-
      Run the same rule at n = 29 on a thousand manufactured digits.
  - workflow: pipeline-improvement
    recording: contemporaneous
    clock_role: finalization
    focus: correctness
    commitment: BC-060
    bead: think-ovp7
    objective: >-
      Run the rule at n = 29, and retain both measurements as tools rather than as
      transcripts.
    status: completed
    entered_by: planned_checkpoint
    switch_reason: >-
      The calibration reached its criterion; the question becomes what the target
      returns.
    budget_minutes: 30
    started_at: '2026-08-29T00:55:46-07:00'
    deadline_at: '2026-08-29T01:25:46-07:00'
    expected_output: >-
      Whatever n = 29 returns, recorded either way, and two devtools that replay it.
    validation_command: >-
      uv run --frozen --all-extras --group dev packing-validate --fast
    kill_condition: >-
      Stop if a refusal is presented as anything other than a result. The spec says
      plainly that a refusal here would say the minimal polynomial is large, which is
      worth knowing and is why the interval route exists.
    fallback: Push with the failing step named.
    outcome: >-
      Refused, in the strongest available form. `pslq` returned **nothing at any degree
      from 2 through 20** below a coefficient bound of `10^22`, on a thousand digits with
      a reported residual bound of `1.09829e-1039`. Not one degree reached a clause.
    evidence:
    - >-
      'The contrast is the result. The planning probe ran on the ~98 serialized digits and
      got relations at almost every degree from 8 to 21 -- a search with more freedom than
      input. Fed a thousand digits manufactured from the closed system, the same search
      falls silent everywhere. A search that answers when under-fed and stops when fed
      properly is evidence about the number rather than about the search.'
    - >-
      'What it bounds: if `s(29)` is algebraic of degree twenty or less, some coefficient
      of its minimal polynomial is at least `10^22`. That is a statement the earlier probe
      could not make at any confidence, and it is the concrete reason the interval route
      exists rather than a preference.'
    - >-
      'The sweep costs about twelve minutes, which is why it is a tool with a recorded
      result rather than a test. `devtools/probe_minimal_polynomial.py` replays it and
      reports which clause decided each degree.'
    - >-
      '`devtools/probe_contact_system.py` is the other half, and it exists because
      D-361 was first found in a throwaway script. It reports what each retained case''s
      assembled system determines, and `--walk` steps the side-changing null direction and
      reads the violation''s *order* in `t` -- `O(t^2)` is an ordinary second-order
      obstruction, `O(t)` means an equation is wrong. That distinction is the whole of
      D-361 and it is now one command.'
    - >-
      'Building it surfaced the same bug D-359 records, in the new tool. The rank verdict
      is a judgement about a gap between singular values, and the gap the SVD can *see* is
      bounded by the precision it runs at: at mpmath''s ambient 15, Göbel''s discarded
      singular value read `2.3e-16` against a counted `0.511`, where pinned at 50 it is
      `1.04e-51`. Same verdict, a gap thirty-five decades narrower than the truth, and no
      way to tell from the output. Precision is pinned per case and printed alongside the
      gap.'
    - >-
      'Reaching into `_symbols_by_name` from the tool was a signal the module''s public
      surface was short, not a reason to suppress a lint. `contact_jacobian` is now public
      on `promote/system.py`, and the rank measurement and the probe share it.'
    stop_reason: criterion
    next_action: >-
      Open block 9 as session-043 under BC-061 and `think-twa7`.
  primary_bead: think-qs6k
  status: completed
  budget:
    wall_minutes: 60
    orientation_minutes: 3
    checkpoint_minutes: 5
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - The block deadline at 2026-08-29T01:25:46-07:00
  - Any clause of the margin rule relaxed to make a candidate pass
  - A refusal at n = 29 presented as anything other than a result
  - Any move of verified_upper_bound, which is a human decision
  progress:
    metric: >-
      Whether a refined value can be turned into a discharged algebraic claim
    before: >-
      No. `promote/solve.py` did not exist, and the only integer-relation evidence was a
      planning probe whose parameters were unrecorded and which accepted a degree-eight
      relation that later analysis called spurious.
    after: >-
      At n = 11 yes, against a published answer and with every number the rule consumed
      on the record. At n = 29 the rule refuses, and the refusal bounds the difficulty:
      no relation through degree twenty below `10^22` at a thousand digits.
  delegations: []
  outputs:
  - src/sqpack/promote/solve.py
  - src/sqpack/promote/system.py
  - devtools/probe_contact_system.py
  - devtools/probe_minimal_polynomial.py
  - tests/test_promote_solve.py
  - devtools/controls.yaml
  checks:
  - 'n = 11: degree 8, coefficients match Trump 1979, irreducible, discharged'
  - 'n = 11 margin rule: C=12420, B=36.85, M=200, residual 4.99e-338 at B+M and 3.38e-412 at 2B+2M'
  - 'n = 29: refined to 1000 digits, residual bound 1.09829e-1039'
  - 'n = 29: no relation at any degree 2..20 below 1e22, in 728.8s -- every degree empty, none refused by a clause'
  - 'uv run --frozen --group dev python -m devtools.run_negative_controls -k "minimal polynomial": 5 of 5 fire'
  stop_reason: >-
    Both phases reached their criteria inside the block clock, read from `date -u` at each
    boundary.
  next_action: >-
    Open block 9 as session-043 under BC-061 and `think-twa7`: an exact LP over certified
    coefficients, removing the `1e-11` float floor. The n = 29 refusal above is what makes
    the interval route the load-bearing one, so the layer that certifies its coefficients
    is the next thing that matters.
---
# session-042 — block 8, the exact route answers once and refuses once

Block 8 of [agenda-006](../agendas/agenda-006-overnight-research-blocks.md), and the
last of the missing middle layers.

## The rule, not the search

An integer-relation algorithm given `d + 1` unknown coefficients and enough digits
returns a relation whether or not one exists.
Ask for degree eight from a hundred digits and you get a degree-eight answer; ask for
twelve and you get one of those too.
So the deliverable is not the search — it is the rule that refuses most of its answers,
and the promotion spec froze that rule as three clauses rather than a caution.

With `C` the largest coefficient the relation *actually carries* and
`B = (d+1) log10(C)`:

1. the relative residual is below `10^-(B+M)`,
2. re-evaluated at `2B + 2M`, the residual keeps **falling** rather than resting near
   `10^-B`,
3. the value comes from a refinement whose *reported residual bound* is below
   `10^-(B+M)`.

Clause 2 is the cheap decisive one, and it is what the planning probe lacked.

## `n = 11`, against a published answer

Trump published the minimal polynomial of `s(11)` in 1979. The rule recovers it from
digits alone:

```
+1*s**8 -20*s**7 +178*s**6 -842*s**5 +1923*s**4 -496*s**3 -6754*s**2 +12420*s -6865

C = 12420    B = 36.85    M = 200
residual 4.99e-338 at B+M, 3.38e-412 at 2B+2M
irreducible over Q, 2 real roots, exactly one isolating the refined value
```

It came back **negated** on the first run, which is why the module normalises: a
relation is determined only up to a unit and a common factor, and an un-normalised
answer reads as a mismatch against a published one.

Fitting is also not minimality — any multiple of the minimal polynomial vanishes just as
well — so `discharge` adds irreducibility over `Q` and an isolating interval.
The square of Trump’s polynomial is refused by name.
What `discharge` does *not* do is rebuild the packing and re-verify it; that needs an
exact solve of every pose unknown, not the side alone, and the docstring says so rather
than letting the name imply otherwise.

## `n = 29`, and the refusal is the result

Refined to a thousand digits from the published closed system, with a reported residual
bound of `1.09829e-1039`:

```
no relation at any degree from 2 through 20, |c| < 1e22, in 728.8s
every degree: pslq returned nothing
```

Not one degree reached a clause.
The search found nothing to judge.

**That contrast is the finding.** The planning probe, on the ~98 serialized digits, got
relations at almost every degree from 8 to 21 — a search with more freedom than input.
Fed a thousand genuine digits, the same search falls silent everywhere.
A search that answers when under-fed and stops when fed properly is evidence about the
number rather than about the search, and what it bounds is concrete: **if `s(29)` is
algebraic of degree twenty or less, some coefficient of its minimal polynomial is at
least `10^22`.**

The spec anticipated this and said what it would mean — “a refusal here is a result: it
would say the minimal polynomial is large, which is itself worth knowing and is why the
interval route exists.”
It is now measured rather than anticipated.

## Two tools, because a measurement in a transcript is not replayable

Both of this run’s last two findings were first made in throwaway scripts.
That is the wrong place for a measurement that overturns something in the record, so
both are now devtools:

- **`devtools/probe_contact_system.py`** reports what each retained case’s assembled
  system determines, and `--walk` steps the side-changing null direction and reads the
  violation’s *order* in `t`. `O(t²)` is an ordinary second-order obstruction; `O(t)`
  means an equation is wrong.
  That distinction is the whole of [D-361](../../../defects.md) and it is now one
  command.
- **`devtools/probe_minimal_polynomial.py`** runs the search above and reports which
  clause decided each degree.
  The `n = 29` sweep takes twelve minutes, which is why it is a tool with a recorded
  result rather than a test.

Building the first surfaced [D-359](../../../defects.md)’s own bug inside it.
A rank verdict is a judgement about a gap between singular values, and the gap the SVD
can *see* is bounded by the precision it runs at: at mpmath’s ambient 15, Göbel’s
discarded singular value read `2.3e-16` against a counted `0.511`, where pinned at 50
digits it is `1.04e-51`. Same verdict, a gap thirty-five decades narrower than the
truth, and nothing in the output to tell them apart.
Precision is now pinned per case and printed next to the gap.

Reaching into `_symbols_by_name` from the tool was a signal that the module’s public
surface was short rather than a reason to suppress a lint, so `contact_jacobian` is
public now and both callers share it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
