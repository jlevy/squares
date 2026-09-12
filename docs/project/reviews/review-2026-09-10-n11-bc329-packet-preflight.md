# BC329: Preflight of the 2880-Step Threshold Packet

Date: 2026-09-10. Bead: `think-17qa`. Scope: read-only review of the retained
T-025/T-026 sources and target-free rational arithmetic at revision
`3a18a05a6af75e3800612549d5a3c5fe419b96f2`.

**Verdict: CONDITIONAL.** The proposed geometry has an exact dilation limit above T-026,
and its net and containment parameters are valid.
The experiment is a coherent single candidate once it explicitly fixes the common
weight-normalization rule.
Its coverage is unmeasured.
Before execution, register that rule and provide a bounded fixed-core runner; the
existing refinement CLI performs a different, adaptive experiment.
No scientific target, coverage sweep, or certificate replay was run for this preflight.
No repository file was changed.

## 1. The Candidate and the Question

A **core** is a closed square of side `B` inside the container `[0,L]^2`. Its
orientation belongs to a finite **direction net**. A point atom contributes its weight
when its point belongs to the core.
A threshold atom `(S,k,w)` contributes `w` when the core contains at least `k` distinct
points of `S`. Its counting budget is `w floor(|S|/k)` because disjoint cores can each
consume at least `k` points of `S` only that many times.

BC329 retains the exact T-025 coordinates, threshold sets, threshold integers, and
relative weights in `packing/cases/n11_threshold_certificate/certificate.json`:

| Quantity | Frozen value |
| --- | --- |
| Number of unit squares | `n=11` |
| Container side | `L=191/50` |
| Point atoms | 584 |
| Threshold atoms | 320, all two-of-three |
| Distinct atom sites | 1440 |
| Original total budget | `M=685457679/62500000` |
| Candidate core side | `B_c=9981/10000` |
| Half-tangent limit | `T=207107/500000` |
| Half-tangent net | `t_k=T k/2880`, `k=0,...,2880` |
| Symmetry | D4, the eight symmetries of the container |

The scientific question is whether the least original-weight charge `m_c` over every
admissible core on this net satisfies

```text
m_c > M/11 = 685457679/687500000.
```

That strict comparison is the necessary and sufficient condition for *some common
positive rescaling of these relative weights* to meet both the coverage and budget
conditions at the fixed `(L,B_c,net)`. It does not optimize the relative weights.

## 2. The Half-Gap Is Correct

The physical direction corresponding to a half-tangent `t` is `theta=2 arctan(t)`. For
consecutive net directions, the greatest error from choosing the nearer endpoint is half
their angular gap. Its tangent is

```text
tan((theta_(k+1)-theta_k)/2)
  = (t_(k+1)-t_k)/(1+t_k*t_(k+1)).
```

Here the numerator is constant, `h=T/2880`, while the denominator is `1+k(k+1)h^2`,
which increases for nonnegative `k`. The maximum occurs at `k=0`, where the denominator
is exactly one. Therefore

```text
D_c = T/2880 = 207107/1440000000.
```

This is the tangent of the worst nearest-direction error, not the full angular gap, and
no further factor of two is needed.
The endpoint reaches the required direction because

```text
T^2+2T-1 = 309449/250000000000 > 0,
```

so `2 arctan(T)>pi/4`. There are 2881 directions in the exact route.
The interval route includes reflected directions and checks 5761 directions.
Those counts were checked by constructing the nets, without checking coverage.

Sources: `packing/devtools/measure_net_refinement.py:half_gap_tangent`, `uniform_net`;
`packing/devtools/decide_threshold_certificate.py:load`;
`packing/src/sqpack/fractional/interval.py:doubled_net`.

## 3. The Geometric Ceiling Strictly Exceeds T-026

For a unit parent and a concentric core with angular error `d`, the core’s width across
either parent edge normal is `B(cos d+sin d)`. Writing `t=tan d`, the support factor is
`(1+t)/sqrt(1+t^2)`. For `0<=t<=D_c<1`, this is at most `(1+D_c)/sqrt(1+D_c^2)`.

