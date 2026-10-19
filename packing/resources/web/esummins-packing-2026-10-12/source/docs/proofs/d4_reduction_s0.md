# The D4 container-symmetry reduction, machine-checked at s0 — A67, 2026-09-02

Addendum discharging checklist item **H12** / depgraph node **D.D4** ("the reduction lemma at
3.84 (A27's `verify_tree2` semantics) must be re-proved at s₀"). The re-run is
**PASS**; this file states exactly what that buys and what it does not.

Verifier: `attempts/A67-d4-rerun/code/verify_d4_s0.py`. It **imports** A27's own
`caselp.py`, `level1.py`, `refine.py`, `verify_tree2.py` and rebinds the two module-level side
constants (`verify_tree2.S`, `refine.S`) — no A27 source is copied or edited, so "same
semantics, same verifier, side changed" is literal. Every predicate is
`fractions.Fraction`-exact.

```
python code/verify_d4_s0.py                                  # s0  -> results/d4_s0.json     PASS  36.7 s
python code/verify_d4_s0.py --s 96/25 --out results/d4_384_control.json
                                                             # 3.84 -> control               PASS   0.1 s
python ../A27-close-384/verify_tree2.py --skip_leaf_verify    # 3.84 harness anchor           PASS  19.1 s
```

## D4.1 What the reduction says

At side s the container is C(s) = [0,s]², the zone is Z(s) = [½+cw, s−½−cw]² with cw = 3/5,
and the fundamental triangle is T(s) = {(x,y) : s/2 ≤ y ≤ x ≤ s−½−cw}. The claim
(`level1.py` docstring, A14 §1) is: *given the certified root occupancy lemma at s — every
11-packing in C(s) has a square whose centre lies in Z(s) — one may assume WLOG that the
witness square's centre lies in T(s) and its orientation in [0°, 90°].*

## D4.2 What was machine-checked at s₀ = 969271/250000 (all exact)

| id | statement | s₀ |
|---|---|---|
| R1 | Z(s₀) is concentric with C(s₀): (A+B)/2 = s₀/2 exactly, Z = [11/10, 694271/250000]² | PASS |
| R2 | the acting group is D4: the 8 signed-permutation matrices are distinct, closed, orders {1,2⁵,4²}, nonabelian — the unique nonabelian order-8 group with 5 involutions | PASS |
| R3 | every g ∈ D4 about (s₀/2, s₀/2) maps C(s₀) **onto** C(s₀) and Z(s₀) **onto** Z(s₀) (exact vertex images; affine bijections carry polytopes onto polytopes) | PASS |
| R4 | the 8 D4-images of T(s₀) **cover** Z(s₀): the octant decomposition is exhibited exactly — 8 triangles, each mapped into the convex T by an explicit element of D4 (3 vertex images), glued pairwise into the 4 quadrants along their shared diagonal, and the quadrants glued into Z because m−h = A and m+h = B exactly | PASS |
| R5 | orientation transport: for each g, M_g·R(t) = R(t′)·P with P a symmetry of the axis-aligned unit square and t′ = t for det +1, t′ = (1−t)/(1+t) (i.e. θ ↦ 90°−θ) for det −1. Both sides times (1+t²) are matrices of polynomials of degree ≤ 2, so agreement at 5 distinct rational t is an identity. Hence g(Q(c,θ)) = Q(g(c), θ′) with θ′ ∈ [0°,90°] | PASS |
| R6 | `verify_tree2` check (2) verbatim at s₀: 216 level-1 cells, x-cuts strictly increasing from m = s₀/2 to B, t-bins union exactly [0,1], cell ↔ rational box exact under A27's own `qbox`/`cell_ijk`, no cell dropped as vacuous or coreless; `level1.check_cover` PASS | PASS |
| R7 | `verify_tree2` check (6) bookkeeping at s₀: σ_t is an exact involution, `sigma_cell` is an involution on the 48 diagonal cells and undefined off-diagonal, the degree bins reflect exactly (k ↔ 5−k), σ swaps a diagonal cell's x/y ranges exactly, and **the t-bins are side-independent** (byte-identical at 96/25 and s₀ — they depend only on NTH) | PASS |
| R8 | census side (A53 `skeletons.py` / `skeletons2.py` at s₀): the 8 maps `d4_images` builds are **the same group of plane maps** as the container D4 of R2/R3; each preserves [0,s₀]², the slot lattice and the 4 corner anchors; `canon` is orbit-invariant and orbit-selecting on the whole corpus (7204 recursively-locked skeletons → 944 classes; 1110 Young slot-sets → 163 classes, D4-closed, ⊆ the locked corpus); and the Young slot map is D4-equivariant: g·slots(c, λ) = slots(g·c, λ) or slots(g·c, λᵀ) for all 8 g, 4 corners, 20 partitions | PASS |

R8 is the "consistent with the container symmetries" obligation the brief names, and it is what
`instratum_bridge.md` §E.2 consumes: the D4 element h = g′g⁻¹ it applies to a packing is an
element of *this* group, and its action on pin-sets is *this* equivariant slot map. The 1110/163
counts reproduce depgraph node **B.CENSUS** exactly.

## D4.3 One reported non-assertion (not a regression)

R7 does **not** assert that σ(box(i,i,k)) ⊆ box(i,i,5−k) in t-coordinates. That containment is
false, by ≈ 5.3·10⁻⁸ at the worst bin, in *both* directions across the mid-bin — because the
box t-endpoints are the outward-rounded dyadics `t_lo`/`t_hi` (denominator 2²⁴) and σ of one
rounding is not inside the other. `verify_tree2.py`'s own docstring records this, which is why
its check (6) evaluates the mirror's certified core against the σ-**image** box rather than
against the mirror's own box. The relation is a property of `t_lo`/`t_hi` alone, so it is
identical at 3.84 and s₀ — the 3.84 control run confirms the same relation multiset. Exact
per-bin gaps are in `results/d4_s0.json` → `checks.R7_sigma.sample_i0`.

## D4.4 What this does NOT establish

1. **No root lemma at s₀.** The WLOG's hypothesis — every 11-packing in [0,s₀]² has a centre in
   Z(s₀) — is a *separate* certified occupancy lemma. It exists at 3.84
   (`certs/casetree_3.84/root_interior_occupancy.json`, τ = 8.240152 < 11); at s₀ it does not.
   R1–R7 are conditional on it, exactly as at 3.84.
2. **No s₀ case tree.** `verify_tree2`'s certificate-consuming checks — (1) root, (3) core
   containment, (4) leaves, (5) refinement tiling, (7) closure — have **no input at s₀**: the
   162 leaf certificates are 3.84 objects. This is not a portability blocker in the reduction
   (nothing in R1–R7 baked in the side); it is the absence of a tree to verify. D.D4 is now
   discharged; D.TREE is not, and is not touched here.
3. **Nothing about tightness.** The reduction is a WLOG, so it removes a factor 8 from the
   search; it proves no bound. It also says nothing about S₁₁ (the square-permutation half of
   H12) — that is seam S6 / node D.S6, still open.
4. **Single implementation.** As with B.CENSUS, the D4 action is checked, not independently
   re-implemented; R8's group identity between the tree side and the census side is the closest
   thing to a cross-check and it holds.

## D4.5 The reduction as a Lean theorem, at every side (A78, 2026-09-02)

`lean/PackingCertMathlib/PackingCertMathlib/D4Wlog.lean`, on the D4 action of `Census.lean`
(R2/R3: `d4Apply`, `d4Apply_mul`/`inv`, `d4Apply_sqdist`, `d4Apply_image_container`; R5:
`d4Sq_set` — the tilt transport `t ↦ (1−t)/(1+t)` for the reflections with
`cosT_tRefl`/`sinT_tRefl`; R8: `d4Apply_slotCentre`, `skeleton_d4`):

* `d4_cover_zone` — R4 at every side `s` and zone width `cw`: for `p ∈ Z(s)` some `g ∈ D4`
  sends `p` into `T(s)` (sign-normalise, then swap if `|dy| > |dx|`);
* `d4_wlog` — D4.1 itself, CONDITIONAL on the root occupancy hypothesis exactly as D4.4(1)
  records: if every packing at side `s` has a square centred in `Z(s)`, then every packing at
  side `s` has a D4-image that is a packing at `s`, has a square centred in `T(s)`, all tilts in
  `[0,1]`, and whose squares are the explicit images `g '' (z j).set`.

D4.4 is unchanged: no root lemma at `s₀`, no `s₀` tree (D.TREE), nothing about `S₁₁` (D.S6). The
Python R6/R7 checks (verify_tree2's cells/t-bins) are tree machinery, not part of the WLOG's
mathematical content, and are not ported.
