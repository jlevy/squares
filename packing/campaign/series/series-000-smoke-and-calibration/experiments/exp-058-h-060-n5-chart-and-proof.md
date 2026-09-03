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
      packet was frozen and exercises all eight there; its readiness review has now
      passed, at final payload digest 743fd18a, which makes the instrument usable and
      decides nothing about H-060
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
      whose replay_scripts block holds the verbatim source and SHA-256 of the seven
      scripts this round built. The round built no repository code. The executable form of
      this mathematics was built after the freeze, at 6580a9fd, as the package
      src/sqpack/local_rigidity/, which binds to devtools/assess_n5_rigidity.py rather
      than extending it as W7's text asks; it is not this round's evidence, though its
      readiness review has since passed
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
    stopped_by: criterion
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
    outcome: criterion_met
    checked_by: >-
      BC-153's independent review, 2026-09-03, classification PASS, which supplies the two
      adjectives this round could not. CHECKED: the reviewer replayed sqpack.local_rigidity
      from clean temporary roots under normal and optimized Python, byte-identically, and
      its neighbourhood receipt is this chart's N exactly -- 128 strict conditions in the
      same four roles and counts -- with all twenty rows' gradients and restricted second
      jets matching and all eight controls rejecting. REVIEWED: the reviewer, who authored
      none of the packet, the instrument or this record, rebuilt the pose, the chart, all
      400 elementary polynomials, the twenty rows, q, the midpoints, the first-order cone
      by 28 hand-built Farkas certificates, the self-stress and Lemma 8 from scratch in
      sympy sharing no code with the author, replayed T-012's 28 stored certificates and
      the packet's five scripts to the digests this record retains, and accepted every
      logical step from nonisolation to the second-order contradiction. The reject clause
      stays unsatisfied: no nonconstant feasible arc through the pose and no exact sequence
      of distinct feasible poses converging to it exists, which is what the theorem proves.
      This determination read no_progress until that review ran; the Amendment below states
      what it said and why it changed
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
    decision: accepted
    needs_review: false
    primary_criterion: >-
      H-060's registered direction, which is frozen and was not amended for this round:
      accept only if a checked intrinsic semialgebraic chart accounts for the entire local
      feasible set, its polynomial derivatives bind exactly to the first- and second-order
      certificates, and a reviewed curve-selection and coefficient argument excludes every
      nonconstant feasible arc; reject only on a verified nonconstant feasible arc through
      the pose or an exact sequence of distinct feasible poses converging to it; otherwise
      unresolved
    reason: >-
      Accepted 2026-09-03 on BC-153's independent review, which returned PASS. The
      registered criterion is frozen, was not amended for this round or for the review, and
      was met as written: the chart is CHECKED -- the reviewer replayed the W7 instrument
      from clean roots under normal and optimized Python and its neighbourhood receipt is
      this chart's N exactly, 128 strict conditions in the same four roles and counts, with
      every gradient and restricted second jet matching and all eight controls rejecting --
      and the argument is REVIEWED, by a reviewer who authored none of the packet, the
      instrument, X-012 or this record, who rebuilt every exact quantity from scratch in
      sympy sharing no code with the author (the 400 margins, the 28 witnesses, the 20
      active rows, -t4^2, q = -2, the displayed g-tilde_3, the midpoints, 28 hand-built
      Farkas certificates plus T-012's 28 stored ones and its self-stress, and Lemma 8 on
      random arcs), replayed the packet's five scripts to digests equal to this record's,
      and accepted every logical step from nonisolation to the second-order contradiction.
      What is accepted is exactly this: for s = 2 + sqrt(2)/2 and Goebel's labeled pose P0
      in C = (R^2 x S^1)^5, P0 is an isolated point of Feas(s) (closed unit squares in
      [0, s]^2, pairwise disjoint interiors); equivalently there is no nonconstant
      continuous feasible path from P0 and no sequence of distinct feasible poses converging
      to it; hence Kingbird-rigid at fixed side. Acceptance widens nothing else: no
      isolation radius, nothing with the side free (which is false, X-007), no global
      uniqueness, no other n = 5 optimum, no applicability of Connelly-Whiteley as stated,
      and no method novelty -- the closing principle is classical and the CW96 Theorem 4.3.1
      proof shape is not new. The review names six gaps carried from the record plus one new
      minor one, none of them a condition of the pass; they are listed in the Amendment
      below and none of them is closed by this acceptance. This round's own account of what
      it did and did not do is unchanged above: its numbers still came from scratchpad
      sympy, and what the review adds is the instrument replay and the independent
      reconstruction that the criterion's two adjectives require
    reopen_when: >-
      only what H-060's frozen rejection clause names: a verified nonconstant feasible arc
      through the pose, or an exact sequence of distinct feasible poses converging to it.
      A lone feasible point at positive distance cannot reopen this -- it could invalidate a
      proposed neighbourhood, and N here is defined by sign persistence rather than by a
      radius. Reaching the printed page of BCR Proposition 8.1.13, or installing the
      Basu-Pollack-Roy plus one-variable-Puiseux derivation the review writes out, would
      close the one cited hypothesis the proof rests on; neither is a condition of this
      verdict
    resume_from: >-
      the frozen packet installed as X-012, SHA-256
      28343b743e689fc99968d589a542d9022d061de8ec3ae5100bf4ef4930e40b6b, together with the
      seven replay scripts retained verbatim in this round's results record
