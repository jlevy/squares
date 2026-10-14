import PackingCertMathlib.Sideband

/-!
# -- OPEN: Lemma TWO-CONTACT — a tilted wall square is not held by ONE other contact (A219)

**What it asserts** (`docs/proofs/wall_torque.md` §2, any `n`, any side).  Let `q` be a unit
square with tilt `θ ∈ (0°, 90°)`, `θ ≠ 45°` (in the `t = tan(θ/2)` parametrisation: `0 < t < 1`,
`t ≠ √2 − 1`), lying in the upper half plane and touching the floor `y = 0` at its lowest
vertex `v` (unique for such `θ`).  Suppose the floor force `W > 0` acts at `v` along `(0, 1)`
and EXACTLY ONE further contact force `F` acts on `q`, at a point `p` of `q`.  Force balance gives
`F = −W (0, 1)`; torque balance about the centre then gives `(v − p) × (0, 1) = 0`, i.e. `p` lies on
the vertical line through `v`.  The geometric core proved here as an axiom-statement:

  **every point `p ≠ v` of `q` on the vertical line through the lowest vertex `v` is NOT a vertex
  of `q`** (`two_contact_core`).

Hence `p` is interior to an edge (or interior to `q`, impossible for a contact), and a frictionless
contact force at an edge-interior point is along that edge's normal — never vertical, since with
`0 < t < 1` no edge of `q` is horizontal (`sinT t ≠ 0` and `cosT t ≠ 0`).  Contradiction: a loaded
tilted wall square needs at least TWO further loaded contacts (squares or walls).

**The exception is genuine.**  At `θ = 45°` the vertical through `v` passes through the centre
and the opposite vertex; a flat square pressing on that vertex from above (force `−W e_y` at the
opposite vertex, along the flat square's edge normal) balances `q` with a single contact — A217's
torque-neutral "corner diamonds" (C5).  At `θ ∈ {0°, 90°}` the square is flush (edge contact,
no single touching vertex) and carries along-wall compression with zero torque — the simple
packing's rows; this is where the PI's L2 as stated ("squares cannot load along a wall without a
net torque") is false, and why L2's force is on the TILTED meeters (Lemma ONE-TILTED).

**Status (2026-09-14).**  [T] in prose (§2: the four vertex abscissae `cx ± (cos θ ∓ sin θ)/2` are
pairwise distinct unless `sin θ cos θ = 0` or `sin θ = cos θ`).  Lean obligation: unfold `q.set`
(`sqSet`, `aff`) and compare first coordinates — routine, not done.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- `p` is one of the four vertices of `q`. -/
def IsVertex (q : PSq) (p : RP) : Prop :=
  p = aff (baseCorner q) (edir q) 0 0 ∨ p = aff (baseCorner q) (edir q) 1 0 ∨
    p = aff (baseCorner q) (edir q) 1 1 ∨ p = aff (baseCorner q) (edir q) 0 1

/-- **[OPEN] Lemma TWO-CONTACT (geometric core).**  For a square of tilt strictly between
`0°` and `90°` and different from `45°`, with lowest point `v`, no vertex other than `v` lies on
the vertical line through `v`. -/
axiom two_contact_core (q : PSq) (h0 : 0 < q.t) (h1 : q.t < 1) (h45 : q.t ≠ Real.sqrt 2 - 1)
    (v : RP) (hv : v ∈ q.set) (hlow : ∀ p ∈ q.set, v.2 ≤ p.2)
    (p : RP) (hp : p ∈ q.set) (hcol : p.1 = v.1) (hne : p ≠ v) : ¬ IsVertex q p

#print axioms two_contact_core

end PackingCert.S11.OpenLemmas
