# RING-CAPACITY — a stable ring needs side ≥ ⌈√n⌉: the statement made exact, the capacity route made exact, and why the count closes nothing — A236, 2026-09-15

The PI (21:00): *"show that the minimal side required to build a stable ring requires a side length strictly greater than
the trivial packing at ⌈√n⌉"*, by CAPACITY: the ring occupies the perimeter band, its tilted members intrude, the interior
left for the other n − p squares is a square of side ≤ s − 2 − 2ι whose capacity must be ≥ n − p.  This file (i) makes
"stable ring" exact, (ii) proves every piece of the capacity route that is true — the band/core/straddler trichotomy,
TILT-BAND (every tilted square intrudes, with no floor), BAND-FLUSH, BAND-COUNT, CORE-CAP, Lemma TWO — (iii) computes the
count for every n and shows it closes for NO n (Theorem NO-CLOSURE: the band and the core have room for exactly m² − 3
squares, one for every n that packs below m), (iv) tests every step on the ring, the 193 held four-crowds, A226's crowd
rings and the 21 records, and (v) states the residue exactly: the POCKET.  Tags: [T] proved, [S] routine given cited items,
[M] measured, [F] false (with the witness), [C] obligation.  Sources: `local_lock.md` (A233: EXTREMAL, LOCKED-CROWD-FREE,
RADIAL, CHAIN), `one_flush.md` (A226: CROWD-ABOVE, ring11), `two_grains.md` (Lemma FLUSH), `realign.md` (WALL-EXCESS,
the area horn), `wall_torque.md` (CEIL, ONE-TILTED, TWO-CONTACT), `tilt_floor_k0.md` (A89: no loaded tilt floor),
`sideband.md` (A2, B1), `literature.md` (Nagamochi, Bentz, Stromquist, Kearney–Shiu, Göbel).  Code
`attempts/A236-ring-capacity/code/` (`band236.py`, `capacity236.py`, `table236.py`, `summarise236.py`, `pages236.py`,
`test236.py`, `run236.sh`), results `results/capacity236.{md,jsonl}`, `table236.{md,jsonl}`, pages
`docs/residue_map/campaigns/A236-ring-capacity/`, Lean `Statements/Open/RingCapacity.lean`.

## 0. Verdict

> **[T] The statement.**  A STABLE RING of n unit squares = a four-crowd (every corner box met by two squares) none of
> whose meeters retreats (§1; LOCKED ⇒ retreat-free, and at the Ψ-minimal optimum every meeter is retreat-free, A233).
> Conjecture RING-CAPACITY(n) [C]: every stable ring has side ≥ ⌈√n⌉ =: m.  It implies LOCKED-CROWD-FREE(n) and hence
> ONE-FLUSH(n) in value form (Lean `locked_crowd_free_of_ring_capacity`, `one_flush_value_of_ring_capacity`); at the
> optimum the two are the same statement.  It holds on every packing the lab has (§4): the 193 held four-crowds sit at
> side ≥ 4.0014, A226's crowd rings below 4 hold 9 squares, not 11.
>
> **[T] The capacity route, exact** (§2).  Cut at the unit band.  Every square is a BAND square (interior missing the open
> centre C = (1, s−1)²), a CORE square (inside [1, s−1]²) or a STRADDLER.  Lemma TILT-BAND: for s > 2 + √2 EVERY tilted
> square meets C — the PI's intrusion is real at every tilt — but its depth is cos θ + sin θ − 1 at most and → 0 with the
> tilt: **no intrusion floor**, and none can come from stability (A89: no loaded tilt floor by any local argument).  Lemma
> BAND-FLUSH: a band square is flush and touches a wall.  Lemma BAND-COUNT: a four-crowd below m has B ≤ 4(m − 2) band
> squares (a wall with m − 1 flush touchers claims both its corner boxes, with m − 2 one, and two walls cannot claim the
> same corner).  Lemma CORE-CAP: K ≤ N(s − 2) ≤ (m − 2)² − 3 (Nagamochi's s(k² − 2) = k); at m = 4 Lemma TWO: N(σ) = 1 for
> σ < 2 (a unit square in a container of side < 2 contains its centre in the interior).  ONE-TILTED: X ≥ 4.
>
> **[T] Theorem NO-CLOSURE** (§3, Lean `count_never_closes`): 4(m − 2) + ((m − 2)² − 3) + 4 = m² − 3 ≥ n for every n with
> s(n) < m.  **The band-plus-core count has room for exactly every n that packs below m; the capacity inequality
> excludes a four-crowd for NO n.**  At n = 11: B ≤ 8, K ≤ 1, X ≥ 4, 8 + 1 + 4 = 13 ≥ 11, slack 2.  The table n = 5..60
> (§3) has slack ≥ 2 on all 21 values below m; the flat-core / all-touching ring variant closes only at n = 41, 54, 55 under
> hypotheses stability does not supply.  So: **RING-CAPACITY does NOT close analytically at n = 11, and closes at no n by
> capacity**; what closes A226's family at n = 11 is the POCKET of the eight-square ring (a region holding one square,
> measured), and the n-general residue is Conjecture POCKET(n) (§5) = LOCKED-CROWD-FREE(n) in region form.
>
> **[F] Lemma BAND as a structure statement** ("every chain member lies within √2 of its wall"): Trump's loaded chain crosses
> the container (its five 40.18° strip squares are straddlers of depth up to 0.94), and on the 193 witnesses the loaded
> component contains a core square in 67 and reaches depth 1.0 (median) into the centre.  A ring in the band is one
> loaded four-crowd among others; the CHAIN corollary only says the loaded component reaches a far wall — through the
> interior as often as around it.  **[F] "Records are rings"**: every record n = 5..55 is CROSS-BRACED (X ≥ 1
> straddlers, the tilted grain crossing the band line; Trump X = 5), none is a four-crowd.  k0_00 unchanged.

