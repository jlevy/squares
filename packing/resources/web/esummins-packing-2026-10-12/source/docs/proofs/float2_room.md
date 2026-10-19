# FLOAT2 ROOM — the room statement of link 5d is CAP-2 of the two box meeters (n ≤ 8 + cap(S_8), and the blockers are pocket squares); one blocker blocks one drop (ONE-DROP), two floaters block at most one drop each of the other (MUTUAL); the FLOAT2 witness has a FREE floor drop and is one Φ₁-step from a JAM corner; the strip lemma transfers to a FLOAT2 floater exactly when its blocker serves the far box; the indirect jam needs no reduction to the direct one, only the same CAP-2; a 6-parameter diameter certificate is designed, benched (12/12 points CERT) and priced 30–1000 CPU-h — not launched — A277, 2026-09-23

The brief (A277 BRIEF): the ROOM statement for the FLOAT2 corner ((a): which of C, D can be replaced by its drop, a
STRIP₂-type lemma each, then pair-type sectors), the INDIRECT JAM ((b): a non-toucher holder; reduce to the direct
jam, to a smaller room, or draw the escape), and what NO-JAM(11) then still lacks ((c)).  Derivation in pieces:
`attempts/A277-float2-room/notes/float277_part0..7.md`.  Tags [T] proved, [T-computed] exact finite check, [M]
measured, [C] conjecture, [F] false (witness).  Code `attempts/A277-float2-room/code/` (`witness277`, `ypoke277`,
`witness277b` the exact witness checks; `diam277` the sector-region diameter; `float277` the P1-sense FLOAT2 search;
`cert277` the CAP-2 kernel + bench; `page277`), results beside it, page `docs/residue_map/campaigns/A277-float2-room/
float2_room.svg`, Lean `Statements/Open/Float2Room.lean`.  Notation as no_jam.md / ring_domain.md: BL frame, wall
x = 0, floor y = 0, O = (s/2, s/2); a floater F has wall distances h_u(F), h_v(F) > 0 and DROPS T_u(F) = F − h_u e_x,
T_v(F) = F − h_v e_y, STRIPS S_u = T_u ∖ F, S_v = T_v ∖ F; a BLOCKER of a drop meets its interior.

## 0. Verdict

