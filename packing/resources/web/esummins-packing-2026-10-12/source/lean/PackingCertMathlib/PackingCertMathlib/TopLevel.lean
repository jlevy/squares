import Mathlib.Data.Real.Basic
import Mathlib.Data.Set.Prod
import Mathlib.Order.Interval.Set.Basic
import Mathlib.Order.ConditionallyCompleteLattice.Basic
import Mathlib.Topology.Instances.Real.Lemmas
import Mathlib.Tactic
import PackingCertMathlib.Bridge
import PackingCertMathlib.Parametrize
import PackingCertMathlib.Measure382
import PackingCertMathlib.Attain
import PackingCertMathlib.ThetaT
import PackingCertMathlib.Census
import PackingCertMathlib.CidlBridge
import PackingCertMathlib.Rigidity

/-!
# The composed optimality theorem for s(11) — formal STATEMENT (A62, checklist item F3)

This file states the top-level theorem of the optimality programme —

  `s(11) = ŝ`, the second real root of
  `x⁸ − 20x⁷ + 178x⁶ − 842x⁵ + 1923x⁴ − 496x³ − 6754x² + 12420x − 6865`,
  with equality attained, up to a symmetry of the container and a relabelling,
  only by Trump's configuration —

with every leaf family of the current proof plan as a NAMED `axiom`.  Nothing beyond the
composition glue is proved here; `#print axioms` on the three theorems at the bottom lists
exactly the declared hypotheses (plus `propext, Classical.choice, Quot.sound` from Mathlib).
Each axiom carries, in its docstring, the lab artefact that is supposed to discharge it and
its status as of 2026-09-02 (A64).  Discharging an axiom = replacing it by a
definition/theorem without changing any statement that mentions it.  Discharged so far:
`shat`/`shat_spec` and `rBasin` (A63); `parametrize` (A64, `Parametrize.lean`) and
`lb_382` (A64, `MeasureBridge.lean` + `Measure382.lean` — the measure bridge formalised,
so `s(11) ≥ 3.82` is an end-to-end Lean theorem whose only extra axiom is
the `native_decide` evaluation axiom); `trump_packs_at_shat` (A64) is now a theorem
from the finer split `shatA22` + `trump_packs_at_shatA22` (certified) +
`shatA22_eq_shat` (the open identity); `attained` (A68, `Attain.lean` — drain lemma D1,
compactness in coordinates); `shatA22_eq_shat` (A78 T2, obligation CIDL-LEAN —
`CidlCheck.lean` + `CidlBridge.lean` replay `certs/cidl_identity.json`, so the algebraic
identity is machine-checked and only A22's *certified content* is assumed, now as the
single axiom `a22_exact_structure`); the census layer `StratumIdx` / `trumpStratum` /
`InStratum` (A78 T1, `Census.lean` — definitions) and with it `stratify` and
`unique_transfer` (A78 T1/T4 — theorems from census exhaustiveness,
`unique_transfer.md` §1; the honest chain + Theorem U route is `UniqueChain.lean`).
Then A79 (`Rigidity.lean`): `zhat` and `shatA22` are DEFINITIONS (the unique zero of
A22's contact system in `box(z0, 1e-50)`, by the Lean replay of the Krawczyk certificate —
θ frame, certified Taylor trigonometry, `native_decide` on `checkA22`),
`trump_packs_at_shatA22` and `basin` are THEOREMS (feasibility of ẑ; the A36 universal
basin certificate's (V′) chain + A22 §5's Farkas optimality + the θ↔t transfer) — the
mpmath.iv trust item (TCB T3 / checklist F6) is gone at both tiers.
**3 named axioms remain** (was 12): the two genuinely-open leaf families
`stratum_kill`, `trump_residual`, and the A22 interface axiom `a22_exact_structure`
(the exact structure of ẑ on the CIDL slice; now an axiom ABOUT the defined `zhat`,
its content within reach of `Rigidity.lean`'s witness lemmas — no axiom of this file
carries open ALGEBRA).

The point of the file (per `docs/publication_checklist.md` F3) is to force the definition of
"packing", the quantifier order, and the exact form of each leaf obligation.  Every ambiguity
this forced is recorded in `attempts/A62-trust-ledger/notes/findings.md` (F-numbered) and the
load-bearing ones are repeated in the docstrings below.

## Definitional debt (opaque layers, declared as axioms)

* `StratumIdx / trumpStratum / InStratum` — DISCHARGED (A78, `Census.lean`): the Young-form
  skeleton census is a Lean DEFINITION (`skeleton`, `censusL`, `classCodes`, the D4 action);
  `StratumIdx` is the index type of the 163 class representatives, `InStratum i s z` is
  "the skeleton of `z` at side `s` is a D4-image of representative `i`" (EXACT class
  membership, as the `stratum_kill` docstring requires), `trumpStratum` the class of
  `((2,1),(1),(1),∅)`.  Census exhaustiveness (`skeleton_mem_census`, A53 L3) then proves
  `stratify` and `unique_transfer` below (unique_transfer.md §1).
* `shat` — DISCHARGED (A63): a definition (unique octic root in the isolating interval),
  with `shat_spec` a theorem; certificate `certs/octic_root_isolation.json` +
  `certs/verify_sturm.py` (checklist S3).
* `zhat` — DISCHARGED (A79): a DEFINITION, the unique zero of A22's contact system in
  `box(z0, 1e-50)` (`Rigidity.lean`, `Rigid.zhatCfg`; the certificate is replayed in the
  θ frame with certified Taylor trigonometry — no `t` re-emission was needed); the
  ŝ_A22 = ŝ identification gap remains `shatA22_eq_shat` (A78, `docs/proofs/attainment_ub.md`).
* `rBasin` — DISCHARGED (A63): a definition, 3/2000, justified by the exact θ↔t transfer
  constants (`docs/proofs/theta_t_transfer.md`).

## A86 roster note (Lean wave 7, 2026-09-03): what each remaining axiom now reduces to

The three named axioms are UNCHANGED here (no statement that mentions them moves), but
`Composition.lean` re-bases both consumers on the tree/tube conclusions, so that:

