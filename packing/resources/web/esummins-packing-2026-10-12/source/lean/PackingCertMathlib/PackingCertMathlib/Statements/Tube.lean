import PackingCertMathlib.RigidTube

/-!
# Theorem T1 — the contraction tube along the dilation ray

**What it says.**  Let `v ∈ ℝ³⁴` be a centre-only direction (`v_s = 1`, zero on tilts) and
`Tube_v(T, r) = { ẑ − t·v + w : 0 ≤ t ≤ T, |w_k| ≤ r_k }` the anisotropic box swept from Trump's
configuration `ẑ` down the ray.  If the certificate checks `checkTube` pass for `(v, T, r)`,
then every FEASIBLE point `z` of the tube (a packing at its own side coordinate `z_s`) has
`z_s ≥ ŝ`, with equality only for `z = ẑ`.  Since the point at depth `t` has side `ŝ − t`, the
tube minus its `t = 0` slice contains no packing at all.

**Why it matters.**  It is the (D) leaf of every class tree and the endpoint of the trump5
residual: a node whose squares are all localised within the tube's radii of the dilated `ẑ`
has NO packing at any side `m ∈ [ŝ − T, ŝ)` and exactly `ẑ` at `ŝ` — the tube reaches from `ŝ`
down to `3.82` in one certificate (`certs/tube_scale_T5.71e-2_window.json`, `T = 0.0571`).
A36's isotropic basin only reached a slab of width `~1e-3`.

**How it is proved** (`RigidTube.lean`, A83; prose `docs/proofs/contraction_tube.md` §1.2):
A36's (V′) dichotomy re-based on the tube — certified Taylor trigonometry in the θ frame,
the 38 contact rows' compression along the ray (Lemma C: every row strictly compressed on the
scale ray), pinning, and the handover to A22 §5's Farkas optimality at the inner radius.  The
certificate is replayed by `native_decide` (`checkTube`).

**For any `n`.**  The tube theorem is a statement about one rigid contact system; the
construction applies to any locally rigid optimal packing with a certified Krawczyk box.
-/

namespace PackingCert.Rigid

open PackingCert.S11

/-- **Theorem T1.**  A feasible point of a certified tube has side `≥ ŝ`, with equality only
at `ẑ`. -/
theorem tube_theorem {c : A22Cert} {tc : TubeCert} (hc : checkA22 c = true)
    (ht : checkTube c tc = true)
    {z : Vec} (hz : InTube (zhatV c hc) (vR tc) tc.T (radR tc) z) (hf : Feas z) :
    sZ (zhatV c hc) ≤ sZ z ∧ (sZ z = sZ (zhatV c hc) → z = zhatV c hc) :=
  tube_basin hc ht hz hf

#print axioms tube_theorem

end PackingCert.Rigid
