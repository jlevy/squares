# Adversarial Review of the T-025 and T-026 Verifiable Claims

**T-025: accept.** The
[standalone T-025 claim](../../../packing/cases/n11_threshold_certificate/t-025-verifiable-claim-191-50.md)
proves the ordinary lower bound $s(11)\geq191/50$ from its embedded threshold
certificate. Its standard-library verifier completes the exact decision on all 181
directions. The threshold counting theorem, symmetry transfer, orientation net, and
event-cell decision support that conclusion.

**T-026: accept.** The
[standalone T-026 claim](../../../packing/cases/n11_threshold_certificate/t-026-verifiable-claim-dilation-limit.md)
proves

$$
s(11)\geq C=
\frac{955000\sqrt{518400042893309449}}{179696714646249}
=3.8264474\ldots.
$$

Its own embedded 1440-step certificate supplies the finite premise.
Common dilation, the sharpened containment inequality, rational density, and upward
embedding then give the displayed ordinary `>=` theorem.
The numerical conclusions of T-025 and T-018 are not premises of this proof.

This review covers the complete threshold-to-limit composition and qualifies as the
review artifact required for T-026 at **V4/C5** under
[the repository’s assurance definitions](../../../epistemics.md).
The [document map](../document-map.yaml) retains this document as a non-superseded
review, and [T-026’s record](../../../packing/frontier/results.yaml) names it as the
`review_artifact`. That satisfies the C5 registration requirement.
It does not confer V5 or constitute external peer review.
No mathematical or certificate-binding finding remains open in the reviewed version.

## Scope and Review Independence

The reviewer was a separate agent from the implementation authors.
I read the theorem and
[standalone checker](../../../packing/cases/n11_threshold_certificate/verify_claim.py),
derived their main obligations from the packing definition, constructed an independent
small-instance geometric oracle, and reported defects for the authors to fix.
I did not edit the checker, its renderer, either claim, or the certificate data.
The authors retained the oracle in the test suite.

The audit also read the
[threshold-theorem review](review-2026-09-09-threshold-certificate-theorem.md), the
[dilation-limit review](review-2026-09-06-t022-dilation-limit.md), the retained exact
and interval decisions, the proof packets, the limit record, and the assurance register.
Those sources provided context; the arguments below recheck the composition used by
these two claims.

I ran the small checks myself and inspected the complete stdout and stderr receipts from
the coordinating agent’s two exhaustive standalone runs.
I did not launch those full runs or repeat the retained interval branch-and-bound in
this review. The standalone checker adds an implementation of the exact event-cell
method; it is not a third distinct mathematical method alongside the retained exact and
interval routes.

## Finite Certificate Theorem

The theorem uses $s(n)$ as the infimum of container sides admitting $n$ unit squares
with pairwise disjoint interiors, with arbitrary rotations.
The final claims state the needed parameter assumptions: positive integers $n,K$,
positive rational $L,B$, $0<T<1$, nonnegative weights, and finite threshold sets of
distinct points with integer thresholds $1\leq k\leq|S|$. A threshold atom $(S,k,w)$
charges $w$ when a closed core contains at least $k$ members of $S$.

The direction proof must act on each packed square separately.
Represent its orientation modulo $\pi/2$ in $[0,\pi/2)$; diagonal reflection brings
orientations above $\pi/4$ into $[0,\pi/4]$. The inequality $T^2+2T-1\geq0$, together
with $0<T<1$, makes the net $\theta_j=2\arctan(Tj/K)$ reach that arc.
The nearer endpoint of each net interval has mismatch $d$ satisfying

$$
\tan d\leq D:=\max_{0\leq j<K}
\frac{t_{j+1}-t_j}{1+t_jt_{j+1}}.
$$

The condition $B(1+D)<1$ puts the concentric closed core strictly inside the reflected
unit square: its half-width across either original edge normal is at most
$B(1+D)/2<1/2$. Apply the net coverage condition there, then pull the core back into the
original packed square.
D4 invariance preserves both point charge and threshold charge.
The individually reflected squares need not themselves form a packing; counting occurs
after the pullback.

The resulting closed cores lie in disjoint unit-square interiors, so they are disjoint
as sets. Each point weight can be charged once.
For one threshold atom, $r$ charged cores consume disjoint traces containing at least
$rk$ distinct members of $S$. Thus $r\leq\lfloor|S|/k\rfloor$, including when $k$ does
not divide $|S|$. Points shared between different atoms cause no problem because the
bound is applied to each atom before summing.
Coverage gives total core charge at least $n$, while the atom budgets give a total
strictly below $n$, a contradiction.

This excludes a packing at side $L$. A packing at any smaller side would embed in the
side-$L$ container, so the infimum definition yields $s(n)\geq L$. No compactness claim
is needed.

## Exact Sweep and Its Boundary Conventions

