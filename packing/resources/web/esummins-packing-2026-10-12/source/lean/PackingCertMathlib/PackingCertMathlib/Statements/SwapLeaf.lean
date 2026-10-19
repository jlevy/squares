import PackingCertMathlib.Statements.Open.RingSwap

/-!
# The SWAP LEAF: a cell dies by certificate, from `cells_swap` and k1-a (A232)

`docs/proofs/swap_leaf.md`.  The PI (2026-09-15 17:30): *"can we prove STEP against the window?
we only need it true ≤ ŝ for the search to ignore k0 entirely."*  This file is the logical core
of the leaf — **everything here is a THEOREM**; the file introduces no axiom of its own and the
only obligation it consumes is passed in as the hypothesis `kill` (that is k1-a, the k1_00
tree's certified corner-slot kill, `k0_route.md` §3).

**The leaf.**  A CELL is any predicate `Cell` on configurations (in the lab: a list of role
boxes over the window, A185's boxed-windows form).  A SWAP-LEAF CERTIFICATE for it names

* an injection `ι : Fin k → Fin 11` — the roles `X` that will be exchanged, `|X| = k`;
* `k` unit squares `F : Fin k → PSq` at FIXED poses, one of them (`F a`) occupying the slot of
  a corner `c`, all inside the container and pairwise interior-disjoint;
* one exact MISS certificate per (cell of `F`, role outside `X`) — hypothesis `hcell`: in every
  configuration the cell admits, no square outside the range of `ι` meets any `F b`.

Then `swap_leaf_exchange` (Lemma CELLS, `cells_swap`) turns every packing of the cell into a
packing AT THE SAME SIDE containing all of `F`, hence with the corner `c` settled; and
`swap_leaf_dead` closes it against `kill`.  `|X| = 1` is K0-FREE (the teleport), `|X| = 2` is
the PI's STEP, larger `|X|` is allowed — the leftovers may go anywhere free.  No LP, no load,
no minimality, and rattler crowds are covered exactly like loaded ones (`ring_swap.md` §1.8).

**What the verifier checks** (`attempts/A232-swap-leaf/code/verify_swap232.py`, stdlib +
exact rationals, a NEW file: the frozen `verify_case.py` / `verify_case_v4.py` are untouched):
containment of every `F b` in `[0, m]²` for every side `m` of the window, pairwise interior-
disjointness, that `F 0` is the corner slot, that every role outside `X` is BOXED, and the exact
miss certificates — i.e. precisely `hboxF`, `hdisj`, `hslot` and `hcell` below.

**Status (2026-09-15).**  `swapCfg_eq`, `swapCfg_ne`, `swap_leaf_exchange`, `swap_leaf_dead`,
`swap_leaf_corner`: theorems (standard axioms only).  Measured: on the eleven converged-alive
`k0_00` cells the certificate does not exist, because ten of the eleven roles there are UNBOXED
and an unboxed role must be put in `X` — see `docs/proofs/swap_leaf.md` §3.
-/

namespace PackingCert.S11

open Set PackingCert.S11.OpenLemmas

/-- The exchanged configuration: the squares of `X = range ι` are replaced by the certificate's
fixed poses `F`, everything else is kept. -/
noncomputable def swapCfg {k : ℕ} (z : Cfg) (ι : Fin k → Fin 11) (F : Fin k → PSq) : Cfg :=
  fun j => if h : ∃ a, ι a = j then F h.choose else z j

theorem swapCfg_eq {k : ℕ} {ι : Fin k → Fin 11} (hι : Function.Injective ι) (z : Cfg)
    (F : Fin k → PSq) (a : Fin k) : swapCfg z ι F (ι a) = F a := by
  have h : ∃ b, ι b = ι a := ⟨a, rfl⟩
  simp only [swapCfg, dif_pos h]
  exact congrArg F (hι h.choose_spec)

theorem swapCfg_ne {k : ℕ} (z : Cfg) (ι : Fin k → Fin 11) (F : Fin k → PSq) {j : Fin 11}
    (hj : ∀ a, ι a ≠ j) : swapCfg z ι F j = z j := by
  have h : ¬ ∃ a, ι a = j := by
    rintro ⟨a, ha⟩
    exact hj a ha
  simp only [swapCfg, dif_neg h]

/-- **The SWAP leaf, exchange half.**  A certificate turns any packing whose squares outside `X`
miss every `F b` into a packing at the SAME side containing all of `F`.  This is Lemma CELLS
(`cells_swap`, `ring_swap.md` §1.3) with the deficiency `|M(Π)| ≤ |Π|` supplied by `hmiss`. -/
theorem swap_leaf_exchange {m : ℝ} {z : Cfg} (hz : CfgPacking m z) {k : ℕ}
    {ι : Fin k → Fin 11} (hι : Function.Injective ι) (F : Fin k → PSq)
    (htF : ∀ a, (F a).t ∈ Icc (0 : ℝ) 1)
    (hboxF : ∀ a, (F a).set ⊆ container m)
    (hdisj : ∀ a b, a ≠ b → Disjoint (interior (F a).set) (interior (F b).set))
    (hmiss : ∀ j, (∀ a, ι a ≠ j) → ∀ a, Disjoint (interior (F a).set) (interior (z j).set)) :
    CfgPacking m (swapCfg z ι F) :=
  cells_swap hz ι F (swapCfg z ι F) (swapCfg_eq hι z F)
    (fun _j hj => swapCfg_ne z ι F hj) htF hboxF hdisj hmiss

/-- The exchanged packing contains the pin-set `{c}`: the certificate's square `F a` occupies
the slot of `c`, and it sits at index `ι a`. -/
theorem swap_leaf_pins {m : ℝ} {z : Cfg} {k : ℕ} {ι : Fin k → Fin 11}
    (hι : Function.Injective ι) (F : Fin k → PSq) (c : Slot) (a : Fin k)
    (hslot : OccupiesSlot (F a) (slotCentre m c)) :
    ContainsPins {c} m (swapCfg z ι F) := by
  refine ⟨fun _ => ι a, ?_, ?_⟩
  · intro x _ y _ _
    rw [Finset.coe_singleton] at *
    simp_all
  · intro b hb
    rw [Finset.mem_singleton] at hb
    subst hb
    rw [swapCfg_eq hι z F a]
    exact hslot

/-- **The SWAP leaf.**  A cell carrying a swap-leaf certificate is EMPTY at every side `m` at
which no packing has a settled corner `c` (k1-a).  Pure logic above `cells_swap`; the geometry
is entirely in `hboxF`, `hdisj`, `hslot` and `hcell`, which is what the certificate lists and
the verifier checks. -/
theorem swap_leaf_dead {m : ℝ} {k : ℕ} {ι : Fin k → Fin 11} (hι : Function.Injective ι)
    (F : Fin k → PSq) (c : Slot) (a : Fin k) (Cell : Cfg → Prop)
    (htF : ∀ b, (F b).t ∈ Icc (0 : ℝ) 1)
    (hboxF : ∀ b, (F b).set ⊆ container m)
    (hdisj : ∀ b b', b ≠ b' → Disjoint (interior (F b).set) (interior (F b').set))
    (hslot : OccupiesSlot (F a) (slotCentre m c))
    (hcell : ∀ z : Cfg, Cell z → ∀ j, (∀ b, ι b ≠ j) →
      ∀ b, Disjoint (interior (F b).set) (interior (z j).set))
    (kill : ∀ z : Cfg, CfgPacking m z → ¬ ContainsPins {c} m z) :
    ∀ z : Cfg, CfgPacking m z → ¬ Cell z := by
  intro z hz hcz
  exact kill _ (swap_leaf_exchange hz hι F htF hboxF hdisj (hcell z hcz))
    (swap_leaf_pins hι F c a hslot)

/-- The form the lab's certificates take: the settled cell is the CORNER slot `⟨c, 0, 0⟩`, which
is the pin-set k1-a kills (`k0_route.md` §3; the same hypothesis as `no_packing_of_raise`). -/
theorem swap_leaf_corner {m : ℝ} {k : ℕ} {ι : Fin k → Fin 11} (hι : Function.Injective ι)
    (F : Fin k → PSq) (cc : Fin 4) (a : Fin k) (Cell : Cfg → Prop)
    (htF : ∀ b, (F b).t ∈ Icc (0 : ℝ) 1)
    (hboxF : ∀ b, (F b).set ⊆ container m)
    (hdisj : ∀ b b', b ≠ b' → Disjoint (interior (F b).set) (interior (F b').set))
    (hslot : OccupiesSlot (F a) (slotCentre m ⟨cc, 0, 0⟩))
    (hcell : ∀ z : Cfg, Cell z → ∀ j, (∀ b, ι b ≠ j) →
      ∀ b, Disjoint (interior (F b).set) (interior (z j).set))
    (kill : ∀ (c : Fin 4) (z : Cfg), CfgPacking m z → ¬ ContainsPins {⟨c, 0, 0⟩} m z) :
    ∀ z : Cfg, CfgPacking m z → ¬ Cell z :=
  swap_leaf_dead hι F ⟨cc, 0, 0⟩ a Cell htF hboxF hdisj hslot hcell (kill cc)

#print axioms swap_leaf_exchange
#print axioms swap_leaf_dead
#print axioms swap_leaf_corner

end PackingCert.S11
