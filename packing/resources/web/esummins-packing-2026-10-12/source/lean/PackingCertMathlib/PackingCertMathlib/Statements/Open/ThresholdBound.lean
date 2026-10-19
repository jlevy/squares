import PackingCertMathlib.TopLevel

/-!
# -- OPEN (EXTERNAL): `s(11) > 31/8` — Kleddamag's certified threshold bound (T-037), replayed by A242

`docs/proofs/threshold_bound.md`; replay and spot-check `attempts/A242-replay-31-8/`.

**The external result.**  Kleddamag, *11-squares-certified-bound*, release `v1.0.2` (commit `6a733f3`,
certificate SHA-256 `57e9927d…cd44458`), reviewed as T-037 in Levy's *n11 threshold bound review*, Part II:
eleven parents of side `A = 764/775` do not fit in a container of side `L = 191/50`.  A fixed rational
certificate assigns to every parent orientation (12,028 half-angle rows) a concentric closed core strictly
inside the parent, and gives every core a charge from 5,284 weighted sites and 2,220 threshold sets
(point / 2-of-3 / 2-of-5 / 3-of-5).  An exact sweep shows every legal core collects at least
`Γ = 0.999962528`; the Budget lemma caps eleven disjoint cores at `M = 10.999479944`; `11 Γ > M`.

**What is a theorem here.**
* `budget_lemma` [T]: pairwise disjoint sub-families of an `m`-set, each of size `≥ k`, number at most `m / k`
  (`q k ≤ m`) — why a `k`-of-`m` charge pays at most `⌊m/k⌋` disjoint cores (the point case is `k = m = 1`).
* `counting` [T]: `11 · 999962528 > 10999479944` (in units of `10⁻⁹`), surplus `107864`.
* `scaling_arith`, `scaling_side` [T]: `(191/50) / (764/775) = 31/8`, so a side `s ≤ 31/8` scaled by `A` is `≤ L`.
* `lb382_of_threshold` [T from the axiom]: the axiom implies Theorem 1 (`191/50 < 31/8`).
* `window_restrict` [T from the axiom]: ANY window statement about packings at sides in `[191/50, b]` follows
  from its restriction to `[31/8, b]`; instances `stratum_kill_of_wnd'` and `trump_residual_of_wnd'` — the two
  open window axioms of `TopLevel.lean` need only be discharged on `W' = [31/8, ŝ]`.

**What is not.**  `threshold_bound_31_8` is an axiom: an EXTERNAL certified computation (their Python sweep +
their stdlib controls), replayed offline by A242 row by row against their recorded per-row minima, with an
independent lab spot-check of (a)-(d) (`results/spot242.json`).  Not a Lean proof of the sweep.
-/

namespace PackingCert.S11.OpenLemmas.ThresholdBound

open Set

/-- **[EXTERNAL, T-037; A242 replay]** No eleven unit squares fit in a square of side `≤ 31/8`. -/
axiom threshold_bound_31_8 : ∀ s : ℝ, Fits 11 s → (31 / 8 : ℝ) < s

/-- **Budget lemma** [T]: `q` pairwise disjoint subsets of `S`, each with at least `k` elements, have `q k ≤ |S|`. -/
theorem budget_lemma {α β : Type*} [DecidableEq α] (S : Finset α) (k : ℕ) (I : Finset β) (T : β → Finset α)
    (hd : ∀ i ∈ I, ∀ j ∈ I, i ≠ j → Disjoint (T i) (T j))
    (hs : ∀ i ∈ I, T i ⊆ S) (hk : ∀ i ∈ I, k ≤ (T i).card) : I.card * k ≤ S.card := by
  calc I.card * k = ∑ _i ∈ I, k := by rw [Finset.sum_const, smul_eq_mul]
    _ ≤ ∑ i ∈ I, (T i).card := Finset.sum_le_sum hk
    _ = (I.biUnion T).card := (Finset.card_biUnion hd).symm
    _ ≤ S.card := Finset.card_le_card (Finset.biUnion_subset.2 hs)

