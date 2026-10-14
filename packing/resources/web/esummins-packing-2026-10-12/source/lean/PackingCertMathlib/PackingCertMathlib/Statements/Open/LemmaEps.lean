import PackingCertMathlib.Sideband
import Mathlib.Analysis.Convex.Topology
import Mathlib.Analysis.Convex.PathConnected

/-!
# Lemma EPS -- the wedges of a near-simple square's cell (A227)

`docs/proofs/lemma_eps.md`.  A unit square `F` (centre `z`, tilt `θ`, `t = tan(θ/2)`) sitting near the slot pose of
a cell `C` leaves uncovered only four thin WEDGES of `C`, one along each side, and any other square meeting `int C`
must enter through one of them.  The statements below are the geometric core, proved from the square's set
description `mem_set_iff_uv` (`|u| ≤ ½ ∧ |v| ≤ ½` in the centred coordinates `u = e·(p−z)`, `v = e⊥·(p−z)`):

* `not_mem_iff_four` -- a point is outside `F` iff one of the four centred coordinates exceeds `½` in absolute
  value: `C \ F` is the union of the four half-plane cuts `W = C ∩ {±u > ½}`, `C ∩ {±v > ½}` (Lemma EPS-1).
* `wedge_right_depth` -- the cut `{u > ½}` is `{x > z_x + (½ − (y − z_y) sin θ)/cos θ}` for `cos θ > 0`: the
  wedge along the right side, with its depth linear in `y` (Lemma EPS-2, the division form).
* `wedge_right_corner` -- the same in `t`: `(1 − x)(1 − t²) < t(1 − t − 2δ_y) − δ_x(1 − t²) − 2t(1 − y)` with
  `δ = z − (½, ½)`; at `y = 1` this is the corner depth `w_R = t(1 − t − 2δ_y)/(1 − t²) − δ_x`, and the depth
  vanishes at `y* = ½ + δ_y + t/2 + δ_x(1 − t²)/(2t)` (the PI's pinwheel for `δ = 0`: the UPPER half of the side).
* `coord_within_h` -- every point of a square of tilt `φ` is within `(|cos φ| + |sin φ|)/2 ≤ 1/√2` of its centre in
  each coordinate: the closed-form pose region of a meeter of a wedge (Lemma EPS-6).
* `gate` -- the topological GATE (Lemma EPS-5): a square whose interior meets a closed region `R` but is not
  contained in it has an interior point on `frontier R`; where every frontier point outside an EXIT set `E` is in
  the closure of the obstacles' interiors `O` (pin cores, the near-simple square's core, the container's
  exterior), that point lies in `E`.  This is what makes a wedge along a pin- or wall-backed side reachable only
  through its open END at the cell's corner (SNAP-DIAG's "point").

**Status (2026-09-15).**  All five are theorems (no axiom, no sorry).  Rule EPS's engine certificate is the
composition of these with A161's exact separating-axis miss test (`attempts/A227-lemma-eps/code/eps227.py`).
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- **Lemma EPS-1.**  A point is outside the square iff one of its two centred coordinates exceeds `½` in
absolute value -- `C \ F` is covered by the four half-plane cuts. -/
theorem not_mem_iff_four (q : PSq) (p : RP) :
    p ∉ q.set ↔
      1 / 2 < |rdot (p.1 - q.cx, p.2 - q.cy) (edir q)| ∨
      1 / 2 < |rdot (p.1 - q.cx, p.2 - q.cy) (perpV (edir q))| := by
  rw [mem_set_iff_uv, not_and_or, not_le, not_le]

theorem cosT_pos_of_lt_one {t : ℝ} (h0 : 0 ≤ t) (h1 : t < 1) : 0 < cosT t := by
  have h := one_add_sq_pos t
  exact div_pos (by nlinarith) h

/-- **Lemma EPS-2 (division form).**  The cut `u > ½` is the region to the RIGHT of the line
`x = z_x + (½ − (y − z_y) sin θ)/cos θ`: a wedge along the right side of the cell whose depth is linear in `y`. -/
theorem wedge_right_depth (q : PSq) (p : RP) (h0 : 0 ≤ q.t) (h1 : q.t < 1)
    (hu : 1 / 2 < rdot (p.1 - q.cx, p.2 - q.cy) (edir q)) :
    q.cx + (1 / 2 - (p.2 - q.cy) * sinT q.t) / cosT q.t < p.1 := by
  have hc := cosT_pos_of_lt_one h0 h1
  simp only [rdot, edir] at hu
  have : (1 / 2 - (p.2 - q.cy) * sinT q.t) / cosT q.t < p.1 - q.cx := by
    rw [div_lt_iff₀ hc]
    linarith
  linarith