---
# exp-058 — H-060 Chart, Constraint Accounting and Order-`2m` Coefficient Proof

`BC-152` asked whether Goebel’s exact `n = 5` optimum is locally rigid at fixed side
under `H-060`’s preregistered criterion.
This round is the mathematics of that lane, frozen.
The argument itself is the proof artifact,
[`X-012`](../../../explorations/X-012-one-chart-four-hundred-inequalities-and-an-order-2m-contradiction.md);
this record is the round that produced it, and the two must be read together.

## What Was Established

Four things, all replayed exactly and none of them a disposition of `H-060`.

**One chart, and no correction term.** An intrinsic half-angle chart on `R^15`,
injective on all of it rather than on some unstated neighbourhood, with cleared
denominators `1 + t_i^2 >= 1` everywhere.
Its second-jet transfer is `J = diag(1, 1, 2)` per square with `Hess Phi(0) = 0`, so
there is no second-order angle correction to carry — which is the reason the coefficient
induction can evaluate Hessians on `e_{t4}` alone.

**The whole constraint system, counted rather than assumed.** All 400 elementary
polynomial inequalities that define a valid packing at side `2 + sqrt(2)/2` were
evaluated in `Q(sqrt 2)` and classified by exact sign: 80 wall-corner functions split 16
active and 64 strictly positive with minimum inactive margin `1 - sqrt(2)/4`, and 320
pair functions over 10 pairs split 4 touching and 6 noncontact.
The agenda’s declared 16/64 and 4/6 counts are confirmed independently and no
discrepancy was found.
On a neighbourhood cut out by 128 strict sign conditions, the local feasible system is
exactly the 20 active rows.
`D-390`’s endpoint incidence and `D-391`’s disjunction are excluded by computation
rather than by argument: every active pair corner sits at along-edge parameter exactly
`1/2`, and exactly one branch is satisfied per touching pair.

**T-012 transfers.** All 28 Farkas certificates and the self-stress replay on the chart
rows, giving `A_chart = A_geo J`, `q_chart = -2` on the pair rows, and
`w . q_chart = -2 sqrt 2 < 0`.

**The induction closes, conditionally.** Given the cited curve selection lemma, no
nonconstant analytic feasible arc through the pose exists, because every coefficient
below order `2m` is forced into the flex line’s kernel and the self-stress contradicts
feasibility at order `2m`.

## What This Round Does Not Establish