Even the retained theorem’s coarser strict containment test passes:

```text
B_c(1+D_c) = 1597189681663/1600000000000 < 1,
1-B_c(1+D_c) = 2810318337/1600000000000 > 0.
```

The sharpened test has exact positive slack

```text
1+D_c^2-B_c^2(1+D_c)^2
  = 727799073259767345908911/207360000000000000000000000 > 0.
```

If coverage and budget pass, simultaneous dilation of the container, sites and cores by
any positive rational factor `q` satisfying `q^2 B_c^2(1+D_c)^2 < 1+D_c^2` preserves the
certificate. The supremum of the resulting side lengths is

```text
S_c = L sqrt(1+D_c^2)/(B_c(1+D_c))
    = 38200*sqrt(2073600042893309449)/14374707134967
    = 3.826721480476156460836881960548...

S_c^2 = 3025880126591632880358760000/206632205216071177554091089.
```

T-026’s retained limit `S_0` has square

```text
S_0^2 = 472793799119770550224225000000/32290909254655439869209770001.
```

The exact comparison is

```text
S_c^2-S_0^2 =
172780970782362059122794111267531069282784376960000 /
82374589971870306695869445414254003282960743287575569 > 0.
```

Both sides are positive, so `S_c>S_0`. Their decimal difference is approximately
`0.0002740699032167167`. The rational side `23917/6250=3.82672` lies strictly between
them; both comparisons also pass by exact squaring.
These are geometric headroom calculations conditional on coverage, not new lower bounds.

The direct formula agrees exactly with
`packing/devtools/dilation_corollary.py:sharp_dilation_ceiling` applied to the candidate
object and multiplied by `L`. The comparison control is
`packing/cases/n11_threshold_certificate/t-026-dilation-limit-corollary.json`.

For this net, any core side `B` that improves T-026 through the same formula must
satisfy

```text
B^2 < L^2(1+D_c^2)/((1+D_c)^2 S_0^2),
B < 0.998171489070944698015287962789...
```

Thus `B_c=0.9981` leaves some geometric room above itself.
A failed test at `B_c` does not eliminate a successful larger core below this upper
limit. Nor would a pass at `B_c` prove that it is the best core side on this net.

## 4. The Missing Normalization Rule

For a common weight multiplier `alpha>0`, least charge becomes `alpha m_c` and budget
becomes `alpha M`. The two required inequalities are

```text
alpha*m_c >= 1,
alpha*M < 11.
```

They have a solution precisely when `m_c>M/11`. A deterministic normalization is
`alpha=1/m_c`; the resulting certificate has least charge exactly one and budget
`M/m_c<11`. This must be declared before the target.
The measured `m_c` then determines the derived bytes by a frozen rule rather than by an
additional search.

An admissible core of original-weight charge at most `M/11` refutes this fixed
relative-weight packet: its charge is an upper bound for `m_c`. Equality refutes it too,
because the budget inequality is strict.
A core of charge merely below one does **not** refute the packet.
It may still permit an acceptable rescaling.

The T-026 source uses the factor

```text
alpha_0 = 500000000/498684619,
m_0 = 498684619/500000000,
m_0-M/11 = 1869377/5500000000 > 0.
```

Target-free comparison confirmed that its point coordinates, threshold sets and
threshold integers equal T-025’s, and every weight has the same factor `alpha_0`. BC329
can use either source as its relative-weight representation, but its record must state
which original budget and charge scale define the acceptance threshold.
Freezing the *absolute* T-026 weights instead would be a narrower experiment.

No crossing-shrink premise is missing for the proposed fixed `B_c`. A crossing search
asks for the least passing core side and is a separate experiment.
The current proposal needs one exact minimum at its one declared core side.

This weight normalization is distinct from the later geometric dilation.
During the coverage test, coordinates and `L` stay fixed.
The later dilation changes coordinates, `L`, and `B` together, while retaining the
normalized weights.

