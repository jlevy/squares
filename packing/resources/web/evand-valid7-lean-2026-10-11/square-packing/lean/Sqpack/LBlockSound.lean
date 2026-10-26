import Sqpack.LBlock

/-!
# Soundness of the L-block check

* §1 options: the value of an option at a pose (`oval`), its corner form, the per-corner inequalities
  (`corner_facts`).
* §2 concavity: the lower bound `Φ` (sum over lines and ends of the minimum over options) is concave in
  the centre, hence `≥ lg` on the box.
* §3 chord and gains: at a pose, each line's chord contains `[b − y, a + x]`; the pieces give parts
  whose masses are at least the core plus `Φ`'s terms.
-/

namespace SquarePacking

namespace ZMTreeM

open BoxTree ZMTree

/-! ## 1.  Options -/

/-- A quadratic's value. -/
noncomputable def e3 (n : SP × SP × SP) (v : ℝ) : ℝ := sv n.1 + sv n.2.1 * v + sv n.2.2 * v ^ 2

/-- The slope magnitude of a condition of type `f` along the line: `4u` (`f = 1`), `2(1 − u²)`. -/
noncomputable def sig (f : ℕ) (u : ℝ) : ℝ := if f = 1 then 4 * u else 2 * (1 - u ^ 2)

/-- The value of an option at a pose (fine units): the cap, or `i − s Q G_k(end point)/σ_k(u)`. -/
noncomputable def oval (Q : ℕ) (l : LLine) (up : Bool) (cap o : ℕ) (c : ℝ × ℝ) (u : ℝ) : ℝ :=
  if o = 0 then (cap : ℝ) else
    sv (if up then l.iU else l.iD) - ((if up then l.sU else l.sD : ℕ) : ℝ) * Q *
      Gv Q (o - 1) (lpx l (if up then l.a else l.b)) (lpy l (if up then l.a else l.b)) c u /
        sig (ktype l.dir (o - 1)) u

lemma ktype_cases (dir k : ℕ) : ktype dir k = 1 ∨ ktype dir k = 2 := by
  unfold ktype
  cases Nat.beq dir 0 <;> cases Nat.blt k 2 <;> simp

lemma sigq_e3 (R f : ℕ) (hf : f = 1 ∨ f = 2) (v : ℝ) : e3 (sigq R f) v = fval f R v := by
  rcases hf with rfl | rfl
  · simp only [sigq, e3, fval, beq_rfl, cond_true, sv, nat_mul_eq]; push_cast; ring
  · simp only [sigq, e3, fval, show Nat.beq 2 1 = false from rfl, cond_false, sv, nat_mul_eq]
    push_cast; ring

lemma fval_sig {R f : ℕ} (hf : f = 1 ∨ f = 2) (u : ℝ) :
    fval f R (u * R) = (R : ℝ) ^ 2 * sig f u := by
  rcases hf with rfl | rfl
  · simp only [fval, sig, if_true]; ring
  · simp only [fval, sig, show (2 : ℕ) ≠ 1 by norm_num, if_false]; ring

/-- The corner form of an option: `N(v)/σ̂(v)` is the option's value at the corner. -/
lemma optN_val {Q R : ℕ} (hQ : 0 < Q) (hR : 0 < R) (l : LLine) (s : ℕ) (i : SP) (t k cx cy : ℕ)
    (hk : k < 4) (u : ℝ) (hsig : sig (ktype l.dir k) u ≠ 0) :
    e3 (optN Q R l s i t k cx cy) (u * R) / fval (ktype l.dir k) R (u * R)
      = sv i - (s : ℝ) * Q * Gv Q k (lpx l t) (lpy l t) ((cx : ℝ) / Q, (cy : ℝ) / Q) u /
          sig (ktype l.dir k) u := by
  have hQr : (Q : ℝ) ≠ 0 := by exact_mod_cast hQ.ne'
  have hRr : (R : ℝ) ≠ 0 := by exact_mod_cast hR.ne'
  have hf := ktype_cases l.dir k
  have hG := gq_eval Q R k (lpx l t, cx) (lpy l t, cy) hQ hR (u * R)
  have huR : u * R / R = u := by field_simp
  rw [huR] at hG
  have hs := sigq_e3 R (ktype l.dir k) hf (u * R)
  have hfv := fval_sig (R := R) hf u
  have hGv : Gv Q k (lpx l t) (lpy l t) ((cx : ℝ) / Q, (cy : ℝ) / Q) u
      = gval (kf k) (sv (lpx l t, cx) / Q) (sv (lpy l t, cy) / Q) u := by
    simp only [Gv, sv_mk, sub_div]
  have e : e3 (optN Q R l s i t k cx cy) (u * R)
      = sv i * e3 (sigq R (ktype l.dir k)) (u * R)
        - s * (sv (gq Q R k (lpx l t, cx) (lpy l t, cy)).1
          + sv (gq Q R k (lpx l t, cx) (lpy l t, cy)).2.1 * (u * R)
          + sv (gq Q R k (lpx l t, cx) (lpy l t, cy)).2.2 * (u * R) ^ 2) := by
    simp only [optN, e3, sv_ssub, sv_smul, sv_sk]; ring
  rw [e, hs, hG, hfv, hGv]
  have hR2 : (R : ℝ) ^ 2 ≠ 0 := pow_ne_zero 2 hRr
  field_simp


/-- The value of an option triple `(type, N)` at `v`. -/
noncomputable def optval (R : ℕ) (t : ℕ × (SP × SP × SP)) (v : ℝ) : ℝ :=
  if t.1 = 0 then sv t.2.1 else e3 t.2 v / fval t.1 R v

lemma optT_type (Q R : ℕ) (l : LLine) (up : Bool) (cap o cx cy : ℕ) :
    (optT Q R l up cap o cx cy).1 = if o = 0 then 0 else ktype l.dir (o - 1) := by
  by_cases h : o = 0
  · subst h; simp [optT]
  · simp [optT, beq_ne h, h]

/-- The corner triple of an option has the option's value. -/
lemma optT_val {Q R : ℕ} (hQ : 0 < Q) (hR : 0 < R) (l : LLine) (up : Bool) (cap o cx cy : ℕ)
    (ho : o ≤ 4) (u : ℝ) (hsig : o ≠ 0 → sig (ktype l.dir (o - 1)) u ≠ 0) :
    optval R (optT Q R l up cap o cx cy) (u * R) = oval Q l up cap o ((cx : ℝ) / Q, (cy : ℝ) / Q) u := by
  by_cases h : o = 0
  · subst h; simp [optval, optT, oval, sv]
  · have ht : (optT Q R l up cap o cx cy).1 ≠ 0 := by
      rw [optT_type, if_neg h]
      rcases ktype_cases l.dir (o - 1) with h1 | h1 <;> omega
    simp only [optval, if_neg ht, oval, if_neg h]
    rw [optT_type, if_neg h]
    have hk : o - 1 < 4 := by omega
    cases up
    · simp only [optT, beq_ne h, cond_false, Bool.false_eq_true, if_false]
      exact optN_val hQ hR l l.sD l.iD l.b (o - 1) cx cy hk u (hsig h)
    · simp only [optT, beq_ne h, cond_false, cond_true, if_true]
      exact optN_val hQ hR l l.sU l.iU l.a (o - 1) cx cy hk u (hsig h)

/-- `a ⊆ f` for the types. -/
def tsub (a f : ℕ) : Prop := a = 0 ∨ a = f ∨ f = 3

lemma tor_le (a b : ℕ) (ha : a ≤ 3) (hb : b ≤ 3) : tor a b ≤ 3 := by
  unfold tor
  rcases Nat.eq_zero_or_pos a with rfl | h1
  · simpa using hb
  rcases Nat.eq_zero_or_pos b with rfl | h2
  · simp [beq_ne (Nat.pos_iff_ne_zero.mp h1)]; omega
  simp only [beq_ne (Nat.pos_iff_ne_zero.mp h1), beq_ne (Nat.pos_iff_ne_zero.mp h2), cond_false]
  by_cases h : a = b
  · subst h; simp [beq_rfl]; omega
  · simp [beq_ne h]

lemma tsub_tor_l (a b : ℕ) (ha : a ≤ 3) (hb : b ≤ 3) : tsub a (tor a b) := by
  unfold tsub tor
  rcases Nat.eq_zero_or_pos a with rfl | h1
  · exact Or.inl rfl
  rcases Nat.eq_zero_or_pos b with rfl | h2
  · simp [beq_ne (Nat.pos_iff_ne_zero.mp h1)]
  simp only [beq_ne (Nat.pos_iff_ne_zero.mp h1), beq_ne (Nat.pos_iff_ne_zero.mp h2), cond_false]
  by_cases h : a = b
  · subst h; simp [beq_rfl]
  · simp [beq_ne h]

lemma tsub_tor_r (a b : ℕ) (ha : a ≤ 3) (hb : b ≤ 3) : tsub b (tor a b) := by
  unfold tsub tor
  rcases Nat.eq_zero_or_pos b with rfl | h2
  · exact Or.inl rfl
  rcases Nat.eq_zero_or_pos a with rfl | h1
  · simp
  simp only [beq_ne (Nat.pos_iff_ne_zero.mp h1), beq_ne (Nat.pos_iff_ne_zero.mp h2), cond_false]
  by_cases h : a = b
  · subst h; simp [beq_rfl]
  · simp [beq_ne h]

lemma tsub_trans {a f g : ℕ} (h1 : tsub a f) (h2 : tsub f g) : tsub a g := by
  unfold tsub at *; omega

/-- The type conditions justifying a denominator. -/
def goodT (R U0 U1 f : ℕ) : Prop := f ≤ 3 ∧ (f % 2 = 1 → 0 < U0) ∧ (2 ≤ f → U1 < R)

lemma goodT_tor {R U0 U1 a b : ℕ} (ha : goodT R U0 U1 a) (hb : goodT R U0 U1 b) :
    goodT R U0 U1 (tor a b) := by
  obtain ⟨a3, a1, a2⟩ := ha
  obtain ⟨b3, b1, b2⟩ := hb
  refine ⟨tor_le a b a3 b3, ?_, ?_⟩ <;> unfold tor
  · rcases Nat.eq_zero_or_pos a with rfl | h1
    · simpa using b1
    rcases Nat.eq_zero_or_pos b with rfl | h2
    · simpa [beq_ne (Nat.pos_iff_ne_zero.mp h1)] using a1
    simp only [beq_ne (Nat.pos_iff_ne_zero.mp h1), beq_ne (Nat.pos_iff_ne_zero.mp h2), cond_false]
    by_cases h : a = b
    · subst h; simpa [beq_rfl] using a1
    · simp only [beq_ne h, cond_false]
      intro _
      rcases Nat.lt_or_ge a 2 with h' | h'
      · exact a1 (by omega)
      · rcases Nat.lt_or_ge b 2 with h'' | h''
        · exact b1 (by omega)
        · omega
  · rcases Nat.eq_zero_or_pos a with rfl | h1
    · simpa using b2
    rcases Nat.eq_zero_or_pos b with rfl | h2
    · simpa [beq_ne (Nat.pos_iff_ne_zero.mp h1)] using a2
    simp only [beq_ne (Nat.pos_iff_ne_zero.mp h1), beq_ne (Nat.pos_iff_ne_zero.mp h2), cond_false]
    by_cases h : a = b
    · subst h; simpa [beq_rfl] using a2
    · simp only [beq_ne h, cond_false]
      intro _
      rcases Nat.lt_or_ge a 2 with h' | h'
      · exact b2 (by omega)
      · exact a2 h'

lemma fval_pos_good {R U0 U1 f : ℕ} (hR : 0 < R) (hg : goodT R U0 U1 f) {v : ℝ}
    (hv0 : (U0 : ℝ) ≤ v) (hv1 : v ≤ U1) : 0 < fval f R v := by
  obtain ⟨h3, h1, h2⟩ := hg
  refine fval_pos hR h3 (fun h => lt_of_lt_of_le (by exact_mod_cast h1 h) hv0)
    (fun h => lt_of_le_of_lt hv1 (by exact_mod_cast h2 h)) (le_trans (Nat.cast_nonneg _) hv0)

lemma fval_split {R f a : ℕ} (hsub : tsub a f) (ha : a = 1 ∨ a = 2) (v : ℝ) :
    fval f R v = fval (f - a) R v * fval a R v := by
  unfold tsub at hsub
  rcases hsub with h | h | h
  · omega
  · subst h; simp [fval]
  · subst h; rcases ha with rfl | rfl <;> simp only [fval, show (3 : ℕ) - 1 = 2 from rfl,
      show (3 : ℕ) - 2 = 1 from rfl] <;> ring

/-- The term of an option in a sum over the common denominator `f`. -/
lemma e5_term {R f : ℕ} (t : ℕ × (SP × SP × SP)) (hf : f ≤ 3) (ht : t.1 = 0 ∨ t.1 = 1 ∨ t.1 = 2)
    (hsub : tsub t.1 f) (v : ℝ) (hne : t.1 ≠ 0 → fval t.1 R v ≠ 0) :
    e5 (term R f t) v = fval f R v * optval R t v := by
  unfold term optval
  simp only [nat_sub_eq]
  rcases ht with h0 | h12
  · rw [h0]; simp only [beq_rfl, cond_true, if_true]; exact e5_cmul f R hf _ v
  · have hne0 : t.1 ≠ 0 := by omega
    have hb : Nat.beq t.1 0 = false := beq_ne hne0
    rw [hb, cond_false, if_neg hne0, e5_tmul _ R (by unfold tsub at hsub; omega),
      fval_split hsub h12 v]
    have hfv := hne hne0
    field_simp
    simp only [e3]
    ring


/-! ### The corner inequalities -/

