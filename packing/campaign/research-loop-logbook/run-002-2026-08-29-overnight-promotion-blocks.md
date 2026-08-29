---
title: run-002 — an overnight run that built both promotion routes and certified s(29) by enclosure
softschema:
  contract: packing.squares:ResearchLoopLogEntry/v1
  schema: ../schemas/research-loop-log-entry.schema.yaml
  envelope: logbook_entry
  status: enforced
logbook_entry:
  id: run-002
  title: Ten bounded overnight blocks that built the promotion pipeline's missing middle
  date: '2026-08-29'
  status: stopped
  objective: >-
    Run one unattended overnight programme across three independent agenda-005 lanes, in
    blocks small enough that an interruption costs one block rather than the night, and
    leave every result in the artifact that owns it. The scientific target was the
    promotion problem at n = 29: whether a reported value can be certified without first
    recovering an exact algebraic form, and whether the exact route's missing middle can
    be built.
  source_sessions:
  - session-036
  - session-037
  - session-038
  - session-039
  - session-040
  - session-041
  - session-042
  - session-043
  - session-044
  primary_bead: think-qs6k
  source_branch: claude/squares-research-blocks-kqu96s
  source_commit: 295a5460fbb02a1ffb18f7ec7ac5b02f6ba57e4a
  timebox:
    target_wall_minutes: 1170
    cycle_minutes: 30
    planned_cycle_slots: 39
  rollup:
    session_count: 9
    phase_count: 32
    workflow_counts:
      pipeline-improvement: 19
      process-review: 10
      general-improvement: 1
      efficiency-loop: 1
      research-pass: 1
    phase_status_counts:
      completed: 31
      stopped: 1
    focus_counts:
      correctness: 21
      process: 9
      efficiency: 1
      insight: 1
    clock_role_counts:
      work: 23
      finalization: 9
    delegation_count: 5
    delegation_status_counts:
      completed: 5
    new_round_decision_counts: {}
  new_round_results: []
  prior_retained_results: []
  defects:
    opened_in_run: [D-356, D-357, D-358, D-359, D-360, D-361]
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
      run falsified. D-358 is this run misreading its own clock by about a factor of four
      and supplying a false reason for stopping early. D-359 is open: the generated atlas
      SVG's coordinate precision is inherited rather than pinned, so the check that its
      stored PNG is current passes on test ordering. D-360 is a null-space claim read off a
      filtered display instead of computed, caught before it was committed. D-361 is the
      one that mattered: an edge-edge contact assembled as one equation where collinearity
      is two, which made close() report four and seven missing "stationarity conditions"
      that were four and seven missing equations. None of the six is about the mathematics
      of packing.
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
  - name: reflected-pose-model
    status: built
    summary: >-
      A pose is a centre, an angle and a chirality. Seven of the n = 29 squares are placed
      by reflection, which no centre-plus-rotation can express; carrying the sign in the
      corner model takes the assembled residual from 2.0 to 1.3e-15 with n = 11 unmoved.
    paths:
    - packing/src/sqpack/promote/system.py
    - packing/src/sqpack/promote/contacts.py
    - packing/atlas/known-best/contact-structures.json
  - name: edge-edge-collinearity
    status: built
    summary: >-
      An edge-edge contact pins collinearity, which is two equations, not one. With the
      second the contact Jacobian reaches full rank at both retained sizes -- 34 of 34 at
      n = 11 and 88 of 88 at n = 29 -- and `close` refuses to add anything. The shortfall
      it had been reporting was this bug, recorded as D-361.
    paths:
    - packing/src/sqpack/promote/system.py
    - packing/tests/test_promote_system.py
  - name: minimal-polynomial-margin-rule
    status: built
    summary: >-
      The integer-relation step under the promotion spec's frozen three-clause rule, with a
      discharge that proves irreducibility over Q and isolates the root. Recovers Trump's
      published degree-eight polynomial at n = 11; returns nothing at any degree through
      twenty at n = 29.
    paths:
    - packing/src/sqpack/promote/solve.py
    - packing/tests/test_promote_solve.py
    - packing/devtools/probe_minimal_polynomial.py
  - name: symbolic-route-and-degree-bound
    status: built
    summary: >-
      The same six-equation transcription now serves floats, intervals and SymPy, so the
      n = 29 system rationalises over Q under the half-angle substitution. Total degrees
      [11, 15, 10, 15, 7, 6] give a Bezout bound of 1,039,500 -- which is what says the
      degree-twenty integer-relation refusal surveyed a corner of the space.
    paths:
    - packing/src/sqpack/promote/interval.py
    - packing/devtools/probe_system_degree.py
    - packing/tests/test_promote_system_degree.py
  - name: pipeline-probes
    status: built
    summary: >-
      Three devtools, because two of this run's findings were first made in throwaway
      scripts and one of those scripts was wrong. They report what an assembled system
      determines, what the margin rule made of a search, and what bounds the degree.
      Documented in development.md so they are reached for before a one-off script.
    paths:
    - packing/devtools/probe_contact_system.py
    - packing/devtools/probe_minimal_polynomial.py
    - packing/devtools/probe_system_degree.py
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
    negative_controls: 113
    note: >-
      Twenty-seven controls added across the run, 86 to 113, each watched to fire before
      being registered. Five were written and withdrawn as unable to fire -- three for the
      n = 29 chain under D-356, one faking `side_leak` to zero when the truth is zero
      everywhere, and one mutating a coefficient that `Poly.from_dict(domain=QQ)` coerces
      back. Several others needed retargeting against what the mutation actually reports,
      which is why each is watched rather than assumed.
  - scope: n29-interval-certificate
    command: uv run --frozen python -m cases.kingbird29.certify_interval
    status: passed
    note: >-
      406 pairs tested, 406 strictly separated, none undecided, at a declared relaxation of
      1e-20. Recorded unresolved with needs_review; no runner may promote it.
  next_action: >-
    Resume at agenda-006 block 11, `BC-066` under `think-obgk`: eliminate the five-unknown
    system that BC-065 left, and record whatever the chain reaches inside a declared cap.
    It is first because it is the only remaining block that can change what this run
    concludes about n = 29; everything after it improves the pipeline. The full ordering
    through block 18 is the continuation schedule in agenda-006, and the endpoint check
    BC-064 is reserved and may not be borrowed from. Separately and not a runner's
    decision: whether the n = 29 interval certificate moves verified_upper_bound. It is
    retained, unpromoted, and 5.23371e-5 below the standing ceiling.

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
substitution; it is stronger, and at `n = 29` this run measured *why* it does not reach.
A sweep under the promotion spec’s frozen margin rule, on a thousand manufactured
digits, returns no relation at any degree through twenty below `10^22` — and the
rationalised system bounds the solution variety at `1,039,500`, so degree twenty was a
corner of the space rather than a survey of it.
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

