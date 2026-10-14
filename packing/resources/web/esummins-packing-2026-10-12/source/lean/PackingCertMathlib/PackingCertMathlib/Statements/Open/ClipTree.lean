import PackingCertMathlib.Statements.Open.TheoremCOUNT

/-!
# -- OPEN: Lemma CT (the clip tree) and Lemma INHERIT (merged certificates)

**Lemma CT** (`attempts/A205-clip-tree/notes/clip_tree.md` §1, any `n`).  At an alive node let
`p` be a forced cell with named candidates `C_p` (`|C_p| ≤ 1`: `H`, or an instantiated role,
not provably missing `B_p⁺`) and alive rows `g₁..g_k` (the cells of `p`'s anonymous option
table).  Two distinct non-pin squares meet `B_p⁺` (Theorem FC); at most `|C_p|` are named; so at
least `2 − |C_p|` are ANONYMOUS free squares, each with its centre in some alive cell.  With
`|C_p| = 0` the two anonymous meeters have centres in DISTINCT cells (Lemma A1); with
`|C_p| = 1` at least one anonymous meeter exists.  Hence every packing of the node realises one
BRANCH — an unordered pair of distinct cells, or a single cell — and the node is DEAD iff every
branch is DEAD.  Stated below (`lemma_CT`) over the abstract `CountPage`; the branch's
instantiation (the row's reach as the new role's pieces, pinned to its cell, named at `p`) is
the certificate emitter's data.  Provable from `Sideband.linf_sep_sqrt` + Theorem FC; not yet
written.

**Lemma INHERIT** (`attempts/A211-coarse-tree/notes/coarse_tree.md` §4).  (a) A refutation of a
node hypothesis refutes every extension of it — kills are final; (b) a certified exhaustive
branch list at a path may be replayed; (c) the page is dead iff every start node of the merged
trie is dead.  The logical cores of (a)–(c) are the two one-line THEOREMS below; the content
that is NOT Lean is the map from a PATH KEY (the recorded branch steps) to the hypothesis it
denotes — `inherit211.py`'s reader, checked by `code/test_inherit211.py`.

**Status (2026-09-14).**  Both [T] in prose; used by A205–A215.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- **[OPEN] Lemma CT, the branching rule.**  An anonymous meeter of `p` with its centre in a
cell exists; with no named candidate a second one exists in a DIFFERENT cell. -/
axiom lemma_CT (pg : CountPage) {s : ℝ} {z : Cfg} (hz : CfgPacking s z)
    (placed named : Finset (Fin 11)) (hnamed : named ⊆ placed) (hnamed1 : named.card ≤ 1)
    (p : Fin pg.m)
    (hcell : ∀ g, ∀ x ∈ pg.cell g, ∀ y ∈ pg.cell g,
      |x.1 - y.1| < 1 / Real.sqrt 2 ∧ |x.2 - y.2| < 1 / Real.sqrt 2)
    (hcover : ∀ i ∈ placed, ∃ g, ((z i).cx, (z i).cy) ∈ pg.cell g)
    (hFC : ∃ i ∈ placed, ∃ j ∈ placed, i ≠ j ∧
      (interior (z i).set ∩ pg.box p).Nonempty ∧ (interior (z j).set ∩ pg.box p).Nonempty) :
    ∃ i ∈ placed, i ∉ named ∧ ∃ g : Fin pg.G, ((z i).cx, (z i).cy) ∈ pg.cell g ∧
      (interior (z i).set ∩ pg.box p).Nonempty ∧
      (named = ∅ → ∃ j ∈ placed, j ≠ i ∧ ∃ g' : Fin pg.G, g' ≠ g ∧
        ((z j).cx, (z j).cy) ∈ pg.cell g' ∧ (interior (z j).set ∩ pg.box p).Nonempty)

/-- **Lemma INHERIT (a), the logical core**: a refuted hypothesis refutes every extension. -/
theorem inherit_kill {P Q : Cfg → Prop} (h : ∀ z, P z → False) :
    ∀ z, P z → Q z → False :=
  fun z hz _ => h z hz

/-- **Lemma INHERIT (b)+(c), the logical core**: an exhaustive branch list whose branches are
all dead kills the node. -/
theorem inherit_branches {P : Cfg → Prop} {ι : Type} {B : ι → Cfg → Prop}
    (hex : ∀ z, P z → ∃ b, B b z) (hdead : ∀ b, ∀ z, B b z → False) :
    ∀ z, P z → False :=
  fun z hz => (hex z hz).elim fun b hb => hdead b z hb

#print axioms lemma_CT
#print axioms inherit_kill
#print axioms inherit_branches

end PackingCert.S11.OpenLemmas
