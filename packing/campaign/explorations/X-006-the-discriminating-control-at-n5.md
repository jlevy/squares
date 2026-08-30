---
title: X-006 — the candidate discriminating control at n = 5 is the one D-034 has been quoting
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-006
  title: The candidate discriminating control at n = 5 is the one D-034 has been quoting
  date: '2026-08-30'
  author: Claude (agent), under BC-083 in agenda-008
  campaign: packing.squares
  brief: >-
    BC-083 asked whether n = 5 can be given a discriminating identity control -- one whose
    proved component count is neither one nor its labelled count -- since D-373 showed the
    existing quotient controls all answer one and D-375 showed the n = 4 labelled control
    answers a number no candidate can reach. A candidate control exists: the pair D-034 has
    named since 2026-08-23 without its two endpoints ever being retained. They are retained
    now, and whichever way its component count resolves it separates relations no existing
    control separates, with one branch refuting contact + closure, the standing sole
    survivor. It is a candidate rather than a control because that count is not proved --
    this report delivers the exit's second branch, naming the missing claim, which exp-042
    already records as a declared scope refusal.
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/bc-083-n5-identity-pair.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/exp-042-h-023-n5-endpoint-aware-rotating-paths.json
  - packing/campaign/explorations/X-005-identity-relation-and-its-controls.md
  - packing/golden/basin-maps.yaml
  - packing/atlas/known-best/contact-enumeration-pricing.json
  - packing/campaign/hypotheses/H-023-n5-terminal-connectivity.md
  - defects.md
  proposes: []
---
# X-006 — The Candidate Discriminating Control at `n = 5`

**Date:** 2026-08-30

**Status:** W3 insight slice under `BC-083`. Delivers the exit’s **second** branch — a
typed statement of what prevents a proved `n = 5` count, naming the quantity and pricing
the alternative route — together with a retained *candidate* control, scored
prospectively against all four relations.

The first branch is not met, and this report does not claim it: that branch requires a
**proved** component count, and `component_count` is `null`. What is established is that
a discriminating control exists as an object, and that both of its possible answers
separate the candidates.
Whether it discriminates *in fact* rests on a count nobody has proved.

**Owns:** The argument.
`devtools/build_n5_identity_pair.py` owns the retained pair,
`devtools/check_identity_relation.py` owns the scoring, and
`tests/test_identity_relation.py` pins both.

## What a Discriminating Control Has to Do

Two earlier findings bracket the question, and between them they say what the answer
must look like.

[`D-373`](../../../defects.md) is the lower bracket: the two quotient controls both have
component count **one**, so a relation that merges everything passes them.
A control whose answer is one confirms every candidate.

[`D-375`](../../../defects.md) is the upper one: the `n = 4` labelled control has count
**24**, and its 24 states are measured to collapse to a single geometric key and a
single contact certificate, so every candidate reports one against it.
A control whose answer no candidate can reach refutes every candidate.

Neither bracket tests anything, and they fail in opposite directions.
So a discriminating control needs a proved count that *some* relabelling-invariant
relation reaches and others do not — which is what `BC-083`’s “neither one nor the
labelled count” was reaching for, now with the reason attached.

## The Control Already Exists, Unretained

`D-034` has recorded since 2026-08-23 that two `n = 5` rows share side `2.767766952966`,
closed form, contact certificate, angle signature and contact count while differing
geometrically. That is exactly the shape required: identical on every invariant but one.

It had never been retained.
`golden/basin-maps.yaml` keeps the aggregate rows and not the poses, so nothing
downstream could score a relation on the pair or check the claim.
The census is a fixed seed stream, so the endpoints were not lost, only unkept;
`devtools/build_n5_identity_pair.py` reproduces them through `check_golden_basins`’s own
functions and retains both.

**The claim is now measured rather than quoted:**

|  | seed 5 | seed 2 |
| --- | --- | --- |
| side | `2.767766952966` | `2.767766952966` |
| geometric key | `0373183838f6…` | `07860b128b38…` |
| contact certificate | `5dcbd27037e1…` | `5dcbd27037e1…` |

Same certificate, different geometric keys, and a side difference of `8.9e-16` — four
orders of magnitude below the `1e-11` quench floor `D-021` records, so the sides are
equal to any precision this pipeline can assert.

