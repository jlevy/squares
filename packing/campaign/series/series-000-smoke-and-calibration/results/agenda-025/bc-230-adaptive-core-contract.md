# BC-230 Adaptive-Core Theorem and Certificate Contract

Status: author checkpoint for source-distinct review under agenda-024. This packet
specifies the theorem and serialized decision boundary; it does not claim that an
adaptive verifier or candidate exists.

Launch base: `c55726e1e885227f63110131c0a914665175ff89`\
Frozen preregistration: `f1b6c641e8d3a2fea39cf5aa5292cb8fc1221772`\
Cell: BC-230 (`think-c678`)

## The Exact Object

Fix $n\in\mathbb Z_{\ge 1}$ and $L\in\mathbb Q_{>0}$, and let `C_L = [0,L]^2`. The
resource is a finite nonnegative atomic measure

\[
\mu=\sum_j w_j\delta_{p_j},\qquad p_j\in C_L,\quad w_j\in\mathbb Q_{\ge 0},
\]

on distinct rational sites.
Its nonzero atomic support and weights are invariant under all eight symmetries of
`C_L`. A site on a symmetry axis or at the center occurs once in the serialized atom
list; orbit multiplicity is never added to its mass.
An absent site implicitly has weight zero, so measure-level invariance alone does not
require images of a listed zero-weight point.
The adaptive schema nevertheless treats the explicitly listed site domain as part of its
presentation: a listed zero-weight site must have all of its distinct `D4` images listed
with weight zero, or the entire zero orbit must be omitted.
This is a closed-schema presentation rule, not a premise needed by the counting theorem.
Thus `mu(C_L)` is the sum of the weights at distinct serialized sites, with no orbit
multiplicity.

The direction net is described by rational half-angle tangents

\[
0=t_0<t_1<\cdots<t_K<1,\qquad \alpha_k=2\arctan t_k.
\]

The final two directions straddle the folded endpoint in the following exact sense:

\[
t_{K-1}^2+2t_{K-1}-1<0\le t_K^2+2t_K-1.
\]

For `1 <= k <= K`, define the seam tangent

\[
q_k=\tan\frac{\alpha_{k-1}+\alpha_k}{2}
    =\frac{t_{k-1}+t_k}{1-t_{k-1}t_k},
\]

and set `q_0 = 0`, `q_{K+1} = 1`. The contract requires

\[
0=q_0<q_1<\cdots<q_K<q_{K+1}=1.
\]

This is a complete rational check that the last Voronoi seam lies before the fold and
that the cells below cover exactly `[0,pi/4]`.

Let `beta_k = arctan(q_k)`. The geometric cell closure for direction `k` is

\[
\overline C_k=[\beta_k,\beta_{k+1}].
\]

The ownership cells are

\[
C_0=[\beta_0,\beta_1],\qquad
C_k=(\beta_k,\beta_{k+1}]\quad(1\le k\le K).
\]

Consequently, angle zero belongs to cell `0`, `pi/4` belongs to cell `K`, and each
interior seam belongs to the lower-index cell.
The closures overlap only to prove endpoint bounds; the ownership cells form a disjoint
partition. A verifier must derive these cells.
It may not accept sampled representatives or caller-supplied gaps.

The full-angle tangent of direction `k` is rational:

\[
a_k=\tan\alpha_k=\frac{2t_k}{1-t_k^2}.
\]

For angles with nonnegative finite tangents, define

\[
r(a,q)=\frac{|a-q|}{1+aq}.
\]

This is exactly the tangent of their absolute angular difference.
The maximum mismatch for the closed cell is therefore the rational number

\[
D_k=\max\{r(a_k,q_k),r(a_k,q_{k+1})\}.
\]

The equality follows because absolute angular difference reaches its maximum at an
endpoint of an interval and tangent is increasing on `[0,pi/2)`. In an interior cell,
the two values are the tangents of the adjacent half-gaps.
The formula also handles the axis and folded endpoints without an irrational
representation of `pi/4`.

Each cell carries a positive rational witness side `B_k`. BC-230 chooses the
`legacy-linear-v1` containment rule:

\[
B_k(1+D_k)<1\qquad\text{for every }k.
\]

