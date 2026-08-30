---
title: X-005 — the relation the atlas should count, and why its acceptance rule could not test one
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-005
  title: The relation the atlas should count, and why its acceptance rule could not test one
  date: '2026-08-30'
  author: Claude (agent), under BC-080 in agenda-007
  campaign: packing.squares
  brief: >-
    BC-046 asked what relation the atlas should count, given that a connected optimal set
    produces many endpoint keys and the current store splits it (D-034). This scores four
    candidate relations against the two exact moduli experiments and finds one that
    survives: contact certificates merged along the retained strata closure. It also finds
    that the acceptance rule as written could not have established that. The rule named the
    two quotient controls, both of which have component count one, so a relation that
    merges everything passes them -- and `side alone` is exactly such a relation and is
    known wrong. The labelled controls, whose answers are 2 and 24, are what refute it.
    The two controls turn out to isolate independent failures: n = 4 is pure symmetry with
    no connectivity, and n = 3 is pure connectivity within one orbit.
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/exp-014-h-032-n3-optimal-moduli.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/exp-015-h-032-n4-optimal-moduli.json
  - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-014-h-032-n3-optimal-moduli.md
  - packing/src/sqpack/research/atlas.py
  - packing/campaign/hypotheses/H-032-small-n-optimal-moduli.md
  - defects.md
  proposes: []
---
# X-005 — The Relation the Atlas Should Count

**Date:** 2026-08-30

**Status:** W3 insight slice under `BC-080`. Declares a relation and reports an
inadequacy in the acceptance rule that was supposed to test one.

**Owns:** The argument.
`devtools/check_identity_relation.py` owns the numbers, and
`tests/test_identity_relation.py` pins the verdicts.

## The Question, and Why the Obvious Answer Is Wrong

`Atlas.add` calls two endpoints the same basin when their quantized geometric key *and*
their contact certificate agree, and `distinct_basins` is then read as a count of
connected terminal components.
[`D-034`](../../../defects.md) records the consequence: the exact `n = 3` side-2 family
has a continuum of interior geometric keys sharing one contact certificate, so one
connected component is split into quantization-dependent rows.

The tempting repair is to drop the geometric key and count contact certificates.
That is wrong on the same control, and the artifact says so: the `D4 x S3` quotient of
`F_3(2)` is one interval carrying **two** contact certificates, `C` on one endpoint and
`G` with `M` on the rest.
Counting certificates reports two components where one is proved.

## Four Candidates, Scored Against Four Proved Answers

Run `uv run --frozen python -m devtools.check_identity_relation`.

| Relation | Level | `n=3` labelled (2) | `n=3` quotient (1) | `n=4` labelled (24) | `n=4` quotient (1) |
| --- | --- | --- | --- | --- | --- |
| side alone | any | 1 refuted | 1 agrees | 1 refuted | 1 agrees |
| geometric + contact | labelled | 4 refuted | — | undecidable | — |
| contact alone | quotient | — | 2 refuted | — | undecidable |
| **contact + closure** | quotient | — | **1 agrees** | — | undecidable |

**Level is part of the relation, not decoration.** A contact certificate is invariant
under relabelling and under `D4`, so it is a statement about the quotient; two labelled
components differing only by a relabelling share it by construction.
Scoring it against a labelled control would reject the right relation for doing what it
is supposed to do, so the instrument reports `n/a` rather than a refutation there.

**The surviving relation is `contact + closure`:** two endpoints are the same terminal
component when their contact certificates agree, or when the strata those certificates
name lie in one closure.
The `n = 3` artifact retains exactly what that needs — `closure(G) = [C, G, M]` — so the
merge is read from the record rather than assumed.

## The Finding: The Acceptance Rule Could Not Have Tested This

`BC-046` wrote the exit as “a declared identity relation with a criterion that the exact
`n = 3` sliding family and the exact `n = 4` point both satisfy”.
Those are the two *quotient* controls, and **both have component count one**.

A relation that merges everything passes both.
`side alone` is that relation: every point of an optimal configuration space has the
optimal side by definition, so it returns one everywhere.
It is right twice by coincidence.
It is also known wrong — `D-034` records two `n = 5` rows sharing side `2.767766952966`
while differing geometrically, which this relation would merge without evidence.

Running the quotient controls alone, three of the four candidates survive.
The labelled controls are what separate them, because their proved answers are `2` and
`24` rather than `1`.

**An acceptance rule whose every control has the same answer cannot distinguish a
relation that merges correctly from one that merges indiscriminately.** That is the
generalizable half of this report, and it is not specific to identity: any criterion
validated only on cases whose answer is one is validated against a constant.

