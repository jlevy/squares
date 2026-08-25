---
type: is
id: is-01m0vxh18tn84y586tps6sskf8
title: "TUTORIAL notation: define every symbol, fix collisions, and introduce them in reading order"
kind: task
status: open
priority: 1
version: 7
spec_path: explorations/packing/docs/project/reviews/review-2026-08-25-tutorial-pedagogy-and-accuracy.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0vxhwqe5yfntb1697t5rk15
  - type: blocks
    target: is-01m0vxv0f1v7nqpeq5a2kfwjwq
  - type: blocks
    target: is-01m0vz75fav40ygkba88fajt0p
parent_id: is-01m0vxe4ntpat4xcagtf04c37z
created_at: 2026-08-25T07:35:31.866Z
updated_at: 2026-08-25T08:05:05.642Z
---
The tutorial has no symbol table, and a reader meets each symbol where it is first used.
Audit of every backticked symbol in `TUTORIAL.md`, by first-use line.

## Defined where introduced, and fine

`(xᵢ, yᵢ)` centre (L74) · `θᵢ ∈ [0, π/2)` per-square angle (L74) · `t` the `n = 3` slider
(L194) · `ℚ(α)` and its primitive element `α` (L285) · `u = tan(a/2)` (L297) · `δ`
inflation slack (L497) · `p` superdisk exponent (L498).

## Never defined

- **`oᵢₖ,ₓ`** (L99), inside the containment row `0 ≤ xᵢ + oᵢₖ,ₓ ≤ s`. Neither `o`, nor
  the corner index `k`, nor the `,ₓ` component convention is introduced.
  [`SYNOPSIS.md`](SYNOPSIS.md#setup) does it properly: corners are
  `(xᵢ, yᵢ) + Rᵢ·(±½, ±½)`, write `oᵢₖ ∈ ℝ²` for the four corner offsets, `k = 1…4`.
  The tutorial dropped the setup and kept the consequence.
- **`β`** (L289). Step 3 of the field procedure opens with "`β = 0` iff its reduced
  representative is the zero polynomial" without ever saying what `β` is—no "let `β` be
  an element of `ℚ(α)`". Step 2 introduces *elements* generically and never names one.
  A second problem rides on the first: `β` is then used three ways in two lines—`β = 0`
  (the field element), `deg β` (the degree of its representative), and `β(α) ≠ 0` (that
  representative evaluated at `α`). `src/sqpack/field.py` keeps element and
  representative distinct in its docstring; the tutorial collapses them.
- **`a*`** (L120). Introduced only as "`0°` on six squares and `a*` on five", so a
  reader learns it is an angle and nothing else. It is the *minimising* value of `a`—the
  argument at which `φ` attains its minimum—which is what L128 and L234 then rely on.
  The `*`-means-optimal convention is never stated, and `a` itself does not appear until
  L124 (see order-of-introduction below).
- **`s*`** (L497, `slack δ in side s* + δ`). Single occurrence, no definition; the same
  unstated `*` convention, and here it means the standing-best side rather than a
  minimiser. Two different meanings for one decoration, neither written down.
- **`m`** in `s(m²) = m` (L23). Also `n` and `C(n,2)` are used without a word, which is
  probably fine, but `m` is not, because of the collision below.

## Collisions—one letter, two meanings

- **`m`**: the integer in `s(m²) = m` (L23) versus the minimal polynomial in
  `degree < deg m`, `reduced modulo m`, `deg β < deg m` (L287, L288, L293).
- **`α`**: the primitive element of `ℚ(α)` (L285, L293, L385) versus **Smale's
  α-theory** (L370)—both inside §5, four paragraphs apart.
- **`*`**: minimiser in `a*`, standing best in `s*`.
- **`gap`**: three senses. §1's table row `gap | 0.088229208023` is
  upper bound − lower bound; §3's "a gap decomposes into a polish failure or an
  exploration failure" and §8's "the remaining gap" are `best_side − standing_best`;
  L22's "the whole subject lives in that gap" is informal. Only the second matches the
  vocabulary card's definition at L618. The bound gap and the search gap are different
  quantities and should be named differently.

## Scalar versus vector, which is the reported confusion

L94 says "fix the angle vector `θ`", but §2's setup (L74) introduces only `θᵢ`, per
square. The vector `θ = (θ₁, …, θₙ)` is never written down, so "fix an angle `θ`" reads
as one angle rather than one angle per square, `i = 1…n`.
Same gap for the centres: the LP variable list `(x₁…xₙ, y₁…yₙ, s)` at L101 is the only
place the reader learns these are `2n` separate scalars and not two vectors.
A rule stated once—**subscript `i` means one square, bare means the whole `n`-vector**—
fixes every instance.

## Introduced out of order

- **`a*`** is used at L120 before **`a`** exists. `a` is only introduced at L124, inside
  a code fence, as part of an informal sentence rather than a definition.
- **`a` versus `θᵢ`**: `a` is the shared angle of Trump's five-square tilted class, so
  `θ = (0,0,0,0,0,0,a,a,a,a,a)` up to labelling. The tutorial never relates them, so a
  reader cannot tell whether `a` is a new object or a coordinate on the old one.
- **`s` versus `s(n)`**: `s(n)` is defined at L14 as the optimal value; bare `s` appears
  at L74 as a decision variable of the program. The distinction—one is the answer, the
  other is a variable being minimised—is never drawn, and it matters at L99 ("note `s`
  appears here, and only here, as a variable").
- **`φ`** (L124) is defined in a code fence as "the LP optimum of Trump's cell with the
  five tilted squares at angle a", with no domain, no codomain, and its dependence on
  the fixed cell only in the surrounding prose. §4 then reasons about `φ` heavily.

## Cross-document consistency, lower priority

Not tutorial bugs, but the same symbols disagree across the directory, so a glossary
should either match the other docs or say it is local:

- `θ` is the per-square angle in the tutorial and synopsis, but the *tilt of the five
  central squares* in the `n = 11` report (`research-2026-08-22-packing-11-unit-squares.md`,
  L1266)—which is the tutorial's `a`.
- `u` is the single primitive element `tan(a/2)` here, but the per-square rationalising
  parameter `u_i = tan(θ_i/2)` in the algorithms report (L94).
- `α` additionally means a gap distance (`n = 11` report L1265) and the Roth–Vaughan
  real parameter (L1443+).
- `ν` is the separating axis in `SYNOPSIS.md`, and the matching number of a hypergraph
  in the `n = 11` report (L1134).
- Subscripts are Unicode (`xᵢ`, `θᵢ`) in the tutorial and synopsis, ASCII (`x_i`,
  `θ_i`) in the algorithms report; `ℚ` here, `Q` there.

## Proposal

A short notation section early in the tutorial—before or at the top of §2, since §1 is
deliberately prose—listing each symbol, its type (scalar, per-square, `n`-vector,
field element), and where it is fixed versus free.
Then rename to remove the collisions, state what `*` decorates, introduce `a` before
`a*`, and state the subscript rule once.
Keep it a table the reader can return to; the vocabulary card in §9 is prose terms, not
symbols, and should stay separate and cross-link.
