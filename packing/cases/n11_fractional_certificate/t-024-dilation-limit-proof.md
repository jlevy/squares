# T-024 Dilation-Limit Corollary on a Finer Net, Derived from T-018’s Atoms

The retained T-018 atoms, placed on a finer direction net at a larger shrunken side and
rescaled by one rational factor, form a certificate of the retained form whose sharpened
dilation family implies the exact weak bound

```text
s(11) >= 3175000*sqrt(518400042893309449)/598960960743657
      = 3.81660950278886223509...
```

T-024 is a limit corollary, not a certificate at the displayed endpoint.
It neither decides whether eleven squares fit at that endpoint nor proves a strict lower
bound. It moves the exact lower endpoint by `0.0065838` beyond T-022.

The registered rung is the certificate on the 1440-step net, `C_1440`. A certificate of
the same kind on the 720-step net, `C_720`, is retained beside it: its own dilation
family reaches `38100000*sqrt(129600042893309449)/3594594251080001 =
3.81573031939551396587...`, and it is the rung the standalone reader `verify_claim.py`
also decides from its bytes.
The reader refuses `C_1440` by name, because it decides at most `1000` directions; that
ceiling is a declared property of a retained reader, not of the mathematics, and the
reader was not edited.

## One-Minute Proof

T-018’s frozen atoms were optimised against a 181-direction net with shrunken side
`B0 = 9977/10000`. Condition 4 ties the shrink to the net’s largest half-gap tangent
`D`: a finer net has a smaller `D` and admits a larger `B`. The measurement behind this
corollary is that the same 1121 atoms, with the same weights, cover every closed
`B`-square at every direction of the 1440-step net `t_k = T k / 1440`,
`T = 207107/500000`, with mass at least `m = 198931/200000` once `B = 2494953/2500000`,
the least rational shrink on a `10^-7` grid at which the least mass over the finer net
stays above `M/11 = 434547/440000`; the binding directions are `k = 978`,
`t = 33758441/120000000`, about `31.4°`, and `k = 979`, and one grid step below that
shrink, at `9979803/10000000`, direction `k = 877`, about `28.3°`, covers only
`39001/40000`. Multiplying every weight by `1/m` restores Condition 5 with least cell
mass exactly `1` and leaves the total mass at
`M/m = 2172735/198931 = 10.922053... < 11`. Conditions 1 to 4 hold in closed form.
So `C_1440` is a certificate of the retained form at side `381/100`.

The rest is T-022’s argument with the new `B` and `D = 207107/720000000`. For
`0 <= t <= D < 1` the identity
`(1 + D)^2 (1 + t^2) - (1 + t)^2 (1 + D^2) = 2 (D - t)(1 - D t) >= 0` bounds the angular
support factor by `(1 + D)/sqrt(1 + D^2)`, so every positive rational `q` with
`q^2 B^2 (1 + D)^2 < 1 + D^2` gives strict containment after common scaling; symmetry
and coverage scale with the geometry while the weights and the net stay fixed, and the
counting contradiction rules out side `q · 381/100`. Rational density supplies such a
`q` above every real side below the supremum
`S* = (381/100) · sqrt(1 + D^2) / (B (1 + D))`, and upward embedding then rules out
every side below `S*`. Hence `s(11) >= S*`, using the infimum definition of `s(11)`, not
compactness or attainment.

## Frozen Premises

| Certificate | Bytes | Shrink `B` | Net | Least unscaled mass | Total mass |
| --- | --- | --- | --- | --- | --- |
| `C_1440` | [`certificate-381-100-net1440.json`](certificate-381-100-net1440.json), SHA-256 `0666bf3d8b45e990c33afdf00be45565222ec9441b1212c2e225d52b1da32ac2` | `2494953/2500000` | `1440` steps, `D = 207107/720000000` | `198931/200000` at `k = 978, 979` | `2172735/198931` |
| `C_720` | [`certificate-381-100-net720.json`](certificate-381-100-net720.json), SHA-256 `e7806824a1b313aa0322341ac6fb4fe12ffa1f22db83e219597fee5e7d8f772a` | `9979243/10000000` | `720` steps, `D = 207107/360000000` | `198931/200000` at `k = 489` | `2172735/198931` |

Both are the T-018 atoms (source SHA-256
`b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a`) with every weight
multiplied by `200000/198931`; the atom positions, the container side `381/100` and the
D4 symmetry are unchanged.
Each certificate’s own claim is `s(11) >= 381/100`, the side T-018 already holds; the
new content is the corollary below.

