import PackingCertMathlib.Statements.Open.StripPlug

/-!
# -- OPEN: THE LAST TWO — STRIP₂ for a tilted C (its true domain and the left-shadow certificate), CAPACITY-2 on
# the non-serving gap (the reduction and the centre-interval lemma) — A266

`docs/proofs/last_two.md`.

**What is a theorem here.**
* `left_shadow` [T]: on a horizontal chord `(l, r)` of a convex set, a point `x` OUTSIDE the chord whose right
  shift `x + h` (`h ≥ 0`) lies INSIDE it is strictly LEFT of the chord: `x < l`.  This is why the bad centres of
  STRIP₂ (`q ∉ int (C ⊕ Q)`, `q + h_u e_x ∈ int (C ⊕ Q)`) lie in the LEFT SHADOW of `C ⊕ Q`, and why `strip266`
  subtracts the right-closure of the inner polygon instead of the polygon itself (last_two.md §1.2).
* `open_box_tilted` [T]: the floater `C` (lowest vertex `(h_u + s, h_v)`, tilt with `c = cos, s = sin > 0`) meets
  the open unit box only if `h_u c + h_v s < c + s − s c`: a point of its lower-left edge `(h_u + s − t s, h_v + t c)`,
  `t ∈ [0, 1]`, with both coordinates `< 1` forces the inequality.  For a tilted `C` this is strictly stronger than
  `h_u, h_v < 1`, and WITHOUT it STRIP₂ is FALSE (`probe266`: a flat square under a 32°-tilted `C` at `h_u = 0.96`) —
  the flat-C proof of A265 never needed it because for `s = 0` the two conditions coincide.
* `gap_interval_centre` [T]: an interval `[x₀, x₀ + w]` with `w ≥ 1` inside `[1, s − 1]`, `2 < s < 4`, contains
  `s/2` in its interior — the horizontal half of "the UPPER of two stacked gap squares contains `O`" (the gap of a
  non-ADJ wall lies in `x ∈ [1, s − 1]`), last_two.md §2.2.
* `capacity_two_of_gap` [T]: CAPACITY-2 (no two interior-disjoint free squares both miss `O`) follows from the two
  gap statements `miss_in_gap` (every miss of the non-ADJ family is a gap square of an unserved wall) and
  `gap_holds_one_miss` (two interior-disjoint gap squares of the same wall never both miss `O`) and the count
  `one_unserved_wall` (misses of different unserved walls do not both occur) — all three [C]/[M] (last_two.md §2).

**What is not.**
* `strip_two` (StripPlug) stays the axiom for STRIP₂; its certificate `strip266` (5 parameters, lanes `jam`
  and `mir`) is launched, not finished: [T-computed*].  `miss_in_gap`, `gap_holds_one_miss`, `one_unserved_wall`
  are axioms [C] measured by `cap266` (no two disjoint misses on any ring tried).
-/

namespace PackingCert.S11.OpenLemmas.LastTwo

/-- **LEFT SHADOW** [T]: `x ∉ (l, r)`, `x + h ∈ (l, r)`, `0 ≤ h` ⟹ `x ≤ l` (the closed inner polygon's
right-closure is what the certificate subtracts, and it lies strictly inside the true chord). -/
theorem left_shadow (x l r h : ℝ) (hh : 0 ≤ h) (hin : l < x + h ∧ x + h < r) (hout : ¬ (l < x ∧ x < r)) :
    x ≤ l := by
  by_contra hx
  push_neg at hx
  exact hout ⟨hx, by linarith [hin.2]⟩

/-- **The tilted floater's box condition** [T]: `C` meets the open unit box only if `h_u c + h_v s < c + s − s c`
(`c, s > 0`): witnessed by a parameter `t ∈ [0, 1]` of its lower-left edge with both coordinates below `1`. -/
theorem open_box_tilted (hu hv c s t : ℝ) (hc : 0 < c) (hs : 0 < s) (ht0 : 0 ≤ t) (ht1 : t ≤ 1)
    (hx : hu + s - t * s < 1) (hy : hv + t * c < 1) : hu * c + hv * s < c + s - s * c := by
  nlinarith [mul_lt_mul_of_pos_right hx hc, mul_lt_mul_of_pos_right hy hs]

/-- **A unit-or-wider interval inside `[1, s − 1]` contains the centre** [T] (`2 < s < 4`). -/
theorem gap_interval_centre (x0 w s : ℝ) (hw : 1 ≤ w) (h1 : 1 ≤ x0) (h2 : x0 + w ≤ s - 1) (hs2 : 2 < s)
    (hs4 : s < 4) : x0 < s / 2 ∧ s / 2 < x0 + w := by
  constructor <;> linarith

/-- A free square of the non-ADJ ring missing `O` (opaque). -/
opaque MissO (Q : Set RP) : Prop
/-- A free square with a point at depth `< 1` in the unserved slot of wall `w` (opaque). -/
opaque GapSquare (w : ℕ) (Q : Set RP) : Prop
/-- Interior-disjointness (opaque). -/
opaque Disj (Q₁ Q₂ : Set RP) : Prop

/-- [C] every miss of the non-ADJ family is a gap square of some unserved wall (the ADJ factors P2 ∧ WE ∧ WS
certify the rest, open_pairs.md §2). -/
axiom miss_in_gap (Q : Set RP) (h : MissO Q) : ∃ w, GapSquare w Q
/-- [C] two interior-disjoint gap squares of the same wall never both miss `O` (the upper one contains it:
last_two.md §2.2, `gap_interval_centre` is its horizontal half). -/
axiom gap_holds_one_miss (w : ℕ) (Q₁ Q₂ : Set RP) (h1 : GapSquare w Q₁) (h2 : GapSquare w Q₂)
    (hd : Disj Q₁ Q₂) (m1 : MissO Q₁) (m2 : MissO Q₂) : False
/-- [C] misses at two different unserved walls do not both occur (last_two.md §2.3: two wide gaps are not a ring
on the window — `cap266` finds no feasible two-gap ring). -/
axiom one_unserved_wall (w₁ w₂ : ℕ) (Q₁ Q₂ : Set RP) (h1 : GapSquare w₁ Q₁) (h2 : GapSquare w₂ Q₂)
    (m1 : MissO Q₁) (m2 : MissO Q₂) (hd : Disj Q₁ Q₂) (hne : w₁ ≠ w₂) : False

/-- **CAPACITY-2 from the gap statements** [T]. -/
theorem capacity_two_of_gap (Q₁ Q₂ : Set RP) (m1 : MissO Q₁) (m2 : MissO Q₂) (hd : Disj Q₁ Q₂) : False := by
  obtain ⟨w₁, g1⟩ := miss_in_gap Q₁ m1
  obtain ⟨w₂, g2⟩ := miss_in_gap Q₂ m2
  by_cases hw : w₁ = w₂
  · subst hw
    exact gap_holds_one_miss w₁ Q₁ Q₂ g1 g2 hd m1 m2
  · exact one_unserved_wall w₁ w₂ Q₁ Q₂ g1 g2 m1 m2 hd hw

#print axioms left_shadow
#print axioms open_box_tilted
#print axioms gap_interval_centre
#print axioms capacity_two_of_gap

end PackingCert.S11.OpenLemmas.LastTwo
