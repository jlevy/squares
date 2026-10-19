import Sqpack.S32Data

/-!
# `s(32) = 6`, from one computational hypothesis

`s(n)` is the side of the smallest square into which `n` closed unit squares with pairwise
disjoint interiors can be placed (rotations allowed): `minSide n = sInf {s | Packs n s}`.

* `packs_grid` — the `n × n` grid packs any `k ≤ n²` squares, so `Packs 32 6`
  (`s32_packs`; no hypothesis).
* `not_packs_of_cover` — the classical scaling argument on top of `packing_le_weight`: a weighted
  cover of `box m` of total weight `< n` excludes packing `n` unit squares in any `box s`, `s < m`.
* `S32Data.check_ok`, `S32Data.total_lt`, `S32Data.d4Inv` — **proved in Lean** (kernel
  evaluation, `decide +kernel`, no `native_decide`) for the cover `S32Data.tree`, transcribed line
  by line from `runs/s32-close_candidate.txt` (`Sqpack/S32Data.lean`): its total weight is
  `3171350535386 / 10¹¹ < 32`, and it is invariant under `x ↦ 6 − x` and `x ↔ y`.
* `S32RegionCover` — **the one hypothesis**: every closed unit square in `[0,6]²` with centre in
  `[0,3]²` and angle `θ ∈ [0, π/4]` contains cover points of total weight `≥ 1`.
  `S32CheckerCover` is the same with the checkers' angle range `θ = 2 arctan u`, `u ∈ [0, 1/2]`
  (a stronger statement, `S32CheckerCover.region`); that is literally what the `zeromargin.py`
  D4 run `runs/s32py_d4` certifies (`notes/lean-s32.md`).
* **`s32_eq_six`** — `S32RegionCover → minSide 32 = 6`, via `s32_isLeast`
  (`IsLeast {s | Packs 32 s} 6`: the minimum exists and is `6`).
-/

open Finset
open scoped Classical

namespace SquarePacking

/-! ## 1.  Packings and `s(n)` -/

/-- `n` closed unit squares with pairwise disjoint interiors fit in the square `[0,s]²`. -/
def Packs (n : ℕ) (s : ℝ) : Prop :=
  ∃ (ctr : Fin n → ℝ × ℝ) (ang : Fin n → ℝ), (∀ i, sq (ctr i) (ang i) 1 ⊆ box s) ∧
    ∀ i j, i ≠ j → Disjoint (sqInt (ctr i) (ang i) 1) (sqInt (ctr j) (ang j) 1)

/-- `s(n)`: the infimum of the sides of the squares into which `n` unit squares can be packed. -/
noncomputable def minSide (n : ℕ) : ℝ := sInf {s | Packs n s}

/-- A unit square's axis-parallel bounding box has side `w(θ) ≥ 1`. -/
lemma one_le_wid (θ : ℝ) : 1 ≤ wid θ := by
  have h := Real.cos_sq_add_sin_sq θ
  have hc := Real.abs_cos_le_one θ
  have hs := Real.abs_sin_le_one θ
  have hc0 := abs_nonneg (Real.cos θ)
  have hs0 := abs_nonneg (Real.sin θ)
  rw [← sq_abs (Real.cos θ), ← sq_abs (Real.sin θ)] at h
  unfold wid
  nlinarith

/-- Scaling by `μ > 0`: `q` is in the `μ`-square about `μ c` iff `q/μ` is in the unit square
about `c`. -/
lemma mem_sq_scale_iff {μ : ℝ} (hμ : 0 < μ) (c : ℝ × ℝ) (θ : ℝ) (q : ℝ × ℝ) :
    q ∈ sq (μ * c.1, μ * c.2) θ μ ↔ (q.1 / μ, q.2 / μ) ∈ sq c θ 1 := by
  have e1 : (coord (μ * c.1, μ * c.2) θ q).1 = μ * (coord c θ (q.1 / μ, q.2 / μ)).1 := by
    simp only [coord]; field_simp
  have e2 : (coord (μ * c.1, μ * c.2) θ q).2 = μ * (coord c θ (q.1 / μ, q.2 / μ)).2 := by
    simp only [coord]; field_simp
  simp only [sq, Set.mem_ofPred_eq, e1, e2, abs_mul, abs_of_pos hμ]
  constructor
  · rintro ⟨h1, h2⟩; constructor <;> nlinarith
  · rintro ⟨h1, h2⟩; constructor <;> nlinarith

