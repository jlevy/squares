# BC-261: Independent Review of the Uniform Leaf Producer

The current phase-I exporter and rational uniform-cell producer are mathematically sound
on their declared exact input domain.
An independently reconstructed uniform cell with an accepted Farkas certificate proves
infeasibility of one selected SAT cell throughout its declared rational angle, center
and side boxes. It supplies no complete case cover by itself.

This is session-092 phase 3, W7 `pipeline-improvement`, under BC-261. The review covers
[`exact_lp.py`](../../../../../src/sqpack/exact_lp.py) and
[`uniform_cell.py`](../../../../../src/sqpack/uniform_cell.py), with the
[BC-260 direct contracts](bc-260-direct-hybrid-contracts.md) as the mathematical
acceptance rule.
Independent geometry reconstruction and the complete small control cover
are separate phase-3 work.
Their eventual acceptance belongs to the coordinator.
No H-118 or H-120 target was executed, and no global packing conclusion follows.

The focused producer suite passed 15 tests after the coordinator repaired the
tie-breaking issue identified below.
Ruff and BasedPyright passed on both producer files and their two focused test files.

## Accepted Subset and Findings

| Surface | Verdict | Exact accepted subset |
| --- | --- | --- |
| `check_infeasibility` | Accepted under its scalar contract | Exact ordered arithmetic, complete original LP rows, nonnegative multipliers, exact cancellation and strictly positive recomputed gap |
| `prove_infeasible` | Accepted | A phase-I optimum produces a checked original-row certificate; feasible, budget and basis refusals remain refusals |
| `cell_lp_for_axes` | Accepted under its geometry contract | Ordered corners of genuine squares and every canonical pair with one explicit directed axis choice; no feasible seed needed |
| `build_uniform_cell` | Accepted | Unit squares, absolute center boxes, independent finite rational half-angle intervals, variable positive side and a selected alternative for each pair |
| Uniform error vector | Accepted analytically | Complete changing-normal and changing-corner products, evaluated at the same absolute center variables |
| Complete packing cover | Pending separate acceptance | The producer defines one selected cell and does not prove branch coverage |
| H-120 feature-family attachment | Pending | A proved inclusion or correctly enclosed retained-feature substitution, followed by complete target coverage |

No producer soundness blocker remains in that subset.
The following distinctions are required at its trust boundary:

- `check_infeasibility` accepts a caller-supplied scalar type and sign function.
  Its `rational_sign` does not validate rational types; the general arithmetic functions
  deliberately support exact algebraic fields as well.
  The rational artifact reader must reject floats, nonfinite numbers and other lossy
  representations before arithmetic, and must check the claimed gap against the
  recomputed gap. A passing descriptor constructor does not validate attached LP or
  certificate values.
- Exact producer arithmetic also requires a field-preserving `one`: Gauss-Jordan
  elimination computes `one / pivot`. With integer-only inputs and `one=1`, Python
  division can introduce floats.
  The reviewed uniform producer supplies `Fraction(1)` and rational rows, so its
  divisions remain exact.
  The division-free Farkas checker can separately accept exact integer coefficients and
  multipliers.
- `cell_lp_for_axes` validates the complete pair-choice mapping, but does not prove that
  arbitrary supplied corners are unit squares in the declared order.
  The uniform producer supplies exact unit corners itself, so that precondition holds on
  the reviewed path. A future external-corner consumer needs its own geometry check.
- Physical pair labels include the canonical pair, axis position and corner indices, but
  not the orientation sign.
  An independent reader must reconstruct full coefficients and right-hand sides;
  matching labels alone cannot bind direction.
  The descriptor does retain the sign.
- `UniformCell` and `ExactLP` are transport objects, not evidence that their contents
  were reconstructed correctly.
  The independent reader must compare the complete physical and bound rows, their
  errors, the variable order and the attached domain.
  A sparse dual can omit zero contributions; it cannot authorize an omitted physical
  alternative or silently change the descriptor.

These are explicit API premises and reader obligations, not evidence that a returned
certificate in the accepted exact domain is false.
The phase-3 reader owner received the number-type and orientation-binding requirements
during this review.

### Addressed Tie-Breaking Finding

The initial `solve` implementation chose the first negative multiplier by its position
in the current active list.
Its docstring claimed Bland’s least-original-index rule.
Those orders differ after a basis reorder or a pivot.
This was a **Medium** liveness and termination-guarantee finding, tracked by the
coordinator as `think-9ovl`; it did not invalidate an independently checked Farkas
contradiction.

The coordinator changed the selection to minimize `active[position]` among negative
multiplier positions.
The inactive list is already sorted, and strict improvement in the ratio comparison
retains the first, hence least-index, entering row on a tie.
The correction is accepted.

