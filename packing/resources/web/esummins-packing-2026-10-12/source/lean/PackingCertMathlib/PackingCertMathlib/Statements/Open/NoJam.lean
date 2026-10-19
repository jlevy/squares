import PackingCertMathlib.Statements.Open.BoxMeeters

/-!
# -- OPEN: NO-JAM — a corner whose box meeter floats dies by COUNT + ROOM — A262

`docs/proofs/no_jam.md`.  Setting as in `BoxMeeters.lean`.  A JAM corner (A261): a floor toucher `A` and a
FLOATER `C` meet the box, a wall toucher `X` sits above `C`; `C` lies in the wedge between a line of slope angle
`α′` (over `A`) and a line of slope angle `ξ > α′` (under `X`), which closes towards the wall.

**What is a theorem here.**
* `retreat_cone_core` [T]: the wedge OPENS away from the corner — for `α′ ≤ ψ ≤ ξ` in `[0, π/2]` the direction
  `+(cos ψ, sin ψ)` has non-negative components along both wedge normals (`sin (ψ − α′) ≥ 0`, `sin (ξ − ψ) ≥ 0`):
  `A` and `X` never block the retreat of `C` (the mirror of `strip_landing_core`).
* `retreat_leaves_box_core` [T]: a point at height `y ≥ h` moved by `μ (cos ψ, sin ψ)` with `μ sin ψ ≥ 1 − h` has
  height `≥ 1`: after a retreat of length `(1 − h_v)/sin ψ` the floater meets no floor-band cell.  With P4
  (RETREAT) of the normal form: a JAM floater is HELD by a square other than `A`, `X` (HELD-JAM, no_jam.md §2).
* `jam_count_core` [T]: the COUNT — walls with `τ_w` touchers, `e_w` of their two end boxes served by floaters,
  `τ_w + e_w ≤ k` (k = m − 2), `f ≤ Σ e_w` box floaters, `u` middle touchers, `r` further squares:
  the total is `≤ 4 k + u + r`.  At `m = 4`, `u = 0`, `r ≤ 1`: `≤ 9 < 11`.
* `opposite_slab_core` [T]: two disjoint floaters on opposite sides of `O`, each within `d < 1/2` of `O`, leave a
  slab of width `< 1`: no unit square contains `O` between them.
* `no_jam_of_count`, `box_meeters_262` [T from the axioms below]: the chain.

**What is not.**
* `jam_count` [C] = JAM-STRUCTURE + SPAN + JAM-ROOM (no_jam.md §3–5): a normal-form family-stuck packing on the
  window with a floating box meeter has at most `4 (m − 2) + 1` squares.  [M]: JAM rings of 8 EXIST on the whole
  window (margin 0.010 at ŝ, 0.004 at 3.82); every free square of every JAM ring found contains `O` (pierce
  margin ≤ −0.07 at ŝ); two opposite JAM corners leave NO free square.  Not certified: a 7-parameter corner
  certificate (priced in no_jam.md §5).  Meant at `m = 4`, `s ≤ ŝ`.

**Status (2026-09-22).**  theorems: `retreat_cone_core`, `retreat_leaves_box_core`, `jam_count_core`,
`opposite_slab_core`, `no_jam_of_count`, `box_meeters_262`; axiom [C]: `jam_count`.
-/

namespace PackingCert.S11.OpenLemmas

/-- **RETREAT CONE, core** [T]: the mirror of `strip_landing_core`. -/
theorem retreat_cone_core (α ψ ξ : ℝ) (h0 : 0 ≤ α) (h1 : α ≤ ψ) (h2 : ψ ≤ ξ) (h3 : ξ ≤ Real.pi / 2) :
    0 ≤ Real.sin (ψ - α) ∧ 0 ≤ Real.sin (ξ - ψ) := by
  have hp := Real.pi_pos
  constructor
  · exact Real.sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith)
  · exact Real.sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith)

/-- **The retreat leaves the floor band** [T]. -/
theorem retreat_leaves_box_core (y h μ sn : ℝ) (hy : h ≤ y) (hμ : 1 - h ≤ μ * sn) : 1 ≤ y + μ * sn := by
  linarith

/-- **JAM COUNT, arithmetic core** [T] (any `k = m − 2`). -/
theorem jam_count_core (k u r f : ℕ) (τ e : Fin 4 → ℕ) (hτ : ∀ w, τ w + e w ≤ k)
    (hf : f ≤ e 0 + e 1 + e 2 + e 3) :
    τ 0 + τ 1 + τ 2 + τ 3 + u + f + r ≤ 4 * k + u + r := by
  have h0 := hτ 0
  have h1 := hτ 1
  have h2 := hτ 2
  have h3 := hτ 3
  omega

/-- The count at `m = 4`: no middle toucher, room at most one ⟹ at most nine squares. -/
theorem jam_count_eleven (u r f : ℕ) (τ e : Fin 4 → ℕ) (hτ : ∀ w, τ w + e w ≤ 2)
    (hf : f ≤ e 0 + e 1 + e 2 + e 3) (hu : u = 0) (hr : r ≤ 1) :
    τ 0 + τ 1 + τ 2 + τ 3 + u + f + r < 11 := by
  have h := jam_count_core 2 u r f τ e hτ hf
  omega

/-- **OPPOSITE SLAB, core** [T]: a unit square containing `O` in its interior between two parallel supporting
lines at signed distances `−d₁ ≤ t ≤ d₂` from `O` needs width `1 ≤ d₁ + d₂`. -/
theorem opposite_slab_core (d₁ d₂ lo hi : ℝ) (hlo : -d₁ ≤ lo) (hhi : hi ≤ d₂) (hw : hi - lo = 1)
    (hd : d₁ + d₂ < 1) : False := by linarith

/-- **JAM-COUNT(n)** [C] (no_jam.md §3–5), meant at `m = 4` on the window `s ≤ ŝ`: structure + span + room. -/
axiom jam_count (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : NormalForm n m s Q) (hfl : FloatingMeeter n m s Q) : n ≤ 4 * (m - 2) + 1

/-- **NO-JAM(n) from the count** [T from `jam_count`]: more than `4 (m − 2) + 1` squares ⟹ no floating meeter. -/
theorem no_jam_of_count (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : NormalForm n m s Q) (hn : 4 * (m - 2) + 1 < n) : ¬ FloatingMeeter n m s Q := by
  intro hfl
  have h := jam_count n m s Q hP hlo hhi hfs hN hfl
  omega

/-- **BOX-MEETERS(n) through the count** [T from `jam_count`, `meeters_split`]; `n = 11`, `m = 4`: `9 < 11`. -/
theorem box_meeters_262 (n m : ℕ) (s : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n s Q)
    (hlo : (m : ℝ) - 1 < s) (hhi : s < m) (hfs : FamilyStuckN n m s Q)
    (hN : NormalForm n m s Q) (hn : 4 * (m - 2) + 1 < n) : BoxMeetersForm n m s Q :=
  meeters_split n m s Q hP hlo hhi hfs (no_jam_of_count n m s Q hP hlo hhi hfs hN hn)

#print axioms retreat_cone_core
#print axioms retreat_leaves_box_core
#print axioms jam_count_core
#print axioms jam_count_eleven
#print axioms opposite_slab_core
#print axioms no_jam_of_count
#print axioms box_meeters_262

end PackingCert.S11.OpenLemmas
