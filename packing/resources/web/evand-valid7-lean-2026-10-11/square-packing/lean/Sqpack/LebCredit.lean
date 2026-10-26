import Sqpack.CovMP
import Sqpack.LemmaEPoly

/-!
# A Lebesgue credit: strips inside every admissible square

For a box of centres `[x0/Q, x1/Q] × [y0/Q, y1/Q]` and angles `θ = 2 arctan u`, `u ∈ [U0/R, U1/R]`,
a list of horizontal strips `[xa/G, xb/G] × [yb/G, (yb + h)/G]`, each inside a Lebesgue rectangle `e`
of the cover and inside the closed unit square of every admissible pose, gives the credit
`amt ≤ w_e · Σ area` towards the rectangle's mass (`cred_sound`).

A point `p` is in the square of centre `c` iff both rotated coordinates are in `[-1/2, 1/2]`; times
`1 + u²` each bound is a polynomial of degree 2 in `u`, checked by Bernstein (`ptOk`) with `c` at
the box corners.  The coordinates are monotone in `c` and in `p` (`cos θ, sin θ ≥ 0`), so the corner
checks bound them on the whole box and the whole strip.
-/

open MeasureTheory

namespace SquarePacking

namespace LebCredit

open BernZ LemmaEPoly ZMTreeM

/-- `(xa, xb, yb)`: the strip `[xa/G, xb/G] × [yb/G, (yb + h)/G]`. -/
abbrev Strip := ℕ × ℕ × ℕ

