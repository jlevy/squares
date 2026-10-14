import PackingCertMathlib.Parametrize

/-!
# -- OPEN: Lemma BASIN — a near-simple square contains the slot's core (A207)

**What it asserts** (`attempts/A207-basin-clip/notes/basin.md` §2, any `n`).  (i) *Containment.*
A unit square whose centre is within `r_c` (ℓ∞) of a slot centre `c_p` and whose tilt satisfies
`|tan(θ/2)| ≤ t_r` contains the slot's core box `K_p = [c_p ± a]²` whenever
`(a + r_c)·w(t_r) ≤ 1/2`, `w = cos + sin`.  (ii) *The P-frame kill.*  Hence, if the extension
certificate `C_r` of `S ∪ {p}` PASSES on `[m_lo, m_hi]`, no packing at a side in that window
contains the pins of `S` together with such a near-simple square — the certificate prices core
containment only (`Statements/CaseVerifier.lean` through Lemma B).  (iii) *The F-frame clip.*
On a page at `s₀` every piece of every role may be cut by the box `B_F(p) × T_B` (the dilated
basin, shrunk by the drift over the page's `λ` range).

**What is Lean.**  Nothing of (i) yet — it is `mem_set_iff_uv` plus the monotonicity of `w`
on `[0°, 45°]`, stated below for the tilt half `t ∈ [0, t_r]` (the other half, `θ` near
`90°`, is the same square re-parametrised).  (ii) is the composition of (i) with Lemma B and
V.CASE; (iii) is a tautologous decomposition of rectangles (`clip207.rect_minus`).

**Status (2026-09-14).**  [T] in prose; the basin clip of A207 on the FULL extension classes.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- **[OPEN] Lemma BASIN (i), containment.**  A square within `(r_c, t_r)` of an axis-aligned
pose at `(cx, cy)` contains the core box `[cx ± a] × [cy ± a]` when `(a + r_c)·wT t_r ≤ 1/2`. -/
axiom lemma_BASIN_containment (q : PSq) (ht0 : 0 ≤ q.t) {tr rc a : ℝ} (htr : q.t ≤ tr)
    (htr1 : tr ≤ 2 / 5) (hrc : 0 ≤ rc) (ha : 0 ≤ a) (hgate : (a + rc) * wT tr ≤ 1 / 2)
    {cx cy : ℝ} (hx : |q.cx - cx| ≤ rc) (hy : |q.cy - cy| ≤ rc) :
    Icc (cx - a) (cx + a) ×ˢ Icc (cy - a) (cy + a) ⊆ q.set

#print axioms lemma_BASIN_containment

end PackingCert.S11.OpenLemmas
