import PackingCertMathlib.Parametrize

/-!
# -- OPEN: Lemma CORNER-COVER — what a square pushed into a corner leaves uncovered

**What it asserts** (`attempts/A210-corner-cover/notes/corner_cover.md` §1, any `n`, any
side).  In a corner frame `(u, v)` (distances from the corner's two walls) let `Q` be a unit
square of tilt `θ ∈ [0°, 90°]`, `c = cos θ`, `s = sin θ`, with axis-parallel half-width
`h = (c + s)/2` and wall slacks `d₁ = u_c − h ≥ 0`, `d₂ = v_c − h ≥ 0`.  On the open corner cell
`B = (0, 1)²` the complement of `Q` is EXACTLY the union of three open wedges:

* `W₀` (corner wedge) `= {c·u + s·v < c·s + c·d₁ + s·d₂}`,
* `W₁` (wall wedge on `v = 0`) `= {c·v < c·d₂ + s·(u − s − d₁)}`,
* `W₂` (wall wedge on `u = 0`) `= {s·u < s·d₁ + c·(v − c − d₂)}`

(the wedges are written multiplied through by `c` resp. `s`, so the degenerate tilts `0°` and
`90°` need no case split: at `θ = 90°`, `W₁ = ∅`; at `θ = 0°`, `W₂ = ∅`).  The fourth half-plane
of `Q` never meets `B`.  Corollary CC0: with `d₁ = d₂ = 0` the inner corner `(1, 1)` of the cell
lies in `Q` for every tilt.  Corollary CC1 gives the band over a tilt interval, and rule CC on a
page: a second meeter of the corner box must have an interior point in a wedge.

**In the tan-half parametrisation** (`t = tan(θ/2) ∈ [0, 1]`, `cosT`, `sinT`, `wT = cosT + sinT`)
the statement below is the identity of §1 verbatim.  It is elementary (four half-plane
inequalities and a substitution) and has not been written in Lean.

**Status (2026-09-14).**  [T] in prose; used by A210's rule CC on the k5/k6 pages.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- The open corner cell `(0, 1)²`. -/
def cornerCell : Set RP := Ioo (0 : ℝ) 1 ×ˢ Ioo (0 : ℝ) 1

/-- **[OPEN] Lemma CORNER-COVER.**  The part of the open corner cell missed by a square pushed
into the corner with slacks `d₁, d₂` is exactly the three wedges. -/
axiom lemma_CORNER_COVER (q : PSq) (ht0 : 0 ≤ q.t) (ht1 : q.t ≤ 1) {d1 d2 : ℝ}
    (hd1 : 0 ≤ d1) (hd2 : 0 ≤ d2)
    (hcx : q.cx = wT q.t / 2 + d1) (hcy : q.cy = wT q.t / 2 + d2) :
    cornerCell \ q.set =
      {x ∈ cornerCell | cosT q.t * x.1 + sinT q.t * x.2 <
          cosT q.t * sinT q.t + cosT q.t * d1 + sinT q.t * d2} ∪
      {x ∈ cornerCell | cosT q.t * x.2 < cosT q.t * d2 + sinT q.t * (x.1 - sinT q.t - d1)} ∪
      {x ∈ cornerCell | sinT q.t * x.1 < sinT q.t * d1 + cosT q.t * (x.2 - cosT q.t - d2)}

#print axioms lemma_CORNER_COVER

end PackingCert.S11.OpenLemmas