lemma isOpt_spec {l : LLine} {up : Bool} {o : ℕ} (h : isOpt l up o = true) :
    o ≤ 4 ∧ (o ≠ 0 → role l.roles (o - 1) = (if up then 1 else 2)) := by
  unfold isOpt at h
  simp only [Bool.or_eq_true, Bool.and_eq_true, Nat.beq_eq, Nat.ble_eq] at h
  rcases h with h | ⟨h1, h2⟩
  · subst h; exact ⟨by norm_num, fun h => absurd rfl h⟩
  · refine ⟨h1, fun _ => ?_⟩
    simp only [nat_sub_eq] at h2
    rw [h2]; cases up <;> rfl

lemma rolesOk_k {R U0 U1 dir roles k : ℕ} (h : rolesOk R U0 U1 dir roles = true) (hk : k < 4) :
    (role roles k = 0 ∨ role roles k = kend dir k) ∧
      (role roles k = 0 ∨ (ktype dir k = 1 → 0 < U0) ∧ (ktype dir k ≠ 1 → U1 < R)) := by
  unfold rolesOk at h
  have := List.all_eq_true.mp h k (List.mem_range.mpr hk)
  simp only [Bool.and_eq_true, Bool.or_eq_true, Nat.beq_eq] at this
  obtain ⟨h1, h2⟩ := this
  refine ⟨h1, ?_⟩
  rcases h2 with h2 | h2
  · exact Or.inl h2
  · right
    by_cases ht : ktype dir k = 1
    · have : Nat.beq (ktype dir k) 1 = true := by rw [ht]; rfl
      rw [this, cond_true, Nat.blt_eq] at h2
      exact ⟨fun _ => h2, fun h => absurd ht h⟩
    · have : Nat.beq (ktype dir k) 1 = false := beq_ne ht
      rw [this, cond_false, Nat.blt_eq] at h2
      exact ⟨fun h => absurd h ht, fun _ => h2⟩

/-- The type of an option is justified by the roles. -/
lemma opt_good {Q R U0 U1 : ℕ} {l : LLine} {up : Bool} {cap o cx cy : ℕ}
    (hro : rolesOk R U0 U1 l.dir l.roles = true) (ho : isOpt l up o = true) :
    goodT R U0 U1 (optT Q R l up cap o cx cy).1 ∧
      ((optT Q R l up cap o cx cy).1 = 0 ∨ (optT Q R l up cap o cx cy).1 = 1 ∨
        (optT Q R l up cap o cx cy).1 = 2) := by
  obtain ⟨ho4, hrole⟩ := isOpt_spec ho
  rw [optT_type]
  by_cases h0 : o = 0
  · simp only [h0, if_true]
    exact ⟨⟨by norm_num, fun h => absurd h (by norm_num), fun h => absurd h (by norm_num)⟩, by simp⟩
  · simp only [h0, if_false]
    have hr := hrole h0
    obtain ⟨_, h2⟩ := rolesOk_k hro (show o - 1 < 4 by omega)
    have hne : role l.roles (o - 1) ≠ 0 := by rw [hr]; cases up <;> simp
    rcases h2 with h2 | ⟨hS, hC⟩
    · exact absurd h2 hne
    rcases ktype_cases l.dir (o - 1) with ht | ht
    · rw [ht]; exact ⟨⟨by norm_num, fun _ => hS ht, fun h => absurd h (by norm_num)⟩, Or.inr (Or.inl rfl)⟩
    · rw [ht]; exact ⟨⟨by norm_num, fun h => absurd h (by norm_num), fun _ => hC (by omega)⟩, Or.inr (Or.inr rfl)⟩

lemma sig_pos {R U0 U1 f : ℕ} (hR : 0 < R) (hg : goodT R U0 U1 f) (hf : f = 1 ∨ f = 2) {u : ℝ}
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) : 0 < sig f u := by
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  obtain ⟨_, h1, h2⟩ := hg
  rcases hf with rfl | rfl
  · simp only [sig, if_true]
    have := h1 (by norm_num)
    have : (0 : ℝ) < (U0 : ℝ) / R := div_pos (by exact_mod_cast this) hRr
    linarith
  · simp only [sig, show (2 : ℕ) ≠ 1 by norm_num, if_false]
    have := h2 le_rfl
    have hlt : (U1 : ℝ) / R < 1 := (div_lt_one hRr).mpr (by exact_mod_cast this)
    have hu : 0 ≤ u := le_trans (div_nonneg (Nat.cast_nonneg _) hRr.le) hu0
    nlinarith

