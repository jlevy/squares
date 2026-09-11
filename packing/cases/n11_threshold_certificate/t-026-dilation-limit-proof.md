# T-026 Dilation-Limit Corollary of the Threshold Certificate on a Finer Net

The frozen T-025 threshold atoms, placed on a finer direction net at the larger shrunken
side that net admits and rescaled by one rational factor, form a threshold certificate
of the retained form whose sharpened dilation family proves the exact lower bound

```text
s(11) >= 955000*sqrt(518400042893309449)/179696714646249
      = 3.82644741057293974417...
```

T-026 proves this ordinary lower bound by a dilation-limit argument: the strict rational
certificate family approaches the displayed side from below, and rational density plus
upward embedding establishes the `>=` conclusion at its supremum.
The record’s `endpoint_certificate: false` says only that this proof supplies no single
certificate at the displayed side.
It does not weaken the theorem or its evidence.
The method does not establish a `>` conclusion there.
The new result raises the proved lower bound by `0.0064474` beyond T-025’s
`191/50 = 3.82`; T-025 continues to supply an individual-side certificate at `3.82`.

The registered rung is the threshold certificate on the 1440-step net, `C_1440`. The
same certificate on the 720-step net, `C_720`, is retained beside it: its own dilation
family reaches
`955000*sqrt(129600042893309449)/89874194646249 = 3.82534784591311198085...`, and it is
the control that isolates where the extra `0.0011` comes from.
The standalone [T-026 verifiable claim](t-026-verifiable-claim-dilation-limit.md) embeds
a standard-library reader, the 1440-step certificate, and the exact dilation record.
It checks this registered rung without importing the repository package.

## One-Minute Proof

T-025’s frozen atoms — 584 point atoms and 320 threshold atoms, every one `2`-of-`3` —
were optimised against a 181-direction net with shrunken side `B0 = 9977/10000`.
Condition 4 ties the shrink to the net’s largest half-gap tangent `D`: a finer net has a
smaller `D` and admits a larger `B`. A finer net also adds directions at which
`Condition 5'` must hold, and on these atoms it costs more than it does on point atoms:
at the certificate’s own shrink the least charge over the 1440-step net falls to
`973862153/1000000000`, below the covering threshold `M/11 = 685457679/687500000`, so
the frozen shrink does not survive the refinement.

The measurement behind this corollary is that the same atoms, with the same weights, do
charge every closed `B`-square at every direction of the 1440-step net
`t_k = T k / 1440`, `T = 207107/500000`, at least `m = 498684619/500000000` once
`B = 249507/250000`, the least rational shrink on a `10^-7` grid at which the least
charge over the finer net stays above `M/11`; one grid step below it, at
`9980279/10000000`, the net does not cover.
The binding direction is unique: `k = 914`, `t = 94647899/360000000`, about `29.46°`.
Both conditions of the threshold theorem that mention the weights are homogeneous in
them, so multiplying every weight by `1/m` restores `Condition 5'` with least cell
charge exactly `1` and leaves the total budget at
`M/m = 5483661432/498684619 = 10.996251384 < 11`. Conditions 1, 1', 2', 3 and 4 hold in
closed form. So `C_1440` is a threshold certificate of the retained form at side
`191/50`.

The rest is T-022’s and T-024’s argument with the new `B` and `D = 207107/720000000`,
and it needs no new theorem.
For `0 <= t <= D < 1` the identity
`(1 + D)^2 (1 + t^2) - (1 + t)^2 (1 + D^2) = 2 (D - t)(1 - D t) >= 0` bounds the angular
support factor by `(1 + D)/sqrt(1 + D^2)`, so every positive rational `q` with
`q^2 B^2 (1 + D)^2 < 1 + D^2` gives strict containment after common scaling.
Conditions 1 and 1' are equivariant under common scaling once every threshold atom’s
points scale with the point atoms; Conditions 2' and 3 do not move, because the weights,
the thresholds and the net are untouched; and `Condition 5'` is preserved by inverse
dilation of placements for the reason `Condition 5` is — the charge of a core is a
function of which atom points it contains, dilation is a bijection on placements, and it
preserves containment, so a core’s trace on each threshold atom’s scaled points is the
trace of its preimage on the unscaled points.
The counting contradiction then rules out side `q · 191/50`. Rational density supplies
such a `q` above every real side below the supremum
`S* = (191/50) · sqrt(1 + D^2) / (B (1 + D))`, and upward embedding rules out every side
below `S*`. Hence `s(11) >= S*`, using the infimum definition of `s(11)`, not
compactness or attainment.

