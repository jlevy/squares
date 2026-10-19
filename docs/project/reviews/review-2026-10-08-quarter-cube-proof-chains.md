# Review of Ryu’s Quarter-Power and Cube-Root Proof Chains

**Decision: the new proof chains are accepted at source-review scope, conditional on the
named imported lemmas and numerical premises.** No new blocking geometric,
measure-theoretic or all-scale inference gap was found.
Independent execution of the new numerical inequalities was pending at the source-review
checkpoint; the numerical addendum below records its subsequent acceptance.
The nine-overlap route retains the earlier independent-per-box limitation; the
thirteen-overlap route avoids that computation.
This review alone changes no assurance rating or frontier claim.

The review was performed by a separately prompted AI reviewer on 8 October 2026 UTC. It
is not a human peer review or a formal proof certificate.
The acquisition and reported-import checkpoint was
`0a9e17179b757a28fea54373858d10d8965aeaa4`.

## Primary Sources and Scope

The complete primary texts read were Sungjoon Ryu’s
[quarter-power paper](https://github.com/squarepacker/k2-minus-c-quarter/blob/abbedcf4bba2e4053f0278e669d84966a89c8b73/paper/paper.tex),
5,471 TeX lines, and
[cube-root paper](https://github.com/squarepacker/k2-minus-c-cube-root/blob/15045f9c6b74bd52f60394b9be593ebe4fb3debc/paper/paper.tex),
584 lines. Their immutable upstream pins are respectively
`abbedcf4bba2e4053f0278e669d84966a89c8b73` and
`15045f9c6b74bd52f60394b9be593ebe4fb3debc`, both v1.0. Their archive identifiers are
[10.5281/zenodo.23211207](https://doi.org/10.5281/zenodo.23211207) and
[10.5281/zenodo.23212059](https://doi.org/10.5281/zenodo.23212059).

The retained
[quarter packet](../../../packing/resources/web/squarepacker-k2-minus-c-quarter-2026-10-07/README.md)
contains nine original files, 2,247,251 bytes; the
[cube packet](../../../packing/resources/web/squarepacker-k2-minus-c-cube-root-2026-10-07/README.md)
contains eleven, 534,546 bytes.
The papers are CC BY 4.0 and the programs MIT. The source credits extensive Claude
assistance and states that there has been no human peer review.
Those statements and licences remain attached to the original bytes.

This review uses the
[v1.2 dependency review](review-2026-10-08-squarepacker-k2-minus-c-v12.md), including
its unchanged geometric blocks and its explicit computational limits.
Here, R denotes that paper, Q the quarter-power paper, and C the cube-root paper.
The review covers Q’s new flow construction and P1–P8, its main threshold and asymptotic
deductions, and C’s complete new argument and eight-row reduction.
Q’s supplementary optimization and sensitivity tables were read as source claims; their
numerical entries were not independently executed.

All theorems concern finitely many unit squares disjoint as closed sets in an
integer-sided container.
Write W = k² − N and Wmin for the least such waste.
Passing to the ordinary packing function uses R’s strict-packing equivalence: s(k² − c)
= k requires c < Wmin(k). None of these astronomical side-length statements supplies a
new case bound at n ≤ 324.

The immutable source links above and below have complete local counterparts in the
retained packets:

| Reviewed source | Repository-relative retained path |
| --- | --- |
| Q paper/paper.tex | `packing/resources/web/squarepacker-k2-minus-c-quarter-2026-10-07/source/paper/paper.tex` |
| Q code/k14_constants_check.py | `packing/resources/web/squarepacker-k2-minus-c-quarter-2026-10-07/source/code/k14_constants_check.py` |
| C paper/paper.tex | `packing/resources/web/squarepacker-k2-minus-c-cube-root-2026-10-07/source/paper/paper.tex` |
| C code/check_table_exact.py | `packing/resources/web/squarepacker-k2-minus-c-cube-root-2026-10-07/source/code/check_table_exact.py` |
| C code/check_table_exact2.py | `packing/resources/web/squarepacker-k2-minus-c-cube-root-2026-10-07/source/code/check_table_exact2.py` |
| C code/check_table_iv.py | `packing/resources/web/squarepacker-k2-minus-c-cube-root-2026-10-07/source/code/check_table_iv.py` |

## Dependency Boundaries

| Route | Imported overlap premise | Consequence for this review |
| --- | --- | --- |
| Nine-overlap constants | R Lemma 4.10, with the reviewed v1.2 geometric reduction | The existing same-program leaf replay and current-host floating comparison argument are available. Independent verification of every box label remains open at C1. New flow arguments do not close it. |
| Thirteen-overlap constants | R Lemma 4.9 and its analytic counting argument | Avoids R Lemma 4.10 and its leaf archive. It retains the small finite class-sequence angle check stated in R Lemma 4.9(b), as well as ordinary numerical constant inequalities. |
| Cube-root extension | Q Sections 3–8, using either overlap premise consistently | Uses Q’s parameterized flow results, not Q’s astronomical quarter-power threshold. Its smaller starting scale is therefore not a circular invocation of the quarter-power theorem. |

R Lemma 4.9 explicitly enumerates class sequences in {2,3,4,5} of length at most five
using 50-digit arithmetic.
The [v1.1 review](review-2026-10-05-squarepacker-k2-minus-c.md#lemma-49-13-by-hand)
records an independent enumeration of that full domain: only rotations of (5,2,5,2)
attain sum 14, and every sum at least 15 violates the angular condition by at least
25.942 degrees. It also checks the two-class-5 refinement.
The v1.2 dependency review found this labelled proof block unchanged, so that accepted
premise is inherited here; no fresh enumeration was run.
Calling its route “analytic” distinguishes it from the large box computation; it should
not imply that this finite numerical premise has disappeared.
The two overlap routes must also use their respective A, A′, death, merge, end-collision
and gap-overlap constants throughout.

Q’s arbitrary-pair charging proposition is needed beyond the visibility graphs appearing
in the imported statements.
The proofs of R Lemmas 4.9 and 4.10 count all relevant near pairs, using square-centre
separation and the two opposite boundary sides rather than graph planarity.
Q explicitly checks the extension, including the fixed-side boundary situation.
The resulting finite-family Tonelli argument gives the required sum of pair wastes
bounded by K W. Assuming that extension silently would leave a dependency gap; Q
supplies it.

## Quarter-Power Flow Construction

The construction fixes the normal direction of every passed square, an accumulated
free-gap budget δ, and a height ceiling.
Death, wall contact, square contact and height termination have an explicit priority.
At a bottom-edge entry, rule R1 selects the lexicographically least
accumulated-gap/floor-coordinate arrival before rule R2 applies the tilt threshold.
This order is used later when entries are charged to tilt.

The construction is finite.
A passed square has inclination below the fixed small threshold; its passage raises
height by at least the corresponding positive cosine.
The resulting bound on path length gives finitely many candidate histories.
Along each history, coordinates and event times are affine in the starting floor
coordinate. Their comparisons cut the floor into finitely many Borel pieces.
Entry maps expand by products of secants, and centre height strictly increases between
entries, so the R1 selection is defined by an acyclic finite induction.

The scale-dependent flows are truncations of this one master flow.
They do not choose new R1 winners.
Their tilt-termination sets increase with scale, and the entry formula defines a Borel
first stopping scale T*. Non-tilt losses and gap overlap are bounded by the master flow.
A finite exceptional-height set works for all scales: new truncation heights are
terminal heights, outside the interior line identities that use them.
This establishes the measurability required for the subsequent scale integrations.

| Step | Mathematical boundary checked | Result |
| --- | --- | --- |
| P1/P2, Q Section 4 | Quantization of entry height and exclusion of bottom-edge contact | The sum of cosine losses and accumulated gaps bounds distance to an integer. The ramp estimate sin(a) + 1 − cos(a) ≤ 1.0001a is used only in its small-angle domain. The line band excludes every bottom-edge contact of a selected square, including vertices and termination ties. |
| P3, Q Section 5 | End collisions, angle reduction and pair multiplicity | Entry-coordinate expansion bounds the losing floor mass by a gap-width strip. The quotient angle and the possible π/4 crossing are treated separately. Each unordered pair has at most two orientations, and floor/ceiling pair families are disjoint. |
| P4, Q Section 6 | Shadow identity at fixed height | Square passages have density at most one. Gap multiplicity is retained explicitly. The identity includes the unoccupied-gap correction; it is asserted off the finite exceptional set, with the inequality needed for integration preserved. |
| P5, Q Section 7 | Deaths, merges and overlapping gaps | A gap point has at most two sources. Two-source points lie in the stated valley rectangle; a third source contradicts the required opposite endpoint positions. The area formula counts deaths with their actual multiplicity. Merge and fixed-height overlap losses use the rectangle widths. |
| P6, Q Section 8 | Inclination budget along nonvertical trajectories | The source constructs waste slits, transfers them to vertical slits with an explicit endpoint loss, proves their disjointness, and applies Cauchy–Schwarz to slit area and pair waste. |
| P7/P8, Q Sections 9–10 | Per-scale count and integration | Selected squares are unreachable and lie in the enlarged height window. Integrating their unit area gives the scale count. Borel measurability and nonnegative integrands justify Tonelli. All charges using the same global W appear additively in the final denominator. |

Three parts require more than a diagram of the trajectories.

First, the valley argument proves both the small separation of the two source squares
and localization of the common gap region.
The width is δ tan(θ)/cos(θ), not merely δ. The imported small-angle waste bound then
controls the sum of widths.
The death estimate uses the map from floor coordinate and cumulative gap length into
waste, with Jacobian at least one and the valley rectangles accounting for multiplicity.
For merges, at most four further unit squares can meet the relevant small disc, after
excluding the two source squares.
These facts yield the distinct D, M and G constants before the losses are combined.

Second, P6 cannot treat a tilted trajectory as a vertical column.
For a used pair X → Y, the convex hull of the used exit coordinates has an affine
positive gap function.
If a third square entered the hull slit, two actually used rays would trap its entire
relevant projection in a strip of width less than δ; that contradicts the minimum width
one of a unit square.
This supplies a waste slit even when the used exit-coordinate set has holes.

The vertical transfer has factor χ greater than 0.99999849. Trimming loses at most
1.0000016 δ β̄ from its projected interval.
Distinct transferred slits are distinct components of vertical waste and hence have
disjoint interiors. The resulting error is bounded by 8.5 × 10⁻¹⁰ W for K = 9 and 1.22 ×
10⁻⁹ W for K = 13, within the 10⁻⁸ allowance in A′ = A/cos(β̄) + 10⁻⁸. Capping
successive quotient angles at β̄ still dominates the selected entry inclination by the
triangle inequality.
This is the path budget subsequently applied to α(T*).

Third, floor and ceiling trajectories stop at heights separated by two.
A square has vertical extent at most √2, so it cannot enter both charged families.
Reflection preserves distance from integer heights because k is an integer.
These are the reasons the two halves can be added without silently doubling the global
pair budget.

## Quarter-Power Integration and Global Coverage

The paper partitions its line set into high-waste, high-inclination and remaining lines.
The first part costs at most $W/(\omega_0 y_0^{3/4})$, and R’s line-inclination estimate
charges the second at A W/(2c₁). On the remaining lines, the excess-chord estimate is
integrated with weight $d(y)^{-3/4}$. Its upper bound Γ is independent of k and includes
both reflected halves.

For each scale s, the enlarged window has length εs + 2.0002. Integrating the per-scale
count against |α′(s)| charges tilt terminations by A′W. Reversing the nonnegative window
integral produces invF. The displayed polynomial identity proves 0 < invF < 1; the
denominator remains positive.
The wall integral is bounded using tan(x) ≤ 1.000001x, giving a logarithmic loss.
The final lower bound has the form

\[
W\ge\Psi_\pi(k)=
\frac{(1-\omega_0)\,8h_0\left(((1-\varepsilon)y_1)^{1/4}-(y_0+1)^{1/4}\right)
-K_W\left(\log(y_1/y_0)+2/y_0\right)}{B},
\qquad y_1=k/2-3.
\]

Q Section 10.2 defines B, h₀ and K_W from the parameter vector and imported constants.
Replacing A, A′ and CΛ by upper bounds enlarges the denominator; the theorem also
handles a negative numerator, for which nonnegative waste supplies the bound.
The successful positive threshold checks must use the larger denominator in every
occurrence, including Γ.

A numerical value at k₀ does not by itself prove a range of k. Q’s monotonicity
proposition supplies the missing implication.
In addition to $\Psi(k_0)\ge c k_0^{1/4}$, it requires

\[
D_1=\frac{h_0(1-\omega_0)(1-\varepsilon)^{1/4}}{B}
-\frac{c}{4\,2^{3/4}}>0,
\qquad y_1(k_0)^{1/4}D_1\ge\frac{K_W}{2B}.
\]

These inequalities make the derivative of $\Psi(k)-c k^{1/4}$ positive for every k ≥ k₀.
The scale-domain constraint also persists as k increases.
The claimed main instantiations use c = 0.1 and k₀ = 4.62 × 10¹² for K = 9, or 2.17 ×
10¹³ for K = 13. Their source table gives positive margins for all three tests.
Independent numerical execution was a separate requirement at this checkpoint and is
recorded in the addendum below.

The optimized asymptotic statement is also an all-scale argument.
For each fixed admissible parameter vector, divide by $k^{1/4}$ and take the lower
limit. Then choose the explicit sequence of parameter vectors with y₀ tending to
infinity, ε = $y_0^{-1/2}$ and ω₀ = $y_0^{-1/4}$. Their constraints hold eventually.
No exchange of a k-dependent parameter limit and the packing minimum is needed.
Optimizing the remaining positive one-variable expression gives

\[
c_\infty=
\frac{16\,2^{-1/4}(1-\lambda)^{5/4}}
{5\,(5.0001)^{1/4}\sqrt{AA'}},
\qquad \lambda=2\delta+2\times10^{-12}.
\]

The source gives 0.1696524… and 0.1411593… for the two routes.
The optimization is within this proof’s bound family; it establishes no optimality of
actual packings. The conversion to fixed-c packing claims uses the strict inequality c <
Wmin. The extra one in the sufficient integer threshold 10⁴c⁴ + 1 supplies that
strictness.

## Cube-Root Extension

C instantiates the general master-flow construction with a fixed tilt threshold θ. Its
parameter choice satisfies Q’s construction hypotheses already for k ≥ 14; it never
invokes Q’s quarter-power theorem at such k.

The new estimate bounds the sum of inclinations along one trajectory.
The passed vertical intervals are disjoint.
On lines with waste below one half, R’s inclination integral applies; the remaining
heights have measure at most 2W. Since each passed inclination is at most θ, their
contribution is bounded explicitly.
Dividing the cosine-weighted sum by cos(β̄) gives B₁W. Lateral drift is therefore at
most B₁W + δ, and both wall losses total at most 4(B₁W + δ).

Choosing θ = min(β̄, 2τ₁/(B₁W)) bounds the accumulated cosine loss by τ₁. This is a
legitimate packing-dependent auxiliary choice because the argument is applied to an
arbitrary fixed packing before deriving an inequality for its W. The integer-height
exclusion then uses τ₀ − 1.0001β > τ₁. It does not need the short-chord angle β to be
smaller than θ.

With the explicit short-chord excess E and total termination bound L(W), the new master
inequality is

\[
(1-2\tau_0)(k-6)
\le \frac W{\nu_0}+\frac{\bar A W}{2\beta}
+\frac{\beta(k/2-1)\,L(W)}{1-\nu_0-E}.
\]

Its denominator requires E < 1 − ν₀. The left-side band measure is exact for integer k,
including odd k; the removed central interval spans six unit periods.
Unreachable-square counting uses Q’s master-flow shadow budget and the path tilt budget,
with the same floor/ceiling disjointness as above.

For a trial $W(k)=\gamma k^p$ and $\beta(k)=b k^{p-1}$, with p equal to one half or one
third, the paper replaces k/2 − 1 by k/2 to form an upper bound R⁺. The right side is
increasing in W while the denominator is positive, so a failed inequality at the trial W
excludes every smaller waste.

The global reduction has two cases.
For p = 1/3, every power of k in R⁺(k)/k is nonincreasing, while the normalized left
side increases.
For p = 1/2, the same conclusion requires staying on the linear branch of
the maximum in L(W):

\[
\gamma\sqrt{k_b}\le W_1=\frac{2\tau_1}{B_1\bar\beta}.
\]

This upper-endpoint test is essential.
Checking only kₐ would not establish the finite interval.
The tightest source row is analytic case 6, whose stated endpoint margin is about 0.43
in W. The eight rows cover the adjacent finite intervals and the two infinite cube-root
tails claimed in C’s theorems.

For the asymptotic result, the paper first chooses a fixed γ below
$((4/27)/(\bar A\,\bar A'B_1))^{1/3}$. Taking τ₀ and τ₁ close to 1/6 and ν₀ small makes
the limiting normalized right side strictly smaller than 1 − 2τ₀; an explicit positive b
minimizes the two surviving terms.
The other terms and E tend to zero, so a sufficiently large finite starting scale
exists, and the monotonicity proposition supplies the whole tail.
The source’s rounded lower constants are 0.06285 and 0.05229. This is a lower-limit
statement, without an explicit starting scale for every coefficient below that limit.

## Numerical Programs and Remaining Execution Boundary

The review read the deciding sections through line 822 of Q’s
[constant checker](https://github.com/squarepacker/k2-minus-c-quarter/blob/abbedcf4bba2e4053f0278e669d84966a89c8b73/code/k14_constants_check.py),
and all three C programs:
[exact intervals](https://github.com/squarepacker/k2-minus-c-cube-root/blob/15045f9c6b74bd52f60394b9be593ebe4fb3debc/code/check_table_exact.py),
[one-sided rational bounds](https://github.com/squarepacker/k2-minus-c-cube-root/blob/15045f9c6b74bd52f60394b9be593ebe4fb3debc/code/check_table_exact2.py),
and
[mpmath intervals](https://github.com/squarepacker/k2-minus-c-cube-root/blob/15045f9c6b74bd52f60394b9be593ebe4fb3debc/code/check_table_iv.py).
None was executed. In particular, no upstream program wrote its output beside the
archived source.

Q evaluates the same formula functions using high-precision scalar and interval
contexts. That is a useful cross-check, but it is one shared formula implementation.
Its main-row logic includes the domain and derivative conditions, rather than merely
comparing displayed constants.
It checks small geometric ceilings, the A/A′ allowances and the aggregate loss
coefficients before the final threshold rows.

C’s first exact program encloses positive roots with rational endpoints whose powers are
checked against the radicand, and uses rational Taylor enclosures for the small-angle
sine and cosine. Its eight-row checks include the finite-interval upper endpoint.
The second exact program uses independent one-sided bounds and an algebraically exact
simplification of A W/(2β). Its printed table-rounding and asymptotic comparisons are
not folded into its aggregate success variable, and its main entry point does not
convert a failed aggregate to a nonzero exit.
Those outputs must not be treated as an enforced CI receipt merely because the process
exited normally. The interval program enforces the eight domain/margin checks and a
failing exit status.
The programs’ finite scalar sample sweeps are diagnostics; the paper’s monotonicity
proof is what supplies continuous scale coverage.

The maintained independent numerical follow-up must retain the full claim roster and
check:

- Both Q parameter domains, geometric constant ceilings, positive denominators,
  threshold margins, derivative conditions and asymptotic constants.
- All eight C rows, including strict line-band separation, excess denominator, main
  contradiction margin and each finite upper-endpoint branch condition.
- Consistent use of the appropriate nine- or thirteen-overlap constants.
  C’s B₁ and L₁ should be evaluated from their formulas when verifying the printed
  outward table bounds; substituting their rounded display ceilings changes the last
  digits in two rows.
- Negative controls that violate the domain and each deciding inequality, rather than
  only controls that alter a stored checksum or table label.

A successful maintained arithmetic check would establish these numerical implications
under the reviewed analytic formulas.
It would not verify the missing independent R Lemma 4.10 box labels, nor turn the AI
source review into a formal or human proof review.

## Review Evidence and Disposition

The reviewer inspected the retained TeX directly in bounded `sed` ranges and located
labelled dependencies with `rg`. The entire new primary argument was read, including the
parameterized construction, exceptional-set treatment, transferred-slit error, final
monotonicity proofs and asymptotic limiting choices.
The numerical programs were inspected as source, and their formula graphs and domains
were supplied to a separate implementation lane.
No producer, packing search, box replay or numeric analogue campaign was run for this
review.

The accepted scope is the conditional mathematical source review and faithful reported
import of the two proof chains.
At the source-review checkpoint, the outstanding new boundary was independent maintained
arithmetic for the deciding constants and complete row roster.
The inherited nine-overlap independent-per-box task remains open, and the analytic
thirteen-overlap route retains its finite angle-check premise.
All source bytes, author credit and computational limitations must remain available with
any later claim expression.

## Maintained Arithmetic Review Addendum

A second independently prompted strong reviewer accepted the maintained arithmetic on 8
October 2026 UTC. The reviewed files are
`packing/cases/asymptotic/quarter_cube_constants.py` and
`packing/tests/test_quarter_cube_constants.py`, frozen before this review’s final runs.
This acceptance establishes the numerical consequences of the reviewed formulas under
the geometric premises stated above.

The reviewer compared the implementation with the pinned Q and C primary texts: Q’s
parameter constraints, Sections 10–11 and derivative proposition; C’s Section 2
constants, Proposition 3.1 and all eight Table 1 rows, including both finite upper
endpoints in each overlap route.
Every decimal input enters through `Fraction`; interval calculations use a private
60-digit context. A strict inequality holds only when its complete interval difference
has negative upper endpoint.
The module reads no archived file and executes no upstream checker.

The command returned exit 0 with **108 of 108 checks holding**. These cover both
quarter-power parameter vectors, threshold margins and derivative certificates; all
eight cube-root domains, contradiction margins and outward table bounds; the four finite
upper-endpoint branch conditions and four infinite-tail exponent checks; four asymptotic
floors; and fourteen numerical ceilings for A, A′, CΛ, S, C_M, C_G and C_E. The two
quarter routes also check both small-angle domains explicitly.
The quarter denominator is positive from its positive summands and the checked positive
inverse factor. The cube denominator is checked before the division that uses it.

The quarter threshold margins are approximately 0.0153398 for K = 9 and 0.00375239 for K
= 13. Their positive derivative constants are approximately 0.00864298 and 0.00557907;
the derivative-loss margins exceed 10.65 and 10.12 respectively.
All eight printed cube bounds are outward, including the rows for which substituting
rounded B₁ and L₁ ceilings would change the last printed digits.
The module evaluates B₁ and L₁ from their formulas.

Two review concerns were corrected before the final run:

- **N1, closed:** selecting one interval as the maximum when the intervals overlap can
  discard a possible upper endpoint.
  `interval_max` now takes the larger lower endpoint and the larger upper endpoint.
  Independent controls in both argument orders return `[2,4]` for intervals `[1,4]` and
  `[2,3]`.
- **N2, closed:** valid row-local inequalities do not establish the published continuous
  range if a caller moves a row’s starting point.
  The cube roster now checks the exact published starts and ends.
  Increasing case 2’s start by one fails that roster check while its local inequalities
  still hold.

The reviewer ran all **17 maintained tests: 17 passed in 0.22 seconds**. A separate
0.111-second probe exercised twelve altered claims or rows and four invalid inputs.
Every altered claim failed its intended predicate: stronger quarter coefficients,
missing rosters, a range gap, case 6’s excessive upper endpoint, invalid line-band
ordering or room, a nonpositive cube denominator, wrong outward table bounds and
inflated asymptotic floors.
Zero coefficients, noninteger quarter scales, negative ν₀ and unsupported exponents
raised domain errors.
Reducing both ambient mpmath contexts to five digits left all 108 returned checks
identical and left those ambient contexts unchanged.
The actual CLI returned the complete two-plus-eight parameter roster, and a controlled
false check made its aggregate result false and its return status 1.

Reproduce the maintained checks from `packing/` with project Python 3.14:

```bash
uv run --frozen --all-extras --group dev python -m cases.asymptotic.quarter_cube_constants
uv run --frozen --all-extras --group dev python -m pytest -p no:cacheprovider tests/test_quarter_cube_constants.py -q
```

The review also corrected the displayed cube master inequality in this document: its
height factor is k/2 − 1 in C’s source theorem.
Replacing that factor by k/2 gives the upper bound used in Proposition 3.1 and in the
maintained checker.

The geometric meaning of the imported constants remains a proof premise, including Q’s
41.933 pair-ratio ceiling and the reviewed small-angle and slit-transfer arguments.
The fourteen fresh ceiling checks evaluate the stated formulas; they do not replace
those arguments.
K = 9 retains the independent-per-box limitation of R Lemma 4.10. K = 13
inherits the previously accepted finite angle enumeration for R Lemma 4.9. No upstream
checker, large box replay, new finite-n packing bound or global-optimality claim enters
through this addendum.
The accepted source-review scope elsewhere in this record remains unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
