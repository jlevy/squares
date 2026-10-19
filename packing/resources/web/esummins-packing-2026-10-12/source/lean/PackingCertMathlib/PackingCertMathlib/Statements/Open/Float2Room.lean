import PackingCertMathlib.Statements.Open.NoJam
import PackingCertMathlib.Statements.Open.RingPocket

/-!
# -- OPEN: FLOAT2 ROOM — the room statement of link 5d is CAP-2 at the corner — A277

`docs/proofs/float2_room.md` (derivation in `attempts/A277-float2-room/notes/float277_part0..8.md`).  Setting as
in `NoJam.lean`: a doubly-met corner box whose two meeters `C`, `D` both FLOAT (no wall toucher meets the box).
Drops `T_u(F) = F − h_u e_x`, `T_v(F) = F − h_v e_y`; a BLOCKER of a drop is a square whose interior meets the
drop's interior.  `S_8` = two meeters per box; the POCKET squares are the squares interior-disjoint from `S_8`.

**What is a theorem here (any `n`).**
* `one_drop_core` [T]: BLOCKER-SIDE (`box_meeters.md` §1.2) makes every normal from a blocker of `T_v(F)` to `F`
  have `n_u < 0 < n_v`, and its mirror every normal from a blocker of `T_u(F)` to `F` have `n_u > 0 > n_v`; one
  square cannot do both (Lemma ONE-DROP, part 2.1).  The same core is Lemma MUTUAL (part 2.2): two floaters
  separated by a positive-slope line block at most the upper-left one's floor drop and the lower-right one's wall
  drop.
* `cap2_count_core` [T]: `n ≤ 8 + cap(S_8)` (every non-`S_8` square is a pocket square: `no_jam.md` §2.3 restated)
  and `cap ≤ 2` give `n ≤ 10 < 11`.  ROOM (`cap ≤ 1`) is one more than needed; for FLOAT2 it is false whenever a
  blocker outside `S_8` misses `O`, so CAP-2 is the statement.
* `cap2_of_diam` [T]: two interior-disjoint unit squares whose centres lie in a set of pairwise squared distance
  `< 1` do not exist (`inradius_sep`, A251) — the DIAMETER test of part 3.3: if the BL-sector admissible-centre
  region has diameter `< 1`, no two disjoint sector misses exist.
* `float2_ten` [T from the axiom]: a FLOAT2 corner with BL-CAP-2 and PAIR-certified other corners has `n ≤ 10`.

**What is not.**
* `Float2Corner`, `BLSectorMiss` are opaque (a normal-form FLOAT2 corner at side in `[3.82, ŝ]`; a unit square of
  the container interior-disjoint from `C`, `D` whose centre is in a BL sector and which misses `O`).
* `bl_cap2_float2` [C]: BL-CAP-2(C, D) — no two interior-disjoint BL-sector misses.  Certificate: the 6-parameter
  diameter tree of `attempts/A277-float2-room/code/cert277.py` (priced in part 6, not launched); the 4-parameter
  route through the drops needs STRIP-C / STRIP-D, which are the JAM strip lemma only when the blockers serve their
  far boxes (part 4).  [M]: on the dropped witness the region's diameter is 0.936.
-/

namespace PackingCert.S11.OpenLemmas.Float2Room

open PackingCert.S11.OpenLemmas

/-- **ONE-DROP / MUTUAL, arithmetic core** [T]: a separating normal cannot be both `(−, +)` and `(+, −)`. -/
theorem one_drop_core (nu nv : ℝ) (h1 : nu < 0) (h2 : 0 < nv) (h3 : 0 < nu) (h4 : nv < 0) : False := by
  linarith

/-- **The count with the spare** [T]: `n ≤ 8 + cap` and `cap ≤ 2` give `n ≤ 10`. -/
theorem cap2_count_core (n c : ℕ) (h : n ≤ 8 + c) (hc : c ≤ 2) : n ≤ 10 := by omega

