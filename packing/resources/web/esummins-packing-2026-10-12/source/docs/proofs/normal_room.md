# NORMAL-ROOM — the pocket of the normal ring holds ONE square: every free square contains the centre — A259, 2026-09-21

The room half of the k0 exclusion in normal form.  A258 (NORMAL-RING, `attempts/A258-normal-ring/notes/family258.md`)
gives the family: a pinwheel of four common-tilt PAIRS of one sense, (a_w, φ_w) per wall + s.  This note bounds the
room of its pocket.  **Domain used: D′ of family258.md VERSION 1 (draft)** — (D1) 0 < φ_w < 45°, (D2) a_w < 1 and
b_w < 1 (every corner box doubly met), (D4) the eight squares a packing; NOT the slot cut (D3).  D ⊆ D′, so every
bound here holds on D.  Tags: [T] proved, [T-computed] certified by a box-valid certificate with its own verifier,
[M] measured, [C] conjecture, [F] false (witness).  Code `attempts/A259-normal-room/code/` (`geom259`, `room259`,
`pair259`, `cert259`, `verify259`, `adv259`, `sample259`, `pairscan259`, `gapscan259`, `capacity259`, `pages259`,
`run259.sh`); results `attempts/A259-normal-room/results/`; certificate `attempts/A259-normal-room/certs/`; pages
`docs/residue_map/campaigns/A259-normal-room/{normal_pocket,corner_gap,worst_case}.svg`; Lean
`Statements/Open/NormalRoom.lean`.  Notation: c = cos φ, z = sin φ, w(θ) = cos θ + sin θ, O = (s/2, s/2), a row's
START offset a (= δ) and END gap b (= e) = s − a − sec φ − c − z.

## 0. Verdict

> **NORMAL-ROOM(11) in the form PIERCE(1) by the container centre: on D′, for s ∈ [3.82, 3.8771] ∋ ŝ, every unit
> square of the pocket contains O in its interior; so the pocket holds ONE square, 8 + 1 = 9 < 11.**
> Status: **[T]** the reduction to four CORNER-PAIR lemmas (4 parameters each, s eliminated; §2), HOLE-ONE in tilt
> form, TOOTH, WEDGE (§2); **[T-computed]** the CORNER-PAIR lemma on the whole pair domain EXCEPT the double-limit
> layer {b > 63/64 and a′ > 63/64 at one corner} (§3; certificate tree launched, ≈ 2 CPU-h, first cells all
> certified, none OPEN); **[C]** that layer (obligation CORNER-NOTCH: at b = a′ = 1 exactly a unit square fits the
> corner gap, so NO box-valid certificate can exist there; [M] 0 counterexamples in 6 177 sampled pairs, 54 rings).
> **[M] the sharp form, ROTATED-HOLE:** a free square of tilt ψ lies in the ψ-ROTATED copy of the flush hole, the
> square of side s − 2 about O; the sup over D′ of the miss-margin is exactly −(4 − s)/2 (the flush limit, where it
> is HOLE-ONE's slack): **MONOTONE-ROOM is true in normal form and the flush limit is extremal** (adversary: 24 runs
> at 3.82 / ŝ / 3.95 / 3.99, all converge to −(4−s)/2 from below; 5 241 + 6 177 random pairs).
> **[F] without (D2):** drop "every row end meets its corner box" and a free square missing O exists at every side
> (+0.17 at ŝ) and TWO disjoint free squares at 3.95 and 3.99 (`capacity259.json`, drawn in `worst_case.svg`).
> The brief's aim (≤ 2, hopefully 1) is met with ONE; there is no separate poker: the poker IS the centre square.

## 1. The pocket of a pair-pinwheel

Floor frame, row of two of tilt φ at START offset a: Q1 = (a+z, 0), (a+w, z), (a+c, w), (a, c), Q2 = Q1 + (sec φ, 0)
(family258 §1).  The row's inner boundary is a SAWTOOTH between depths c and w: tips T1 = (a+c, w), T2 = T1 + (sec φ, 0),
one TOOTH between them — a right-angled notch, apex A = (a + sec φ, c), sides tan φ (along Q1) and 1 (along Q2).  Under
the row: a sealed triangle; beyond its END an open floor wedge of angle φ under Q2 and the END GAP of width b < 1 at
the height of Q2's end vertex (s − b, z); before its START the START GAP, bounded by Q1's edge from (a+z, 0) to its
vertex (a, c).  At a corner the END gap of wall k−1 and the START gap of wall k merge into the CORNER GAP, capped by
the next row's first square, whose lowest vertex sits at depth c′ < 1 and height a′ < 1.

