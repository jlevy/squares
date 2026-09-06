# T-022 Dilation-Limit Corollary, Derived from T-018

The retained T-018 certificate implies the exact weak bound

```text
s(11) >= 38100*sqrt(8100042893309449)/899996306539
      = 3.8100257236147034071933954110...
```

T-022 is a limit corollary, not a certificate at the displayed endpoint.
It neither decides whether eleven squares fit at that endpoint nor proves a strict lower
bound.

## One-Minute Proof

T-018’s frozen measure has total mass below `11`, and every side-`B` square at a net
direction inside the container carries mass at least `1`. Its full replay accepts
Conditions 1–5. For `0 <= t <= D < 1`, the identity
`(1 + D)^2(1 + t^2) - (1 + t)^2(1 + D^2) = 2(D - t)(1 - Dt) >= 0` bounds the angular
support by `(1 + D)/sqrt(1 + D²)`. Hence every positive rational `q` with
`q²B²(1 + D)² < 1 + D²` gives strict containment after common scaling.
Symmetry and coverage scale with the geometry while mass and the direction net stay
fixed, so the same counting contradiction rules out side `qL`. Rational density supplies
such a `q` above every real side smaller than
`S* = 38100*sqrt(8100042893309449)/899996306539`; upward embedding then rules out every
side below `S*`, proving `s(11) >= S*`. As a sanity check, `q = 500003/500000` yields
the valid side `3.81002286`, already beyond the old coarse ceiling.

## Frozen Premise

The source is [`certificate.json`](certificate.json), SHA-256
`b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a`. Its exact parameters
are

```text
L = 381/100
B = 9977/10000
D = 207107/90000000
B(1 + D) = 899996306539/900000000000 < 1
```

The full source replay accepts Conditions 1–5, including total mass `434547/40000 < 11`
and least reachable-cell mass `4001/4000 >= 1`. The machine-readable
[`t-022-dilation-limit-corollary.json`](t-022-dilation-limit-corollary.json) parses and
hashes one byte snapshot, checks that the path did not change during replay, and records
every accepted source condition.

## Sharpened Containment Lemma

The frozen certificate theorem uses the sufficient condition `B(1 + D) < 1`. The support
calculation inside its proof yields a sharper condition.
For angular error `d`, put `t = tan(d)`. The net gives `0 <= t <= D`, and `D < 1`. The
exact identity

```text
cos(d) + sin(d) = (1 + t)/sqrt(1 + t^2)
```

and the factorization

```text
(1 + D)^2(1 + t^2) - (1 + t)^2(1 + D^2)
  = 2(D - t)(1 - Dt) >= 0
```

show that

```text
cos(d) + sin(d) <= (1 + D)/sqrt(1 + D^2).
```

After a positive rational dilation `q`, strict containment therefore holds whenever

```text
q^2 B^2(1 + D)^2 < 1 + D^2.                 (1)
```

All quantities in (1) are rational.
This lemma is separate from the frozen source’s coarser Condition 4; a scaled instance
may satisfy (1) even when it fails `qB(1 + D) < 1`.

## The Strict Rational Family

Let

```text
A = 90000000^2 + 207107^2 = 8100042893309449,
c = sqrt(1 + D^2)/(B(1 + D))
  = 10000*sqrt(A)/899996306539
  = 1.0000067516049090307594213677...
```

For every rational `q` with `q > 0` and `q^2 < c^2`, multiply every atom coordinate,
`L`, and `B` by `q`, leaving the weights and direction net unchanged.
Condition 1 is equivariant under common scaling.
Conditions 2 and 3 are unchanged.
Inverse dilation is a bijection on admissible placements and preserves covered mass, so
Condition 5 is unchanged.
Equation (1) supplies strict containment in place of the source theorem’s coarse
Condition 4. The source proof then rules out a packing at side `qL`.

The rational factor

```text
q = 500003/500000
qL = 190501143/50000000 = 3.81002286
```

lies strictly above the old coarse ceiling `900000000000/899996306539`. The frozen
Condition 4 rejects it, but the sharpened test has positive exact slack

```text
(1 + D^2) - q^2 B^2(1 + D)^2
  = 33822158946641039188838841479
    /22500000000000000000000000000000000 > 0.
```

This control proves that the sharpened family is larger than the coarse rational family
rather than a different expression for the same ceiling.

## Density and the Infimum

Fix any real `x` with `0 <= x < cL`. Rational density supplies a rational `q` such that
`x/L < q < c`; because both sides are positive, this is equivalent to the rational test
`q^2 < c^2`. If a packing existed at side `x`, placing its container inside the larger
square of side `qL` would give a packing there, contradicting the strict-subfactor
proof. Hence no real side below `cL` is packable.

By the definition of `s(11)` as the infimum of packable container sides,

```text
s(11) >= cL
      = 38100*sqrt(8100042893309449)/899996306539.
```

The endpoint is the positive root of

```text
809993351783841654158521*x^2
  - 11758103264356929262890000 = 0.
```

The proof uses neither compactness nor attainment of the infimum.

## Endpoint and Scope

At `q = c`, equation (1) is an equality.
A finite net gap attains `D`, and its midpoint realizes the corresponding maximum
angular error, so this uniform strict-containment argument cannot include the endpoint.
It supplies none of these stronger claims:

- the retained data form a certificate at `cL`;
- no packing exists at `cL`;
- `s(11) > cL`.

The value `cL` is the supremum for uniform dilation with the fixed `B`, one concentric
core per unit square, and this strict support-containment lemma.
It is not proved to be the strongest consequence of the retained atoms or coverage
cells. Direction-specific cores or an argument using cell geometry may yield more from
the same source data.

## Replay

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.dilation_corollary \
  cases/n11_fractional_certificate/certificate.json \
  --source-name packing/cases/n11_fractional_certificate/certificate.json \
  --check-limit-record cases/n11_fractional_certificate/t-022-dilation-limit-corollary.json
```

The command replays Conditions 1–5 from the exact source bytes, proves the separate
sharpened-containment record, and compares it with the checked-in record.
It is part of `packing-validate`’s fast exact-verification step.
Focused arithmetic, positive, and refusal controls are in
[`test_dilation_corollary.py`](../../tests/test_dilation_corollary.py).

The scoped novelty search is recorded in the
[`2026-09-06 endpoint literature audit`](../../resources/web/s11-exact-endpoint-literature-audit-2026-09-06/README.md).
A negative search is supporting evidence, not proof of priority.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