/-- **CAP-2 by diameter** [T]: two interior-disjoint unit squares (inscribed discs of radius `1/2` about `c`, `d`)
with `c, d` in a set `X` of pairwise squared distances `< 1` cannot exist (`inradius_sep`). -/
theorem cap2_of_diam (X : Set RP) (hX : ∀ p ∈ X, ∀ q ∈ X, sqdist p q < 1) {S T : Set RP} {c d : RP}
    (hcX : c ∈ X) (hdX : d ∈ X)
    (hc : ∀ p : RP, sqdist p c < 1 / 4 → p ∈ interior S)
    (hd : ∀ p : RP, sqdist p d < 1 / 4 → p ∈ interior T)
    (hST : Disjoint (interior S) (interior T)) : False :=
  absurd (inradius_sep hc hd hST) (not_le.mpr (hX c hcX d hdX))

/-- A normal-form FLOAT2 corner (two floating box meeters `C`, `D`, no wall toucher meets the box) at a side in
`[3.82, ŝ]`: opaque. -/
opaque Float2Corner : Prop

/-- `Q` is a unit square of the container, interior-disjoint from `C` and `D`, with its centre in a BL sector and
`O ∉ interior Q`: opaque. -/
opaque BLSectorMiss (Q : Set RP) : Prop

/-- **BL-CAP-2(C, D)** [C] (float2_room.md §3): no two interior-disjoint BL-sector misses. -/
axiom bl_cap2_float2 (h : Float2Corner) (Q₁ Q₂ : Set RP) (h₁ : BLSectorMiss Q₁) (h₂ : BLSectorMiss Q₂)
    (hd : Disjoint (interior Q₁) (interior Q₂)) : False

/-- **FLOAT2 ⟹ n ≤ 10** [T from `bl_cap2_float2`]: `hpocket` abstracts part 3.1–3.2 — the pocket squares are
pairwise interior-disjoint, at most one contains `O`, and (the other corners being PAIR-certified) every other
pocket square is a BL-sector miss; with `m` pocket squares `n = 8 + m`; two disjoint misses are impossible, so
`m ≤ 2`. -/
theorem float2_ten (h : Float2Corner) (n m : ℕ) (hn : n = 8 + m)
    (P : Fin m → Set RP) (hdisj : ∀ a b, a ≠ b → Disjoint (interior (P a)) (interior (P b)))
    (hone : ∀ a b c, a ≠ b → b ≠ c → a ≠ c → BLSectorMiss (P a) ∧ BLSectorMiss (P b) ∨
      BLSectorMiss (P a) ∧ BLSectorMiss (P c) ∨ BLSectorMiss (P b) ∧ BLSectorMiss (P c)) : n ≤ 10 := by
  subst hn
  by_contra hlt
  push_neg at hlt
  have h3 : 3 ≤ m := by omega
  have a0 : (0 : ℕ) < m := by omega
  have a1 : (1 : ℕ) < m := by omega
  have a2 : (2 : ℕ) < m := by omega
  have h01 : (⟨0, a0⟩ : Fin m) ≠ ⟨1, a1⟩ := by simp
  have h12 : (⟨1, a1⟩ : Fin m) ≠ ⟨2, a2⟩ := by simp
  have h02 : (⟨0, a0⟩ : Fin m) ≠ ⟨2, a2⟩ := by simp
  rcases hone ⟨0, a0⟩ ⟨1, a1⟩ ⟨2, a2⟩ h01 h12 h02 with ⟨x, y⟩ | ⟨x, y⟩ | ⟨x, y⟩
  · exact bl_cap2_float2 h _ _ x y (hdisj _ _ h01)
  · exact bl_cap2_float2 h _ _ x y (hdisj _ _ h02)
  · exact bl_cap2_float2 h _ _ x y (hdisj _ _ h12)

#print axioms one_drop_core
#print axioms cap2_count_core
#print axioms cap2_of_diam
#print axioms float2_ten

end PackingCert.S11.OpenLemmas.Float2Room