The fast gate was run and left green at every block checkpoint; the full strict gate was
run once at the block-5 endpoint.
Negative controls rose from 86 to 113, each watched to fire before registration — and
five were written and then withdrawn as unable to fire, which is the same discipline
pointing the other way.

The consumer contract on `verified_upper_bound` caught four of this run’s session
records before they landed, each time for naming the field in a stop condition without
declaring what the record takes it to mean.
That is friction working as designed.

Two environment facts, recorded because they cost time and will cost it again: the
container needed Python 3.14.7 installed through a newer `uv` than it shipped with, and
`git fetch --unshallow`, without which the provenance step fails on an unreachable
engine commit.

## Claim Boundary and Next Action

The `n = 29` certificate proves an upper bound at a declared relaxation and nothing
more. It is not the optimum, not an optimality result, and not promoted.
`verified_upper_bound` is where it was.

The next action is a human one — whether that bound moves.
It is not a runner’s to make.

## The continuation, in session 044

Eleven commitments, all terminal, in a session that reached its last research block with
over two hours of wall budget unspent — which is why `BC-070`, `BC-071`, `BC-072` and
`BC-073` exist at all: they are the remainder spent on the question rather than an early
finish.

| Block | Commitment | Outcome |
| ---: | --- | --- |
| 11 | `BC-066` — eliminate the five-unknown system | A measured wall. OOM at degree 32, `13.8 GB`; swell is not the cause |
| 12 | `BC-070` — bound the degree without a basis | `15,744` by mixed volume, sixty-six times tighter than Bézout |
| 13 | `BC-067` — the `n = 11` round trip | Closed. Reconstructed side exactly the field generator |
| 14 | `BC-068` — pin the atlas emission (`D-359`) | Fixed; no stored artifact changed a byte |
| 15 | `BC-069` — the one `n = 5` condition | Rank `16/16`; the promised form could not have closed it (`D-363`) |
| 16 | `BC-061` — exact LP over certified coefficients | Optimum exact; `ambiguous` empty |
| 17 | `BC-071` — phase 1 of that LP | First vertex from the cell’s own coefficients, no float solver |
| 18 | `BC-063` — first-party `n = 5` rigidity | Infinitesimally flexible, second-order rigid |
| 19 | `BC-072` — retrack at higher precision | Every path labelled; the count still refused, for a narrower reason |
| 20 | `BC-073` — the sweep’s true reach | Refusal carries from degree 20 to 29; `D-364` found on the way |
| 21 | `BC-064` — endpoint check | Two strict failures: `D-365` pre-existing, `D-366` this session’s |
| — | `BC-062` — reachability-scoped verification | Stopped deliberately; a measurement block on a contended machine |

