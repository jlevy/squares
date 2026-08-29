---
title: run-002 — an overnight run that built both promotion routes and certified s(29) by enclosure
softschema:
  contract: packing.squares:ResearchLoopLogEntry/v1
  schema: ../schemas/research-loop-log-entry.schema.yaml
  envelope: logbook_entry
  status: enforced
logbook_entry:
  id: run-002
  title: Four bounded overnight blocks across the interval and exact promotion routes
  date: '2026-08-29'
  status: stopped
  objective: >-
    Run one unattended overnight programme across three independent agenda-005 lanes, in
    blocks small enough that an interruption costs one block rather than the night, and
    leave every result in the artifact that owns it. The scientific target was the
    promotion problem at n = 29: whether a reported value can be certified without first
    recovering an exact algebraic form, and whether the exact route's missing middle can
    be built.
  source_sessions: [session-036, session-037, session-038]
  primary_bead: think-qs6k
  source_branch: claude/squares-research-blocks-kqu96s
  source_commit: 90b74afd517cb29fab21898088a5d2536c70cdcf
  timebox:
    target_wall_minutes: 690
    cycle_minutes: 30
    planned_cycle_slots: 23
  rollup:
    session_count: 3
    phase_count: 9
    workflow_counts:
      pipeline-improvement: 6
      process-review: 3
    phase_status_counts:
      completed: 9
    focus_counts:
      correctness: 6
      process: 3
    clock_role_counts:
      work: 6
      finalization: 3
    delegation_count: 0
    delegation_status_counts: {}
    new_round_decision_counts: {}
  new_round_results: []
  prior_retained_results: []
  defects:
    opened_in_run: [D-356, D-357]
    preexisting_relevant: []
    note: >-
      Both concern the negative-control harness rather than the mathematics. D-356 records
      that the harness prunes the literature archive from its snapshot, so the n = 29 chain
      -- whose input is an archived SVG -- cannot be mutation-controlled there; three
      controls written for it were withdrawn and their guards asserted directly in the test
      instead. D-357 is a correction of this run's own record: a synopsis control failed
      four times running, including against a stashed clean tree, and was first written up
      as a standing failure; it later fired correctly with nothing changed, so the entry now
      says plainly that the trigger is not identified rather than keeping a claim a later
      run falsified.
  pipeline_changes:
  - name: interval-certification
    status: built
    summary: >-
      The interval route, end to end. Outward-rounded interval scalars over mpmath.iv with
      a sign that refuses on a straddling enclosure; forward-mode automatic differentiation
      so the Jacobian is enclosed over a box rather than differenced at a point; the
      Krawczyk operator with existence and uniqueness reported separately; the layout map
      to outward-rounded corner boxes; and a separating-axis test whose three verdicts --
      separated, overlapping, undecided -- are kept apart.
    paths:
    - packing/src/sqpack/promote/interval.py
    - packing/src/sqpack/promote/krawczyk.py
    - packing/src/sqpack/promote/enclose.py
    - packing/src/sqpack/promote/interval_verify.py
    - packing/tests/test_promote_krawczyk.py
    - packing/tests/test_promote_interval_verify.py
  - name: relaxation-bound
    status: built
    summary: >-
      A certified upper bound at a declared relaxation, which is what makes the interval
      route usable on a tight packing at all. Scaling centres apart by 1 + eps leaves every
      square exactly unit and oriented, moves nothing toward the origin, and strictly opens
      every contact; the bound is read off the relaxed corners rather than supplied, so it
      cannot be inflated until verification passes.
    paths:
    - packing/src/sqpack/promote/relax.py
    - packing/tests/test_promote_relax.py
  - name: kingbird29-symbolic-layout
    status: built
    summary: >-
      The n = 29 layout as a function of the unknowns rather than of the printed digits,
      using the source's own transforms with entity references kept as markers until
      evaluation, plus an equivalence check against the existing numeric walk.
    paths:
    - packing/cases/kingbird29/layout.py
    - packing/cases/kingbird29/certify_interval.py
  - name: contact-system-assembly
    status: built
    summary: >-
      The exact route's missing middle. Contact extraction now identifies which features
      realise each contact, and assembly turns a structure into scalar equations whose
      closure is sized by the measured rank shortfall rather than by counting rows.
    paths:
    - packing/src/sqpack/promote/system.py
    - packing/src/sqpack/promote/contacts.py
    - packing/tests/test_promote_system.py
    - packing/atlas/known-best/contact-structure.schema.yaml
  validation:
  - scope: fast-gate
    command: uv run --frozen --all-extras --group dev packing-validate --fast
    status: passed
    steps: 16
    wall_seconds: 239
    note: >-
      Run and left green at each of the three block checkpoints. The measured baseline on
      this container is 4m15s, dominated by roughly 250s of behavioural tests against 40s
      of soft-schema validation and 30s of lint.
  - scope: negative-controls
    command: uv run --frozen --group dev python -m devtools.run_negative_controls
    status: passed
    negative_controls: 97
    note: >-
      Eleven controls added across the run, 86 to 97, each watched to fire before being
      registered. Three further controls for the n = 29 chain were written and withdrawn
      under D-356.
  - scope: n29-interval-certificate
    command: uv run --frozen python -m cases.kingbird29.certify_interval
    status: passed
    note: >-
      406 pairs tested, 406 strictly separated, none undecided, at a declared relaxation of
      1e-20. Recorded unresolved with needs_review; no runner may promote it.
  next_action: >-
    A human decision, not a runner's: whether the n = 29 interval certificate moves
    verified_upper_bound. It is retained, unpromoted, and 5.23371e-5 below the standing
    ceiling. After that, the queue is BC-051 and BC-049 in agenda-005 -- neither was run
    here -- and the two questions block 3 left open: deriving the determinant conditions
    the rank shortfall calls for, and giving the pose model a chirality so reflected
    layouts can be assembled.