## 1. Stable ring, exact (any n)

Setting: n unit squares in [0, s]², s > 2 + √2 (a square meets at most one corner box, CC-1(ii); the corner arms are
disjoint from the far walls), m := ⌈√n⌉, s < m.  Corner box (0, 1)² in the corner frame; MEETS = open interiors meet;
FOUR-CROWD = every corner met by ≥ 2 squares (`FourCrowdN`).  **Retreat** (A233, `Retreats`): a re-placement of ONE
square at the same side that strictly lowers its depth at a corner and deepens nothing.  **STABLE RING** [T, definition;
Lean `StableRing`]: a four-crowd none of whose meeters retreats.  Relation to the lab's notions [T]: LOCKED (ROT / ROT-W:
no strictly opening first-order motion) ⇒ retreat-free (`local_lock.md` §1.1); at the Ψ-minimal optimal packing every
square is retreat-free (`no_retreat_of_psiMin`); "all eight meeters loaded" is the measured proxy (the witnesses' bounded
FJ stress).  **Conjecture RING-CAPACITY(n)** [C]: every stable ring of n squares has side ≥ m.  [T] RING-CAPACITY(n) ⇒
LOCKED-CROWD-FREE(n) (the optimal case) ⇒ ONE-FLUSH(n) value form (A233's route).  Conversely LOCKED-CROWD-FREE(n) is
RING-CAPACITY restricted to optimal packings; the PI's form asks it of every packing ("the minimal side to BUILD a stable
ring"), which is what a capacity argument would deliver if it delivered anything, since capacity sees no optimality.
Rattler crowds (A226's CROWD-ABOVE, unloaded meeters that retreat) are excluded by "stable" as the brief intends.

## 2. The capacity route, made exact

**2.1 The trichotomy [T].**  C := (1, s−1)² (the open centre), C̄ := [1, s−1]².  Q is BAND iff int Q ∩ C = ∅ (⟺ Q ∩ C = ∅:
an open set meeting a closed square meets its interior); CORE iff Q ⊂ C̄; STRADDLER otherwise.  Core ⇒ not band (int Q ⊂
int C̄ = C, and int Q ≠ ∅; Lean `core_not_band`, `interior_centreClosed`).  So n = B + K + X exactly (Lean
`band_or_core_or_straddler` for the cases).  [M] on all 224 packings tested.

**2.2 Lemma TILT-BAND [T] (any n, s > 2 + √2).**  Every tilted unit square Q ⊂ [0, s]² (tilt θ ∉ 90°ℤ) meets C.  *Proof.*
By the dihedral symmetry put Q's centre in the BL quadrant (c_x, c_y ≤ s/2); then every point of Q has coordinates
≤ s/2 + 1/√2 < s − 1, so it suffices to find a point with x > 1 and y > 1.  Let a := min_Q x ≥ 0, b := min_Q y ≥ 0,
φ := θ mod 90° ∈ (0°, 90°), c = cos φ, d = sin φ.  The max-x vertex is v_R = (a + c + d, b + d) and the max-y vertex is
v_T = (a + c, b + c + d); they are adjacent, joined by the edge v_R + ℓ(−d, c), ℓ ∈ [0, 1].  A point of it has x > 1 iff
ℓ < (a + c + d − 1)/d =: u and y > 1 iff ℓ > (1 − b − d)/c =: l.  Now l < u: at a = b = 0 it reads d(1 − d) < c(c + d − 1),
i.e. 0 < c² + d² + cd − c − d = (1 − c)(1 − d), true; larger a, b only widen the interval.  Also l < 1 (1 < c + d) and u > 0,
so (max(l, 0), min(u, 1)) ≠ ∅ and some point of the edge, hence of Q, lies in {x > 1, y > 1}.  ∎  **No floor** [T]: for a
square touching its wall the reach beyond the band is exactly ι(φ) = c + d − 1, → 0 as φ → 0 (A226's B′ at tilt ε/2 has
depth O(ε): `ring11` rows, depth 0.015 at ε = 0.02); a stable ring cannot supply a floor either — A89: no loaded tilt
floor θ₀ follows from any local argument, the near-flush jam is first-order consistent with criticality.  [M] TILT-BAND
193/193 four-crowds, 22/22 records, 9/9 crowd rings; 3 000 random squares (`test236.py`).

**2.3 Lemma BAND-FLUSH [T] (s > 2 + √2).**  A band square is flush and touches a wall.  *Proof.*  Tilted ⇒ not band
(2.2).  A flush Q = [a, a+1] × [b, b+1] misses C iff a + 1 ≤ 1 or a ≥ s − 1 or b + 1 ≤ 1 or b ≥ s − 1, i.e. Q touches a wall.
∎  So B = Σ_w f_w where f_w = the flush touchers of wall w, a corner slot square counted twice.  [M] 193/193, 22/22.

**2.4 Lemma BAND-COUNT [T].**  In a four-crowd at side s (no corner slot square, since a slot square makes its corner singly
met) B ≤ 4(⌊s⌋ − 1); below m: B ≤ 4(m − 2).  *Proof.*  The f_w flush touchers of w have disjoint unit x-intervals in
[0, s] (WALL-EXCESS's chords), so f_w ≤ ⌊s⌋.  A flush toucher whose interval starts at a ∈ (0, 1) meets the corner box
at that end (its point (a + ½, ½) is in it): say it CLAIMS the corner.  OVERLAP: two flush touchers claiming the same
corner from its two walls overlap ([a, a+1] × [0, 1] and [0, 1] × [b, b+1] with a, b ∈ (0, 1) share the open rectangle
(a, 1) × (b, 1)); so each corner is claimed by at most one wall.  If f_w = ⌊s⌋ the leftmost interval starts at
a₁ ≤ s − ⌊s⌋ < 1, a₁ ≠ 0, and the rightmost ends ≥ ⌊s⌋ > s − 1: both corners claimed.  If f_w = ⌊s⌋ − 1 the intervals
cannot all lie in [1, s − 1] (length s − 2 < ⌊s⌋ − 1): one corner claimed.  With deficits x_w := ⌊s⌋ − f_w ≥ 0 the claims
are ≥ 2 − x_w per wall and ≤ 4 in all, so Σ x_w ≥ 4.  ∎  [M] 193/193 (B ≤ 12 at s ∈ [4, 5); realised max 5).  At n = 11:
B ≤ 8 (page `n11_capacity.svg` (b): 3 + 2 + 2 + 1).

**2.5 Lemma TWO [T] (any n).**  A unit square inside a square container of side σ < 2 contains the container's centre O in
its interior; hence N(σ) = 1 for σ < 2 (s(2) = 2 exactly).  *Proof.*  Q = c + R_θ[−½, ½]², e := cos θ + sin θ ∈ [1, √2]
(mod 90°).  Q ⊂ [0, σ]² forces |c − O|_∞ ≤ (σ − e)/2, and |R_θᵀ v|_∞ ≤ e |v|_∞, so |R_θᵀ(O − c)|_∞ ≤ e(σ − e)/2 < ½ iff
σ < e + 1/e, and e + 1/e ≥ 2 > σ.  Two interior-disjoint squares cannot both contain O in their interiors.  ∎
[M] 3 000 random squares.  **Lemma CORE-CAP [T-lit].**  K ≤ N(s − 2), N(σ) := max{k : s(k) ≤ σ}; for σ < m − 2, N(σ) ≤
(m − 2)² − 3 by s(k² − 2) = k (Nagamochi 2005, `literature.md` B3), i.e. by the proven staircase s(k²) = s(k² − 1) =
s(k² − 2) = k, s(5) = 2 + 1/√2, s(6..8) = 3, s(10) = 3 + 1/√2, s(13) = 4, s(22) = s(23) = 5, s(33) = 6, s(46) = 7 and
Stromquist's s(11) ≥ 3.789 (`band236.N_proved`); the record staircase gives the conjectural N (`N_record`).  [M] K ≤
N_proved(s − 2) on all 224.

**2.6 The intrusion ι, exact.**  A wall-touching square of tilt φ reaches 1 + ι(φ) = cos φ + sin φ from its wall; its ∞-depth
into the centre d(Q) := sup{t : Q ∩ [1 + t, s − 1 − t]² ≠ ∅} is ≤ ι(φ) near a corner and larger for a hovering square.
[M] the ring's eight meeters: ι = 0.282 (20°), d ∈ [0.21, 0.30]; the 193: tilted meeters' ι median 0.169, min 0 (near-flush
meeters exist), d median 0.16; Trump's crowd carrier (40.18°, the TR crowd in the survey's frame): ι = 0.409, d = 0.41;
its strip squares reach d = 0.94 (`capacity236.md` §1, §3).

## 3. The count, and Theorem NO-CLOSURE

**[T] The inequality.**  In a four-crowd at s < m: n = B + K + X with B ≤ 4(m − 2), K ≤ (m − 2)² − 3, X ≥ 4 (ONE-TILTED:
each corner has a tilted meeter, distinct for s > 2 + √2, and a tilted meeter is a straddler by 2.2 — it is not core, it
meets its corner box).  **Theorem NO-CLOSURE [T]** (Lean `count_never_closes`): 4(m − 2) + ((m − 2)² − 3) + 4 = m² − 3,
and n ≤ m² − 3 whenever s(n) < m (s(m² − 2) = m).  So B_max + K_max + X_min ≥ n: the count never contradicts, at any n,
and it is tight at n = m² − 3 (n = 13, 22, 33, 46 are exactly the values Bentz / Nagamochi had to prove by hand).  The
excess over the grid's accounting is one square: the grid at side m has 4(m − 1) band + (m − 2)² core; below m the band
loses 4 (the claims) and the core loses 3, while n loses 3.  Nothing here uses stability, and nothing can: A226's
CROWD-ABOVE four-crowds exist at every side in (s(n), m) for n = 26, 28, 29, 37, 40, 50, 51, 55, so any inequality valid
for all four-crowds is satisfied there; stability enters only through an intrusion floor (none, 2.2) or through the
straddlers' geometry (§5).  **The table** (`table236.md`, n = 5..60; 21 values below m): slack m² − 3 − n ≥ 2, minimum at
n = 11 (2), 5 at 17, 3 at 19, 4 at 29, 6 at 41, 3 at 55; X_forced = max(4, n − B_max − N(s − 2)) is the trivial 4 at every
n on both staircases — the band and the core alone have room for n everywhere.  The FLAT-CORE variant (every non-ring
square flat inside the core, so n − p ≤ (m − 3)² by Lemma FLUSH, and every ring member a wall toucher, p ≤ 4(m − 1) by
WALL-EXCESS) closes iff n > m² − 2m + 5: n = 41, 54, 55 only — [T] under its hypotheses, [F] as a route (rattlers tilt,
ring members hover: the ring's holder 9 and the 193's loaded components reach depth 1.0 into the centre).  **At n = 11
[T]: B ≤ 8, K ≤ 1, X ≥ 4; the count closes NOT; analytically, nothing below 13 is excluded.**

## 4. The tests (`capacity236.md`)

[M] **The ring + 193 four-crowds** (sides 4.0014..4.42, above m: the lemma must not fire, and it does not): TILT-BAND,
BAND-FLUSH, WALL-EXCESS, touchers ≤ ⌊s⌋, BAND-COUNT, CORE-CAP, ONE-TILTED, B + K + X = 11 on 193/193.  B ∈ {0..5}
(median 1), K ∈ {0..3}, X ∈ {4..11} (median 9): a held four-crowd is almost all straddlers.  The loaded component U (A233's
chain, union over corners): p = 11 on 122, 9–10 on 67 (the ring: p = 9, rest = the rattlers 0 (straddler) and 1 (core));
U contains a core square on 67/193 and reaches depth median 1.02 into the centre — "the ring lies in the band" holds for
the ring (U within depth 0.30, a band of width 1.3) and fails for most crowds.  n − p ≤ N_record(s − 2) on 189/193 (the
4 others have no chain record): consistent, never contradicted, as it must be above m.  **A226's crowd rings** (S = 3.90 /
3.95 / 3.99, ε = 0.02 / 0.05 / 0.10; the only four-crowd family below 4): B = 4 (the lifted flush corner squares, band),
X = 4 (the ε/2-tilted neighbours, depth 0.015–0.073), K = 0; the pocket holds 1 square (A222's greedy placer, 1 not 2;
A226: 1 not 3), its largest flush square has side 1.76–1.96 < 2: 8 + 1 = 9 < 11, while the count allows 13.  **The 21
records**: none a four-crowd (0 doubly-met corners; Trump 1); every one satisfies the lemmas; X ∈ {1..8} straddlers
(median 5) — the records are cross-braced, B is 4(⌊s⌋ − 1) or just below (Göbel n = 10: 8 + 0 + 2; n = 27: 16 + 9 + 2),
K < N(s − 2) strictly on every record (the core is never full: the grain crosses it).  Pages: `ring_band.svg` (the ring, Trump, the
crowd ring at 3.99 with its one square), `n11_capacity.svg` (TILT-BAND's point at 10°, the 8 + 1 slots at n = 11, the
record n = 26 with its straddlers); each panel geometry-checked, note per panel.

## 5. The residue, exactly

What the capacity route needs and does not have is a bound on the STRADDLERS beyond X ≥ 4 — equivalently, on the packing
number of the ring's POCKET.  **Conjecture POCKET(n) [C]** (n-general): for every stable ring at side s < m with loaded
component U (p = |U|), the region [0, s]² ∖ ∪U holds fewer than n − p unit squares.  [T] POCKET(n) ⟺ RING-CAPACITY(n)
(a stable ring at s < m is exactly a packing of the other n − p squares into the pocket).  This is a region-packing
statement: the pocket of the eight-square ring at n = 11 is a pinwheel (central box of side S − 2 − ε with four stubs of
width ≈ 0.9) whose capacity 1 is measured, not derived — a flush square cannot enter a stub of width < 1, a tilted square
enters by a tip only, but the exact capacity of a pinwheel with side-1.96 centre and 0.9 stubs is a search.  What a
large-n stable ring would need, n-generally: its straddlers must destroy m² − 3 − n + 1 ≥ 3 of the count's slots
(at n = 11: 3 of 13) — every tilted meeter kills band slots only through the claims (already counted) and core slots only
through its intrusion, which has no floor; so the residue is not a local waste count but the global shape of the pocket,
the same obstruction `one_flush.md` §3.3 (c) and `realign.md` §4 met (O(ε) waste per crowd; the area horn 3 < 4.03 at
n = 11).  **At n = 11 the exact obligation is unchanged**: LOCKED-CROWD-FREE(11) = POCKET(11) on [3.82, ŝ], the k0_00
row; no capacity argument shortens it, and A226's one ring family plus A217's 883 FJ points are its evidence.

## 6. Lean, files, obligations

`Statements/Open/RingCapacity.lean`: `centreOpen`, `centreClosed`, `IsBand`, `IsCore`, `IsStraddler`, `StableRing`;
axiom `ring_capacity` ([C], n-general, every packing); theorems `locked_crowd_free_of_ring_capacity`,
`one_flush_value_of_ring_capacity` (ONE-FLUSH(n) value form via `no_retreat_of_psiMin`),
`optimal_psiMin_not_stuck_of_ring_capacity` (n = 11), `interior_centreClosed`, `core_not_band`,
`band_or_core_or_straddler`, `count_never_closes` (NO-CLOSURE, pure arithmetic); `lake build` + `lean/audit.py` exit 0,
no sorry.  Obligations: O-TILT-BAND, O-BAND-FLUSH, O-BAND-COUNT, O-TWO (the four [T] lemmas of §2 over `IsUnitSquare`,
routine but not done); POCKET(n) [C].  Resume: `bash attempts/A236-ring-capacity/code/run236.sh` (25 s of python, then
the Lean build + audit ≈ 5 min; `--lean-only` for the build alone).