**One thing `D-034` never noted: the pair is not optimal.** `s(5) = 2 + √2/2 ≈ 2.7071`
and these endpoints sit at `2.7678`, which the golden map records as
`found_optimum: false`. The four existing controls describe the *optimal* configuration
space; this pair describes two terminal endpoints of the quench.
Those are different objects, and the pair is the one `distinct_basins` actually counts.

## What It Would Decide

Run `uv run --frozen python -m devtools.check_identity_relation`.

| Relation | reports on the pair | if the count is 1 | if the count is 2 |
| --- | ---: | --- | --- |
| side alone | 1 | agrees | **refuted** |
| geometric + contact | 2 | **refuted** | agrees |
| contact alone | 1 | agrees | **refuted** |
| contact + closure | 1 | agrees | **refuted** |

Neither branch is unanimous, so the control discriminates either way — the first thing
required of it, and the thing neither bracket above manages.

**The second branch is the valuable one.** If the count is two, `contact + closure` —
the sole survivor of all four proved answers, and the relation `X-005` declared — is
refuted, and the relation `Atlas.add` already implements is the one left standing.
A control that could only confirm the incumbent would not be worth proving.

There is no closure data at `n = 5`, so `contact alone` and `contact + closure` coincide
here. That is not a defect of the control — it is what makes the control reach something
nothing else does.

[`D-378`](../../../defects.md) records why.
The only closure the record carries is `closure(G) = [C, G, M]`, and it covers **every**
stratum the `n = 3` quotient has, so on that control `contact + closure` returns one
whatever its certificates say.
Its “agrees” there is a property of the control rather than a test of the relation, and
no retained control separates it from a relation that merges everything.
The `n = 5` pair carries no closure for the merge to hide behind, so it is the first
control that reaches the relation’s certificate half at all.

## The One Missing Quantity, and Why the `n = 3` Route Does Not Supply It

The count is not proved, and cannot be proved the way `n = 3` and `n = 4` were.

Two conditions make those classifications exhaustive, and **both are properties of
container side exactly 2 with unit squares**, not of small `n`.

First, orientation is forced.
`orientation_forcing_record` proves it from containment on the chart `[-1,1]^2`, through
the exact identity `1/2 - w(1 - w/2) = (w-1)^2/2`; the argument holds for any `n >= 2`
at side 2 and fails the moment `s > 2`. Second, and this is what makes the
classification *finite*, each separation disjunct pins a coordinate to an endpoint of
`[0,1]`, which is why the enumerator can assert that `free_variables` is `{1}` at
`n = 3` and `{0}` at `n = 4`.

Neither survives `s > 2`. At `s(5) = 2.7071`, or the pair’s `2.7678`, the cells would be
positive-dimensional polytopes *even with orientation forced*, so `4^C(5,2) = 1048576`
branches is not the work either and **the obstruction is the method’s kind, not its
cost**.

An earlier draft gave “the `n = 5` optimum has two angle classes” as the reason.
That is a true statement about the optimum and the wrong cause: it makes the obstruction
look contingent on which optimum `n = 5` happens to have, when it follows from the side
alone.
The same draft said the cells are “decided by a linear program”; they are not — no
LP is solved anywhere in that classification, and the cells are decided by exact
endpoint propagation.

The contact-scaffold route prices `n = 5` at `9,296,855,040` units of raw orbit work
against a declared `10,000,000` cap, and its retained pricing therefore records
`decision: enumerate-isomorph-free` with the realization stage `lp_solves: null` — not
run. That route reduces to `11,013` canonical orbits, which is tractable, but its
declared scope is “connected, one semantic angle color, no walls”, which is not the
object here either.

The missing claim is named exactly, and by the record rather than by this report:
`exp-042` lists `A_to_B_stationary_connection` first among eleven declared scope
refusals. That is the quantity.
Proving it closes `D-034` and resolves this control in one step; until then the control
is retained, scored prospectively, and honest about which of the two columns it is in.

## What Is Not Established

**No component count is claimed.** The retained artifact carries `component_count: null`
and a field saying why, so a future run cannot mistake the prospective scoring for a
verdict.

**This does not close `D-034`.** It does not shrink the proof obligation by any amount:
`A_to_B_stationary_connection` is exactly as hard as it was.
What changes is the *price* of the obligation, which was previously unstated — proving
it now also resolves an identity control, so the work buys two things rather than one.

**The pair is two endpoints, not a census.** Whether other `n = 5` rows would sharpen or
complicate the control is unexamined; six seeds produced six rows and only these two
collide.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