At one rational half-tangent, write $c=(1-t^2)/(1+t^2)$ and $s=2t/(1+t^2)$. The
admissible physical centers form $[h,L-h]^2$, where $h=B(c+s)/2$. Rotation into
coordinates $(u,v)$ gives a convex polygon with nonempty interior.
The loader refuses a certificate if any checked direction lacks that interior.
Both retained inputs pass this restriction.

For every site $p$, membership of $p$ in a closed core is equivalent to the center lying
in a closed axis-parallel rectangle $R_p$ of side $B$. The event coordinates include
every rectangle edge, including sites appearing only in threshold atoms, and the
extremes of the center domain.
Every point-membership trace is constant on an open event cell.
At a cell boundary, closedness can only add members to the trace.
Since the actual charge is monotone in that trace, boundary charge cannot be smaller.
Convexity and nonempty interior ensure that every admissible center is in the closure of
an open cell meeting the domain.
Therefore open cells suffice to decide the minimum, including centers on the container
boundary.

The code accepts the two-of-three threshold atoms used here.
Their signed rectangle expansion is exact:

$$
[m\geq2]=\binom m2-2\binom m3\qquad(0\leq m\leq3).
$$

Each pair contributes its rectangle intersection with coefficient $w$, and the triple
contributes with coefficient $-2w$. An intersection with zero width or height contains
no open cell and may be omitted.
The signs belong to this arithmetic expansion; the result being minimized is still the
nonnegative, monotone threshold charge.

The sweep applies a rectangle’s start addition and end subtraction before querying the
next open $u$ slab. Its active horizontal indices are consequently `start <= i < end`. A
vertical range update covers leaves `j0` through `j1 - 1`, which represent open cells
between consecutive event coordinates.
Events outside the admissible domain are still processed, preserving the active sum on
entry.

For a slab intersecting the domain, let $[\mathrm{low},\mathrm{high}]$ be the vertical
projection of its closed clipped polygon.
The queried indices are `bisect_right(V, low) - 1` through `bisect_left(V, high) - 1`,
clamped to the event grid.
These select exactly the cells with `V[j] < high` and `V[j+1] > low`. Convexity and
nonempty interior make each selected open rectangle reachable by an admissible center in
that open slab. The strict comparisons exclude cells that only touch a projected
endpoint. This establishes the reachability obligation behind the reported cell counts,
rather than relying on the final witness alone.

The range tree accumulates scaled integer charges using Python’s unbounded integers.
The scale is the least common multiple of all weight denominators, so conversion is
exact. Lazy addition preserves the minimizing index within a uniformly updated node;
pulling or querying chooses the leftmost minimum on ties.
The final cell witness is constructed by exact clipping and checked by direct point and
threshold membership.
That witness checks attainment; enumeration and the boundary argument establish the
global lower bound.

## T-026 Dilation and the Endpoint

T-026’s finite premise uses $L=191/50$, $B=249507/250000$, and $D=207107/720000000$. Its
minimum charge is exactly one and its total budget is $5483661432/498684619<11$. These
facts come from its own certificate and full sweep.

Scale the container, core, every point atom, and every member of every threshold set by
a positive rational $q$, leaving weights, thresholds, and the direction net fixed.
Inverse dilation gives a bijection of admissible placements preserving every trace, and
therefore coverage and the budget.
D4 invariance transfers to the scaled container.
This checks the threshold-specific part of the dilation argument.

For the angular mismatch parameter $t=\tan d$, the identity

$$
(1+D)^2(1+t^2)-(1+t)^2(1+D^2)=2(D-t)(1-Dt)\geq0
$$

holds for $0\leq t\leq D<1$. Together with $\cos d+\sin d=(1+t)/\sqrt{1+t^2}$, it gives
strict containment whenever $q^2B^2(1+D)^2<1+D^2$. This replaces the coarser containment
condition in the scaled family.
The retained test includes a rational $q$ that fails the coarse test but passes this
sharpened one, so the distinction is exercised.

Set $c_*:=\sqrt{1+D^2}/(B(1+D))>0$ and $C=Lc_*$. Direct rational calculation gives

$$
c_*^2=\frac{32400002680831840562500000000}{32290909254655439869209770001},
\qquad
C^2=\frac{472793799119770550224225000000}{32290909254655439869209770001}.
$$

The reported radical is positive and has that square.
Every positive rational $q<c_*$ therefore excludes a packing at side $qL$. For every
positive real $x<C$, choose a rational $x/L<q<c_*$. A packing at side $x$ would embed at
side $qL$, contradicting the finite certificate.
Hence all sides below $C$ are excluded and $s(11)\geq C$. Equality in the uniform
containment test at $q=c_*$ does not weaken that conclusion.
The proof asserts neither a certificate at the endpoint nor a strict `>` theorem.

## Data Binding and Controls

