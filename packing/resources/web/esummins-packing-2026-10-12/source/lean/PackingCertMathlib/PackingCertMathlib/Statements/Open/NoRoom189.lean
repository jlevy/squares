import PackingCertMathlib.NoRoom

/-!
# -- OPEN: A189 Lemma 1 at packing level — the residue cover and the lane cover

**What it asserts** (`attempts/A189-noroom/code/noroom189.py`, header LEMMA 1, any `n`).  A
packing of `n` unit squares at side `s` has `k` ROLE squares, each containing its certified
core `K_j` (A132: the core lies inside every pose of the role's box), and `n − k` FREE squares.
Suppose (residue) every unit-square pose inside the container whose interior misses all `k`
cores has its centre in one of `r` closed axis-aligned POCKETS, and (lanes) for every pocket
`P_j` at most `lane j` pairwise interior-disjoint non-role squares of the packing meet
`int P_j`.  If `Σ_j lane j < n − k`, the packing does not exist.

**What is Lean** (`Statements/NoRoom.lean`, `NoRoom.noroom_dead`): the counting, with the
residue cover and the lane bounds as hypotheses on the free squares.  **What is not**: this
packing-level form (provable from `noroom_dead` + `parametrize` + the free squares' interiors
being disjoint from the closed role squares, hence from the cores), and — the real content —
the two hypotheses' certification: the bisection's dead test (`multibox` / `dead_poly`, "every
pose of a dropped piece meets some core") and the lane test (`multibox.Node.lane` ∈ `{0, 1}`:
every pose meeting `int C` meets a core, or any two poses meeting `int C` overlap — A161's pair
test).  Both are exact rational tests in Python with no Lean checker yet.

**Status (2026-09-14).**  [T] in prose; the leaf rule of A189/A208/A211.
-/

namespace PackingCert.S11.OpenLemmas

open Set NoRoom

/-- **[OPEN] A189 Lemma 1, packing level.** -/
axiom lemma_A189_noroom {n r k : ℕ} {s : ℝ} (Q : Fin n → Set RP) (hQ : IsPacking n s Q)
    (K : Fin k → Set RP) (role : Fin k → Fin n) (hinj : Function.Injective role)
    (hK : ∀ j, K j ⊆ Q (role j))
    (P : Fin r → Pocket) (lane : Fin r → ℕ)
    (hres : ∀ q : PSq, q.t ∈ Icc (0 : ℝ) 1 → q.set ⊆ container s →
      (∀ j, Disjoint (interior q.set) (K j)) → ∃ j, (q.cx, q.cy) ∈ (P j).set)
    (hlane : ∀ j, ∀ G : Finset (Fin n), (∀ i ∈ G, ∀ j', role j' ≠ i) →
      (∀ i ∈ G, (interior (Q i) ∩ interior (P j).set).Nonempty) → G.card ≤ lane j)
    (hsum : ∑ j, lane j < n - k) : False

#print axioms lemma_A189_noroom

end PackingCert.S11.OpenLemmas