/-- **Lemma EPS-2 (the `t` form).**  With `δ = z − (½, ½)`:
`(1 − x)(1 − t²) < t(1 − t − 2δ_y) − δ_x(1 − t²) − 2t(1 − y)`.  At `y = 1` the right-hand side over `1 − t²` is
the corner depth `w_R = t(1 − t − 2δ_y)/(1 − t²) − δ_x`; the depth is zero at `y* = ½ + δ_y + t/2 + δ_x(1 − t²)/(2t)`. -/
theorem wedge_right_corner (q : PSq) (p : RP) (h0 : 0 ≤ q.t) (h1 : q.t < 1)
    (hu : 1 / 2 < rdot (p.1 - q.cx, p.2 - q.cy) (edir q)) :
    (1 - p.1) * (1 - q.t ^ 2) <
      q.t * (1 - q.t - 2 * (q.cy - 1 / 2)) - (q.cx - 1 / 2) * (1 - q.t ^ 2) - 2 * q.t * (1 - p.2) := by
  have hpos := one_add_sq_pos q.t
  have hne : (1 + q.t ^ 2 : ℝ) ≠ 0 := hpos.ne'
  simp only [rdot, edir] at hu
  have hc : cosT q.t * (1 + q.t ^ 2) = 1 - q.t ^ 2 := by unfold cosT; field_simp
  have hs : sinT q.t * (1 + q.t ^ 2) = 2 * q.t := by unfold sinT; field_simp
  have h2 := mul_lt_mul_of_pos_right hu hpos
  have h3 : 1 / 2 * (1 + q.t ^ 2) <
      (p.1 - q.cx) * (1 - q.t ^ 2) + (p.2 - q.cy) * (2 * q.t) := by
    have e : ((p.1 - q.cx) * cosT q.t + (p.2 - q.cy) * sinT q.t) * (1 + q.t ^ 2)
        = (p.1 - q.cx) * (1 - q.t ^ 2) + (p.2 - q.cy) * (2 * q.t) := by
      rw [add_mul, mul_assoc, hc, mul_assoc, hs]
    linarith [e]
  nlinarith [h3]

/-- **Lemma EPS-6.**  Every point of a square of tilt `φ` lies within `(|cos φ| + |sin φ|)/2` of the centre in the
`x` coordinate (and, by the same proof with the roles of `e`, `e⊥` exchanged, in `y`).  So the centres of the
squares of tilt `φ` meeting a set `W` lie in `W` dilated by that half-width in `ℓ∞` -- at most `1/√2`. -/
theorem coord_within_h (q : PSq) {p : RP} (hp : p ∈ q.set) :
    |p.1 - q.cx| ≤ (|cosT q.t| + |sinT q.t|) / 2 := by
  obtain ⟨hu, hv⟩ := (mem_set_iff_uv q p).mp hp
  have hcs := cosT_sq_add_sinT_sq q.t
  have hdx : p.1 - q.cx =
      rdot (p.1 - q.cx, p.2 - q.cy) (edir q) * cosT q.t
        - rdot (p.1 - q.cx, p.2 - q.cy) (perpV (edir q)) * sinT q.t := by
    simp only [rdot, edir, perpV]
    linear_combination (-(p.1 - q.cx)) * hcs
  have h1 : |rdot (p.1 - q.cx, p.2 - q.cy) (edir q) * cosT q.t| ≤ 1 / 2 * |cosT q.t| := by
    rw [abs_mul]; exact mul_le_mul_of_nonneg_right hu (abs_nonneg _)
  have h2 : |rdot (p.1 - q.cx, p.2 - q.cy) (perpV (edir q)) * sinT q.t| ≤ 1 / 2 * |sinT q.t| := by
    rw [abs_mul]; exact mul_le_mul_of_nonneg_right hv (abs_nonneg _)
  rw [hdx, abs_le]
  constructor
  · linarith [le_abs_self (rdot (p.1 - q.cx, p.2 - q.cy) (edir q) * cosT q.t),
              neg_abs_le (rdot (p.1 - q.cx, p.2 - q.cy) (edir q) * cosT q.t),
              le_abs_self (rdot (p.1 - q.cx, p.2 - q.cy) (perpV (edir q)) * sinT q.t),
              neg_abs_le (rdot (p.1 - q.cx, p.2 - q.cy) (perpV (edir q)) * sinT q.t)]
  · linarith [le_abs_self (rdot (p.1 - q.cx, p.2 - q.cy) (edir q) * cosT q.t),
              neg_abs_le (rdot (p.1 - q.cx, p.2 - q.cy) (edir q) * cosT q.t),
              le_abs_self (rdot (p.1 - q.cx, p.2 - q.cy) (perpV (edir q)) * sinT q.t),
              neg_abs_le (rdot (p.1 - q.cx, p.2 - q.cy) (perpV (edir q)) * sinT q.t)]