---
# run-002 — an overnight run across both promotion routes

## Context

`s(n)` is the smallest square that holds `n` unit squares.
For most `n` the best known packing is a *reported* number: someone found an
arrangement, published its coordinates, and nobody has independently proved that the
arrangement is even valid, let alone optimal.
This repository separates those claims — `reported_upper_bound` is what a source says,
`verified_upper_bound` is what has been checked here or replayed from a public
certificate — and the gap between them at `n = 29` was the subject of this run.

Verifying a packing exactly is harder than it sounds, and the reason is the whole
argument for the machinery below.
A tight packing has pairs of squares touching at *exactly* zero separation.
Floating point can certify a strict inequality and can never certify an equality: any
tolerance loose enough to accept a true contact also accepts an overlap smaller than
itself, and a tolerance of zero rejects the valid packing outright.
So a real certificate needs either exact algebra or rigorous enclosures.

Two routes lead there.
The **exact route** recovers the packing’s minimal polynomial and discharges it by exact
substitution; it is stronger, and at `n = 29` it is stalled, because a sweep recorded in
`X-004` found no integer relation through degree twenty with coefficients below `10^22`.
The **interval route** proves that a root exists and is unique inside a box and checks
separation on enclosures; it never needs the polynomial.
This run built both.

## Outcome

Both routes moved, and one produced a result.

At `n = 29` the interval route now certifies

```
s(29) <= 5.93383346267692918974379895098      (eps = 1e-20, 406 pairs, none undecided)
```

which sits `5.23371e-5` below the standing verified ceiling — the gap
`plan-2026-08-28-interval-certification` names as closable by no amount of better
sourcing, because no public certificate exists.

**Nothing in this run promoted it.** It is retained `unresolved` with
`needs_review: true`, `frontier/` was not written to, and `exact_verify` still raises
`checker-not-built` because no witness branch was written.
Whether the ceiling moves is a reviewed human decision through the evidence contract.

The claim is also narrower than it looks: an upper bound at a *declared relaxation*, not
a statement about the optimum, and not an optimality result — the `n = 29` bound gap of
about `0.46` is untouched.

## Run Rollup

Three sessions, nine phases, no delegations.
Four blocks were planned; three ran.

| Block | Commitment | State |
| --- | --- | --- |
| 1 | `BC-052` — interval arithmetic and the Krawczyk operator | complete |
| 2 | `BC-053` — calibration, then `n = 29` | complete |
| 3 | `BC-054` — contact features and system assembly | complete |
| 4 | `BC-055` — reachability-scoped verification, `n = 5` rigidity | **not run** |

Blocks 2 and 3 each overran into the slack block 4 was placed last to absorb, which is
what the slack was for.
At the boundary the choice was between a rushed change to the shared verification gate
and a real endpoint check; the endpoint check won.
`BC-055` is recorded `stopped` rather than left `ready`, so the queue does not imply
work this run did not do.

## Phase History

Every block ran two work phases and one finalization phase, all `pipeline-improvement`
with a `correctness` focus except the finalization phases, which are `process-review`.
No phase was stopped and none overran its own declared deadline; the overruns were of
block boundaries, taken from the following block’s budget.