> **[T] ONE-DROP.**  A square interior-disjoint from a box-meeting floater F blocks at most one of T_u(F), T_v(F)
> (BLOCKER-SIDE and its mirror force a separating normal to be (−, +) and (+, −) at once).  **[T] MUTUAL.**  Two
> floaters C, D meeting the open box are either (P) separated by a positive-slope line — then, C upper-left, D may
> block T_v(C) and C may block T_u(D), never the other two — or (N) block no drop of each other.  **[T]** in the
> Φ₁-maximiser every drop of every non-toucher is blocked, so a FLOAT2 corner carries two blockers OUTSIDE {C, D}.
> **[F] the brief's witness reading.**  In `float262.json` A blocks nothing: D's floor drop is FREE (h_v(D) = 0.0047,
> overlap 0 with A, X, C, exact), so D drops, becomes a floor toucher meeting the box, and the corner is a JAM corner
> inside H1–H3.  A262's "JAMMED FLOAT2 EXISTS" is A261's coarse-grid J (the drop cell is off the grid).  A floor
> toucher Y (tilt 77.2°, left vertex under D's right vertex) DOES block that drop with every gap ≥ 0.00055 [T-computed]
> — all four drops blocked — but P1 still lands D (a flat floor cell met only by D: J_D = +0.024): **no FLOAT2 corner
> in normal form is in hand**; [M] `float277` (P1-sense objective, drops + any-pose cells): sup ≤ 0 on the 4-square
> model from the witness and random seeds (§4).
> **[T] The statement.**  n ≤ 8 + cap(S_8), S_8 = two meeters per box: every other square — middle touchers and
> blockers included — is a pocket square.  So what n = 11 needs is **CAP-2(S_8)**, and by the two-miss sector
> reduction (A259 §2.2 twice; the PAIR corners kill their misses) it is corner-local:
> **BL-CAP-2(C, D): no two interior-disjoint unit squares, each interior-disjoint from C and D, both with centres in
> the BL sectors and both missing O.**  ROOM (one miss) is one more than needed and is FALSE for FLOAT2 whenever a
> blocker outside S_8 misses O.  Test: the BL-sector admissible-centre region has diameter < 1 (`cap2_of_diam`).
> **[T] The drop route.**  In case (P) T_u(C) and T_v(D) stay interior-disjoint; given STRIP-C, STRIP-D (no sector
> miss meets S_u(C), S_v(D)) BL-CAP-2 reduces to the 4-parameter pair (T_u(C), T_v(D)).  Lemma LOW holds with the
> floating D in A's role (its proof uses only a point of the lower-right square under the separator), so WEDGE-FLOAT
> applies to C and, mirrored, to D; the whole JAM strip lemma (A267–A276) transfers to C iff its blocker is X serving
> TL (H1), and to D iff its blocker is A₂ serving BR.  A middle-toucher or free blocker breaks H1: [C] there.
> **[T] The indirect jam** needs no reduction: its holder is a pocket square, counted by cap(S_8); BL-CAP-2(A, C)
> (5 parameters) covers direct and indirect holders and the middle toucher above X alike.  The "P4 chain ends at a
> toucher" is true and useless (the toucher holds the last link, not C).  No exact escape configuration exists on
> disk: a free holder must enter S_u(C) from the right above X_low through a gap X_low − C_top < 0.56 — the STRIP₂
> geometry with H2 replaced by X_low ≥ C_top, [C].
> **[M] on the dropped witness** the two-obstacle region has diameter 0.936 (a floor miss exists where Y stands),
> with Y the region is empty.  **Certificate** (`cert277`): 6-parameter (5 for JAM) diameter tree, 0.02 s per box,
> 12/12 bench points CERT at radii 1/16–1/1024; price 30–1000 CPU-h (float2), 3–100 (jam): **not launched**.
> **NO-JAM(11) still lacks** (§6): `pair3` (not landed); 5b's two capped cells; 5d = BL-CAP-2(C, D) and BL-CAP-2(A, C)
> [C] with the axiom `bl_cap2_float2`; Lean `jam_count`.  k0_00 unchanged.

## 1. Blockers: ONE-DROP, MUTUAL, and the drop form of P1  [T]  (part 2)

**1.1 ONE-DROP.**  BLOCKER-SIDE (box_meeters.md §1.2; hypotheses: F meets the open box, K interior-disjoint from F,
K meets int T_v(F)): every separating normal n from K to F has n_v > 0 and n_u < 0.  Its mirror for T_u(F): m_u > 0 >
m_v.  Disjoint convex bodies have a separating line; one normal cannot be both (Lean `one_drop_core`).  ∎
**1.2 MUTUAL.**  C, D floaters meeting the open box.  D blocks T_v(C) ⟺ every (D→C) normal is (−, +); C blocks T_u(D)
⟺ every (C→D) normal is (+, −) ⟺ the same; D blocks T_u(C) or C blocks T_v(D) would force (D→C) = (+, −).  So (P):
a positive-slope separator, C upper-left — D may block T_v(C), C may block T_u(D), never the other two; (N): no
positive-slope separator — no mutual blocking.  ∎  **1.3** Φ₁ (# wall touchers) is the first potential of the normal
form (normal_ring.md §1.2); an unblocked drop is a same-side packing with one more toucher.  So every drop of every
non-toucher is blocked, and a FLOAT2 corner has blockers K_C of T_u(C) and K_D of T_v(D) outside {C, D} (case (P); in
(N) at least two outside blockers for four drops).  A blocker is a wall toucher (X above / Y right, missing the box:
X ⊆ {y ≥ 1}, Y ⊆ {x ≥ 1}), a middle toucher, or a non-toucher.

## 2. The witness, exactly  [T-computed]  (part 2.4, `witness277`, `ypoke277`, `witness277b`)

float262.json poses (centre, tilt): C (0.7307, 1.5955, 14.47°), D (0.9503, 0.6035, 12.87°), A (1.9911, 0.6090,
14.45°), X (0.6549, 2.6825, 22.85°).  Drops: T_u(C) ← X (area 0.0024), T_v(C) ← D (0.743), T_u(D) ← C (0.043),
T_v(D) ← nobody (h_v(D) = 0.0047; overlap 0 with A, X, C).  A's leftmost x = 1.382: it meets no box (a MIDDLE toucher).
So D drops to the floor (Φ₁ + 1) and the corner is a JAM corner in H1–H3 (X_top 3.337 > s − 1, X_low 2.028 ≥ 1, X
meets int T_u(C), D′ meets the open box, D′ ∩ int C = ∅).  Y := the floor toucher with cos α = R_y − 0.006 (α =
77.21°), left vertex 0.0008 left of D's right vertex R_D = (1.549, 0.227): gaps Y–D 0.00055, Y–C 0.43, Y–X 1.30, Y
misses the open box (x_min 1.548), Y meets int T_v(D) (area 3.1·10⁻⁷) — all four drops blocked.  But A261's any-pose
P1 test on the coarse grid gives J_D = +0.024 (J_C = −0.0022): a flat floor cell [x, x+1] × [0, 1] with x ∈ (0.37,
0.55) meets D and nothing else (C's part below height 1 ends at x ≈ 0.38, Y starts at 1.548), so Lemma CELLS moves D
onto it: not normal.  Neither A nor Y alone makes the corner normal; both cannot stand (they overlap).

## 3. The statement and its reduction  [T]  (part 3)

**3.1** n ≤ 8 + cap(S_8) (Lean `cap2_count_core`): every non-S_8 square is a pocket square.  **3.2** Two misses ⟹ two
BL-sector misses when the other corners are PAIR-certified (pair3 at BR / TL, PAIR or hybrid at TR; a miss is free of
all of S_8).  **3.3** BL-CAP-2(C, D) as in §0; X, A₂ ∈ S_8 may be added as obstacles, the blockers may not.  s
eliminated at s_max = 3.8771 (`corner_frame_mono`: sector half-planes and container relax with s).  **3.4** Diameter:
two squares with centres at distance < 1 overlap (`inradius_sep`, Lean `cap2_of_diam`).  **3.5 [M]** dropped witness
(`diam277`, 1° grid, exact centre sets): {T_u(C), T_v(D)}: region area 0.121, diam 0.936, worst miss +0.640 at centre
(1.94, 0.77) tilt 13° (page (b), exactly free, misses O); {C, D}: 0.111 / 0.934; adding Y or {X, Y}: empty.

## 4. Does a normal-form FLOAT2 corner exist?  [M]  (`float277`, results/float277.jsonl; part 7)

Objective t = min(local261's terms: gaps, containment, box depths of C and D, X and Y miss the box, floats, every drop
of every floater blocked; and −J_F for every floater F on A261's coarse any-pose grid).  sup t > 0 ⟺ a FLOAT2 corner
that neither a drop nor P1 lands, in the 4- or 5-square local model.  Rows finished at this writing (12 restarts each,
6 seeded from the exact witness of §2 with jitter): **F4 (C, D, X, Y): sup = −0.000000 (seeds 1, 2), NO-WITNESS** — the
optimum is the degenerate boundary (a floater touching); **F5 (+ a fifth floater K as an indirect blocker): sup = −0.000002
(seed 1), NO-WITNESS.**  F5 seed 2, F3 (no floor toucher), F4b (X, Y free to meet the box): see the jsonl / log; whatever they say is [M] for the local model only.

## 5. Strips and the indirect jam  (parts 4, 5)

**5.1 LOW with a floating D [T].**  ring_domain.md (F4) uses of A: a positive-slope separator with A below (SLOPE) and
ONE point of A under it whose height is ≥ cos α (left vertex), the top vertex, or the upper-left edge; D floating has
the same points 0 ≤ h_v(D) higher.  So L_h(C) > 1 (≥ 1.121 in cases a, b) in case (P), and mirrored L_h^mirror(D) > 1.
**5.2 Transfer table.**  STRIP-C = STRIP₂-IN-JAM verbatim iff K_C = X serves TL (H1, H2 hold; (D1) by 5.1): 5b's status
([T] on θ, φ ≤ 5° (A276) + A273's tree, c5_4 / c5_5 capped).  STRIP-D = its mirror iff K_D = A₂ serves BR.  A middle
toucher or a free blocker breaks H1 (X_low > 1.406 is used by A272/A273/A276): [C].  **5.3 Indirect jam [T]**: the
holder is a pocket square; BL-CAP-2(A, C) (5 parameters) is the whole obligation; the P4 chain (antisymmetric "left
of at a shared height") ends at a toucher holding the LAST link — no reduction.  **5.4** Middle toucher above X: S
replaces X in S_8, X is a pocket miss, CAP-2 again; H1 for X fails for the strip route.  **5.5 [C] INDIRECT-FREE**: under
H1 for X and C meeting the box, no non-toucher square disjoint from C and X has a point in S_u(C) — for X_low < C_top
this is STRIP₂-IN-JAM; for X_low ≥ C_top (X not holding C) it is the same shadow geometry with a gap ≤ 0.56, unproved.

## 6. What NO-JAM(11) still lacks, exactly  (BRIEF (c))

(L1) `pair3` at TL and BR (A262 chain3 never produced an index) — needed by every route here for the PAIR corners of a
JAM or FLOAT2 ring.  (L2) 5b's drop tree: c5_4 / c5_5 (θ 25–30°) capped with OPEN leaves; the corner is [T] (A276).
(L3) **5d = two CAP-2 statements, both [C]**: BL-CAP-2(C, D) for FLOAT2 (Lean axiom `bl_cap2_float2`; certificate
designed, 30–1000 CPU-h, not launched; a P1-aware PRUNE first) and BL-CAP-2(A, C) for the indirect JAM and the middle
toucher above X (5 parameters, 3–100 CPU-h; the direct JAM keeps its ROOM route).  Cheaper sub-case: FLOAT2 with both
blockers serving their far boxes — the 4-parameter dropped pair (~3 CPU-h) + 5b's strips.  (L4) [C] INDIRECT-FREE (§5.5)
would delete free holders and leave middle touchers as the only indirect case.  (L5) Lean: `jam_count` stays an axiom;
`bl_cap2_float2` is new; `Float2Corner`, `BLSectorMiss` opaque.  (L6) A normal-form FLOAT2 corner may not exist at all
([M] §4: sup ≤ 0 in the 4-square model); a THEOREM to that effect (P1 with the flat floor cells under D, §2) would remove
BL-CAP-2(C, D) from the list — not attempted here beyond the observation in §2.

## 7. What the brief had wrong

1. "A on the floor and X on the wall block their drops": A blocks nothing (T_v(D) is free); the witness is one drop from
a JAM corner and A262's verdict rests on a coarse grid (§2).  2. "S_min at the corner = {C, D} + their blockers": the
blockers are NOT in S_min and need not be in S_8; charging them as pocket squares is what makes the count close (§3.1) —
and it shows ROOM is the wrong target for FLOAT2 (false whenever a blocker misses O); CAP-2 is right.  3. "Reduce as for
JAM: which of C, D can be replaced by its drop": both can, in case (P), and the strip lemma transfers verbatim — but only
when the blocker serves the far box (§5.2); otherwise the strip is a new [C], and the direct 6-parameter CAP-2 avoids
strips altogether.  4. "The sectors are pair-type certificates already run": A259's PAIR and pair3 need a common-tilt
row; the dropped pair has independent tilts, and two-obstacle ROOM is false on the witness (+0.64); no existing
certificate covers it.  5. "(b) reduces to the direct JAM via the P4 chain": true chain, no reduction (§5.3); the count
never needed one.  6. "A middle toucher above X — harmless for ROOM": harmless for the COUNT via CAP-2; it breaks the
strip route's H1.  7. Right in the brief: WEDGE-FLOAT applies to the FLOAT2 floaters verbatim (with LOW generalised, §5.1).

## 8. Lean, reproduce

`Statements/Open/Float2Room.lean`: theorems `one_drop_core`, `cap2_count_core`, `cap2_of_diam` (from `inradius_sep`),
`float2_ten` (from the axiom); opaque `Float2Corner`, `BLSectorMiss`; axiom [C] `bl_cap2_float2`; one import line in
`Statements.lean`; `lean/AUDIT.md` regenerated, 0 sorry.  Reproduce (< 1 min each unless said): `python witness277.py`,
`python ypoke277.py`, `JAM_COARSE=1 python witness277b.py`, `python diam277.py`, `python page277.py`, `python cert277.py
--mode bench --fam float2|jam`; the search `python float277.py --restarts 12 --seeds 1,2` (≈ 8 min per row, resumable,
one python, BelowNormal).  General n: §1, §3.1–3.4, §5.1 are s-free and n-free (the count reads 4(m − 2) + cap); the
numbers (1.406, 3.8771, the sectors at O) are m = 4.