/-- The same for interiors. -/
lemma mem_sqInt_scale_iff {μ : ℝ} (hμ : 0 < μ) (c : ℝ × ℝ) (θ : ℝ) (q : ℝ × ℝ) :
    q ∈ sqInt (μ * c.1, μ * c.2) θ μ ↔ (q.1 / μ, q.2 / μ) ∈ sqInt c θ 1 := by
  have e1 : (coord (μ * c.1, μ * c.2) θ q).1 = μ * (coord c θ (q.1 / μ, q.2 / μ)).1 := by
    simp only [coord]; field_simp
  have e2 : (coord (μ * c.1, μ * c.2) θ q).2 = μ * (coord c θ (q.1 / μ, q.2 / μ)).2 := by
    simp only [coord]; field_simp
  simp only [sqInt, Set.mem_ofPred_eq, e1, e2, abs_mul, abs_of_pos hμ]
  constructor
  · rintro ⟨h1, h2⟩; constructor <;> nlinarith
  · rintro ⟨h1, h2⟩; constructor <;> nlinarith

/-- **Lower bounds from a weighted cover.**  If every closed unit square inside `box m` captures
weight `≥ 1` from a weighted point set of total weight `< n`, then `n` unit squares cannot be
packed in `box s` for any `s < m`: scale such a packing by `m/s > 1` and apply
`packing_le_weight`. -/
theorem not_packs_of_cover (m : ℝ) (A : Finset (ℝ × ℝ)) (w : ℝ × ℝ → ℝ)
    (hw : ∀ a ∈ A, 0 ≤ w a)
    (hcover : ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box m →
        1 ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a)
    (n : ℕ) (htot : ∑ a ∈ A, w a < n) {s : ℝ} (hs : s < m) : ¬ Packs n s := by
  rintro ⟨ctr, ang, hin, hdisj⟩
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · have := Finset.sum_nonneg hw
    simp only [Nat.cast_zero] at htot
    linarith
  -- a unit square fits, so `s ≥ 1`
  have hs1 : 1 ≤ s := by
    obtain ⟨h1, h2, _, _⟩ := (sq_subset_box_iff s _ _).mp (hin ⟨0, hn⟩)
    linarith [one_le_wid (ang ⟨0, hn⟩)]
  have hs0 : 0 < s := by linarith
  set μ := m / s with hμdef
  have hμ : 1 < μ := (one_lt_div hs0).mpr hs
  have hμ0 : 0 < μ := by linarith
  have hμs : μ * s = m := by rw [hμdef]; field_simp
  have h := packing_le_weight A w hw (box m) hcover n μ hμ
    (fun i => (μ * (ctr i).1, μ * (ctr i).2)) ang ?_ ?_
  · linarith
  · intro i q hq
    rw [mem_sq_scale_iff hμ0] at hq
    obtain ⟨h1, h2, h3, h4⟩ := hin i hq
    simp only at h1 h2 h3 h4
    have e1 : q.1 = μ * (q.1 / μ) := by field_simp
    have e2 : q.2 = μ * (q.2 / μ) := by field_simp
    refine ⟨?_, ?_, ?_, ?_⟩
    · rw [e1]; positivity
    · rw [e1, ← hμs]; exact mul_le_mul_of_nonneg_left h2 hμ0.le
    · rw [e2]; positivity
    · rw [e2, ← hμs]; exact mul_le_mul_of_nonneg_left h4 hμ0.le
  · intro i j hij
    rw [Set.disjoint_left]
    intro q hqi hqj
    rw [mem_sqInt_scale_iff hμ0] at hqi hqj
    exact Set.disjoint_left.mp (hdisj i j hij) hqi hqj