*This section is the round on its own, as frozen.
`H-060` was resolved later and elsewhere — by `BC-153`’s independent review, which is
what the verdict now records; see the
[Amendment](#amendment--the-bc-153-independent-review-and-acceptance).*

`H-060` was **unresolved** at the freeze.
`instrument_ready` is **true**, and that flag is about the instrument, not about the
hypothesis: it says the instrument may be used to evaluate `H-060`, not that `H-060` is
decided.
No target determination ran at the readiness checkpoint, and the instrument sets
`isolation_decided` false unconditionally, so it cannot decide isolation even in
principle. The registered criterion accepts only on a *checked* chart and a *reviewed*
argument, and neither adjective applied to this round on its own.
Of the two obligations below the first was discharged at the readiness checkpoint; the
second is *not* closed — `BC-153` judged it non-blocking on a derivation rather than
reaching the printed page, which is gap 1 of the Amendment:

1. **Discharged.** A `W7` instrument whose readiness review passes — it passed on the
   third round, at final payload digest `743fd18a`; the history, the reviewer’s one
   residual recommendation and what the lane changed after the pass are below.
   That does not make *this* round’s chart checked: only `C8` was pre-run here, and only
   to confirm that `exp-034` is not a refutation — not to exercise an instrument
   refusal, and every number in this record still comes from scratchpad sympy.
2. **Open.** Primary-text confirmation of the curve-selection statement, `BCR`
   Proposition 8.1.13 — or Milnor 1968 Lemma 3.1 *together with* the finite-union
   reduction of `X-012` §4.1, which is what puts the set into Milnor’s narrower class of
   real algebraic sets cut by strict inequalities.
   The printed text was unavailable in this environment.
   What is quoted verbatim in the artifact is one of `BCR`’s own authors, in notes he
   describes as provisional, plus four uses of the proposition by a single author group;
   the packet’s second secondary source has since been withdrawn there as an
   over-attribution. That is author-written and single-group attestation, not independent
   corroboration, and a quotation is not a reading.

The artifact’s second proof, by the classical second-order sufficiency principle,
reaches the same conclusion from strictly weaker hypotheses and is recorded because an
error in the curve-selection section would not by itself break isolation.
It is explicitly **not** the acceptance route.
Acceptance was preregistered on curve selection, so the second proof softens no
obligation above. Its one substantive subtlety is worth keeping in view because it is
easy to get backwards: the multiplier scaling is not cosmetic.
At `mu = 1` the sufficiency inequality reads `-2 + 2 sqrt 2 > 0` and holds in the chart
normalization, but reads `-2 + sqrt(2)/2 < 0` and *fails* in the `(c, theta)`
normalization; the threshold is `mu > 2/(-w . q)`.

## Where the `W7` Instrument Stands

This round’s mathematics was frozen before any instrument existed, and the instrument
that was then built is not this round’s evidence.
It is recorded here because the round’s disposition turns on its review state, and
because a reader who is told only that the chart is unchecked would infer that nothing
was built.

Built at `6580a9fd`, sixteen minutes before this record was registered, as the package
`src/sqpack/local_rigidity/`. It binds to
[`devtools/assess_n5_rigidity.py`](../../../../devtools/assess_n5_rigidity.py) rather
than extending it, which is a deviation from `W7`’s registered instrument text.
It self-reports `instrument_ready` with `isolation_decided` false — it does not decide
isolation — and it exercises all eight controls `C1`–`C8`, matching the artifact’s table
one for one.

Its readiness review has now **passed**, on the third round, which is what moved `H-060`
to `instrument_ready: true`:

- Reviewed build: payload digest
  `1ab2708623cf4dd077a0f125ba81cf3777088ea8e4d750a56d1dc3f55f807978` at commit
  `2f112f4c`. Classification **BOUNDED-CAVEAT**, not a pass.
  Every mathematical and computational claim reproduced, but two of the eight registered
  controls — `C1` `changed_feature` and `C4` `invented_contact` — were structurally
  incapable of failing and never reached the binding’s refusal path, so “all eight
  controls reject” overstated the evidence for the one refusal the instrument exists to
  make.
- Repaired at `609e7392`; digest
  `ba99ccccd7303f260f48c62a10fb9b6dc43ca3e8ff804646ef5de89a48967971`. The re-review
  verified the repair by removal — neutering the guard or the binding makes both
  controls stop rejecting — and returned **BOUNDED-CAVEAT** again: a pass conditional on
  one unclosed provenance item, since the digested payload pins commit `2f112f4c`, whose
  code cannot produce that payload, so a replayer following the pin gets
  CANNOT-REPRODUCE.
- **PASS.** Final payload digest
  `743fd18a839fbc3dc566b5e622f688c5745845573414eea40ebf52d620d2cc67` over source digest
  `9382bae12976bc1225382ef79ab4a777d5982cbc6b04a47dfbdba51d22c36357`, the reviewer
  reproducing that source digest independently from the recipe.
  Replayed from a clean root at a commit one past the author’s observed commit, with the
  package untouched between the two, and byte-identical under normal and optimized
  Python; 46 tests pass.
  The leaf diff against the author’s final certificate shows exactly one differing leaf,
  `/claim_boundary/provenance/pinned_commit`, with `tree_matches: True` and
  `paths_differing: []` — which is precisely the provenance item the second round left
  open, now closed. The `C1`/`C4` repair was re-verified by removal: replace the guard
  with a no-op and both controls stop rejecting.
  The corrected constant is confirmed on all sixteen support features,
  `G''(e_u4) = -2(m+1)` exactly; the reviewer’s earlier `-(m + 1/2)` was the geometric
  gap’s second derivative rather than the cleared chart polynomial’s. The structural
  conclusion is unchanged and now machine-checked: the restricted second jet is an
  affine function of the support feature’s own base margin, and is **not** an
  independent identifier.

### What Changed After the Pass, and What It Does Not Change

The reviewer carried one residual **recommendation**, explicitly not a condition of the
pass: `source_digest` covered the instrument package and its driver but not the three
files the instrument reads — [`sqpack/field.py`](../../../../src/sqpack/field.py),
[`cases/gobel5/packing.py`](../../../../cases/gobel5/packing.py) and
[`devtools/assess_n5_rigidity.py`](../../../../devtools/assess_n5_rigidity.py).
A change to any of those would have altered what the instrument computes while leaving
`source_digest` unchanged.

The lane has since implemented it.
The three inputs are hashed, the hashed set is derived from the **imported module
objects** rather than from a path list, so it cannot drift from what the driver actually
imported, and the `tree_matches` dirty check was widened to that same set — hashing the
inputs while checking only the package would have let `tree_matches: True` stand over a
modified input. The hashed set went from 9 files to 12.

The current build is therefore **not** the reviewed build, and carries no readiness
review of its own:

|  | reviewed | current |
| --- | --- | --- |
| payload digest | `743fd18a…` | `bd450cb610a866972043a98a04673d6a9d75acd78642b658b9dccb098a18b26e` |
| source digest | `9382bae1…` | `ad32062e5a01…` |
| observed commit | `d45a3269…` | `15ebfa98d66a…` |

The current build carries receipt `f8262c77…` and certificate `f3b0c2d6…`, is
byte-identical under normal and optimized Python, and reports `tree_matches: True` with
no differing paths. Its leaf diff against the reviewed build is exactly four leaves, all
under `/claim_boundary/provenance`: `note`, `pinned_commit`, `source_digest`, and the
length of `source_files`. **No package code changed**, which is why the 46 passing tests
and the clean linters from the reviewed round remain current.

`pinned_commit` moved from `d45a3269…` to `15ebfa98…` only because an unrelated commit
landed between runs.
That is the documented sensitivity of the observing mechanism, not an instrument change;
`source_digest` is the leaf that moved for a substantive reason.

**Replayed since, by `BC-153` (§6.3).** This paragraph first said only that the current
build is not claimed to be reviewed, which now understates what has been done to it.
The `BC-153` reviewer replayed *this* build — not the reviewed one — from clean roots
under both interpreters, reproduced every count, margin, row, jet and control verdict,
and leaf-diffed his certificate against the author’s current certificate (exactly
**one** differing leaf, `/claim_boundary/provenance/pinned_commit`, `15ebfa98` →
`ceff4400`, an unrelated commit landing between runs) and against the instrument
reviewer’s replay of the reviewed build (differences only under
`/claim_boundary/provenance`). That confirms the four-leaf difference above from outside
the lane, so the readiness `PASS` at `743fd18a…` carries over to the current build.
It is still not a second readiness review, and none is claimed.

Two limitations stay named rather than fixed:

- **`certificate_drift` digests a reduced payload.** It computes its recorded digest
  without the controls list and without provenance, so that field does not equal the
  shipped payload digest and a reader who expects it to match will be surprised.
  It remains a sound drift test — the digest moves under two independent mutations and
  is stable on rebuild — so this is a known cosmetic discrepancy, disclosed by the lane
  unprompted and deliberately left in place.
- **Replayability rests on `tree_matches`, not on the digest alone.** With the widened
  hashed set the digest now covers the inputs, but what a replayer follows is still the
  pinned commit, and that pin is what fixes the whole tree.

The instrument’s own declared boundaries, none of which this record could state while it
denied the instrument existed:

- **Four mathematical inputs are cited, not machine-checked**: the separating-axis
  theorem for convex polygons; the topological half of `u -> 2 atan(u)` being a
  homeomorphism onto `(-pi, pi)` (the polynomial injectivity is verified, the topology
  is cited); containment of a convex square in a convex rectangle reducing to its four
  corners; and continuity of polynomials, which is what makes `U` open.
- **The binding compares a restricted second jet**, along one chart ray only — the image
  of `T-012`’s single free direction, `e_u4` halved — not the full chart Hessian.
  Directions outside the first-order cone are not compared, because `T-012` supplies no
  `q` for them.
- **Classification covers single-support-feature touches only**; edge-flush and
  corner-on-corner touches are refused rather than classified.
- **The reduction audit samples only inside `U`**, on a fixed grid rather than a search
  towards `U`’s boundary, which is where a reduction argument is most likely to fail.
  Points outside `U` are counted and skipped, so the filter is exercised, but no sampled
  point sits near the boundary by construction.

The frozen packet itself is not subject to the restricted-jet limitation:
`verify_chart.py` compares `H_chart` against `J^T H_geo J` on all twenty rows.
The limitation belongs to the instrument’s binding, and the difference is exactly the
kind of gap between a paper proof and an instrument that a round record exists to state.

## Reading `assurance: verified` Correctly

The subject declares `assurance: verified` with `method: exact-algebraic`, which is the
combination this campaign uses whenever the arithmetic is exact over `Q(sqrt 2)` rather
than finite-precision.
It describes the arithmetic, not the hypothesis.
It does **not** mean `H-060` is verified: the verdict is the field that carries the
hypothesis’s disposition, and what put `accepted` there is `BC-153`’s review, not this
line. Every quantity here was computed by scratchpad sympy scripts run read-only against
the repository, independently of `sqpack.field`; none of it came from a repository
instrument, because the `W7` instrument was built only after this packet was frozen, and
its readiness review — which has since passed — certifies the instrument rather than
this round’s numbers.

`selftest_passed` is `false` for the same reason: there is no engine gate to run.

## What This Round Cost

`wall_seconds` is 11.33: the measured wall time to extract all seven scripts from the
results record and re-run them, on 2026-09-03, with every script’s bytes hashing back to
its recorded digest.
That is the replay cost, and it is the only machine time this round has that can be
measured after the fact.

`agent_minutes` is **absent, and absent on purpose**. The packet lane did not record its
own operator time before freezing, and the integration lane that wrote this record is
not the lane that did the mathematics, so any number here would be a guess dressed as a
measurement. `agenda-016` allots `BC-152` 360 elapsed minutes and the packet declares
itself phase 0–105, but an allotment is not a spend.
The consequence is real and worth stating rather than hiding: this round contributes
nothing to the campaign’s agent-minute total, so that total now understates what `H-060`
has cost.

## Where the Artifacts Are

The proof went in as an exploration report rather than as a new document kind, because
that is the campaign’s slot for a long-form research document and the only one the
document map already covers.
That SHA-256 — `28343b743e689fc99968d589a542d9022d061de8ec3ae5100bf4ef4930e40b6b` —
names the frozen source and not the installed file, and the installed body is **not**
byte-identical to it.
It was reformatted to house Markdown conventions at installation, and a later disclosed
provenance pass rewrote the citation apparatus of `X-012` §4.1, withdrawing one
citation. No statement, number, count, margin, inequality, proof step or claim boundary
changed in either pass; the citation apparatus did.

The seven replay scripts are retained verbatim, with their sizes and digests, in
[this round’s results record](../results/exp-058-h-060-n5-chart-and-proof.json) rather
than installed as repository code.
Nothing under `campaign/` is code — the campaign tree holds records — and the executable
form of this mathematics was built after the freeze as
[`src/sqpack/local_rigidity/`](../../../../src/sqpack/local_rigidity/), which binds to
[`devtools/assess_n5_rigidity.py`](../../../../devtools/assess_n5_rigidity.py) rather
than extending it as `W7`’s text asks.
Installing seven one-off scripts as tooling would cross that boundary and preserve a
measurement in one-off code.
The `command` above extracts them from the record and re-runs all seven; that extraction
and replay was exercised on 2026-09-03 and every script’s bytes hash back to its
recorded digest.

## Novelty, as Scoped

The admissible claim is the first exact proof that Goebel’s `n = 5` optimum is locally
rigid at fixed side — a property Kingbird asserts with no method anywhere on the site,
that Goebel’s 1979 paper does not state (the words “rigid” and “unique” occur zero times
in it), and that Friedman’s survey does not annotate.
Carried *outside* the claim, as an unverified survey assertion: the coordinator’s
prior-art survey reports that no theorem stated in the structural-rigidity or jamming
literature covers polygon contact systems.
That is the survey’s wording and its scope, it was not verified against the primary
texts by any lane, and the instrument review directed that it be carried this way rather
than inside the claim.
It is narrower than “no stated rigidity theorem covers this”: the same survey records
that the classical second-order sufficiency theorems have no failing hypothesis here
once the system is reduced, so a stated theorem does cover the reduced system.
Score **S3, not S4**. The closing principle is the classical second-order sufficient
optimality condition and the curve-selection proof shape matches Connelly–Whiteley 1996
Theorem 4.3.1; **neither is claimed as new**, nor is the half-angle rationalization, the
separating-axis accounting, or Farkas certification.
The scoping was this lane’s assertion when written.
`BC-153` has since checked the three load-bearing sources first-hand — Kingbird line 44,
Friedman `DS7`, Goebel 1979 — and independently accepted the `S3` claim in those words;
the wider survey scoping stays outside the claim, still unverified against the primary
texts.

## Claim Boundary

Not established and not claimed: a numerical isolation radius; rigidity when the
container side is free, which `X-007` measured to be false; global uniqueness of the
`n = 5` optimum; rigidity of any other `n = 5` optimal family; applicability of the
Connelly–Whiteley theorem as stated; any novelty beyond the above.

No frontier property, result-register entry or evidence record changed *in this round*,
and none changed before `BC-153`’s independent review; what that review then authorised
is listed in the Amendment.
`H-060` itself was not amended: its registered criterion is frozen, this round was
measured against it as written, and so was the review.

## Amendment — the `BC-153` Independent Review and Acceptance

`BC-153` reviewed this round on 2026-09-03 and returned **PASS**. The reviewer authored
none of the packet, the instrument, `X-012`, the round record or the three supporting
reviews, wrote only to their own scratchpad, and used the supporting reviews as evidence
rather than as authority: every mathematical step was re-derived.
The verdict above moves from `unresolved` to `accepted` on that review, and
`needs_review` is cleared.

**What the pass rests on.** Three layers, from most to least independent of the authors’
code.

1. **A from-scratch reconstruction.** In sympy, sharing no code with the packet, with
   `sqpack` or with the instrument, the reviewer rebuilt the pose and chart and
   reproduced: all 400 elementary polynomials classified by exact sign (80 wall-corner
   functions 16/64 with minimum inactive margin `1 - √2/4`; 320 pair functions, 4
   touching pairs and 6 noncontact); the 28 negative witnesses, value for value; the 128
   strict conditions of `N`; the 20 active rows in `T-012`’s own order, with every
   gradient matching the §2.5 table and column `t4` identically zero; `q_chart = -2` on
   the four pair rows with each pair row restricting to exactly `-t4²` on the flex line;
   the packet’s displayed `g̃_3` as a polynomial; the four exact edge midpoints; the
   first-order cone by **28 Farkas certificates the reviewer built by hand** from the
   row inequalities; the self-stress, `w · q_chart = -2√2`, and `Φ = Σ w_j g̃_j`
   restricting to `-√2 · t4²`; `T-012`’s 28 stored certificates and its self-stress
   replayed against the reviewer’s own `S A_chart`; and Lemma 8 on random rational arcs
   at `m = 2, 3`.
2. **This round’s own scripts**, run read-only, all passing, with all seven files
   hashing to the digests retained in this round’s
   [results record](../results/exp-058-h-060-n5-chart-and-proof.json).
3. **The instrument**, `sqpack.local_rigidity`, replayed from clean temporary roots
   under normal and optimized Python: payload digest identical under both, `ready`,
   `controls_all_reject`, no refusals, `isolation_decided` false as designed, and a
   neighbourhood receipt that is this document’s `N` exactly — 128 strict conditions, 64
   \+ 24 + 12 positive and 28 negative — with `gradient_matches` and
   `second_jet_matches` true on all twenty rows.
   A leaf diff against the reviewed build `743fd18a` differs only under
   `/claim_boundary/provenance`, in no margin, count, row, jet, control verdict or
   determination, which confirms independently of this record’s own statement that the
   current build differs from the reviewed one in provenance metadata only.

**The exact scope, and it is the whole of what is claimed.** For `s = 2 + √2/2` and
Goebel’s labeled pose `P⁰` in `C = (ℝ² × S¹)⁵`, `P⁰` is an isolated point of `Feas(s)`
(closed unit squares in `[0, s]²`, pairwise disjoint interiors); equivalently there is
no nonconstant continuous feasible path from `P⁰` and no sequence of distinct feasible
poses converging to it; hence Kingbird-rigid at fixed side.

**Not claimed, and not to be claimed on this review:** any isolation radius; rigidity
with the side free, which is false (`X-007`); global uniqueness; any other `n = 5`
optimum; applicability of Connelly–Whiteley as stated; and any method novelty — the
closing principle is classical and the `[CW96]` Theorem 4.3.1 proof shape is not new.

**Novelty, `S3`, in the reviewer’s own words as accepted:** the first exact *proof* of
fixed-side local rigidity of Goebel’s `n = 5` optimum — a property *asserted without
proof* by Kingbird (archived page, line 44), not stated by Goebel, and not stated by
Friedman (`DS7` Theorem 2 is a lower bound only).
The reviewer checked those three sources first-hand rather than through the survey.

**Six named gaps, and one new minor one.
None is a condition of the pass, and none is closed by acceptance.**

1. **`BCR` Proposition 8.1.13’s printed page is still unread.** Non-blocking: the
   review’s §6.5 derives the needed statement from primary-text `BPR` Theorem 3.22 plus
   the one-variable Puiseux fact, through the `t = u^p` bridge Coste states and the
   reviewer verified first-hand in his notes; Milnor with the finite-union reduction of
   `X-012` §4.1 is a third route.
2. **The second-order-sufficiency numbering is from memory** — on the non-acceptance
   route only; Theorem 11 is proved in full.
3. **Prior-art scoping comes from the coordinator’s survey and is unverified against the
   primary texts** — carried *outside* the claim, which is where it stays.
4. **The instrument binds only the restricted jet along `e_{u4}`** — sufficient, since
   Lemma 8 at order `2m` and Theorem 11 consume only `eᵀ H_j e`.
5. **The instrument’s reduction audit samples only the neighbourhood interior** —
   irrelevant to the proof: `N` is defined by sign persistence rather than by a radius,
   and the proof consumes no boundary behaviour.
6. **The Kingbird thirteen-versus-four list tension** (`X-012` §7.3) is real and
   unresolved, and not load-bearing: `n = 5` is on both lists.
7. **New, minor:** `X-012` §1.3 (i) is terse — a path can be constant on an initial
   segment, so the argument wants one sentence taking the supremum of that interval.
   The conclusion holds; the frozen mathematics is left as it stands and this is
   recorded rather than patched.

**What this record changed, and what it did not.** The verdict is `accepted` with
`needs_review` false; the outcome determination, which read `no_progress` with
`checked_by` “nothing that the criterion accepts”, now reads `criterion_met` on the
review; and `effort.stopped_by` moves from `dependency` to `criterion`, because the
dependency this round stopped on — an independent review — arrived and decided it, so
the round is no longer resumable work.
Unchanged: `H-060`’s registered criterion, which is frozen and was met as written and
not amended for this round or for the review; every number, count, margin and
determination above; and this round’s
[results record](../results/exp-058-h-060-n5-chart-and-proof.json), which is immutable
run data and still states the round’s own disposition at the freeze.

**What the pass authorised elsewhere**, and it is the complete list: clearing
`needs_review` here; setting the `n = 5` frontier rigidity property to locally rigid at
fixed side, with a new evidence record `E-n005-fixed-side-local-rigidity`; and
registering the theorem as `T-014`, `apparently-novel` at `S3`, which is permitted only
because the reviewer independently accepted the novelty basis.
`T-012`’s recorded next action — “local rigidity needs the curve-selection argument
written out in `X-007` to become a computation” — is discharged by that registration,
and `X-012`’s stale `instrument_ready: false` statements are corrected.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
