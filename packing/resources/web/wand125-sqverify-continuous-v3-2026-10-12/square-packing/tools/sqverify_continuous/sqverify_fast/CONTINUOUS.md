# Continuous-angle mode

Version v3 (see `../PROVENANCE.md` for the version table and the `source_sha256`).

`sqverify-fast --continuous` checks a rectangle-density certificate at every orientation
instead of on a net of directions.
The code is `src/slab.rs`, with tests in `src/slab_tests.rs`.
Everything else it uses comes from the crate unchanged:

- the admission and D4 expansion (`certificate.rs`);
- the outward-rounded arithmetic (`interval.rs`, lemma I1 of SOUNDNESS.md);
- the exact axis sweep (`axis.rs`, lemmas A1 and A2);
- the exact oracle (`oracle.rs`).

## Claim

Let μ be the certificate's measure: each positive rectangle's mass is spread uniformly over
its eight images under the symmetries of K = [0, L]², so μ has total mass M.
Take a core side B, a threshold τ, and rationals 0 < ε < T ≤ 1/2 with T² + 2T − 1 > 0.
The run proves:

> every closed square P of side B with P ⊆ K, at any centre and any angle, has μ(P) ≥ τ.

It then checks that nτ > M exactly.
If n unit squares with disjoint interiors fit in a square of side L/B, scaling by B gives
n such squares of side B in K. Their boundaries have measure zero, so their captures sum to
at most M, which contradicts nτ > M.
Hence s(n) > L/B; the endpoint is excluded as well.

## Lemmas

**C1 (reduction).** μ is invariant under the eight symmetries of K. A reflection maps a
square at angle θ to one at −θ, and a square's angle only matters modulo π/2, so it is
enough to take θ ∈ [0, π/4].
A quarter turn about the centre of K preserves the angle modulo π/2 and maps any centre into
the closed north-east quadrant.
Write t = tan(θ/2), c = (1 − t²)/(1 + t²), s = 2t/(1 + t²), W = c + s and h = B/2. A square
lies in K exactly when |x − L/2| ≤ E and |y − L/2| ≤ E, where E(t) = L/2 − hW(t).
So the legal north-east poses are x = L/2 + uE(t) and y = L/2 + vE(t) with (u, v) ∈ [0, 1]²
and t ∈ [0, tan(π/8)]. That range of t lies inside [0, T].
E > 0 everywhere because W ≤ √2 and L² > 2B² (an exact premise).

**C2 (angle enclosures).** On [0, 1], c decreases and s increases. W increases on
[0, √2 − 1] and decreases after it, with maximum √2.
For a box t ∈ [ta, tb] ⊂ [0, 1/2], `angles` returns C = [c(tb), c(ta)] and
S = [s(ta), s(tb)], evaluated with directed rounding.
W is enclosed as follows:
- lower bound: min(W(ta), W(tb));
- upper bound: W at the end nearer √2 − 1 when the box lies on one side of it, otherwise
  `up(SQRT_2)` > √2.

Which side each end lies on is decided from directed bounds of t² + 2t − 1.

**C3 (centre bound for every angle of a box).** Fix the box midpoint (u0, v0) and the path
x_m(t) = L/2 + u0 E(t), y_m(t) = L/2 + v0 E(t). Xm and Ym enclose the path over the box.
In coordinates relative to the path centre, the inner rectangle
[x1.hi − Xm.lo, x2.lo − Xm.hi] × [y1.hi − Ym.lo, y2.lo − Ym.hi] lies in R − (x_m, y_m) at
every t of the box.
At a fixed angle, the section length of the centred square over the line ξ, clipped to
[b, e], is

σ(ξ) = min(e, (h − cξ)/s, (h + sξ)/c) − max(b, (−h − cξ)/s, (sξ − h)/c).