/-! ## 2.  The grid packing -/

lemma mem_sq_zero (c p : ℝ × ℝ) (L : ℝ) :
    p ∈ sq c 0 L ↔ |p.1 - c.1| ≤ L / 2 ∧ |p.2 - c.2| ≤ L / 2 := by
  simp [sq, coord]

lemma mem_sqInt_zero (c p : ℝ × ℝ) (L : ℝ) :
    p ∈ sqInt c 0 L ↔ |p.1 - c.1| < L / 2 ∧ |p.2 - c.2| < L / 2 := by
  simp [sqInt, coord]

/-- Two open unit intervals `(a, a+1)`, `(b, b+1)` with `a ≠ b` natural numbers are disjoint. -/
lemma nat_eq_of_abs_lt {a b : ℕ} {x : ℝ} (ha : |x - ((a : ℝ) + 1 / 2)| < 1 / 2)
    (hb : |x - ((b : ℝ) + 1 / 2)| < 1 / 2) : a = b := by
  rw [abs_lt] at ha hb
  have h1 : (a : ℝ) < b + 1 := by linarith
  have h2 : (b : ℝ) < a + 1 := by linarith
  have h1' : a < b + 1 := by exact_mod_cast h1
  have h2' : b < a + 1 := by exact_mod_cast h2
  omega

/-- **The grid packing.**  The `n × n` grid of axis-parallel unit squares packs any `k ≤ n²` of
them in `[0,n]²`. -/
theorem packs_grid (n k : ℕ) (hk : k ≤ n * n) : Packs k n := by
  refine ⟨fun i => ((((i : ℕ) / n : ℕ) : ℝ) + 1 / 2, (((i : ℕ) % n : ℕ) : ℝ) + 1 / 2),
    fun _ => 0, ?_, ?_⟩
  · intro i p hp
    rw [mem_sq_zero] at hp
    obtain ⟨h1, h2⟩ := hp
    rw [abs_le] at h1 h2
    have hi : (i : ℕ) < n * n := lt_of_lt_of_le i.2 hk
    have hn : 0 < n := by
      rcases Nat.eq_zero_or_pos n with h | h
      · simp [h] at hi
      · exact h
    have hq : (i : ℕ) / n + 1 ≤ n := Nat.div_lt_of_lt_mul hi
    have hr : (i : ℕ) % n + 1 ≤ n := Nat.mod_lt _ hn
    have hq' : ((((i : ℕ) / n : ℕ) : ℝ)) + 1 ≤ n := by exact_mod_cast hq
    have hr' : ((((i : ℕ) % n : ℕ) : ℝ)) + 1 ≤ n := by exact_mod_cast hr
    have hq0 : (0 : ℝ) ≤ (((i : ℕ) / n : ℕ) : ℝ) := Nat.cast_nonneg _
    have hr0 : (0 : ℝ) ≤ (((i : ℕ) % n : ℕ) : ℝ) := Nat.cast_nonneg _
    simp only at h1 h2
    exact ⟨by linarith, by linarith, by linarith, by linarith⟩
  · intro i j hij
    rw [Set.disjoint_left]
    intro p hpi hpj
    rw [mem_sqInt_zero] at hpi hpj
    have e1 := nat_eq_of_abs_lt (by simpa using hpi.1) (by simpa using hpj.1)
    have e2 := nat_eq_of_abs_lt (by simpa using hpi.2) (by simpa using hpj.2)
    apply hij
    apply Fin.ext
    rw [← Nat.div_add_mod (i : ℕ) n, ← Nat.div_add_mod (j : ℕ) n, e1, e2]

/-! ## 3.  The `s(32)` cover -/

namespace S32Data

/-- The entries of the cover, as a finite set of integer triples `(x, y, w)`. -/
def entries : Finset (ℕ × ℕ × ℕ) := tree.toList.toFinset

/-- The point of an entry: `(x/1000, y/1000)`. -/
noncomputable def pt (e : ℕ × ℕ × ℕ) : ℝ × ℝ := ((e.1 : ℝ) / 1000, (e.2.1 : ℝ) / 1000)