/-- **Lemma EPS-5 (GATE).**  `M` a unit square, `R` a closed region met by `int M` in a point of `int R` and not
containing `int M`; `O` the union of the obstacles' interiors (`int M ∩ O = ∅`); every point of `frontier R`
outside the exit set `E` lies in `closure O`.  Then `int M` contains a point of `E`.
Proof: `int M` is convex, so the segment from `a ∈ int M ∩ int R` to `b ∈ int M \ R` lies in `int M`; it is
connected, so it crosses `frontier R` at some `q ∈ int M`; `q` cannot be in `closure O` because `int M` is an
open neighbourhood of `q` disjoint from `O`; so `q ∈ E`. -/
theorem gate (M : PSq) {R O E : Set RP} (hR : IsClosed R)
    (hdisj : Disjoint (interior M.set) O)
    (hblock : ∀ q ∈ frontier R, q ∉ E → q ∈ closure O)
    (ha : ∃ a ∈ interior M.set, a ∈ interior R) (hb : ∃ b ∈ interior M.set, b ∉ R) :
    ∃ q ∈ interior M.set, q ∈ E := by
  obtain ⟨a, haM, haR⟩ := ha
  obtain ⟨b, hbM, hbR⟩ := hb
  have hconv : Convex ℝ (interior M.set) := (psq_convex M).interior
  have hseg : segment ℝ a b ⊆ interior M.set := hconv.segment_subset haM hbM
  have hpre : IsPreconnected (segment ℝ a b) := (convex_segment (𝕜 := ℝ) a b).isPreconnected
  have key : ∃ q ∈ segment ℝ a b, q ∈ frontier R := by
    by_contra hno
    push_neg at hno
    have hsub : segment ℝ a b ⊆ R ∪ closure Rᶜ := by
      intro x _
      by_cases hx : x ∈ R
      · exact Or.inl hx
      · exact Or.inr (subset_closure hx)
    have hemp : segment ℝ a b ∩ (R ∩ closure Rᶜ) = ∅ := by
      rw [eq_empty_iff_forall_notMem]
      rintro x ⟨hxs, hxR, hxc⟩
      apply hno x hxs
      rw [frontier_eq_closure_inter_closure, hR.closure_eq]
      exact ⟨hxR, hxc⟩
    rcases (isPreconnected_iff_subset_of_disjoint_closed.mp hpre) R (closure Rᶜ) hR isClosed_closure
        hsub hemp with h | h
    · exact hbR (h (right_mem_segment (𝕜 := ℝ) a b))
    · have hb' := h (left_mem_segment (𝕜 := ℝ) a b)
      rw [closure_compl] at hb'
      exact hb' haR
  obtain ⟨q, hqs, hqf⟩ := key
  refine ⟨q, hseg hqs, ?_⟩
  by_contra hqE
  have hcl := hblock q hqf hqE
  rw [mem_closure_iff_nhds] at hcl
  obtain ⟨o, hoM, hoO⟩ := hcl _ (isOpen_interior.mem_nhds (hseg hqs))
  exact Set.disjoint_left.mp hdisj hoM hoO

#print axioms not_mem_iff_four
#print axioms wedge_right_depth
#print axioms wedge_right_corner
#print axioms coord_within_h
#print axioms gate

end PackingCert.S11.OpenLemmas