## Results

### New Scientific Results From This Run

No `exp-NNN` rounds were opened.
This was `pipeline-improvement` work throughout: it built instruments and measured their
behaviour, and the measurements below belong to the session records rather than to
preregistered rounds.
The `n = 29` certificate is a retained result awaiting review, not an accepted round.

### Prior Retained Results Used or Rechecked

None were replayed against their own criteria.
Two prior *artifacts* were used as known answers and are worth naming even though
neither is an experiment record: Trump’s exactly verified `n = 11` packing, and the
`n = 29` contact structure BC-042 froze in session-035.

## What Worked

**Calibrating against implementations that share no code.** Both soundness bugs found in
block 1 were caught by the known-answer check rather than by reading the code, and both
pointed the flattering way.
Certificate endpoints were being serialized by rounding *to nearest*, which at 40 digits
lifts both ends of `sqrt(2)`'s box above `sqrt(2)` — the operator proved something true
and then wrote down something false.
And the operator reported its last iteration rather than the verdict it had *proved*,
discarding a uniqueness result obtained two iterations earlier once contraction drove
the box tight enough that rounding widened `K(X)` past `X`.

**Checking discrimination, not just agreement.** A checker that returned “valid”
unconditionally would pass every agreement test in block 2. So the same packings were
pushed into infeasibility by amounts no float check can see: an overlap of `1e-30` is
*proved* by the interval route and reported **valid** by `float_sign(1e-9)`.

**Two routes meeting.** Verified unrelaxed, the interval chain cannot decide exactly 52
pairs of the `n = 29` packing — and those are precisely the 52 pair contacts BC-042
extracted by an entirely different method.
Neither was built to agree with the other.

## What Did Not Work

**The spec’s reusable seam.** `verify_packing` takes an injected `sign`, and the
interval one was expected to drop in.
Measured, it refuses on a layout with a tenth of a unit of clearance on every pair,
because the projection step orders enclosures that overlap and the separation step folds
four axes together so one undecided sign discards a pair another axis separates
strictly. The fold is reimplemented; the geometry is still shared.

**Counting rows.** The promotion spec’s phase-2 control asks for the unclosed contact
system to be reported underdetermined.
At `n = 11` it is overdetermined by the count — 35 equations against 34 unknowns — and
four conditions short by the rank, at the same time.
That control cannot fire as written, and closure is sized by the shortfall instead.

**Angle identities.** Angle classes hold modulo ninety degrees, so `t_i = t_j` is false
for a class member a quarter or half turn from another.
Emitting them left `n = 11` at the noise floor — its classes happen to have equal angles
— and drove `n = 29` to a residual of exactly `pi`.

**Assembling `n = 29`.** Seven of its twenty-nine squares are built inside `scale(-1 1)`
mirror groups and have clockwise corner winding, which a centre-plus-rotation pose
cannot produce.
Assembly refuses them by name rather than describing their mirror images.
That is a limitation, not a result, and it is the block’s clearest open question.

## Pipeline Changes

Four, all built: the interval-certification stack, the relaxation bound, the `n = 29`
symbolic layout, and contact-system assembly.
The frontmatter above lists their paths.

## Defects Affecting This Run

`D-356` and `D-357`, both about the negative-control harness and neither about the
mathematics. The second is a correction of this run’s own first write-up, which is the
more useful half: a control that failed four times running, including on a clean tree,
later fired correctly with nothing changed, and the entry now says the trigger is
unidentified rather than keeping the claim that it could not fire.

## Validation

The fast gate was run and left green at all three block checkpoints; the full strict
gate was run once at the endpoint.
Negative controls rose from 86 to 97, each watched to fire before registration.

Two environment facts, recorded because they cost time and will cost it again: the
container needed Python 3.14.7 installed through a newer `uv` than it shipped with, and
`git fetch --unshallow`, without which the provenance step fails on an unreachable
engine commit.

## Claim Boundary and Next Action

The `n = 29` certificate proves an upper bound at a declared relaxation and nothing
more. It is not the optimum, not an optimality result, and not promoted.
`verified_upper_bound` is where it was.

The next action is a human one — whether that bound moves — and after it the queue is
`BC-051` and `BC-049`, neither run here, and the two questions block 3 left open:
deriving the determinant conditions the rank shortfall calls for, and giving the pose
model a chirality so reflected layouts can be assembled.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
