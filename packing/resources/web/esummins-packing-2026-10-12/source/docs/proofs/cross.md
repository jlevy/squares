# CROSS — the PI's X-sketch made exact: Lemma OPPOSE tested and refuted, the torque of a corner joint, the bracing chains, Theorem CROSS-PLANAR, and the shared square — A240, 2026-09-16

The PI (12:00): "Using C and W to denote different torques, and the fact that corner jams require opposing torques, we end up
with this cross shape, where the left C grain needs to touch the right C grain to brace against the opposite wall, but that
would prevent the W grains from meeting.  So my intuition is that such a configuration that is globally locked is not
possible."  This file makes each step exact for every n, proves what is a theorem, tests every step on every witness
corner, and says what the sketch leaves.  Tags: [T] proved, [S] routine given cited items, [M] measured, [F] false (with
the witness), [C] obligation.  Sources: `local_lock.md` (RADIAL, CHAIN, NO-SELF-STRESS, LOCKED-CROWD-FREE), `wall_torque.md`
(Lemma W, TWO-CONTACT, ONE-TILTED, STRUT), `k0_count.md` (PUSH, HOLD), `two_grains.md` (handedness, CORNER-LOAD),
`handedness.md` (TORQUE-ID, the reservoir), `no_vv.md`, A217 `notes/torque.md` (the gear rule as stated), A219 `rows219`,
A234 `stress234`.  Code `attempts/A240-cross/code/` (`cross240.py`, `summarise240.py`, `pages240.py`, `test240.py`); results
`results/cross240.{jsonl,md}`; pages `docs/residue_map/campaigns/A240-cross/`; Lean `Statements/Open/Cross.lean`.

## 0. Verdict