The retained regression
[`test_bland_choice_is_independent_of_starting_basis_order`](../../../../../tests/test_exact_lp_infeasibility.py)
uses $x\ge0$, $y\ge0$, $x+y\le1$ and objective $-x-y$. With one pivot and initial bases
`(0, 1)` and `(1, 0)`, both runs must reach $(1,0)$. The old position rule chose the
other optimal endpoint for the reversed basis.
This distinguishes the defect from an arbitrary choice among valid optima.
The updated regression passed in the independent 15-test replay.

## Phase-I Certificate Lifting

The original convention is $Az\le b$, with all variables free.
The auxiliary program is

$$
\min t\quad\text{subject to}\quad Az-wt\le b,\qquad -t\le0.
$$

The construction selects a full-rank original row basis $S$, sets $z_0=A_S^{-1}b_S$ and
$d=A_S^{-1}\mathbf1$, and fixes $w_i=1$ on $S$. For every other row it chooses
$w_j=1+\max(A_jd,0)$. Thus along $(z_0+td,t)$ the basis rows stay tight and every other
row’s left-hand-side rate is at most $-1$. A sufficiently large nonnegative height is
feasible. The first blocking nonbasis row, or the floor at height zero, adds an
independent row because its value changes along that edge.
This supplies the auxiliary starting vertex without a feasible source pose.

At an exact positive optimum $t_*$, the floor is inactive.
The nonnegative active dual multipliers satisfy

$$
\lambda^TA=0,\qquad \lambda^Tw=1.
$$

Multiplying the active equalities gives

$$
\lambda^Tb=\lambda^T(Az_*-wt_*)=-t_*<0.
$$

`prove_infeasible` places those multipliers at their original row indices and fills
other positions with zero.
Its guard refuses a nonzero floor multiplier.
It then calls `check_infeasibility` on the original LP, so neither the auxiliary
variable nor its weights are needed by the final reader.
The reader checks every multiplier sign, every original-variable cancellation and
$-\lambda^Tb>0$. Its conclusion is the contradiction $0=\lambda^TAz\le\lambda^Tb<0$,
independent of the objective or simplex search.

A zero phase-I optimum raises `feasible`; a negative artificial coordinate, exhausted
pivot budget or missing full-rank starting basis cannot become a certificate.
The checker itself needs no rank assumption, as the rank-deficient control demonstrates.
Every uniform outer LP has explicit bounds for every variable, which already supply a
full-rank row subset for this producer.
A general rank-reduction framework is not needed to run the reviewed uniform cells.

The certificate’s stored `gap` and pivot count are reporting fields.
A reader must recompute the mathematical gap and validate any fields it accepts as
receipt metadata.
It must not accept an `infeasible` status or a positive stored gap as a
substitute for the multiplier calculation.
Legal touching can give zero row residuals or zero dual gap; the required strict
contradiction preserves it.

## Arbitrary Selected-Axis Geometry

The arbitrary-cell path removes the feasible-seed dependency while keeping the existing
translation LP. Its variables are all $x$ translations, all $y$ translations and $L$.
Let $d_i$ denote a square’s translation from its supplied reference corners.
For a reference corner $q$, containment is expressed by its four weak wall inequalities.
For a chosen directed axis $n$, with square `lo` before `hi`, every one of the sixteen
corner pairs supplies

$$
n\cdot(d_{\rm lo}-d_{\rm hi})
\le n\cdot(q_{\rm hi}-q_{\rm lo}).
$$

All sixteen inequalities together are the selected support separation.
Requiring only one chosen corner pair would not suffice.
The source pose may overlap because the variables translate it; reference feasibility is
not used by the assembly.

For `uniform_cell`, the supplied reference squares are centered at zero, so those same
translation variables are absolute centers.
The corner order is $(-1,-1),(1,-1),(1,1),(-1,1)$ before the half-size rotation.
`edge_axes` consequently returns $(f_i,-e_i,f_j,-e_j)$, where $e=(c,s)$ and $f=(-s,c)$.
Positions 0 and 1 belong to square $i$; positions 2 and 3 belong to square $j$.
Orientation `+1` places $i$ before $j$ along that chosen normal; `-1` reverses their
order.
The four positions and two signs cover the usual four SAT axes in both directions.

Negative orientation swaps which square owns the first corner index in a physical row
label. This does not alter the error formula because its two square radii and
center-difference bounds enter symmetrically.
The normal owner is determined by the axis position, not by the `lo`/`hi` order.

