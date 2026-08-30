---
title: X-006 — n = 5 does admit a discriminating control, and it is the one D-034 has been quoting
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-006
  title: n = 5 admits a discriminating control, and it is the one D-034 has been quoting
  date: '2026-08-30'
  author: Claude (agent), under BC-083 in agenda-008
  campaign: packing.squares
  brief: >-
    BC-083 asked whether n = 5 can be given a discriminating identity control -- one whose
    proved component count is neither one nor its labelled count -- since D-373 showed the
    existing quotient controls all answer one and D-375 showed the n = 4 labelled control
    answers a number no relabelling-invariant relation can reach. The answer is yes, and
    the control has been named in D-034 since 2026-08-23 without its two endpoints ever
    being retained. They are retained now. Whichever way its component count resolves it
    separates relations no existing control separates, and one of the two branches refutes
    contact + closure, the standing sole survivor. What it lacks is that count, and exp-042
    already names the missing claim as a declared scope refusal.
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
# X-006 — The Discriminating Control at `n = 5`

**Date:** 2026-08-30

**Status:** W3 insight slice under `BC-083`. Answers the first branch of the exit — a
declared `n = 5` control, scored against all four candidate relations — and names the
one quantity it waits on.

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
**24**, and every candidate relation is invariant under relabelling by construction, so
each reports one against it.
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
here. That is not a defect of the control; it is the statement that closure is what
separates them, and `n = 5` has not been given any.

## The One Missing Quantity, and Why the `n = 3` Route Does Not Supply It

The count is not proved, and cannot be proved the way `n = 3` and `n = 4` were.

Those classifications are exhaustive because **orientation is forced**: every square is
axis-aligned, so the configuration space is a finite union of separation cells — `64`
raw branches at `n = 3` and `4096` at `n = 4`, each decided by a linear program.
The `n = 5` optimum has two angle classes, so orientation is not forced and the space
carries continuous angle parameters.
`4^C(5,2) = 1048576` branches would be affordable; **the obstruction is the method’s
kind, not its cost.** The separation-cell enumeration decides axis-aligned
configurations, and this is not one.

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

**This does not close `D-034`**, and does not narrow it either.
It converts a quoted claim into a checked one and identifies what the claim would buy.

**The pair is two endpoints, not a census.** Whether other `n = 5` rows would sharpen or
complicate the control is unexamined; six seeds produced six rows and only these two
collide.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