/-- The weight of an entry: `w/10¹¹`. -/
noncomputable def wt (e : ℕ × ℕ × ℕ) : ℝ := (e.2.2 : ℝ) / 100000000000

/-- The cover as a weighted point set (the form `packing_le_weight` takes). -/
noncomputable def A : Finset (ℝ × ℝ) := coverA entries pt

/-- Its weight function: the total weight of the entries at a point. -/
noncomputable def w : ℝ × ℝ → ℝ := coverW entries pt wt

/-- The integer images of an entry under `x ↦ 6 − x` and `x ↔ y`. -/
def gX (e : ℕ × ℕ × ℕ) : ℕ × ℕ × ℕ := (6000 - e.1, e.2.1, e.2.2)
def gS (e : ℕ × ℕ × ℕ) : ℕ × ℕ × ℕ := (e.2.1, e.1, e.2.2)

/-- The data checks: keys strictly increasing (so no entry is repeated), `x ≤ 6000`, and the two
reflections of every entry, with the same weight, are entries. -/
def check : Bool :=
  PTree.chainB tree.toList &&
    tree.all (fun e => Nat.ble e.1 6000 && tree.mem (gX e) && tree.mem (gS e))

/-- **The data checks pass** (kernel evaluation, ~30 s). -/
theorem check_ok : check = true := by decide +kernel

/-- **The total weight, as an integer** (kernel evaluation). -/
theorem wsum_tree : tree.wsum = 3171350535386 := by decide +kernel

theorem nodup : tree.toList.Nodup := by
  have h := check_ok
  simp only [check, Bool.and_eq_true] at h
  exact PTree.nodup_of_chainB _ h.1

/-- **13,085 entries**, one per certificate line (kernel evaluation). -/
theorem card_entries : entries.card = 13085 := by
  have hl : tree.toList.length = 13085 := by decide +kernel
  rw [entries, List.toFinset_card_of_nodup nodup, hl]

theorem entry_ok (e : ℕ × ℕ × ℕ) (he : e ∈ entries) :
    e.1 ≤ 6000 ∧ gX e ∈ entries ∧ gS e ∈ entries := by
  have h := check_ok
  simp only [check, Bool.and_eq_true] at h
  have h2 := (PTree.all_iff _ tree).mp h.2 e (List.mem_toFinset.mp he)
  simp only [Bool.and_eq_true, Nat.ble_eq] at h2
  exact ⟨h2.1.1, List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.1.2),
    List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.2)⟩

/-- **The total weight is `31.7135… < 32`** (proved). -/
theorem total_lt : ∑ a ∈ A, w a < 32 := by
  rw [A, w, sum_coverA]
  have hsum : ∑ e ∈ entries, wt e = (3171350535386 : ℝ) / 100000000000 := by
    have hn : ∑ e ∈ entries, e.2.2 = 3171350535386 := by
      rw [entries, List.sum_toFinset _ nodup, ← PTree.wsum_eq, wsum_tree]
    have hr : ∑ e ∈ entries, (e.2.2 : ℝ) = 3171350535386 := by
      rw [← Nat.cast_sum, hn]; norm_num
    unfold wt
    rw [← Finset.sum_div, hr]
  rw [hsum]
  norm_num

/-- The weights are non-negative. -/
theorem w_nonneg : ∀ a ∈ A, 0 ≤ w a := by
  intro a _
  unfold w coverW
  exact Finset.sum_nonneg fun e _ => by unfold wt; positivity

/-- **The cover is D4-invariant** (proved). -/
theorem d4Inv : D4Inv 6 A w := by
  refine D4Inv_cover 6 entries pt wt gX gS ?_ ?_
  · intro e he
    obtain ⟨hx, hgX, _⟩ := entry_ok e he
    refine ⟨hgX, ?_, rfl, ?_⟩
    · simp only [pt, gX, reflX, Nat.cast_sub hx]
      ext
      · simp; ring
      · simp
    · obtain ⟨a, b, c⟩ := e
      simp only [gX] at hx ⊢
      ext <;> simp; omega
  · intro e he
    exact ⟨(entry_ok e he).2.2, rfl, rfl, rfl⟩