**What the continuation was for, and what it settled.** The exact route’s every layer
below the field is now built and exercised end to end at `n = 11`. At `n = 29` the
degree bound falls from `1,039,500` to `15,744` and the relation refusal carries from
degree 20 to 29. The field itself remains out of reach — but out of reach *measured*
rather than assumed, which is the difference between a gap and a wall.

**Five record defects a cold start inherits** were found by picking this branch up in a
fresh container and following its own instructions: five bootstrap commands that do not
run, a dangling `agenda-007`, four beads carrying pre-renumbering ids, a bead closed
with a reason `D-358` retracts, and a commit hook that was not installed.
All repaired.

A sixth was reported and then retracted, and the retraction is the more useful half.
Two beads the agenda names were written up as never created, on the strength of
`tbd show` reporting them missing.
They existed the whole time on the shared `tbd-sync` branch; this container’s freshly
materialized local store did not have them, and an unsynced bead is reported as missing
rather than as unsynced.
The duplicates that mistake created are closed against the originals, and the gate is
what caught it — `check_bead_tree` refuses two open beads sharing a title.
The lesson that survives is narrower: a local bead store can be silently stale, so “the
bead does not exist” is a claim that needs a sync behind it.

**Four defects opened.** `D-362` and `D-365` are checks that passed for a reason other
than the one they state; `D-363` is a closure form named in the record that could not
close the case it was named for; `D-364` is the margin rule counting digits the value
does not carry — flattering, and never fired, because no sweep had gone past twenty.
`D-366` is this session’s own cost regression in the control suite.

## Where to resume