## 5. What Existing Evidence Does and Does Not Supply

T-026 verifies all 1440-step directions at `B_0=249507/250000`. Since
`B_c-B_0=9/125000>0`, every such direction remains above the original threshold:
increasing the core side increases its charge at each remaining center and reduces the
admissible-center domain.
The 2880-step net contains the 1440-step net, so only the inserted directions introduce
unknown exploratory coverage obligations.
The final retention gate should still run its complete exact and reflected interval nets
on the same normalized bytes.

The retained measurements at the original `B=9977/10000` show failures on the 360-,
720-, and 1440-step nets.
They do not determine the changed core side.
The reported passing crossings at 720 and 1440 steps do not imply the same crossing at
2880 steps. The small T-026 budget margin supplies no exhaustion theorem.

The source lane retains summaries but explicitly does not retain its 48 per-direction
logs. A new runner must not reconstruct a cache of exact witnesses from their absence or
describe the summaries as full per-direction replay artifacts.
Earlier LP results at `383/100` concern different geometry and column sets; they do not
decide BC329.

Sources: `packing/cases/n11_threshold_certificate/t-026-dilation-limit-proof.md`;
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a2-threshold-certificate-on-finer-nets.md`;
the adjacent `lane-a2-summary-N720.json`, `lane-a2-summary-N1440.json`, and
`lane-a3-threshold-loop-at-383-100.md`.

## 6. Freeze Before Execution

The prospective hypothesis and experiment should identify the following inputs and
decisions:

1. The clean implementation revision, exact T-025 source path, and T-026 comparison
   record. Preserve atom order, all coordinates, threshold membership and integers, and
   relative weights. Record the frozen accepted artifact identity through the existing
   verifier’s byte-binding mechanism.
2. `n`, `L`, `B_c`, `T`, the uniform-net formula, the 2881 and 5761 direction counts, D4
   symmetry, and the unrestricted admissible-core domain.
   No owner conditions, selected angle classes or pose truncation enter this experiment.
3. The exact original budget `M`, the criterion `m_c>M/11`, and the deterministic
   normalization `alpha=1/m_c`. Derive all declared mass and budget fields from the
   transformed weights; declare `least_cell_charge="1"` in the final candidate.
4. One fixed core size, with no automatic bisection or fallback value.
   Any changed core, angle net, site, threshold or relative weight belongs to another
   registered packet.
5. The exact coverage implementation, interval implementation, integer-mass limits,
   interval resolution floor, and per-direction box budget.
   Record workers, host, complete direction dispositions, rational witnesses and totals,
   source identities, and retained logs.
6. A supervised worker-process deadline and atomic process-level partial output,
   including the normalized gate and the dilation record’s additional source replay.
   The parent-side Git, runtime, and source preflight currently precedes that clock and
   must be bounded before target registration.
   Any staged deadlines must be fixed before the target; an incomplete stage cannot
   silently acquire another budget.
7. The outcome table below and the scope of any rejection.
   Preserve every completed direction observed by the coordinator when a timeout or
   invalid invocation stops the run.

Runner admission is not a BC329 measurement.
It uses a separate `fixed-core-packet-calibration/v1` receipt and a frozen known-answer
fixture that exercises the real raw, exact, interval, dilation, publication, and
per-direction readback paths at the full 14,404-record shape.
That schema cannot carry a scientific acceptance and the scientific reader refuses it.
Three fresh runs price operational overhead on the intended host; their timing does not
bound the harder BC329 computation.
A source-distinct reader must accept the calibration receipts before the target is
registered.

The branch now contains the maintained fixed-packet entry point
`packing/devtools/fixed_core_packet.py`. It binds the T-025 and T-026 source bytes,
project runtime, and complete local implementation manifest; keeps raw and exact
submissions bounded; retains coordinator-observed direction rows; checks the normalized
candidate through exact, interval, and dilation routes; and rejects incomplete evidence
as scientifically unresolved.
Its target-free controls currently pass 156 tests with three platform skips, and an
independent source review found no acceptance-safety blocker in the current
implementation. That establishes the implementation checkpoint only.

The older `packing/devtools/measure_threshold_net_refinement.py:main` remains an
adaptive core-sweep and bisection tool.
Running it with `--nets 2880` does not execute this one fixed packet.
Before the fixed-packet runner is admitted for BC329, the separate full-shape
calibration must pass three host runs and source-distinct readback.
The parent preflight must gain a bounded clock, and partial interval and dilation
receipts must name their exact published direction sets.
None of those remaining tasks asks the BC329 coverage question.

The raw sweep should precede the normalized retention gate.
Feeding the original weights directly to `decide_threshold_certificate` and treating its
below-one refusal as the packet verdict would use the wrong acceptance threshold.

The interval input size guard passes without a coverage run: 1440 distinct sites, 904
atoms, and a `904 by 3` member table.
Original weight denominators divide `10^9`; the original integer budget is
`10967322864`. A measured minimum is an integer multiple of `10^-9`, so normalization
preserves an exact integer representation well below the verifier’s `2^62` limit.
This does not guarantee that interval boxes avoid seams, resolve within their budget, or
finish within the wall deadline.

## 7. Acceptance and Outcome Boundaries

| Outcome | Required evidence | Permitted inference |
| --- | --- | --- |
| Accept | Exact `m_c>M/11`; normalized bytes pass all closed-form conditions; the complete exact and interval routes accept and agree at minimum one; dilation replay produces the exact `S_c>S_0` record | A stronger unconditional lower bound `s(11)>=S_c` |
| Reject this relative-weight packet | One independently re-evaluated admissible rational core with original-weight charge `<=M/11`, or a fully checked minimum implying normalized budget `>=11` | These fixed sites, threshold atoms, relative weights, core side and net cannot satisfy the retained criterion under any common scaling |
| Unresolved | Timeout, incomplete directions, interval stalls, exhausted box budgets, or a nonzero-width enclosure without a verified refuting witness | The planned run did not decide the packet |
| Invalid | Mutated or mismatched sources, malformed declarations, wrong geometry, disagreement between methods, or a purported witness failing exact membership/admissibility checks | Repair the instrument or invocation; no scientific verdict |

For the registered target, use `packing/devtools/fixed_core_packet.py` at the exact
admitted implementation revision.
Direct calls to `packing/devtools/decide_threshold_certificate.py` or the
arithmetic-only dilation calculation do not establish the packet result.
The runner requires every exact direction, zero dense/slab disagreements, exact witness
membership agreement, every interval direction, zero stalled boxes, zero exhausted
direction budgets, a zero-width enclosure equal to the exact minimum, and a dilation
record that replays its normalized source.

At the limiting dilation factor, the strict containment inequality becomes equality.
Success therefore proves the lower bound through all strict rational subfactors and
order completeness. The conclusion is the ordinary exact lower bound `s(11)>=S_c`.

The argument would not establish the separate strict inequality `s(11)>S_c`. This would
not qualify the proved lower bound.
A rejection does not decide other core sides, other nets, reoptimized relative weights,
changed atoms or conditional geometry.

## 8. Preflight Checks Performed

Using only `packing/.venv/bin/python3` (project Python 3.14), the review decoded the
retained records, recomputed budget and source scaling, constructed the proposed nets,
verified the half-gap formula, checked the closed-form conditions and interval input
sizes, and compared the proposed squared surd against T-026 with exact `Fraction`
arithmetic. The formula agreed with the maintained dilation helper.
Decimal renderings used 70-digit `Decimal` arithmetic after exact decisions.

All those target-free mathematical checks passed.
The runner’s target-free unit and integration controls also pass, but the full-shape
calibration and its independent readback remain unrun.
BC329 coverage, normalization by its measured minimum, two-route retention, and
dilation-source replay remain unrun.
The packet becomes suitable for prospective registration only after the remaining
admission tasks above are resolved.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