/-- **Counting** [T]: `11 Γ > M` in units of `10⁻⁹`, with surplus `107864`. -/
theorem counting : (10999479944 : ℤ) < 11 * 999962528 ∧ 11 * 999962528 - 10999479944 = (107864 : ℤ) := by
  norm_num

/-- **Scaling lemma, arithmetic** [T]: `L / A = 31/8`. -/
theorem scaling_arith : ((191 : ℚ) / 50) / (764 / 775) = 31 / 8 := by norm_num

/-- **Scaling lemma, side form** [T]: a container of side `s ≤ 31/8`, scaled by `A = 764/775`, has side `≤ L`. -/
theorem scaling_side (s : ℝ) (h : s ≤ 31 / 8) : (764 / 775 : ℝ) * s ≤ 191 / 50 := by linarith

/-- A packing configuration witnesses `Fits`. -/
theorem fits_of_cfgPacking {s : ℝ} {z : Cfg} (hz : CfgPacking s z) : Fits 11 s :=
  ⟨fun i => (z i).set, hz.2⟩

/-- The axiom implies Theorem 1 (`s(11) ≥ 3.82`). -/
theorem lb382_of_threshold : ∀ s : ℝ, Fits 11 s → (191 / 50 : ℝ) ≤ s := fun s hs => by
  have := threshold_bound_31_8 s hs
  linarith

/-- The shrunk window `W' = [31/8, ŝ]`. -/
def wnd' : Set ℝ := Icc (31 / 8 : ℝ) shat

theorem wnd'_subset_wnd : wnd' ⊆ wnd := fun s hs => ⟨by linarith [hs.1], hs.2⟩

/-- **Window restriction** [T from the axiom]: a statement about packings at sides in `[191/50, b]` follows from
its restriction to `[31/8, b]`, for any upper end `b` and any predicate `P`. -/
theorem window_restrict (b : ℝ) (P : ℝ → Prop)
    (h : ∀ s ∈ Icc (31 / 8 : ℝ) b, Fits 11 s → P s) : ∀ s ∈ Icc (191 / 50 : ℝ) b, Fits 11 s → P s :=
  fun s hs hf => h s ⟨le_of_lt (threshold_bound_31_8 s hf), hs.2⟩ hf

/-- `stratum_kill` needs only `W'` [T from the axiom]. -/
theorem stratum_kill_of_wnd'
    (h : ∀ i : StratumIdx, i ≠ trumpStratum → ∀ s ∈ wnd', ∀ z : Cfg, CfgPacking s z → ¬InStratum i s z) :
    ∀ i : StratumIdx, i ≠ trumpStratum → ∀ s ∈ wnd, ∀ z : Cfg, CfgPacking s z → ¬InStratum i s z :=
  fun i hi s hs z hz =>
    h i hi s ⟨le_of_lt (threshold_bound_31_8 s (fits_of_cfgPacking hz)), hs.2⟩ z hz

/-- `trump_residual` needs only `W'` [T from the axiom]. -/
theorem trump_residual_of_wnd'
    (h : ∀ s ∈ wnd', ∀ z : Cfg, CfgPacking s z → InStratum trumpStratum s z →
      ∃ (z' : Cfg) (f : RP → RP) (e : Equiv.Perm (Fin 11)),
        IsCtrSym s f ∧ CfgPacking s z' ∧ InBasin z' ∧ ∀ j, (z (e j)).set = f '' (z' j).set) :
    ∀ s ∈ wnd, ∀ z : Cfg, CfgPacking s z → InStratum trumpStratum s z →
      ∃ (z' : Cfg) (f : RP → RP) (e : Equiv.Perm (Fin 11)),
        IsCtrSym s f ∧ CfgPacking s z' ∧ InBasin z' ∧ ∀ j, (z (e j)).set = f '' (z' j).set :=
  fun s hs z hz =>
    h s ⟨le_of_lt (threshold_bound_31_8 s (fits_of_cfgPacking hz)), hs.2⟩ z hz

#print axioms budget_lemma
#print axioms window_restrict
#print axioms stratum_kill_of_wnd'

end PackingCert.S11.OpenLemmas.ThresholdBound