/-- The value of an option at a corner, from its triple, on the bin. -/
lemma optval_oval {Q R U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) {l : LLine} {up : Bool}
    {cap o cx cy : ℕ} (hro : rolesOk R U0 U1 l.dir l.roles = true) (ho : isOpt l up o = true)
    {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    optval R (optT Q R l up cap o cx cy) (u * R) = oval Q l up cap o ((cx : ℝ) / Q, (cy : ℝ) / Q) u := by
  obtain ⟨ho4, _⟩ := isOpt_spec ho
  refine optT_val hQ hR l up cap o cx cy ho4 u fun h0 => ?_
  obtain ⟨hg, _⟩ := opt_good (Q := Q) (cap := cap) (cx := cx) (cy := cy) hro ho
  rw [optT_type, if_neg h0] at hg
  exact (sig_pos hR hg (ktype_cases _ _) hu0 hu1).ne'

lemma v_range {R U0 U1 : ℕ} (hR : 0 < R) {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    (U0 : ℝ) ≤ u * R ∧ u * R ≤ U1 := by
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  exact ⟨by rw [div_le_iff₀ hRr] at hu0; linarith, by rw [le_div_iff₀ hRr] at hu1; linarith⟩

lemma fval_ne_of_good {R U0 U1 f : ℕ} (hR : 0 < R) (hg : goodT R U0 U1 f) {u : ℝ}
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) : fval f R (u * R) ≠ 0 := by
  obtain ⟨v0, v1⟩ := v_range hR hu0 hu1
  exact (fval_pos_good hR hg v0 v1).ne'

/-- **A slack check**, read back: at the corner, `chosen − other ≤ σ` on the bin. -/
lemma slack_fact {Q R U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU01 : U0 ≤ U1) {l : LLine}
    {up : Bool} {cap ch σ cx cy o : ℕ} (hro : rolesOk R U0 U1 l.dir l.roles = true)
    (hch : isOpt l up ch = true) (ho : isOpt l up o = true)
    (h : slackOk Q R U0 U1 l up cap ch σ cx cy o = true) {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u)
    (hu1 : u ≤ (U1 : ℝ) / R) :
    oval Q l up cap ch ((cx : ℝ) / Q, (cy : ℝ) / Q) u - oval Q l up cap o ((cx : ℝ) / Q, (cy : ℝ) / Q) u
      ≤ σ := by
  obtain ⟨v0, v1⟩ := v_range hR hu0 hu1
  unfold slackOk at h
  have hb := bOk5_e5 h hU01 v0 v1
  obtain ⟨g1, t1⟩ := opt_good (Q := Q) (cap := cap) (cx := cx) (cy := cy) hro hch
  obtain ⟨g2, t2⟩ := opt_good (Q := Q) (cap := cap) (cx := cx) (cy := cy) hro ho
  set T1 := optT Q R l up cap ch cx cy
  set T2 := optT Q R l up cap o cx cy
  set f := tor T1.1 T2.1
  have hg : goodT R U0 U1 f := goodT_tor g1 g2
  have hf3 : f ≤ 3 := hg.1
  have e1 := e5_term (R := R) T1 hf3 t1 (tsub_tor_l _ _ g1.1 g2.1) (u * R)
    (fun _ => fval_ne_of_good hR g1 hu0 hu1)
  have e2 := e5_term (R := R) T2 hf3 t2 (tsub_tor_r _ _ g1.1 g2.1) (u * R)
    (fun _ => fval_ne_of_good hR g2 hu0 hu1)
  simp only [e5_add, e5_neg] at hb
  rw [e1, e2, e5_cmul f R hf3] at hb
  rw [optval_oval hQ hR hro hch hu0 hu1, optval_oval hQ hR hro ho hu0 hu1] at hb
  have hpos := fval_pos_good hR hg v0 v1
  simp only [sv_mk, Nat.cast_zero, sub_zero] at hb
  by_contra hc
  push Not at hc
  have := mul_pos hpos (sub_pos.mpr hc)
  linarith

/-- The sum of the chosen terms. -/
lemma mainP_e5 {Q R S U0 U1 f : ℕ} (hQ : 0 < Q) (hR : 0 < R) (cls : List (SegE × ℕ)) (cx cy : ℕ)
    {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) (hf3 : f ≤ 3) :
    ∀ lc : List (LLine × (ℕ × ℕ × ℕ × ℕ)),
      (∀ x ∈ lc, rolesOk R U0 U1 x.1.dir x.1.roles = true ∧ isOpt x.1 true x.2.1 = true ∧
        isOpt x.1 false x.2.2.2.1 = true ∧
        tsub (optT Q R x.1 true (capU S Q cls x.1) x.2.1 cx cy).1 f ∧
        tsub (optT Q R x.1 false (capD S Q cls x.1) x.2.2.2.1 cx cy).1 f) →
      e5 (mainP Q R S f cls cx cy lc).1 (u * R)
        = fval f R (u * R) * (lc.map fun x =>
            oval Q x.1 true (capU S Q cls x.1) x.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u +
            oval Q x.1 false (capD S Q cls x.1) x.2.2.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u).sum ∧
      (mainP Q R S f cls cx cy lc).2 = (lc.map fun x => x.2.2.1 + x.2.2.2.2).sum
  | [], _ => by simp [mainP, e5, z0, sv]
  | x :: t, h => by
    obtain ⟨hro, hU, hD, sU, sD⟩ := h x List.mem_cons_self
    obtain ⟨ih1, ih2⟩ := mainP_e5 hQ hR cls cx cy hu0 hu1 hf3 t
      (fun y hy => h y (List.mem_cons_of_mem _ hy))
    obtain ⟨gU, tU⟩ := opt_good (Q := Q) (cap := capU S Q cls x.1) (cx := cx) (cy := cy) hro hU
    obtain ⟨gD, tD⟩ := opt_good (Q := Q) (cap := capD S Q cls x.1) (cx := cx) (cy := cy) hro hD
    obtain ⟨l, c⟩ := x
    simp only [mainP, e5_add, List.map_cons, List.sum_cons, nat_add_eq] at ih1 ih2 ⊢
    refine ⟨?_, by rw [ih2]⟩
    rw [ih1, e5_term _ hf3 tU sU (u * R) (fun _ => fval_ne_of_good hR gU hu0 hu1),
      e5_term _ hf3 tD sD (u * R) (fun _ => fval_ne_of_good hR gD hu0 hu1),
      optval_oval hQ hR hro hU hu0 hu1, optval_oval hQ hR hro hD hu0 hu1]
    ring

lemma tsub_mainF {Q R S : ℕ} (cls : List (SegE × ℕ)) (cx cy : ℕ) {U0 U1 : ℕ} :
    ∀ lc : List (LLine × (ℕ × ℕ × ℕ × ℕ)),
      (∀ x ∈ lc, rolesOk R U0 U1 x.1.dir x.1.roles = true ∧ isOpt x.1 true x.2.1 = true ∧
        isOpt x.1 false x.2.2.2.1 = true) →
      goodT R U0 U1 (mainF Q R S cls cx cy lc) ∧
      ∀ x ∈ lc, tsub (optT Q R x.1 true (capU S Q cls x.1) x.2.1 cx cy).1 (mainF Q R S cls cx cy lc) ∧
        tsub (optT Q R x.1 false (capD S Q cls x.1) x.2.2.2.1 cx cy).1 (mainF Q R S cls cx cy lc)
  | [], _ => ⟨⟨by simp [mainF], by simp [mainF], by simp [mainF]⟩, by simp⟩
  | x :: t, h => by
    obtain ⟨hro, hU, hD⟩ := h x List.mem_cons_self
    obtain ⟨ihg, ihs⟩ := tsub_mainF cls cx cy t (fun y hy => h y (List.mem_cons_of_mem _ hy))
    obtain ⟨gU, _⟩ := opt_good (Q := Q) (cap := capU S Q cls x.1) (cx := cx) (cy := cy) hro hU
    obtain ⟨gD, _⟩ := opt_good (Q := Q) (cap := capD S Q cls x.1) (cx := cx) (cy := cy) hro hD
    have g12 := goodT_tor gU gD
    have gall := goodT_tor g12 ihg
    refine ⟨by simp only [mainF]; exact gall, fun y hy => ?_⟩
    simp only [mainF]
    have k1 := tsub_tor_l _ _ g12.1 ihg.1
    have k2 := tsub_tor_r _ _ g12.1 ihg.1
    rcases List.mem_cons.mp hy with rfl | hy
    · exact ⟨tsub_trans (tsub_tor_l _ _ gU.1 gD.1) k1, tsub_trans (tsub_tor_r _ _ gU.1 gD.1) k1⟩
    · obtain ⟨a1, a2⟩ := ihs y hy
      exact ⟨tsub_trans a1 k2, tsub_trans a2 k2⟩

/-- **The main check**, read back: at the corner, `Σ (chosen − σ) ≥ lg` on the bin. -/
lemma main_fact {Q R S U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU01 : U0 ≤ U1)
    (cls : List (SegE × ℕ)) {lg cx cy : ℕ} {lc : List (LLine × (ℕ × ℕ × ℕ × ℕ))}
    (hl : ∀ x ∈ lc, rolesOk R U0 U1 x.1.dir x.1.roles = true ∧ isOpt x.1 true x.2.1 = true ∧
        isOpt x.1 false x.2.2.2.1 = true)
    (h : bOk5 (p5neg (p5add (mainP Q R S (mainF Q R S cls cx cy lc) cls cx cy lc).1
      (p5neg (cmul (mainF Q R S cls cx cy lc) R
        (Nat.add (mainP Q R S (mainF Q R S cls cx cy lc) cls cx cy lc).2 lg, 0))))) U0 U1 = true)
    {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    (lg : ℝ) ≤ (lc.map fun x =>
        (oval Q x.1 true (capU S Q cls x.1) x.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u - x.2.2.1) +
        (oval Q x.1 false (capD S Q cls x.1) x.2.2.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u - x.2.2.2.2)).sum := by
  obtain ⟨v0, v1⟩ := v_range hR hu0 hu1
  have hb := bOk5_e5 h hU01 v0 v1
  obtain ⟨hg, hsub⟩ := tsub_mainF (Q := Q) (S := S) cls cx cy lc hl
  set f := mainF Q R S cls cx cy lc
  obtain ⟨e1, e2⟩ := mainP_e5 (S := S) hQ hR cls cx cy hu0 hu1 hg.1 lc
    (fun x hx => ⟨(hl x hx).1, (hl x hx).2.1, (hl x hx).2.2, (hsub x hx).1, (hsub x hx).2⟩)
  simp only [e5_neg, e5_add] at hb
  rw [e1, e5_cmul f R hg.1, e2] at hb
  have hpos := fval_pos_good hR hg v0 v1
  have hs : ∀ M : List (LLine × (ℕ × ℕ × ℕ × ℕ)),
      (((M.map fun x => x.2.2.1 + x.2.2.2.2).sum : ℕ) : ℝ)
        = (M.map fun x => ((x.2.2.1 : ℝ) + x.2.2.2.2)).sum := by
    intro M
    induction M with
    | nil => simp
    | cons a M ih => simp only [List.map_cons, List.sum_cons, Nat.cast_add, ih]
  simp only [sv_mk, Nat.cast_zero, sub_zero, nat_add_eq, Nat.cast_add] at hb
  rw [hs] at hb
  have key : (lg : ℝ) ≤ (lc.map fun x =>
      oval Q x.1 true (capU S Q cls x.1) x.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u +
      oval Q x.1 false (capD S Q cls x.1) x.2.2.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u).sum
      - (lc.map fun x => ((x.2.2.1 : ℝ) + x.2.2.2.2)).sum := by
    by_contra hc
    push Not at hc
    have := mul_pos hpos (sub_pos.mpr hc)
    linarith
  have e3' : ∀ M : List (LLine × (ℕ × ℕ × ℕ × ℕ)), (M.map fun x =>
      (oval Q x.1 true (capU S Q cls x.1) x.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u - x.2.2.1) +
      (oval Q x.1 false (capD S Q cls x.1) x.2.2.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u - x.2.2.2.2)).sum
      = (M.map fun x =>
      oval Q x.1 true (capU S Q cls x.1) x.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u +
      oval Q x.1 false (capD S Q cls x.1) x.2.2.2.1 ((cx : ℝ) / Q, (cy : ℝ) / Q) u).sum
      - (M.map fun x => ((x.2.2.1 : ℝ) + x.2.2.2.2)).sum := by
    intro M
    induction M with
    | nil => simp
    | cons a M ih => simp only [List.map_cons, List.sum_cons, ih]; ring
  rw [e3']
  exact key

/-! ## 2.  The lower bound `Φ` and its concavity -/

/-- The options of an end. -/
def opts (l : LLine) (up : Bool) : List ℕ := (List.range 5).filter fun o => isOpt l up o

lemma zero_mem_opts (l : LLine) (up : Bool) : 0 ∈ opts l up := by
  simp [opts, isOpt]

lemma mem_opts {l : LLine} {up : Bool} {o : ℕ} (h : o ∈ opts l up) : isOpt l up o = true := by
  simp only [opts, List.mem_filter] at h; exact h.2

/-- The end's minimum over its options. -/
noncomputable def emin (Q : ℕ) (l : LLine) (up : Bool) (cap : ℕ) (c : ℝ × ℝ) (u : ℝ) : ℝ :=
  (opts l up).foldr (fun o m => min (oval Q l up cap o c u) m) (cap : ℝ)

lemma le_foldr_min (f : ℕ → ℝ) (X m0 : ℝ) : ∀ L : List ℕ, (∀ o ∈ L, X ≤ f o) → X ≤ m0 →
    X ≤ L.foldr (fun o m => min (f o) m) m0
  | [], _, h => h
  | o :: L, h, h0 => by
    simp only [List.foldr_cons]
    exact le_min (h o List.mem_cons_self) (le_foldr_min f X m0 L
      (fun o' ho' => h o' (List.mem_cons_of_mem _ ho')) h0)

/-- `Φ`: the sum over the lines of the two ends' minima. -/
noncomputable def Phi (Q S : ℕ) (cls : List (SegE × ℕ)) (ls : List LLine) (c : ℝ × ℝ) (u : ℝ) : ℝ :=
  (ls.map fun l => emin Q l true (capU S Q cls l) c u + emin Q l false (capD S Q cls l) c u).sum

/-- The end's minimum is at least the chosen option minus the slack. -/
lemma emin_ge {Q R U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU01 : U0 ≤ U1) {l : LLine} {up : Bool}
    {cap ch σ cx cy : ℕ} (hro : rolesOk R U0 U1 l.dir l.roles = true)
    (h : endOk Q R U0 U1 l up cap ch σ cx cy = true) {u : ℝ} (hu0 : (U0 : ℝ) / R ≤ u)
    (hu1 : u ≤ (U1 : ℝ) / R) :
    oval Q l up cap ch ((cx : ℝ) / Q, (cy : ℝ) / Q) u - σ ≤ emin Q l up cap ((cx : ℝ) / Q, (cy : ℝ) / Q) u := by
  simp only [endOk, Bool.and_eq_true, List.all_eq_true, Bool.or_eq_true, Bool.not_eq_true'] at h
  obtain ⟨hch, hall⟩ := h
  have hs : ∀ o, isOpt l up o = true →
      oval Q l up cap ch ((cx : ℝ) / Q, (cy : ℝ) / Q) u - oval Q l up cap o ((cx : ℝ) / Q, (cy : ℝ) / Q) u ≤ σ := by
    intro o ho
    obtain ⟨ho4, _⟩ := isOpt_spec ho
    rcases hall o (List.mem_range.mpr (by omega)) with h1 | h1
    · rw [ho] at h1; exact absurd h1 (by decide)
    · exact slack_fact hQ hR hU01 hro hch ho h1 hu0 hu1
  refine le_foldr_min _ _ _ _ (fun o ho => by linarith [hs o (mem_opts ho)]) ?_
  have h0 := hs 0 (by simp [isOpt])
  have e0 : oval Q l up cap 0 ((cx : ℝ) / Q, (cy : ℝ) / Q) u = cap := by simp [oval]
  linarith

/-- An option is affine in the centre. -/
lemma oval_affine (Q : ℕ) (l : LLine) (up : Bool) (cap o : ℕ) (u : ℝ) :
    ∃ K A B : ℝ, ∀ c : ℝ × ℝ, oval Q l up cap o c u = K + A * c.1 + B * c.2 := by
  by_cases h : o = 0
  · exact ⟨cap, 0, 0, fun c => by simp [oval, h]⟩
  set X := lpx l (if up then l.a else l.b)
  set Y := lpy l (if up then l.a else l.b)
  set i := sv (if up then l.iU else l.iD)
  set s := ((if up then l.sU else l.sD : ℕ) : ℝ)
  set sg := sig (ktype l.dir (o - 1)) u
  set k := kf (o - 1)
  refine ⟨i - s * Q * (-(1 + u ^ 2) + galpha k u * ((X : ℝ) / Q) + gbeta k u * ((Y : ℝ) / Q)) / sg,
    s * Q * galpha k u / sg, s * Q * gbeta k u / sg, fun c => ?_⟩
  simp only [oval, if_neg h, Gv, gval_eq]
  ring

/-- Concavity in each coordinate, in the convex-combination form. -/
def ConcXY (f : ℝ → ℝ → ℝ) : Prop :=
  (∀ y x0 x1 t, 0 ≤ t → t ≤ 1 → t * f x0 y + (1 - t) * f x1 y ≤ f (t * x0 + (1 - t) * x1) y) ∧
  (∀ x y0 y1 t, 0 ≤ t → t ≤ 1 → t * f x y0 + (1 - t) * f x y1 ≤ f x (t * y0 + (1 - t) * y1))

lemma concXY_affine (K A B : ℝ) : ConcXY fun x y => K + A * x + B * y :=
  ⟨fun y x0 x1 t _ _ => le_of_eq (by ring), fun x y0 y1 t _ _ => le_of_eq (by ring)⟩

lemma concXY_min {f g : ℝ → ℝ → ℝ} (hf : ConcXY f) (hg : ConcXY g) :
    ConcXY fun x y => min (f x y) (g x y) := by
  constructor
  · intro y x0 x1 t h0 h1
    refine le_min ?_ ?_
    · have := hf.1 y x0 x1 t h0 h1
      nlinarith [min_le_left (f x0 y) (g x0 y), min_le_left (f x1 y) (g x1 y),
        mul_le_mul_of_nonneg_left (min_le_left (f x0 y) (g x0 y)) h0,
        mul_le_mul_of_nonneg_left (min_le_left (f x1 y) (g x1 y)) (by linarith : (0 : ℝ) ≤ 1 - t)]
    · have := hg.1 y x0 x1 t h0 h1
      nlinarith [mul_le_mul_of_nonneg_left (min_le_right (f x0 y) (g x0 y)) h0,
        mul_le_mul_of_nonneg_left (min_le_right (f x1 y) (g x1 y)) (by linarith : (0 : ℝ) ≤ 1 - t)]
  · intro x y0 y1 t h0 h1
    refine le_min ?_ ?_
    · have := hf.2 x y0 y1 t h0 h1
      nlinarith [mul_le_mul_of_nonneg_left (min_le_left (f x y0) (g x y0)) h0,
        mul_le_mul_of_nonneg_left (min_le_left (f x y1) (g x y1)) (by linarith : (0 : ℝ) ≤ 1 - t)]
    · have := hg.2 x y0 y1 t h0 h1
      nlinarith [mul_le_mul_of_nonneg_left (min_le_right (f x y0) (g x y0)) h0,
        mul_le_mul_of_nonneg_left (min_le_right (f x y1) (g x y1)) (by linarith : (0 : ℝ) ≤ 1 - t)]

lemma concXY_add {f g : ℝ → ℝ → ℝ} (hf : ConcXY f) (hg : ConcXY g) :
    ConcXY fun x y => f x y + g x y := by
  constructor
  · intro y x0 x1 t h0 h1; have := hf.1 y x0 x1 t h0 h1; have := hg.1 y x0 x1 t h0 h1; linarith
  · intro x y0 y1 t h0 h1; have := hf.2 x y0 y1 t h0 h1; have := hg.2 x y0 y1 t h0 h1; linarith

lemma concXY_emin (Q : ℕ) (l : LLine) (up : Bool) (cap : ℕ) (u : ℝ) :
    ConcXY fun x y => emin Q l up cap (x, y) u := by
  unfold emin
  induction opts l up with
  | nil => exact concXY_affine cap 0 0 |>.imp (fun h y x0 x1 t h0 h1 => by
      have := h y x0 x1 t h0 h1; simpa using this) (fun h x y0 y1 t h0 h1 => by
      have := h x y0 y1 t h0 h1; simpa using this)
  | cons o L ih =>
    obtain ⟨K, A, B, hf⟩ := oval_affine Q l up cap o u
    have ha : ConcXY fun x y => oval Q l up cap o (x, y) u := by
      have := concXY_affine K A B
      simpa only [hf] using this
    simpa only [List.foldr_cons] using concXY_min ha ih

lemma concXY_Phi (Q S : ℕ) (cls : List (SegE × ℕ)) (ls : List LLine) (u : ℝ) :
    ConcXY fun x y => Phi Q S cls ls (x, y) u := by
  unfold Phi
  induction ls with
  | nil => simpa using concXY_affine 0 0 0
  | cons l ls ih =>
    simp only [List.map_cons, List.sum_cons]
    exact concXY_add (concXY_add (concXY_emin Q l true _ u) (concXY_emin Q l false _ u)) ih

lemma concXY_interval {f : ℝ → ℝ → ℝ} (hf : ConcXY f) :
    (∀ y x0 x1 x, x0 ≤ x → x ≤ x1 → min (f x0 y) (f x1 y) ≤ f x y) ∧
    (∀ x y0 y1 y, y0 ≤ y → y ≤ y1 → min (f x y0) (f x y1) ≤ f x y) := by
  constructor
  · intro y x0 x1 x hx0 hx1
    rcases eq_or_lt_of_le (le_trans hx0 hx1) with h | h
    · have : x = x0 := by linarith
      rw [this]; exact min_le_left _ _
    set t := (x1 - x) / (x1 - x0)
    have hd : 0 < x1 - x0 := by linarith
    have t0 : 0 ≤ t := div_nonneg (by linarith) hd.le
    have t1 : t ≤ 1 := by rw [div_le_one hd]; linarith
    have hx : t * x0 + (1 - t) * x1 = x := by simp only [t]; field_simp; ring
    have := hf.1 y x0 x1 t t0 t1
    rw [hx] at this
    nlinarith [min_le_left (f x0 y) (f x1 y), min_le_right (f x0 y) (f x1 y),
      mul_le_mul_of_nonneg_left (min_le_left (f x0 y) (f x1 y)) t0,
      mul_le_mul_of_nonneg_left (min_le_right (f x0 y) (f x1 y)) (by linarith : (0 : ℝ) ≤ 1 - t)]
  · intro x y0 y1 y hy0 hy1
    rcases eq_or_lt_of_le (le_trans hy0 hy1) with h | h
    · have : y = y0 := by linarith
      rw [this]; exact min_le_left _ _
    set t := (y1 - y) / (y1 - y0)
    have hd : 0 < y1 - y0 := by linarith
    have t0 : 0 ≤ t := div_nonneg (by linarith) hd.le
    have t1 : t ≤ 1 := by rw [div_le_one hd]; linarith
    have hy : t * y0 + (1 - t) * y1 = y := by simp only [t]; field_simp; ring
    have := hf.2 x y0 y1 t t0 t1
    rw [hy] at this
    nlinarith [mul_le_mul_of_nonneg_left (min_le_left (f x y0) (f x y1)) t0,
      mul_le_mul_of_nonneg_left (min_le_right (f x y0) (f x y1)) (by linarith : (0 : ℝ) ≤ 1 - t)]

/-- `Φ` at a corner, from the corner check. -/
lemma Phi_corner {Q R S U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU01 : U0 ≤ U1)
    (cls : List (SegE × ℕ)) {lg cx cy : ℕ} {ls : List LLine} {ch : List (ℕ × ℕ × ℕ × ℕ)}
    (hlen : ch.length = ls.length) (hro : ∀ l ∈ ls, rolesOk R U0 U1 l.dir l.roles = true)
    (h : cornerOk Q R S U0 U1 cls lg cx cy (ls.zip ch) = true) {u : ℝ}
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    (lg : ℝ) ≤ Phi Q S cls ls ((cx : ℝ) / Q, (cy : ℝ) / Q) u := by
  simp only [cornerOk, Bool.and_eq_true, List.all_eq_true] at h
  obtain ⟨hends, hmain⟩ := h
  have hmem : ∀ x ∈ ls.zip ch, x.1 ∈ ls := fun x hx => (List.of_mem_zip hx).1
  have hl : ∀ x ∈ ls.zip ch, rolesOk R U0 U1 x.1.dir x.1.roles = true ∧ isOpt x.1 true x.2.1 = true ∧
      isOpt x.1 false x.2.2.2.1 = true := by
    intro x hx
    have he := hends x hx
    simp only [endOk, Bool.and_eq_true] at he
    exact ⟨hro x.1 (hmem x hx), he.1.1, he.2.1⟩
  have hm := main_fact hQ hR hU01 cls hl hmain hu0 hu1
  refine le_trans hm (le_of_eq_of_le rfl ?_)
  -- termwise, over the zipped list, whose first components are the lines
  have hz : (ls.zip ch).map Prod.fst = ls := List.map_fst_zip (by omega)
  unfold Phi
  conv_rhs => rw [← hz, List.map_map]
  apply List.sum_le_sum
  intro x hx
  have he := hends x hx
  try simp only [Bool.and_eq_true] at he
  have a := emin_ge hQ hR hU01 (hro x.1 (hmem x hx)) he.1 hu0 hu1
  have b := emin_ge hQ hR hU01 (hro x.1 (hmem x hx)) he.2 hu0 hu1
  simp only [Function.comp]
  linarith

/-- **`Φ ≥ lg` on the box**: concavity from the four corners. -/
lemma Phi_box {D S R x0 x1 y0 y1 U0 U1 : ℕ} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    {c : ℝ × ℝ} {u : ℝ} (P : Pose S (D * S) R x0 x1 y0 y1 U0 U1 c u) (cls : List (SegE × ℕ))
    {B : LBlk} (hlen : B.corners.length = 4) (hlen' : ∀ ch ∈ B.corners, ch.length = B.lines.length)
    (hro : ∀ l ∈ B.lines, rolesOk R U0 U1 l.dir l.roles = true)
    (h00 : cornerOk (D * S) R S U0 U1 cls B.lg x0 y0 (B.lines.zip (B.corners.getD 0 [])) = true)
    (h01 : cornerOk (D * S) R S U0 U1 cls B.lg x0 y1 (B.lines.zip (B.corners.getD 1 [])) = true)
    (h10 : cornerOk (D * S) R S U0 U1 cls B.lg x1 y0 (B.lines.zip (B.corners.getD 2 [])) = true)
    (h11 : cornerOk (D * S) R S U0 U1 cls B.lg x1 y1 (B.lines.zip (B.corners.getD 3 [])) = true) :
    (B.lg : ℝ) ≤ Phi (D * S) S cls B.lines c u := by
  have hQ : 0 < D * S := Nat.mul_pos hD hS
  have gl : ∀ j < 4, (B.corners.getD j []).length = B.lines.length := by
    intro j hj
    rw [List.getD_eq_getElem _ _ (by omega)]
    exact hlen' _ (List.getElem_mem _)
  have hc := concXY_interval (concXY_Phi (D * S) S cls B.lines u)
  have key := concave_corners (f := fun x y => Phi (D * S) S cls B.lines (x, y) u)
    (x0 := (x0 : ℝ) / (D * S : ℕ)) (x1 := (x1 : ℝ) / (D * S : ℕ)) (y0 := (y0 : ℝ) / (D * S : ℕ))
    (y1 := (y1 : ℝ) / (D * S : ℕ)) (x := c.1) (y := c.2)
    (fun y' x' h1 h2 => hc.1 y' _ _ x' h1 h2) (fun x' y' h1 h2 => hc.2 x' _ _ y' h1 h2)
    P.hx0 P.hx1 P.hy0 P.hy1
    (Phi_corner hQ hR P.hU01 cls (gl 0 (by norm_num)) hro h00 P.hu0 P.hu1)
    (Phi_corner hQ hR P.hU01 cls (gl 1 (by norm_num)) hro h01 P.hu0 P.hu1)
    (Phi_corner hQ hR P.hU01 cls (gl 2 (by norm_num)) hro h10 P.hu0 P.hu1)
    (Phi_corner hQ hR P.hU01 cls (gl 3 (by norm_num)) hro h11 P.hu0 P.hu1)
  exact key

/-! ## 3.  The chord of a line, and the gains -/

/-- The gain check, read back: `s X + i ≤ C + Σ r · clamp(X − o₀, 0, o₁ − o₀)` for `X ≤ D`. -/
lemma gain_lb (s : ℕ) (i : SP) (D : ℕ) : ∀ (C : ℕ) (L : List (ℕ × ℕ × ℕ)), gainOk s i D C L = true →
    (∀ p ∈ L, p.2.1 ≤ p.2.2) → ∀ X : ℝ, X ≤ D →
      (s : ℝ) * X + sv i ≤ C + (L.map fun p => (p.1 : ℝ) *
        max 0 (min (X - p.2.1) ((p.2.2 : ℝ) - p.2.1))).sum
  | C, [], h, _, X, hX => by
    simp only [gainOk, ellLe, sle0_iff, sv_ssub, sv_sadd, sv_mk, nat_mul_eq, Nat.cast_mul,
      Nat.cast_zero, sub_zero] at h
    simp only [List.map_nil, List.sum_nil, add_zero]
    have : (s : ℝ) * X ≤ s * D := mul_le_mul_of_nonneg_left hX (Nat.cast_nonneg _)
    linarith
  | C, (r, o0, o1) :: t, h, hle, X, hX => by
    simp only [gainOk, Bool.and_eq_true, ellLe, sle0_iff, sv_ssub, sv_sadd, sv_mk, nat_mul_eq,
      nat_add_eq, nat_sub_eq, Nat.cast_mul, Nat.cast_add, Nat.cast_zero, sub_zero] at h
    obtain ⟨⟨h0, h1⟩, ht⟩ := h
    have ho : o0 ≤ o1 := hle _ List.mem_cons_self
    rw [Nat.cast_sub ho] at h1
    replace h0 : (s : ℝ) * o0 + sv i ≤ C := by linarith
    replace h1 : (s : ℝ) * o1 + sv i ≤ C + r * (o1 - o0) := by linarith
    have ih := gain_lb s i D (C + r * (o1 - o0)) t ht (fun p hp => hle p (List.mem_cons_of_mem _ hp)) X hX
    have hnn : ∀ M : List (ℕ × ℕ × ℕ), 0 ≤ (M.map fun p => (p.1 : ℝ) *
        max 0 (min (X - p.2.1) ((p.2.2 : ℝ) - p.2.1))).sum := by
      intro M
      exact List.sum_nonneg fun x hx => by
        obtain ⟨p, _, rfl⟩ := List.mem_map.mp hx
        exact mul_nonneg (Nat.cast_nonneg _) (le_max_left _ _)
    have hs0 : (0 : ℝ) ≤ s := Nat.cast_nonneg _
    have hr0 : (0 : ℝ) ≤ r := Nat.cast_nonneg _
    simp only [List.map_cons, List.sum_cons]
    have hor : (o0 : ℝ) ≤ o1 := by exact_mod_cast ho
    rcases le_total X o0 with hx | hx
    · -- before the piece
      have : (s : ℝ) * X ≤ s * o0 := mul_le_mul_of_nonneg_left hx hs0
      have := hnn t
      have : 0 ≤ (r : ℝ) * max 0 (min (X - o0) ((o1 : ℝ) - o0)) :=
        mul_nonneg hr0 (le_max_left _ _)
      linarith
    rcases le_total X o1 with hx' | hx'
    · -- inside the piece
      have hc : max 0 (min (X - o0) ((o1 : ℝ) - o0)) = X - o0 := by
        rw [min_eq_left (by linarith), max_eq_right (by linarith)]
      rw [hc]
      have := hnn t
      rcases eq_or_lt_of_le hor with he | hlt
      · have : X = o0 := by linarith
        subst this
        linarith
      · have hd : (0 : ℝ) < o1 - o0 := by linarith
        -- interpolation
        have key : ((s : ℝ) * X + sv i) * (o1 - o0)
            = ((s : ℝ) * o0 + sv i) * (o1 - X) + ((s : ℝ) * o1 + sv i) * (X - o0) := by ring
        have k1 : ((s : ℝ) * o0 + sv i) * (o1 - X) ≤ (C : ℝ) * (o1 - X) :=
          mul_le_mul_of_nonneg_right h0 (by linarith)
        have k2 : ((s : ℝ) * o1 + sv i) * (X - o0) ≤ ((C : ℝ) + r * (o1 - o0)) * (X - o0) :=
          mul_le_mul_of_nonneg_right h1 (by linarith)
        have : ((s : ℝ) * X + sv i) * (o1 - o0) ≤ ((C : ℝ) + r * (X - o0)) * (o1 - o0) := by
          nlinarith
        have := le_of_mul_le_mul_right this hd
        linarith
    · -- after the piece
      have hc : max 0 (min (X - o0) ((o1 : ℝ) - o0)) = o1 - o0 := by
        rw [min_eq_right (by linarith), max_eq_right (by linarith)]
      rw [hc]
      push_cast [Nat.cast_sub ho] at ih
      linarith

lemma gainSum_eq : ∀ (C : ℕ) (L : List (ℕ × ℕ × ℕ)),
    (gainSum C L : ℝ) = C + (L.map fun p => (p.1 : ℝ) * ((p.2.2 - p.2.1 : ℕ) : ℝ)).sum
  | C, [] => by simp [gainSum]
  | C, (r, o0, o1) :: t => by
    simp only [gainSum, nat_add_eq, nat_mul_eq, nat_sub_eq, List.map_cons, List.sum_cons]
    rw [gainSum_eq]; push_cast; ring

/-- The line coordinate's slope of a violation polynomial. -/
noncomputable def lslope (dir : ℕ) (k : Fin 4) (u : ℝ) : ℝ :=
  if dir = 0 then gbeta k u else galpha k u

/-- A violation polynomial along the line. -/
noncomputable def lgv (Q dir K : ℕ) (k : Fin 4) (c : ℝ × ℝ) (u t : ℝ) : ℝ :=
  gval k ((lpt Q dir K t).1 - c.1) ((lpt Q dir K t).2 - c.2) u

lemma lgv_affine (Q dir K : ℕ) (k : Fin 4) (c : ℝ × ℝ) (u t t0 : ℝ) :
    lgv Q dir K k c u t = lgv Q dir K k c u t0 + lslope dir k u * (t - t0) := by
  by_cases hd : dir = 0
  · simp only [lgv, lpt, hd, if_true, lslope, gval_eq]; ring
  · simp only [lgv, lpt, hd, if_false, lslope, gval_eq]; ring

/-- The slope of a typed condition: `+σ` at the up end, `−σ` at the down end. -/
lemma lslope_spec (dir k : ℕ) (hk : k < 4) (u : ℝ) :
    lslope dir (kf k) u = (if kend dir k = 1 then 1 else -1) * sig (ktype dir k) u := by
  by_cases hd : dir = 0
  · subst hd
    interval_cases k <;> simp (config := { decide := true }) [lslope, kend, ktype, kf, gbeta, sig] <;>
      ring
  · have hb : Nat.beq dir 0 = false := beq_ne hd
    interval_cases k <;> simp (config := { decide := true }) [lslope, kend, ktype, kf, galpha, sig, hd, hb] <;>
      ring

/-- The chord end's distance beyond the certified point, `−Q G_k(t)/σ_k` (over `Q`). -/
noncomputable def xk (Q : ℕ) (l : LLine) (t k : ℕ) (c : ℝ × ℝ) (u : ℝ) : ℝ :=
  -(Q : ℝ) * Gv Q k (lpx l t) (lpy l t) c u / sig (ktype l.dir k) u

def typedU (l : LLine) : List ℕ := (List.range 4).filter fun k => role l.roles k = 1
def typedD (l : LLine) : List ℕ := (List.range 4).filter fun k => role l.roles k = 2

/-- How far the up end moves: `min(Δ↑, min_k x_k)`. -/
noncomputable def Xup (Q : ℕ) (l : LLine) (c : ℝ × ℝ) (u : ℝ) : ℝ :=
  (typedU l).foldr (fun k m => min (xk Q l l.a k c u) m) (l.du : ℝ)
noncomputable def Ydn (Q : ℕ) (l : LLine) (c : ℝ × ℝ) (u : ℝ) : ℝ :=
  (typedD l).foldr (fun k m => min (xk Q l l.b k c u) m) (l.dd : ℝ)

lemma foldr_min_le (f : ℕ → ℝ) (d : ℝ) : ∀ L : List ℕ,
    L.foldr (fun k m => min (f k) m) d ≤ d ∧ ∀ k ∈ L, L.foldr (fun k m => min (f k) m) d ≤ f k
  | [] => ⟨le_rfl, by simp⟩
  | k :: L => by
    obtain ⟨h1, h2⟩ := foldr_min_le f d L
    simp only [List.foldr_cons]
    refine ⟨le_trans (min_le_right _ _) h1, fun j hj => ?_⟩
    rcases List.mem_cons.mp hj with rfl | hj
    · exact min_le_left _ _
    · exact le_trans (min_le_right _ _) (h2 j hj)

lemma foldr_min_mem (f : ℕ → ℝ) (d : ℝ) : ∀ L : List ℕ,
    L.foldr (fun k m => min (f k) m) d = d ∨ ∃ k ∈ L, L.foldr (fun k m => min (f k) m) d = f k
  | [] => Or.inl rfl
  | k :: L => by
    simp only [List.foldr_cons]
    rcases min_choice (f k) (L.foldr (fun k m => min (f k) m) d) with h | h <;> rw [h]
    · exact Or.inr ⟨k, List.mem_cons_self, rfl⟩
    · rcases foldr_min_mem f d L with h' | ⟨j, hj, h'⟩
      · exact Or.inl h'
      · exact Or.inr ⟨j, List.mem_cons_of_mem _ hj, h'⟩

lemma lcert_spec {Q R x0 x1 y0 y1 U0 U1 : ℕ} {l : LLine}
    (h : lcertOk Q R x0 x1 y0 y1 U0 U1 l = true) :
    l.b ≤ l.a ∧ l.dd ≤ l.b ∧ rolesOk R U0 U1 l.dir l.roles = true ∧
    ∀ k < 4, (role l.roles k = 1 → admK Q R x0 x1 y0 y1 U0 U1 (lpx l l.a) (lpy l l.a) k = true) ∧
      (role l.roles k = 2 → admK Q R x0 x1 y0 y1 U0 U1 (lpx l l.b) (lpy l l.b) k = true) ∧
      (role l.roles k ≠ 1 → role l.roles k ≠ 2 →
        admK Q R x0 x1 y0 y1 U0 U1 (lpx l (l.b - l.dd)) (lpy l (l.b - l.dd)) k = true ∧
        admK Q R x0 x1 y0 y1 U0 U1 (lpx l (l.a + l.du)) (lpy l (l.a + l.du)) k = true) := by
  simp only [lcertOk, Bool.and_eq_true, Nat.ble_eq, List.all_eq_true] at h
  obtain ⟨⟨⟨hba, hdd⟩, hro⟩, hall⟩ := h
  refine ⟨hba, hdd, hro, fun k hk => ⟨fun h1 => ?_, fun h2 => ?_, fun h1 h2 => ?_⟩⟩
  · have := hall k (List.mem_range.mpr hk)
    have hb : Nat.beq (role l.roles k) 1 = true := by rw [h1]; rfl
    simpa [hb] using this
  · have := hall k (List.mem_range.mpr hk)
    have hb1 : Nat.beq (role l.roles k) 1 = false := by rw [h2]; rfl
    have hb2 : Nat.beq (role l.roles k) 2 = true := by rw [h2]; rfl
    simpa [hb1, hb2] using this
  · have := hall k (List.mem_range.mpr hk)
    have hb1 : Nat.beq (role l.roles k) 1 = false := beq_ne h1
    have hb2 : Nat.beq (role l.roles k) 2 = false := beq_ne h2
    simp only [hb1, hb2, cond_false, Bool.and_eq_true, nat_sub_eq, nat_add_eq] at this
    exact this

lemma role_cases {R U0 U1 dir roles k : ℕ} (h : rolesOk R U0 U1 dir roles = true) (hk : k < 4) :
    role roles k = 0 ∨ (role roles k = 1 ∧ kend dir k = 1) ∨ (role roles k = 2 ∧ kend dir k = 2) := by
  obtain ⟨h1, _⟩ := rolesOk_k h hk
  have hke : kend dir k = 1 ∨ kend dir k = 2 := by
    unfold kend; cases Nat.beq dir 0 <;> cases Nat.beq (Nat.mod k 2) 0 <;>
      cases (Nat.beq k 0 || Nat.beq k 3) <;> simp
  rcases h1 with h1 | h1
  · exact Or.inl h1
  · rcases hke with h2 | h2 <;> rw [h2] at h1
    · exact Or.inr (Or.inl ⟨h1, h2⟩)
    · exact Or.inr (Or.inr ⟨h1, h2⟩)

/-- **The chord**: at every admissible pose, the line's points between `b − Y` and `a + X` are in the
square. -/
lemma chord {S Q R x0 x1 y0 y1 U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) {c : ℝ × ℝ} {u : ℝ}
    (P : Pose S Q R x0 x1 y0 y1 U0 U1 c u) {l : LLine}
    (h : lcertOk Q R x0 x1 y0 y1 U0 U1 l = true) {t : ℝ}
    (ht0 : ((l.b : ℝ) - Ydn Q l c u) / Q ≤ t) (ht1 : t ≤ ((l.a : ℝ) + Xup Q l c u) / Q) :
    lpt Q l.dir l.K t ∈ sq c (2 * Real.arctan u) 1 := by
  obtain ⟨hba, hdd, hro, hk⟩ := lcert_spec h
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  rw [mem_sq_iff_gval]
  intro k
  have hk4 := k.isLt
  obtain ⟨hup, hdn, hun⟩ := hk k.val hk4
  have A := fun (XS YS : ℕ) (hh : admK Q R x0 x1 y0 y1 U0 U1 XS YS k.val = true) =>
    admK_sound hQ hR P.hU01 P.hU1 hh P.hx0 P.hx1 P.hy0 P.hy1 P.hu0 P.hu1 P.hwx P.hwy
  have hXd := (foldr_min_le (fun k => xk Q l l.a k c u) (l.du : ℝ) (typedU l)).1
  have hYd := (foldr_min_le (fun k => xk Q l l.b k c u) (l.dd : ℝ) (typedD l)).1
  have hlp : ∀ (t0 : ℕ), Gv Q k.val (lpx l t0) (lpy l t0) c u = lgv Q l.dir l.K k c u ((t0 : ℝ) / Q) := by
    intro t0; simp only [lpx, lpy]; rw [Gv_lpt]; rfl
  change lgv Q l.dir l.K k c u t ≤ 0
  rcases role_cases hro hk4 with h0 | ⟨h1, he⟩ | ⟨h2, he⟩
  · -- untyped: certified on the whole range
    obtain ⟨a1, a2⟩ := hun (by omega) (by omega)
    have g1 := A _ _ a1
    have g2 := A _ _ a2
    rw [hlp] at g1 g2
    have hX : Xup Q l c u ≤ l.du := hXd
    have hY : Ydn Q l c u ≤ l.dd := hYd
    refine gval_lpt_between g1 g2 ?_ ?_
    · rw [Nat.cast_sub hdd]
      refine le_trans (div_le_div_of_nonneg_right (by linarith) hQr.le) ht0
    · push_cast
      exact le_trans ht1 (div_le_div_of_nonneg_right (by linarith) hQr.le)
  · -- typed up: below the threshold
    have g := A _ _ (hup h1)
    rw [hlp] at g
    have hsl := lslope_spec l.dir k.val hk4 u
    rw [kf_val, he, if_pos rfl, one_mul] at hsl
    obtain ⟨gk, _⟩ := opt_good (Q := Q) (up := true) (cap := 0) (o := k.val + 1) (cx := 0) (cy := 0) hro
      (by simp [isOpt, h1]; try omega)
    rw [optT_type, if_neg (by omega), show k.val + 1 - 1 = k.val by omega] at gk
    have hsp := sig_pos hR gk (ktype_cases _ _) P.hu0 P.hu1
    have hmem : k.val ∈ typedU l := by simp [typedU, h1, hk4]
    have hXk := (foldr_min_le (fun k => xk Q l l.a k c u) (l.du : ℝ) (typedU l)).2 k.val hmem
    change Xup Q l c u ≤ xk Q l l.a k.val c u at hXk
    simp only [xk] at hXk
    rw [hlp] at hXk
    rw [lgv_affine Q l.dir l.K k c u t ((l.a : ℝ) / Q), hsl]
    have e1 : t - (l.a : ℝ) / Q ≤ Xup Q l c u / Q := by
      have := ht1; rw [add_div] at this; linarith
    have e2 : Xup Q l c u / Q ≤ -(lgv Q l.dir l.K k c u ((l.a : ℝ) / Q)) / sig (ktype l.dir k.val) u := by
      rw [div_le_iff₀ hQr]
      have : -(Q : ℝ) * lgv Q l.dir l.K k c u ((l.a : ℝ) / Q) / sig (ktype l.dir k.val) u
          = -(lgv Q l.dir l.K k c u ((l.a : ℝ) / Q)) / sig (ktype l.dir k.val) u * Q := by ring
      rw [this] at hXk; exact hXk
    have e3 := le_trans e1 e2
    rw [le_div_iff₀ hsp] at e3
    nlinarith
  · -- typed down: above the threshold
    have g := A _ _ (hdn h2)
    rw [hlp] at g
    have hsl := lslope_spec l.dir k.val hk4 u
    rw [kf_val, he, if_neg (by norm_num)] at hsl
    obtain ⟨gk, _⟩ := opt_good (Q := Q) (up := false) (cap := 0) (o := k.val + 1) (cx := 0) (cy := 0) hro
      (by simp [isOpt, h2]; try omega)
    rw [optT_type, if_neg (by omega), show k.val + 1 - 1 = k.val by omega] at gk
    have hsp := sig_pos hR gk (ktype_cases _ _) P.hu0 P.hu1
    have hmem : k.val ∈ typedD l := by simp [typedD, h2, hk4]
    have hYk := (foldr_min_le (fun k => xk Q l l.b k c u) (l.dd : ℝ) (typedD l)).2 k.val hmem
    change Ydn Q l c u ≤ xk Q l l.b k.val c u at hYk
    simp only [xk] at hYk
    rw [hlp] at hYk
    rw [lgv_affine Q l.dir l.K k c u t ((l.b : ℝ) / Q), hsl]
    have e1 : (l.b : ℝ) / Q - t ≤ Ydn Q l c u / Q := by
      have := ht0; rw [sub_div] at this; linarith
    have e2 : Ydn Q l c u / Q ≤ -(lgv Q l.dir l.K k c u ((l.b : ℝ) / Q)) / sig (ktype l.dir k.val) u := by
      rw [div_le_iff₀ hQr]
      have : -(Q : ℝ) * lgv Q l.dir l.K k c u ((l.b : ℝ) / Q) / sig (ktype l.dir k.val) u
          = -(lgv Q l.dir l.K k c u ((l.b : ℝ) / Q)) / sig (ktype l.dir k.val) u * Q := by ring
      rw [this] at hYk; exact hYk
    have e3 := le_trans e1 e2
    rw [le_div_iff₀ hsp] at e3
    nlinarith

/-! ## 4.  The parts of a line and of a block -/

lemma xk_nonneg {S Q R x0 x1 y0 y1 U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) {c : ℝ × ℝ} {u : ℝ}
    (P : Pose S Q R x0 x1 y0 y1 U0 U1 c u) {l : LLine} {t k : ℕ} (hk : k < 4)
    (hro : rolesOk R U0 U1 l.dir l.roles = true) (hr : role l.roles k ≠ 0)
    (h : admK Q R x0 x1 y0 y1 U0 U1 (lpx l t) (lpy l t) k = true) : 0 ≤ xk Q l t k c u := by
  have g := admK_sound hQ hR P.hU01 P.hU1 h P.hx0 P.hx1 P.hy0 P.hy1 P.hu0 P.hu1 P.hwx P.hwy
  obtain ⟨_, h2⟩ := rolesOk_k hro hk
  rcases h2 with h2 | ⟨hS, hC⟩
  · exact absurd h2 hr
  have hsp : 0 < sig (ktype l.dir k) u := by
    rcases ktype_cases l.dir k with ht | ht
    · exact sig_pos hR ⟨by rw [ht]; norm_num, fun _ => hS ht, fun h => by rw [ht] at h; omega⟩
        (Or.inl ht) P.hu0 P.hu1
    · exact sig_pos hR ⟨by rw [ht]; norm_num, fun h => by rw [ht] at h; omega, fun _ => hC (by omega)⟩
        (Or.inr ht) P.hu0 P.hu1
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  unfold xk
  apply div_nonneg _ hsp.le
  nlinarith

lemma Xup_nonneg {S Q R x0 x1 y0 y1 U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) {c : ℝ × ℝ} {u : ℝ}
    (P : Pose S Q R x0 x1 y0 y1 U0 U1 c u) {l : LLine} (h : lcertOk Q R x0 x1 y0 y1 U0 U1 l = true) :
    0 ≤ Xup Q l c u := by
  obtain ⟨_, _, hro, hk⟩ := lcert_spec h
  unfold Xup
  refine le_foldr_min _ _ _ _ (fun k hk' => ?_) (Nat.cast_nonneg _)
  simp only [typedU, List.mem_filter, List.mem_range, decide_eq_true_eq] at hk'
  exact xk_nonneg hQ hR P hk'.1 hro (by omega) ((hk k hk'.1).1 hk'.2)

lemma Ydn_nonneg {S Q R x0 x1 y0 y1 U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) {c : ℝ × ℝ} {u : ℝ}
    (P : Pose S Q R x0 x1 y0 y1 U0 U1 c u) {l : LLine} (h : lcertOk Q R x0 x1 y0 y1 U0 U1 l = true) :
    0 ≤ Ydn Q l c u := by
  obtain ⟨_, _, hro, hk⟩ := lcert_spec h
  unfold Ydn
  refine le_foldr_min _ _ _ _ (fun k hk' => ?_) (Nat.cast_nonneg _)
  simp only [typedD, List.mem_filter, List.mem_range, decide_eq_true_eq] at hk'
  exact xk_nonneg hQ hR P hk'.1 hro (by omega) ((hk k hk'.1).2.1 hk'.2)

/-- The segment of a piece. -/
def pent (cls : List (SegE × ℕ)) (p : ℕ × ℕ × ℕ) : SegE := (cls.getD (Nat.sub p.1 1) ec0).1

/-- The parts of a line at a pose: down zone (from `b − Y`), core, up zone (to `a + X`). -/
noncomputable def dnPart (Q : ℕ) (cls : List (SegE × ℕ)) (l : LLine) (c : ℝ × ℝ) (u : ℝ)
    (p : ℕ × ℕ × ℕ) : SegE × ℝ × ℝ :=
  (pent cls p, min ((p.2.2 : ℝ) / Q) (max ((p.2.1 : ℝ) / Q) (((l.b : ℝ) - Ydn Q l c u) / Q)),
    (p.2.2 : ℝ) / Q)
noncomputable def corePart (Q : ℕ) (cls : List (SegE × ℕ)) (p : ℕ × ℕ × ℕ) : SegE × ℝ × ℝ :=
  (pent cls p, (p.2.1 : ℝ) / Q, (p.2.2 : ℝ) / Q)
noncomputable def upPart (Q : ℕ) (cls : List (SegE × ℕ)) (l : LLine) (c : ℝ × ℝ) (u : ℝ)
    (p : ℕ × ℕ × ℕ) : SegE × ℝ × ℝ :=
  (pent cls p, (p.2.1 : ℝ) / Q,
    max ((p.2.1 : ℝ) / Q) (min ((p.2.2 : ℝ) / Q) (((l.a : ℝ) + Xup Q l c u) / Q)))

noncomputable def lparts (Q : ℕ) (cls : List (SegE × ℕ)) (l : LLine) (c : ℝ × ℝ) (u : ℝ) :
    List (SegE × ℝ × ℝ) :=
  l.dn.map (dnPart Q cls l c u) ++ l.core.map (corePart Q cls) ++ l.up.map (upPart Q cls l c u)

lemma lpc_spec {S tag : ℕ} {cls : List (SegE × ℕ)} {l : LLine} {zlo zhi : ℕ} {p : ℕ × ℕ × ℕ}
    (htag : 0 < tag) (h : lpcOk S tag cls l zlo zhi p = true) :
    (pent cls p, tag) ∈ cls ∧ onLine S l.dir l.K (pent cls p) = true ∧
      slo S l.dir (pent cls p) ≤ p.2.1 ∧ p.2.1 ≤ p.2.2 ∧ p.2.2 ≤ shi S l.dir (pent cls p) ∧
      zlo ≤ p.2.1 ∧ p.2.2 ≤ zhi := by
  simp only [lpcOk, Bool.and_eq_true, Nat.beq_eq, Nat.ble_eq] at h
  obtain ⟨⟨⟨⟨⟨⟨ht, hon⟩, h1⟩, h2⟩, h3⟩, h4⟩, h5⟩ := h
  have hm := getD_mem_of_tag htag ht
  refine ⟨?_, hon, h1, h2, h3, h4, h5⟩
  have : (pent cls p, tag) = cls.getD (Nat.sub p.1 1) ec0 := by
    unfold pent; rw [← ht]
  rw [this]; exact hm

lemma psorted_pairwise : ∀ L : List (ℕ × ℕ × ℕ), psorted L = true → (∀ p ∈ L, p.2.1 ≤ p.2.2) →
    L.Pairwise fun p q => p.2.2 ≤ q.2.1
  | [], _, _ => List.Pairwise.nil
  | [_], _, _ => List.pairwise_singleton _ _
  | p :: q :: t, h, hle => by
    simp only [psorted, Bool.and_eq_true, Nat.ble_eq] at h
    have ih := psorted_pairwise (q :: t) h.2 (fun r hr => hle r (List.mem_cons_of_mem _ hr))
    refine List.Pairwise.cons (fun r hr => ?_) ih
    rcases List.mem_cons.mp hr with rfl | hr
    · exact h.1
    · have := List.rel_of_pairwise_cons ih hr
      have hq := hle q (List.mem_cons_of_mem _ List.mem_cons_self)
      omega


lemma up_len {lo hi z : ℝ} (h : lo ≤ hi) : max lo (min hi z) - lo = max 0 (min (z - lo) (hi - lo)) := by
  rcases le_total z lo with h1 | h1
  · rw [min_eq_right (le_trans h1 h), max_eq_left h1, max_eq_left (by
      exact le_trans (min_le_left _ _) (by linarith))]; ring
  · rcases le_total z hi with h2 | h2
    · rw [min_eq_right h2, max_eq_right h1, min_eq_left (by linarith), max_eq_right (by linarith)]
    · rw [min_eq_left h2, max_eq_right h, min_eq_right (by linarith), max_eq_right (by linarith)]

lemma dn_len {lo hi z : ℝ} (h : lo ≤ hi) : hi - min hi (max lo z) = max 0 (min (hi - z) (hi - lo)) := by
  rcases le_total z lo with h1 | h1
  · rw [max_eq_left h1, min_eq_right h, min_eq_right (by linarith), max_eq_right (by linarith)]
  · rcases le_total z hi with h2 | h2
    · rw [max_eq_right h1, min_eq_right h2, min_eq_left (by linarith), max_eq_right (by linarith)]
    · rw [max_eq_right h1, min_eq_left h2, max_eq_left (by
        exact le_trans (min_le_left _ _) (by linarith))]; ring

lemma mm_scale {A B Q : ℝ} (hQ : 0 < Q) : max 0 (min (A / Q) (B / Q)) * Q = max 0 (min A B) := by
  have key : ∀ {A B : ℝ}, A ≤ B → max 0 (min (A / Q) (B / Q)) * Q = max 0 (min A B) := by
    intro A B h
    rw [min_eq_left (div_le_div_of_nonneg_right h hQ.le), min_eq_left h]
    rcases le_total 0 A with h0 | h0
    · rw [max_eq_right (div_nonneg h0 hQ.le), max_eq_right h0]; field_simp
    · rw [max_eq_left (div_nonpos_of_nonpos_of_nonneg h0 hQ.le), max_eq_left h0]; simp
  rcases le_total A B with h | h
  · exact key h
  · rw [min_comm (A / Q), min_comm A]; exact key h

/-- The density bound of one piece: `Q · pval ≥ ρ̂ · length` (length over `Q`). -/
lemma piece_rho {D S : ℕ} (hD : 0 < D) (hS : 0 < S) {cls : List (SegE × ℕ)} {l : LLine}
    {p : ℕ × ℕ × ℕ} (hon : onLine S l.dir l.K (pent cls p) = true) (lo' hi' : ℝ) (hlh : lo' ≤ hi') :
    (rho S (D * S) cls l p : ℝ) * ((hi' - lo') * (D * S : ℕ))
      ≤ (D * S : ℕ) * pval D (pent cls p, lo', hi') := by
  have hQr : (0 : ℝ) < (D * S : ℕ) := by exact_mod_cast Nat.mul_pos hD hS
  obtain ⟨_, _, _, hlt, _⟩ := onLine_spec (K := l.K) hD hS rfl hon
  rw [pval_line hD hS rfl hon]
  have hl : (0 : ℝ) < (shi S l.dir (pent cls p) : ℝ) - slo S l.dir (pent cls p) := by
    have : (slo S l.dir (pent cls p) : ℝ) < shi S l.dir (pent cls p) := by exact_mod_cast hlt
    linarith
  have hr : (rho S (D * S) cls l p : ℝ) ≤ ((pent cls p).2.2.2.2 : ℝ) * (D * S : ℕ) /
      ((shi S l.dir (pent cls p) : ℝ) - slo S l.dir (pent cls p)) := by
    unfold rho
    simp only [nat_div_eq, nat_mul_eq, nat_sub_eq]
    have := Nat.cast_div_le (α := ℝ) (m := (pent cls p).2.2.2.2 * (D * S))
      (n := shi S l.dir (pent cls p) - slo S l.dir (pent cls p))
    rw [Nat.cast_mul, Nat.cast_sub hlt.le] at this
    unfold pent at this ⊢
    exact this
  have hnn : 0 ≤ (hi' - lo') * (D * S : ℕ) := mul_nonneg (by linarith) hQr.le
  calc (rho S (D * S) cls l p : ℝ) * ((hi' - lo') * (D * S : ℕ))
      ≤ ((pent cls p).2.2.2.2 : ℝ) * (D * S : ℕ) /
        ((shi S l.dir (pent cls p) : ℝ) - slo S l.dir (pent cls p)) * ((hi' - lo') * (D * S : ℕ)) :=
        mul_le_mul_of_nonneg_right hr hnn
    _ = (D * S : ℕ) * (((pent cls p).2.2.2.2 : ℝ) * (D * S : ℕ) * (hi' - lo') /
        ((shi S l.dir (pent cls p) : ℝ) - slo S l.dir (pent cls p))) := by ring

/-- The option `k + 1` at the up end is `i + s x_k`. -/
lemma oval_up_xk (Q : ℕ) (l : LLine) (cap k : ℕ) (c : ℝ × ℝ) (u : ℝ) :
    oval Q l true cap (k + 1) c u = sv l.iU + l.sU * xk Q l l.a k c u := by
  simp only [oval, show k + 1 ≠ 0 by omega, if_false, if_true, show k + 1 - 1 = k by omega, xk]
  ring
lemma oval_dn_xk (Q : ℕ) (l : LLine) (cap k : ℕ) (c : ℝ × ℝ) (u : ℝ) :
    oval Q l false cap (k + 1) c u = sv l.iD + l.sD * xk Q l l.b k c u := by
  simp only [oval, show k + 1 ≠ 0 by omega, if_false, Bool.false_eq_true, show k + 1 - 1 = k by omega, xk]
  ring

lemma emin_le_cap (Q : ℕ) (l : LLine) (up : Bool) (cap : ℕ) (c : ℝ × ℝ) (u : ℝ) :
    emin Q l up cap c u ≤ cap := (foldr_min_le _ _ _).1
lemma emin_le_opt {Q : ℕ} {l : LLine} {up : Bool} {cap o : ℕ} (c : ℝ × ℝ) (u : ℝ)
    (ho : isOpt l up o = true) (ho4 : o < 5) : emin Q l up cap c u ≤ oval Q l up cap o c u :=
  (foldr_min_le _ _ _).2 o (by simp [opts, ho, ho4])

/-- **The up gain**: `Q Σ pval(up parts) ≥ emin up`. -/
lemma up_gain {D S R x0 x1 y0 y1 U0 U1 : ℕ} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    {c : ℝ × ℝ} {u : ℝ} (P : Pose S (D * S) R x0 x1 y0 y1 U0 U1 c u) {cls : List (SegE × ℕ)}
    {tag : ℕ} (htag : 0 < tag) {l : LLine}
    (hc : lcertOk (D * S) R x0 x1 y0 y1 U0 U1 l = true)
    (hup : ∀ p ∈ l.up, lpcOk S tag cls l l.a (l.a + l.du) p = true)
    (hg : gainOk l.sU l.iU l.du 0 (upOff S (D * S) cls l) = true) :
    emin (D * S) l true (capU S (D * S) cls l) c u
      ≤ (D * S : ℕ) * ((l.up.map (upPart (D * S) cls l c u)).map (pval D)).sum := by
  set Q := D * S with hQdef
  have hQr : (0 : ℝ) < Q := by exact_mod_cast Nat.mul_pos hD hS
  have hXd : Xup Q l c u ≤ l.du := (foldr_min_le _ _ _).1
  have hsp : ∀ p ∈ l.up, (p.2.1 - l.a : ℕ) ≤ (p.2.2 - l.a : ℕ) ∧ p.2.2 ≤ l.a + l.du ∧ l.a ≤ p.2.1 ∧
      p.2.1 ≤ p.2.2 := by
    intro p hp
    obtain ⟨_, _, _, h2, _, h4, h5⟩ := lpc_spec htag (hup p hp)
    exact ⟨by omega, h5, h4, h2⟩
  -- the ρ̂-sum is below `Q Σ pval`
  have hsum : ((upOff S Q cls l).map fun p => (p.1 : ℝ) *
        max 0 (min (Xup Q l c u - p.2.1) ((p.2.2 : ℝ) - p.2.1))).sum
      ≤ (Q : ℝ) * ((l.up.map (upPart Q cls l c u)).map (pval D)).sum := by
    unfold upOff
    rw [List.map_map, List.map_map, ← List.sum_map_mul_left]
    apply List.sum_le_sum
    intro p hp
    obtain ⟨_, hon, _, _, _, _, _⟩ := lpc_spec htag (hup p hp)
    obtain ⟨_, _, ha, hlh⟩ := hsp p hp
    simp only [Function.comp, upPart]
    have hlh' : (p.2.1 : ℝ) / Q ≤ max ((p.2.1 : ℝ) / Q) (min ((p.2.2 : ℝ) / Q) (((l.a : ℝ) + Xup Q l c u) / Q)) :=
      le_max_left _ _
    have key := piece_rho hD hS hon _ _ hlh'
    refine le_trans (le_of_eq ?_) key
    rw [up_len (div_le_div_of_nonneg_right (by exact_mod_cast hlh) hQr.le)]
    simp only [nat_sub_eq]
    rw [Nat.cast_sub ha, Nat.cast_sub (le_trans ha hlh)]
    congr 1
    have e1 : ((l.a : ℝ) + Xup Q l c u) / Q - (p.2.1 : ℝ) / Q = (Xup Q l c u - (p.2.1 - l.a)) / Q := by ring
    have e2 : (p.2.2 : ℝ) / Q - (p.2.1 : ℝ) / Q = ((p.2.2 - l.a) - (p.2.1 - l.a)) / Q := by ring
    rw [e1, e2, ← hQdef, mm_scale hQr]
  have hgl := gain_lb l.sU l.iU l.du 0 (upOff S Q cls l) hg (fun p hp => by
    simp only [upOff, List.mem_map] at hp
    obtain ⟨q, hq, rfl⟩ := hp
    exact (hsp q hq).1) (Xup Q l c u) hXd
  rcases foldr_min_mem (fun k => xk Q l l.a k c u) (l.du : ℝ) (typedU l) with h | ⟨k, hk, h⟩
  · -- the end moves the whole zone: the cap
    change Xup Q l c u = l.du at h
    have hcap : (capU S Q cls l : ℝ) = ((upOff S Q cls l).map fun p => (p.1 : ℝ) *
        max 0 (min (Xup Q l c u - p.2.1) ((p.2.2 : ℝ) - p.2.1))).sum := by
      unfold capU
      rw [gainSum_eq, Nat.cast_zero, zero_add]
      unfold upOff
      rw [List.map_map, List.map_map]
      congr 1
      apply List.map_congr_left
      intro p hp
      obtain ⟨h0, h1, ha, hlh⟩ := hsp p hp
      simp only [Function.comp, nat_sub_eq, h]
      rw [Nat.cast_sub h0, Nat.cast_sub ha, Nat.cast_sub (le_trans ha hlh)]
      congr 1
      have : ((p.2.2 : ℝ) - l.a) ≤ l.du := by
        have : (p.2.2 : ℝ) ≤ l.a + l.du := by exact_mod_cast h1
        linarith
      rw [min_eq_right (by linarith), max_eq_right (by
        have : (p.2.1 : ℝ) ≤ p.2.2 := by exact_mod_cast hlh
        linarith)]
    have := emin_le_cap Q l true (capU S Q cls l) c u
    linarith
  · -- the end is a threshold `x_k`
    change Xup Q l c u = xk Q l l.a k c u at h
    simp only [typedU, List.mem_filter, List.mem_range, decide_eq_true_eq] at hk
    have ho : isOpt l true (k + 1) = true := by simp [isOpt, hk.2]; omega
    have h1 := emin_le_opt (Q := Q) (cap := capU S Q cls l) c u ho (by omega)
    rw [oval_up_xk, ← h] at h1
    simp only [Nat.cast_zero, zero_add] at hgl
    linarith

/-- **The down gain**: `Q Σ pval(down parts) ≥ emin down`. -/
lemma dn_gain {D S R x0 x1 y0 y1 U0 U1 : ℕ} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    {c : ℝ × ℝ} {u : ℝ} (P : Pose S (D * S) R x0 x1 y0 y1 U0 U1 c u) {cls : List (SegE × ℕ)}
    {tag : ℕ} (htag : 0 < tag) {l : LLine}
    (hc : lcertOk (D * S) R x0 x1 y0 y1 U0 U1 l = true)
    (hdn : ∀ p ∈ l.dn, lpcOk S tag cls l (l.b - l.dd) l.b p = true)
    (hg : gainOk l.sD l.iD l.dd 0 (dnOff S (D * S) cls l) = true) :
    emin (D * S) l false (capD S (D * S) cls l) c u
      ≤ (D * S : ℕ) * ((l.dn.map (dnPart (D * S) cls l c u)).map (pval D)).sum := by
  set Q := D * S with hQdef
  have hQr : (0 : ℝ) < Q := by exact_mod_cast Nat.mul_pos hD hS
  have hYd : Ydn Q l c u ≤ l.dd := (foldr_min_le _ _ _).1
  obtain ⟨hba, hdd, _, _⟩ := lcert_spec hc
  have hsp : ∀ p ∈ l.dn, (l.b - p.2.2 : ℕ) ≤ (l.b - p.2.1 : ℕ) ∧ l.b - l.dd ≤ p.2.1 ∧
      p.2.2 ≤ l.b ∧ p.2.1 ≤ p.2.2 := by
    intro p hp
    obtain ⟨_, _, _, h2, _, h4, h5⟩ := lpc_spec htag (hdn p hp)
    exact ⟨by omega, h4, h5, h2⟩
  have hsum : ((dnOff S Q cls l).map fun p => (p.1 : ℝ) *
        max 0 (min (Ydn Q l c u - p.2.1) ((p.2.2 : ℝ) - p.2.1))).sum
      ≤ (Q : ℝ) * ((l.dn.map (dnPart Q cls l c u)).map (pval D)).sum := by
    unfold dnOff
    rw [List.map_reverse, List.sum_reverse, List.map_map, List.map_map, ← List.sum_map_mul_left]
    apply List.sum_le_sum
    intro p hp
    obtain ⟨_, hon, _, _, _, _, _⟩ := lpc_spec htag (hdn p hp)
    obtain ⟨_, h4, hb, hlh⟩ := hsp p hp
    simp only [Function.comp, dnPart]
    have hlh' : min ((p.2.2 : ℝ) / Q) (max ((p.2.1 : ℝ) / Q) (((l.b : ℝ) - Ydn Q l c u) / Q))
        ≤ (p.2.2 : ℝ) / Q := min_le_left _ _
    have key := piece_rho hD hS hon _ _ hlh'
    refine le_trans (le_of_eq ?_) key
    rw [dn_len (div_le_div_of_nonneg_right (by exact_mod_cast hlh) hQr.le)]
    simp only [nat_sub_eq]
    rw [Nat.cast_sub hb, Nat.cast_sub (le_trans hlh hb)]
    congr 1
    have e1 : (p.2.2 : ℝ) / Q - ((l.b : ℝ) - Ydn Q l c u) / Q = (Ydn Q l c u - (l.b - p.2.2)) / Q := by
      ring
    have e2 : (p.2.2 : ℝ) / Q - (p.2.1 : ℝ) / Q = ((l.b - p.2.1) - (l.b - p.2.2)) / Q := by ring
    rw [e1, e2, ← hQdef, mm_scale hQr]
  have hgl := gain_lb l.sD l.iD l.dd 0 (dnOff S Q cls l) hg (fun p hp => by
    simp only [dnOff, List.mem_reverse, List.mem_map] at hp
    obtain ⟨q, hq, rfl⟩ := hp
    exact (hsp q hq).1) (Ydn Q l c u) hYd
  rcases foldr_min_mem (fun k => xk Q l l.b k c u) (l.dd : ℝ) (typedD l) with h | ⟨k, hk, h⟩
  · change Ydn Q l c u = l.dd at h
    have hcap : (capD S Q cls l : ℝ) = ((dnOff S Q cls l).map fun p => (p.1 : ℝ) *
        max 0 (min (Ydn Q l c u - p.2.1) ((p.2.2 : ℝ) - p.2.1))).sum := by
      unfold capD
      rw [gainSum_eq, Nat.cast_zero, zero_add]
      unfold dnOff
      rw [List.map_reverse, List.map_reverse, List.sum_reverse, List.sum_reverse,
        List.map_map, List.map_map]
      congr 1
      apply List.map_congr_left
      intro p hp
      obtain ⟨h0, h4, hb, hlh⟩ := hsp p hp
      simp only [Function.comp, nat_sub_eq, h]
      rw [Nat.cast_sub h0, Nat.cast_sub hb, Nat.cast_sub (le_trans hlh hb)]
      congr 1
      have : ((l.b : ℝ) - p.2.1) ≤ l.dd := by
        have : ((l.b - l.dd : ℕ) : ℝ) ≤ p.2.1 := by exact_mod_cast h4
        rw [Nat.cast_sub hdd] at this
        linarith
      rw [min_eq_right (by linarith), max_eq_right (by
        have : (p.2.1 : ℝ) ≤ p.2.2 := by exact_mod_cast hlh
        linarith)]
    have := emin_le_cap Q l false (capD S Q cls l) c u
    linarith
  · change Ydn Q l c u = xk Q l l.b k c u at h
    simp only [typedD, List.mem_filter, List.mem_range, decide_eq_true_eq] at hk
    have ho : isOpt l false (k + 1) = true := by simp [isOpt, hk.2]; omega
    have h1 := emin_le_opt (Q := Q) (cap := capD S Q cls l) c u ho (by omega)
    rw [oval_dn_xk, ← h] at h1
    simp only [Nat.cast_zero, zero_add] at hgl
    linarith

/-- The cores: `Σ pval(core parts) ≥ coreVal`. -/
lemma core_val {D S : ℕ} (hD : 0 < D) (hS : 0 < S) {cls : List (SegE × ℕ)} {tag : ℕ}
    (htag : 0 < tag) {l : LLine} (hcore : ∀ p ∈ l.core, lpcOk S tag cls l l.b l.a p = true) :
    (coreVal S cls l : ℝ) ≤ ((l.core.map (corePart (D * S) cls)).map (pval D)).sum := by
  unfold coreVal
  rw [List.map_map]
  push_cast [Nat.cast_list_sum]
  rw [List.map_map]
  apply List.sum_le_sum
  intro p hp
  obtain ⟨_, hon, _, hlh, _, _, _⟩ := lpc_spec htag (hcore p hp)
  obtain ⟨_, _, _, hlt, _⟩ := onLine_spec (K := l.K) hD hS rfl hon
  simp only [Function.comp, corePart]
  rw [pval_line hD hS rfl hon]
  have hQr : (0 : ℝ) < (D * S : ℕ) := by exact_mod_cast Nat.mul_pos hD hS
  unfold cmass
  simp only [nat_div_eq, nat_mul_eq, nat_sub_eq]
  have := Nat.cast_div_le (α := ℝ) (m := (pent cls p).2.2.2.2 * (p.2.2 - p.2.1))
    (n := shi S l.dir (pent cls p) - slo S l.dir (pent cls p))
  rw [Nat.cast_mul, Nat.cast_sub hlt.le, Nat.cast_sub hlh] at this
  unfold pent at this ⊢
  refine le_trans this (le_of_eq ?_)
  field_simp

/-- **A line at a pose**: its parts are parts, pairwise disjoint on each segment, and certify its
core plus its ends' minima. -/
theorem line_sound {D S R x0 x1 y0 y1 U0 U1 : ℕ} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    {c : ℝ × ℝ} {u : ℝ} (P : Pose S (D * S) R x0 x1 y0 y1 U0 U1 c u) {cls : List (SegE × ℕ)}
    {tag : ℕ} (htag : 0 < tag) {l : LLine}
    (hc : lcertOk (D * S) R x0 x1 y0 y1 U0 U1 l = true) (hp : lpcsOk S (D * S) tag cls l = true) :
    (∀ x ∈ lparts (D * S) cls l c u, PartOK D (sq c (2 * Real.arctan u) 1) x ∧ (x.1, tag) ∈ cls ∧
        onLine S l.dir l.K x.1 = true) ∧
      (lparts (D * S) cls l c u).Pairwise PRel ∧
      (coreVal S cls l : ℝ) + (emin (D * S) l true (capU S (D * S) cls l) c u +
          emin (D * S) l false (capD S (D * S) cls l) c u) / (D * S : ℕ)
        ≤ ((lparts (D * S) cls l c u).map (pval D)).sum := by
  set Q := D * S with hQdef
  have hQ : 0 < Q := Nat.mul_pos hD hS
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  obtain ⟨hba, hdd, hro, hk⟩ := lcert_spec hc
  have hp' := hp
  simp only [lpcsOk, Bool.and_eq_true, List.all_eq_true] at hp'
  obtain ⟨⟨⟨⟨⟨⟨⟨hup, hsu⟩, hcore⟩, hsc⟩, hdn⟩, hsd⟩, hgu⟩, hgd⟩ := hp'
  have hX0 := Xup_nonneg hQ hR P hc
  have hY0 := Ydn_nonneg hQ hR P hc
  have hch := fun t ht0 ht1 => chord hQ hR P hc (t := t) ht0 ht1
  have cQ : ∀ {m n : ℕ}, m ≤ n → (m : ℝ) / Q ≤ (n : ℝ) / Q :=
    fun h => div_le_div_of_nonneg_right (by exact_mod_cast h) hQr.le
  have hab : ((l.b : ℝ) - Ydn Q l c u) / Q ≤ (l.a : ℝ) / Q := by
    rw [div_le_div_iff_of_pos_right hQr]; have : (l.b : ℝ) ≤ l.a := by exact_mod_cast hba
    linarith
  have hba' : (l.b : ℝ) / Q ≤ ((l.a : ℝ) + Xup Q l c u) / Q := by
    rw [div_le_div_iff_of_pos_right hQr]; have : (l.b : ℝ) ≤ l.a := by exact_mod_cast hba
    linarith
  have Pup : ∀ p ∈ l.up, PartOK D (sq c (2 * Real.arctan u) 1) (upPart Q cls l c u p) ∧
      (pent cls p, tag) ∈ cls ∧ onLine S l.dir l.K (pent cls p) = true := by
    intro p hpm
    obtain ⟨hm, hon, h1, h2, h3, h4, h5⟩ := lpc_spec htag (hup p hpm)
    obtain ⟨hax, hlo, hhi, _, hlp⟩ := onLine_spec (K := l.K) hD hS hQdef hon
    refine ⟨?_, hm, hon⟩
    simp only [upPart]
    refine ⟨hax, by rw [hlo]; exact cQ h1, le_max_left _ _, ?_, fun t ht1 ht2 => ?_⟩
    · rw [hhi]; exact max_le (cQ (le_trans h2 h3)) (le_trans (min_le_left _ _) (cQ h3))
    · simp only at ht1 ht2 ⊢
      rw [hlp]
      have hta : (l.a : ℝ) / Q ≤ t := le_trans (cQ h4) ht1.le
      refine hch t (by linarith) ?_
      rcases le_total ((p.2.1 : ℝ) / Q) (min ((p.2.2 : ℝ) / Q) (((l.a : ℝ) + Xup Q l c u) / Q))
        with hm' | hm'
      · rw [max_eq_right hm'] at ht2; exact le_trans ht2.le (min_le_right _ _)
      · rw [max_eq_left hm'] at ht2; exact absurd (lt_trans ht1 ht2) (lt_irrefl _)
  have Pcore : ∀ p ∈ l.core, PartOK D (sq c (2 * Real.arctan u) 1) (corePart Q cls p) ∧
      (pent cls p, tag) ∈ cls ∧ onLine S l.dir l.K (pent cls p) = true := by
    intro p hpm
    obtain ⟨hm, hon, h1, h2, h3, h4, h5⟩ := lpc_spec htag (hcore p hpm)
    obtain ⟨hax, hlo, hhi, _, hlp⟩ := onLine_spec (K := l.K) hD hS hQdef hon
    refine ⟨?_, hm, hon⟩
    simp only [corePart]
    refine ⟨hax, by rw [hlo]; exact cQ h1, cQ h2, by rw [hhi]; exact cQ h3, fun t ht1 ht2 => ?_⟩
    simp only at ht1 ht2 ⊢
    rw [hlp]
    refine hch t ?_ ?_
    · have : ((l.b : ℝ) - Ydn Q l c u) / Q ≤ (l.b : ℝ) / Q :=
        div_le_div_of_nonneg_right (by linarith) hQr.le
      linarith [cQ h4]
    · have : (l.a : ℝ) / Q ≤ ((l.a : ℝ) + Xup Q l c u) / Q :=
        div_le_div_of_nonneg_right (by linarith) hQr.le
      linarith [cQ h5]
  have Pdn : ∀ p ∈ l.dn, PartOK D (sq c (2 * Real.arctan u) 1) (dnPart Q cls l c u p) ∧
      (pent cls p, tag) ∈ cls ∧ onLine S l.dir l.K (pent cls p) = true := by
    intro p hpm
    obtain ⟨hm, hon, h1, h2, h3, h4, h5⟩ := lpc_spec htag (hdn p hpm)
    obtain ⟨hax, hlo, hhi, _, hlp⟩ := onLine_spec (K := l.K) hD hS hQdef hon
    refine ⟨?_, hm, hon⟩
    simp only [dnPart]
    refine ⟨hax, ?_, min_le_left _ _, by rw [hhi]; exact cQ h3, fun t ht1 ht2 => ?_⟩
    · rw [hlo]; exact le_min (cQ (le_trans h1 h2)) (le_trans (cQ h1) (le_max_left _ _))
    · simp only at ht1 ht2 ⊢
      rw [hlp]
      have htb : t ≤ (l.b : ℝ) / Q := le_trans ht2.le (cQ h5)
      refine hch t ?_ (by linarith)
      rcases le_total ((p.2.2 : ℝ) / Q) (max ((p.2.1 : ℝ) / Q) (((l.b : ℝ) - Ydn Q l c u) / Q))
        with hm' | hm'
      · rw [min_eq_left hm'] at ht1; exact absurd (lt_trans ht1 ht2) (lt_irrefl _)
      · rw [min_eq_right hm'] at ht1; exact le_trans (le_max_right _ _) ht1.le
  refine ⟨?_, ?_, ?_⟩
  · intro x hx
    simp only [lparts, List.mem_append, List.mem_map] at hx
    rcases hx with (⟨p, hp, rfl⟩ | ⟨p, hp, rfl⟩) | ⟨p, hp, rfl⟩
    · exact Pdn p hp
    · exact Pcore p hp
    · exact Pup p hp
  · have ord_up := psorted_pairwise l.up hsu (fun p hp => (lpc_spec htag (hup p hp)).2.2.2.1)
    have ord_core := psorted_pairwise l.core hsc (fun p hp => (lpc_spec htag (hcore p hp)).2.2.2.1)
    have ord_dn := psorted_pairwise l.dn hsd (fun p hp => (lpc_spec htag (hdn p hp)).2.2.2.1)
    simp only [lparts, List.pairwise_append, List.pairwise_map, List.mem_append, List.mem_map]
    refine ⟨⟨ord_dn.imp_of_mem fun {p q} _ hq h _ => ?_, ord_core.imp fun {p q} h _ => ?_, ?_⟩,
      ord_up.imp_of_mem fun {p q} hp _ h _ => ?_, ?_⟩
    · simp only [dnPart]
      exact le_min (le_trans (cQ h) (cQ (lpc_spec htag (hdn q hq)).2.2.2.1))
        (le_trans (cQ h) (le_max_left _ _))
    · simp only [corePart]; exact cQ h
    · rintro x ⟨p, hp, rfl⟩ y ⟨q, hq, rfl⟩ _
      simp only [dnPart, corePart]
      exact cQ (le_trans (lpc_spec htag (hdn p hp)).2.2.2.2.2.2
        (lpc_spec htag (hcore q hq)).2.2.2.2.2.1)
    · simp only [upPart]
      exact le_trans (max_le (cQ (lpc_spec htag (hup p hp)).2.2.2.1) (min_le_left _ _)) (cQ h)
    · rintro x hx y ⟨q, hq, rfl⟩ _
      simp only [upPart]
      rcases hx with ⟨p, hp, rfl⟩ | ⟨p, hp, rfl⟩
      · simp only [dnPart]
        exact cQ (le_trans (lpc_spec htag (hdn p hp)).2.2.2.2.2.2
          (le_trans hba (lpc_spec htag (hup q hq)).2.2.2.2.2.1))
      · simp only [corePart]
        exact cQ (le_trans (lpc_spec htag (hcore p hp)).2.2.2.2.2.2
          (lpc_spec htag (hup q hq)).2.2.2.2.2.1)
  · have gU := up_gain hD hS hR P htag hc hup hgu
    have gD := dn_gain hD hS hR P htag hc hdn hgd
    have cV := core_val hD hS htag hcore
    simp only [lparts, List.map_append, List.sum_append]
    rw [← hQdef] at gU gD
    have e : (emin Q l true (capU S Q cls l) c u + emin Q l false (capD S Q cls l) c u) / (Q : ℕ)
        ≤ ((l.up.map (upPart Q cls l c u)).map (pval D)).sum
          + ((l.dn.map (dnPart Q cls l c u)).map (pval D)).sum := by
      rw [div_le_iff₀ hQr]; nlinarith
    linarith

/-! ## 5.  The block -/

lemma lsorted_pairwise : ∀ L : List LLine, lsorted L = true →
    L.Pairwise fun l m => l.dir < m.dir ∨ (l.dir = m.dir ∧ l.K < m.K)
  | [], _ => List.Pairwise.nil
  | [_], _ => List.pairwise_singleton _ _
  | l :: m :: t, h => by
    simp only [lsorted, Bool.and_eq_true, Bool.or_eq_true, Nat.blt_eq, Nat.beq_eq] at h
    have ih := lsorted_pairwise (m :: t) h.2
    refine List.Pairwise.cons (fun r hr => ?_) ih
    rcases List.mem_cons.mp hr with rfl | hr
    · exact h.1
    · have := List.rel_of_pairwise_cons ih hr
      rcases h.1 with h1 | ⟨h1, h2⟩ <;> rcases this with h3 | ⟨h3, h4⟩ <;> omega

/-- An entry lies on one line only (directions `0`, `1`). -/
lemma onLine_unique {S d1 d2 K1 K2 : ℕ} {e : SegE} (h1 : onLine S d1 K1 e = true)
    (h2 : onLine S d2 K2 e = true) (hd1 : d1 ≤ 1) (hd2 : d2 ≤ 1) : d1 = d2 ∧ K1 = K2 := by
  have spec : ∀ {d K : ℕ}, onLine S d K e = true →
      (d = 0 ∧ e.1 = e.2.2.1 ∧ e.1 * S = K ∧ e.2.1 < e.2.2.2.1) ∨
      (d ≠ 0 ∧ e.2.1 = e.2.2.2.1 ∧ e.2.1 * S = K ∧ e.1 < e.2.2.1) := by
    intro d K h
    by_cases hd : d = 0
    · subst hd
      simp only [onLine, beq_rfl, cond_true, Bool.and_eq_true, Nat.beq_eq, Nat.blt_eq,
        nat_mul_eq] at h
      exact Or.inl ⟨rfl, h.1.1, h.1.2, h.2⟩
    · simp only [onLine, beq_ne hd, cond_false, Bool.and_eq_true, Nat.beq_eq, Nat.blt_eq,
        nat_mul_eq] at h
      exact Or.inr ⟨hd, h.1.1, h.1.2, h.2⟩
  rcases spec h1 with ⟨a1, a2, a3, a4⟩ | ⟨a1, a2, a3, a4⟩ <;>
    rcases spec h2 with ⟨b1, b2, b3, b4⟩ | ⟨b1, b2, b3, b4⟩
  · exact ⟨by omega, by omega⟩
  · omega
  · omega
  · exact ⟨by omega, by rw [← a3, ← b3]⟩

/-- **Soundness of an L-block**: at every admissible pose, parts of its segments certify its value. -/
theorem lblk_sound {D S R x0 x1 y0 y1 U0 U1 : ℕ} (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    {c : ℝ × ℝ} {u : ℝ} (P : Pose S (D * S) R x0 x1 y0 y1 U0 U1 c u) {cls : List (SegE × ℕ)}
    {tag : ℕ} (htag : 0 < tag) {B : LBlk}
    (h : lblkOk S (D * S) R x0 x1 y0 y1 U0 U1 cls tag B = true) :
    ∃ L : List (SegE × ℝ × ℝ),
      (∀ x ∈ L, PartOK D (sq c (2 * Real.arctan u) 1) x ∧ (x.1, tag) ∈ cls) ∧
      L.Pairwise PRel ∧ (lblkVal S (D * S) cls B : ℝ) ≤ (L.map (pval D)).sum := by
  simp only [lblkOk, Bool.and_eq_true, List.all_eq_true, Nat.beq_eq, Nat.ble_eq] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨hls, hlines⟩, hlen⟩, hlen'⟩, h00⟩, h01⟩, h10⟩, h11⟩ := h
  have hQr : (0 : ℝ) < (D * S : ℕ) := by exact_mod_cast Nat.mul_pos hD hS
  have LS := fun l (hl : l ∈ B.lines) =>
    line_sound hD hS hR P htag (hlines l hl).1.2 (hlines l hl).2
  refine ⟨B.lines.flatMap fun l => lparts (D * S) cls l c u, ?_, ?_, ?_⟩
  · intro x hx
    obtain ⟨l, hl, hx⟩ := List.mem_flatMap.mp hx
    obtain ⟨a1, a2, _⟩ := (LS l hl).1 x hx
    exact ⟨a1, a2⟩
  · rw [List.pairwise_flatMap]
    refine ⟨fun l hl => (LS l hl).2.1, ?_⟩
    have hp := lsorted_pairwise B.lines hls
    refine hp.imp_of_mem fun {l m} hl hm hlm x hx y hy hxy => ?_
    exfalso
    obtain ⟨_, _, ox⟩ := (LS l hl).1 x hx
    obtain ⟨_, _, oy⟩ := (LS m hm).1 y hy
    rw [hxy] at ox
    obtain ⟨e1, e2⟩ := onLine_unique ox oy (hlines l hl).1.1 (hlines m hm).1.1
    omega
  · have hro : ∀ l ∈ B.lines, rolesOk R U0 U1 l.dir l.roles = true :=
      fun l hl => (lcert_spec (hlines l hl).1.2).2.2.1
    have hPhi := Phi_box hD hS hR P cls hlen hlen' hro h00 h01 h10 h11
    unfold lblkVal
    have hsum : ∀ ls : List LLine, (∀ l ∈ ls, l ∈ B.lines) →
        (((ls.map (coreVal S cls)).sum : ℕ) : ℝ) + Phi (D * S) S cls ls c u / (D * S : ℕ)
          ≤ ((ls.flatMap fun l => lparts (D * S) cls l c u).map (pval D)).sum := by
      intro ls
      induction ls with
      | nil => intro _; simp [Phi]
      | cons l ls ih =>
        intro hls'
        have ih' := ih (fun m hm => hls' m (List.mem_cons_of_mem _ hm))
        have hl := (LS l (hls' l List.mem_cons_self)).2.2
        simp only [Phi, List.map_cons, List.sum_cons, List.flatMap_cons, List.map_append,
          List.sum_append, Nat.cast_add] at ih' hl ⊢
        rw [add_div]
        linarith
    have h1 := hsum B.lines (fun l hl => hl)
    have hd : ((B.lg / (D * S) : ℕ) : ℝ) ≤ (B.lg : ℝ) / (D * S : ℕ) := Nat.cast_div_le
    have h2 : (B.lg : ℝ) / (D * S : ℕ) ≤ Phi (D * S) S cls B.lines c u / (D * S : ℕ) :=
      div_le_div_of_nonneg_right hPhi hQr.le
    simp only [nat_div_eq]
    rw [Nat.cast_add]
    linarith

end ZMTreeM

end SquarePacking
