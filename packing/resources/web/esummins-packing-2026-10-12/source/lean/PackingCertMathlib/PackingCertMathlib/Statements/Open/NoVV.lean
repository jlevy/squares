import Mathlib.LinearAlgebra.Span.Basic
import PackingCertMathlib.Sideband

/-!
# -- OPEN: Lemma NO-VV — a loaded vertex-on-vertex contact between non-parallel squares (A235)

`docs/proofs/no_vv.md`.  The PI (2026-09-15, 20:20): "if you epsilon-perturb ALL the dimensions and let
it relax, the point-on-point configuration won't survive; point-on-side is absolutely valid".

**The geometry (prose [T], `no_vv.md` §1).**  Two non-parallel unit squares `A`, `B` with disjoint
interiors touch in at most ONE point `P`; if `P` is a vertex of both (a VV contact) then exactly one
edge `e` of `A` through `P` and exactly one edge `f` of `B` through `P` are separating lines, so the pair
contributes exactly two tight separating-axis rows, `g_A` (`B`'s vertex against the line of `e`) and
`g_B` (`A`'s vertex against the line of `f`), and near the contact the pair is interior-disjoint iff
`g_A ≥ 0 ∨ g_B ≥ 0` — a UNION of two half-spaces (a reflex corner), not their intersection.

**The two-selection principle (prose [T], D1 / D3′).**  A local minimiser of the side is a local
minimiser of `NLP(S_A)` and of `NLP(S_B)`, so it carries Fritz-John multipliers for BOTH: the contact
force at `P` is realisable along `n_e` alone in one balanced stress and along `n_f` alone in another.

**The Lean content of this file — the independent-rows core.**  Write `e = e_s` (the side's gradient),
`v r` (`r ∈ ι`) for the gradients of the other active rows, `vA = ∇g_A`, `vB = ∇g_B`.  If
`e = Σ λ_r v_r + a·vA` (a multiplier of `NLP(S_A)`) and `e = Σ μ_r v_r + b·vB` (one of `NLP(S_B)`) and
`vA` is NOT in the span of the other rows and `vB`, then `a = 0` (`no_vv_of_not_mem_span`); symmetric
for `b`; both at once under both non-membership hypotheses (`no_vv_pair`).  Hence
**Corollary NO-VV-IND**: when the active rows at the minimiser are linearly independent (the generic,
"epsilon-perturbed" situation), the VV contact carries NO load in any multiplier.  No sign condition
on `λ`, `μ`, `a`, `b` is needed for this core; the packing content is in the two prose principles above.

**What is NOT proved (`no_vv.md` §3, [C]).**  When `∇g_A` lies in the span of the other rows (an
over-braced contact: a triple point or a closed contact loop through `P`) both selections can be KKT, and
the rolling family about `P` is blocked at first order by the other loads on `A` and `B` at 48 of the 55
loadable tilted VV contacts of the HELD / CROWD witnesses (the ring's 4|6 among them), so Theorem SO's
second-order test does not reach them; the free-problem census (0 loaded tilted VV at 883 genuine
Fritz-John points) is consistent with NO-VV but not explained by the local tests.

**Status (2026-09-15).**  Theorems below: proved (no new axiom).  The geometric core (VV-AXES) and the
two-selection principle are prose; no Lean object for the NLP multipliers exists in the readable layer.
-/

namespace PackingCert.S11.OpenLemmas

open Submodule

/-- **Lemma NO-VV, the independent-rows core.**  Two representations of the same vector `e` over the row
gradients `v`, one using `vA` (coefficient `a`) and one using `vB` (coefficient `b`): if `vA` is not in the
span of the other rows together with `vB`, its coefficient `a` vanishes. -/
theorem no_vv_of_not_mem_span {ι V : Type*} [Fintype ι] [AddCommGroup V] [Module ℝ V]
    (v : ι → V) (vA vB e : V) (lam mu : ι → ℝ) (a b : ℝ)
    (hA : e = (∑ r, lam r • v r) + a • vA) (hB : e = (∑ r, mu r • v r) + b • vB)
    (hspan : vA ∉ span ℝ (Set.range v ∪ {vB})) : a = 0 := by
  by_contra ha
  apply hspan
  have h1 : a • vA = (∑ r, mu r • v r) + b • vB - ∑ r, lam r • v r := by
    rw [← hB, hA]
    abel
  have h2 : (∑ r, mu r • v r) + b • vB - ∑ r, lam r • v r = (∑ r, (mu r - lam r) • v r) + b • vB := by
    simp only [sub_smul, Finset.sum_sub_distrib]
    abel
  have key : vA = a⁻¹ • ((∑ r, (mu r - lam r) • v r) + b • vB) := by
    rw [← h2, ← h1, smul_smul, inv_mul_cancel₀ ha, one_smul]
  rw [key]
  refine smul_mem _ _ (add_mem (sum_mem fun r _ => smul_mem _ _ ?_) (smul_mem _ _ ?_))
  · exact subset_span (Set.mem_union_left _ ⟨r, rfl⟩)
  · exact subset_span (Set.mem_union_right _ (Set.mem_singleton vB))

/-- **Corollary NO-VV-IND (both rows).**  If neither VV row lies in the span of the remaining rows, the
contact is unloaded in both selections' multipliers. -/
theorem no_vv_pair {ι V : Type*} [Fintype ι] [AddCommGroup V] [Module ℝ V]
    (v : ι → V) (vA vB e : V) (lam mu : ι → ℝ) (a b : ℝ)
    (hA : e = (∑ r, lam r • v r) + a • vA) (hB : e = (∑ r, mu r • v r) + b • vB)
    (hspanA : vA ∉ span ℝ (Set.range v ∪ {vB})) (hspanB : vB ∉ span ℝ (Set.range v ∪ {vA})) :
    a = 0 ∧ b = 0 :=
  ⟨no_vv_of_not_mem_span v vA vB e lam mu a b hA hB hspanA,
   no_vv_of_not_mem_span v vB vA e mu lam b a hB hA hspanB⟩

#print axioms no_vv_of_not_mem_span
#print axioms no_vv_pair

end PackingCert.S11.OpenLemmas
