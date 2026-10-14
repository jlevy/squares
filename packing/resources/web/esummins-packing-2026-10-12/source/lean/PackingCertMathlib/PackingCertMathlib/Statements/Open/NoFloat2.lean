import PackingCertMathlib.Statements.Open.Float2Room

/-!
# -- OPEN: NO-FLOAT2 — no normal-form corner box is met by two floaters — A278

`docs/proofs/no_float2.md` (derivation in `attempts/A278-no-float2/notes/nofloat278_part0..5.md`).  Setting as in
`Float2Room.lean`: a corner box `B = (0,1)²` met by two FLOATERS `C`, `D` (no wall toucher meets the box), in a
normal-form (Φ₁-maximal) family-stuck packing at a side in `[3.82, ŝ]`.

**What is a theorem here (any `n`, any `s`).**
* `float_slope_core` [T]: FLOAT-SLOPE (part 2).  Two interior-disjoint unit squares of the quadrant both meeting the
  open box are separated only by positive-slope lines, and one of them (`C`) is upper-left of EVERY separator: a
  separating normal `n` with `n_u, n_v ≥ 0` puts the lower-left square in the triangle `{u, v ≥ 0, n·x ≤ β}` with
  `β < n_u + n_v` (the other square has a box point), while SQUARE-IN-TRIANGLE needs `β ≥ n_u + n_v`.  So A277's
  case (N) of MUTUAL is empty; `T_u(C)` and `T_v(D)` are blocked by squares `X`, `Y` outside `{C, D}` (Cor. 2.1).
* `shadow_cell_core` [T]: SHADOW-CELL (part 3).  If every point of a cell `T` outside the floater `F` lies in the
  shadow `Sh` of an obstacle set (no admissible square covers it), then every square `Z ≠ F` that avoids `F` and
  `Sh` misses `T`; so `M(T) ⊆ {F}` and P1 (Lemma CELLS, `|Π| = 1`) lands `F`.
* [T-computed] A277's Y-poke witness: the flat floor cell `[0.486, 1.486] × [0, 1]` is met by `D` alone in EVERY
  packing containing `C, D, X, Y` (disc test, margin 0.032; `attempts/A278-no-float2/code/cell278.py`).

**What is not.**
* `Float2Local` (the 4-square statement L of part 3: for every FLOAT2 quadruple `(C, D, X, Y)` some wall cell has its
  part outside `D` (or `C`) in the shadow of the four and misses the other three) and `NoFloat2` are opaque.
* `no_float2_of_local` [T-prose]: Theorem 3.1 — L implies NO-FLOAT2 (FLOAT-SLOPE + Cor. 2.1 + SHADOW-CELL).
* `float2_local` [C]: L itself.  Residual = part 4 (10 parameters with toucher blockers, 12 with free ones; s = ŝ is
  the worst case); certificate designed (prune / cell / shadow by cores), not priced below 10³ CPU-h, not launched.
* `no_float2` [T from the two axioms]: what would delete `bl_cap2_float2` from link 5d.
-/

namespace PackingCert.S11.OpenLemmas.NoFloat2

/-- **FLOAT-SLOPE, arithmetic core** [T]: a separating normal with both components `≥ 0` gives `β < n_u + n_v` (a
box point of the far square) while SQUARE-IN-TRIANGLE for the near square gives `n_u + n_v ≤ β`. -/
theorem float_slope_core (nu nv β : ℝ) (hbox : β < nu + nv) (htri : nu + nv ≤ β) : False := by
  linarith

/-- **SHADOW-CELL, set core** [T]: `T ⊆ F ∪ Sh`; a square `Z ≠ F` that avoids `F` and `Sh` misses `T`. -/
theorem shadow_cell_core {α : Type*} (T F Sh Z : Set α) (hT : ∀ p ∈ T, p ∉ F → p ∈ Sh)
    (hZF : ∀ p ∈ Z, p ∉ F) (hZSh : ∀ p ∈ Z, p ∉ Sh) : ∀ p ∈ T, p ∉ Z := by
  intro p hpT hpZ
  exact hZSh p hpZ (hT p hpT (hZF p hpZ))

/-- The local statement L (part 3): opaque. -/
opaque Float2Local : Prop

/-- NO-FLOAT2: no normal-form corner box at a side in `[3.82, ŝ]` is met by two floaters: opaque. -/
opaque NoFloat2 : Prop

/-- **Theorem 3.1** [T-prose]: L implies NO-FLOAT2 (FLOAT-SLOPE, Cor. 2.1, SHADOW-CELL). -/
axiom no_float2_of_local : Float2Local → NoFloat2

/-- **L** [C]: every FLOAT2 quadruple has a shadow cell.  Certified on A277's witness only. -/
axiom float2_local : Float2Local

/-- **NO-FLOAT2** [T from `no_float2_of_local`, `float2_local`]. -/
theorem no_float2 : NoFloat2 := no_float2_of_local float2_local

#print axioms float_slope_core
#print axioms shadow_cell_core
#print axioms no_float2

end PackingCert.S11.OpenLemmas.NoFloat2