/-- A credit: the rectangle, the denominator `G`, the strip height `h`, the amount (units of the
rectangle weight's scale, like `W`) and the strips (`yb` increasing by at least `h`). -/
structure Cred where
  e : RectE
  G : ℕ
  h : ℕ
  amt : ℕ
  strips : List Strip

/-! ## 1.  A point in every square -/

/-- The bounds of the point `(a/G, b/G)` against the centre `(x/Q, y/Q)`, times `2GQ(1 + u²)`:
`A cos + B sin ≤ 1/2`, `≥ -1/2`, `-A sin + B cos ≤ 1/2`, `≥ -1/2` (`A = a/G − x/Q`, `B = b/G − y/Q`). -/
def q0 (H dx dy : ℤ) : Poly := [H - 2 * dx, -4 * dy, H + 2 * dx]
def q1 (H dx dy : ℤ) : Poly := [H + 2 * dx, 4 * dy, H - 2 * dx]
def q2 (H dx dy : ℤ) : Poly := [H - 2 * dy, 4 * dx, H + 2 * dy]
def q3 (H dx dy : ℤ) : Poly := [H + 2 * dy, -4 * dx, H - 2 * dy]

/-- Bound `k` of the point `(a/G, b/G)` against the centre `(x/Q, y/Q)`. -/
def qk (G Q a b x y k : ℕ) : Poly :=
  let dx : ℤ := (a : ℤ) * Q - (x : ℤ) * G
  let dy : ℤ := (b : ℤ) * Q - (y : ℤ) * G
  let H : ℤ := (G : ℤ) * Q
  match k with
  | 0 => q0 H dx dy
  | 1 => q1 H dx dy
  | 2 => q2 H dx dy
  | _ => q3 H dx dy

def bOk (G Q U0 U1 R a b x y k : ℕ) : Bool := check (qk G Q a b x y k) 2 U0 U1 R

/-- The rotated coordinates, with `co = cos θ`, `s = sin θ`. -/
def E1 (co s : ℝ) (p c : ℝ × ℝ) : ℝ := (p.1 - c.1) * co + (p.2 - c.2) * s
def E2 (co s : ℝ) (p c : ℝ × ℝ) : ℝ := -(p.1 - c.1) * s + (p.2 - c.2) * co

section point

variable {G Q R U0 U1 : ℕ} {u : ℝ}

/-- **The four bounds**: `E1 ≤ 1/2`, `E1 ≥ -1/2`, `E2 ≤ 1/2`, `E2 ≥ -1/2` at `u` from the checks. -/
lemma bnd_sound (hG : 0 < G) (hQ : 0 < Q) (hR : 0 < R) (a b x y : ℕ)
    (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R) :
    let co := (1 - u ^ 2) / (1 + u ^ 2)
    let t := 2 * u / (1 + u ^ 2)
    let p : ℝ × ℝ := ((a : ℝ) / G, (b : ℝ) / G)
    let c : ℝ × ℝ := ((x : ℝ) / Q, (y : ℝ) / Q)
    (bOk G Q U0 U1 R a b x y 0 = true → E1 co t p c ≤ 1 / 2) ∧
      (bOk G Q U0 U1 R a b x y 1 = true → -(1 / 2) ≤ E1 co t p c) ∧
      (bOk G Q U0 U1 R a b x y 2 = true → E2 co t p c ≤ 1 / 2) ∧
      (bOk G Q U0 U1 R a b x y 3 = true → -(1 / 2) ≤ E2 co t p c) := by
  intro co t p c
  have hGr : (0 : ℝ) < G := by exact_mod_cast hG
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  set A : ℝ := (a : ℝ) / G - (x : ℝ) / Q with hA
  set B : ℝ := (b : ℝ) / G - (y : ℝ) / Q with hB
  have dxA : (a : ℝ) * Q - x * G = G * Q * A := by rw [hA]; field_simp
  have dyB : (b : ℝ) * Q - y * G = G * Q * B := by rw [hB]; field_simp
  have hGQ : (0 : ℝ) < G * Q := by positivity
  have key : ∀ T : ℝ, 0 ≤ G * Q * T → 0 ≤ T := fun T h => (mul_nonneg_iff_of_pos_left hGQ).mp h
  have f1 : E1 co t p c = (A * (1 - u ^ 2) + B * (2 * u)) / (1 + u ^ 2) := by
    simp only [E1, co, t, p, c]; rw [hA, hB]; field_simp
  have f2 : E2 co t p c = (-A * (2 * u) + B * (1 - u ^ 2)) / (1 + u ^ 2) := by
    simp only [E2, co, t, p, c]; rw [hA, hB]; field_simp
  refine ⟨fun h => ?_, fun h => ?_, fun h => ?_, fun h => ?_⟩ <;>
    have e := nonneg_of_check h hR hb0 hb1 <;>
    simp only [qk, q0, q1, q2, q3, eval_cons, eval_nil, mul_zero, add_zero] at e <;>
    push_cast at e <;> rw [dxA, dyB] at e
  · have k := key ((1 + u ^ 2) - 2 * A * (1 - u ^ 2) - 4 * B * u) (by linarith [e])
    rw [f1, div_le_iff₀ hN]; linarith
  · have k := key ((1 + u ^ 2) + 2 * A * (1 - u ^ 2) + 4 * B * u) (by linarith [e])
    rw [f1, le_div_iff₀ hN]; linarith
  · have k := key ((1 + u ^ 2) - 2 * B * (1 - u ^ 2) + 4 * A * u) (by linarith [e])
    rw [f2, div_le_iff₀ hN]; linarith
  · have k := key ((1 + u ^ 2) + 2 * B * (1 - u ^ 2) - 4 * A * u) (by linarith [e])
    rw [f2, le_div_iff₀ hN]; linarith

end point

/-! ## 2.  Strips -/

/-- The strip `[xa/G, xb/G] × [yb/G, (yb + h)/G)` (half-open in `y`, so consecutive strips are
disjoint). -/
def stripSet (G h : ℕ) (s : Strip) : Set (ℝ × ℝ) :=
  Set.Icc ((s.1 : ℝ) / G) ((s.2.1 : ℝ) / G) ×ˢ Set.Ico ((s.2.2 : ℝ) / G) (((s.2.2 + h : ℕ) : ℝ) / G)

/-- A strip inside the rectangle `e` (over `D`) and inside every admissible square: each rotated
coordinate is extreme at one corner of the strip and one corner of the box, so four checks. -/
def stripOk (D G Q x0 x1 y0 y1 U0 U1 R h : ℕ) (e : RectE) (s : Strip) : Bool :=
  Nat.ble s.1 s.2.1 && Nat.ble (e.1 * G) (s.1 * D) && Nat.ble (s.2.1 * D) (e.2.2.1 * G) &&
    Nat.ble (e.2.1 * G) (s.2.2 * D) && Nat.ble ((s.2.2 + h) * D) (e.2.2.2.1 * G) &&
    bOk G Q U0 U1 R s.2.1 (s.2.2 + h) x0 y0 0 && bOk G Q U0 U1 R s.1 s.2.2 x1 y1 1 &&
    bOk G Q U0 U1 R s.1 (s.2.2 + h) x1 y0 2 && bOk G Q U0 U1 R s.2.1 s.2.2 x0 y1 3

section strip

variable {D G Q R U0 U1 x0 x1 y0 y1 h : ℕ} {e : RectE} {s : Strip}

lemma strip_sub_rect (hD : 0 < D) (hG : 0 < G) (hs : stripOk D G Q x0 x1 y0 y1 U0 U1 R h e s = true) :
    stripSet G h s ⊆ rectSet D e := by
  simp only [stripOk, Bool.and_eq_true, Nat.ble_eq] at hs
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨_, r1⟩, r2⟩, r3⟩, r4⟩, _⟩, _⟩, _⟩, _⟩ := hs
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hGr : (0 : ℝ) < G := by exact_mod_cast hG
  have q1 : (e.1 : ℝ) / D ≤ (s.1 : ℝ) / G := by
    rw [div_le_div_iff₀ hDr hGr]; exact_mod_cast r1
  have q2 : (s.2.1 : ℝ) / G ≤ (e.2.2.1 : ℝ) / D := by
    rw [div_le_div_iff₀ hGr hDr]; exact_mod_cast r2
  have q3 : (e.2.1 : ℝ) / D ≤ (s.2.2 : ℝ) / G := by
    rw [div_le_div_iff₀ hDr hGr]; exact_mod_cast r3
  have q4 : (((s.2.2 + h : ℕ) : ℝ)) / G ≤ (e.2.2.2.1 : ℝ) / D := by
    rw [div_le_div_iff₀ hGr hDr]; exact_mod_cast r4
  rintro p ⟨⟨a1, a2⟩, ⟨b1, b2⟩⟩
  exact ⟨⟨q1.trans a1, a2.trans q2⟩, ⟨q3.trans b1, b2.le.trans q4⟩⟩

lemma strip_sub_sq (hG : 0 < G) (hQ : 0 < Q) (hR : 0 < R)
    (hs : stripOk D G Q x0 x1 y0 y1 U0 U1 R h e s = true) {u : ℝ} (hu0 : 0 < u) (hu1 : u < 1)
    (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R) {c : ℝ × ℝ}
    (hx0 : (x0 : ℝ) / Q ≤ c.1) (hx1 : c.1 ≤ (x1 : ℝ) / Q) (hy0 : (y0 : ℝ) / Q ≤ c.2)
    (hy1 : c.2 ≤ (y1 : ℝ) / Q) :
    stripSet G h s ⊆ sq c (2 * Real.arctan u) 1 := by
  simp only [stripOk, Bool.and_eq_true, Nat.ble_eq] at hs
  obtain ⟨⟨⟨⟨_, p0⟩, p1⟩, p2⟩, p3⟩ := hs
  have m1 := (bnd_sound hG hQ hR _ _ _ _ hb0 hb1).1 p0
  have m2 := (bnd_sound hG hQ hR _ _ _ _ hb0 hb1).2.1 p1
  have m3 := (bnd_sound hG hQ hR _ _ _ _ hb0 hb1).2.2.1 p2
  have m4 := (bnd_sound hG hQ hR _ _ _ _ hb0 hb1).2.2.2 p3
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have hco : 0 ≤ (1 - u ^ 2) / (1 + u ^ 2) := div_nonneg (by nlinarith) hN.le
  have hsn : 0 ≤ 2 * u / (1 + u ^ 2) := div_nonneg (by linarith) hN.le
  simp only [E1, E2] at m1 m2 m3 m4
  rintro p ⟨⟨a1, a2⟩, ⟨b1, b2⟩⟩
  have b2' := b2.le
  simp only [sq, coord, (trig u).1, (trig u).2, abs_le]
  set co := (1 - u ^ 2) / (1 + u ^ 2)
  set t := 2 * u / (1 + u ^ 2)
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · linarith [mul_le_mul_of_nonneg_right a1 hco, mul_le_mul_of_nonneg_right b1 hsn,
      mul_le_mul_of_nonneg_right hx1 hco, mul_le_mul_of_nonneg_right hy1 hsn]
  · linarith [mul_le_mul_of_nonneg_right a2 hco, mul_le_mul_of_nonneg_right b2' hsn,
      mul_le_mul_of_nonneg_right hx0 hco, mul_le_mul_of_nonneg_right hy0 hsn]
  · linarith [mul_le_mul_of_nonneg_right a2 hsn, mul_le_mul_of_nonneg_right b1 hco,
      mul_le_mul_of_nonneg_right hx0 hsn, mul_le_mul_of_nonneg_right hy1 hco]
  · linarith [mul_le_mul_of_nonneg_right a1 hsn, mul_le_mul_of_nonneg_right b2' hco,
      mul_le_mul_of_nonneg_right hx1 hsn, mul_le_mul_of_nonneg_right hy0 hco]

end strip

/-! ## 3.  Areas -/

section area

variable {G h : ℕ}

lemma measurableSet_stripSet (s : Strip) : MeasurableSet (stripSet G h s) :=
  measurableSet_Icc.prod measurableSet_Ico

lemma volume_stripSet (hG : 0 < G) (s : Strip) (hs : s.1 ≤ s.2.1) :
    volume (stripSet G h s) = ENNReal.ofReal (((s.2.1 - s.1) * h : ℕ) / ((G : ℝ) * G)) := by
  have hGr : (0 : ℝ) < G := by exact_mod_cast hG
  rw [stripSet, Measure.volume_eq_prod, Measure.prod_prod, Real.volume_Icc, Real.volume_Ico,
    ← ENNReal.ofReal_mul (by rw [sub_nonneg]; exact div_le_div_of_nonneg_right (by exact_mod_cast hs) hGr.le)]
  congr 1
  push_cast [Nat.cast_sub hs]
  field_simp
  ring

lemma disjoint_stripSet {s t : Strip} (hst : s.2.2 + h ≤ t.2.2) :
    Disjoint (stripSet G h s) (stripSet G h t) := by
  rw [Set.disjoint_left]
  rintro p ⟨_, _, b2⟩ ⟨_, c1, _⟩
  have : (((s.2.2 + h : ℕ) : ℝ)) / G ≤ (t.2.2 : ℝ) / G :=
    div_le_div_of_nonneg_right (by exact_mod_cast hst) (Nat.cast_nonneg _)
  linarith

/-- Strips of a list sorted by `yb` (gaps at least `h`) have the sum of their areas. -/
lemma volume_union_strips (hG : 0 < G) :
    ∀ l : List Strip, l.Pairwise (fun s t => s.2.2 + h ≤ t.2.2) → (∀ s ∈ l, s.1 ≤ s.2.1) →
      volume (⋃ s ∈ l, stripSet G h s) =
        ENNReal.ofReal ((l.map fun s => (((s.2.1 - s.1) * h : ℕ) : ℝ) / ((G : ℝ) * G)).sum)
  | [], _, _ => by simp
  | a :: l, hp, hs => by
    rw [List.pairwise_cons] at hp
    have e : (⋃ s ∈ a :: l, stripSet G h s) = stripSet G h a ∪ ⋃ s ∈ l, stripSet G h s := by
      ext p; simp
    rw [e, measure_union (Set.disjoint_iUnion₂_right.mpr fun t ht => disjoint_stripSet (hp.1 t ht))
      (MeasurableSet.biUnion (Set.to_countable _) fun t _ => measurableSet_stripSet t),
      volume_stripSet hG a (hs a List.mem_cons_self),
      volume_union_strips hG l hp.2 fun t ht => hs t (List.mem_cons_of_mem _ ht), List.map_cons,
      List.sum_cons, ENNReal.ofReal_add (by positivity)
        (List.sum_nonneg fun x hx => by
          obtain ⟨t, _, rfl⟩ := List.mem_map.mp hx; positivity)]

end area

/-! ## 4.  The credit -/

/-- Consecutive strips are at least `h` apart in `yb`. -/
def sortedOk (h : ℕ) : List Strip → Bool
  | [] => true
  | [_] => true
  | s :: t :: l => Nat.ble (s.2.2 + h) t.2.2 && sortedOk h (t :: l)

lemma pairwise_of_sortedOk (h : ℕ) :
    ∀ l : List Strip, sortedOk h l = true → l.Pairwise fun s t => s.2.2 + h ≤ t.2.2
  | [], _ => List.Pairwise.nil
  | [_], _ => List.pairwise_singleton _ _
  | s :: t :: l, hs => by
    simp only [sortedOk, Bool.and_eq_true, Nat.ble_eq] at hs
    have ih := pairwise_of_sortedOk h (t :: l) hs.2
    rw [List.pairwise_cons] at ih ⊢
    refine ⟨fun w hw => ?_, List.pairwise_cons.mpr ih⟩
    rcases List.mem_cons.mp hw with rfl | hw
    · exact hs.1
    · have := ih.1 w hw; omega

/-- **The test of a credit**: the rectangle is in the cover, the strips are sorted with gaps `h`, each
is inside the rectangle and every admissible square, and `amt ≤ w_e · Σ area`. -/
def credOk (D Q x0 x1 y0 y1 U0 U1 R : ℕ) (rects : List RectE) (cr : Cred) : Bool :=
  rects.contains cr.e && Nat.blt 0 cr.G &&
    sortedOk cr.h cr.strips &&
    cr.strips.all (stripOk D cr.G Q x0 x1 y0 y1 U0 U1 R cr.h cr.e) &&
    Nat.ble (cr.amt * (cr.G * cr.G)) (cr.e.2.2.2.2 * (cr.strips.map fun s => (s.2.1 - s.1) * cr.h).sum)

lemma sum_map_div (G : ℝ) : ∀ (l : List Strip) (f : Strip → ℕ),
    (l.map fun s => (f s : ℝ) / G).sum = (((l.map f).sum : ℕ) : ℝ) / G
  | [], _ => by simp
  | a :: l, f => by
    simp only [List.map_cons, List.sum_cons, Nat.cast_add, sum_map_div G l f, add_div]

/-- **The credit is at most the rectangle's mass** in every admissible square. -/
theorem cred_sound {D Q x0 x1 y0 y1 U0 U1 R : ℕ} {rects : List RectE} {cr : Cred} (hD : 0 < D)
    (hQ : 0 < Q) (hR : 0 < R) (h : credOk D Q x0 x1 y0 y1 U0 U1 R rects cr = true) {u : ℝ}
    (hu0 : 0 < u) (hu1 : u < 1) (hb0 : (U0 : ℝ) / R ≤ u) (hb1 : u ≤ (U1 : ℝ) / R) {c : ℝ × ℝ}
    (hx0 : (x0 : ℝ) / Q ≤ c.1) (hx1 : c.1 ≤ (x1 : ℝ) / Q) (hy0 : (y0 : ℝ) / Q ≤ c.2)
    (hy1 : c.2 ≤ (y1 : ℝ) / Q) :
    (cr.amt : ℝ) ≤ ZMTreeM.rectMass D rects (sq c (2 * Real.arctan u) 1) := by
  simp only [credOk, Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq, List.all_eq_true,
    List.contains_iff_mem] at h
  obtain ⟨⟨⟨⟨he, hG⟩, hch⟩, hst⟩, hamt⟩ := h
  set Qs := sq c (2 * Real.arctan u) 1
  have hpw := pairwise_of_sortedOk cr.h cr.strips hch
  have hle : ∀ s ∈ cr.strips, s.1 ≤ s.2.1 := fun s hs => by
    have := hst s hs; simp only [stripOk, Bool.and_eq_true, Nat.ble_eq] at this; exact this.1.1.1.1.1.1.1.1
  -- the strips lie in the square and in the rectangle
  have hsub : (⋃ s ∈ cr.strips, stripSet cr.G cr.h s) ⊆ Qs ∩ rectSet D cr.e :=
    Set.iUnion₂_subset fun s hs => Set.subset_inter
      (strip_sub_sq hG hQ hR (hst s hs) hu0 hu1 hb0 hb1 hx0 hx1 hy0 hy1)
      (strip_sub_rect hD hG (hst s hs))
  have hfin : volume (Qs ∩ rectSet D cr.e) ≠ ⊤ := by
    refine ne_top_of_le_ne_top ?_ (measure_mono Set.inter_subset_right)
    rw [rectSet, Measure.volume_eq_prod, Measure.prod_prod, Real.volume_Icc, Real.volume_Icc]
    exact ENNReal.mul_ne_top ENNReal.ofReal_ne_top ENNReal.ofReal_ne_top
  have hvol : ENNReal.ofReal ((cr.strips.map fun s => (((s.2.1 - s.1) * cr.h : ℕ) : ℝ) /
      ((cr.G : ℝ) * cr.G)).sum) ≤ volume (Qs ∩ rectSet D cr.e) := by
    rw [← volume_union_strips hG cr.strips hpw hle]; exact measure_mono hsub
  rw [ENNReal.ofReal_le_iff_le_toReal hfin, sum_map_div] at hvol
  -- the credit
  have hGr : (0 : ℝ) < cr.G := by exact_mod_cast hG
  have hamt' : (cr.amt : ℝ) ≤ cr.e.2.2.2.2 *
      ((((cr.strips.map fun s => (s.2.1 - s.1) * cr.h).sum : ℕ) : ℝ) / ((cr.G : ℝ) * cr.G)) := by
    rw [mul_div_assoc', le_div_iff₀ (by positivity)]
    exact_mod_cast hamt
  have hone : (cr.e.2.2.2.2 : ℝ) * (volume (Qs ∩ rectSet D cr.e)).toReal ≤
      ZMTreeM.rectMass D rects Qs := by
    unfold ZMTreeM.rectMass
    exact Finset.single_le_sum (f := fun e : RectE => (e.2.2.2.2 : ℝ) * (volume (Qs ∩ rectSet D e)).toReal)
      (fun _ _ => mul_nonneg (Nat.cast_nonneg _) ENNReal.toReal_nonneg) (List.mem_toFinset.mpr he)
  calc (cr.amt : ℝ) ≤ _ := hamt'
    _ ≤ (cr.e.2.2.2.2 : ℝ) * (volume (Qs ∩ rectSet D cr.e)).toReal :=
        mul_le_mul_of_nonneg_left hvol (Nat.cast_nonneg _)
    _ ≤ _ := hone

end LebCredit

end SquarePacking
