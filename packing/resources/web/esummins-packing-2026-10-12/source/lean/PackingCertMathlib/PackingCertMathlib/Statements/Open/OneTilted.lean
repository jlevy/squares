import PackingCertMathlib.Sideband

/-!
# -- OPEN: Lemma ONE-TILTED — two flat meeters of an open corner box overlap (A219)

**What it asserts** (`docs/proofs/wall_torque.md` §3, any `n`, any side).  Two axis-parallel
unit squares in the quadrant `{x ≥ 0, y ≥ 0}` that both meet the open corner box `(0, 1)²`
have intersecting interiors.  Proof: a flat square in the quadrant meeting the open box is
`[a, a+1] × [b, b+1]` with `0 ≤ a, b < 1`; two such have `|a − a′| < 1` and `|b − b′| < 1`, so
the open rectangles overlap.  Consequently, of the two meeters of a doubly-met open corner at
least one is TILTED — the square on which the PI's wall-torque limitation L2 acts
(Lemma TWO-CONTACT); the flat square in edge-to-edge contact (the simple packing's rows,
zero torque) is never both meeters.

**Status (2026-09-14).**  [T] in prose (three lines).  Lean obligation: for `t = 0` or `t = 1`
the set `q.set` is the closed axis box at `(cx − 1/2, cy − 1/2)` (`cosT 0 = 1`, `sinT 0 = 0`;
`cosT 1 = 0`, `sinT 1 = 1`, F8), `InQuadrant` gives `cx, cy ≥ 1/2`, `Meets q 1` gives
`cx, cy < 3/2`, and `mem_interior_iff_uv` (`Attain.lean`) exhibits the common interior point
`(max cx cx′, max cy cy′)` — routine, not done.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- **[OPEN] Lemma ONE-TILTED.**  Two flat (`t = 0` or `t = 1`) unit squares in the quadrant,
both meeting the open unit corner box, are not interior-disjoint. -/
axiom one_tilted (q q' : PSq) (hq : q.t = 0 ∨ q.t = 1) (hq' : q'.t = 0 ∨ q'.t = 1)
    (hin : InQuadrant q) (hin' : InQuadrant q') (hm : Meets q 1) (hm' : Meets q' 1) :
    ¬ Disjoint (interior q.set) (interior q'.set)

#print axioms one_tilted

end PackingCert.S11.OpenLemmas