The complete pair inventory is checked exactly.
The descriptor requires every canonical pair once in lexicographic order and rejects
reversed, missing or repeated pairs.
Strict integer checks reject bool and float axis indices and signs.
A selected alternative is still one branch: the eight alternatives for each unrestricted
pair remain a separate cover obligation.

## Uniform Error Proof

For finite real half-angle coordinates,

$$
c(t)=\frac{1-t^2}{1+t^2},\qquad
s(t)=\frac{2t}{1+t^2},\qquad
c'(t)=\frac{-4t}{(1+t^2)^2},\qquad
s'(t)=\frac{2(1-t^2)}{(1+t^2)^2}.
$$

The denominator is positive.
The inequalities $2\lvert t\rvert\le1+t^2$ and $\lvert1-t^2\rvert\le1+t^2$ give
$\lvert c'\rvert,\lvert s'\rvert\le2$ for every real $t$. Thus at chart radius
$\delta_i$, each corner coordinate changes by at most $2\delta_i$, and each unit normal
coordinate changes by at most $2\delta_i$. This is a half-angle-coordinate radius, not a
radius in radians.

For a pair row, let $D=C_{\rm lo}-C_{\rm hi}$ and $d=q_{\rm lo}-q_{\rm hi}$. The actual
residual is $n\cdot(D+d)$; the midpoint residual is $n_m\cdot(D+d_m)$. Their difference
is

$$
(n-n_m)\cdot D+(n-n_m)\cdot d+n_m\cdot(d-d_m).
$$

For center intervals $I,J$, the maximum possible coordinate difference is
$\max(\lvert I_- - J_+\rvert,\lvert I_+ - J_-\rvert)$. Let the two coordinate bounds be
$D_x,D_y$, and let the selected normal’s owner be $k$. Each centered unit corner
coordinate has absolute value at most one, so each coordinate of $d$ is at most two in
absolute value. Each coordinate of $n_m$ is at most one.
Therefore the three terms above have total absolute value at most

$$
E_{ij}=2\delta_k(D_x+D_y)+8\delta_k+4\delta_i+4\delta_j.
$$

This is exactly `_physical_errors`. The $8\delta_k$ term covers products of a changing
normal and corner offsets; retaining only the center contribution would be unsound.
The bound is conservative but valid for the entire declared box, including negative
half-angle intervals and all its interior points.
Endpoint tests check implementation signs and indexing; they are not the proof of this
uniform bound.

A wall residual changes by at most $2\delta_i$. Its side coefficient is exactly $0$ or
$-1$ and does not vary with angle, so variable $L$ needs no extra angular error.
The producer therefore uses the correct outward relaxation

$$
A_m z\le b_m+E.
$$

Every physical point satisfying its chosen original row satisfies that relaxed row.
The exact center and side bound rows have zero error and bind all variables used in the
estimate. Midpoint coefficients, endpoints and errors remain rational throughout.

Actual orientation is $2\arctan t$ modulo quarter turns.
Finite rational intervals are legitimate continuous charts; the proof does not assume
angles are acute or distinct.
At quarter-turn-equivalent endpoints, normals and corner labels can permute.
Keeping all relevant alternatives preserves the geometry, while any deduplication or
chart identification needs its own exact equivalence.
No axis, equal-angle or touching seam is removed by these formulas.

## H-120 Attachment and the Smallest Useful Next Step

The [accepted BC-273 pilot](bc-273-release-domain-independent-review.md) has ten
parameters, retained wall and segment equations, a variable side and two actual angle
parameters. The current generic box LP can safely forget the common-angle and retained
feature equalities if an adapter proves that every pilot packing maps into the stated
boxes and allowed SAT branches.
Excluding that larger domain would exclude the pilot.
Failure to exclude the larger domain says nothing about feasibility of the pilot.

Forgetting those equalities can be costly: four equal oblique angles become independent
box coordinates, and center relations that determine the contact block disappear.
This is a possible loss of proof strength, not an unsound relaxation.
A useful adapter should retain the exact axis-wall relations and exploit contact-forced
alternatives before introducing a large generic branching framework.
Every forced alternative requires a source-feature implication, and every other pair
must retain its complete SAT disjunction, including ties.

An affine family substitution at fixed angles can reuse the existing LP and Farkas
exporter, but it changes the uniform error problem.
Write the family centers as $C_i(t,\eta)$, where $\eta$ contains its remaining
parameters. The current proof compares changing angles at the same absolute centers.
After substitution the desired comparison also changes the centers to $C_i(t_m,\eta)$.
An additional term such as

$$
n_m\cdot\bigl(C_i(t,\eta)-C_i(t_m,\eta)
-C_j(t,\eta)+C_j(t_m,\eta)\bigr)
$$

