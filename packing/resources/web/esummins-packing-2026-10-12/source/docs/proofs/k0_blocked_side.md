# K0-BLOCKED ⇒ side ≥ ŝ: the substantive / nicked split, the crowd certificate, and Lemma SLIDE — A92, 2026-09-03

Target (A92 BRIEF, PI 2026-09-03): a K0-BLOCKED packing (every corner's open unit slot met by
≥ 2 squares) has side ≥ ŝ = 3.877083590022814, with a clear boundary above ŝ if the proof gives
one; split into (S) SUBSTANTIVE crowding (every corner's second intruder has depth ≥ δ ⇒ side
≥ f(δ) > ŝ, boundary named) and (N) NICKED corners (some second intruder shallower than δ), each at
drain-v3 rigour with the exact residue named. Labels: [T] proved, [S] routine given cited items,
[M] measured (`attempts/A92-blocked-side/notes/crowd92_report.md`, Opus chore), [C] open.
Conventions: `nocrit_k0_blocked.md` (corner frame, μ_c, d_c, Lemma K, Lemma CLUSTER, retreat
cone, RES(4)), `tilt_floor_k0.md` (Lemma ID, JAM-0, TF-U), `k0_route.md` (K0-FREE (k1-a)/(k1-b),
K0-WIDEN, K0-REUSE, Lemma B.0, λ_max), `frame_census.md` (F1–F8), A89-O3 (`o3_report.md`: the
exempt-family root certificate R1 and its engine), the frozen `verify_case.py` (claim in its
header). s0 = 969271/250000 = ŝ + 4.1·10⁻⁷; λ_max = s0/3.82 = 969271/955000; E(m) = m² − 11.

## 0. Verdict