σ is concave, as a minimum of affine functions minus a maximum of affine functions, and the
area of the overlap is ∫ max(0, σ).
`section_lo` bounds σ(ξ) below for every (c, s) ∈ C × S and every h ≥ h.lo. Each quotient
is bounded with the sign of its numerator, and σ increases with h.
On each segment between knots, concavity gives ∫σ ≥ (σ(a) + σ(b))(b − a)/2, which is at
least the same expression with the lower bounds in place of σ(a) and σ(b). Taking positive
parts and summing over the segments gives a lower bound on the area at every t of the box.
The knots are the estimated breakpoints of σ at both end angles of the box. Their positions
affect accuracy only.

**C4 (classification).** A rectangle is *outside* every square of the box when one of the
following holds:
- it is separated from the square's bounding box, whose half-extent is at most hW, along
  x or y;
- along one of the square's axes (c, s) and (−s, c), the smallest possible distance between
  the centres, minus the rectangle's half-width c·hx + s·hy (or s·hx + c·hy), is at least
  h.hi.

It is *inside* when, along both axes, the largest possible distance plus that half-width is
at most h.lo. That condition says exactly that the rectangle lies in both slabs that define
the square.
All tests are interval comparisons over X × Y × C × S; there is no tolerance.
A child box's poses are a subset of its parent's, so a child may inherit the parent's
inside mass and boundary list.

**C5 (from the path to the box).** At fixed t, ∂F/∂x is the sum over rectangles of
ρ(ℓ(x1) − ℓ(x2)), where ℓ(z) is the length of the square's chord on the line x = z, clipped
to [y1, y2]. The same holds for ∂F/∂y.
F is Lipschitz in the centre, so these a.e. derivatives integrate.
`chord` encloses ℓ over X × Y × C × S with the same section formulas. A rectangle that is
inside or outside for the whole box contributes zero derivative.
For a pose (x, y, t) of the box, |x − x_m(t)| = |u − u0| E(t) ≤ dx, and likewise for y. The
path (x_m, y_m) → (x, y_m) → (x, y) stays in X × Y.
Hence F(x, y, t) ≥ F(x_m, y_m, t) − dx·Gx − dy·Gy.
A box is accepted only when the downward-rounded bound reaches the upward enclosure of τ.

**C6 (near the axis).** On t ∈ [0, ε], W increases, and A·W(ε) ≤ B is an exact premise, so
the square of side B at angle θ contains the concentric axis-aligned square of side A.
Its corners (±A/2, ±A/2) satisfy |c·x + s·y| ≤ (A/2)W ≤ h, and likewise along the other
axis.
That smaller square lies in K too, and μ is nonnegative, so the exact axis sweep of
`axis.rs` with core A over [L/2, L − A/2]² (lemma A1: the minimum is at a vertex of the
event grid) bounds every such pose. The default A is B/W(ε) rounded down to 10⁻⁹.

**Coverage of the search.** The roots are [ε, k₁], [k₁, k₂], …, [k_m, T], with each
endpoint enclosed outward, so neighbouring roots overlap.
A split halves one of u, v or t at a binary64 midpoint, so the two children's closed boxes
cover their parent.
A root is verified only when its stack empties. A node budget or a box below resolution
stops the root with a refusal and records an exact capture at the stopping pose.

## Tests

`cargo test --release --lib slab`:

- `angle_enclosures_contain_exact_values`: C, S and W against exact rationals.
- `box_bounds_hold_at_sampled_poses`: at random boxes and random poses, compared with the
  exact oracle. It checks:
  - inside and outside verdicts;
  - the area bound at the path centre;
  - the x-derivative enclosure against an exact difference quotient;
  - the whole box bound.
- `classification_near_the_edge`: small rectangles within 3% of the square's edges.

Mutations that each test catches: the area scaled by 1.0005; a section term scaled by 1.001;
the gradient halved; dx shrunk; the inside test loosened by 0.5% or 1%; the outside test
loosened by 2%.

## Limits

Points and segments in a format L candidate are not counted in the capture. Dropping
nonnegative mass only lowers the capture, so the bound stays valid. The counting step uses
the full mass M, so it stays valid too. Such a candidate simply loses that mass.