must be enclosed, together with the analogous wall-center variation.
Reusing the current errors unchanged after midpoint substitution is unjustified.
Another valid approach keeps absolute center variables and adds independently justified
outer relaxations of the feature equations.
Axis-wall equalities involving $L$ have no angle-dependent center coefficient and can be
imposed exactly.

Two bounded routes deserve comparison.
The following are planning estimates in agent time, not measured target runtimes or
promised completion times:

| Route | First useful slice | Independent acceptance and unresolved cost |
| --- | --- | --- |
| Direct analytic cavity cover | One prospectively recorded 30-minute attempt to state and prove a finite geometric implication for the smallest useful closed BC-273 child | Reserve 15–30 minutes to review a completed implication; an unresolved geometric premise remains open |
| Family-affine LP adapter | One 30-minute descriptor/error design slice, then one 30-minute implementation/control slice using the existing exporter | Independent reconstruction and a complete SAT cover are still required; price target and replay from resulting controls and observed open leaves |

The analytic route can use the already accepted equivalence between exclusion and
coverage of the final square’s contained-center region by **interiors** of ten
forbidden-center polygons.
It must handle every admitted skeleton and allowed angle; closed polygon coverage can
incorrectly exclude legal touching.
It buys useful new mathematics without expanding the solver if a finite strict-cover
argument can be identified.
It should be attempted on a prospectively selected closed family, with the source
parent/seam control and uncovered siblings stated, rather than by enlarging generic
infrastructure first.

The affine route is justified when a concrete geometric obstruction identifies which
retained relation the box relaxation loses.
Reuse `ExactLP`, `prove_infeasible` and the independent reader; add one family adapter
with its substitution and error proof.
There is no need for a second exporter.
Its control packet must bind the exact Trump parent, variable-side wall dependence,
segment signs and margins, shared-angle relations, 9–10 recontact and the local-scope
separation.
A complete two-square cover does not discharge the eleven-square branch cover
or H-120’s sibling obligations.

The recommended next mathematical slice is the bounded analytic cavity argument for the
smallest useful accepted child.
If it exposes a specific relation that needs an LP certificate, that relation defines
the small adapter’s scope.
Neither route currently supports a target verdict, and neither a failed box LP nor a
partial cavity argument improves the retained global bound.

## Validation and Work Receipt

Actual review startup was the first clock read at `2026-09-07T07:18:30Z`, within the
parent phase that began at `07:17:24Z`. Inspection covered the two producers, the
existing verifier’s axis convention, both focused test files, BC-260 and the accepted
BC-273 review. The coordinator supplied and owns the small Bland correction; this
reviewer changed no source or test file.

From `packing/`, the independently executed focused command was

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /Users/levy/wrk/github/squares/packing/.venv/bin/python3 \
  -m pytest -q -p no:cacheprovider \
  tests/test_exact_lp_infeasibility.py tests/test_uniform_cell.py
