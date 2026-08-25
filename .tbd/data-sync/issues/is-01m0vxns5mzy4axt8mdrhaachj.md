---
type: is
id: is-01m0vxns5mzy4axt8mdrhaachj
title: "TUTORIAL: add a prerequisites-and-further-reading section, plus what actually implements the exact arithmetic"
kind: task
status: open
priority: 1
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies: []
parent_id: is-01m0vxe4ntpat4xcagtf04c37z
created_at: 2026-08-25T07:38:07.412Z
updated_at: 2026-08-25T08:01:36.926Z
---
The tutorial declares its audience as "anyone arriving at this directory without a
background in the problem", then uses linear programming, primitive elements and minimal
polynomials, Gröbner bases in lex order, resultants, PSLQ/LLL integer relation,
Lagrange/Fritz-John conditions in determinant form, Jacobian nullity, Bouligand tangent
cones, interval-Newton, Krawczyk, Smale's α-theory, Lindemann–Weierstrass, and
Stillinger–Weber inherent structures. Every one is named in passing.
There is no place a reader can go to learn any of them, and no reference list at all:
§10's table points only to other documents inside this directory.

## What to reference

Group by concept, cite one good source each, and keep it to a reader's on-ramp rather
than a bibliography:

- **Linear programming**—what it is, polyhedra and vertices, the simplex and
  interior-point methods, bases and degeneracy, duality.
  Needed by §2 and, more urgently, by §4, whose corner mechanism is stated entirely in
  terms of "the LP's optimal basis" (see think-ejgd).
- **Real algebraic number fields**—primitive elements, minimal polynomials, root
  isolation, and why equality becomes decidable. Needed by §5.
- **Certified and interval numerics**—interval arithmetic, interval-Newton and
  Krawczyk, Smale's α-theory. §5 names all three in one sentence.
- **Symbolic elimination**—Gröbner bases and lex order, resultants.
- **Integer relation**—PSLQ and LLL, and what "finds a relation, not a proof" means.
- **Optimality conditions**—Lagrange and Fritz-John, why a rank drop supplies the
  missing equations, and why the condition is necessary and not sufficient.
- **Energy landscapes**—Stillinger and Weber's inherent structures, and the
  Doye–Miller–Wales 38-atom Lennard-Jones double funnel that §7's rarity premise rests
  on. Both are already cited in `SYNOPSIS.md`'s references; the tutorial invokes them
  with no pointer.
- **The problem's own literature**—Stromquist 2003, Trump 1979, Friedman's DS7 survey,
  Erdős–Graham, Nagamochi 2005, Bidwell 1998, Montanher 2018.
  All are archived locally under [`resources/`](resources/README.md), and the tutorial
  names several of them without saying that local copies exist.
  A tutorial that mentions "Stromquist proved" three times should link the paper.

## And what actually implements this here

Separate from outside reading, the tutorial never says how the exact arithmetic is done,
which is a fair question for a reader deciding whether to trust or reuse it.
The facts, from `pyproject.toml` and `src/sqpack/field.py`:

- **Exact `ℚ(α)` is hand-rolled and standard library only**: elements are polynomials
  with `fractions.Fraction` coefficients reduced modulo the minimal polynomial; equality
  is a zero-representative test and sign is rational-interval bisection over an
  isolating interval. No floating point in either decision path.
  No computer algebra system is involved.
- **SymPy is optional and marginal**—only `cases.trump11.derive_field` uses it, to
  re-derive a constant the verifier already carries.
- **The LP is `scipy.optimize.linprog` over HiGHS**, whose feasibility tolerance is the
  origin of the `polished` tier's floor (see think-i22v).
- **The screening annealer is Rust** (`sqsearch/`).
- **Named but deliberately unbuilt**: python-flint as an accelerated algebraic scalar
  (benchmarked at 177×–578× over `fractions` by degree), `msolve` for F4 Gröbner
  elimination and real root isolation, and any Lean formalisation.
  Worth listing precisely because a reader will assume a project doing exact algebra
  depends on a CAS, and it does not.

## Proposal

Two additions, since these serve different moments.
A short **prerequisites** note early—the four or five concepts a reader needs and where
to learn them—so §2 and §5 are not read cold.
A **further reading** section near §10 with the full grouped list plus the local
`resources/` copies and the implementation inventory above.
Keep both as links and one-line reasons, not summaries; the tutorial should not become a
survey.