## 2. What is proved  [T]

**2.1 HOLE-ONE, tilt form (Lean `hole_one_tilt`).**  A unit square of tilt θ inside an axis-parallel rectangle of
sides σ_x, σ_y ≤ w(θ) + 1/w(θ) contains the rectangle's centre p (interior if <).  *Proof.*  Its centre q has
|q − p|_∞ ≤ (σ − w)/2 =: h, so for an edge direction u, |(p − q)·u| ≤ h·w ≤ ½.  ∎  (σ ≤ 2 ≤ w + 1/w is A253's
HOLE-ONE; the bound w + 1/w ∈ [2, 2.1213] is what a tilted free square really needs.)

**2.2 MISS ⟹ a corner PAIR.**  Let Q (centre q, tilt ψ ∈ [−45°, 45°), u = (cos ψ, sin ψ), v = u^⊥) be free and
O ∉ int Q.  Then (q − O)·n ≥ ½ for some n ∈ {−v, u, v, −u} — the normal pointing (within 45°) at the floor, right
wall, ceiling, left wall.  Rotate so that n points at the floor (D′ is invariant under the cyclic relabelling of
walls) and split by q_x ≥ s/2 or ≤ s/2; the second case is the first after one more quarter turn with n = u and
q_y ≤ s/2.  So, with PAIR(b, φ; a′, φ′; s) := *no unit square inside [0, s]² and free of the FOUR squares of the
two rows meeting at corner BR (floor row with END gap b, tilt φ; right-wall row with START offset a′, tilt φ′) has
(i) (q − O)·(−v) ≥ ½ and q_x ≥ s/2, or (ii) (q − O)·u ≥ ½ and q_y ≤ s/2*:
**PAIR at the four corners ⟹ every free square contains O.**  Dropping the other four squares only enlarges the
free set, so the reduction is sound; [M] it loses nothing (pair margin = full-ring margin on every sampled ring).

**2.3 s is eliminated (Lean `corner_frame_mono`).**  In the corner frame (origin at BR) the four squares depend on
(b, φ, a′, φ′) only, O = (−s/2, s/2), and for both normals n_x − n_y ≥ 0, so (q − O)·n = q·n + (s/2)(n_x − n_y) is
nondecreasing in s; the half-plane clips q_x ≥ −s/2, q_y ≤ s/2 and the far walls also relax as s grows.  Hence
PAIR(·; s_max) ⟹ PAIR(·; s) for every s ≤ s_max, on the domain b > s_min − 1 − span(φ) (⟸ a < 1 at any s ≥ s_min).
**Four parameters per corner instead of nine** (A251 priced 17 at 5·10¹⁴ CPU-h).