The two-route retention gate (`devtools.decide_certificate`) accepts both: the interval
route returns the width-zero enclosure `(1, 1)` over `11,186,383` boxes with none
stalled for `C_1440` and over `5,681,191` boxes for `C_720`, and the exact event-cell
sweep returns least cell mass exactly `1` for each.
The standalone reader `verify_claim.py` decides `C_720` from its bytes
(`VERIFIED: s(11) >= 381/100`, least covered mass `1` at direction `489`,
`2,266,310,085` cells over `721` directions) and refuses `C_1440` by name because it
exceeds the reader’s `1000`-direction ceiling.

## Sharpened Containment and the Strict Rational Family

For `C_1440`, put `A = (720000000)^2 + 207107^2 = 518400042893309449`; the factor
supremum is

```text
c = sqrt(1 + D^2)/(B (1 + D)) = 2500000*sqrt(A)/1796882882230971
  = 1.00173477763487197772...
```

For every rational `q` with `0 < q` and `q^2 < c^2`, multiplying every atom coordinate,
`L` and `B` by `q` and leaving the weights and the net unchanged gives a valid
certificate at side `q L`. The control rational `q = 100173477/100000000`,
`qL = 38166094737/10000000000 = 3.8166094737`, lies strictly above the coarse Condition
4 ceiling `762000000000000/199653653581219 = 3.816609344...` and has exact positive
slack

```text
(1 + D^2) - q^2 B^2 (1 + D)^2
  = 493882966082381591605089414259023868111 / 32400000000000000000000000000000000000000000000 > 0,
```

so the sharpened family is strictly larger than the coarse rational family.
The side supremum `cL = 3175000*sqrt(A)/598960960743657` is the positive root of

```text
358754232494964621814465733649*x^2 - 5225796432391367564325625000000 = 0.
```

For `C_720` the same computation with `A' = (360000000)^2 + 207107^2 =
129600042893309449` gives
`c' = 10000000*sqrt(A')/3594594251080001 = 1.00150402083871...`, side supremum
`38100000*sqrt(A')/3594594251080001`, the positive root of
`12921107829897393270354902160001*x^2 - 188128718264356929262890000000000 = 0`, and the
control `q = 31297/31250`, `qL = 11924157/3125000 = 3.81573024`, above the coarse
ceiling `13716000000000000/3594594251080001 = 3.815729687...` with exact positive slack
`175562685975750629706766716352597 / 4218750000000000000000000000000000000000`.

## Endpoint and Scope

At `q = c` the sharpened test is an equality; a finite net gap attains `D` and its
midpoint realises the maximum angular error, so the uniform argument cannot include the
endpoint. Nothing here claims that the retained data form a certificate at `cL`, that no
packing exists at `cL`, or that `s(11) > cL`.

The value is the supremum for uniform dilation of these atoms with one concentric core
per square and strict support containment on the 1440-step net.
What the measurement behind it showed is the shape of the remaining room: at the
original shrink the same atoms fail every finer net at an intermediate direction (least
mass `96377/100000`), so the gain comes entirely from the larger shrink the finer net
admits; the 1440-step net adds a direction near `28.3°` that the 720-step crossing
shrink does not cover, so it pays `5.69 · 10^-5` in `B` to halve `D`, and the net gain
over `C_720` is `0.00087918` in side against the `0.0011` a fixed crossing would have
given. The exact ceiling family retained at
`campaign/series/series-000-smoke-and-calibration/results/agenda-034/ceiling-family-191-50.json`
shows that no certificate of this one-body form, at any shrink and on any net containing
its six directions, can pass unit side `3.8288`, that is `L < 3.8288 · B`. The
unit-equivalent side of `C_1440` and `C_720` is `3.8177` and `3.8179`, about `0.011`
below that cap. The exploration
[X-023](../../campaign/explorations/X-023-three-losses-and-a-new-atom.md) records the
measurements and what remains.

## Replay

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.decide_certificate \
  cases/n11_fractional_certificate/certificate-381-100-net1440.json
uv run --frozen --all-extras --group dev python -m devtools.dilation_corollary \
  cases/n11_fractional_certificate/certificate-381-100-net1440.json \
  --source-name packing/cases/n11_fractional_certificate/certificate-381-100-net1440.json \
  --check-limit-record cases/n11_fractional_certificate/t-024-net1440-dilation-limit-corollary.json
```

The first decides the certificate by both routes (about ten minutes on one core), and
the second replays Conditions 1 to 5 from the bytes and re-derives the limit record.
The same two commands with `certificate-381-100-net720.json` and
`t-024-dilation-limit-corollary.json` decide the 720-step rung, and

```bash
uv run --frozen --all-extras --group dev python cases/n11_fractional_certificate/verify_claim.py \
  cases/n11_fractional_certificate/certificate-381-100-net720.json
```

is the standalone reader on that rung (about twenty-three minutes).
The retained instrument that produced the crossing shrinks is
`devtools.measure_net_refinement`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