Its cellwise safe-side supremum is `1/(1+D_k)`. The inequality is strict, so no largest
rational side is attained; a generator may choose its largest proposed rational strictly
below that supremum.
This is the precise meaning of a cell’s “largest safe” side in this contract.

This conservative rule preserves the current scalar decision exactly.
The stronger squared comparison

\[
B_k^2(1+D_k)^2<1+D_k^2
\]

is a sound future contract version, but it is not part of this one.
Indeed, an interior cell’s endpoint mismatch is half an adjacent direction gap, the
first cell has the same form, and the folded-endpoint bracket bounds the last cell’s
other endpoint mismatch.
Because every net direction lies strictly below `pi/2`, these checks give
`0 <= D_k < 1`; on that range `(1+D_k)/sqrt(1+D_k^2)` is increasing and the squared
comparison is the exact worst-endpoint test.
Mixing the two rules under one variant would change the legacy refusal boundary.

## Adaptive-Core Lemma

Let a unit square have orientation `theta`. Reduce it modulo `pi/2` to the unique
`bar_theta` in `[0,pi/2)`, and set

\[
\phi=\min\{\bar\theta,\pi/2-\bar\theta\}\in[0,\pi/4].
\]

This folded angle is unique even when more than one container symmetry realizes it at an
axis or diagonal. Any realizing symmetry gives the same theorem verdict by `D4`
invariance; an implementation uses one fixed `D4` order only to make witness receipts
deterministic. If `phi` belongs to ownership cell `C_k`, the unit square contains, about
the same center and strictly inside its interior, a closed square of side `B_k` and
orientation `alpha_k` in the folded coordinates.

To prove this, put `delta = |phi-alpha_k|`. Since `phi` lies in the closed cell used to
define `D_k`, `tan(delta) <= D_k`. In coordinates aligned with the unit square, the
half-extent of the proposed core along either axis is

\[
\frac{B_k}{2}(\cos\delta+\sin\delta).
\]

For `0 <= delta < pi/2`,

\[
\cos\delta+\sin\delta
=\frac{1+\tan\delta}{\sqrt{1+\tan^2\delta}}
\le 1+\tan\delta
\le 1+D_k.
\]

The strict contract inequality makes this half-extent strictly less than `1/2`. Hence
the closed core lies in the open interior of the unit square.
The conclusion holds at cell seams because the mismatch bound was taken over each closed
cell, even though the ownership rule selects only one of the two neighboring directions.

## Adaptive Fractional-Certificate Theorem

The following conditions imply that `n` unit squares with pairwise disjoint interiors do
not fit in `C_L`:

1. The atoms are distinct, rational, nonnegative, inside `C_L`, and the resulting
   measure is invariant under `D4`.
2. Their total mass is strictly below `n`.
3. The rational net and derived ownership cells satisfy the complete folded-cover
   conditions above.
4. Every cell satisfies `B_k(1+D_k) < 1` under `legacy-linear-v1`.
5. For every `k` and every center `c` for which the closed square `Q(c,alpha_k,B_k)`
   lies in `C_L`, `mu(Q(c,alpha_k,B_k)) >= 1`.

Suppose a packing existed.
Fold each packed square independently by a symmetry of the container, select the unique
owning cell, and apply the adaptive-core lemma.
Undoing the symmetry gives a closed core strictly inside the original square.
The cores are pairwise disjoint because the packed-square interiors are pairwise
disjoint.

`D4` invariance gives each unfolded core the same mass as its folded representative.
Condition 5 gives every core mass at least one.
Nonnegativity and disjointness then give

\[
n\le\sum_{i=1}^n\mu(Q_i)=\mu\!\left(\bigsqcup_i Q_i\right)
\le\mu(C_L)<n,
\]

a contradiction. Under the repository’s bound convention, the certificate establishes
`s(n) >= L`.

Condition 5 is universal over centers.
For atomic measures, the existing exact event sweep can decide it separately at each
pair `(alpha_k,B_k)`: coverage is constant on open center cells, and a boundary can only
add atoms because every weight is nonnegative.
A finite sample of centers is not a decision route.

## Exact Scalar Specialization

Take a current scalar certificate and set every `B_k` to its single `B`. The production
nets have the final seam before `pi/4`, so the largest endpoint mismatch among all
closed cells is exactly