The documents embed all executable data; a reader needs only the saved Markdown file,
its copied verifier block, and CPython 3.12 or later.
SHA-256 and byte counts bind the exported blocks to their declarations.
They establish identity at this distribution boundary; the sweep and proofs establish
validity.

The limit check binds its source digest and mathematical source fields to the
certificate just decided.
It recomputes the factor square, positive radical forms, side square, defining
polynomials, and containment coefficients.
It checks the strict factor domain, support and monotonicity identities, and endpoint
fields against the exact forms reviewed above.
Narrative metadata is not an additional theorem premise.
The generator’s tests also require both embedded checker copies and all embedded data to
equal the current source files byte for byte.

The following findings were fixed and rechecked before acceptance:

- The theorem now states its parameter preconditions and orientation convention.
- The factor-domain check now compares the exact mathematical field.
  A regression preserves the correct bound while changing `<` to `>`, and is refused.
- A declared limit with a malformed standalone marker is refused before the sweep; it
  cannot silently become a source-only decision.
  The regression changes the data marker rather than the marker constant inside the
  embedded Python block.
- The claim defines the positive limiting factor, states where sharpened containment
  replaces the coarse estimate, and accurately describes the recomputed minimizing
  direction and the checker’s storage cost.

The final fast run covered the
[standalone controls](../../../packing/tests/test_verify_threshold_claim.py) and
[independent half-plane oracle](../../../packing/tests/test_verify_threshold_claim_oracle.py):
**21 passed, 2 exhaustive tests deselected**, under the project interpreter on
2026-09-10. It includes refusal controls, byte binding, exact source-weight rescaling,
limit algebra, and generated-document freshness.

The independent oracle enumerates intersections of physical-coordinate half-planes and
evaluates direct membership without using the sweep’s clipping or reachability helpers.
Across seven seam, oblique, threshold-only, and mixed fixtures, it agrees with every
queried slab, range minimum, minimizing index, and leaf charge: **272 reachable cells in
49 slabs**. Its positive threshold-only fixture has minimum $7/5$. These small checks
exercise endpoint conventions and threshold events that a global-minimum-only comparison
could miss; they do not replace exhaustive replay of the retained certificates.

## Exhaustive Replay Receipts

The following are compact records transcribed from the coordinated runs’ complete stdout
and stderr. Both accepted all closed-form conditions and all declared values.

| Claim | Directions | Reachable event cells | Least charge | First minimizing index | Result |
| --- | --- | --- | --- | --- | --- |
| T-025 | 181 | 1,044,374,137 | $100000203/100000000$ | 69 | `VERIFIED: s(11) >= 191/50` |
| T-026 | 1,441 | 8,344,684,609 | $1$ | 914 | `VERIFIED: s(11) >= 955000*sqrt(518400042893309449)/179696714646249` |

The certificate identities checked in those runs are:

- T-025: 673,639 bytes, SHA-256
  `3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c`.
- T-026: 673,899 bytes, SHA-256
  `dc2da20c75d952690c93d67fb4b3eb8552e879585902fde98eedc9b3179ed3d0`.
- T-026 limit record: 3,965 bytes, SHA-256
  `04fd6bbca1941671ddbabbe359219011b8217818b0a291f4c9a00f5fa7834f8e`.

Both definitive runs used the current checker, SHA-256
`3be3ec677cd7e49b87b8bf7a4957d3c4a5b41c11bf9505e31c70265dbcd64b28`. T-025’s receipt
records 87.50 seconds of user CPU time.
T-026’s definitive receipt records 718.60 seconds of user CPU time and 750.00 seconds
elapsed. It accepts all 1,441 directions, the exact minimum and declarations, and the
factor, side, polynomial, strict-family, and endpoint fields.

I checked that the final T-026 document has SHA-256
`2e18708c83f883bc5ae5d11010d6c9b1823dedd39dc3131d67a1c475edcb40f4` and that the current
checker has the digest above.
After reading the completed receipt, I reran the generated-byte and renderer-freshness
tests: **3 passed**. Both claims embed the current checker and their exact certificate
data.

## Assurance Decision and Remaining Limits

T-025 retains its V4/C5 status, now with a self-contained direct claim and an additional
standard-library replay.
T-026’s finite exact and interval evidence supplies C4; this source-distinct review
covers the combined threshold counting, finite decision, dilation, and endpoint proof
needed for C5. Its registration as the current retained review artifact closes that
requirement, so T-026 is V4/C5.

The trust base remains the stated mathematics, the complete retained certificate data,
and the implementation and runtime of the exact and interval checks.
This audit does not establish another atom family, another net, optimality of the source
LP, optimality of the shrink, or inability of further refinement to improve the bound.
The 720-step control and the numerical value of an earlier theorem are not necessary to
either accepted conclusion.
Formal proof-assistant verification and external review remain separate assurance steps.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
