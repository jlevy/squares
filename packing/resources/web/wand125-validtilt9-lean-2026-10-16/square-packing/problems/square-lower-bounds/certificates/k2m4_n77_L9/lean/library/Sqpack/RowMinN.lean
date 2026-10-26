import Sqpack.RowMinK

/-!
# The digit loop of `RowMinK` on natural numbers

`rmLoop` takes the balanced digits of each value with `Int` division; in a kernel check the values
stay unevaluated terms `shiftD K (shiftD K (… v))`, recomputed at every digit.  Here each value `v`
is offset by `H = maskR K L` (each of the `L` digits raised by `2ᴷ⁻¹`): if `v + H ≥ 0`, the plain
digits of `w = v + H` are the balanced digits of `v` plus `2ᴷ⁻¹` (`digit_step`), so the loop runs on
`w &&& (2ᴷ - 1)` and `w >>> K`, natural numbers the kernel computes once each.  `rmChk_sound`: the
natural loop passing implies `rmLoop` passing.
-/

namespace SquarePacking

namespace KArith

/-! ## 1.  The loop -/

/-- The minimum of a list of naturals, `h` for the empty list. -/
def minN (h : ℕ) : List ℕ → ℕ
  | [] => h
  | [a] => a
  | a :: b :: l => min a (minN h (b :: l))

/-- The digit `w mod 2ᴷ` (`neg`: `2ᴷ` minus it), the balanced digit times `±1` plus `2ᴷ⁻¹`. -/
def digN (K : ℕ) (neg : Bool) (w : ℕ) : ℕ :=
  if neg then 2 ^ K - (w &&& (2 ^ K - 1)) else w &&& (2 ^ K - 1)

/-- `rmLoop` on the offset values (`cnt` the number of rows and fixed terms). -/
def rmLoopN (K : ℕ) (neg : Bool) (cnt : ℕ) : ℕ → List (List ℕ) → List ℕ → Bool
  | 0, _, _ => true
  | L + 1, rows, fx =>
    Nat.ble (cnt * 2 ^ (K - 1))
        ((rows.map fun r => minN (2 ^ (K - 1)) (r.map (digN K neg))).sum + (fx.map (digN K neg)).sum) &&
      rmLoopN K neg cnt L (rows.map (·.map (· >>> K))) (fx.map (· >>> K))

/-- **The check**: `ε = ±1`, every `v + maskR K L ≥ 0`, and the loop on the offset values. -/
def rmChk (K : ℕ) (ε : ℤ) (L : ℕ) (rows : List (List ℤ)) (fx : List ℤ) : Bool :=
  let H : ℤ := ((maskR K L : ℕ) : ℤ)
  (ε == 1 || ε == -1) &&
    rows.all (·.all fun v => decide (0 ≤ v + H)) && fx.all (fun v => decide (0 ≤ v + H)) &&
    rmLoopN K (ε != 1) (rows.length + fx.length) L (rows.map (·.map fun v => (v + H).toNat))
      (fx.map fun v => (v + H).toNat)

/-! ## 2.  One digit -/

