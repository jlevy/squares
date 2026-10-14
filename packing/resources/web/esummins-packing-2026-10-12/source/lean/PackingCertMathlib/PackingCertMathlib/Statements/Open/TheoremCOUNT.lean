import PackingCertMathlib.Sideband

/-!
# -- OPEN: Theorem COUNT — the option-table count of a page (A198 FASTPROP)

**What it asserts** (`attempts/A198-fastprop/notes/fastprop.md`, any `n`).  On a page, lay a
grid of closed cells of side `< 1/√2` over the centre range; for a cell `g` and a set `S` of
forced cells, `Reach(g, S)` is the certified pose set of a free square with centre in `g`
meeting the widened box `B_p⁺` of every `p ∈ S` (empty = the row is dead).  Then for every
packing of the page there is an assignment of each placed (non-pin) square `i` to a row
`(g_i, S_i)` such that (a) the square's pose lies in `Reach(g_i, S_i)`; (b) the cells `g_i` are
pairwise distinct (Lemma A1: two interior-disjoint unit squares have centres at ℓ∞-distance
`≥ 1/√2`, Lean `Sideband.linf_sep_sqrt`); (c) every forced cell `p` is claimed by at least two
placed squares (Theorem FC).  Hence, if the exact search over the option table finds no such
assignment, the page is DEAD.  (Clause (d), the guard-line chord sums, is
`Statements/GuardLines.lean` `line_1` and is omitted here.)

**The Lean shape.**  The option table is Python data (`fastprop198.py`); it enters as an
abstract `CountPage` whose `reach` semantics is a HYPOTHESIS (`hreach`), as is the forcing
(`hFC`).  What the axiom then claims is provable from Lemma A1 (`linf_sep_sqrt`) and
bookkeeping — it is stated as an axiom because that bookkeeping has not been written.

**Status (2026-09-14).**  [T] in prose; used by every A198–A215 page verdict.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- A page's option table, abstracted: `G` grid cells, `m` forced cells with widened boxes,
and per row `(g, S)` the certified pose set `reach g S`. -/
structure CountPage where
  G : ℕ
  m : ℕ
  cell : Fin G → Set RP
  box : Fin m → Set RP
  reach : Fin G → Finset (Fin m) → Set PSq

/-- **[OPEN] Theorem COUNT.**  Every packing of the page yields an injective row assignment
of its placed squares with every forced cell claimed at least twice. -/
axiom theorem_COUNT (pg : CountPage) {s : ℝ} {z : Cfg} (hz : CfgPacking s z)
    (placed : Finset (Fin 11))
    (hcell : ∀ g, ∀ x ∈ pg.cell g, ∀ y ∈ pg.cell g,
      |x.1 - y.1| < 1 / Real.sqrt 2 ∧ |x.2 - y.2| < 1 / Real.sqrt 2)
    (hcover : ∀ i ∈ placed, ∃ g, ((z i).cx, (z i).cy) ∈ pg.cell g)
    (hreach : ∀ i ∈ placed, ∀ g, ((z i).cx, (z i).cy) ∈ pg.cell g →
      ∀ S : Finset (Fin pg.m), (∀ p ∈ S, (interior (z i).set ∩ pg.box p).Nonempty) →
        z i ∈ pg.reach g S)
    (hFC : ∀ p, ∃ i ∈ placed, ∃ j ∈ placed, i ≠ j ∧
      (interior (z i).set ∩ pg.box p).Nonempty ∧ (interior (z j).set ∩ pg.box p).Nonempty) :
    ∃ (g : Fin 11 → Fin pg.G) (S : Fin 11 → Finset (Fin pg.m)),
      Set.InjOn g (placed : Set (Fin 11)) ∧ (∀ i ∈ placed, z i ∈ pg.reach (g i) (S i)) ∧
      ∀ p, 2 ≤ (placed.filter fun i => p ∈ S i).card

#print axioms theorem_COUNT

end PackingCert.S11.OpenLemmas