end S32Data

open S32Data

/-! ## 4.  The hypothesis and the theorem -/

/-- **The computational hypothesis.**  Every closed unit square inside `[0,6]²` whose centre lies
in `[0,3]²` and whose angle lies in `[0, π/4]` contains entries of the cover
(`runs/s32-close_candidate.txt`) of total weight `≥ 1`. -/
def S32RegionCover : Prop :=
  ∀ (c : ℝ × ℝ) (θ : ℝ), c.1 ∈ Set.Icc 0 3 → c.2 ∈ Set.Icc 0 3 →
    θ ∈ Set.Icc 0 (Real.pi / 4) → sq c θ 1 ⊆ box 6 →
      1 ≤ ∑ e ∈ entries.filter (fun e => pt e ∈ sq c θ 1), wt e

/-- **The hypothesis in the checkers' coordinates**: the root domain `[0,3]² × u ∈ [0, 1/2]`
with `θ = 2 arctan u`, which `zeromargin.py` covers by its 7,200 D4 roots. -/
def S32CheckerCover : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ), c.1 ∈ Set.Icc 0 3 → c.2 ∈ Set.Icc 0 3 →
    u ∈ Set.Icc 0 (1 / 2) → sq c (2 * Real.arctan u) 1 ⊆ box 6 →
      1 ≤ ∑ e ∈ entries.filter (fun e => pt e ∈ sq c (2 * Real.arctan u) 1), wt e

/-- The checker's statement implies the region statement (its angle range is larger). -/
theorem S32CheckerCover.region (h : S32CheckerCover) : S32RegionCover := by
  intro c θ h1 h2 hθ hsub
  obtain ⟨u, hu, rfl⟩ := exists_u_of_theta hθ
  exact h c u h1 h2 hu hsub

/-- From the region to every closed unit square in `[0,6]²` (the D4 reduction). -/
theorem s32_cover_all (h : S32RegionCover) :
    ∀ (c : ℝ × ℝ) (θ : ℝ), sq c θ 1 ⊆ box 6 →
      1 ≤ ∑ a ∈ A.filter (fun a => a ∈ sq c θ 1), w a := by
  refine d4_reduction 6 A w d4Inv fun c θ h1 h2 hθ hsub => ?_
  have e : (6 : ℝ) / 2 = 3 := by norm_num
  rw [e] at h1 h2
  rw [A, w, sum_filter_coverA]
  exact h c θ h1 h2 hθ hsub

/-- **Lower bound**: under the hypothesis, 32 unit squares do not fit in a square of side `< 6`. -/
theorem s32_not_packs (h : S32RegionCover) {s : ℝ} (hs : s < 6) : ¬ Packs 32 s :=
  not_packs_of_cover 6 A w w_nonneg (s32_cover_all h) 32 (by exact_mod_cast total_lt) hs

/-- **Upper bound**: 32 unit squares fit in `[0,6]²` (the 6 × 6 grid minus 4). -/
theorem s32_packs : Packs 32 6 := by
  have h := packs_grid 6 32 (by norm_num)
  simpa using h

/-- Under the hypothesis, `6` is the least side of a square holding 32 unit squares. -/
theorem s32_isLeast (h : S32RegionCover) : IsLeast {s | Packs 32 s} 6 :=
  ⟨s32_packs, fun _ hs => not_lt.mp fun hlt => s32_not_packs h hlt hs⟩

/-- **`s(32) = 6`**, from the single computational hypothesis `S32RegionCover`. -/
theorem s32_eq_six (h : S32RegionCover) : minSide 32 = 6 :=
  (s32_isLeast h).csInf_eq

/-- **`s(32) = 6`**, from the statement the `zeromargin.py` D4 run certifies. -/
theorem s32_eq_six_of_checker (h : S32CheckerCover) : minSide 32 = 6 :=
  s32_eq_six h.region

end SquarePacking
