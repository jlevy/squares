import PackingCertMathlib.Statements.Open.K0Count

/-!
# -- OPEN: Lemma WEDGED-SEAL — a corner meeter touching both walls is alone (A239)

`docs/proofs/wedged_seal.md`.  The PI (2026-09-16, 11:00): "take a square and push it into the corner so two of
its corners touch the two adjacent walls: no second meeter of the corner box is geometrically permitted, for any
rotation".

**The statement (any `n`, any side).**  A unit square `q` in the closed quadrant `{u ≥ 0, v ≥ 0}` that touches the
floor `v = 0` and the wall `u = 0` (`Wedged q`; tilt `θ ∈ [0°, 90°]`, so the flush slot square included) leaves the
open corner box `(0, 1)²` met by NO other unit square of the quadrant.  It is Corollary B1 of `sideband.md` §4
("pressed ⇒ lonely", A169, proved there from Theorem B's four clauses); `wedged_seal.md` gives the PI's direct
proof (the sealed triangle and the two wedges, the segment-crossing computation with the small and large tilts)
and the two-line proof from Lemma PUSH that is formalised here.

**The Lean content.**  Two interior-disjoint unit squares have a separating line parallel to an edge of one of
them (`sat_selection_thm`, a theorem of the project); `separates_of_gsel` turns that selection row into a
`Separates` witness (a unit normal `n` and a level `β` with `qw ⊆ {n·x ≤ β}`, `qo ⊆ {n·x ≥ β}`).  Lemma PUSH
(`lemma_PUSH`, axiom [T] in prose, `k0_count.md` §2) applied to the pair (`g`, `q`) says the normal pointing
INTO the wedged square has `n_u > 0` (it touches the floor) and `n_v > 0` (it touches the wall); applied to
(`q`, `g`) it says the normal pointing into `g`, which is `−n`, has a positive component.  Contradiction:
`wedged_seal_of_separates`, `wedged_seal`.  Consequence (prose): in a doubly-met open corner neither meeter
touches both walls (Cor. B1's form, the setting of PUSH / HOLD), and a meeter touching both walls is the corner's
only meeter, which K0-FREE teleports (`k0_route.md` §3).

**Status (2026-09-16).**  `wedged_seal`: theorem; its only non-standard dependence is `lemma_PUSH`.
-/

namespace PackingCert.S11.OpenLemmas

open Set
open PackingCert.S11.LocalCert

/-- WEDGED: the square touches the floor `v = 0` and the wall `u = 0` of the corner. -/
def Wedged (q : PSq) : Prop := (∃ p ∈ q.set, p.2 = 0) ∧ (∃ p ∈ q.set, p.1 = 0)

/-- A separating line read from the other side. -/
theorem Separates.symm {n : RP} {β : ℝ} {q₁ q₂ : PSq} (h : Separates n β q₁ q₂) :
    Separates (-n.1, -n.2) (-β) q₂ q₁ := by
  obtain ⟨hn, h1, h2⟩ := h
  refine ⟨?_, ?_, ?_⟩
  · change (-n.1) ^ 2 + (-n.2) ^ 2 = 1
    rw [neg_sq, neg_sq]
    exact hn
  · intro p hp
    have := h2 p hp
    change -n.1 * p.1 + -n.2 * p.2 ≤ -β
    linarith
  · intro p hp
    have := h1 p hp
    change -β ≤ -n.1 * p.1 + -n.2 * p.2
    linarith

/-- **Lemma WEDGED-SEAL, from a separating line.**  A wedged square `q` and a second meeter `g` of the open unit
box, both in the quadrant, cannot be separated by any line: Lemma PUSH on (`g`, `q`) makes both components of
the normal into `q` positive, Lemma PUSH on (`q`, `g`) makes one component of its negative positive. -/
theorem wedged_seal_of_separates (q g : PSq) (hq : q.t ∈ Icc (0 : ℝ) 1) (hg : g.t ∈ Icc (0 : ℝ) 1)
    (hqQ : InQuadrant q) (hgQ : InQuadrant g) (hqm : Meets q 1) (hgm : Meets g 1) (hw : Wedged q)
    {n : RP} {β : ℝ} (hsep : Separates n β g q) : False := by
  obtain ⟨_, hfloor, hwall⟩ := lemma_PUSH g q hg hq hgQ hqQ hgm hqm hsep
  have h1 : 0 < n.1 := hfloor hw.1
  have h2 : 0 < n.2 := hwall hw.2
  obtain ⟨hpos, _, _⟩ := lemma_PUSH q g hq hg hqQ hgQ hqm hgm hsep.symm
  rcases hpos with h | h
  · change 0 < -n.1 at h
    linarith
  · change 0 < -n.2 at h
    linarith

/-- `a·d = (d·e)(a·e) + (d·e⊥)(a·e⊥)` for a unit vector `e`, `e⊥ = (−e.2, e.1)`. -/
theorem dot_decomp (a d e : RP) (he : e.1 ^ 2 + e.2 ^ 2 = 1) :
    a.1 * d.1 + a.2 * d.2
      = (d.1 * e.1 + d.2 * e.2) * (a.1 * e.1 + a.2 * e.2)
        + (d.1 * (-e.2) + d.2 * e.1) * (a.1 * (-e.2) + a.2 * e.1) := by
  linear_combination (-(a.1 * d.1 + a.2 * d.2)) * he

/-- The support of a square in the direction `a`: `|a·(p − c)| ≤ (|a·e| + |a·e⊥|)/2` for `p` in the square. -/
theorem support_le (q : PSq) (a : RP) {p : RP} (hp : p ∈ q.set) :
    |a.1 * (p.1 - q.cx) + a.2 * (p.2 - q.cy)|
      ≤ (|a.1 * cosT q.t + a.2 * sinT q.t| + |a.1 * (-sinT q.t) + a.2 * cosT q.t|) / 2 := by
  obtain ⟨hu, hv⟩ := (mem_set_iff_uv q p).mp hp
  simp only [rdot, edir, perpV] at hu hv
  have hcs := cosT_sq_add_sinT_sq q.t
  have key := dot_decomp a (p.1 - q.cx, p.2 - q.cy) (cosT q.t, sinT q.t) hcs
  dsimp only at key
  rw [key]
  set u := (p.1 - q.cx) * cosT q.t + (p.2 - q.cy) * sinT q.t with hu_def
  set v := (p.1 - q.cx) * -sinT q.t + (p.2 - q.cy) * cosT q.t with hv_def
  set x := a.1 * cosT q.t + a.2 * sinT q.t with hx_def
  set y := a.1 * -sinT q.t + a.2 * cosT q.t with hy_def
  calc |u * x + v * y| ≤ |u * x| + |v * y| := abs_add_le _ _
    _ = |u| * |x| + |v| * |y| := by rw [abs_mul, abs_mul]
    _ ≤ 1 / 2 * |x| + 1 / 2 * |y| := by
        gcongr
    _ = (|x| + |y|) / 2 := by ring

/-- A separating line from a separating AXIS `a` (unit), a sign `eps = ±1`, the owner's own support bound, the
other square's support bound `≤ wrel` and the selection inequality. -/
theorem separates_of_axis (qw qo : PSq) (a : RP) (ha : a.1 ^ 2 + a.2 ^ 2 = 1) (eps : ℝ)
    (heps : eps = 1 ∨ eps = -1)
    (hown : ∀ p ∈ qw.set, |a.1 * (p.1 - qw.cx) + a.2 * (p.2 - qw.cy)| ≤ 1 / 2)
    (hW : |a.1 * cosT qo.t + a.2 * sinT qo.t| + |a.1 * (-sinT qo.t) + a.2 * cosT qo.t| ≤ wrel qw qo)
    (hg : 1 / 2 + wrel qw qo / 2 ≤ eps * ((qo.cx - qw.cx) * a.1 + (qo.cy - qw.cy) * a.2)) :
    Separates (eps * a.1, eps * a.2) (eps * (a.1 * qw.cx + a.2 * qw.cy) + 1 / 2) qw qo := by
  have heps2 : eps ^ 2 = 1 := by rcases heps with h | h <;> subst h <;> norm_num
  refine ⟨?_, ?_, ?_⟩
  · change (eps * a.1) ^ 2 + (eps * a.2) ^ 2 = 1
    calc (eps * a.1) ^ 2 + (eps * a.2) ^ 2 = eps ^ 2 * (a.1 ^ 2 + a.2 ^ 2) := by ring
      _ = 1 := by rw [heps2, ha]; ring
  · intro p hp
    have hX := hown p hp
    set X := a.1 * (p.1 - qw.cx) + a.2 * (p.2 - qw.cy) with hX_def
    have h1 := le_abs_self X
    have h2 := neg_le_abs X
    change eps * a.1 * p.1 + eps * a.2 * p.2 ≤ eps * (a.1 * qw.cx + a.2 * qw.cy) + 1 / 2
    have e : eps * a.1 * p.1 + eps * a.2 * p.2 - eps * (a.1 * qw.cx + a.2 * qw.cy) = eps * X := by
      rw [hX_def]; ring
    rcases heps with h | h <;> subst h <;> linarith
  · intro p hp
    have hY := support_le qo a hp
    set Y := a.1 * (p.1 - qo.cx) + a.2 * (p.2 - qo.cy) with hY_def
    set Z := (qo.cx - qw.cx) * a.1 + (qo.cy - qw.cy) * a.2 with hZ_def
    have h1 := le_abs_self Y
    have h2 := neg_le_abs Y
    change eps * (a.1 * qw.cx + a.2 * qw.cy) + 1 / 2 ≤ eps * a.1 * p.1 + eps * a.2 * p.2
    have e : eps * a.1 * p.1 + eps * a.2 * p.2 - eps * (a.1 * qw.cx + a.2 * qw.cy) = eps * (Y + Z) := by
      rw [hY_def, hZ_def]; ring
    rcases heps with h | h <;> subst h <;> linarith

/-- The selection row `gsel qw qo k eps ≥ 0` of `sat_selection_thm` is a separating line: the owner's axis
`a = axk qw k`, signed by `eps`, at level `eps a·c_w + 1/2`. -/
theorem separates_of_gsel (qw qo : PSq) (k : Bool) (eps : ℝ) (heps : eps = 1 ∨ eps = -1)
    (hg : 0 ≤ gsel qw qo k eps) :
    Separates (eps * (axk qw k).1, eps * (axk qw k).2)
      (eps * ((axk qw k).1 * qw.cx + (axk qw k).2 * qw.cy) + 1 / 2) qw qo := by
  have hcs := cosT_sq_add_sinT_sq qw.t
  unfold gsel at hg
  refine separates_of_axis qw qo (axk qw k) ?_ eps heps ?_ ?_ (by linarith)
  · cases k <;> simp only [axk, Bool.false_eq_true, ↓reduceIte] <;> linear_combination hcs
  · intro p hp
    obtain ⟨hu, hv⟩ := (mem_set_iff_uv qw p).mp hp
    simp only [rdot, edir, perpV] at hu hv
    cases k <;> simp only [axk, Bool.false_eq_true, ↓reduceIte]
    · rcases abs_le.mp hu with ⟨h1, h2⟩
      exact abs_le.mpr ⟨by linarith, by linarith⟩
    · rcases abs_le.mp hv with ⟨h1, h2⟩
      exact abs_le.mpr ⟨by linarith, by linarith⟩
  · unfold wrel
    cases k <;> simp only [axk, Bool.false_eq_true, ↓reduceIte]
    · change |cosT qw.t * cosT qo.t + sinT qw.t * sinT qo.t| + |cosT qw.t * (-sinT qo.t) + sinT qw.t * cosT qo.t|
          ≤ |cosT qw.t * cosT qo.t + sinT qw.t * sinT qo.t| + |cosT qw.t * sinT qo.t - sinT qw.t * cosT qo.t|
      have e : |cosT qw.t * (-sinT qo.t) + sinT qw.t * cosT qo.t|
          = |cosT qw.t * sinT qo.t - sinT qw.t * cosT qo.t| := by
        rw [← abs_neg]
        congr 1
        ring
      exact le_of_eq (by rw [e])
    · change |-sinT qw.t * cosT qo.t + cosT qw.t * sinT qo.t| + |-sinT qw.t * (-sinT qo.t) + cosT qw.t * cosT qo.t|
          ≤ |cosT qw.t * cosT qo.t + sinT qw.t * sinT qo.t| + |cosT qw.t * sinT qo.t - sinT qw.t * cosT qo.t|
      have e1 : |-sinT qw.t * cosT qo.t + cosT qw.t * sinT qo.t|
          = |cosT qw.t * sinT qo.t - sinT qw.t * cosT qo.t| := by
        congr 1
        ring
      have e2 : |-sinT qw.t * (-sinT qo.t) + cosT qw.t * cosT qo.t|
          = |cosT qw.t * cosT qo.t + sinT qw.t * sinT qo.t| := by
        congr 1
        ring
      exact le_of_eq (by rw [e1, e2, add_comm (|cosT qw.t * sinT qo.t - sinT qw.t * cosT qo.t|)])

/-- **Lemma WEDGED-SEAL.**  A wedged corner meeter admits no second meeter of the open unit box: any interior-
disjoint unit square `g` of the quadrant meeting the box contradicts Lemma PUSH through its separating axis. -/
theorem wedged_seal (q g : PSq) (hq : q.t ∈ Icc (0 : ℝ) 1) (hg : g.t ∈ Icc (0 : ℝ) 1)
    (hqQ : InQuadrant q) (hgQ : InQuadrant g) (hqm : Meets q 1) (hgm : Meets g 1) (hw : Wedged q)
    (hd : Disjoint (interior g.set) (interior q.set)) : False := by
  rcases sat_selection_thm g q hd with ⟨k, eps, heps, hsel⟩ | ⟨k, eps, heps, hsel⟩
  · exact wedged_seal_of_separates q g hq hg hqQ hgQ hqm hgm hw (separates_of_gsel g q k eps heps hsel)
  · exact wedged_seal_of_separates q g hq hg hqQ hgQ hqm hgm hw
      (separates_of_gsel q g k eps heps hsel).symm

#print axioms wedged_seal_of_separates
#print axioms separates_of_gsel
#print axioms wedged_seal

end PackingCert.S11.OpenLemmas