## Frozen Premises

| Certificate | Bytes | Shrink `B` | Net | Least unscaled charge | Total budget |
| --- | --- | --- | --- | --- | --- |
| `C_1440` | [`certificate-191-50-net1440.json`](certificate-191-50-net1440.json), SHA-256 `dc2da20c75d952690c93d67fb4b3eb8552e879585902fde98eedc9b3179ed3d0` | `249507/250000` | `1440` steps, `D = 207107/720000000` | `498684619/500000000` at `k = 914` | `5483661432/498684619` |
| `C_720` | [`certificate-191-50-net720.json`](certificate-191-50-net720.json), SHA-256 `fff8b2bcab95a0041e69fec30c704dd708908125883b6ed645bc2c653ecbf8cf` | `249507/250000` | `720` steps, `D = 207107/360000000` | `498684619/500000000` at `k = 457` | `5483661432/498684619` |

Both are the T-025 atoms (source SHA-256
`3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c`) with every weight
multiplied by `500000000/498684619`; the atom positions, the threshold atoms’ points and
thresholds, the container side `191/50` and the D4 symmetry are unchanged.
Of the rescaled budget, `4336840816/498684619 = 8.696560212` is point mass and
`1146820616/498684619 = 2.299691172` is threshold budget.
Each certificate’s own claim is `s(11) >= 191/50`, the side T-025 already holds as an
endpoint; the new content is the corollary below.

**The crossing shrink is the same at both nets.** `249507/250000` covers at 720 steps
and at 1440 steps, with the same least charge `498684619/500000000` and the same binding
angle `t = 94647899/360000000` — index `457` in the 720-step net and `914` in the
1440-step net, the same direction under the nesting `t_k = T k / N`. The two records
differ in `direction_steps` and in nothing else, so the extra `0.0011` the 1440-step
rung buys comes from `D` halving alone, not from a larger shrink.
That is why `C_720` is retained beside the registered rung: it is decidable by the exact
sweep in about a fifth of the time and it is the control on where the movement comes
from.

The two-route retention gate (`devtools.decide_threshold_certificate`) accepts both.
For `C_1440` the interval route returns the width-zero enclosure `(1, 1)` over
`11,892,823` boxes on `2881` doubled-net directions with none stalled and none
budget-exhausted, and the exact event-cell sweep returns least cell charge exactly `1`
at direction `914`, with the dense-grid and slab evaluations agreeing at every direction
and the charge re-evaluated at the witness by membership counting.
For `C_720` the same two routes return `(1, 1)` over `5,944,975` boxes on `1441`
directions, and least cell charge exactly `1` at direction `457`. Each file declares
`least_cell_charge` as `1`, which both routes are then held to; the declaration is the
one edit made to the measured bytes before they were retained here.

## Sharpened Containment and the Strict Rational Family

For `C_1440`, put `A = (720000000)^2 + 207107^2 = 518400042893309449`; the factor
supremum is

```text
c = sqrt(1 + D^2)/(B (1 + D)) = 250000*sqrt(A)/179696714646249
  = 1.00168780381490569219...
```

For every rational `q` with `0 < q` and `q^2 < c^2`, multiplying every point atom’s
coordinates, every threshold atom’s points, `L` and `B` by `q`, and leaving the weights,
the thresholds and the net unchanged, gives a valid threshold certificate at side `q L`.
The control rational `q = 100168777/100000000`, `qL = 19132236407/5000000000 =
3.8264472814`, lies strictly above the coarse Condition 4 ceiling
`76400000000000/19966301627361 = 3.826447252...` and has exact positive slack