> **(S) is a certificate question, and the certificate is a weighted root measure certificate
> checked by two runs of the frozen verifier (Lemma CW, §2.4) — not the "8-core K-leaf" of the
> brief, which does not exist (§2.0: the depth-δ pose set has EMPTY core for δ < 0.134). Its
> boundary, when it passes at δ, is s0 = 3.877084 for every side of the window [3.82, s0):
> f(δ) ≥ s0 > ŝ. **CERTIFIED at δ_S = 0.3 [M, §2.5]: `certs/runA_S_d0.3_e1_v2.json` (n = 19,
> total 18.962684 < 19, 1148 atoms) + `certs/runB_S_d0.3_e1_v2.json` (same atoms, weights
> halved, 413 exempt boxes, 0 holes), both PASS under the frozen `verify_case.py` at depth 56,
> re-verified independently by the lead (rc 0, 15 s / 299 s; verifier sha256 521cb01f… =
> A89's). Hence Theorem S(0.3): no K0-BLOCKED packing at any side m ∈ [3.82, s0) has every
> corner's second intruder at depth ≥ 0.3; boundary s0 = 3.877084.** At δ = 0.2 the LP is
> UNDECIDED: its 900-s value 18.104 < 19 was a non-converged LOWER bound that rises with rows
> (18.42 at 18 273 rows, minmass 0.94–0.97 < the 0.970 a certificate needs), and the two-run
> certificate FAILS on geometry (65/65 run-B holes inside the crowd family after the cover fix);
> δ ≤ 0.1 is dead outright (η > 0 for every e; at 0.05 the fractional adversary puts all eleven
> squares in the crowd family). So this certificate's (S)/(N) boundary is δ_S = 0.3 (certified),
> with 0.2 open and ≤ 0.1 impossible for the weighted root LP. With Theorem CEIL the substantive
> band (S) covers is δ ∈ [0.3, 0.2929]: the certificate kills exactly the near-diagonal crowds
> (Corollary CEIL-2: α ∈ [41°, 49°] at all four corners).**
>
> **Theorem CEIL [T] (§2.1): two interior-disjoint unit squares in a quadrant satisfy
> max(μ(A), μ(B)) ≥ 1/(cos α + sin α) ≥ 1/√2, α the angle of a separating line; so every corner
> of every packing has min(d₁, d₂) ≤ 1 − 1/√2 = 0.292893, with equality only for the diagonal
> 45° pair. (S) is vacuous above that; the certified frontier value 0.292893 of `d2front87` is
> the theoretical maximum. Corollary [T]: the pair CHARGE (stranded corner area) is ≤ 1 at every
> δ, so 4 × charge ≤ 4 < E(ŝ) = 4.0318 — the brief's route 2 (area alone) cannot close (S) at
> any δ; the wall-strip count of route 1 has the same ceiling (§2.2).**
>
> **(N): Lemma SLIDE [T] (§3.1, ∀-packings, no selection, modulo K0-O1 = k1_00's tree on the
> window, the dependency K0-FREE already carries): a packing at side m ∈ [3.82, ŝ) whose corner
> c has intruders of total depth T below the deepest one, with m + T < ŝ, does not exist — slide
> the shallow intruders' retreat clusters along the diagonal (rate exactly 1/√2 in depth per
> 1/√2 in side), let the container grow with them, then teleport (K0-FREE). Hence at every
> corner of every K0-BLOCKED packing at side m < ŝ: d₂(c) ≥ ŝ − m. Nicks are bounded BELOW by
> the distance to ŝ. Composition (§3.3): a crowd certificate C(δ, m_lo) (window [m_lo, s0], depth
> δ > 0.4403·(s0 − m_lo)) together with SLIDE and K0-FREE kills EVERY packing at every side
> m ∈ [m_lo, ŝ − δ]; a finite chain of such certificates raises the certified lower bound to
> s(11) ≥ ŝ − δ_∞, δ_∞ = the smallest depth at which the crowd LP still passes. The EXACT
> residue of (N) is the slab RES-N(δ_∞) := {K0-BLOCKED packings at side m ∈ (ŝ − δ_∞, ŝ] with some
> corner's second intruder at depth in [ŝ − m, δ_∞)} — plus the uniqueness clause at ŝ, which
> SLIDE does not reach (T > 0 overshoots ŝ). Inside the slab, NOCRIT-SEL anchors every nick,
> JAM-0 pins the nick of an axis-aligned deep partner, K0-REUSE removes the δ_pin pocket; none of
> them empties the slab (§3.4). The pad constant 0.4403 = (1 + 1/√2)/s0 < 1 is what makes the
> chain converge geometrically instead of stalling; it fails only where the LP fails.**

## 1. Setting

Packings at side m: eleven closed unit squares, pairwise interior-disjoint, in [0, m]². Corner
frame of c ∈ {BL, BR, TL, TR}: the D4 map sending c to the origin with the container in the
positive quadrant. For a closed unit square Q in the quadrant
  μ(Q) := min_{p ∈ Q} max(p_x, p_y),   d(Q) := max(0, 1 − μ(Q))   (A90's depth).
[T, A90 §1] d(Q) > 0 ⟺ int Q ∩ (0,1)² ≠ ∅; μ(Q) ≤ a ⟺ Q ∩ [0, a]² ≠ ∅ (closed meeting; the
min is attained). Intruder at c: d_c(Q) > 0; d₁(c) ≥ d₂(c) ≥ … the depths of c's intruders in
decreasing order; K0-BLOCKED: d₂(c) > 0 at all four corners. A square intrudes at most one corner
(CC-1(ii)). D2 := min_c d₂(c).

## 2. (S) — substantive crowding: min_c d₂(c) ≥ δ

### 2.0 [T] The brief's route-3 object does not exist (why the certificate is weighted)

For a ∈ (0, 1) let D(a) := {closed unit squares Q in the quadrant with μ(Q) ≤ a} (depth ≥ 1 − a).
Its CORE ∩_{Q ∈ D(a)} Q is EMPTY for a > 0.866 (δ < 0.134): take Q₁ with lowest vertex V = (1/2, a)
and edges from V in directions (√3/2, 1/2) and (−1/2, √3/2) (a unit square hanging from the left
wall at tilt 60°, leftmost vertex (0, a + √3/2), inside the quadrant, μ(Q₁) = a), and Q₂ its
x ↔ y mirror. A common point solves (1/2 + (√3/2)u − w/2, a + u/2 + (√3/2)w) = (a + u′/2 +
(√3/2)w′, 1/2 + (√3/2)u′ − w′/2) with u, w, u′, w′ ∈ [0, 1]; subtracting the two coordinate
equations gives (√3 − 1)/2·(u + u′) − (√3 + 1)/2·(w + w′) = 2a − 1, whose left side is ≤ √3 − 1 =
0.732; so there is no solution when 2a − 1 > 0.732, i.e. a > 0.866: for δ = 1 − a < 0.134 the two
squares Q₁, Q₂ ∈ D(1 − δ) have NO common point. Hence no rational core square K ⊂ every member of
D(1 − δ) exists, and the frozen `verify_case.py` semantics (cores = containment hypotheses "some
square contains K"; NO-families = "no square in F") cannot state "some square lies in D(1−δ)" at
the root without branching over a cover of D(1−δ) by boxes with non-empty cores — which is A85's
corner pair tree (`k0_route.md` §7.2: 2.9·10¹⁶ four-corner nodes; `realise85.md`: 3.9·10¹³
after realisability), priced dead. The object that DOES exist is the weighted certificate of §2.4.

### 2.1 [T] Theorem CEIL — the one-corner ceiling, with the separating angle

**Wedge Lemma.** Let W(x₀, α) := {p : p_y ≥ 0, p_y ≤ (p_x − x₀) tan α}, α ∈ (0°, 90°], x₀ ∈ ℝ.
If a closed unit square Q ⊂ W(x₀, α) then min_{p ∈ Q} p_x ≥ x₀ + cos²α / sin α.

*Proof.* Translate so that x₀ = 0. Let p* = (x*, y*) be a vertex of Q of minimal x-coordinate.
Both unit edges from p* point into {x ≥ x*}, so they are e₁ = (c, −s), e₂ = (s, c) with c, s ≥ 0,
c² + s² = 1. W is convex, so Q ⊂ W iff its vertices are in W: (i) p* + e₁ ∈ W gives y* − s ≥ 0;
(ii) p* ∈ W gives y* ≤ x* tan α; (iii) p* + e₂ ∈ W gives y* + c ≤ (x* + s) tan α. From (ii) and
(i), x* ≥ y* cot α ≥ s cot α; from (iii) and (i), x* ≥ (y* + c) cot α − s ≥ (s + c) cot α − s.
So x* ≥ φ(s) := max(s cot α, (s + c) cot α − s), c = √(1 − s²). The difference of the two
branches, c cot α − s, is strictly decreasing in s and vanishes at s = cos α (c = sin α). On
[cos α, 1] the max is s cot α ≥ cos α cot α. On [0, cos α] the max is (s + c) cot α − s, concave
in s (c is concave), hence ≥ min of its endpoint values cot α and cos α cot α. So
x* ≥ cos α cot α = cos²α / sin α. (α = 90°: cot α = 0 and the bound is x₀, correct.) ∎

**Theorem CEIL.** Let A, B be closed unit squares in the quadrant {x ≥ 0, y ≥ 0} with disjoint
interiors. Then max(μ(A), μ(B)) ≥ 1/√2; more precisely, if L = {n·p = d} (n a unit vector) is a
line with A ⊂ {n·p ≥ d}, B ⊂ {n·p ≤ d} (it exists: separation of the convex sets int A and B),
then either one of μ(A), μ(B) is ≥ 1/2 + 1/(2√2) = 0.8536 (L cuts off the corner) or, with
tan α := |n_x / n_y| ∈ (0, ∞), max(μ(A), μ(B)) ≥ 1/(cos α + sin α) ≥ 1/√2. Equality
max(μ(A), μ(B)) = 1/√2 holds only for L the diagonal and A, B the two 45° squares with a common
edge on it, each touching one wall (the `deepfront87` motif).

*Proof.* Case 1: n_x, n_y ≥ 0. The centre c_B of B satisfies c_B,x, c_B,y ≥ 1/2 (B's inscribed
disc of radius 1/2 lies in the quadrant) and c_B + n/2 ∈ B, so d ≥ n·c_B + 1/2 ≥ (n_x + n_y)/2 +
1/2. Every p ∈ A has n·p ≥ d, and if max(p_x, p_y) < d/(n_x + n_y) then n·p < d; so μ(A) ≥
d/(n_x + n_y) ≥ 1/2 + 1/(2(n_x + n_y)) ≥ 1/2 + 1/(2√2). Case 2: n_x, n_y ≤ 0: Case 1 with A, B
swapped (replace (n, d) by (−n, −d)): μ(B) ≥ 0.8536. Case 3: n_x > 0 > n_y (the case n_x < 0 <
n_y is Case 3 with A, B swapped). Put tan α := n_x/(−n_y), x₀ := d/n_x. Dividing n·p ≥ d by
−n_y > 0: A ⊂ {y ≤ (x − x₀) tan α} ∩ {y ≥ 0} = W(x₀, α), so by the Wedge Lemma min_A x ≥ x₀ +
cos²α/sin α =: L_A, and μ(A) ≥ min_A x since max(x, y) ≥ x. Likewise B ⊂ {x ≤ x₀ + y cot α} ∩
{x ≥ 0}; reflecting x ↔ y this is the wedge W(−x₀ tan α, 90° − α), so min_B y ≥ −x₀ tan α +
sin²α/cos α =: L_B and μ(B) ≥ L_B. Now tan α · L_A + L_B = cos α + sin²α/cos α = 1/cos α, hence
max(L_A, L_B) ≥ (tan α · L_A + L_B)/(tan α + 1) = 1/(cos α + sin α) ≥ 1/√2. Equality forces
α = 45°, x₀ = 0 (L_A = L_B), and equality in the Wedge Lemma for both squares (s = cos 45°, p* on
the diagonal): the diagonal pair. ∎

**Corollary CEIL-1 (per-corner ceiling).** At every corner of every packing, min(d₁, d₂) ≤ 1 −
1/√2 = 0.29289321881, with equality only for the diagonal 45° pair. So (S) is vacuous for δ >
0.292893, and `d2front87`'s certified 0.292893 (side 4.357) is the maximum possible D2 at any
side. [The `deepfront87` derivation assumed the separating line passes through the corner point;
Theorem CEIL removes that assumption.]

**Corollary CEIL-2 (the shape of a substantive crowd).** If both intruders of c have depth ≥ δ,
their separating line has cos α + sin α ≥ 1/(1 − δ), i.e. α within 45° ± arccos((1−δ)⁻¹/√2) of
the diagonal (δ = 0.05: α ∈ [3.1°, 86.9°]; 0.1: [8.7°, 81.3°]; 0.2: [17.1°, 72.9°]; 0.29: [41°,
49°]), and x₀ ∈ [−(1−δ) cot α + …]: explicitly L_A ≤ 1 − δ and L_B ≤ 1 − δ.

### 2.2 [T] Routes 1 and 2 of the brief are closed (negative)

**Pair charge.** For a 2-crowd (A, B) at c define its charge as the area of the quadrant region
near c covered by no unit square of the packing; the brief's route 2 wanted charge(δ) :=
min{charge : d_A, d_B ≥ δ} > E(ŝ)/4 = 1.008 for some δ. At the ceiling δ = 1 − 1/√2 the only
admissible pair is the diagonal pair (Theorem CEIL, equality case), whose uncovered region is
the triangle {x, y ≥ 0, x + y ≤ √2} of area exactly 1 (it holds no third unit square: the largest
square in a right isosceles triangle with legs √2 has side √2/2 < 1), so charge(0.2929) = 1;
and charge is nonincreasing in δ (a min over a growing set). Hence **charge(δ) ≤ 1 for every
δ, and 4·charge ≤ 4 < 4.0318 = E(ŝ): area alone never closes (S)** (it would at sides m < √15 =
3.87298 and δ = 0.2929 only). Interior wastage has to be priced with it — which is what the
LP measure of §2.4 does. **Wall strips (route 1).** The brief's projection count s ≥ 2 + 2g(δ)
has the same ceiling: the substantive crowd of one corner projects onto its two walls with
extents ≤ 1 + √2 each, and the pinwheel placement (each crowd stacked along one wall, the four
stacks in rotational order) fits eight crowd squares along every wall at length ≤ 2.12 + 1.42 <
ŝ for every δ ≤ 0.2929; the obstruction is the room left for the three free squares, a global
area/shape question, not a wall length. No wall-strip lemma with a boundary above ŝ exists
for δ < 0.2929, and I state none.

### 2.3 [T] Lemma B-YES — the crowd hypothesis transfers to s0 (with a pad)

Let P be a packing at side m ∈ [3.82, s0), λ := s0/m ∈ (1, λ_max], F := Δ_λ P (centres scaled by
λ about the origin, tilts unchanged; Lemma B.0: F is a family of 11 pairwise DISJOINT closed unit
squares in [0, s0]² with positive wall margins). If Q ∈ P satisfies μ_c(Q) ≤ a (Q meets [0,a]² in
c's frame), then Q′ := Δ_λ Q satisfies μ_c(Q′) ≤ a_w(a, λ) := λ a + (λ − 1)/√2 ≤ a_w(a) :=
λ_max a + (λ_max − 1)/√2.

*Proof (BL; other corners by Δ_λ ∘ g_m = g_{s0} ∘ Δ_λ).* Take p ∈ Q ∩ [0, a]²; p′ := p + (λ − 1)c_Q
∈ Q′ (Q′ = Q + (λ − 1)c_Q). Since |c_Q − p|_∞ ≤ h(θ) ≤ √2/2, c_{Q,x} ≤ a + √2/2, so 0 ≤ p′_x ≤ a +
(λ − 1)(a + √2/2) = λa + (λ − 1)/√2; same for y. ∎

Numerics (rational, √2/2 ≤ 0.7072): a = 1 − δ, δ = 0.3 → a_w = 0.72103; 0.2 → 0.82252; 0.1 →
0.92402; 0.05 → 0.97477. The **pad** a_w − a = (λ_max − 1)(a + 1/√2) is at most 0.0254; a_w < 1
iff δ > δ_pad := (1 + 1/√2)(s0 − m_lo)/s0 = 0.4403·(s0 − m_lo), i.e. δ > 0.02514 for the full
window [3.82, s0). For a sub-window [m_lo, s0) the pad scales with s0 − m_lo (used in §3.3).
Two squares of F meeting different corners' boxes [0, a_w]² (a_w < 1) are distinct (the boxes
are s0 − 2a_w > √2 apart). At m = s0 itself no dilation is available and the closed squares of
P may touch; the certificate excludes sides m < s0 only.

### 2.4 [T] Lemma CW — the crowd-weighted certificate, verified by two frozen runs

Let μ = Σ_i w_i δ_{p_i} be a finite nonnegative atomic measure on [0, s0]², e ∈ ℚ_{>0} with
8e ∈ ℤ, F_c(a) := {admissible closed unit squares Q ⊂ [0,s0]² : μ_c(Q) ≤ a}, and E a set of
admissible squares with E ∩ F_c(a_w) = ∅ for every corner c (in the implementation E is the exact
complement of an outer cover G ⊇ ∪_c F_c(a_w), and every E box is certified disjoint from F_c(a_w)
itself). Suppose
 (A) μ(Q) ≥ 1 for every admissible closed unit square Q ⊂ [0, s0]²;
 (B) μ(Q) ≥ 1 + e for every admissible Q ∉ E;
 (C) μ([0, s0]²) < 11 + 8e.
Then no family of 11 pairwise disjoint closed unit squares in [0, s0]² has, at every corner c,
two members in F_c(a_w). *Proof.* The 8 crowd members are distinct (§2.3) and lie in ∪_c F_c(a_w),
hence not in E, so each has mass ≥ 1 + e by (B); the other 3 have mass ≥ 1 by (A); disjointness gives
Σ_i μ(Q_i) = μ(∪ Q_i) ≤ μ([0,s0]²) < 11 + 8e ≤ Σ_i μ(Q_i). ∎

**Verification with the frozen `verify_case.py` (two runs, one measure).** Run A: certificate
(s0, atoms, weights w, n = budget = 11 + 8e ∈ ℤ, no cores, no NO-families); its PASS is exactly
(A) + (C) (header claim: every admissible closed unit square has mass ≥ 1 and total < n). Run B:
the same atoms with weights w/(1 + e), n = budget = 1000 (a dummy: its "total < n" clause is not
used), NO-families = an inner cover E of the complement of G by rect × t-interval boxes; its PASS
gives "(μ/(1+e))(Q) ≥ 1 for every admissible Q not provably in a NO-family", and a Q ∉ E lies in
no NO-family, so (B) holds. The soundness of each run is the verifier's own header claim
(V.CASE, Lean-proved for the coverage clause); Lemma CW is the only mathematics on top. G is the
outer cover of §1 of `chore_crowd_cert.md` (exact: a rect × θ-bin is dropped only if f at its
lower-left corner minus the Lipschitz pad exceeds a_w on an exact θ-grid — f nondecreasing in
both centre coordinates, (√2/2)-Lipschitz in θ, A89 o3fam facts), E its exact rectilinear
complement; both bit-exactly D4-closed, so the LP runs in the D4 quotient. The certificate
proves, by Lemma B-YES, **Theorem S(δ): no K0-BLOCKED packing at any side m ∈ [3.82, s0) has
min_c d₂(c) ≥ δ**, i.e. f(δ) ≥ s0 — with the CLOSED-meeting hypothesis μ_c ≤ 1 − δ, which is
implied by depth ≥ δ.

Remarks. (i) The dual reading: the LP passes at e iff no FRACTIONAL packing (density ≤ 1) has
Σλ + e Σ_{G} λ ≥ 11 + 8e; the plain root at s0 has τ ≥ 11 exactly (Trump exists below s0), so
the certificate lives entirely on the tradeoff between total mass and crowd mass: it passes iff
the point (11, 8) is separated from the achievable (total, crowd-mass) set by a line of slope −e.
Smaller families (larger δ) make it easier; a_w → 1 makes it impossible (the tangent squares
1, 8, 9 of Trump enter the family and every image realises the hypothesis — the canary). (ii)
Canary: for a_w < 1 no D4 image of Trump has two placements with f_c ≤ a_w at every corner (TL has
0.8317 / 0.8445, the three other corners have one placement at 0 and tangent squares at exactly
1), so the hypothesis is never image-realisable and the engine's refusal gate is not triggered;
the certified K0-BLOCKED packings of `d2front87` (sides 4.03–4.36) and s0115 (3.985) lie outside
the certificate's scope (side > s0) and are not touched by Theorem S(δ) at any δ — consistent
with the brief's canaries by construction, not by luck: Theorem S(δ) says nothing above s0.
(iii) A certificate at a side s > s0 (window [s0, s]) would give f(δ) ≥ s; the engine's side is a
parameter (A82 emitter) and the images are absent there (no canary needed); not run in this
attempt — see §6.

### 2.5 [M] Results of the crowd certificate (Opus chore; `notes/crowd92_report.md`)

Engine: A89's stack copied, one change (per-pose rhs 1 + e·[Q ∈ G] with a two-pass row oracle,
`lpbox92.py`), families exact (G 145–151 boxes per corner, overshoot 7.6–11 %; E 413–425 boxes
certified disjoint from F_c(a_w) at all four corners; D4 defect 2·10⁻¹⁶), canary PASS at every a_w
(no image has two placements below a_w at every corner). D4 quotient, lp_time 900 s, warm pool
A38/A07 columns. n = 11 + 8e.

| δ | a_w | e | n | τ | η = τ − n | minmass | LP s | LP verdict |
|---|---|---|---|---|---|---|---|---|
| 0.30 | 0.72103 | 1 | 19 | **16.4459** | **−2.554** | 0.843 | 968 | PASS |
| 0.20 | 0.82253 | 1 | 19 | **18.1042** | **−0.896** | 0.901 | 983 | PASS |
| 0.10 | 0.92402 | 1 / 1/2 / 2 / 1/4 | 19 / 15 / 27 / 13 | 21.047 / 16.057 / 31.057 / 13.585 | +2.05 / +1.06 / +4.06 / +0.59 | 0.91–0.96 | ≈ 950 | refused (all e) |
| 0.05 | 0.97477 | 1 / 1/2 / 2 / 1/4 | 19 / 15 / 27 / 13 | 22.000 / 16.500 / 33.000 / 13.750 | +3.00 / +1.50 / +6.00 / +0.75 | 0.98–1.00 | ≈ 850 | refused (all e) |

Reading. (i) At δ = 0.05 the LP value is EXACTLY 11(1 + e) for every e: the fractional adversary
puts all eleven squares inside the (dilated) crowd family — at a_w = 0.975 the family's centre
region reaches 1.70 from each corner and the four regions cover the container up to a thin cross;
the certificate is structurally dead there, as predicted by the pad discussion. At δ = 0.1 the
crowd mass of the best fractional packing is ≈ 10 (η ≈ +2 at e = 1): dead too. (ii) At δ = 0.3
the LP passes with room (η = −2.55, converged enough to certify); at 0.2 the 900-s value
(η = −0.90) is a non-converged lower bound (18.42 after 2 926 s more, still rising). So the LP boundary of (S)
is δ_S = 0.3 certified, 0.2 open (its 900-s τ is a non-converged lower bound), ≤ 0.1 dead. (iii) CERTIFICATION. First pass: both LP-passing nodes FAILED run B
(26 / 23 holes) although run A passed. Root cause [M, found by the chore]: the complement cover
E was emitted as ABUTTING strips, and `verify_case.nofam_exempt` is a per-family containment
test — a box straddling two abutting families is never exempt, and those seams lie deep inside
E where the measure carries mass 1, not 1 + e, so every seam is a guaranteed hole (A89's o3fam
never met this: its staircase rects are nested). With one-cell OVERLAPPING strips (every E box
still exactly certified disjoint from F_c(a_w) at all four corners — overlap does not affect
Lemma CW) the SAME node certifies: **`certs/runA_S_d0.3_e1_v2.json` PASS (n = 19, total
4740671/250000 = 18.962684, 1148 atoms, 252 116 boxes, 0 exempt, 0 holes, max depth 33) and
`certs/runB_S_d0.3_e1_v2.json` PASS (n = 1000 dummy, total 9.481342, 413 NO-families, 629 840
boxes, 265 016 exempt, 0 holes, max depth 39); sha256 257f267b… / bd78ce08…; independently
re-run by the lead with the byte-identical frozen verifier (sha256 521cb01f… = A89's = A85's):
rc 0 / rc 0.** So **δ_S = 0.3: Theorem S(0.3) holds on the whole window, boundary s0.** δ = 0.2, re-run with
the overlapping E (warm re-solve 2 926 s, 18 273 rows): τ = 18.417 (NOT converged; τ rises with
rows, so the sweep's 18.104 was a lower bound and the true optimum may exceed 19), minmass 0.939
(four attempts 0.943–0.966 against the 0.970 the certificate scale needs); run A 13 holes, run B 65
holes all INSIDE the crowd family (0 seam holes) — a geometric refusal at the LP's present
convergence, not an engineering one; δ = 0.2 is OPEN, δ = 0.15 not attempted (interpolated τ ≈
19.5 > 19), δ ≤ 0.1 dead at the LP level. The certified frontier from the other side
(`d2front87`, side 4.038 at D2 = 0.034; 4.10 at 0.078; 4.19 at 0.154; 4.357 at 0.293) is
consistent: no K0-BLOCKED packing with D2 ≥ 0.2 is known below side 4.19, and Theorem S(0.3)
says none exists below s0.

## 3. (N) — nicked corners: some d₂(c) < δ

### 3.1 [T] Lemma SLIDE (∀-packings; uses only (k1-a) of Lemma K0-FREE, i.e. K0-O1)

**Lemma SLIDE.** Let P be a packing at side m ∈ [3.82, ŝ), c a corner, and Q₀, Q₁, …, Q_k (k ≥ 1)
the intruders of c. Put T := Σ_{i ≥ 1} d_c(Q_i) (any k of the k + 1; take Q₀ the deepest). If
m + T < ŝ then P does not exist. Equivalently: **every K0-BLOCKED packing at side m < ŝ has, at
every corner, d₂(c) ≥ ŝ − m** (and Σ_{i≥1} d_c(Q_i) ≥ ŝ − m).

*Proof.* Work in c's frame; write u := (1, 1)/√2 (the diagonal, pointing away from c) and let the
container grow at c's two far walls. Step 1 (one intruder out). Let B := Q₁ and let C := C_u(B)
be its u-retreat cluster for a consistent selection S at P (Lemma CLUSTER's forward closure of
"presses against u"). Translate the members of C by t·u, t ≥ 0, and keep the container
[0, m + t/√2]² (in c's frame; the far walls move by t/√2, c's walls do not). Every row of S is
affine in t (Fact A): rows among members are constant; a member–outsider row that is active has
slope ≥ 0 (closedness); inactive rows have positive margin; near-wall rows of members increase
(u has positive components); far-wall rows of members are constant (the wall moves with them);
outsiders' rows are constant (their far-wall rows gain t/√2). So the configuration is S-feasible
— a packing at side m + t/√2 — until the first t₁ at which an inactive member–outsider row
becomes active. At t₁ let N be the outsider of that row; replace C by the forward closure of
C ∪ {N} under "presses against u" for a selection consistent with the new configuration, and
continue; C only grows, so this happens at most 10 times, and the translation can be continued
to any t. Along the motion μ_c(B + t u) = μ_c(B) + t/√2 EXACTLY (max(p_x + t/√2, p_y + t/√2) =
max(p_x, p_y) + t/√2 for every point), so at t = √2·d_c(B) the square B has μ_c ≥ 1 — it no longer
meets the open slot — at side m + d_c(B). No square's depth at c has increased (translating along
u never decreases μ_c) and no new intruder of c has appeared. Step 2 (repeat). Apply Step 1 to
Q₂, …, Q_k in turn (each time with the current configuration, cluster and selection; the depths
used are the current ones, ≤ the original). Total side increase ≤ Σ_{i≥1} d_c(Q_i) = T; the result
P′ is a packing at side m′ := m + T (in a container whose c-corner is unchanged) in which the
open slot at c is met by at most one square (Q₀, possibly moved, possibly out). Step 3
(teleport). Replace that square (or any square if the slot is free) by the slot square at c:
P″ is a packing at side m′ containing an axis-aligned unit square at a corner slot (Lemma
K0-FREE's construction, `teleport_packing`). Since 3.82 ≤ m < m′ < ŝ, (k1-a) says P″ does not
exist. ∎

Remarks. (a) No minimality, no selection functional, no Fritz-John: the only input is the
affine feasibility of Lemma CLUSTER and the k1_00 tree over the window (K0-O1), exactly as for
Lemma K0-FREE, of which SLIDE is the quantitative form (K0-FREE is the case T = 0). (b) The
diagonal direction is chosen because its depth rate is 1/√2 for EVERY intruder type (Lemma K's
cardinal rates can be as small as 1/2 for tilted D-type intruders, and cost side at the same
rate 1); the cost is one unit of side per unit of depth. (c) At m = ŝ the lemma is void (m′ > ŝ
is outside (k1-a), and (k1-b) at exactly ŝ would need m′ = ŝ, T = 0). (d) [F] The empirical
"anchored-only frontier collapse" of `d2front87` (b) (anchored D2 = 10⁻⁴ at side 4.08, no
anchored candidate at 4.05) is a different phenomenon (side > ŝ, no k1 kill); SLIDE is its
rigorous counterpart BELOW ŝ: nicks shallower than ŝ − m are not merely un-anchored, they are
impossible.

### 3.2 [T] Corollary (the nick floor and the substantive/nicked split, quantified)

For a K0-BLOCKED packing at side m ∈ [3.82, ŝ): min_c d₂(c) ≥ ŝ − m > 0. Hence, with Theorem
S(δ) available at some δ: (i) if δ ≤ ŝ − m the packing does not exist (its D2 ≥ ŝ − m ≥ δ is
substantive); (ii) the nicked case (N) is confined to the slab ŝ − δ < m < ŝ, with the nick's
depth in [ŝ − m, δ). The brief's canary s0115 (side 3.985, nicks 8·10⁻⁹) is outside [3.82, ŝ)
and is not constrained; inside the window such nicks cannot occur at any side below ŝ − 8·10⁻⁹.

### 3.3 [T] Composition — the certificate chain and the exact residue

**Definition.** C(δ, m_lo) := a crowd certificate (Lemma CW, two frozen runs) at s0 built with
the pad of the window [m_lo, s0), i.e. with a_w := λ(m_lo)(1 − δ) + (λ(m_lo) − 1)/√2, λ(m_lo) =
s0/m_lo; it requires δ > δ_pad(m_lo) = 0.44034·(s0 − m_lo) (so that a_w < 1, canary-free) and
proves: no K0-BLOCKED packing at side m ∈ [m_lo, s0) has min_c d₂ ≥ δ.

**Theorem N (composition).** Assume K0-O1 (k1_00's tree closed on [3.82, ŝ], as K0-FREE needs).
(1) C(δ, m_lo) + Lemma SLIDE + Lemma K0-FREE exclude every packing at every side m ∈ [m_lo, ŝ − δ].
*Proof.* A packing at such m is K0-FREE (excluded by K0-FREE) or K0-BLOCKED with min_c d₂ ≥ ŝ − m
≥ δ (SLIDE), excluded by C(δ, m_lo). ∎
(2) Let a finite chain C(δ_k, m_k), k = 1..K, satisfy m₁ = 3.82, m_{k+1} ≤ ŝ − δ_k, and put
δ_∞ := δ_K. Then **s(11) ≥ ŝ − δ_∞** (no packing at any side in [3.82, ŝ − δ_∞]) and the residue
of the whole k0_00 problem below ŝ is
   RES-N(δ_∞) := {K0-BLOCKED packings at side m ∈ (ŝ − δ_∞, ŝ) with min_c d₂(c) ∈ [ŝ − m, δ_∞)},
together with, at ŝ itself, the non-image K0-BLOCKED packings with min_c d₂ < δ_∞ (uniqueness).
(3) The chain converges geometrically: C(δ_k, m_k) needs δ_k > 0.44034(s0 − m_k), and the next
window starts at m_{k+1} = ŝ − δ_k, so δ_{k+1} > 0.44034·δ_k + 1.8·10⁻⁷: each step shrinks the
residual slab by the factor 0.44034 = (1 + 1/√2)/s0 — the step's pad is smaller than the depth
floor SLIDE provides (coefficient 1) because the dilation moves a corner square by (λ − 1)·(a +
1/√2) < (λ − 1)·s0 while SLIDE charges the full depth. The chain stops where the crowd LP stops
passing: δ_∞ is an LP constant, not a geometric one; the (S)/(N) boundary of the brief is δ_∞,
and the side boundary of (S) is s0 at every step.

*The exact residue, named.* RES-N(δ_∞): a K0-BLOCKED packing at side m within δ_∞ of ŝ (from
below) whose shallowest second intruder has depth between ŝ − m and δ_∞. Nothing in the lab
excludes it: the certified K0-BLOCKED packings at sides ≥ 3.985 (`k0dir87`) show the pattern
(nicks of 10⁻⁸ … 10⁻² with the rest of the packing tight) is realisable 0.11 above ŝ; whether it
survives down to ŝ is exactly the PI conjecture in its remaining form.

### 3.4 What the selection lemmas add inside the slab (and what they do not)

Take z* a Ψ-minimal σ-minimiser at side m = s(11) ∈ (ŝ − δ_∞, ŝ) (SEL-Ψ), K0-BLOCKED, with a
nicked corner c: d₂(c) ∈ [ŝ − m, δ_∞). Then, in addition to SLIDE's floor:
 * [T, NOCRIT-SEL] both intruders A (deeper) and B (the nick) are anchored in each cardinal retreat
   direction, pressed toward c by far-side neighbours, and are not rattlers; B's retreat cluster
   reaches a far wall (≥ 3 squares, Lemma COL, m ≥ 1 + 2√2) or contains a deepening intruder of
   another corner. SLIDE shows what anchoring costs in side: exactly the depth removed. At the
   minimiser this is consistent (the slid packing has side m + d_B < ŝ only if d_B < ŝ − m, which
   SLIDE already excludes) — anchoring is NOT an extra contradiction, and RES(4)'s frame structure
   (A90 §4, A91) is inherited by RES-N verbatim: RES-N ⊂ RES(4) ∩ {slab}.
 * [T, JAM-0] if A is axis-aligned at offset g < 1/√2 in c's frame then sin(tilt B) ≤ g and d_B ≤
   g²/√(1 − g²); with SLIDE, g²/√(1 − g²) ≥ ŝ − m, so g ≥ √(ŝ − m) up to second order: an
   axis-aligned deep intruder of a nicked corner sits at least ≈ √(ŝ − m) off the slot.
 * [T, K0-REUSE / Lemma PD] if A contains K_p = [δ_pin, 1 − δ_pin]² (δ_pin = 0.02) in c's frame,
   the packing satisfies k1_00's slack-core root hypothesis and is excluded by k1_00's tree
   (K0-O1); JAM-0 then makes d_B ≤ 4.0·10⁻⁴ — such nicks are also SLIDE-excluded for m < ŝ − 4·10⁻⁴.
 * [T, Lemma ID + R1] some corner has DEPTH ≥ 0.3; not the nicked one necessarily.
 * [C] TF-U's Φ-selection does not combine with Ψ-minimality (a flushing motion of an intruder may
   change its depth), so no "flush-or-locked" clause is claimed for A or B here.
Which nicked configurations remain: all of RES-N(δ_∞) — K0-BLOCKED frames (A90/A91 sense) at
side in (ŝ − δ_∞, ŝ) with a nick in [ŝ − m, δ_∞) at some corner, its deep partner ≥ √(ŝ − m) off
the slot if axis-aligned, and no square containing K_p at any corner. Nothing smaller.

## 4. Canaries

* Trump: K0-FREE ((1,1,2,1) intruders), so Theorem S(δ) and SLIDE do not apply to it; its TL crowd
  (0.1683/0.1555, separating angle ≈ 45°+) satisfies Theorem CEIL (max μ = 0.8445 ≥ 0.7071) and
  Corollary CEIL-2 at δ = 0.155 (cos α + sin α ≥ 1.18 ⟺ α ∈ [11.5°, 78.5°]); the crowd
  hypothesis at a_w < 1 is not realised by any image (§2.4 (ii)): PASS.
* The certified K0-BLOCKED packings at 4.03–4.36 (`d2front87`, D2 0.034–0.293): Corollary CEIL-1
  holds at all of them (max 0.292893 ≤ 0.2928932, certified 6.4·10⁻⁸ under the ceiling); they are
  outside every window of §2–3 (side > s0): no lemma here claims a boundary above their side. PASS.
* s0115 (3.985, nicks 8·10⁻⁹ / 1.7·10⁻⁸ at TL/TR, d₂ = 0.0145 at BL/BR): falls in (N) — it is a
  K0-BLOCKED packing with min_c d₂ < δ for every δ > 8·10⁻⁹ — and is outside the window, so
  neither SLIDE (needs m < ŝ) nor Theorem S constrains it. PASS.

## 5. Obligations ledger and Lean notes

| # | item | status |
|---|---|---|
| A92-O1 | route-3 object empty (no core of D(1−δ), δ < 0.134); weighted certificate replaces it | [T] §2.0, §2.4 |
| A92-O2 | Wedge Lemma; Theorem CEIL; Corollaries CEIL-1/2 (per-corner ceiling 1 − 1/√2, equality case) | [T] §2.1 |
| A92-O3 | routes 1–2 closed: pair charge ≤ 1, 4 < E(ŝ) | [T] §2.2 |
| A92-O4 | Lemma B-YES (transfer with pad (λ−1)(a + 1/√2)); Lemma CW (two-run soundness) | [T] §2.3–2.4 |
| A92-O5 | Theorem S(δ) certificates at s0, window [3.82, s0) | [M] §2.5 — chore |
| A92-O6 | Lemma SLIDE; nick floor d₂ ≥ ŝ − m; Theorem N (chain, residue RES-N(δ_∞)) | [T] §3.1–3.3 (modulo K0-O1) |
| A92-G1 | RES-N(δ_∞): the slab (ŝ − δ_∞, ŝ) with a nick in [ŝ − m, δ_∞); uniqueness at ŝ for nicked non-images | **OPEN** — the exact residue |
| A92-G2 | the certificate chain below the first δ (sub-windows near ŝ): LP constant δ_∞ unknown | [C] §6 |

Lean-readiness. Theorem CEIL is elementary (`nlinarith`-sized after the case split; the Wedge
Lemma is a two-variable inequality). Lemma B-YES is K0-WIDEN's proof with a instead of 1. Lemma CW
consumes `MeasurePy`/V.CASE twice (coverage clause of run B with the exemptions, coverage + total
of run A) and one counting step; it needs no new checker. Lemma SLIDE needs Fact A / Lemma CLUSTER
(A90's N1–N2) plus the exact diagonal rate (a one-line `max` identity) and `teleport_packing`;
it feeds `stratum_kill` (k0_00 piece) in the ∀-packings form, and its consumer is the same
`class_kill` of k1_00 that K0-FREE uses. No `lean/` edits in this attempt.

## 6. Price and next steps

* One crowd certificate: ≈ 1 000 s LP (D4) + 2 × ≈ 100–1 000 s verification; the chain of §3.3
  needs one certificate per factor 0.44 in δ: from δ = 0.05 to 0.005 is 3 certificates, to 0.001
  is 5 — hours, not days — IF the LP passes at those depths (a_w → 1); the first failing depth is
  δ_∞. Sub-window certificates need the A82 emitter's window parametrisation with m_lo > 3.82 (the
  pad formula of §2.3 with λ = s0/m_lo); nothing else changes.
* Boundary above s0 for (S): re-run C(δ, ·) at s = 3.9 / 3.95 (window [s0, s]); each pass raises
  f(δ) to that side. The `d2front87` frontier bounds it from above: f(0.078) ≤ 4.10, f(0.034) ≤ 4.038.
* [S] A near-Trump reduction of RES-N is available IF k1_00's tree is re-emitted at a side s₁ > ŝ
  (window [ŝ, s₁) in its (D)-leaf form): SLIDE's P″ then has side m + T ∈ [ŝ, s₁) with a corner slot
  square, so it lands in a (D) leaf — within the landing radii (1.6·10⁻³, 2.1·10⁻³) of a Trump image
  — and every RES-N packing is an image with one slot square swapped for an intruder and one
  cluster shifted by ≤ √2·δ_∞ along a diagonal: the A91 archetype, localised. With the present
  tree (s0 = ŝ + 4·10⁻⁷) the window above ŝ is 4·10⁻⁷ wide and the reduction is void.
* RES-N(δ_∞) is where the PI conjecture now lives; its refutation is a statement about packings
  within δ_∞ of ŝ, i.e. the regime of the basin/tube machinery (E.A36, A83) — a natural next
  question is whether a K0-BLOCKED packing at side ŝ − ε with a nick of size ≈ ε can exist at all
  as ε → 0 (a limit at ŝ would be a K0-BLOCKED-or-tangent packing at ŝ, i.e. a Trump image by the
  uniqueness clause — but Trump's images are NOT limits of K0-BLOCKED packings with all four
  corners doubly met unless the tangent squares 1/8/9 can be nicked at zero side cost, which
  rigidity (A22) forbids to first order). That is the (N) attack for the next attempt.
