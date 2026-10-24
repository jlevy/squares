import Sqlean.Rect
import Sqlean.CheckCore

/-!
# Soundness of the integer certificate checker

`check_sound`: if `unitOK`, `boxOK`, `sortedX` and `headsOK` accept a list `L` of integer squares
(`Sqlean/CheckCore.lean`), then the squares with centres `(X / D, Y / D)` and rotations
`(C / N, S / N)` form a packing of `L.length` unit squares in `[0, Wn / Sd] × [0, Hn / Sd]`.

`headsOK_chunks` glues kernel checks of consecutive chunks of rows.
-/

open Set

namespace UnitSquarePacking.Cert

/-! ## Real values of an integer square -/

/-- Centre `x`. -/
noncomputable def xr (D : ℤ) (q : Sq) : ℝ := (q.X : ℝ) / D
noncomputable def yr (D : ℤ) (q : Sq) : ℝ := (q.Y : ℝ) / D
noncomputable def cr (q : Sq) : ℝ := (q.C : ℝ) / q.N
noncomputable def sr (q : Sq) : ℝ := (q.S : ℝ) / q.N

lemma unitOK_spec {q : Sq} (h : unitOK q = true) :
    cr q ^ 2 + sr q ^ 2 = 1 ∧ (0 : ℝ) < q.N := by
  simp only [unitOK, Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h
  obtain ⟨h1, h2⟩ := h
  have hN : (0 : ℝ) < q.N := by exact_mod_cast h2
  refine ⟨?_, hN⟩
  have h1' : (q.C : ℝ) * q.C + q.S * q.S = q.N * q.N := by exact_mod_cast h1
  simp only [cr, sr]
  field_simp
  linear_combination h1'

/-- `a = ±1/2` as `ea / 2` with `ea = ±1`. -/
lemma half_cases {a : ℝ} (h : Half a) : ∃ e : ℤ, (e = 1 ∨ e = -1) ∧ a = (e : ℝ) / 2 := by
  rcases h with rfl | rfl
  · exact ⟨1, Or.inl rfl, by norm_num⟩
  · exact ⟨-1, Or.inr rfl, by norm_num⟩

lemma cornerOK_spec {D Wn Hn Sd : ℤ} {q : Sq} {ea eb : ℤ} (hD : 0 < D) (hN : 0 < q.N) (hSd : 0 < Sd)
    (h : cornerOK D Wn Hn Sd q ea eb = true) :
    0 ≤ xr D q + cr q * (ea / 2) - sr q * (eb / 2) ∧
      xr D q + cr q * (ea / 2) - sr q * (eb / 2) ≤ (Wn : ℝ) / Sd ∧
      0 ≤ yr D q + sr q * (ea / 2) + cr q * (eb / 2) ∧
      yr D q + sr q * (ea / 2) + cr q * (eb / 2) ≤ (Hn : ℝ) / Sd := by
  simp only [cornerOK, Bool.and_eq_true, decide_eq_true_eq] at h
  obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := h
  have hD' : (0 : ℝ) < D := by exact_mod_cast hD
  have hN' : (0 : ℝ) < q.N := by exact_mod_cast hN
  have hS' : (0 : ℝ) < Sd := by exact_mod_cast hSd
  have hM : (0 : ℝ) < 2 * q.N * D := by positivity
  have ex : xr D q + cr q * (ea / 2) - sr q * (eb / 2) =
      ((2 * q.N * q.X + D * (ea * q.C - eb * q.S) : ℤ) : ℝ) / (2 * q.N * D) := by
    simp only [xr, cr, sr]; push_cast; field_simp; ring
  have ey : yr D q + sr q * (ea / 2) + cr q * (eb / 2) =
      ((2 * q.N * q.Y + D * (ea * q.S + eb * q.C) : ℤ) : ℝ) / (2 * q.N * D) := by
    simp only [yr, cr, sr]; push_cast; field_simp; ring
  rw [ex, ey]
  have h1' : (0 : ℝ) ≤ ((2 * q.N * q.X + D * (ea * q.C - eb * q.S) : ℤ) : ℝ) := by exact_mod_cast h1
  have h3' : (0 : ℝ) ≤ ((2 * q.N * q.Y + D * (ea * q.S + eb * q.C) : ℤ) : ℝ) := by exact_mod_cast h3
  have h2' : ((2 * q.N * q.X + D * (ea * q.C - eb * q.S) : ℤ) : ℝ) * Sd ≤ (2 * q.N * D) * Wn := by
    exact_mod_cast h2
  have h4' : ((2 * q.N * q.Y + D * (ea * q.S + eb * q.C) : ℤ) : ℝ) * Sd ≤ (2 * q.N * D) * Hn := by
    exact_mod_cast h4
  refine ⟨div_nonneg h1' hM.le, ?_, div_nonneg h3' hM.le, ?_⟩
  · rw [div_le_div_iff₀ hM hS']; linarith
  · rw [div_le_div_iff₀ hM hS']; linarith

lemma boxOK_spec {D Wn Hn Sd : ℤ} {q : Sq} (hD : 0 < D) (hN : 0 < q.N) (hSd : 0 < Sd)
    (h : boxOK D Wn Hn Sd q = true) :
    InBoxR ((Wn : ℝ) / Sd) ((Hn : ℝ) / Sd) (xr D q) (yr D q) (cr q) (sr q) := by
  simp only [boxOK, Bool.and_eq_true] at h
  obtain ⟨⟨⟨hpp, hpm⟩, hmp⟩, hmm⟩ := h
  intro a b ha hb
  obtain ⟨ea, hea, rfl⟩ := half_cases ha
  obtain ⟨eb, heb, rfl⟩ := half_cases hb
  rcases hea with rfl | rfl <;> rcases heb with rfl | rfl
  · exact cornerOK_spec hD hN hSd hpp
  · exact cornerOK_spec hD hN hSd hpm
  · exact cornerOK_spec hD hN hSd hmp
  · exact cornerOK_spec hD hN hSd hmm

/-! ## Separating sides -/

lemma nrm_eq (q : Sq) (k : Fin 4) :
    nrm (cr q) (sr q) k = ((nA q.C q.S k : ℝ) / q.N, (nB q.C q.S k : ℝ) / q.N) := by
  fin_cases k <;> simp [nrm, nA, nB, cr, sr, neg_div]

lemma neg_abs_le_mul {e u : ℤ} (he : e = 1 ∨ e = -1) : -(u.natAbs : ℤ) ≤ e * u := by
  rw [Int.natCast_natAbs]
  rcases he with rfl | rfl
  · simpa using neg_abs_le u
  · simpa using le_abs_self u

lemma sepOK_spec {D : ℤ} {i j : Sq} {k : Fin 4} (hD : 0 < D) (hNi : 0 < i.N) (hNj : 0 < j.N)
    (h : sepOK D i j k = true) :
    SepSide (xr D i) (yr D i) (cr i) (sr i) (xr D j) (yr D j) (cr j) (sr j) k := by
  simp only [sepOK, decide_eq_true_eq] at h
  intro a b ha hb
  obtain ⟨ea, hea, rfl⟩ := half_cases ha
  obtain ⟨eb, heb, rfl⟩ := half_cases hb
  rw [nrm_eq]
  set A := nA i.C i.S k
  set B := nB i.C i.S k
  set u := A * j.C + B * j.S
  set v := B * j.C - A * j.S
  set E : ℤ := 2 * j.N * (A * (j.X - i.X) + B * (j.Y - i.Y)) + D * (ea * u + eb * v)
  have hE : i.N * j.N * D ≤ E := by
    have h1 := neg_abs_le_mul (u := u) hea
    have h2 := neg_abs_le_mul (u := v) heb
    have hD0 := hD.le
    simp only [E]
    nlinarith
  have hD' : (0 : ℝ) < D := by exact_mod_cast hD
  have hNi' : (0 : ℝ) < i.N := by exact_mod_cast hNi
  have hNj' : (0 : ℝ) < j.N := by exact_mod_cast hNj
  have hM : (0 : ℝ) < 2 * i.N * j.N * D := by positivity
  have ee : (A : ℝ) / i.N * (xr D j + cr j * (ea / 2) - sr j * (eb / 2) - xr D i) +
      (B : ℝ) / i.N * (yr D j + sr j * (ea / 2) + cr j * (eb / 2) - yr D i) =
      (E : ℝ) / (2 * i.N * j.N * D) := by
    simp only [E, u, v, xr, yr, cr, sr]; push_cast; field_simp; ring
  simp only
  rw [ee, le_div_iff₀ hM]
  have : ((i.N * j.N * D : ℤ) : ℝ) ≤ (E : ℝ) := by exact_mod_cast hE
  push_cast at this
  linarith

lemma sepAny_spec {D : ℤ} {i j : Sq} (hD : 0 < D) (hNi : 0 < i.N) (hNj : 0 < j.N)
    (h : sepAny D i j = true) :
    ∃ k, SepSide (xr D i) (yr D i) (cr i) (sr i) (xr D j) (yr D j) (cr j) (sr j) k := by
  simp only [sepAny, Bool.or_eq_true] at h
  rcases h with ((h | h) | h) | h
  · exact ⟨0, sepOK_spec (k := 0) hD hNi hNj h⟩
  · exact ⟨1, sepOK_spec (k := 1) hD hNi hNj h⟩
  · exact ⟨2, sepOK_spec (k := 2) hD hNi hNj h⟩
  · exact ⟨3, sepOK_spec (k := 3) hD hNi hNj h⟩

/-! ## Far pairs -/

lemma far_real {D : ℤ} {i j : Sq} (hD : 0 < D)
    (h : 2 * D * D < (j.X - i.X) * (j.X - i.X) + (j.Y - i.Y) * (j.Y - i.Y)) :
    2 < (xr D i - xr D j) ^ 2 + (yr D i - yr D j) ^ 2 := by
  have hD' : (0 : ℝ) < D := by exact_mod_cast hD
  have h' : (2 * D * D : ℝ) < ((j.X : ℝ) - i.X) * (j.X - i.X) + (j.Y - i.Y) * (j.Y - i.Y) := by
    exact_mod_cast h
  have e : (xr D i - xr D j) ^ 2 + (yr D i - yr D j) ^ 2 =
      (((j.X : ℝ) - i.X) * (j.X - i.X) + (j.Y - i.Y) * (j.Y - i.Y)) / (D * D) := by
    simp only [xr, yr]; field_simp; ring
  rw [e, lt_div_iff₀ (by positivity)]
  linarith

lemma pairOK_spec {D : ℤ} {i j : Sq} (hD : 0 < D) (hNi : 0 < i.N) (hNj : 0 < j.N)
    (h : pairOK D i j = true) :
    2 < (xr D i - xr D j) ^ 2 + (yr D i - yr D j) ^ 2 ∨
      SepPair (xr D i) (yr D i) (cr i) (sr i) (xr D j) (yr D j) (cr j) (sr j) := by
  simp only [pairOK, Bool.or_eq_true] at h
  rcases h with (h | h) | h
  · simp only [farOK, decide_eq_true_eq] at h
    exact Or.inl (far_real hD h)
  · exact Or.inr (Or.inl (sepAny_spec hD hNi hNj h))
  · exact Or.inr (Or.inr (sepAny_spec hD hNj hNi h))

/-! ## The list checks -/

theorem sortedX_pairwise : ∀ L : List Sq, sortedX L = true → L.Pairwise (fun a b => a.X ≤ b.X)
  | [], _ => List.Pairwise.nil
  | [_], _ => List.pairwise_singleton _ _
  | a :: b :: rest, h => by
    simp only [sortedX, Bool.and_eq_true, decide_eq_true_eq] at h
    have ih := sortedX_pairwise (b :: rest) h.2
    refine List.Pairwise.cons ?_ ih
    intro r hr
    rcases List.mem_cons.1 hr with rfl | hr
    · exact h.1
    · exact le_trans h.1 (List.rel_of_pairwise_cons ih hr)

lemma farOK_of_cut {D : ℤ} {q r r' : Sq} (h : cutX D q r = true) (hr : r.X ≤ r'.X) :
    pairOK D q r' = true := by
  simp only [cutX, Bool.and_eq_true, decide_eq_true_eq] at h
  obtain ⟨h1, h2⟩ := h
  have a : 0 ≤ r.X - q.X := by omega
  have b : r.X - q.X ≤ r'.X - q.X := by omega
  have hsq : (r.X - q.X) * (r.X - q.X) ≤ (r'.X - q.X) * (r'.X - q.X) :=
    Int.mul_le_mul b b a (le_trans a b)
  have hy : 0 ≤ (r'.Y - q.Y) * (r'.Y - q.Y) := mul_self_nonneg _
  simp only [pairOK, farOK, Bool.or_eq_true, decide_eq_true_eq]
  left; left
  omega

lemma rowOK_spec {D : ℤ} {q : Sq} : ∀ rs : List Sq, rowOK D q rs = true →
    rs.Pairwise (fun a b => a.X ≤ b.X) → (∀ r ∈ rs, q.X ≤ r.X) → ∀ r ∈ rs, pairOK D q r = true
  | [], _, _, _ => by simp
  | r :: rs, h, hs, hq => by
    simp only [rowOK, Bool.or_eq_true, Bool.and_eq_true] at h
    rcases h with h | ⟨h1, h2⟩
    · intro r' hr'
      rcases List.mem_cons.1 hr' with rfl | hr'
      · exact farOK_of_cut h le_rfl
      · exact farOK_of_cut h (List.rel_of_pairwise_cons hs hr')
    · intro r' hr'
      rcases List.mem_cons.1 hr' with rfl | hr'
      · exact h1
      · exact rowOK_spec rs h2 hs.of_cons (fun r hr => hq r (List.mem_cons_of_mem _ hr)) r' hr'

theorem headsOK_nil (D : ℤ) : ∀ k, headsOK D k [] = true
  | 0 => rfl
  | _ + 1 => rfl

theorem headsOK_spec {D : ℤ} : ∀ (k : ℕ) (L : List Sq), headsOK D k L = true →
    L.Pairwise (fun a b => a.X ≤ b.X) → L.length ≤ k → L.Pairwise (fun a b => pairOK D a b = true)
  | _, [], _, _, _ => List.Pairwise.nil
  | 0, _ :: _, _, _, hk => by simp at hk
  | k + 1, q :: rest, h, hs, hk => by
    simp only [headsOK, Bool.and_eq_true] at h
    refine List.Pairwise.cons ?_ (headsOK_spec k rest h.2 hs.of_cons (by simpa using hk))
    exact rowOK_spec rest h.1 hs.of_cons (fun r hr => List.rel_of_pairwise_cons hs hr)

theorem headsOK_add (D : ℤ) : ∀ (a b : ℕ) (L : List Sq),
    headsOK D (a + b) L = (headsOK D a L && headsOK D b (L.drop a))
  | 0, b, L => by simp [headsOK]
  | a + 1, b, [] => by simp [headsOK_nil]
  | a + 1, b, q :: rest => by
    rw [show a + 1 + b = (a + b) + 1 by omega]
    simp only [headsOK, List.drop_succ_cons, headsOK_add D a b rest, Bool.and_assoc]

theorem headsOK_chunks (D : ℤ) (L : List Sq) (k : ℕ) :
    ∀ m : ℕ, (∀ i < m, headsOK D k (L.drop (k * i)) = true) → headsOK D (k * m) L = true
  | 0, _ => by simp [headsOK]
  | m + 1, h => by
    rw [Nat.mul_succ, headsOK_add, headsOK_chunks D L k m (fun i hi => h i (by omega)),
      h m (by omega)]
    rfl

/-- **Soundness of the checker.** -/
theorem check_sound (D Wn Hn Sd : ℤ) (L : List Sq) (K : ℕ) (hD : 0 < D) (hSd : 0 < Sd)
    (hu : L.all unitOK = true) (hb : L.all (boxOK D Wn Hn Sd) = true) (hs : sortedX L = true)
    (hK : L.length ≤ K) (hh : headsOK D K L = true) :
    PacksR L.length ((Wn : ℝ) / Sd) ((Hn : ℝ) / Sd) := by
  rw [List.all_eq_true] at hu hb
  have hN : ∀ q ∈ L, 0 < q.N := fun q hq => by
    have := unitOK_spec (hu q hq); exact_mod_cast this.2
  have hp := headsOK_spec K L hh (sortedX_pairwise L hs) hK
  refine packsR_of_cert (fun i => xr D L[i]) (fun i => yr D L[i]) (fun i => cr L[i])
    (fun i => sr L[i]) (fun i => (unitOK_spec (hu _ (List.getElem_mem _))).1)
    (fun i => boxOK_spec hD (hN _ (List.getElem_mem _)) hSd (hb _ (List.getElem_mem _))) ?_
  intro i j hij
  exact pairOK_spec hD (hN _ (List.getElem_mem _)) (hN _ (List.getElem_mem _))
    (List.pairwise_iff_getElem.1 hp i j i.2 j.2 hij)

end UnitSquarePacking.Cert