lemma two_pow_eq {K : ℕ} (hK : 0 < K) : (2 : ℤ) ^ K = 2 * 2 ^ (K - 1) := by
  rw [← pow_succ']; congr 1; omega

lemma balD_shiftD' {K : ℕ} (hK : 0 < K) {c : ℤ} (t : ℤ) (hc0 : -2 ^ (K - 1) ≤ c)
    (hc1 : c < 2 ^ (K - 1)) : balD K (c + 2 ^ K * t) = c ∧ shiftD K (c + 2 ^ K * t) = t := by
  have hX := two_pow_eq hK
  have hpos : (0 : ℤ) < 2 ^ (K - 1) := by positivity
  have hmod : (c + 2 ^ K * t) % 2 ^ K = c % 2 ^ K := by
    rw [add_comm, Int.mul_add_emod_self_left]
  have hb : balD K (c + 2 ^ K * t) = c := by
    unfold balD
    rw [hmod]
    rcases le_or_gt 0 c with h0 | h0
    · rw [Int.emod_eq_of_lt h0 (by linarith), if_pos hc1]
    · have e : c % 2 ^ K = c + 2 ^ K := by
        have e1 : (c + 2 ^ K * 1) % 2 ^ K = c % 2 ^ K := Int.add_mul_emod_self_left _ _ _
        rw [mul_one] at e1
        rw [← e1, Int.emod_eq_of_lt (by linarith) (by linarith)]
      rw [e, if_neg (by linarith)]; ring
  refine ⟨hb, ?_⟩
  unfold shiftD
  rw [hb, add_sub_cancel_left, Int.mul_ediv_cancel_left _ (by positivity)]

/-- **One digit**: if `w = v + maskR K (m + 1)`, the low digit of `w` is the balanced digit of `v`
plus `2ᴷ⁻¹`, and the rest is `shiftD K v + maskR K m`. -/
lemma digit_step {K : ℕ} (hK : 0 < K) {v : ℤ} {m w : ℕ} (hw : (w : ℤ) = v + (maskR K (m + 1) : ℕ)) :
    balD K v = ((w &&& (2 ^ K - 1) : ℕ) : ℤ) - 2 ^ (K - 1) ∧
      ((w >>> K : ℕ) : ℤ) = shiftD K v + (maskR K m : ℕ) := by
  rw [Nat.and_two_pow_sub_one_eq_mod, Nat.shiftRight_eq_div_pow]
  have hX := two_pow_eq hK
  have hdm := Nat.mod_add_div w (2 ^ K)
  have hlt : w % 2 ^ K < 2 ^ K := Nat.mod_lt _ (by positivity)
  have hlt' : ((w % 2 ^ K : ℕ) : ℤ) < 2 ^ K := by exact_mod_cast hlt
  have hv : v = (((w % 2 ^ K : ℕ) : ℤ) - 2 ^ (K - 1)) +
      2 ^ K * (((w / 2 ^ K : ℕ) : ℤ) - (maskR K m : ℕ)) := by
    have e : ((w : ℕ) : ℤ) = ((w % 2 ^ K : ℕ) : ℤ) + 2 ^ K * ((w / 2 ^ K : ℕ) : ℤ) := by
      exact_mod_cast hdm.symm
    have em : ((maskR K (m + 1) : ℕ) : ℤ) = 2 ^ (K - 1) + 2 ^ K * ((maskR K m : ℕ) : ℤ) := by
      simp [maskR]
    rw [em] at hw
    linarith
  have hnn : (0 : ℤ) ≤ ((w % 2 ^ K : ℕ) : ℤ) := Nat.cast_nonneg _
  obtain ⟨h1, h2⟩ := balD_shiftD' hK (((w / 2 ^ K : ℕ) : ℤ) - (maskR K m : ℕ))
    (c := ((w % 2 ^ K : ℕ) : ℤ) - 2 ^ (K - 1)) (by linarith) (by linarith)
  rw [← hv] at h1 h2
  exact ⟨h1, by rw [h2]; ring⟩

/-- The digit times `±1`. -/
lemma digN_eq {K : ℕ} (hK : 0 < K) (neg : Bool) {v : ℤ} {m w : ℕ}
    (hw : (w : ℤ) = v + (maskR K (m + 1) : ℕ)) :
    (if neg then -1 else 1) * balD K v = (digN K neg w : ℤ) - 2 ^ (K - 1) := by
  obtain ⟨h1, -⟩ := digit_step hK hw
  have hX := two_pow_eq hK
  have hlt : w &&& (2 ^ K - 1) < 2 ^ K := by
    rw [Nat.and_two_pow_sub_one_eq_mod]; exact Nat.mod_lt _ (by positivity)
  cases neg with
  | false => simp [digN, h1]
  | true =>
    simp only [digN, if_true, h1]
    rw [Nat.cast_sub hlt.le]
    push_cast
    linarith

/-! ## 3.  Minima and sums -/

lemma minL_eq {f : ℤ → ℤ} {g : ℕ → ℕ} {h : ℕ} {P : ℤ → ℕ → Prop}
    (hfg : ∀ v w, P v w → f v = (g w : ℤ) - h) :
    ∀ (r : List ℤ) (rN : List ℕ), List.Forall₂ P r rN →
      minL (r.map f) = (minN h (rN.map g) : ℤ) - h
  | [], [], _ => by simp [minL, minN]
  | [a], [w], List.Forall₂.cons ha List.Forall₂.nil => by simp [minL, minN, hfg a w ha]
  | a :: b :: l, w :: w' :: lN, List.Forall₂.cons ha hrest => by
    have ih := minL_eq hfg (b :: l) (w' :: lN) hrest
    simp only [List.map_cons] at ih ⊢
    rw [minL, minN, ih, hfg a w ha, Nat.cast_min, min_sub_sub_right]
  | [_], _ :: _ :: _, List.Forall₂.cons _ h => by cases h
  | _ :: _ :: _, [_], List.Forall₂.cons _ h => by cases h

lemma sum_eq {α β : Type*} {F : α → ℤ} {G : β → ℕ} {h : ℕ} {P : α → β → Prop}
    (hFG : ∀ a b, P a b → F a = (G b : ℤ) - h) :
    ∀ (l : List α) (lN : List β), List.Forall₂ P l lN →
      (l.map F).sum = ((lN.map G).sum : ℤ) - l.length * h
  | [], [], _ => by simp
  | a :: l, b :: lN, List.Forall₂.cons hab hrest => by
    simp only [List.map_cons, List.sum_cons, List.length_cons]
    rw [sum_eq hFG l lN hrest, hFG a b hab]
    push_cast
    ring

/-! ## 4.  Soundness -/

theorem rmLoopN_sound {K : ℕ} (hK : 0 < K) (neg : Bool) (cnt : ℕ) :
    ∀ (L : ℕ) (rows : List (List ℤ)) (fx : List ℤ) (rowsN : List (List ℕ)) (fxN : List ℕ),
      cnt = rows.length + fx.length →
      List.Forall₂ (List.Forall₂ fun (v : ℤ) (w : ℕ) => (w : ℤ) = v + (maskR K L : ℕ)) rows rowsN →
      List.Forall₂ (fun (v : ℤ) (w : ℕ) => (w : ℤ) = v + (maskR K L : ℕ)) fx fxN →
      rmLoopN K neg cnt L rowsN fxN = true → rmLoop K (if neg then -1 else 1) L rows fx = true
  | 0, _, _, _, _, _, _, _, _ => rfl
  | L + 1, rows, fx, rowsN, fxN, hcnt, hrows, hfx, h => by
    simp only [rmLoopN, Bool.and_eq_true, Nat.ble_eq] at h
    obtain ⟨h0, hrest⟩ := h
    simp only [rmLoop, Bool.and_eq_true, decide_eq_true_eq]
    have hd : ∀ (v : ℤ) (w : ℕ), (w : ℤ) = v + (maskR K (L + 1) : ℕ) →
        (if neg then -1 else 1) * balD K v = (digN K neg w : ℤ) - (2 ^ (K - 1) : ℕ) := by
      intro v w hw; push_cast; exact digN_eq hK neg hw
    have hrow : ∀ (r : List ℤ) (rN : List ℕ), List.Forall₂ (fun (v : ℤ) (w : ℕ) => (w : ℤ) = v + (maskR K (L + 1) : ℕ)) r rN →
        minL (r.map fun v => (if neg then -1 else 1) * balD K v) =
          (minN (2 ^ (K - 1)) (rN.map (digN K neg)) : ℤ) - (2 ^ (K - 1) : ℕ) :=
      fun r rN hr => minL_eq hd r rN hr
    have s1 := sum_eq (F := fun r => minL (r.map fun v => (if neg then -1 else 1) * balD K v))
      (G := fun r => minN (2 ^ (K - 1)) (r.map (digN K neg))) hrow rows rowsN hrows
    have s2 := sum_eq (F := fun v => (if neg then -1 else 1) * balD K v) (G := digN K neg) hd fx fxN hfx
    refine ⟨?_, ?_⟩
    · rw [s1, s2]
      have : ((cnt * 2 ^ (K - 1) : ℕ) : ℤ) ≤
          (((rowsN.map fun r => minN (2 ^ (K - 1)) (r.map (digN K neg))).sum +
            (fxN.map (digN K neg)).sum : ℕ) : ℤ) := by exact_mod_cast h0
      rw [hcnt] at this
      push_cast at this ⊢
      linarith
    · have hsh : ∀ (v : ℤ) (w : ℕ), (w : ℤ) = v + (maskR K (L + 1) : ℕ) →
          ((w >>> K : ℕ) : ℤ) = shiftD K v + (maskR K L : ℕ) := fun v w hw => (digit_step hK hw).2
      refine rmLoopN_sound hK neg cnt L _ _ _ _ (by simp [hcnt]) ?_ ?_ hrest
      · rw [List.forall₂_map_left_iff, List.forall₂_map_right_iff]
        refine hrows.imp fun r rN hr => ?_
        rw [List.forall₂_map_left_iff, List.forall₂_map_right_iff]
        exact hr.imp fun v w hw => hsh v w hw
      · rw [List.forall₂_map_left_iff, List.forall₂_map_right_iff]
        exact hfx.imp fun v w hw => hsh v w hw

lemma forall₂_toNat {H : ℤ} : ∀ (l : List ℤ), (∀ v ∈ l, 0 ≤ v + H) →
    List.Forall₂ (fun (v : ℤ) (w : ℕ) => (w : ℤ) = v + H) l (l.map fun v => (v + H).toNat)
  | [], _ => List.Forall₂.nil
  | v :: l, h => List.Forall₂.cons (Int.toNat_of_nonneg (h v List.mem_cons_self))
      (forall₂_toNat l fun x hx => h x (List.mem_cons_of_mem _ hx))

/-- **`rmChk` implies `rmLoop`.** -/
theorem rmChk_sound {K : ℕ} (hK : 0 < K) {ε : ℤ} {L : ℕ} {rows : List (List ℤ)} {fx : List ℤ}
    (h : rmChk K ε L rows fx = true) : rmLoop K ε L rows fx = true := by
  simp only [rmChk, Bool.and_eq_true, Bool.or_eq_true, beq_iff_eq, List.all_eq_true,
    decide_eq_true_eq] at h
  obtain ⟨⟨⟨hε, hr⟩, hf⟩, hloop⟩ := h
  have e : ε = if (ε != 1) = true then -1 else 1 := by
    rcases hε with rfl | rfl <;> simp
  rw [e]
  refine rmLoopN_sound hK _ _ L rows fx _ _ rfl ?_ (forall₂_toNat fx hf) hloop
  rw [List.forall₂_map_right_iff]
  exact List.forall₂_same.mpr fun r hr' => forall₂_toNat r (hr r hr')

end KArith

end SquarePacking
