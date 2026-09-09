# Independent Polygon-Union Audit of the Five Dots

**Status:** reviewed in Session114 and confirmed by the independent exp145 replay in
Session115. All 361 exact uncovered areas were zero in one 39.06-second process.
This checks the finite-net portion of [T-023](../../frontier/RESULTS.md), using the same
rational input patches and dots with a different geometric computation.

## The Set the Checker Must Cover

Fix one proper rational rotation with orthonormal axes $u,v$. Let
$S=\{au+bv:|a|,|b|\le B/2\}$ be the closed, centred square of side $B$. For $u=(c,s)$
and $v=(-s,c)$, put

$$e=\frac B2(|c|+|s|),\qquad K=[e,q-e]^2.$$

Then $z+S\subseteq[0,q]^2$ exactly when $z\in K$. The checker requires $q-2e>0$, so $K$
has positive area.

Let $A_1,\ldots,A_4$ be the four closed rational owner patches, and let $p_1,\ldots,p_5$
be the five dots. Construct nine closed collision polygons:

$$F_i=A_i+(-S)\quad(1\le i\le4),\qquad
F_{4+j}=p_j+(-S)\quad(1\le j\le5).$$

Here $+$ denotes the Minkowski sum: all sums of one point from each set.
For compact convex polygons, this is the convex hull of the sums of their vertices.
In particular,

$$z\in F_i\iff(z+S)\cap A_i\ne\varnothing,\qquad
z\in F_{4+j}\iff p_j\in z+S.$$

Thus $K\subseteq\bigcup_{i=1}^9 F_i$ says that every contained core either meets an
owner patch or contains a dot.
A selected residual core cannot meet an owner patch: both it and each owner patch lie
inside strictly separated selected cores of distinct physical squares.
It must therefore contain a dot.

## Why an Exact Area Calculation Decides Coverage

Put $C_i=K\cap F_i$. Inclusion-exclusion gives

$$
\operatorname{area}\!\left(\bigcup_{i=1}^9 C_i\right)
=\sum_{\varnothing\ne I\subseteq\{1,\ldots,9\}}
(-1)^{|I|+1}\operatorname{area}\!\left(\bigcap_{i\in I}C_i\right).
$$

There are at most $2^9-1=511$ terms.
Each intersection is convex and is computed by rational half-plane clipping; the
shoelace formula gives its exact rational area.
An empty intersection permits pruning every superset containing it.
Zero-area intersections contribute zero, and all descendant intersections obtained by
adding further constraints also contribute zero.

The uncovered area must be nonnegative.
A negative computed value is an instrument error, never evidence of coverage.
If the uncovered area is zero, the finite closed union contains $\operatorname{int}K$:
otherwise an omitted point in the interior has a small open disk disjoint from the
closed union, contributing positive uncovered area.
The union is closed, so it also contains $K=\overline{\operatorname{int}K}$. This proves
actual coverage, including boundaries; it does not rely on a tolerance or on discarding
a set of measure zero without justification.

A positive uncovered area refutes these five dots on this particular relaxed four-patch
domain and orientation.
It does not construct a feasible packing of the four owners and seven residual squares,
or refute the broader conditional-cover method.

## Inputs and Independence

The source is the unchanged endpoint arm in
[exp143](../../campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json),
identified by Git blob `cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19`. The loader must
retain its actual repository-relative path and source revision.
The checker constructs the complete 361-orientation net independently from the declared
rational net parameters; proper rotations, uniqueness and completeness are required
inputs to an accepted result.
It does not import the production geometry, residual-domain decomposition, weighted
event-grid evaluator or source reconstructor.

The owner-patch containment and finite-net-to-physical-angle arguments remain shared
analytic premises, as specified in the
[physical transfer review](../../campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/five-dot-transfer-review.md).
The independent check confirms coverage only.
It does not compute the minimum mass, prove an LP optimum, enlarge the owner-class
family, or independently re-prove those analytic premises.
Agreement does not automatically change T-023’s confirmation classification.

## Prospective Acceptance Boundary

Before the target, pass synthetic controls with known full covers and exact gaps,
including overlapping, duplicate, nested, tangent and rotated polygons.
A mutation must turn a covered fixture into a positive exact deficit.
Input, source-binding, timeout and incomplete-manifest failures must remain visibly
unresolved rather than success.

The subsequent registered experiment accepts only if all 361 unique directions finish
under the declared guards with zero uncovered area.
A positive exact deficit rejects this replication and stops extension pending
discrepancy review. Failed controls, source mismatch, malformed geometry, exception,
guard refusal or a partial receipt provide no coverage verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
