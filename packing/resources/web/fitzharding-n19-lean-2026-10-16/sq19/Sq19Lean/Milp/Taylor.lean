import Sq19Lean.Milp.Interval

/-!
# First-order Taylor forms

A form `t = ⟨c, l⟩` encloses a real function `f` of the angle offsets `δ` on the box `|δ k| ≤ H k`
when `f δ - Σ_k l[k] δ_k ∈ c` for every such `δ`. The linear part is exact (rational); every error
(products of linear parts, rounding of coefficients, Taylor remainders) goes into the interval `c`.
This keeps the cancellation between rows that a centred form keeps, using only elementary bounds.
-/
namespace Sq19.Milp

/-- `Σ_k l[k] δ_k`. -/
def linEval : List ℚ → (ℕ → ℝ) → ℝ
  | [], _ => 0
  | a :: l, δ => (a : ℝ) * δ 0 + linEval l (fun k => δ (k+1))

/-- `Σ_k |l[k]| H_k`. -/
def linNorm : List ℚ → (ℕ → ℚ) → ℚ
  | [], _ => 0
  | a :: l, H => |a| * H 0 + linNorm l (fun k => H (k+1))

theorem abs_linEval_le (l : List ℚ) (δ : ℕ → ℝ) (H : ℕ → ℚ) (hδ : ∀ k, |δ k| ≤ H k) :
    |linEval l δ| ≤ (linNorm l H : ℝ) := by
  induction l generalizing δ H with
  | nil => simp [linEval, linNorm]
  | cons a l ih =>
    simp only [linEval, linNorm]
    push_cast
    have h1 : |(a:ℝ) * δ 0| ≤ |(a:ℝ)| * H 0 := by
      rw [abs_mul]; exact mul_le_mul_of_nonneg_left (hδ 0) (abs_nonneg _)
    have h2 := ih (fun k => δ (k+1)) (fun k => H (k+1)) (fun k => hδ (k+1))
    exact (abs_add_le _ _).trans (add_le_add h1 h2)

theorem linNorm_nonneg (l : List ℚ) (H : ℕ → ℚ) (hH : ∀ k, 0 ≤ H k) : 0 ≤ linNorm l H := by
  induction l generalizing H with
  | nil => simp [linNorm]
  | cons a l ih =>
    simp only [linNorm]
    exact add_nonneg (mul_nonneg (abs_nonneg a) (hH 0)) (ih _ (fun k => hH (k+1)))

def ladd : List ℚ → List ℚ → List ℚ
  | [], l => l
  | a :: l, [] => a :: l
  | a :: l, b :: l' => (a+b) :: ladd l l'