\[
\max_k D_k
=\max_{0\le k<K}\frac{t_{k+1}-t_k}{1+t_kt_{k+1}}
=D,
\]

the current verifier’s largest half-gap tangent.
At the folded endpoint, `beta_K < pi/4 <= alpha_K` by the seam and bracket checks, so
`alpha_K - pi/4 < alpha_K - beta_K`. Its mismatch is therefore no larger than the final
adjacent half-gap.

Since `B > 0`, all per-cell inequalities `B(1+D_k)<1` hold if and only if `B(1+D)<1`.
Condition 5 invokes the same direction list, the same `B`, the same center domains, and
the same atoms as the scalar sweep.
Conditions 1 and 2 are unchanged, and the exact folded-cover check implies the current
net-reaches-`pi/4` condition.

The legacy loader specialization must construct this adaptive object in memory without
rewriting the retained JSON. On the current n=11 and n=12 retained positives, it must
return the same retention verdict, exact total mass, exact least covered mass, and first
worst direction as the scalar verifier.
On the n=17 source control, the underlying scalar and adaptive exact verifiers must both
recompute total `203/12` and least mass `1`, while the retention command must preserve
its current refusal because the source object does not declare `least_cell_mass`. The
archived verifier and source-distinct checker must continue to accept those original
bytes. Every current scalar refusal remains a refusal.
The unchanged scalar route continues to refuse a short legacy net under its current
net-reaches-`pi/4` condition; the adaptive route refuses the corresponding new object
under the complete folded-cover condition.

## Serialized Soft Contract

An adaptive candidate uses this closed JSON shape.
All rational quantities are canonical reduced rational strings: integers use their
base-ten spelling with no leading zero, and nonintegers use
`numerator/positive_denominator` in lowest terms.
JSON numbers are allowed only for the integer fields.
Unknown fields are refused.
This contract inherits the current retention limits: at most 8,388,608 input bytes,
4,096 atoms, 10,001 angle cells, and 512 characters in any rational string.
The angle cell limit is the current 10,000-step ceiling plus its initial direction.
All three decision routes enforce the same limits before geometry or sweeping.

```json
{
  "id": "C-example-adaptive",
  "variant": "adaptive-unconditional",
  "n": 1,
  "claim": "s(1) >= 1/2",
  "outer_side": "1/2",
  "symmetry": "D4",
  "containment_rule": "legacy-linear-v1",
  "seam_owner": "lower-index",
  "angle_cells": [
    {
      "index": 0,
      "half_tangent": "0",
      "lower_boundary_tangent": "0",
      "upper_boundary_tangent": "1/2",
      "max_mismatch_tangent": "1/2",
      "square_side": "1/2"
    },
    {
      "index": 1,
      "half_tangent": "1/2",
      "lower_boundary_tangent": "1/2",
      "upper_boundary_tangent": "1",
      "max_mismatch_tangent": "1/2",
      "square_side": "1/2"
    }
  ],
  "total_mass": "0",
  "least_cell_mass": null,
  "atoms": []
}
```

This format-only example passes the rational net and containment-shape checks but fails
Condition 5 because it has no atoms; it is not a positive certificate.

`variant`, `symmetry`, `containment_rule`, and `seam_owner` must equal the four literal
strings shown above.
`id` is an arbitrary JSON string used only for provenance; it has no theorem meaning and
is constrained by the whole-file byte limit.
`claim` must be the literal string `s(N) >= OUTER_SIDE`, with the object’s base-ten `n`
substituted for `N` and its canonical `outer_side` string substituted for `OUTER_SIDE`.
The remaining scalar fields and atom coordinates have the quantified meanings already
given in the theorem.
No `source` or other provenance extension is allowed on the adaptive variant; such
metadata belongs in its decision receipt.

`angle_cells` must contain `K+1 >= 2` entries.
Indices must be the contiguous sequence `0..K`; half-tangents must be strictly
increasing from zero.
The loader recomputes every boundary and `D_k` from the half-tangents and requires
byte-value equality with the declared rational fields.
This redundancy makes a cell’s decision boundary visible in the frozen object without
allowing the generator to define it.

