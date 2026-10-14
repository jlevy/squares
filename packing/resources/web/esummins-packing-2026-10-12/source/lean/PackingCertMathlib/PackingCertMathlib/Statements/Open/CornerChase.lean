import PackingCertMathlib.Statements.Open.LocalLock
import PackingCertMathlib.Statements.Open.SnapDown
import PackingCertMathlib.Statements.Open.PerimeterWalk

/-!
# -- OPEN: the CORNER CHASE -- POKE, NO-ROTATE, and the chase around the perimeter (A248)

`docs/proofs/corner_chase.md`.  The PI (2026-09-17, 00:30): the flat floor meeter `A` slides off the
wall to let a second meeter `B` poke down into the corner box; `B`'s tilt sense is forced (POKE); the
pair `(B, B')` on the wall cannot rotate out of the way at the Ψ-minimal optimum (NO-ROTATE); chasing
the pinning options around the perimeter without an interior square should contradict.

**POKE** [F] as a directional statement, [T] in its true form (`corner_chase.md` §1).  The tilt sense of
the poking meeter is NOT forced: the square with `cos θ = 3/5, sin θ = 4/5`, lowest vertex `(4/5, 9/10)`,
wall vertex `(0, 3/2)`, top vertex `(3/5, 23/10)` beside `A = [19/20, 39/20] × [0, 1]` is interior-disjoint
from `A`, meets the corner box, touches the wall, and has its lowest vertex FARTHER from the wall than
its highest (the CW sense); 7 of the 288 type-F corner views of the 764-packing corpus are CW.  What is
true (TOP-2, the poker's top vertex `T = (cos θ, y_T)` has `y_T ≥ 2`: TILT-MIN `y_V ≥ 1 − (δ − sin θ) tan θ`
and `(1 − sin θ) tan θ ≤ cos θ + sin θ − 1`) and its corollary FLAT-ABOVE (no flat wall square
`[0,1] × [y₀, y₀+1]` with `0 < y₀ < 2` coexists with the poker: `B`'s open diagonal `V → T` crosses its
interior) are recorded as axioms [T-prose]: `top_two`, `flat_above`.

**NO-ROTATE** [T] (`corner_chase.md` §2), derived from A233's `PsiMin` — which is a GLOBAL minimum, so
the retreat may move several squares: `psiMin_no_lowering` (theorem).  The retreat named is the
FLUSH-STACK exchange (A245's click at `y₀ = 1`): the wall pair `(B, B')` is replaced by `[0,1] × [1,2]`
and `[0,1] × [2,3]`.  Below side `4` the lower flush square meets no corner box and the upper one
meets the far box `TL` to depth exactly `4 − m` (`click_account`, axiom [T-prose]: the depth of a flush
square is `1 −` its distance to the corner), so `Ψ` falls by `d_BL(B) + d_TL(B') + d_BL(B') − (4 − m)`.
Theorem `no_rotate`: at a Ψ-minimal packing no flush-stack exchange with `d + d' + d'' > 4 − m` is a
packing — i.e. its window `[0,1] × [1,3]` minus `B ∪ B'` is met by a THIRD square (H-ROOM fails).  Who
supplies it without an interior square is the chase (`corner_chase.md` §3): the flat floor meeter `A`
never (it lies in `{v ≤ 1}`), the next corner's flat ceiling meeter always (its part below height 3 at
`u < 1`), so NO-ROTATE is satisfied EXTERNALLY at every wall of the pattern the chase leaves.

**The chase** (`corner_chase.md` §3–§4).  FLAT-ABOVE leaves one external way to supply a poker's wall
slot: the adjacent corner's poker on the same wall (the mutual tilted pair), and **TWO-POKERS**
(`two_pokers`, [T-prose] + a certified two-variable minimum) excludes it below
`s* = 3.9342370…` — above the whole k0 window (`two_pokers_window`).  So on the window every type-F
poker's slot is met by an interior square, one wall carries at most one type-F poker, and a
12-stuck packing with four type-F corners would need four free squares in four notches ([T] given
SEPARATE-NOTCHES [M]: no free square serves two adjacent notches, `notches248`) — the PI's "cannot
be pinned without an internal square", in incidence form, for type-F corners.  Above `s*` the
external 8-square ring exists (`external248` at 3.97), so the argument is a window statement.  What
it does not reach: corners of type T (both meeters tilted), 2 912 of the corpus's 3 056 corners.  The
closing statement is the axiom `corner_chase_closes` [C], consequence `optimal_psiMin_not_twelve_stuck`.

