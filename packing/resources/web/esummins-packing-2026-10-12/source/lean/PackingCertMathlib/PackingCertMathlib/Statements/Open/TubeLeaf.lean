import PackingCertMathlib.Composition

/-!
# -- OPEN: Lemma TUBE-LEAF — a fully named node inside the tube radii is a (D) leaf (A212)

**What it asserts** (`attempts/A212-trump5-tree/notes/trump5_tree.md` §2).  Let `N` be a
pad-0 node at `s₀` all of whose eleven squares are named, `g ∈ D4`, and suppose every piece of
every named role lies within `(r_c′, r_θ)` of its assigned square of the embedded image
`g·ẑ` dilated to `s₀`, with `r_c′ = r_c − 2(s₀ − ŝ)`.  Then for every `m ∈ [ŝ − T, ŝ]` and every
packing `P′` at side `m` whose dilate `Δ_{s₀/m} P′` satisfies `N`, the configuration `g⁻¹P′`
(after the relabelling) is a point of the scale-ray tube `Tube_scale(T, r)` at side `m` — so by
Theorem T1 (`Statements/Tube.lean`) `m = ŝ` and `P′ = g·ẑ`: the node holds the Trump image and
nothing else (`TRUMP-TUBE`, not a kill).  The proof is three lines: `c_{P′} = (m/s₀) c_F`, and
`|c_{P′} − (m/ŝ) ĉ| ≤ r_c′ + 2(s₀ − ŝ) = r_c`; tilts are unchanged by the dilation.

**The Lean shape.**  Exactly the `dOK` field of `ZoneTree.ClosedTree` for the leaf predicate
`N` — the form `Composition.classKilledAt_of_tree` consumes.  `TubeSeam.seam_inTube` (Lemma
SEAM) already proves the `g = 1` case with the free/pinned split (`I = ∅` here); what is missing
is the `D4` transport (`d4Cfg` commutes with the dilation about the origin up to the side) and
the relabelling bookkeeping.

**Status (2026-09-14).**  [T] in prose; the tube leaf of A212's trump5 tree, consumed with
`certs/tube_scale_T5.71e-2_window.json` (`T = 571/10000`, `r_c = 1/625`, `r_θ = 21/10000`).
-/

namespace PackingCert.S11.OpenLemmas

open Set Rigid

/-- **[OPEN] Lemma TUBE-LEAF.**  A node localised within the tube radii of `g·ẑ` satisfies the
(D)-leaf obligation of a closed zone-tree. -/
axiom lemma_TUBE_LEAF {tc : TubeCert} (ht : checkTube Data.a22 tc = true) {s0 : ℝ}
    (hs0 : shatR ≤ s0) (g : D4) (N : Cfg → Prop) {rc' : ℝ}
    (hrc : rc' + 2 * (s0 - shatR) ≤ (tc.rC : ℝ))
    (hN : ∀ F : Cfg, N F → ∃ e : Equiv.Perm (Fin 11), ∀ i,
      |(d4Cfg s0 g F (e i)).cx - (s0 / shatR) * (zhatCfg i).cx| ≤ rc' ∧
      |(d4Cfg s0 g F (e i)).cy - (s0 / shatR) * (zhatCfg i).cy| ≤ rc' ∧
      |thetaOf (d4Cfg s0 g F (e i)).t - thetaOf (zhatCfg i).t| ≤ (tc.rT : ℝ)) :
    ∀ (P : Cfg) (m : ℝ), shatR - (tc.T : ℝ) ≤ m → m ≤ shatR → CfgPacking m P →
      N (dil s0 m P) →
      ∃ (e : Equiv.Perm (Fin 11)) (Q : Cfg),
        (∀ j, (Q j).set = (d4Cfg m g P (e j)).set) ∧ (∀ j, (Q j).t ∈ Icc (0 : ℝ) 1) ∧
        InTube zhatVec (vR tc) tc.T (radR tc) (mkVec Q m)

#print axioms lemma_TUBE_LEAF

end PackingCert.S11.OpenLemmas
