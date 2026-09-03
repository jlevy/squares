---
title: exp-058 — H-060 chart, constraint accounting and order-2m coefficient proof at n = 5
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-058
  series: series-000
  title: >-
    Test H-060's preregistered neighbourhood, curve-selection and coefficient criterion in
    one intrinsic half-angle chart at Goebel's exact n = 5 side
  date: '2026-09-03'
  hypotheses:
  - H-060
  tier: confirmatory
  subject:
    label: >-
      exact fixed-side local isolation of Goebel's labeled n = 5 pose, over Q(sqrt 2), in
      one intrinsic half-angle chart
    engine: >-
      BC-152 chart-and-proof replay set 1.0.0 (seven sympy scripts, retained verbatim in
      this round's results record); read-only against the repository
    assurance: verified
    method: exact-algebraic
    host_system: linux x86_64, Python 3.14.7, sympy 1.14.0
    selftest_passed: false
  instance:
    axis: n
    point: 5
    role: target
  method:
    control: >-
      T-012's retained certificate record bc-049-n5-rigidity-certificates.json and X-007,
      both held fixed and neither edited; the pose read corner-for-corner out of
      cases/gobel5; the C8 exp-034 specificity control, pre-run here through the T-012
      machinery and then decided exactly on container side; and the seven remaining
      declared controls C1-C7, which are specified in the proof artifact and belong to the
      W7 instrument phase rather than to this round. That instrument was built after this
      packet was frozen and exercises all eight there; its readiness review has not passed
    candidate: >-
      an intrinsic half-angle chart Phi on R^15, injective everywhere, with cleared
      denominators 1 + t_i^2 >= 1 and second-jet transform J = diag(1, 1, 2) per square; a
      complete exact accounting of all 400 elementary wall-corner and pair inequalities at
      the pose; a neighbourhood N cut out by 128 strict sign conditions on which the local
      feasible system is exactly the 20 active rows; and an induction on the Taylor
      coefficients of a putative nonconstant analytic feasible arc through order 2m
    runs_per_condition: 1
    interleaved: false
    operator: Claude (agent), BC-152 n = 5 proof lane of agenda-016, bead think-760r
    entry_point: >-
      campaign/series/series-000-smoke-and-calibration/results/exp-058-h-060-n5-chart-and-proof.json,
      whose replay_scripts block holds the verbatim source and SHA-256 of the seven scripts
      this round built. The round built no repository code. The executable form of this
      mathematics was built after the freeze, at 6580a9fd, as the package
      src/sqpack/local_rigidity/, which binds to devtools/assess_n5_rigidity.py rather than
      extending it as W7's text asks; it is not this round's evidence, and its readiness
      review has not passed
    command: >-
      cd packing && mkdir -p /tmp/replay058 && .venv/bin/python3 -c "import json,pathlib;
      r=json.loads(pathlib.Path('campaign/series/series-000-smoke-and-calibration/results/exp-058-h-060-n5-chart-and-proof.json').read_text());
      [pathlib.Path('/tmp/replay058',s['name']).write_text(s['source']) for s in
      r['replay_scripts']['scripts']]" && cd /tmp/replay058 && for f in verify_chart.py
      margins.py midpoint_check.py control_exp034.py c8_side_check.py sosc_check.py; do
      /home/user/squares/packing/.venv/bin/python3 $f; done &&
      /home/user/squares/packing/.venv/bin/python3 print_polys.py verify_chart.py
    budget: >-
      agenda-016 BC-152 allots 360 elapsed minutes in the n = 5 lane; the frozen packet
      declares itself phase 0-105, mathematics rather than code. No command was run during
      the 105-165 repository-wide quiet lease. Stop before any accept determination on a
      missing readiness checkpoint, an unverified theorem hypothesis, or an incomplete
      neighbourhood obligation, and leave H-060 unresolved rather than widen the claim
    record: campaign/series/series-000-smoke-and-calibration/results/exp-058-h-060-n5-chart-and-proof.json
  effort:
    timebox: >-
      the 360-minute BC-152 n = 5 lane of agenda-016, of which this record covers the
      packet's declared phase 0-105 plus its freeze
    wall_seconds: 11.33
    stopped_by: dependency
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes:
    - >-
      a paper proof can be exactly replayed and still not be an instrument receipt, so a
      reader who sees "verified" on the subject may read it as a disposition of H-060
    - >-
      a corroborating second proof with weaker hypotheses can be mistaken for the
      acceptance route and used to retire an obligation it does not discharge
    notes: >-
      No repository code changed. The seven replay scripts are retained as raw run data in
      this round's results record rather than installed as tooling: nothing under campaign/
      is code, and the W7 instrument they would become belongs to a separate lane.
      effort.agent_minutes is deliberately absent rather than estimated: the packet lane's
      own operator time was not recorded before the freeze, and a number invented at
      integration time would price the next round against a guess.
  results:
  - shape: determination
    question: >-
      Is Goebel's exact labeled n = 5 pose an isolated point of Feas(2 + sqrt(2)/2) under
      H-060's registered criterion, which accepts only on a CHECKED chart accounting for
      the entire local feasible set and a REVIEWED curve-selection and coefficient
      argument?
    role: outcome
    outcome: no_progress
    checked_by: >-
      nothing that the criterion accepts. The mathematics of the registered route is
      complete on paper and every exact quantity in it replays, but no instrument checked
      the chart and no independent reviewer has read the argument, so neither accept
      condition is satisfied; and no nonconstant feasible arc through the pose and no exact
      sequence of distinct feasible poses converging to it was found, so the reject clause
      is not satisfied either. Validly undecided, in exp-045's sense: a finite named
      obligation remains, so the determination is no_progress and the verdict is unresolved
  - shape: determination
    question: >-
      Do the chart's cleared polynomials, their gradients and their second jets bind
      exactly to T-012's A and q under the declared coordinate transform and positive row
      scalings?
    role: mechanism
    outcome: criterion_met
    checked_by: >-
      verify_chart.py, in sympy over Q(sqrt 2) and independent of sqpack.field:
      A_chart = A_geo J with J = diag(1, 1, 2) per square, H_chart = J^T H_geo J on all
      twenty rows with no second-order angle correction, q_chart = 4 q_geo (-2 on the four
      pair rows, 0 on the sixteen wall rows), each pair polynomial restricted to the flex
      line exactly -t4^2, column t4 of A_chart identically zero, all 28 retained Farkas
      certificates replaying on S A_chart to pin the other 14 coordinates, and the
      self-stress replaying with w . q_chart = -2 sqrt 2 < 0
  - shape: determination
    question: >-
      Do the exact base margins at the pose reproduce the agenda's declared 16/64
      wall-corner and 4/6 pair counts, with every one of the 400 elementary functions
      evaluated?
    role: guard
    outcome: criterion_met
    checked_by: >-
      verify_chart.py and margins.py: 16 vanishing and 64 strictly positive wall-corner
      functions with minimum inactive margin 1 - sqrt(2)/4, 4 touching and 6 noncontact
      pairs over 320 pair functions, least negative violated-branch witness -sqrt(2)/4. No
      discrepancy with the agenda's counts was found. midpoint_check.py puts all four
      active pair corners at along-edge parameter exactly 1/2, so no D-390 endpoint
      incidence arises, and exactly one branch is satisfied per touching pair, so no D-391
      disjunction arises
  - shape: determination
    question: >-
      Given the Nash curve selection lemma as cited -- quoted verbatim in the words of one
      of BCR's own authors, in notes he describes as provisional, and applied verbatim in
      four papers by a single author group -- does the order-2m coefficient induction close?
    role: mechanism
    outcome: criterion_met
    checked_by: >-
      the proof artifact's Lemmas 7-8 and Theorem 9, with every sign explicit and every
      exact quantity replayed. The hypothesis is conditional and stays conditional: the
      printed BCR text was not available in this environment, so the lemma's statement is
      cited rather than confirmed against a primary source, and confirming it is this
      round's single largest remaining proof obligation
  - shape: determination
    question: >-
      Is the exp-034 exact fixed-side angle-and-slide family, the one place a nonconstant
      feasible arc is known to exist, outside Feas(2 + sqrt(2)/2) and therefore not a
      refutation of H-060?
    role: guard
    outcome: criterion_met
    checked_by: >-
      c8_side_check.py through sqpack.verify: the family is valid at side 1 + 5 sqrt(2)/4
      and invalid at Goebel's side for every sampled u, its square 1 overshooting the wall
      by exactly 3 sqrt(2)/4 - 1 > 0, so the two feasible sets are disjoint and the family
      is at positive distance from the pose. control_exp034.py separately shows the cone is
      open there, which is what the unbuilt instrument's C8 refusal will have to reproduce
  verdict:
    decision: unresolved
    needs_review: true
    primary_criterion: >-
      H-060's registered direction, which is frozen and was not amended for this round:
      accept only if a checked intrinsic semialgebraic chart accounts for the entire local
      feasible set, its polynomial derivatives bind exactly to the first- and second-order
      certificates, and a reviewed curve-selection and coefficient argument excludes every
      nonconstant feasible arc; reject only on a verified nonconstant feasible arc through
      the pose or an exact sequence of distinct feasible poses converging to it; otherwise
      unresolved
    reason: >-
      Both accept conditions are unmet and both reject conditions are absent, so the only
      honest disposition is unresolved. The chart is not CHECKED in the criterion's sense --
      every number in it was computed by scratchpad sympy, not by a repository instrument.
      A W7 instrument was built after this packet was frozen, at 6580a9fd, as the package
      sqpack.local_rigidity binding to devtools.assess_n5_rigidity rather than extending it;
      it self-reports instrument_ready with isolation_decided false and it does exercise the
      eight controls C1-C8. Its independent readiness review returned BOUNDED-CAVEAT and not
      a pass, because two of the eight registered controls, C1 changed_feature and C4
      invented_contact, could not fail and never reached the refusal path; the repair landed
      at 609e7392, a re-review verified it by removal and returned BOUNDED-CAVEAT again, a
      pass conditional on one unclosed provenance item -- the digested payload pins commit
      2f112f4c, which cannot produce the recorded digest. So H-060 keeps instrument_ready
      false because that review has not passed, not because nothing was built. The argument
      is not REVIEWED -- BC-153 has not run -- and its curve-selection step rests on
      quotations rather than on BCR Proposition 8.1.13 itself: one of BCR's own authors, in
      self-described provisional notes, plus four verbatim uses by a single author group.
      The packet's second secondary source was withdrawn from X-012 as an over-attribution,
      so no independent corroborating source stands behind the citation. The
      corroborating second-order-sufficiency proof recorded in the artifact reaches the
      same conclusion from strictly weaker hypotheses, but acceptance was preregistered on
      the curve-selection route, so it discharges nothing. What this round does establish
      is that the mathematics of the registered route is complete on paper and replays
      exactly, that the agenda's constraint counts are confirmed with no discrepancy, and
      that the one known nonconstant feasible arc lives at a different container side
    reopen_when: >-
      the W7 instrument's readiness review passes -- it emits a neighbourhood receipt for
      this chart, refuses all eight controls substantively, and pins the commit that
      produces its digest -- and a reviewer confirms the curve-selection statement against a
      primary text; either alone leaves the round where it is
    resume_from: >-
      the frozen packet installed as X-012, SHA-256
      28343b743e689fc99968d589a542d9022d061de8ec3ae5100bf4ef4930e40b6b, together with the
      seven replay scripts retained verbatim in this round's results record
---
# exp-058 — H-060 Chart, Constraint Accounting and Order-`2m` Coefficient Proof

`BC-152` asked whether Goebel’s exact `n = 5` optimum is locally rigid at fixed side under
`H-060`’s preregistered criterion.
This round is the mathematics of that lane, frozen.
The argument itself is the proof artifact,
[`X-012`](../../../explorations/X-012-one-chart-four-hundred-inequalities-and-an-order-2m-contradiction.md);
this record is the round that produced it, and the two must be read together.

## What Was Established

Four things, all replayed exactly and none of them a disposition of `H-060`.

**One chart, and no correction term.** An intrinsic half-angle chart on `R^15`, injective
on all of it rather than on some unstated neighbourhood, with cleared denominators
`1 + t_i^2 >= 1` everywhere.
Its second-jet transfer is `J = diag(1, 1, 2)` per square with `Hess Phi(0) = 0`, so there
is no second-order angle correction to carry — which is the reason the coefficient
induction can evaluate Hessians on `e_{t4}` alone.

**The whole constraint system, counted rather than assumed.** All 400 elementary
polynomial inequalities that define a valid packing at side `2 + sqrt(2)/2` were evaluated
in `Q(sqrt 2)` and classified by exact sign: 80 wall-corner functions split 16 active and
64 strictly positive with minimum inactive margin `1 - sqrt(2)/4`, and 320 pair functions
over 10 pairs split 4 touching and 6 noncontact.
The agenda’s declared 16/64 and 4/6 counts are confirmed independently and no discrepancy
was found.
On a neighbourhood cut out by 128 strict sign conditions, the local feasible system is
exactly the 20 active rows.
`D-390`’s endpoint incidence and `D-391`’s disjunction are excluded by computation rather
than by argument: every active pair corner sits at along-edge parameter exactly `1/2`, and
exactly one branch is satisfied per touching pair.

**T-012 transfers.** All 28 Farkas certificates and the self-stress replay on the chart
rows, giving `A_chart = A_geo J`, `q_chart = -2` on the pair rows, and
`w . q_chart = -2 sqrt 2 < 0`.

**The induction closes, conditionally.** Given the cited curve selection lemma, no
nonconstant analytic feasible arc through the pose exists, because every coefficient below
order `2m` is forced into the flex line’s kernel and the self-stress contradicts
feasibility at order `2m`.

## What This Round Does Not Establish

`H-060` is **unresolved** and `instrument_ready` stays **false**.
The registered criterion accepts only on a *checked* chart and a *reviewed* argument, and
neither adjective applies yet.
Two obligations are open and both belong to other lanes:

1. A `W7` instrument whose readiness review passes. Only `C8` was pre-run here, and only
   to confirm that `exp-034` is not a refutation — not to exercise an instrument refusal.
   An instrument was built after this packet was frozen; where its review stands is below.
2. Primary-text confirmation of the curve-selection statement, `BCR` Proposition 8.1.13 —
   or Milnor 1968 Lemma 3.1 *together with* the finite-union reduction of `X-012` §4.1,
   which is what puts the set into Milnor's narrower class of real algebraic sets cut by
   strict inequalities. The printed text was unavailable in this environment. What is
   quoted verbatim in the artifact is one of `BCR`'s own authors, in notes he describes as
   provisional, plus four uses of the proposition by a single author group; the packet's
   second secondary source has since been withdrawn there as an over-attribution. That is
   author-written and single-group attestation, not independent corroboration, and a
   quotation is not a reading.

The artifact’s second proof, by the classical second-order sufficiency principle, reaches
the same conclusion from strictly weaker hypotheses and is recorded because an error in
the curve-selection section would not by itself break isolation.
It is explicitly **not** the acceptance route.
Acceptance was preregistered on curve selection, so the second proof softens no obligation
above. Its one substantive subtlety is worth keeping in view because it is easy to get
backwards: the multiplier scaling is not cosmetic.
At `mu = 1` the sufficiency inequality reads `-2 + 2 sqrt 2 > 0` and holds in the chart
normalization, but reads `-2 + sqrt(2)/2 < 0` and *fails* in the `(c, theta)`
normalization; the threshold is `mu > 2/(-w . q)`.

## Where the `W7` Instrument Stands

This round's mathematics was frozen before any instrument existed, and the instrument that
was then built is not this round's evidence.
It is recorded here because the round's disposition turns on its review state, and because
a reader who is told only that the chart is unchecked would infer that nothing was built.

Built at `6580a9fd`, sixteen minutes before this record was registered, as the package
`src/sqpack/local_rigidity/`. It binds to
[`devtools/assess_n5_rigidity.py`](../../../../devtools/assess_n5_rigidity.py) rather than
extending it, which is a deviation from `W7`'s registered instrument text.
It self-reports `instrument_ready` with `isolation_decided` false — it does not decide
isolation — and it exercises all eight controls `C1`–`C8`, matching the artifact's table
one for one.

Its readiness review has **not** passed, and that, not absence, is why `H-060` keeps
`instrument_ready: false`:

- Reviewed build: payload digest
  `1ab2708623cf4dd077a0f125ba81cf3777088ea8e4d750a56d1dc3f55f807978` at commit `2f112f4c`.
  Classification **BOUNDED-CAVEAT**, not a pass.
  Every mathematical and computational claim reproduced, but two of the eight registered
  controls — `C1` `changed_feature` and `C4` `invented_contact` — were structurally
  incapable of failing and never reached the binding's refusal path, so “all eight controls
  reject” overstated the evidence for the one refusal the instrument exists to make.
- Repaired at `609e7392`; digest
  `ba99ccccd7303f260f48c62a10fb9b6dc43ca3e8ff804646ef5de89a48967971`.
  The re-review verified the repair by removal — neutering the guard or the binding makes
  both controls stop rejecting — and returned **BOUNDED-CAVEAT** again: a pass conditional
  on one unclosed provenance item, since the digested payload pins commit `2f112f4c`, whose
  code cannot produce that payload, so a replayer following the pin gets CANNOT-REPRODUCE.
- Any build after `609e7392` is unreviewed. No statement here refers to one.

The instrument's own declared boundaries, none of which this record could state while it
denied the instrument existed:

- **Four mathematical inputs are cited, not machine-checked**: the separating-axis theorem
  for convex polygons; the topological half of `u -> 2 atan(u)` being a homeomorphism onto
  `(-pi, pi)` (the polynomial injectivity is verified, the topology is cited); containment
  of a convex square in a convex rectangle reducing to its four corners; and continuity of
  polynomials, which is what makes `U` open.
- **The binding compares a restricted second jet**, along one chart ray only — the image of
  `T-012`'s single free direction, `e_u4` halved — not the full chart Hessian.
  Directions outside the first-order cone are not compared, because `T-012` supplies no `q`
  for them.
- **Classification covers single-support-feature touches only**; edge-flush and
  corner-on-corner touches are refused rather than classified.
- **The reduction audit samples only inside `U`**, on a fixed grid rather than a search
  towards `U`'s boundary, which is where a reduction argument is most likely to fail.
  Points outside `U` are counted and skipped, so the filter is exercised, but no sampled
  point sits near the boundary by construction.

The frozen packet itself is not subject to the restricted-jet limitation: `verify_chart.py`
compares `H_chart` against `J^T H_geo J` on all twenty rows.
The limitation belongs to the instrument's binding, and the difference is exactly the kind
of gap between a paper proof and an instrument that a round record exists to state.

## Reading `assurance: verified` Correctly

The subject declares `assurance: verified` with `method: exact-algebraic`, which is the
combination this campaign uses whenever the arithmetic is exact over `Q(sqrt 2)` rather
than finite-precision.
It describes the arithmetic, not the hypothesis.
It does **not** mean `H-060` is verified, and the verdict is the field that says so.
Every quantity here was computed by scratchpad sympy scripts run read-only against the
repository, independently of `sqpack.field`; none of it came from a repository instrument,
because the `W7` instrument was built only after this packet was frozen and its readiness
review has not passed.

`selftest_passed` is `false` for the same reason: there is no engine gate to run.

## What This Round Cost

`wall_seconds` is 11.33: the measured wall time to extract all seven scripts from the
results record and re-run them, on 2026-09-03, with every script’s bytes hashing back to
its recorded digest.
That is the replay cost, and it is the only machine time this round has that can be
measured after the fact.

`agent_minutes` is **absent, and absent on purpose**.
The packet lane did not record its own operator time before freezing, and the integration
lane that wrote this record is not the lane that did the mathematics, so any number here
would be a guess dressed as a measurement.
`agenda-016` allots `BC-152` 360 elapsed minutes and the packet declares itself phase
0–105, but an allotment is not a spend.
The consequence is real and worth stating rather than hiding: this round contributes
nothing to the campaign’s agent-minute total, so that total now understates what `H-060`
has cost.

## Where the Artifacts Are

The proof went in as an exploration report rather than as a new document kind, because
that is the campaign’s slot for a long-form research document and the only one the
document map already covers.
That SHA-256 — `28343b743e689fc99968d589a542d9022d061de8ec3ae5100bf4ef4930e40b6b` — names
the frozen source and not the installed file, and the installed body is **not**
byte-identical to it.
It was reformatted to house Markdown conventions at installation, and a later disclosed
provenance pass rewrote the citation apparatus of `X-012` §4.1, withdrawing one citation.
No statement, number, count, margin, inequality, proof step or claim boundary changed in
either pass; the citation apparatus did.

The seven replay scripts are retained verbatim, with their sizes and digests, in
[this round’s results record](../results/exp-058-h-060-n5-chart-and-proof.json) rather than
installed as repository code.
Nothing under `campaign/` is code — the campaign tree holds records — and the executable
form of this mathematics was built after the freeze as
[`src/sqpack/local_rigidity/`](../../../../src/sqpack/local_rigidity/), which binds to
[`devtools/assess_n5_rigidity.py`](../../../../devtools/assess_n5_rigidity.py) rather than
extending it as `W7`'s text asks.
Installing seven one-off scripts as tooling would cross that boundary and preserve a
measurement in one-off code.
The `command` above extracts them from the record and re-runs all seven; that extraction
and replay was exercised on 2026-09-03 and every script’s bytes hash back to its recorded
digest.

## Novelty, as Scoped

The admissible claim is the first exact proof that Goebel’s `n = 5` optimum is locally
rigid at fixed side — a property Kingbird asserts with no method anywhere on the site, that
Goebel’s 1979 paper does not state (the words “rigid” and “unique” occur zero times in it),
and that Friedman’s survey does not annotate.
Carried *outside* the claim, as an unverified survey assertion: the coordinator's prior-art
survey reports that no theorem stated in the structural-rigidity or jamming literature
covers polygon contact systems.
That is the survey's wording and its scope, it was not verified against the primary texts
by any lane, and the instrument review directed that it be carried this way rather than
inside the claim.
It is narrower than “no stated rigidity theorem covers this”: the same survey records that
the classical second-order sufficiency theorems have no failing hypothesis here once the
system is reduced, so a stated theorem does cover the reduced system.
Score **S3, not S4**. The closing principle is the classical second-order sufficient
optimality condition and the curve-selection proof shape matches Connelly–Whiteley 1996
Theorem 4.3.1; **neither is claimed as new**, nor is the half-angle rationalization, the
separating-axis accounting, or Farkas certification.
The scoping is this lane’s assertion, not a reviewed finding; `BC-153` owns it.

## Claim Boundary

Not established and not claimed: a numerical isolation radius; rigidity when the container
side is free, which `X-007` measured to be false; global uniqueness of the `n = 5` optimum;
rigidity of any other `n = 5` optimal family; applicability of the Connelly–Whiteley
theorem as stated; any novelty beyond the above.

No frontier property, result-register entry or evidence record changed, and none may
change before `BC-153`’s independent review.
`H-060` itself was not amended: its registered criterion is frozen, and this round was
measured against it as written.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