`least_cell_mass` may be `null` only in generator output.
A retention decision refuses null, recomputes every directional minimum, and requires
the declared value to equal their exact global minimum.
`total_mass` must equal the exact sum of atom weights.
`claim` must equal the conclusion determined by `n` and `outer_side`; neither summary
field is trusted.

The retention gate also preserves the scalar method ceiling.
Let `m` be the least integer with `m^2 >= n`. Because cell `0` is axis-aligned and uses
side `B_0`, it refuses

\[
L>mB_0.
\]

With strict inequality, `n` closed axis-aligned `B_0` squares can be separated inside
`C_L`; Condition 5 and nonnegativity would force total mass at least `n`. Equality is
not covered by that disjoint-closed-square argument and remains eligible.
When every side equals `B`, this is exactly the existing scalar ceiling guard.

Legacy unconditional objects retain their present schema and decision route, including
the n=17 control’s provenance-only `source` field and the fields `angle_limit`,
`direction_steps`, and `square_side`. For the canonical production nets used by the
retained positives, an in-memory compatibility adapter derives `t_k = angle_limit*k/K`,
copies the scalar side into every cell, and applies `legacy-linear-v1`. This adapter is
an equivalence assertion, not a file migration or a replacement for the scalar route.
A noncanonical legacy net remains a legacy object and keeps its existing scalar verdict;
it is not silently reclassified under the stricter adaptive folded-cover schema.
An adaptive object cannot carry both representations.

## Required Decision Routes

BC-231 must implement three agreeing routes before an adaptive object can enter BC-238:

- the project exact event-cell sweep, using each cell’s own `B_k`;
- the interval route, extended to the same per-cell center domains; and
- a standard-library
  `packing/cases/n11_fractional_certificate/adaptive_minimal_verify.py` that parses the
  frozen JSON independently and imports no `sqpack` code.

All routes derive the seams, mismatches, and containment predicates themselves.
Shared serialized values are inputs to compare against those derivations, not shared
geometry code. A verdict or exact minimum disagreement is a guard refusal.
If the interval route retains its current doubled-net implementation, it assigns the
same `B_k` to `alpha_k` and its reflected direction `pi/2-alpha_k`. It may not
interpolate sides or borrow a neighboring cell’s side.

The decision receipt binds the candidate SHA-256 and records each cell’s exact minimum,
each route’s first deterministic witness or terminal interval box, the exact global
minimum and first cell attaining it, event-cell or interval-box counts, wall and CPU
cost, and every refusal or skipped route.
These are recomputed outputs, not trusted candidate fields.

## Refusal Boundary

The adaptive gate refuses before an expensive sweep when any of these holds:

- malformed or duplicate-key JSON, an inexact numeric rational, a nonfinite token, an
  oversized field or object, an unknown variant, rule, seam policy, or field;
- nonpositive `n`, `L`, or any `B_k`; fewer than two cells; noncontiguous indices;
  unsorted, repeated, negative, or nonfinite half-tangents; `t_0 != 0`; or `t_k >= 1`;
- failure to straddle `pi/4`, a final seam at or beyond `pi/4`, nonmonotone seams, a
  missing cell, or a declared boundary or mismatch unequal to the derived rational;
- containment equality or failure in any cell;
- malformed atoms, duplicate sites, a negative weight, a site outside `C_L`, a missing
  or unequal-weight `D4` image of positive support, an incomplete explicitly listed
  zero-weight orbit under the schema’s domain-completeness rule, a false declared total,
  or a claim inconsistent with `(n,L)`;
- total mass at least `n`, or `L > ceil(sqrt(n)) B_0` under the exact integer-square
  comparison above.

After those checks, the gate refuses a directional minimum below one, a false declared
minimum, an event/interval/standalone disagreement, a path that changes during review,
or a required route that did not run.
It reports every invalid or time-limited attempt; it never converts one into a negative
theorem result.

## Limits and Follow-On

This packet proves a certificate language.
It does not show that adaptive sides improve the covering objective, supply an adaptive
candidate, price decision cost, or justify angle-cell kernels.
BC-231 owns implementation and mutation controls after independent review.
A stronger exact-squared containment rule requires a new contract version and its own
scalar-compatibility decision; it cannot be enabled as an implementation detail.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