theorem linEval_ladd (l l' : List ℚ) (δ : ℕ → ℝ) :
    linEval (ladd l l') δ = linEval l δ + linEval l' δ := by
  induction l generalizing l' δ with
  | nil => simp [ladd, linEval]
  | cons a l ih =>
    cases l' with
    | nil => simp [ladd, linEval]
    | cons b l' =>
      simp only [ladd, linEval, ih]
      push_cast; ring

def lscale (q : ℚ) (l : List ℚ) : List ℚ := l.map (q * ·)

theorem linEval_lscale (q : ℚ) (l : List ℚ) (δ : ℕ → ℝ) :
    linEval (lscale q l) δ = q * linEval l δ := by
  induction l generalizing δ with
  | nil => simp [lscale, linEval]
  | cons a l ih =>
    simp only [lscale, List.map_cons, linEval] at ih ⊢
    rw [ih]; push_cast; ring

/-- Coefficients rounded down to the grid, and the rounding errors. -/
def lround (l : List ℚ) : List ℚ := l.map rdn
def lerr (l : List ℚ) : List ℚ := l.map (fun a => a - rdn a)

theorem linEval_lround (l : List ℚ) (δ : ℕ → ℝ) :
    linEval l δ = linEval (lround l) δ + linEval (lerr l) δ := by
  induction l generalizing δ with
  | nil => simp [lround, lerr, linEval]
  | cons a l ih =>
    simp only [lround, lerr, List.map_cons, linEval] at ih ⊢
    rw [ih]; push_cast; ring

/-- The form `a δ_k`. -/
def lsingle : ℕ → ℚ → List ℚ
  | 0, a => [a]
  | k+1, a => 0 :: lsingle k a

theorem linEval_lsingle (k : ℕ) (a : ℚ) (δ : ℕ → ℝ) : linEval (lsingle k a) δ = a * δ k := by
  induction k generalizing δ with
  | zero => simp [lsingle, linEval]
  | succ k ih => simp [lsingle, linEval, ih]

structure TF where
  c : Iv
  l : List ℚ

/-- `t` encloses `f` on the box `|δ k| ≤ H k`. -/
def TF.Encl (H : ℕ → ℚ) (t : TF) (f : (ℕ → ℝ) → ℝ) : Prop :=
  ∀ δ : ℕ → ℝ, (∀ k, |δ k| ≤ H k) → Iv.mem (f δ - linEval t.l δ) t.c

def TF.const (I : Iv) : TF := ⟨I, []⟩
def TF.add (t u : TF) : TF := ⟨t.c.add u.c, ladd t.l u.l⟩
def TF.neg (t : TF) : TF := ⟨t.c.neg, lscale (-1) t.l⟩
/-- Coefficients rounded, the error moved into the interval. -/
def TF.tidy (H : ℕ → ℚ) (t : TF) : TF := ⟨t.c.widen (linNorm (lerr t.l) H), lround t.l⟩
def TF.mulRaw (H : ℕ → ℚ) (t u : TF) : TF :=
  let N := linNorm t.l H
  let N' := linNorm u.l H
  ⟨(t.c.mul u.c).widen (t.c.rad * N' + u.c.rad * N + N * N'),
    ladd (lscale t.c.mid u.l) (lscale u.c.mid t.l)⟩
def TF.mul (H : ℕ → ℚ) (t u : TF) : TF := (TF.mulRaw H t u).tidy H
/-- An interval containing every value of an enclosed function on the box. -/
def TF.range (H : ℕ → ℚ) (t : TF) : Iv := t.c.widen (linNorm t.l H)

theorem TF.encl_const (H : ℕ → ℚ) (I : Iv) (f : (ℕ → ℝ) → ℝ) (hf : ∀ δ, Iv.mem (f δ) I) :
    (TF.const I).Encl H f := by
  intro δ _; simpa [TF.const, linEval] using hf δ

theorem TF.encl_add {H : ℕ → ℚ} {t u : TF} {f g : (ℕ → ℝ) → ℝ} (ht : t.Encl H f)
    (hu : u.Encl H g) : (t.add u).Encl H (fun δ => f δ + g δ) := by
  intro δ hδ
  have h := Iv.mem_add (ht δ hδ) (hu δ hδ)
  simp only [TF.add, linEval_ladd]
  convert h using 1; ring

theorem TF.encl_neg {H : ℕ → ℚ} {t : TF} {f : (ℕ → ℝ) → ℝ} (ht : t.Encl H f) :
    t.neg.Encl H (fun δ => -f δ) := by
  intro δ hδ
  have h := Iv.mem_neg (ht δ hδ)
  simp only [TF.neg, linEval_lscale]
  convert h using 1; push_cast; ring

theorem TF.encl_tidy {H : ℕ → ℚ} {t : TF} {f : (ℕ → ℝ) → ℝ} (ht : t.Encl H f) :
    (t.tidy H).Encl H f := by
  intro δ hδ
  have h := Iv.mem_widen (ht δ hδ) (abs_linEval_le (lerr t.l) δ H hδ)
  simp only [TF.tidy]
  convert h using 1
  rw [linEval_lround t.l δ]; ring

theorem TF.encl_mulRaw {H : ℕ → ℚ} {t u : TF} {f g : (ℕ → ℝ) → ℝ} (ht : t.Encl H f)
    (hu : u.Encl H g) : (TF.mulRaw H t u).Encl H (fun δ => f δ * g δ) := by
  intro δ hδ
  set C := f δ - linEval t.l δ with hC
  set C' := g δ - linEval u.l δ with hC'
  set Λ := linEval t.l δ
  set Λ' := linEval u.l δ
  have hCm := ht δ hδ
  have hC'm := hu δ hδ
  have hN := abs_linEval_le t.l δ H hδ
  have hN' := abs_linEval_le u.l δ H hδ
  have hr := Iv.abs_sub_mid hCm
  have hr' := Iv.abs_sub_mid hC'm
  have hP := Iv.mem_mul hCm hC'm
  set m : ℝ := (t.c.mid : ℝ)
  set m' : ℝ := (u.c.mid : ℝ)
  have hE : |(C - m) * Λ' + (C' - m') * Λ + Λ * Λ'| ≤
      ((t.c.rad * linNorm u.l H + u.c.rad * linNorm t.l H +
        linNorm t.l H * linNorm u.l H : ℚ) : ℝ) := by
    push_cast
    have a1 : |(C - m) * Λ'| ≤ (t.c.rad : ℝ) * linNorm u.l H := by
      rw [abs_mul]; exact mul_le_mul hr hN' (abs_nonneg _) ((abs_nonneg _).trans hr)
    have a2 : |(C' - m') * Λ| ≤ (u.c.rad : ℝ) * linNorm t.l H := by
      rw [abs_mul]; exact mul_le_mul hr' hN (abs_nonneg _) ((abs_nonneg _).trans hr')
    have a3 : |Λ * Λ'| ≤ (linNorm t.l H : ℝ) * linNorm u.l H := by
      rw [abs_mul]; exact mul_le_mul hN hN' (abs_nonneg _) ((abs_nonneg _).trans hN)
    calc _ ≤ |(C - m) * Λ' + (C' - m') * Λ| + |Λ * Λ'| := abs_add_le _ _
      _ ≤ |(C - m) * Λ'| + |(C' - m') * Λ| + |Λ * Λ'| := by
          gcongr; exact abs_add_le _ _
      _ ≤ _ := by linarith
  have h := Iv.mem_widen hP hE
  simp only [TF.mulRaw]
  convert h using 1
  rw [linEval_ladd, linEval_lscale, linEval_lscale]
  simp only [hC, hC', m, m']
  ring

theorem TF.encl_mul {H : ℕ → ℚ} {t u : TF} {f g : (ℕ → ℝ) → ℝ} (ht : t.Encl H f)
    (hu : u.Encl H g) : (TF.mul H t u).Encl H (fun δ => f δ * g δ) :=
  TF.encl_tidy (TF.encl_mulRaw ht hu)

theorem TF.mem_range {H : ℕ → ℚ} {t : TF} {f : (ℕ → ℝ) → ℝ} (ht : t.Encl H f)
    (δ : ℕ → ℝ) (hδ : ∀ k, |δ k| ≤ H k) : Iv.mem (f δ) (t.range H) := by
  have h := Iv.mem_widen (ht δ hδ) (abs_linEval_le t.l δ H hδ)
  simp only [TF.range]
  convert h using 1; ring

end Sq19.Milp
