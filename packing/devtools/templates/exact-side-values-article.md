{{FRONT_MATTER}}

The side length recorded for a packing and the mathematical optimum $s(n)$ are different
claims. A polynomial can identify the recorded side exactly.
A feasible geometric realization establishes an upper bound on $s(n)$. Only an equal
lower bound establishes global optimality.
The tables below keep those three levels separate.

The [source register](../../frontier/exact-values.json.gz) retains the complete source
history. This report publishes current values and additional source records; superseded
sides and their redundant notes remain in the register.

## Coverage

{{REGISTER_SUMMARY}}

### Source identities

{{REGISTER_SOURCES}}

An irreducibility certificate proves irreducibility over $\mathbb{Q}$, and an isolating
interval selects one algebraic root.
Agreement with the printed frontier decimal checks that this root is the number the
record names. These checks do not establish a feasible packing, local optimality, or
global optimality. The KKT column reports an independently computed numerical value from
a source-labelled KKT local minimum when one is available.
It is a separate numerical agreement check, not an exact contact or geometry
certificate. Likewise, a PSLQ relation by itself remains a numerical candidate until
exact elimination, branch selection, and geometric feasibility link it to the packing.

## Closed-Form Families

{{CLOSED_FORM_FAMILIES}}

### Every recorded exact expression

The table includes integers and rational values as well as nonrational radical forms.
An exact rational feasibility bound $p/q$ in lowest terms has degree one and primitive
polynomial $qs-p=0$. Native witness sides and certified outward ceilings have distinct
provenance. The Rehwaldt finite refinements require the reported decimal, verified
decimal, exact fraction and retained witness side to agree exactly, together with
matching source/count evidence, complete replay receipts and geometric custody.
Daniel’s new arrangements retain the native fraction and full reported decimal, while
the verified 16-place display is its least upward decimal ceiling.
RyXu and Gupta rational bounds independently bind the native `exact_form`; both their
reported and verified 16-place displays are its least upward ceilings.
The linear polynomial describes the native fraction.
The RyXu $n = 51$ radical has a separate quadratic identity and reported and verified
upward displays. The earlier outward-ceiling identity at $n = 292$ remains in dated
acquisition, prior-state records and receipt controls; the current catalogue uses the
refined native fraction.
These finite identities do not determine an ideal stationary side or the unknown optimum
$s(n)$. “Claim” describes the geometric and global status recorded for each value.

{{EXACT_FORMS}}

## Exact Checks for Current Polynomials

The record/KKT column gives decimal digits of agreement in that order.
“One real root” refers to the stated rational interval, not to all real roots of the
polynomial. Recorded decimals ordinarily truncate or round the isolated root.
For a replay-backed SQUISH, RyXu or Gupta rational upper bound, the display is an upward
decimal ceiling: if its final printed unit is $u$, the exact rational side $r$ and
display $d$ satisfy $r\le d<r+u$. The register retains $r$ exactly and checks this
inequality; the decimal ceiling establishes no additional optimality claim.

{{CHECK_SUMMARIES}}

## Missing Exact Values and Assigned Routes

Degree-only rows have an algebraic degree but no retained polynomial text.
Numeric-only rows have no recorded exact identity.
Routes and bead identifiers are reproduced from the register.

{{MISSING_VALUES}}

The
[Rehwaldt n68 v1.2 report](../../resources/web/rehwaldt-n68-exact-root-2026-10-08/README.md)
defines a proposed side through a multivariate system of 153 rational polynomials and an
isolating root box. It supplies no univariate minimal polynomial.
Independent acceptance remains open under `think-nv5o`; the current n68 row retains the
earlier admitted finite rational witness.

[Wand125’s finer-net reports and n27 follow-up](../../resources/web/wand125-fine-net-lower-bounds-2026-10-08/README.md)
concern lower bounds rather than exact packing-side identities.
Their whole-net native replay and adoption remain open.
The
[Couzo extended-range reports](../../resources/web/couzo-extended-reports-2026-10-08/README.md)
retain decimal poses outside this report’s current range; those decimal prefixes supply
no additional exact polynomial identities.

The
[Daniel record-hunt certificates](../../resources/web/evand-record-hunt-2026-10-09/README.md)
add a pending exact rational side at n=132 (T-131) and a separate certificate for the
same exact n=155 side as Couzo’s T-128 offer.
Both source occurrences retain their own certificate and replay custody at V0/C0. Equal
n=155 sides establish neither local-minimum equivalence nor motion between packings;
these records update no current side or optimality status.

## Full Current Polynomial Catalogue

Each polynomial is primitive and is printed from its coefficient vector.
Expanded forms are split across display lines.
A high-degree polynomial is written as $P_n(s)=\sum_{k=0}^{d}a_ks^k=0$ followed by every
coefficient $a_k$; this preserves every integer value in a table whose digits wrap to
the reading width.

{{CURRENT_POLYNOMIALS}}

## Additional Source Polynomials

This collection keeps the current $n=1\ldots324$ values and their totals separate from
additional exact sides from retained primary sources.
These additional records include facts beyond the current frontier, source-invalid
proposals and roots awaiting geometric reconciliation.
Superseded sides are omitted.
A `catalogue` row retains a printed polynomial.
A `derived-from-source-closed-form` row retains the source’s expression and a polynomial
computed from it here; its citation identifies that expression rather than a printed
equation. Citations for the same polynomial and isolated root are merged.
A `source-invalid` row preserves a printed equation that may pass its algebraic checks,
but the source row does not furnish a valid packing upper bound.
An `unreconciled-source` row with `reported-source-polynomial` origin retains a
separately reported root whose polynomial and isolating interval have been independently
checked.
Its geometry and Lean replay await verification, so its assurance remains V0/C0.
The register preserves the complete source row, original checker flags and acquisition
identity. A root below a current finite bound does not update that bound without a
verified geometric realization and field-to-side linkage.

Finite source-certificate rows also retain exact rational sides awaiting packing
adoption.
Their native geometry replay receipts are recorded separately from that pending
adoption, which remains V0/C0. Each row shows its source revision, original certificate,
retained facts and replay status.
Its linear polynomial identifies the source side; adoption and global optimality require
their own evidence.

Each entry carries its own attribution and source labels.
Its checks compare the polynomial with the source’s side and, where retained, verify
that the closed form selects that root.
They do not compare it with a current packing’s KKT value.

{{HISTORICAL_SUMMARY}}

{{HISTORICAL_POLYNOMIALS}}

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