```text
(1 + D^2) - q^2 B^2 (1 + D)^2
  = 21875139388017997436352028517441994271 / 324000000000000000000000000000000000000000000 > 0,
```

so the sharpened family is strictly larger than the coarse rational family here too.
The side supremum `cL = 955000*sqrt(A)/179696714646249` is the positive root of

```text
32290909254655439869209770001*x^2 - 472793799119770550224225000000 = 0.
```

For `C_720` the same computation with `A' = (360000000)^2 + 207107^2 =
129600042893309449` gives
`c' = 250000*sqrt(A')/89874194646249 = 1.00139995966311831959...`, side supremum
`955000*sqrt(A')/89874194646249`, the positive root of
`8077370863311852414249770001*x^2 - 118198479119770550224225000000 = 0`, and the control
`q = 5006999/5000000`, `qL = 956336809/250000000 = 3.825347236`, above the coarse
ceiling `38200000000000/9986021627361 = 3.825347212...` with exact positive slack
`64573179319590516732280982491243999 / 202500000000000000000000000000000000000000`.

## Endpoint and Scope

At `q = c` the sharpened test is an equality; a finite net gap attains `D` and its
midpoint realises the maximum angular error, so the uniform argument cannot include the
endpoint. Nothing here claims that the frozen data form a certificate at `cL`, that no
packing exists at `cL`, or that `s(11) > cL`. T-025’s `191/50` remains the largest side
at which this project holds an endpoint certificate.
This limit on the method does not weaken the exact conclusion `s(11) >= cL`, which
follows from the whole strict family by density and upward embedding.

The value is the supremum for uniform dilation of these atoms with one concentric core
per square and strict support containment on the 1440-step net.
At 1440 steps the rescaled budget is `5483661432/498684619 = 10.996251384`, leaving
`1869377/498684619` below eleven.
The frozen certificate’s budget was `10.967323`. At the original shrink the complete
mixed certificate’s least charge falls from `1.00000203` to `0.973862153` on the
1440-step net; the larger admitted shrink partly recovers it.
These are measurements of the complete certificate, not of the two-of-three component
separately. These figures describe the measured 1440-step certificate.
They do not decide another net and do not prove that refinement of the frozen atoms is
exhausted. Re-optimizing the atoms at a finer net, retaining them on another net, and
changing the atom family remain separate hypotheses.
The 360-step rung of the same family (side supremum
`38200000*sqrt(32400042893309449)/1798171928825841 = 3.82388604850764671009...`) is
retained in the lane document only, not as a case file.
The lane report
[`lane-a2-threshold-certificate-on-finer-nets.md`](../../campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a2-threshold-certificate-on-finer-nets.md)
records the measurements, the crossing brackets and what remains open.

## Replay

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.decide_threshold_certificate \
  cases/n11_threshold_certificate/certificate-191-50-net1440.json
uv run --frozen --all-extras --group dev python -m devtools.dilation_corollary \
  cases/n11_threshold_certificate/certificate-191-50-net1440.json \
  --source-name packing/cases/n11_threshold_certificate/certificate-191-50-net1440.json \
  --check-limit-record cases/n11_threshold_certificate/t-026-dilation-limit-corollary.json
```

The first decides the certificate by both routes (936 s on two workers of a four-cpu
host, 782 s of it the exact sweep), and the second replays Conditions 1, 1', 2', 3, 4
and 5' from the bytes and re-derives the limit record.
The same two commands with `certificate-191-50-net720.json` and
`t-026-net720-dilation-limit-corollary.json` decide the 720-step rung, at about half the
cost. Both replays are deferred validation steps rather than pull-request ones, for that
reason. The retained instrument that produced the crossing shrinks is
`devtools.measure_threshold_net_refinement`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