**2.4 TOOTH.**  Let the vertex P of Q nearest a wall lie over that row's tooth span (between the tips), Q's tilt ψ
measured like φ.  Then depth(P) ≥ τ_φ(ψ), with τ = c(1 + sin(φ − ψ)) for 0 ≤ ψ ≤ φ (Q's far edge bridges the two
sides of the notch: contact parameters cos(φ−ψ) ≤ 1 and sin(φ−ψ) ≤ tan φ) and, for ψ ≥ φ, τ = c + z tan φ tan(ψ − φ)
(Q's other edge rests on the lip T1; valid while tan φ ≤ cos(ψ−φ)), else τ = c + z sin(ψ − φ) (that edge ends inside).  In particular **depth ≥ cos φ, with equality only at ψ = φ**, and a
FLAT square enters by at most z(1 − c): c(1 + z) ≥ 1 on [0°, 45°] (Lean `tooth_flat`).  *Proof.*  Q's vertex is a
right-angled wedge with unit sides inside a right-angled notch of the row's tilt; resolve the unit edge on the
notch's two sides.  ∎  ([T-computed] `tooth259`: τ equals the exact centre-set value to 4·10⁻¹⁶ at 7 tilts × 30 ψ; [M] `dipscan259`: least dip over 4 847 pairs = cos φ to 3 decimals, at ψ = φ.)

**2.5 WEDGE (the START gap holds nothing).**  If a < 1, no unit square lies in {x, y ≥ 0, x c + y z ≤ (a + z) c}
(left of Q1's edge line).  *Proof.*  A unit square of tilt θ ∈ [0°, 90°) with lowest vertex (p, q), p ≥ sin θ, q ≥ 0
has support p c + q z + cos(θ−φ) + max(0, sin(φ−θ)) in direction (c, z), which is ≥ f(θ) := sin θ · c + cos(θ−φ) +
max(0, sin(φ−θ)).  On [0, φ] and on [φ, 90°] f is concave (f″ = −f), and f(0) = c + z, f(φ) = z c + 1,
f(90°) = c + z all exceed (a + z) c because a c < 1 and a c < c.  ∎  So a free square near a START corner must lean
over Q1's vertex (a, c) — where the previous row's last square sits (a′-type vertex at height b̃ < 1).

**2.6 The region R and the sub-domain where §2 alone suffices.**  R(ψ) := ∏ [d_k(ψ), s − d_{k+2}(ψ)], d_k := the
least wall depth of a free square of tilt ψ.  If every d_k ≥ τ_{φ_k}(ψ) ≥ cos φ_k, then R(ψ) ⊆ R_cos := [c₃, s − c₁] ×
[c₀, s − c₂], and by 2.1 every free square contains the centre of R_cos as soon as c₀ + c₂ ≥ s − 2 and
c₁ + c₃ ≥ s − 2 (all tilts ≤ 20.2° at ŝ, 24.5° at 3.82; A249's 14.5° ring is inside).  d_k ≥ τ is 2.4 when the
extreme vertex is over the tooth span; when it is over a corner gap it is **GAP-DEPTH-ONE [M → C]: depth ≥ 1**
(`gapscan259`: least END-gap dip 1.0615, least START-gap depth 1.0003, over 6 177 pairs — the corner gaps admit no
poke at all).  GAP-DEPTH-ONE is s-free and m-free; it is the analytic statement still missing (§6).

## 3. The certificate  [T-computed]  (`cert259.py`, `verify259.py`)

PAIR is certified box-valid on (b, φ, a′, φ′) ∈ [0,1] × [0°,45°] × [0,1] × [0°,45°] at s_max = 3.8771 ≥ ŝ, domain
bounds from s_min = 3.82.  **Soundness direction: the pocket is OVER-approximated.**  Over a box each of the four
squares is replaced by its CORE — box-centre pose, half-side 1/(2 w(r_φ)) − ρ, ρ = r_pos + (1 + k sec φ tan φ) r_φ
(mean-value bound on the centre, |·|₁; k = 1 for the square that moves with sec φ) — which lies inside the true
square at EVERY parameter of the box; Q's tilt is binned (1°) and replaced by the KERNEL of half-side 1/(2 w(Δ))
(A237); so C_bin = container ⊖ K minus ⋃(core ⊕ K) contains every admissible centre, and the linear forms are
bounded by (q−O)·n_mid + Δ|q−O| at the polygon vertices (convex).  PRUNE only when two cores of different rows
overlap or the box misses the domain.  Adaptive bisection (tilt radians weighted ×2), depth ≤ 26.
**Benchmark:** 0.04 s per box; even the thinnest samples (margin −0.065) certify at radius (0.01, 0.005 rad);
a 5° × 5° tilt cell costs 50–95 s and ≈ 1 400 leaves; **the whole window ≈ 2 CPU-h** (81 cells) — launched detached
(`run259.sh chain`: tree → verifier → the remaining cross-check samples; resumable per cell, `logs/STOP`).
The first run (s_max = ŝ, archived in `certs/archive_smax_shat/`) certified its 5 cells with 0 OPEN leaves.
**3.1 The LAYER (not certified, grey stipple on `corner_gap.svg`).**  At b = a′ = 1 the corner gap IS a unit
square, so capacity jumps on the closure of D′ and no over-approximation can certify a neighbourhood: boxes inside
{b ≥ 63/64 and a′ ≥ 63/64} are reported LAYER.  One of the two near 1 alone is certified (the other vertex blocks
by a margin).  Own verifier: every CERT / PRUNE leaf re-checked with an independent tilt binning (0.5° bins offset
¼°), exact dyadic tiling identity per cell, LAYER / OPEN listed and never counted.

## 4. Cross-check against exact region search  [M]

`room259.pierce_O`: the exact per-tilt centre sets C(θ) (A222 / A237's configuration space, 1° grid, 0.5° for
reported values) on full rings of 8: **54 rings** (30 random in D′ at ŝ / 3.82 / 3.95; 24 adversarial maximisers at
3.82, ŝ, 3.95, 3.99 — the extremes of D′; the chain appends ≈ 100 more) all have ONE centre-set component and miss-margin < 0: capacity exactly 1.
Worst in D′: −0.0703 (ŝ), −0.1019 (3.82), −0.0288 (3.95), −0.0050 (3.99) against −(4−s)/2 = −0.0615, −0.09,
−0.025, −0.005.  C4 slice at ŝ: −0.064 (2°), −0.11 (14.545°), −0.22 … −0.28 (30°).  Every reported / drawn witness
passes the exact SAT + hard-containment check (`free_margin`); the adversary rejects infeasible proposals (no
penalty terms).

## 5. QUANT-ROOM, MONOTONE-ROOM  (brief task 3)

PAIR on D′ makes A254's non-effective τ₀ unnecessary: the room bound holds at EVERY tilt, not near the flush
stratum only.  QUANT-ROOM in normal form reads: free squares lie in R_cos (constant "c = sin" in A254's form:
1 − cos τ ≤ intrusion ≤ 0) — [T] over the tooth spans, [M] over the gaps.  **MONOTONE-ROOM: restate as
ROTATED-HOLE [M, C]** (§0); retire the tilt-monotone form.  It is stated for the NORMAL ring only: A249's ring
(one teleport per wall from normal) has its own poker room; the exchange of §2.4 of common_sense.md is what
removes it.

## 6. General m  (brief task 4)

Rows of m − 2 (m − 3 teeth each).  [T] for every m: 2.1, 2.4 (each tooth), 2.5, and the corner frame of 2.2–2.3 —
a corner PAIR sees only one row's END and the next row's START, so its geometry is m-free; what changes is the
centre: for m ≥ 5 the statement is not "contains O" but **PEEL in normal form: all n − 4(m−2) free squares lie in
R_cos, so s ≥ 2 min_k cos φ_k + s(n − 4(m−2))** — [T] given GAP-DEPTH-ONE, which is [M] and s-free (one 4-parameter
statement for all m).  For m = 4 the hole side s − 2 cos φ may exceed 2, which is why 2.1's tilt form and the
PAIR certificate are needed; for m ≥ 5 the mid-wall slack (A254 §2.3) does not arise in a normal row (adjacent
squares touch), only the two end gaps per wall.

## 7. Plainly

NORMAL-ROOM(11), capacity ≤ 1: **[T] reduction + [T-computed] on D′ ∖ LAYER for s ∈ [3.82, 3.8771] (pending the
detached tree's index: every cell `ok`) + [C] on the LAYER; [M] everywhere incl. the stretch to 3.99.**  Chain:
NORMAL-RING(11) [C, A258] + `pair_pierce` ⟹ no row-normal packing of 11 is family-stuck on the window (Lean
`no_normal_family_stuck`) ⟹ with ONE-STEP NORMALISATION [T] FAMILY-STUCK-EXIST(11) in value form ⟹ k0_00.
**Remaining obligations, exactly:** (O1) CORNER-NOTCH: PAIR for b, a′ ∈ (63/64, 1) — analytic, s-free; the natural
proof is GAP-DEPTH-ONE via 2.5 + the capping vertex; (O2) the detached tree finishing with 0 OPEN and the verifier
passing (`results/verify259.json`); (O3) the stretch (ŝ, 4): rerun `cert259` with s_max = 3.95, 3.99 (margin
(4−s)/2 → finer boxes; est. 10–40 CPU-h at 3.99), not launched; (O4) NORMAL-RING(11) itself and family258 VERSION 2
(mixed senses — A258: a +++− ring of pairs exists from s = 3.9298 > ŝ, so on the STRETCH the one-sense D′ is not the
whole family and the mixed corner PAIR types (+−, −+) need their own certificate, same 4-parameter design; rows of
three, type F, a third box meeter): the room of THOSE structures is not bounded here;
(O5) Lean: `pair_pierce` is an axiom; its reduction §2.2 is prose.

## 8. What the brief had wrong

1. "at most TWO (poker + centre square)": in normal form there is no second square anywhere on D′ — the poker is
the centre square; the corner gap holds nothing (depth ≥ 1).  2. "centre square of side s − 2(cos + sin)-ish
enlarged by POKE": the teeth reach depth cos φ, so the box is s − 2 cos φ (> 2 beyond 20°: a box argument alone
fails there), and the sharp region is the ROTATED hole of side s − 2.  3. "≤ 9 coordinates": 4 per corner, s
eliminated, and the certificate costs hours, not the 150 CPU-h budget.  4. Not said in the brief: the statement is
NOT uniform on D′ — at the closed corner b = a′ = 1 the capacity jumps, so (D2) strictness is essential and a
layer must be closed analytically.