## What the Two Controls Actually Isolate

They are not two instances of one test.
They fail differently, and each isolates one of the two independent reasons the atlas
key disagrees with a component count:

- **`n = 4` is pure symmetry.** Twenty-four isolated labelled grids, no connectivity
  anywhere, and a `D4 x S4` quotient that is a single point.
  A relation that does not quotient reports `24` where the answer is `1`.
- **`n = 3` is pure connectivity.** One orbit, one interval, three strata, and two
  contact certificates on it.
  A relation that does not merge along closure reports `2` where the answer is `1`.

So `distinct_basins` is wrong twice over, and the two errors compose rather than
cancelling.
It is a **strict upper bound** on the number of connected terminal components
under `D4 x S_n`, and strict on both controls.

## What Is Not Established

**This is not a component counter.** `contact + closure` survives four proved answers;
it has not been shown to decide the relation in general, and the closure data it needs
is retained for `n = 3` because an exhaustive classification produced it.
At `n = 5` no such classification exists, which is why `H-032`’s instrument readiness is
still false there.

**The `n = 4` samples are not retained**, so the relation the atlas uses today cannot be
scored on the control that would most directly test it—the instrument reports
`undecidable` rather than guessing.
Retaining per-sample keys for `exp-015` would close that, and is cheap.

**Nothing here moves `D-034`.** It stays outstanding: its fix requires certifying
connected terminal components under a fully specified quench and quotient, and this
report neither specifies the quench nor certifies anything at `n >= 5`. What it removes
is the possibility of closing `D-034` against a rule that a merge-everything relation
would have passed.

## Addendum, 2026-08-30 — What Retaining the `n = 4` Keys Showed

`BC-082` retained the per-sample keys this report said were missing, and the instrument
then contradicted two things above.
The conclusion is unchanged — `contact + closure` is still the sole survivor of all four
proved answers — but two of the arguments for it were wrong, and the second one changes
what `BC-083` should look for.
Both corrections are `D-375`.

**`geometric + contact` is a quotient relation, not a labelled one.** The table declared
it `labelled` and refuted it on the `n = 3` labelled control.
But both its inputs are canonical under relabelling and under `D4` *by construction*:
`geometric_key` sorts the squares and minimises over the eight container images, and
`contact_certificate` does the same.
This report made exactly that argument for `contact alone` and `contact + closure` —
that scoring a quotient invariant against a labelled control refutes it for doing what
it is built to do — and did not apply it here.
Scored at its true level it is refuted by the `n = 3` quotient control, `4` against a
proved `1`, which is `D-034` and is the refutation that was always carrying the weight.

The corrected row, and the corrected count below it:

| Relation | Level | `n=3` labelled (2) | `n=3` quotient (1) | `n=4` labelled (24) | `n=4` quotient (1) |
| --- | --- | --- | --- | --- | --- |
| geometric + contact | quotient | — | **4 refuted** | — | 1 agrees |

**Two of the four candidates survive the quotient controls alone, not three.** The
finding this report exists for is unaffected: `side alone` and `contact + closure` are
still indistinguishable there, so the rule as written still cannot separate a relation
that merges correctly from one that merges indiscriminately.

**`distinct_basins` is wrong once, not twice, and the “strict upper bound” argument
loses half its support.** The `n = 4` symmetry failure above is a failure of *a relation
that does not quotient*, and `distinct_basins` is not that relation — it quotients by
`D4` and by relabelling before it hashes.
On the `n = 4` quotient control it reports `1` against a proved `1`, correctly.
So the two errors do not compose, because there is one error: the geometric key’s
quantization splitting a connected family, which is `D-034`. Whether `distinct_basins`
bounds the quotient component count from above now rests on that single mechanism rather
than on two, and is not re-established here.

**The `n = 4` labelled control refutes every candidate and separates none of them.** Its
24 states differ only by relabelling, and every relation in the table is relabelling
invariant, so each reports `1` against a proved `24`.

> A control whose answer no candidate can produce refutes the whole family and separates
> nothing. That is the dual of this report’s own finding, where every control’s answer
> was one and everything passed.

This is the measured reason `BC-083` asks for an `n = 5` control whose proved count is
*neither one nor the labelled count*. A control at either extreme is uninformative, and
which extreme it sits at decides whether it passes everything or fails everything.
`think-byc6` is closed by this addendum.

## The Next Bounded Question

Not a larger census.
Whether the `n = 5` case can be given a discriminating control at all—one whose proved
component count is neither `1` nor equal to its labelled count—because until such a
control exists, any `n = 5` identity claim is being validated against a constant in
exactly the way this report describes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