**Start at
[agenda-006’s continuation schedule](../agendas/agenda-006-overnight-research-blocks.md#the-continuation-schedule).**
Blocks 1–10 closed in this run; the continuation blocks closed in
[session 044](../agent-sessions/session-044-agenda006-continuation.md).

### Where the exact route stands, in one place

This is the thing hardest to reconstruct from the diff, because the answer is a shape
rather than a result.

**Every layer downstream of the field is now built.** Contact extraction, system
assembly, chirality in the pose model, the `edge-edge` collinearity repair, closure at
all three retained sizes, minimal-polynomial recovery under the frozen margin rule,
irreducibility and root isolation, the round trip back to a verified packing, an exact
LP over certified coefficients, and phase 1 of that LP so it needs no float starting
vertex. At `n = 11`, where the field is published, the chain runs end to end and returns
the published side with a difference of exactly zero.

**The one missing piece is the field itself at `n = 29`, and everything is blocked
behind it.** The exact LP cannot be pointed at `n = 29` for the same reason the round
trip cannot: `fixed_cell_lp` needs exact coordinates, exact coordinates need an
algebraic number field, and there is no minimal polynomial for `s(29)` to build one
from.
Assembling the `n = 29` contact system as an LP is therefore not the next block; it
is the same block wearing different clothes.

**And that missing piece has now been measured twice rather than assumed.** `BC-060`
found no integer relation through degree twenty below `10^22` on a thousand digits.
`BC-066` found that Gröbner elimination does not reach an eliminant on this hardware,
and — more usefully — that coefficient swell is *not* what stops it: over `F_p`, where a
coefficient is one machine word, the matrices reach the same dimensions and the cheapest
monomial order still does not terminate, so what is being measured is the size of the
ideal.
`BC-070` then bounded the degree of the Kingbird solution at **`15,744`** by mixed
volume, down from Bézout’s `1,039,500`, which is a sixty-sixfold improvement and still
far beyond what an integer-relation search reaches.

So the honest state is: the pipeline is finished and the number is not available.
A route that produces the minimal polynomial of `s(29)` — or a proof that its degree is
large enough to close the question — is the whole of what remains, and the interval
certificate carries the bound in the meantime for a reason that is now measured.

`BC-064`, the endpoint check, is reserved and may not be borrowed from.

What a fresh agent needs to know that is not obvious from the diff:

- **Read block boundaries from `date -u`.** This run misread its own clock by about a
  factor of four ([D-358](../../../defects.md)) and the practice change has caught a
  wrong estimate twice since.
- **A cited measurement goes in a tool, not a transcript.** Two findings here were first
  made in throwaway scripts and one of those was wrong;
  `devtools/probe_contact_system.py`, `probe_minimal_polynomial.py` and
  `probe_system_degree.py` exist for that reason and are documented in `development.md`.
- **Every block owes the five things listed in the agenda** — merge `origin/main`,
  `tbd sync`, commit and push and update the PR, leave the gate green or name the
  failure, and record the result in the artifact that owns it.
- **A refusal is a result.** Three of this run’s most useful findings are refusals, and
  none of them was reached by loosening anything.
- **`verified_upper_bound` may not be moved by a runner**, and any record that names the
  field must declare what it takes it to mean or the gate will refuse it.

### What `BC-066` would and would not buy

Worth knowing before spending a block on it, because the instinct that elimination is
the “real” answer is right about rigour and easy to over-read about consequence.

Writing the system down is **not** the hard part and is already done, twice: our own
assembly from the contact topology (122 equations in 88 unknowns, full rank, residual
`1.3e-15`) and the source’s own six-equation system, which is itself the product of a
large hand-elimination — Kingbird expressed all twenty-nine poses in six parameters.
Rationalised, that is six polynomials over `Q`, and five after `s` is solved out.
The wall is the elimination, not the transcription.

Elimination is also genuinely **less error-prone** than integer relation, and that is
the honest argument for it.
Integer relation is guess-and-check: `pslq` emits candidates and the margin rule filters
them, so the rule carries all the epistemic weight.
Elimination is a derivation — exact by construction, with no margin, no precision
question, and nothing to be fooled by.

But a complete success upgrades the `n = 29` **upper bound** from “certified at a
relaxation of `1e-20`” to “exactly this algebraic number”.
It says nothing about optimality.
The bound gap of about `0.46` at `n = 29` is untouched either way, and so is the
question of whether Kingbird’s packing is the best one.
Do the block for exactness and for making the pipeline general at sizes with no
published system — not as a route to a larger theorem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