> **[F] Lemma OPPOSE is false.**  At a LOCKED open corner (both meeters loaded, no external row on either) the two meeters
> are SAME-handed in 215 of 1 363 doubly-met corners and opposite-handed in 11 (T1 of `cross240.md`): HELD 121 : 9, CROWD
> 50 : 1, and — decisive, no external row anywhere — the free Fritz-John points 44 : 1.  Most same-handed locks are flush
> same-tilt pairs (HELD 114, FJ 36, CROWD 41), but 23 are vertex-on-edge pairs, 17 of them with both tilts ≥ 1° off flat.
> The reason is exact (§1, Lemma PARTNER-TORQUE [T]): the torque a partner contact puts on the VERTEX owner is a function of
> the tilt DIFFERENCE, the torque on the EDGE owner a function of the contact POSITION along the edge, and a flush pair's
> line of action is free in the overlap — handedness (tilt ≶ 45°) enters none of them.  The ring's same-handed corners need
> the tilt floor because their unloaded-wall meeters (4, 8, 2) are two-contact squares whose forces are not collinear
> (Lemma STRUT's condition fails), not because of handedness; 121 HELD and 44 free locked same-handed corners are balanced
> by walls and contacts alone.
>
> **[F] Alternation (ii)** occurs on 0 of 193 four-crowds; 110 have a wall whose two meeters are loaded with OPPOSITE
> handedness (T5), the ring's floor (4 '−' | 6 '+') and ceiling among them — exactly what CORNER-LOAD's corollary says two
> floor meeters holding each other must do.
>
> **[T] Chains (iii)** are Corollary CHAIN; made exact in §3 ("braces against the opposite wall" = the loaded component of the
> corner's meeters reaches the wall opposite to one of its two walls) and measured: on the four-crowds 525 of 618 loaded
> crowd components reach BOTH far walls and 486 contain the OPPOSITE corner's meeters — the loaded component is the whole
> packing; at the free FJ points 68 / 84 (T8).
>
> **[T] Planarity (iv) is Theorem CROSS-PLANAR** (§4, Lean `crossing_lemma` (classical), `chains_meet`,
> `chains_share_or_touch`): a left-right chain and a floor-ceiling chain of closed squares in a packing SHARE a square OR a
> square of one TOUCHES a square of the other.  The second alternative is real: on 589 witnesses carrying both loaded
> chains, 586 share a square and 3 (the n = 26 record `square-26b`, two free FJ points) meet only at an unloaded contact.
>
> **[F] The shared square (v) is not obstructed.**  On the 126 four-crowds with both loaded chains the crossing carries
> 220 shared squares: 90 are TILTED squares that are not meeters and carry no external row — they take both chains and are
> torque-balanced by their contacts (47 four-crowds have every crossing square of this kind); 38 more are tilted meeters
> with no external row; the ring's crossing is its tilted meeter 6 (VV + flush, external load 0).  The gear rule bites on
> wall-touchers only (Lemma W); an interior grain receives holder torques of both signs (A217, 254 / 254).  The flush case
> (b) is realised at the optimum itself: Trump's chains cross at the flush square 3 on the left wall.
>
> **[C] So CROSS + A233 does not close LOCKED-CROWD-FREE(n) for any n and does not reduce it to the flush-crossing case:
> both the tilted and the flush crossing exist and balance.  The residue is unchanged; at n = 11 it is RAISE(0 → 1) / STEP.**

## 1. Lemma OPPOSE and the torque of a corner joint (task 1)

**1.1 The statement as meant.**  Corner c, frame (u, v), meeters A (NW cell, touching the u-wall) and B (SE cell, touching
the floor), frame tilts φ_A, φ_B ∈ [0°, 90°), handedness χ = +1 for φ < 45°, −1 for φ > 45°, 0 flat / diamond.  LOCKED: both
meeters carry a loaded wall or pair row and no external row (tilt bound, crowd pull) is loaded on either — the corner's joint
is force- and torque-balanced by walls and contacts alone.  *Conjecture OPPOSE:* at a locked corner χ_A = −χ_B.  Reading of
the gear rule: Lemma W torques each meeter toward its own alignment (sign −χ); if the partner contact had to supply the
anti-aligning torque (+χ) to both, the joint would be a pair of meshing gears turning in opposite senses.

**1.2 [T] Lemma PARTNER-TORQUE (any n).**  A loaded vertex-on-edge row (vertex h_k of square P on edge e of square O, multiplier
λ, outward normal n_e(θ_O) = R(θ_O) ν_e, contact point V) exerts about the centres
  τ_P = λ · h_k × R(θ_O − θ_P) ν_e     (the VERTEX owner: a function of the tilt difference and the labels (k, e) only),
  τ_O = λ · x,  x = t·(V − c_O), t = J n_e   (the EDGE owner: the tangential coordinate of the contact, a POSITION).
*Proof.*  ∂_θ of the row n_e(θ_O)·(V(θ_P) − c_O) − ½: V − c_P = R(θ_P) h_k gives ∂_{θ_P} = n_e·J R(θ_P) h_k = (R(θ_P) h_k) × n_e =
h_k × R(θ_O − θ_P) ν_e (a cross product is rotation-invariant); ∂_{θ_O} = (J n_e)·(V − c_O) = x. ∎  [M] test 1: error ≤ 10⁻¹⁵
on the 2 272 loaded edge rows of Trump + A217's witnesses.
**Corner form.**  At the {NW, SE} joint PUSH fixes the force on B to λ n, n = (sin φ_o, −cos φ_o), φ_o the OWNER's frame tilt
(`two_grains.md` 1.4).  If B owns (A's vertex on B's top edge, x ∈ [−½, ½] toward B's top vertex): τ_B = −λ x, and with
δ = φ_B − φ_A: τ_A = −λ (cos δ + sin δ)/2 when φ_A > φ_B (A's lowest vertex), τ_A = λ (cos δ − sin δ)/2 when φ_A < φ_B (A's
rightmost vertex).  If A owns (B's vertex on A's bottom edge): τ_A = λ x and the mirror formulas for τ_B.  Hence
  sign τ_{vertex owner} = sign(φ_owner − φ_vertex owner) for a tilt gap < 45° (the vertex owner is turned TOWARD its
  partner's tilt), reversed beyond 45°;   sign τ_{edge owner} = −sign x, free.
A FLUSH pair (φ_A = φ_B) carries two rows along the common normal: its line of action is anywhere in the overlap and both
torques are free in sign.  **Nothing in the joint's torque bookkeeping sees whether φ is below or above 45°**: OPPOSE cannot be a
consequence of Lemma W + PUSH + HOLD + the balance of the joint, and a same-handed locked joint is the generic case
(a flush pair is automatically same-handed).

**1.3 [M] The test** (`cross240.py`, every doubly-met corner of every stressed witness: Trump, S02, S07, 21 records, A217's
486 witnesses, the 883 free FJ points; the bounded L1-minimal FJ stress of A234, torques in the frame):

| lock status × frame pair | same | opposite | flat / diamond |
|---|---|---|---|
| LOCKED (both loaded, no external row): HELD / CROWD / free FJ / Trump / records | 121 / 50 / 44 / 0 / 0 | 9 / 1 / 1 / 0 / 0 | 6 / 22 / 39 / 1 / 1 |
| external row loaded on a meeter (HELD / CROWD) | 279 / 296 | 26 / 9 | 2 / 228 |
| a meeter unloaded (rattler crowds) | 16 / 113 / 64 | 0 / 13 / 2 | 0 / 8 / 12 |

Locked by partner contact type: same/flush 191, same/VE 23, same/none 1, opposite/VE 11, flat/… 69 (T2).  The partner torque
is anti-aligning on both meeters (pattern AA) at 97 locked corners, on one only (Aa) at 126, on neither (aa) at 2 (T3): the
"meshing gears" sign pattern is one of three that occur.  Lemma W: sign −χ on 2 382 / 2 382 loaded tilted meeters; 326 flat
wall-loaded meeters carry a free self-torque.  Examples (page `oppose_corners.svg`): a HELD flush same-handed lock, the free FJ
point `fj_rand_0_0073_free` TR (tilts 81.9° and 75.1°, VE, both wall-loaded, locked), a HELD opposite-handed lock
(`w300_held` BR), Trump's TL (flat + 49.8°).

**1.4 The ring's tilt floor.**  `rand_0_0569|t20` (T4): every corner is a flush same-handed pair and the tilt bound is loaded on
4 (−0.300), 7 (−0.018), 8 (+0.196), 2 (+0.073); 4, 8, 2 carry NO wall load and exactly two loaded contacts (the flush partner
and the lean / holder), whose forces are not collinear — a two-force member is stationary only under STRUT's collinearity
(`wall_torque.md` §5), so a third torque is needed and the bound supplies it.  "Is that the general fact?" — **no**: the 121
HELD locked same-handed corners are balanced with no bound on their meeters (the bounds sit on other squares), and the 44
free-FJ ones with no external row in the packing at all.

## 2. Alternation (task 2) — [F]

If OPPOSE held, the two meeters of each wall would share the wall's handedness only under a further hypothesis (that a wall's two
meeters are coupled); neither holds.  [M] T5: of the 772 walls of the 193 four-crowds, 373 have one-handed loaded meeters, 144
carry BOTH handednesses, 146 a tilted and a flat one, 75 flat only, 34 none loaded; the PI's alternation (left = right, top =
bottom, left ≠ top, every wall one-handed) occurs on 0 / 193; 110 four-crowds have a mixed wall.  The ring: floor 4 '−' | 6
'+', ceiling 3 '−' | 10 '+', left 5 '−', right 7 '+' — its grains are the LEFT and RIGHT halves (a vertical cut), not the X's
sectors (page `cross_ring_x.svg` (a)).  [T] CORNER-LOAD's corollary (`two_grains.md` 1.4) says the opposite of alternation: two
floor-loaded corners whose floor meeters hold each other directly have OPPOSITE global handedness (a lean).  So CORNER-LOAD is
consistent with the data and inconsistent with (ii); the sector labelling of the sketch has no realisation among the
witnesses.

## 3. The bracing chains (task 3) — [T], measured

**Definition.**  For corner c let U*(c) be the loaded component of its meeters (closure under loaded pair rows, `local_lock.md`
§3.2).  The chain BRACES AGAINST A FAR WALL when a far-wall row of a member is loaded; against the OPPOSITE wall of the
u-wall (resp. floor) when that far wall is x = s (resp. v = s); it reaches the OPPOSITE CORNER when a meeter of the
diagonally opposite corner is in U*(c).  [T] Corollary CHAIN: if any row of U*(c) ∪ {c's walls} is loaded, some far-wall row
of U*(c) or a crowd row is loaded (RADIAL with U = U*(c)).  [M] T8, loaded crowds only: four-crowds 618 corners — both far
walls 525 (opposite corner contained 486), one far wall 79, none 14 (crowd-row anchored, external); free FJ points 84 —
both 68, one 7, none 9; HELD 411 — both 407.  The loaded component of a loaded crowd is, almost always, the whole loaded
packing: the two chains of the sketch are not two objects but one, and "the left grain reaches the right wall" is CHAIN's
statement with no extra content.  Where the 953 unanchored clusters of A233 end is answered by their class: rattler meeters.

## 4. Theorem CROSS-PLANAR (task 4, the Jordan step) — [T]

**Lemma CROSSING (classical).**  Let K, L ⊆ [0, s]² be compact and connected, K meeting the left wall {x = 0} and the right
wall {x = s}, L meeting the floor {y = 0} and the ceiling {y = s}.  Then K ∩ L ≠ ∅.
*Proof.*  Suppose K ∩ L = ∅; d := dist(K, L) > 0.  The open d/3-neighbourhood N_K of K is a union of discs centred in the
connected set K, hence connected, hence (open in the plane) path-connected; so there is a path in N_K ∩ [0, s]² … from a point
of K on the left wall to a point of K on the right wall — by a polygonal path (N_K is open), and likewise a polygonal path in
N_L from the floor to the ceiling; N_K ∩ N_L = ∅.  Two disjoint polygonal paths in the square, one joining the left and right
sides and the other the bottom and top, contradict the Brouwer fixed-point theorem (Maehara, *Amer. Math. Monthly* 91 (1984),
Lemma 1: the map x ↦ x + (d_h(x), d_v(x))-type displacement built from the two paths has no fixed point).  ∎

**Theorem CROSS-PLANAR (any n).**  In a packing of n unit squares at side s, let I be a LEFT-RIGHT CHAIN (a set of squares whose
union is connected and meets the left and the right wall) and J a FLOOR-CEILING CHAIN.  Then (i) ⋃_I Q_i ∩ ⋃_J Q_j ≠ ∅, and
(ii) I and J share a square, or some square of I and some square of J touch (a common boundary point; interiors are disjoint).
*Proof.*  Each Q_i is compact (the continuous image of [0, 1]² under aff), a finite union of compact sets is compact,
connectedness is the hypothesis, containment in [0, s]² is the packing's; CROSSING gives p ∈ Q_i ∩ Q_j with i ∈ I, j ∈ J; i = j
or i ≠ j.  ∎  Lean: `crossing_lemma` (axiom, classical, not in Mathlib), `isCompact_of_isUnitSquare`, `chains_meet`,
`chains_share_or_touch` (theorems).  A contact chain's union is connected (each square is connected and consecutive members
share a point), so the loaded component of §3 is a chain whenever it reaches both walls.
**What the sketch omits: alternative (ii-b).**  The chains may meet at a contact carrying NO load — then no square carries
both grains.  [M] On the 589 stressed witnesses with both loaded chains: 586 share a square, 3 only touch — the n = 26
record `square-26b` (chain squares 2|1, 18|17, 18|21, 20|17, 20|21 in contact, unloaded), `fj_cp85_188_free`,
`fj_rand_0_0543_free`; never neither (test 4).  On the 193 four-crowds: both chains exist on 126 (LR only 19, TB only 21,
neither 27 — the crowd-pulled ones), shared squares 1–5 per witness, always ≥ 1.  No four-crowd has an LR and a TB chain
avoiding every corner meeter (0 / 193): at n = 11 eight of eleven squares are meeters and the crossing sits in the corner
arms or next to them; at large n the interior crossing is the generic case, and it is the case §5 shows to be unobstructed.

## 5. The shared square (task 4 (v)) — tilted [F], flush [M, realised at the optimum]

**(a) Tilted.**  A shared square S receives loaded contacts from both chains.  If S touches a wall, Lemma W torques it with
sign −χ_S and TWO-CONTACT demands two further contacts — supplied by the two chains; if S is interior, no wall torque
constrains it and A217 measured holder torques of BOTH signs on every loaded interior grain (254 / 254).  The chains' contacts
on S are vertex-on-edge or flush rows whose torques are PARTNER-TORQUE's — tilt differences and positions — and the two
"torque senses" C and W are handedness labels that the rows do not carry.  [M] T7: of the 220 crossing squares on the 126
four-crowds, 90 are tilted non-meeters with no external row, 38 tilted meeters with no external row (the ring's 6: '+', VV
lean 4|6 and flush 6|7, external load 0), 64 tilted meeters with a crowd pull; 47 four-crowds have every crossing square
tilted and externally unloaded (page `cross_ring_x.svg` (c): `w037_crowd`, crossing at the interior square 0).  So (v) is
FALSE as a local statement about the shared square: its torque balance closes.  What fails at these witnesses is elsewhere
(the crowd pulls / tilt bounds on other squares — RING).
**(b) Flush.**  A flush square at the crossing is torque-neutral on every edge (two vertex rows per contact, self-torque free
in ±W/2): the reservoir of `handedness.md` §4.  [M] Trump: LR chain 3–1–8–2, TB chain 0–3–7–9–5, shared square 3, flush on the
left wall, contacts flush / flush / VE — the optimum has a flush crossing.  In a four-crowd a floating flush square (no slot)
braced by two chains needs its four contacts to close force and torque balance with zero wall torque — nothing prevents it;
18 flush meeters and 6 flush non-meeters sit at four-crowd crossings.  Neither case is the residue; both are ordinary.

## 6. What is proved, what is open

[T] PARTNER-TORQUE (§1.2), CROSSING and CROSS-PLANAR (§4), CHAIN (A233) — every one n-general.  [F] OPPOSE, alternation, the
shared-square obstruction — refuted on free FJ points and on the ring.  [C] LOCKED-CROWD-FREE(n) exactly as A233 left it:
CROSS + A233 does not close it for any n and does not reduce it to the flush-crossing case.  What the X-sketch is right
about is CHAIN + CROSS-PLANAR: a locked four-crowd's load paths form one connected structure that crosses itself; what it
lacks is any per-square obstruction at the crossing, because torque signs are not grain labels.  No axiom is added for a
refuted statement.  n = 11: k0_00 unchanged (RAISE(0 → 1) / STEP).

## 7. Files, reproduction

`python cross240.py` (13 s, 1 393 witnesses; 1 python, BelowNormal), `python summarise240.py`, `python pages240.py` (3 pages,
11 panels, geometry check printed per panel), `python test240.py` (5 checks, 40 s); Lean `lake build` + `lean/audit.py`
(`logs/lean240.log`).  Resume: `bash attempts/A240-cross/code/run240.sh`.