**Status (2026-09-17).**  `psiMin_no_lowering`, `no_rotate`, `two_pokers_window`,
`optimal_psiMin_not_twelve_stuck`: theorems.  `top_two`, `flat_above`, `click_account`, `two_pokers`:
axioms [T-prose] (`two_pokers` with a certified computation).  `corner_chase_closes`: axiom [C].
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- **Ψ-minimality is global**: no packing at the same side has a strictly smaller `Ψ`, whatever number
of squares it moves (`no_retreat_of_psiMin` is the one-square case). -/
theorem psiMin_no_lowering {n : ℕ} {s : ℝ} {Q : Fin n → Set RP} (h : PsiMin n s Q)
    (Q' : Fin n → Set RP) (hP' : IsPacking n s Q') : ¬ Psi s Q' < Psi s Q :=
  fun hlt => absurd (h.2 Q' hP') (not_le.mpr hlt)

/-- The flat wall square `[0,1] × [y₀, y₀+1]` on the wall `x = 0`. -/
def flatWall (y0 : ℝ) : Set RP := Icc (0 : ℝ) 1 ×ˢ Icc y0 (y0 + 1)

/-- The flat floor square `[δ, δ+1] × [0, 1]`. -/
def flatFloor (δ : ℝ) : Set RP := Icc δ (δ + 1) ×ˢ Icc (0 : ℝ) 1

/-- **TOP-2** [T-prose] (`corner_chase.md` §1.2, any `n`, any side): a square `B` of a packing meeting the
open corner box beside the flat floor meeter `A = [δ, δ+1] × [0,1]`, `0 < δ < 1`, has a point with
`u < 1` at height `≥ 2` (its top vertex, at abscissa `cos θ`): the crowd occupies `[0, ≥ 2]` along the
wall.  Proof: `B` is tilted (ONE-TILTED), its cap below height `1` lies in `{u ≤ δ}` (else it crosses
`int A`), so `y_V ≥ 1 − (δ − x_V) tan θ` with `x_V ≥ sin θ`, and `y_T = y_V + cos θ + sin θ ≥ 2` because
`(1 − sin θ) tan θ ≤ cos θ + sin θ − 1 ⟺ sin θ (1 − cos θ) ≤ 1 − cos θ`. -/
axiom top_two (n : ℕ) (m : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n m Q) (i j : Fin n) (hij : i ≠ j)
    (δ : ℝ) (hδ : 0 < δ ∧ δ < 1) (hA : Q i = flatFloor δ) (hB : MeetsCell (Q j) 0 1 0 1) :
    ∃ p ∈ Q j, p.1 < 1 ∧ 2 ≤ p.2

/-- **FLAT-ABOVE** [T-prose] (`corner_chase.md` §1.3): no flat wall square `[0,1] × [y₀, y₀+1]` with
`0 < y₀ < 2` is interior-disjoint from the poker `B`: `B`'s open diagonal from its lowest vertex
(`u = x_V ∈ (0, 1)`, height `< 1`) to its top vertex (`u = cos θ ∈ (0,1)`, height `≥ 2`) is interior to
`B` and crosses the band `(0,1) × (y₀, y₀+1)`.  In particular the second meeter of the wall slot
`(0,1) × (1,2)` above a type-F corner is never a flat wall square. -/
axiom flat_above (n : ℕ) (m : ℝ) (Q : Fin n → Set RP) (hP : IsPacking n m Q) (i j k : Fin n)
    (hij : i ≠ j) (hjk : j ≠ k) (hik : i ≠ k) (δ : ℝ) (hδ : 0 < δ ∧ δ < 1) (hA : Q i = flatFloor δ)
    (hB : MeetsCell (Q j) 0 1 0 1) (y0 : ℝ) (hy : 0 < y0 ∧ y0 < 2) (hC : Q k = flatWall y0) : False

/-- The FLUSH-STACK exchange of the wall pair `(i, j)`: `Q'` agrees with `Q` off `{i, j}` and puts the
flush squares `[0,1] × [1,2]`, `[0,1] × [2,3]` in their place (A245's click at `y₀ = 1`). -/
def FlushStack {n : ℕ} (Q Q' : Fin n → Set RP) (i j : Fin n) : Prop :=
  i ≠ j ∧ (∀ k, k ≠ i → k ≠ j → Q' k = Q k) ∧ Q' i = flatWall 1 ∧ Q' j = flatWall 2

/-- **CLICK-ACCOUNT** [T-prose] (`corner_chase.md` §2.1): at a side `3 ≤ m < 4`, if `B = Q i` meets no
corner box but `BL` (corner `0`) and `B' = Q j` no box but `BL` and `TL` (corner `3`), then the flush
stack changes `Ψ` by exactly `(4 − m) − depthC m 0 (Q i) − depthC m 3 (Q j) − depthC m 0 (Q j)`: the
lower flush square `[0,1] × [1,2]` has depth `0` at every corner, the upper one `[0,1] × [2,3]` has depth
`4 − m` at `TL` (its distance to the corner `(0, m)` is `m − 3`) and `0` elsewhere. -/
axiom click_account {n : ℕ} (m : ℝ) (hm : 3 ≤ m ∧ m < 4) (Q Q' : Fin n → Set RP) (i j : Fin n)
    (hfs : FlushStack Q Q' i j)
    (hBi : ∀ c : Fin 4, c ≠ 0 → depthC m c (Q i) = 0)
    (hBj : ∀ c : Fin 4, c ≠ 0 → c ≠ 3 → depthC m c (Q j) = 0) :
    Psi m Q' = Psi m Q + (4 - m) - depthC m 0 (Q i) - depthC m 3 (Q j) - depthC m 0 (Q j)

/-- **NO-ROTATE** [T]: at a Ψ-minimal packing, a wall pair whose depths exceed the click's cost `4 − m`
admits no flush-stack exchange that is a packing — the window `[0,1] × [1,3]` minus the pair is met
by a third square (A245's H-ROOM fails).  Pure logic from `psiMin_no_lowering` and `click_account`. -/
theorem no_rotate {n : ℕ} (m : ℝ) (hm : 3 ≤ m ∧ m < 4) (Q : Fin n → Set RP) (hpsi : PsiMin n m Q)
    (i j : Fin n)
    (hBi : ∀ c : Fin 4, c ≠ 0 → depthC m c (Q i) = 0)
    (hBj : ∀ c : Fin 4, c ≠ 0 → c ≠ 3 → depthC m c (Q j) = 0)
    (hdeep : 4 - m < depthC m 0 (Q i) + depthC m 3 (Q j) + depthC m 0 (Q j))
    (Q' : Fin n → Set RP) (hfs : FlushStack Q Q' i j) : ¬ IsPacking n m Q' := by
  intro hP'
  apply psiMin_no_lowering hpsi Q' hP'
  rw [click_account m hm Q Q' i j hfs hBi hBj]
  linarith

/-- The TWO-POKERS threshold `s* = 2 + min_θ (tan(45° − θ/2) + tan(θ/2) + sec θ) = 3.9342370…`
(`corner_chase.md` §3.2; the minimum over the whole (θ, θ_f) triangle is certified ≥ 1.934236 by
146 403 monotone-enclosure boxes, `twopokers248`). -/
def twoPokersStar : ℝ := 3.934236

/-- **TWO-POKERS** [T-prose + T-computed] (`corner_chase.md` §3.2, any `n`): two wall-touching pokers
on one wall of `[0, m]²` — `B` meeting the lower corner box beside the lower corner's flat floor meeter
(offset `≤ 1`), `B'` meeting the upper corner box beside the upper corner's flat ceiling meeter — cannot
be interior-disjoint when `m < s*`.  Proof: TOP-2 puts `B`'s top vertex `T = (cos θ, ≥ 2)` above `B'`'s
bottom vertex `T' = (cos θ_f, ≤ m − 2)`; the vertical chords at `x = cos θ_f` and `x = cos θ` give
`m ≥ 2 + ψ(θ) + ψ(θ_f) + sin θ_f + max(cos θ_f tan θ, sin θ − (cos θ − cos θ_f) cot θ_f)`, `ψ = (1 − sin)/cos`,
whose minimum is `s* − 2` on the line `θ + θ_f = 90°` (certified over the triangle).  Stated for the wall
`x = 0` (the others are D4 images); the flat meeters' offsets `δ, δ' < 1` are what `flatFloor`/the
ceiling square encode. -/
axiom two_pokers (n : ℕ) (m : ℝ) (hm : m < twoPokersStar) (Q : Fin n → Set RP) (hP : IsPacking n m Q)
    (i j k l : Fin n) (hij : i ≠ j) (hkl : k ≠ l) (hik : i ≠ k) (hjl : j ≠ l) (hil : i ≠ l) (hjk : j ≠ k)
    (δ δ' : ℝ) (hδ : 0 < δ ∧ δ < 1) (hδ' : 0 < δ' ∧ δ' < 1)
    (hA : Q i = flatFloor δ) (hB : MeetsCell (Q j) 0 1 0 1) (hBw : TouchesLeftWall (Q j))
    (hA' : Q k = Icc δ' (δ' + 1) ×ˢ Icc (m - 1) m) (hB' : MeetsCell (Q l) 0 1 (m - 1) m)
    (hB'w : TouchesLeftWall (Q l)) : False

/-- On the k0 window (`m ≤ ŝ = 3.877084 < s*`) no wall carries two type-F pokers. -/
theorem two_pokers_window (n : ℕ) (m : ℝ) (hm : m ≤ 3.877084) (Q : Fin n → Set RP)
    (hP : IsPacking n m Q) (i j k l : Fin n) (hij : i ≠ j) (hkl : k ≠ l) (hik : i ≠ k) (hjl : j ≠ l)
    (hil : i ≠ l) (hjk : j ≠ k) (δ δ' : ℝ) (hδ : 0 < δ ∧ δ < 1) (hδ' : 0 < δ' ∧ δ' < 1)
    (hA : Q i = flatFloor δ) (hB : MeetsCell (Q j) 0 1 0 1) (hBw : TouchesLeftWall (Q j))
    (hA' : Q k = Icc δ' (δ' + 1) ×ˢ Icc (m - 1) m) (hB' : MeetsCell (Q l) 0 1 (m - 1) m)
    (hB'w : TouchesLeftWall (Q l)) : False :=
  two_pokers n m (by unfold twoPokersStar; linarith) Q hP i j k l hij hkl hik hjl hil hjk δ δ' hδ hδ'
    hA hB hBw hA' hB' hB'w

/-- **[OPEN] CORNER-CHASE** [C]: the chase's closing statement — no Ψ-minimal optimal eleven-square
packing below side `4` is 12-stuck.  What is proved of it: POKE's true form, NO-ROTATE, and that the
external chase is CONSISTENT (an 8-square ring realises it), so the statement rests on the room for
the three free squares (POCKET(11)), exactly A246's residue. -/
axiom corner_chase_closes (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hopt : ∀ s' : ℝ, Fits 11 s' → m ≤ s') (hpsi : PsiMin 11 m (fun i => (z i).set))
    (h12 : TwelveStuck m z) : False

/-- The consequence the chase would buy: an optimal Ψ-minimal packing below `4` is not 12-stuck (with
`wall_slot_link` and K0-FREE it then raises to a corner slot, `no_packing_of_stuck_exist`'s route). -/
theorem optimal_psiMin_not_twelve_stuck (m : ℝ) (hm : m < 4) (z : Cfg) (hz : CfgPacking m z)
    (hopt : ∀ s' : ℝ, Fits 11 s' → m ≤ s') (hpsi : PsiMin 11 m (fun i => (z i).set)) :
    ¬ TwelveStuck m z :=
  fun h12 => corner_chase_closes m hm z hz hopt hpsi h12

#print axioms psiMin_no_lowering
#print axioms top_two
#print axioms flat_above
#print axioms click_account
#print axioms no_rotate
#print axioms two_pokers
#print axioms two_pokers_window
#print axioms corner_chase_closes
#print axioms optimal_psiMin_not_twelve_stuck

end PackingCert.S11.OpenLemmas