* `stratum_kill` (non-Trump classes) and `trump_residual` (the Trump class) are together
  REPLACED, for `s_eleven_ge_of_classes` / `s_eleven_unique_of_classes`, by the single
  per-class window obligation `ClassKilledAt i m` ("every packing of class `i` at side `m`
  has `m ≥ ŝ`, and at `m = ŝ` is a `D4`-image of `ẑ`"); the old axioms imply it
  (`classKilledAt_of_stratum_kill`, `classKilledAt_trump_of_residual`).  Each instance
  reduces (`classKilledAt_of_tree` + `classKilledAt_of_slabs`) to CERTIFICATE-FILE facts:
  a closed zone-tree (`ZoneTree.ClosedTree`: (K)/(N) leaves = `checkCaseI … = true` at
  `s0` with the node cores/NO-families, (C) leaves, (D) leaves = the landing bookkeeping
  of Lemma SEAM (`TubeSeam.seam_inTube`), (D′) leaves = `checkAtlas … = true` with
  `L ≥ s0`, and the tree's `cover` from the rule library), one tube certificate per
  direction (`RigidTube.tube_basin`, `checkTube … = true`), Step 1's slot/drift budget
  (`root_of_containsPins`), and, below the tube's reach, plain slab kills
  (`WindowRows.SlabKill`: `checkParamI` / slack-core `checkCaseI` / M1 rows).
  `basin` is no longer consumed on this route (the tube hands over to `a22_optimal'`).
* `a22_exact_structure` is untouched (A78's A22 interface; `shatR = shat` via CIDL).
* The `stratum_kill` re-split of `lean/k0_readiness_A85.md` (`StratumKillAll` /
  `StratumKillMin`) is stated and both consumers are proved from it
  (`s_eleven_ge_of_split`, `s_eleven_unique_of_split`) — needed only if minimality-based
  (K0-ROT) leaves are used.

## A93 roster note (Lean wave 8, 2026-09-04): the k0 chain — what the axioms reduce to now

The three named axioms are again UNCHANGED.  `Composition.lean` (Theorem N, A92's re-based
k0_00 plan, `docs/proofs/k0_blocked_side.md` §3.3) adds a CLASS-BLIND route below a shell:

* **Lemma SLIDE is a theorem** (`Slide.slide_crowd`): under K0-O1 alone, EVERY packing at side
  `m ∈ [3.82, ŝ)` has, at every corner, two distinct squares meeting the closed box
  `[0, 1 − (ŝ − m)]²` (second intruder at depth `≥ ŝ − m`).  K0-O1 (`Composition.K0O1`) is
  k1_00's monotone slab kill `SlabKill {corner slot} 3.82 ŝ` at each corner — delivered by
  k1_00's closed tree (`slabKill_of_tree`, the tube slab) + its regime-1 slab kills
  (`WindowRows.SlabKill`).  Lemma K0-FREE (`Slide.k0free_kill`) is the `T = 0` case.
* **Lemma CW is a theorem** (`Crowd.crowd_sound`, `crowd_cert_kill`): a crowd certificate
  `C(δ, m_lo)` is FOUR Bool facts about two files — `checkCaseI` run A (`n ≤ 11 + 8e`, no
  cores, no NO-families), `checkCaseI` run B (no cores), `sameMeasure` (one measure, weights
  in the exact ratio `1 + e`), `crowdZones` (run B's NO-families avoid the crowd family
  `[0, a_w]²` at every corner; `CrowdZone.lean`) — plus rational side conditions (the pad
  `a_w ≥ (s0/m_lo)(1−δ) + (s0/m_lo − 1)·0.7072`, Lemma B-YES `scaleC_meets_cornerBox`; the
  separation `(s0 − 2a_w)² > 2`).  `crowdKill_of_files` packages them into
  `CrowdKill δ m_lo s0`; `lean/gen_crowd_lean.py` emits the isolated replay module per
  certificate (`Corpus/Crowd/Check_<tag>.lean`, `native_decide`).
* **Theorem N** (`theoremN_slab`, `chain_cover`, `no_packing_of_chain`): K0-O1 + a chain
  `(δ_k, m_k)`, `m_0 ≤ 3.82`, `m_{k+1} ≤ ŝ − δ_k`, exclude EVERY packing at every side
  `m ∈ [3.82, ŝ − δ_K]`; hence `s_eleven_ge_of_chain : s(11) ≥ ŝ − δ_K`, and
  `classKilledAt_below_of_chain : ClassKilledAt i m` for EVERY class `i` there.
* So `stratum_kill` now reduces to: (i) K0-O1 (k1_00's tree, A84 O1–O5 — the one tree the
  route needs); (ii) the chain's certificate replays; (iii) `ShellKill i δ_K` per class on
  the SHELL `(ŝ − δ_K, ŝ]` (`classKilledAt_of_chain`): for the certified classes and the
  K1-protected `k ≤ 4` tier, their A86-T3 trees/slabs restricted to the shell (the tube
  slab `[ŝ − 0.1305, ŝ]` contains it); for k0_00 it is RES-N(δ_K) — the named open residue
  (depgraph K0.RESN): a packing in the shell with two squares at depth `≥ ŝ − m` at every
  corner but not two at depth `≥ δ_K` at some corner, plus the non-crowded non-images at `ŝ`.
* `trump_residual` reduces to `ClassKilledAt trumpStratum m` on the shell only (A60's tree
  through `classKilledAt_of_tree`; below `ŝ − δ_K` the chain kills the Trump class too, so
  A60's regime-1 slab kills are no longer load-bearing).
* Replay obligations and the T5 cost law (A78 `t5_timings.jsonl`: 0.4–0.6 ms per box;
  K61 median 452 k boxes → 268 s, max 7.4 M boxes → 2 800 s): per crowd certificate two
  `checkCaseI` evaluations at depth 56 with ≤ 1 600 D4-expanded atoms (box counts from the
  chore's `.report.json`; expect minutes to ~1 h each), `sameMeasure` (< 1 s),
  `crowdZones` (≈ 420 zones × 4 corners × ≤ 2^fuel pose boxes, fuel 10: ≲ 1 min); a chain
  from δ = 0.05 to 0.005 is 3 certificates, to 0.001 is 5 (ratio 0.4403).  No certificate
  has been delivered by the A92 chore at this commit (LP sweep parked on the commit gate), so
  no replay module exists yet; the generator and the smoke tests
  (`scratch/A93CheckerTest.lean`) are in place.
-/

namespace PackingCert
namespace S11

noncomputable section

open Set

/-! ## The packing problem, set level

`container`, `IsPacking` and `Fits` live in `PackingCertMathlib/Parametrize.lean` since A64
(moved there unchanged, same namespace, so the measure bridge can consume them). -/

/-- `s(n)`, as an infimum (checklist S2).  `attained` below is the statement that the
infimum is a minimum (drain lemma D1). -/
def sPack (n : ℕ) : ℝ := sInf {s : ℝ | Fits n s}

/-! ## The packing problem, configuration level (tan-half parametrisation)

The configuration layer (`cosT`, `sinT`, `PSq`, `edir`, `baseCorner`, `PSq.set`)
lives in `PackingCertMathlib/Parametrize.lean` since A64 (moved there unchanged,
same namespace, so that the parametrisation lemma and the measure bridge can use
it without importing this statement file). -/

/-- A configuration: 11 parametrised squares — the 33 coordinates
`(cxᵢ, cyᵢ, tᵢ)` every certificate family speaks about. -/
abbrev Cfg := Fin 11 → PSq

/-- A configuration is a packing at side `s`. -/
def CfgPacking (s : ℝ) (z : Cfg) : Prop :=
  (∀ i, (z i).t ∈ Icc (0 : ℝ) 1) ∧ IsPacking 11 s fun i => (z i).set

/-! ## Symmetries of the container -/

/-- A symmetry of the container `[0,s]²`: a plane map that preserves squared Euclidean
distance and maps the container onto itself.  For `s > 0` these are exactly the 8 elements
of the dihedral group D₄, but the composition below never needs that classification. -/
structure IsCtrSym (s : ℝ) (f : RP → RP) : Prop where
  isometry : ∀ p q, sqdist (f p) (f q) = sqdist p q
  maps : f '' container s = container s

theorem IsCtrSym.comp {s : ℝ} {f g : RP → RP} (hf : IsCtrSym s f) (hg : IsCtrSym s g) :
    IsCtrSym s (f ∘ g) where
  isometry p q := by
    simp only [Function.comp_apply, hf.isometry, hg.isometry]
  maps := by rw [Set.image_comp, hg.maps, hf.maps]

/-! ## The algebraic value -/

/-- Trump's octic (A03; Ellsworth 2023). -/
def trumpOctic (x : ℝ) : ℝ :=
  x ^ 8 - 20 * x ^ 7 + 178 * x ^ 6 - 842 * x ^ 5 + 1923 * x ^ 4 - 496 * x ^ 3
    - 6754 * x ^ 2 + 12420 * x - 6865

/-- The Taylor expansion of the octic at `a = 3877083/1000000`: every coefficient above
degree 0 is POSITIVE (certificate `certs/octic_root_isolation.json`, checker
`certs/verify_sturm.py`), so the octic is strictly increasing on `[a, ∞)` by pure algebra —
no calculus enters the uniqueness argument. -/
private lemma trumpOctic_taylor (x : ℝ) :
    trumpOctic x =
      -(89907663116138493411101284007125861208828959 /
          1000000000000000000000000000000000000000000000000)
        + (19047448354002451638684536547366689841780627 /
            125000000000000000000000000000000000000000)
            * (x - 3877083 / 1000000)
        + (165507240204079365683276620593074875583 / 250000000000000000000000000000000000)
            * (x - 3877083 / 1000000) ^ 2
        + (140531576756507493150247963879501 / 125000000000000000000000000000)
            * (x - 3877083 / 1000000) ^ 3
        + (75650550884558810753780247 / 100000000000000000000000)
            * (x - 3877083 / 1000000) ^ 4
        + (31128529333060215509 / 125000000000000000)
            * (x - 3877083 / 1000000) ^ 5
        + (14024503122223 / 250000000000)
            * (x - 3877083 / 1000000) ^ 6
        + (1377083 / 125000)
            * (x - 3877083 / 1000000) ^ 7
        + (x - 3877083 / 1000000) ^ 8 := by
  unfold trumpOctic; ring

/-- The octic strictly increases to the right of `a = 3877083/1000000`. -/
private lemma trumpOctic_strictMono {x y : ℝ}
    (hx : (3877083 / 1000000 : ℝ) ≤ x) (hxy : x < y) : trumpOctic x < trumpOctic y := by
  rw [trumpOctic_taylor x, trumpOctic_taylor y]
  set u := x - 3877083 / 1000000 with hu_def
  set v := y - 3877083 / 1000000 with hv_def
  have hu : (0 : ℝ) ≤ u := by simp only [hu_def]; linarith
  have huv : u < v := by simp only [hu_def, hv_def]; linarith
  have huv' : u ≤ v := le_of_lt huv
  have h2 : u ^ 2 ≤ v ^ 2 := pow_le_pow_left₀ hu huv' 2
  have h3 : u ^ 3 ≤ v ^ 3 := pow_le_pow_left₀ hu huv' 3
  have h4 : u ^ 4 ≤ v ^ 4 := pow_le_pow_left₀ hu huv' 4
  have h5 : u ^ 5 ≤ v ^ 5 := pow_le_pow_left₀ hu huv' 5
  have h6 : u ^ 6 ≤ v ^ 6 := pow_le_pow_left₀ hu huv' 6
  have h7 : u ^ 7 ≤ v ^ 7 := pow_le_pow_left₀ hu huv' 7
  have h8 : u ^ 8 ≤ v ^ 8 := pow_le_pow_left₀ hu huv' 8
  linarith

private lemma trumpOctic_continuous : Continuous trumpOctic := by
  unfold trumpOctic; fun_prop

/-- **[S3 — root isolation, existence half]** sign change on the isolating interval. -/
private lemma trumpOctic_exists_root :
    ∃ x ∈ Icc (3877083 / 1000000 : ℝ) (3877084 / 1000000), trumpOctic x = 0 := by
  have hab : (3877083 / 1000000 : ℝ) ≤ 3877084 / 1000000 := by norm_num
  have hivt := intermediate_value_Icc hab trumpOctic_continuous.continuousOn
  have h0 : (0 : ℝ) ∈ Icc (trumpOctic (3877083 / 1000000)) (trumpOctic (3877084 / 1000000)) := by
    have ha : trumpOctic (3877083 / 1000000 : ℝ) < 0 := by unfold trumpOctic; norm_num
    have hb : 0 < trumpOctic (3877084 / 1000000 : ℝ) := by unfold trumpOctic; norm_num
    exact ⟨le_of_lt ha, le_of_lt hb⟩
  exact hivt h0

/-- **[S3 — root isolation]** the octic has exactly one root in `[3.877083, 3.877084]`.
Certificate: `certs/octic_root_isolation.json` (Sturm; the octic has exactly TWO real
roots, the other in `(-2, -1)`, so this root is the SECOND real root, as the theorem
statement requires), checker `certs/verify_sturm.py` (exact rational arithmetic, stdlib
only).  The Lean proof is certificate-free: IVT for existence, the all-positive Taylor
shift for uniqueness. -/
theorem trumpOctic_existsUnique :
    ∃! x : ℝ, x ∈ Icc (3877083 / 1000000 : ℝ) (3877084 / 1000000) ∧ trumpOctic x = 0 := by
  obtain ⟨x, hx, hfx⟩ := trumpOctic_exists_root
  refine ⟨x, ⟨hx, hfx⟩, ?_⟩
  rintro y ⟨hy, hfy⟩
  by_contra hne
  rcases lt_or_gt_of_ne hne with h | h
  · have := trumpOctic_strictMono hy.1 h
    rw [hfy, hfx] at this
    exact lt_irrefl 0 this
  · have := trumpOctic_strictMono hx.1 h
    rw [hfx, hfy] at this
    exact lt_irrefl 0 this

/-- **ŝ = 3.877083590022813…**, the value of `s(11)`: the unique (and second real) root of
the octic in `[3.877083, 3.877084]`.  A DEFINITION since A63 (was an axiom); tied to the
octic by the theorem `shat_spec` below. -/
noncomputable def shat : ℝ := trumpOctic_existsUnique.choose

/-- **[S3 — root isolation]** ŝ is the unique root of the octic in `[3.877083, 3.877084]`.
DISCHARGED (A63): was an axiom; now proved from `trumpOctic_existsUnique`
(certificate `certs/octic_root_isolation.json` + `certs/verify_sturm.py` document the
Sturm count and the second-root index; the Lean proof itself needs neither).
Findings F7 closed. -/
theorem shat_spec :
    trumpOctic shat = 0 ∧ shat ∈ Icc (3877083 / 1000000 : ℝ) (3877084 / 1000000) ∧
      ∀ x ∈ Icc (3877083 / 1000000 : ℝ) (3877084 / 1000000), trumpOctic x = 0 → x = shat := by
  obtain ⟨⟨hmem, hroot⟩, huniq⟩ := trumpOctic_existsUnique.choose_spec
  exact ⟨hroot, hmem, fun x hx hfx => huniq x ⟨hx, hfx⟩⟩

/-- The window on which every per-stratum obligation is stated: `[3.82, ŝ]`.
The lower end is Theorem 1 (`lb_382`); certificates are produced on the rational
superset `[191/50, 969271/250000]` (A56's window), which contains this one. -/
def wnd : Set ℝ := Icc (191 / 50 : ℝ) shat

/-! ## The named hypotheses (the leaf families of the proof plan) -/

theorem shat_ge_382 : (191 / 50 : ℝ) ≤ shat := by
  have h := shat_spec.2.1.1
  norm_num at h ⊢
  linarith

theorem shat_mem_wnd : shat ∈ wnd := ⟨shat_ge_382, le_refl _⟩


/-- **[D1 — attainment]** `{s | Fits 11 s}` has a least element.  DISCHARGED (A68): was an
axiom; now the theorem `attained_thm` of `PackingCertMathlib/Attain.lean`
(`docs/proofs/drain_lemma.md` D1).  No Hausdorff limits: the coordinate feasible region
(33 square coordinates + the side, cut out by `t ∈ [0,1]`, the `set_subset_container_iff`
containment inequalities and pairwise non-overlap) is closed and bounded, the side
projection continuous; non-overlap is closed because the interior of a parametrised
square is EXACTLY the open `u/v` box (`mem_interior_iff_uv`).  Axioms: `propext,
Classical.choice, Quot.sound` only. -/
theorem attained : ∃ m, IsLeast {s : ℝ | Fits 11 s} m := attained_thm

/-!
**[parametrisation]** — every set-level packing is represented by a configuration
(`parametrize`).  DISCHARGED (A64): was an axiom here; now a THEOREM in
`PackingCertMathlib/Parametrize.lean` (the square's own 90° symmetry `sqSet_rot` brings the
edge vector into the closed first quadrant, then the half-angle substitution
`t = e₂/(1+e₁) ∈ [0,1]` is exact algebra — no transcendental functions).
Prose: `docs/proofs/parametrization.md`.
-/

/-- **[Theorem 1 — s(11) ≥ 3.82]** DISCHARGED (A64): was an axiom; now the end-to-end
theorem `s_eleven_ge_382` (`Measure382.lean`): the `native_decide` evaluation of
`checkMeasureI` on `certs/measure_certificate_3.82.json` composed with the FORMALISED
measure bridge (`MeasureBridge.lean` — checker soundness: interval arithmetic, grid
trigonometry, clip/sift/split/branch-and-bound, coverage, and the scaling/counting
argument; was the A28 §7 item 4 prose, checklist F2).  Axioms: `propext,
Classical.choice, Quot.sound, Lean.ofReduceBool`. -/
theorem lb_382 : ∀ s : ℝ, Fits 11 s → (191 / 50 : ℝ) ≤ s := s_eleven_ge_382

/-- **[UB at ŝ exactly]** Trump's configuration.  SPLIT by A64 into its certified and open
parts (the A63 route decision, executed Lean-side): route (a) — A22 Krawczyk existence +
FEASIBILITY — certifies `Fits ŝ_A22` for the INTRINSIC side `shatA22` of the contact
solution (`trump_packs_at_shatA22` below); the whole algebraically-open residue is the
single identity axiom `shatA22_eq_shat`.  Route (b) remains REFUTED as a finite route
(`docs/proofs/attainment_ub.md` §2).
DISCHARGED (A79): a DEFINITION — `Rigid.zhatCfg`, the unique zero of the curated 34-row
contact system in `box(z0, 1e-50)` (`Rigid.krawczyk_sound`, Banach on the true box), read
in the half-angle parametrisation `t = tan(θ̂/2)`. -/
noncomputable def zhat : Cfg := Rigid.zhatCfg

/-- **[UB at ŝ — intrinsic side]** The side of A22's unique contact solution ẑ in the
Krawczyk box `N = box(z0, 5e-4)`: `‖ẑ − z0‖∞ ≤ 1e-50`, and ẑ IS a packing at its own
side (A22 §4 feasibility).  DISCHARGED (A79): a DEFINITION, `Rigid.shatR = ẑ_33`; the
mpmath.iv trust item (TCB T3 / checklist F6) is gone at both tiers — the Lean replay stays
in the θ frame with certified Taylor trigonometry (`RigidityCheck.lean`). -/
noncomputable def shatA22 : ℝ := Rigid.shatR

/-- See `shatA22`: A22 feasibility, i.e. `Fits 11 shatA22` in configuration form.
DISCHARGED (A79): a THEOREM (`Rigid.zhatCfg_packing` — interval SAT for the 41
non-contact pairs, exact half-plane separation for the contact pairs, and the
exact-structure witnesses searched in `S` for the flush pairs and the dropped wall rows;
axioms `propext, Classical.choice, Quot.sound` + the `native_decide` evaluation of
`checkA22`). -/
theorem trump_packs_at_shatA22 : CfgPacking shatA22 zhat := Rigid.zhatCfg_packing

/-- **[UB at ŝ — A22's certified content on the exact-structure slice]**
The A22 interface axiom that REPLACES the former opaque identity axiom
`shatA22_eq_shat` (A78 T2, obligation CIDL-LEAN, `docs/proofs/attainment_ub.md` §7.5).
It asserts nothing algebraic: only what A22's certificate already establishes about the
point `P̂` (`attempts/A22-local-rigidity/notes.md` headline items 1–3, and the
composition paragraph of `certs/verify_cidl.py`'s docstring):

1. **the tilt is in the gate interval.**  A22's second Krawczyk system `F̃` encloses the
   common angle `θ̂` of squares 6–10 within 1e-50 of the A03 rational angle
   `0.70130710554614222…`, so `θ̂/2 ∈ [0.35, 0.351]`; with `x ≤ tan x ≤ x + x³/(3(1−x²))`
   there, `t̂ = tan(θ̂/2) ∈ [0.35, 0.3672] ⊂ [3/10, 2/5]`.
2. **the side is in the octic's isolating interval.**  `ŝ_A22` is within 1e-50 of the A03
   rational side `3.87708359002281417…` (4.1e-7 clearance to both ends).
3. **the 13 reduced contact rows vanish at `P̂`.**  A22 item 2 pins the EXACT structure of
   ẑ (squares 0–5 axis-parallel at `(½,½), (3/2,½), (S−½,½), (½,3/2), (½,y4),
   (S−½,S−½)`; squares 6–10 sharing exactly one angle θ̂), and all 38 curated constraint
   rows vanish at ẑ (A22 §3).  Substituting the structure and `t = tan(θ/2)` and clearing
   the positive factors `(1+t²)^k` turns the 18 surviving rows into the 13 distinct
   polynomial generators `Cidl.gens` — REBUILT in `CidlGen.lean` from A22's own
   corner/edge conventions, byte-for-byte the construction of `certs/verify_cidl.py`.

The 13 coordinates are, in `certs/verify_cidl.py`'s `VARS` order,
`(t, y4, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10, S)` = the common tilt of squares 6–10,
square 4's centre height, the five tilted centres, and the side.

TCB: exactly A22's (mpmath.iv Krawczyk + the A70 exact-rational re-check
`a22_recheck_exact.py`).  NO algebra is assumed: the ideal-membership identity
`e(t)·Δ(t)⁸·octic(S) = Σ_j q_j(t,S)·G_j` and both sign gates are machine-checked
(`CidlCheck.lean`, `native_decide` over ℚ) and composed in `CidlBridge.lean`. -/
axiom a22_exact_structure :
    (zhat 6).t ∈ Icc (3 / 10 : ℝ) (2 / 5) ∧
      shatA22 ∈ Icc (3877083 / 1000000 : ℝ) (3877084 / 1000000) ∧
      ∀ g ∈ Cidl.gens, Cidl.eval g
        (Cidl.pt13 (zhat 6).t (zhat 4).cy (zhat 6).cx (zhat 6).cy (zhat 7).cx (zhat 7).cy
          (zhat 8).cx (zhat 8).cy (zhat 9).cx (zhat 9).cy (zhat 10).cx (zhat 10).cy
          shatA22) = 0

/-- **[UB at ŝ — the algebraic identity]** `ŝ_A22 = ŝ_octic`.  A THEOREM since A78 T2
(obligation CIDL-LEAN of `docs/proofs/attainment_ub.md` §7.5 — DISCHARGED; was an axiom).

Route: `Cidl.octic_zero_of_generators` (`CidlBridge.lean`) is the composed content of the
(c-idl) saturated ideal-membership certificate `certs/cidl_identity.json` — the identity

    e(t)·Δ(t)⁸·octic(S) = Σ_j q_j(t,S)·G_j

over the 13 reduced A22 contact rows, replayed in Lean by `native_decide` over ℚ with the
generators REBUILT from A22's conventions, plus the sign gates `e < 0` and `Δ < 0` on
`[3/10, 2/5]` (a monomial interval bound — strictly stronger than the checker's Sturm
"no root", and certified by the same evaluation).  Feeding it `a22_exact_structure`
gives `trumpOctic ŝ_A22 = 0`; `shat_spec`'s uniqueness on `[3.877083, 3.877084]` then
gives `ŝ_A22 = ŝ`, the octic's SECOND real root (the other lies in `(−2,−1)`).

En route A69 DERIVED the tan-half minimal polynomial
`5t⁸−10t⁷−2t⁶+14t⁵+12t⁴−6t³+2t²+2t−1` (upgrading A22 §7 gap 2), and A53 L4's
"degree-7 coordinate / compositum 56" obstacle is VOID (spurious A03 minpoly
annotations; every ẑ-coordinate lies in ℚ(t̂), degree 8). -/
theorem shatA22_eq_shat : shatA22 = shat := by
  obtain ⟨ht, hs, hg⟩ := a22_exact_structure
  have hoct : Cidl.octicR shatA22 = 0 :=
    Cidl.octic_zero_of_generators _ _ _ _ _ _ _ _ _ _ _ _ _ hg ht.1 ht.2
  refine shat_spec.2.2 shatA22 hs ?_
  simpa only [trumpOctic, Cidl.octicR_eq] using hoct

/-- The composed upper-bound-at-ŝ statement — a THEOREM from the split (A64); its
`#print axioms` separates the certified feasibility from the certified identity. -/
theorem trump_packs_at_shat : CfgPacking shat zhat :=
  shatA22_eq_shat ▸ trump_packs_at_shatA22

/-- **[census]** Index type of the stratification: the D4 class representatives of the
Young-form census (`Census.lean`: `classCodes`, the distinct canonical codes of the 1110
census tuples — 163 of them, `CensusCheck.lean`).  DISCHARGED (A78): was an opaque axiom;
checklist F11/H2. -/
def StratumIdx : Type := Fin classCodes.length

/-- Trump's tuple lies in the census (kernel `decide`), hence its canonical code is one of
the class codes. -/
theorem trumpCode_mem : canonCode trumpPins ∈ classCodes :=
  List.mem_dedup.mpr (List.mem_map.mpr
    ⟨trumpPins, mem_censusL_of_isCensusTuple trumpPins_isCensusTuple, rfl⟩)

/-- The distinguished stratum: Trump's `k = 5` skeleton class (`trump5`,
`((2,1),(1),(1),∅)` up to D4; `trumpPins`).  DISCHARGED (A78): a definition. -/
def trumpStratum : StratumIdx :=
  ⟨classCodes.idxOf (canonCode trumpPins), List.idxOf_lt_length_of_mem trumpCode_mem⟩

/-- `InStratum i s z`: the configuration `z`, as a packing at side `s`, has skeleton
EXACTLY of class `i` — its Young-form skeleton at side `s` (`skeleton s z`, the largest
Young set of exactly-on-grid axis-aligned squares at each corner, A53 L1) is a D4-image of
the class representative `classRep i`.  DISCHARGED (A78): a definition.  The side
parameter is essential: skeleton pins are anchored to the walls of `[0,s]²`, so the
predicate is a different subset of configuration space at every `s` — this is what makes
window transfer (H6) a per-certificate obligation rather than a bookkeeping step.
Findings F4/F6. -/
def InStratum (i : StratumIdx) (s : ℝ) (z : Cfg) : Prop :=
  InClassOf (skeleton s z) (classRep i)

/-- The window sits inside `(3, 4)`, where the census is one object (A53 L2(iv),
`Census.lean`). -/
theorem wnd_subset_Ioo {m : ℝ} (hm : m ∈ wnd) : 3 < m ∧ m < 4 := by
  obtain ⟨h1, h2⟩ := hm
  have h3 := shat_spec.2.1.2
  norm_num at h1 h3
  exact ⟨by linarith, by linarith⟩

/-- **Census exhaustiveness in composition form** (A53 L3, `skeleton_mem_census` +
`exists_class_skeleton`): every packing at a side in the window lies in some stratum. -/
theorem exists_stratum {m : ℝ} (hm : m ∈ wnd) {z : Cfg} (hz : CfgPacking m z) :
    ∃ i : StratumIdx, InStratum i m z :=
  exists_class_skeleton (wnd_subset_Ioo hm).1 (wnd_subset_Ioo hm).2 hz.2

/-- **[H1 + H2 — selection + exhaustiveness]** If the minimum is attained at
`m ∈ [3.82, ŝ]`, then SOME minimiser lies in some stratum.  DISCHARGED (A78): was an
axiom; now a theorem from `parametrize` + census exhaustiveness (`exists_stratum`).  As
STATED the selection content is empty — any minimiser has a skeleton — and the
k-maximal/teleport-stuck selection (`exists_kmax_skeleton`, `cc2_stuck_census` in
`CensusSelection.lean`) is consumed downstream by the H10-stuck route of
`stratum_kill`'s quantifier caveat, not here.  The uniqueness clause needs the separate
`unique_transfer` below (findings F3). -/
theorem stratify : ∀ m : ℝ, IsLeast {s : ℝ | Fits 11 s} m → m ∈ wnd →
    ∃ (z : Cfg) (i : StratumIdx), CfgPacking m z ∧ InStratum i m z := by
  intro m hm hw
  obtain ⟨Q, hQ⟩ := hm.1
  obtain ⟨z, hzt, hzQ⟩ := parametrize Q hQ
  have hz : CfgPacking m z := by
    refine ⟨hzt, ?_⟩
    have hfun : (fun i => (z i).set) = Q := funext fun i => (hzQ i).symm
    rw [hfun]
    exact hQ
  obtain ⟨i, hi⟩ := exists_stratum hw hz
  exact ⟨z, i, hz, hi⟩

/-- **[per-stratum kills, window form]** No packing at any side `s ∈ [3.82, ŝ]` has
skeleton exactly of a non-Trump class.  This single axiom fuses THREE obligations that are
separate artefacts in the lab, and the fusion is forced (A56 refuted "kill at s₀ + transfer
principle" as a factorisation — a general transfer axiom would be FALSE):
(1) the certificate kills — 61 exact pin-set certificates (k=3:1, k=4:8, k=5:19+2 via A57
    sub-trees, k=6:33) + K1 upward cap for k ≥ 7;
(2) window coverage — A56/A61 parametric 4-D certificates; 12 strata + the A57 sub-tree
    kills + 2 sliver bands are s₀-only as of this commit;
(3) the k ≤ 4 tier — the K1-protected classes ({k4_03, k4_05, k4_06, k4_08, k4_11,
    corners4} and the ten k ≤ 3 classes) can NEVER be killed by the pin-certificate route
    (A55 sharpness); their exclusion must come from the "exactly" in `InStratum` (skeleton
    maximality: A58 clear-corner/exchange route, checklist H10 — OPEN).
Certificates natively prove the monotone form "no packing whose skeleton CONTAINS these
pins"; the composition needs the exact-skeleton form; the bridge is K1 + the census
containment lattice and must become a written lemma (findings F4).
FOURTH fused obligation (findings F9, checklist S4): a `verify_case` PASS speaks about
families of pairwise-DISJOINT closed squares, while this axiom quantifies over
interior-disjoint packings (contacts allowed — the minimiser has them).
A63 STATUS UPDATE:
* (F9/S4) the λ-dilation bridge is now WRITTEN and proved:
  `docs/proofs/closed_disjoint_bridge.md` Lemma B + Corollary B′ (centre dilation to a
  certified rational side strictly above the packing's side; corpus containment margin
  ρ ≈ 1.0000009e-9, exactly positive, uniform across all 68 kill certificates).
* (F4) the monotone→exact bridge is written: `docs/proofs/instratum_bridge.md` (K1 +
  Lemma M→E); it covers exactly the certified classes, and records that the K1-protected
  tier is H10's business, in the target form H10-stuck (`unique_transfer.md` §3).
* (F6, SHARPENED) via Lemma B an s₀-only certificate reaches only sides within relative
  distance ~4e-10 below s₀ — i.e. NO side of `[3.82, ŝ]` at all (the gap to ŝ is
  ~1.06e-7 relative).  The window quantifier of this axiom is carried by parametric
  coverage + B′ for the 38(+A61) full-window classes; the A57 k5_11/k5_16 trees and any
  s₀-only stragglers instantiate NOTHING here until re-emitted (parametric form, or the
  slack-core fixed-side grid of `closed_disjoint_bridge.md` B.4).
* QUANTIFIER CAVEAT (A63, from `unique_transfer.md` §1): as stated this axiom quantifies
  over ALL packings.  For the K1-protected classes at `s = ŝ` that strength is equivalent
  to (a piece of) the uniqueness theorem and can never come from certificates; the
  non-circular discharge routes the uniqueness composition through teleport-stuck
  packings (H10-stuck) + Theorem U — see `unique_transfer.md`.  At sides `< ŝ` the
  low-k instances are needed only for the `stratify`-selected minimiser. -/
axiom stratum_kill : ∀ i : StratumIdx, i ≠ trumpStratum → ∀ s ∈ wnd, ∀ z : Cfg,
    CfgPacking s z → ¬InStratum i s z

/-- The basin radius (∞-norm, in `(cx, cy, t)` coordinates): **3/2000 = 1.5e-3**.
A DEFINITION since A63 (was an opaque axiom, findings F5).  Derivation
(`docs/proofs/theta_t_transfer.md` X.3): A36 certifies the basin at radius 37/10000 in
`(c, θ, s)`; a t-deviation ≤ 3/2000 gives a θ-deviation ≤ 3/1000 ≤ 37/10000 (X.1,
`|Δθ| ≤ 2|Δt|`), and the corner-perturbation bound `r·(1+√2) < 37/10000` (X.2) closes the
`∀ s` slab so that every case of the `basin` axiom below lands inside A36's certified
34-dim box.  The A60 residual tree's landing radius 4.45e-4 sits at 0.30 × this value. -/
noncomputable def rBasin : ℝ := 3 / 2000

/-- **X.3(a), machine-checked (A68)**: the tilt-transfer gate `2·rBasin ≤ h_A36`.
With `theta_lipschitz` (`ThetaT.lean`), a `t`-deviation ≤ `rBasin` is a θ-deviation
≤ `2·rBasin ≤ 37/10000`, inside A36's box radius. -/
theorem rBasin_gate_tilt : 2 * rBasin ≤ 37 / 10000 := gate_tilt

/-- **X.3(b), machine-checked (A68)**: the slab gate `rBasin·(1+√2) < h_A36` (the binding
condition of `docs/proofs/theta_t_transfer.md` X.3).  With `corner_perturb`
(`ThetaT.lean`, sharp constant `r_c + √2·r_t`), every corner coordinate of a
configuration inside the `rBasin` box moves by `< 37/10000`, which closes the `∀ s` slab
of the `basin` axiom against A36's certified box. -/
theorem rBasin_gate_slab : rBasin * (1 + Real.sqrt 2) < 37 / 10000 := gate_slab

/-- `z` lies in the certified rigidity box around Trump's configuration. -/
def InBasin (z : Cfg) : Prop := ∀ i,
  |(z i).cx - (zhat i).cx| ≤ rBasin ∧ |(z i).cy - (zhat i).cy| ≤ rBasin ∧
    |(z i).t - (zhat i).t| ≤ rBasin

/-- **[trump5 residual — A59/A60]** Every packing in the Trump stratum at side
`s ∈ [3.82, ŝ]` is, after a container symmetry and a relabelling, a packing landing inside
the rigidity basin.  STATUS: A60 campaign running (zone cover + residue ladders +
confinement, every kill an exact certificate); the low-`s` slab (H7/G-A59-7) and the
s-parametric form of the (K) leaves are open — as stated the axiom quantifies over the
whole window, which is exactly that open obligation.  A63 sharpening
(`closed_disjoint_bridge.md` B.2/B.4): the tree's s₀ kill certificates, with the library's
ε-fat pin cores (margin ~1e-9), instantiate at NO side of the window via the dilation
bridge; the named upgrade paths are parametric re-emission or the slack-core fixed-side
grid (pricing HELD pending A60's δ-re-emission test — its measured law is η ≤ −1, stricter
than A56's slack gate).  The confinement leaves (nonempty `nofams`, the only route for the
outer triple) transfer via Lemma B-NO (B.2″) as occupancy with the zone contracted by 1/λ —
downstream consumers must hypothesise the outward-widened zone.  Dilation transfers KILLS only, never this axiom's containment conclusion (the
pulled-back basin box misses `InBasin` by ~(λ−1)·|ĉ| ≫ rBasin) — D.SLAB stands.  The
`InBasin` target is now concrete: all 33 coordinates within 3/2000, mod G (A60's landing
radius 4.45e-4 = 0.30 × rBasin).  The symmetry/relabelling is produced by the D4 reduction
inside the tree (H12; machine-checked at 3.84, re-proof at s₀ listed as mechanical). -/
axiom trump_residual : ∀ s ∈ wnd, ∀ z : Cfg, CfgPacking s z → InStratum trumpStratum s z →
    ∃ (z' : Cfg) (f : RP → RP) (e : Equiv.Perm (Fin 11)),
      IsCtrSym s f ∧ CfgPacking s z' ∧ InBasin z' ∧ ∀ j, (z (e j)).set = f '' (z' j).set

/-- **[A22/A36 — local rigidity at Trump]** Inside the basin box: every packing side is
≥ ŝ, and a packing at side exactly ŝ inside the box IS Trump's configuration.
DISCHARGED (A79): a THEOREM from `Rigid.basin_tframe` (the (V′) chain of A36's UNIVERSAL
certificate `G3_UNIVERSAL` at radius `3689/10⁶`, composed with A22 §5's Farkas optimality
at the handover radius, and the θ↔t transfer of `ThetaT.lean`; the slab gate is closed
against the universal radius, `(3/2000)(1 + √2) ≤ 3689/10⁶` — the 16 variant certificates
are replayed but not load-bearing) and the identity `shatA22_eq_shat`.  Axioms:
`propext, Classical.choice, Quot.sound`, the two `native_decide` evaluations
(`checkA22`, `checkA36` on UNIVERSAL) and `shatA22_eq_shat`. -/
theorem basin : ∀ z : Cfg, InBasin z →
    (∀ s : ℝ, CfgPacking s z → shat ≤ s) ∧ (CfgPacking shat z → z = zhat) := by
  intro z hz
  have h := Rigid.basin_tframe z (fun i => by simpa [rBasin, zhat] using hz i)
  rw [← shatA22_eq_shat]
  exact h

/-- **[uniqueness transfer]** EVERY packing at side ŝ has, after a container symmetry and
a relabelling, a representative that lies in some stratum.  STATUS RE-DIAGNOSED by A63
(`docs/proofs/unique_transfer.md`): AS STATED this axiom follows from census
exhaustiveness (A53 L3 — every packing has exactly one Young skeleton; take the D4
normalisation).  The F3 hole did not close, it MOVED: `s_eleven_unique` then feeds an
arbitrary packing to `stratum_kill`, whose ∀-packing strength at the K1-protected classes
is not what H10's machinery will prove (see the quantifier caveat on `stratum_kill`).
The full uniqueness architecture is now on file at drain-lemma rigor: selection CHAIN of
CC-2 teleports to a teleport-stuck packing (degenerate H1 cases resolved — teleports need
no corridor), stuck-packing kills (H10-stuck), residual+basin at the endpoint, and the
COLLAPSE back along the chain via Theorem U (one-square rigidity of ẑ), the single new
leaf, with an executable 11-certificate spec (re-insertion certificates at a rational
side in T1's isolating interval, budget 1, `nofams` zone inside the basin box).
Obligations ledger: U-O1..U-O4 in `unique_transfer.md` §5.
DISCHARGED (A78): was an axiom; now a theorem — exactly §1's re-diagnosis: with
`InStratum` definitional, EVERY packing at `ŝ` lies in some stratum (`exists_stratum`),
with `f = id`, `e = 1`, `z' = z` (the D4 normalisation is absorbed by the class
definition).  The hole is therefore now entirely visible in `stratum_kill`'s
∀-packings quantifier at the K1-protected classes (its docstring), where the
non-circular route is the CC-2 chain + Theorem U collapse (`unique_transfer.md` §2–§4;
the chain/collapse formalisation `unique_via_chain` is in `UniqueChain.lean`). -/
theorem unique_transfer : ∀ z : Cfg, CfgPacking shat z →
    ∃ (z' : Cfg) (f : RP → RP) (e : Equiv.Perm (Fin 11)) (i : StratumIdx),
      IsCtrSym shat f ∧ CfgPacking shat z' ∧ InStratum i shat z' ∧
        ∀ j, (z (e j)).set = f '' (z' j).set := by
  intro z hz
  obtain ⟨i, hi⟩ := exists_stratum shat_mem_wnd hz
  refine ⟨z, id, 1, i, ⟨fun _ _ => rfl, Set.image_id _⟩, hz, hi, fun j => ?_⟩
  simp

/-- Every D4 element is a container symmetry (`Census.lean`: `d4Apply_sqdist`,
`d4Apply_image_container`) — the `f` of `trump_residual`/`unique_transfer` can be taken
to be an explicit signed permutation. -/
theorem isCtrSym_d4Apply (s : ℝ) (g : D4) : IsCtrSym s (d4Apply s g) :=
  ⟨d4Apply_sqdist s g, d4Apply_image_container s g⟩

/-! ## Composition glue (the only proofs in this file) -/

theorem fits_shat : Fits 11 shat := ⟨fun i => (zhat i).set, trump_packs_at_shat.2⟩

/-- **The lower bound, operative form**: no 11-packing at any side below ŝ. -/
theorem s_eleven_ge : ∀ s : ℝ, Fits 11 s → shat ≤ s := by
  intro s hs
  obtain ⟨m, hm⟩ := attained
  have hms : m ≤ s := hm.2 hs
  have h382 : (191 / 50 : ℝ) ≤ m := lb_382 m hm.1
  have hmshat : m ≤ shat := hm.2 fits_shat
  have hwin : m ∈ wnd := ⟨h382, hmshat⟩
  obtain ⟨z, i, hz, hstr⟩ := stratify m hm hwin
  have hshatm : shat ≤ m := by
    by_cases hi : i = trumpStratum
    · subst hi
      obtain ⟨z', f, e, hsym, hz', hbasin, hrel⟩ := trump_residual m hwin z hz hstr
      exact (basin z' hbasin).1 m hz'
    · exact absurd hstr (stratum_kill i hi m hwin z hz)
  linarith

/-- **The composed optimality theorem**: `s(11) = ŝ`. -/
theorem s_eleven_eq : sPack 11 = shat := by
  obtain ⟨m, hm⟩ := attained
  have h1 : sPack 11 = m := hm.csInf_eq
  have h2 : shat ≤ m := s_eleven_ge m hm.1
  have h3 : m ≤ shat := hm.2 fits_shat
  rw [h1]
  linarith

/-- **The uniqueness clause**: every packing at side ŝ is, up to a symmetry of the
container and a relabelling, Trump's packing. -/
theorem s_eleven_unique : ∀ Q : Fin 11 → Set RP, IsPacking 11 shat Q →
    ∃ (f : RP → RP) (e : Equiv.Perm (Fin 11)),
      IsCtrSym shat f ∧ ∀ i, Q i = f '' (zhat (e i)).set := by
  intro Q hQ
  obtain ⟨z, hzt, hzQ⟩ := parametrize Q hQ
  have hz : CfgPacking shat z := by
    refine ⟨hzt, ?_⟩
    have hfun : (fun i => (z i).set) = Q := funext fun i => (hzQ i).symm
    rw [hfun]
    exact hQ
  obtain ⟨z', f1, e1, i, hsym1, hz', hstr, hrel1⟩ := unique_transfer z hz
  have hi : i = trumpStratum := by
    by_contra hi
    exact stratum_kill i hi shat shat_mem_wnd z' hz' hstr
  subst hi
  obtain ⟨z'', f2, e2, hsym2, hz'', hbasin, hrel2⟩ :=
    trump_residual shat shat_mem_wnd z' hz' hstr
  have hzz : z'' = zhat := (basin z'' hbasin).2 hz''
  refine ⟨f1 ∘ f2, (e2.trans e1).symm, hsym1.comp hsym2, fun j => ?_⟩
  have key : ∀ k, (z ((e2.trans e1) k)).set = (f1 ∘ f2) '' (zhat k).set := by
    intro k
    have h1 := hrel1 (e2 k)
    have h2 := hrel2 k
    rw [hzz] at h2
    rw [Equiv.trans_apply, h1, h2, Set.image_comp]
  have hk := key ((e2.trans e1).symm j)
  rw [Equiv.apply_symm_apply] at hk
  rw [hzQ j, hk]

end

end S11
end PackingCert