```

The initial producer suite reported `14 passed in 0.25s`. After the Bland correction,
the same command reported `15 passed in 0.26s`, with no skipped test reported.
These tests cover dense rational and algebraic Farkas replay; changed signs, gaps, rows
and coefficients; touching feasibility; budget and rank refusals; all directed axis
owners; positive-width outer exclusion; widening and the old dual; endpoint row
residuals; and malformed descriptor choices and numbers.
The expanded suite adds the basis-order regression.
No test result is treated as a substitute for the analytic uniform proof.

Ruff `check --no-cache` passed on the two producers and their two focused test files.
The same four paths passed BasedPyright with zero errors, warnings or notes.
These are focused checks; this review does not claim the repository’s full validation
gate or the separately developing reader and cover tests passed.

Only this assigned Markdown report was written.
No Git operation, shared registry, new ID, dependency or external application was
changed. No scientific target or unretained numerical measurement was executed.
The report received the common documentation and de-slop passes.
The terminal review checkpoint was `2026-09-07T07:33:15Z`, 14 minutes 45 seconds (885
seconds) after startup.
Flowmark 0.4.0 passed its full auto-format check with `--no-cache`; the whitespace scan
found no trailing blanks; all five linked files existed; the guideline-footer count was
one; and the formatted report was reread for mathematical meaning.
No background command remains.

## Phase-4 Acceptance: Independent Reader and Two-Square Cover

The finished [`uniform_cell_check.py`](../../../../../src/sqpack/uniform_cell_check.py)
and [`uniform_cover.py`](../../../../../src/sqpack/uniform_cover.py) are accepted for
independent rational selected-cell replay and the complete flat cover of one declared
two-square root. No soundness correction was found.
This closes the corresponding phase-3 pending reader and small-control reviews; it does
not accept an eleven-square cover or the H-120 feature-family attachment.

The reader imports public receipt types but calls neither the producer’s geometry
builder and selected-axis assembler nor its Farkas checker.
It independently derives the midpoint corners from $(c+s)/2$ and $(c-s)/2$, constructs
normals $(f,-e)$, and rebuilds every wall row, sixteen-corner pair conjunction, uniform
allowance and variable bound.
Its four-endpoint center-difference maximum agrees with the producer’s bound.
The complete reconstructed midpoint LP, outer LP and error tuple must equal their stored
counterparts, including the objective, row order, labels, coefficients and right-hand
sides. A direction change therefore cannot hide behind an unchanged pair label.

The reader revalidates nested descriptor fields without relying on their constructors.
Stored interval endpoints, matrix entries, errors, identities and dual entries must be
actual `Fraction` objects.
For those rational fields, bool, int, float, NaN and substituted scalar representations
are refused at this receipt boundary; producer constructors may normalize ordinary input
integers before producing the receipt.
Exact `zero` and `one` are checked.
The reader independently sums the dense dual, requires nonnegative entries, exact
cancellation in every column and a strictly negative weighted right-hand side, and
returns the recomputed positive gap.
It consumes no asserted gap or solver status.

The cover reader takes an authoritative `expected_root` separately from the packet.
It revalidates both roots and requires equality.
Each leaf must retain exactly that root’s center boxes, actual half-angle intervals and
variable-side interval, and must choose pair `(0, 1)` with one of the four axis
positions and two signs.
Requiring eight leaves and equality with the eight-element alternative set also rules
out duplicates. Leaf order is immaterial.
Every leaf is then checked by the independent rational reader; one invalid or unresolved
leaf prevents acceptance.

The coverage implication is complete at this scope: every legal two-square packing in
the declared closed root has at least one of those directed separating axes.
Its parameters therefore satisfy a corresponding child’s physical conditions and their
uniform outer rows. A positive Farkas contradiction in every child excludes every such
packing. Children share the entire root domain, so no angle or center seam disappears
through interval subdivision.
Weak geometry preserves touching, coincident angles and axis endpoints; duplicate
physical axes need no deduplication argument because all eight alternatives remain.
The format has no recursive references, symmetry metadata or lemma substitutions whose
extra implications would need checking.

The caller must supply the intended root independently rather than adopting a root from
an untrusted proof packet.
A valid proof for a narrower, reflected or otherwise different root certifies only that
other root. The new root-mismatch controls exercise this distinction with independently
valid restricted leaves and a valid reflected packet, rather than merely corrupting
their arithmetic.

The focused replay ran once from `packing/`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /Users/levy/wrk/github/squares/packing/.venv/bin/python3 \
  -m pytest -q -p no:cacheprovider \
  tests/test_exact_lp_infeasibility.py tests/test_uniform_cell.py \
  tests/test_uniform_cell_check.py tests/test_uniform_cover.py
```

It reported `31 passed in 0.61s`, with no skipped test reported.
The new controls cover all directed normal owners, sign and physical-row mutations,
stale angles and bounds, lossy nested receipt fields, nonpositive or corrupted duals,
missing or duplicated alternatives, invalid individual leaves, restricted or reflected
root substitution, unsupported reference metadata, and feasible touching in every
zero-width alternative.
The positive-width complete-cover control also varies side over $[9/5,19/10]$;
acceptance is not confined to a fixed-side LP. Widened rows have a displayed feasible
outer point and refuse stale duals.
These controls corroborate the uniform implication proved in the preceding review;
endpoint sampling is not promoted to a uniform proof.

Ruff and BasedPyright passed on the two new modules and their tests, with zero type
errors, warnings or notes.
The coordinator’s separate record, mutation and pre-push checks were not rerun or
independently claimed by this slice.
H-120 still needs its own domain inclusion or sound feature substitution, complete
target coverage, source controls and scientific determination.
No target theorem work was performed here.

The phase-4 audit began at the actual clock read `2026-09-07T07:51:00Z`; the parent
phase began at `07:44:12Z` and its delegation wave at `07:49:50Z`. Only this addendum
was written. No code, test, Git, registry, ID or dependency change was made by this
reviewer. The terminal checkpoint was `2026-09-07T07:56:28Z`, 5 minutes 28 seconds (328
seconds) after startup.
Flowmark 0.4.0 passed its full auto-format check with `--no-cache`; the whitespace scan
found no trailing blanks; all seven linked files existed; and the guideline-footer count
was one. The formatted addendum was reread for meaning, and no background command
remains.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
