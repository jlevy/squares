{{FRONT_MATTER}}

The side length recorded for a packing and the mathematical optimum $s(n)$ are different
claims. A polynomial can identify the recorded side exactly.
A feasible geometric realization establishes an upper bound on $s(n)$. Only an equal
lower bound establishes global optimality.
The tables below keep those three levels separate.

The source is the generated [`exact-values.json`](../../frontier/exact-values.json)
register. The paper copies no mathematical value from another file.

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
“Claim” describes the geometric and global status recorded for that value.

{{EXACT_FORMS}}

## Exact Checks for Current Polynomials

The record/KKT column gives decimal digits of agreement in that order.
“One real root” refers to the stated rational interval, not to all real roots of the
polynomial.

{{CHECK_SUMMARIES}}

## Missing Exact Values and Assigned Routes

Degree-only rows have an algebraic degree but no retained polynomial text.
Numeric-only rows have no recorded exact identity.
Routes and bead identifiers are reproduced from the register.

{{MISSING_VALUES}}

## Historical Source Polynomials

This collection keeps the current $n=1\ldots324$ values and their totals separate from
additional polynomial-side pairs printed in retained primary sources.
It includes superseded sides and facts beyond the current frontier.
A `source-invalid` row preserves a printed equation that may pass its algebraic checks,
but the source row does not furnish a valid packing upper bound.
Each entry carries its own attribution and source labels.
Its checks compare the polynomial with its printed side; they do not compare it with a
current packing’s KKT value.

{{HISTORICAL_SUMMARY}}

{{HISTORICAL_POLYNOMIALS}}

## Full Current Polynomial Catalogue

Each polynomial is primitive and is printed from its coefficient vector.
Expanded forms are split across display lines.
A high-degree polynomial is written as $P_n(s)=\sum_{k=0}^{d}a_ks^k=0$ followed by every
coefficient $a_k$; this preserves the full integer values while allowing long entries to
continue across pages.

{{CURRENT_POLYNOMIALS}}

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
