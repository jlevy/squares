# Mathematical Review: Overbeck’s Candidate Proof That `s(17) = L`, Correctness Lane

Reviewed 2026-10-13 and 2026-10-14 from the public source
[`Kleddamag/the-seventeenth-square-candidate`](https://github.com/Kleddamag/the-seventeenth-square-candidate)
at pin `653b9589d0f8a152f01adc56b1d48ba53d49abc3` (version 1, candidate, 2026-10-12;
release `large-files-v1` with 12 assets, none downloaded), by an AI agent: the
mathematical-correctness lane of the project’s review of this candidate, a Claude model
at the tbd-strong-max tier, reasoning max.
The lane worked from a clone of the source in its own scratch directory, read the source
freely and executed none of its programs; every computation below is the lane’s own
code, written from the source’s specifications and run under the project interpreter.
The lane was kept blind to the project’s two earlier reviews of this candidate and to
the notes of `T-153` until §§0–9 were written; §10 was added afterwards.
Nothing was posted anywhere, the author was not contacted, and no upstream bytes are
proposed for retention.

This review registers nothing and moves no bound.

## Summary for the Author

The lane read the statement, the proof text (`PROOF.md`, 116 paragraphs), the fifteen
premises and the documents the edition binds to them, the certificate specification
`SPEC_v3.0.md` and the Python checker written from it, the capture checkers and their
specifications, and the records of the rigidity part.
It re-derived or recomputed, with its own code, everything it could reach in the time
available: the root isolation and the twenty decimal places of `L`; the packing at side
exactly `L` (every wall clearance and every pair separation, strict ones by interval
arithmetic and the 29 flush contacts and 22 tangencies by exact ideal membership); every
literal geometric fact of §§3–6 of the proof text; the case partition; the admission of
all eleven roots; the three hand-overs of §8; the whole single-node tree certificate
`JQ` with a checker of its own (which reproduces the stored lower bound of the zero step
exactly, a rational with about 2,500 digits); and the parallel-pair row derivation of §8
by hand and by random test.

No step read here is false.
No finding is blocking or major.
Three findings are minor, all of presentation: a lemma of the root admission that stands
only in a code comment, a compressed normalization argument in the rigidity part whose
record states the needed scale-uniformity but the proof text does not, and admission
margins (one of them exactly zero) that no stored output records.
The remaining findings are notes.
The boundary of this review is the boundary of what could be recomputed: the 98 capture
rows and 12 of the 13 tree certificates were not rerun here, and their acceptance rests
on the author’s two checkers, whose rules the lane found sound as specified and whose
one small instance it reproduced to the last digit.

**Verdict: accepted**, in the record’s vocabulary, with this scope: every argument the
lane read is correct as stated or as repaired by the author’s own known-issues list;
every computation the lane could repeat independently agrees; the large computations it
could not repeat are not vouched for here beyond the soundness of their acceptance
rules.

## 0. What Was Read, Run and Not Reached

Paths are relative to the source root.
`PKT/` stands for
`research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/`,
`WX/` for `research/window-extension-20261008/`, `CAP/` for
`research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture/`
and `AUTH/` for `research/finishing-threshold-goal-20261007/current-author-20261012t/`.

**Read in full.** `STATEMENT.md`, `STATEMENT_STATUS.md`, `PROOF.md` (a byte copy of
`PKT/revision-v7/PROOF.md`), `PREMISES.md`, `KNOWN_ISSUES.md`, `KNOWN_LIMITS.md`;
`PKT/OBLIGATIONS.json` (210 rows, 15 of kind mathematical premise);
`PKT/revision-v7/{CLASS_ROW_LEMMA,NOTATION,GLOSSARY,ANALYTIC_ENVELOPES,FINITE_PARALLEL_DERIVATION}.md`,
`LABELS.tsv`, `scripts/run_adm.py`, `scripts/adm.py`,
`runtime/SELECTED_ORIGINAL_MAP.json`, `runtime/THEOREM_MANIFEST.json`,
`FRAME_DISJOINTNESS_PUBLIC.json`, `SMALL_CHECKS_PUBLIC.json`, `ENDPOINT_AUDIT.md`,
`INDEX_SAFETY.md`, `CAPTURE_EXECUTION_NOTES.json`, `records/THEOREM_G20S.md`;
`WX/SPEC_v3.0.md` (885 lines, all sections), `WX/SPEC_v3.0_NOTES.md`,
`WX/checker/wxcheck_v30.py` sections F to K (the store bounds, the exclusion test, the
declarations, the term rules, the raw and centred remainder rules, store acceptance, the
closures and the tree, root and child conditions, lines 1455–2760),
`WX/acceptance/h_report30.py`, `WX/acceptance/EXPECT_G20S.json`, `EXPECT_HW.json`, the
acceptance reports of `JQ`, `G20S` and `HW`, `WX/bigbox/join/*_exact_*.json`;
`CAP/statements/*/classes.json` for all 98 class certificates,
`CAP/checker_sources/src/{exact_classes,exact_restricted,exact_general,integer_sweep,boolean_rule}.py`,
the restricted-checker specification `RESTRICTED_CHECKER.md` and the class format
`CLASS_FORMAT.md`; the premise documents `FRAME_L9.{md,json}`,
`c7-c8-inherited-producer/PROOF.md`, `case-repair-S/PROOF.md`,
`review-repair-O/{F1_PROOF.md,LOOSE_IDENTITIES.json}`,
`coarse-capacity-AP/PROOF_BRIDGE_V2.md`, `coarse-capacity-R/{PROOF.md,RESULT.json}`,
`reader-corrections-AQ/{WALL_TRIGGERS.json,FRAME_CHECK.json}`,
`endpoint-normalization-producer/THEOREM.md`,
`second-order-20261010/theorem/{ENDPOINT_CASE_G_LEMMA.md,EXACT_ENDPOINT_AND_CASES.json,UPPER_FORMULAS.md,UPPER_LAYOUT.py.txt}`,
`third-order-20261010/manuscript/check_case_partition.py`, and under
`AUTH/g20s-terminal-audit/` the sixteen-square corollary, the full stopped propagation
(`continuation/THEOREM.md`), the finite-entry stop pruning (`PROOF.md`, `PRUNING.json`)
and `MATHEMATICAL_INTERFACE.json`; `upper-packing-certificate.json`; the certificate
`JQ_v1/jQTw.n0.JQ.cert.jsonl.gz` whole.

**Skimmed.** `OVERVIEW.md`, `AUDIT.md`, `READING_ORDER.md`, `CHECK.md`; the head of
`uniform-capture-20261007/uniform.py`; the 72 MB certificate `JPG15p_v5` (header and
node counts only).

**Run (own code only, listed with outputs in §8).** Exact Krawczyk root isolation; the
seed packing at side `R`; the packing at side `L`; 194 literal checks of §§3–6; the case
partition; the admission of the eleven roots; the hand-overs of §8; random tests of
every lemma of `SPEC_v3.0.md`; a checker for the certificate `JQ`; a random test of the
parallel-pair row derivation.

**Not reached.** The 98 capture rows (release assets; each row is hours of exact
sweeping) and 12 of the 13 tree certificates (`JG_v2`, `JPA_v5`, the six `JPG*_v5`,
`JPWS_v4`, `JPW13_v2x`, `G20S`, `HW`; all but `JPG15p_v5` are release assets, and a
replay would need the author’s checker or a checker of this size written here); the
seventeen finite rounds and the five-model continuation of the rigidity part (their
records were read, their dual replays were not repeated); the Node checker
`wxcheck2_v30.js` (not read); the retained reviews inside the edition (not read, by
design of this lane).

## 1. The Statement and the Root

`STATEMENT.md` defines a packing (seventeen closed unit squares in `[0,S]^2`, disjoint
interiors, contacts allowed), two polynomials `F`, `G` in `(t, b)`, the box
`[t_0 ± 10^-12] × [b_0 ± 10^-12]`, `L = (6+4t_*)/(1+2t_*-t_*^2)`, the bound
`4.67553009360455095163 < L < 4.67553009360455095164`, and the claim that a packing at
side `L` exists and every packing has side at least `L`. `STATEMENT_STATUS.md` says the
claim is conditional on the 210 obligations of `PKT/OBLIGATIONS.json`.

The lane proved the definitions well posed with its own exact Krawczyk operator
(`root_isolation.py`, `root_box.py`): on the stated box `K(X)` lies strictly inside `X`
and `‖I − Y·J(X)‖_∞ ≤ 4.985·10^-11`, so the box holds exactly one zero; five contracting
iterations with outward rounding to `10^-90` give `t_*`, `b_*` and
`L = 4.67553009360455095163411127048314664876714385501587969541689…` to ninety places.
The denominator `1+2t_*−t_*^2` is positive, and `L` is decreasing in `t` on the box.
The three rational constants of the proof order as claimed:
`L < R = 4675530093604551/10^15` with `R − L ≈ 4.8366·10^-17`,
`R < C = 4675531/10^6 < U = 1169/250`, and `R − L − ε ≈ 4.319·10^-17 > 0` for the flush
offset `ε` of `PROOF.md` line 269 (P087), which the composition uses to keep `ξ ≤ 0` at
right and top wall ends.
Premise `ALGEBRAIC_ENDPOINT` is proved here.

## 2. The Five Steps

### Step 1, the upper bound (`PROOF.md` §1, lines 23–55; premise `UPPER`)

`UPPER_FORMULAS.md` gives the seventeen centres and directions as rational functions of
`(t, b)`; the side is `(6+4t)/(1+2t−t^2) = L`. The lane evaluated the construction over
its own enclosure of the root (`upper_at_L_check.py`). All 272 corner-to-wall clearances
are nonnegative: 243 are strictly positive by interval arithmetic and 29 are exactly
zero, proved by reducing the numerator of the exact expression to zero modulo a lex
Gröbner basis of `(F, G)` (three polynomials of total degrees 22, 22 and 23) with the
denominator bounded away from zero on the enclosure.
All 136 pairs have disjoint interiors: 114 strictly by a separating side direction with
positive interval margin, and 22 with a tangency, the touching corner expressions again
exactly zero. The divisors `c`, `s` and `slack` of the formulas are positive on the
enclosure, so every formula is defined.
The tangent pairs, in construction labels, are (1,2), (1,3), (2,3), (2,4), (2,13),
(3,9), (3,11), (4,10), (5,7), (7,14), (8,16), (9,10), (9,11), (10,12), (10,15), (11,12),
(12,14), (12,16), (13,14), (14,17), (15,16), (16,17). `s(17) ≤ L` is therefore proved
here, independently of the author’s `check_endpoint.py`.

The lane also checked the rational seed `upper-packing-certificate.json` at side `R`
(`seed_packing_check.py`): 68 wall clearances nonnegative with minimum exactly `ε` (14
flush sides), 136 pairs separated, none touching.
This is the reference file whose SHA-256 every tree certificate names; the trees’
reference centres and directions are read from it, with `p_13` corrected by
`−(T_0/3)v_13` as `SPEC_v3.0.md` line 63 prescribes.

### Step 2, capture (`PROOF.md` §§2–6, lines 56–222)

**Normalization (P021, line 71; premise `ENDPOINT`).** A packing of side `S_0 < L` is
translated by `(L−S_0)/2` and lies strictly inside `[0,L]^2`; placed concentrically in
`F_U = [0,U]^2` it lies inside the concentric square of side `C > L`, for which the
class certificates are stated.
`endpoint-normalization-producer/THEOREM.md` proves this; it is a translation, so
parents, poses and labels are preserved.
Proved here by reading.

**Class certificates (P030–P039, lines 97–124; premise `CHARGE_SEMANTICS`).** The 98
certificates are weighted counting certificates of the kind this project already holds
for the `4.66001` bound: sites, Boolean features, a budget `M`, a charge scale `Γ`, rows
of angle intervals with a concentric core square, and closed pose classes with
thresholds. The class-row lemma (`PKT/revision-v7/CLASS_ROW_LEMMA.md`) states that a
complete passed row cover gives `Γ Σ_p τ(p) ≤ M < βΓ` for every packing in the side-`C`
square, where `τ(p)` is the minimum threshold of a class containing the pose, and `1`
outside every class.
The lane read the four links of the lemma (capacity, row validity, closed-boundary limit
with the cell level, sweep arithmetic) and the checkers that implement them: the cell
rule of `CAP/checker_sources/src/exact_classes.py` (`check_row`, lines 431–505: a cell’s
level is the largest high threshold whose slot image the cell meets, else the smallest
low threshold whose slot image contains the whole cell-times-row product, else `1`), the
mirror validation `check_mirror` (lines 228–252) and the orbit mode of
`exact_general.py`, and the slab exemption of `exact_restricted.py` (`SlabExemption`,
lines 588–685). The three files `exact_general.py`, `integer_sweep.py` and
`boolean_rule.py` are byte-identical to the copies this project retains under
`packing/resources/web/n17-kleddamag-466001-2026-09-27/…/global_src/` (SHA-256 prefixes
`89954c6c`, `3a2bfd88`, `c49d38ac`). The cell rule dominates `τ` because a high class is
detected by meeting and a low class is accepted only when the whole product lies in one
slot image, so a pose in the cell lies in that class; the priority order (high before
low before `1`) can only raise the level above `τ`. The lane found the lemma correct as
stated. It did not rerun any row, and the author’s own known-issues list (item 2) says
the lemma’s proof is spread over five files rather than written out once.

**Frame assignment (P040–P042, lines 127–135; premise `FRAME_ASSIGNMENT`).** The lane
verified every literal fact (`literal_checks.py`, 194 checks at 83 sites, no failure):
`ρ = 207107/500000` exceeds `tan(π/8)` because `ρ^2 + 2ρ − 1 > 0`; the marker hexagon
has half-width `493/1250` and is symmetric about `U/2`; the `FRAME` thresholds, bounds,
disjointness and `BONUS` equalities; `L9` is the `x`-mirror of `L17`; every clipped
diameter of the frame polygons is at most `11566501/25000000 < 1`, so each holds at most
one centre; and the counting arithmetic of P041–P042 (`t ≥ 2m`, `N ≥ 2`, `h = 5`, and
`17 + m/4 − t/8 < 137/8`). The inference from the counts to one `D4` image with the
half-marker occupied, a unique occupant of `L9` and a distinct occupant of `L17` is
correct.

**`KEY_W` elimination (P049, line 155; premise `KEY_W_ELIMINATION`).** The `KEY_W` slot
is `L9 × [30651/100000, 44941/100000]`, the wall slots have `x ≤ 53/100`, only the
identity lift of the angle meets `[0, π/2)`, and the gap to the lower exit is exactly
`1/200000` (P057, line 179). With the budget and the occupied half-marker the unique
`L9` parent lies in the gate-or-wall union.
Correct.

**Wall partition (P051–P053, lines 160–168; premise `WALL_PARTITION`).** For
`x_9 ≤ 53/100` the branches `y ≤ 129/50`, `129/50 < y ≤ 13/5`, `y > 13/5` are disjoint
and exhaustive; the 29 wall triggers of `WALL_TRIGGERS.json` were recomputed.
Correct.

**Loose identities and coarse capacity (P054–P066, lines 169–207; premise
`COARSE_LOOSE_CAPACITY`).** The clipped squared diameters of `S_3`, `S_15`, `S_17` are
exactly `1097067164761/4·10^12`, `799624844761/4·10^12`, `1059571044761/4·10^12`, all
below `1`; the regions are disjoint; `S_17 ⊂ L17`; each `S_k` lies in its coarse region;
the coarse region 17 has clipped squared diameter `1851391155161/4·10^12 < 1`. The
wall-strip lemma of `coarse-capacity-AP/PROOF_BRIDGE_V2.md` rests on the quartic
`P(u) = (1−w) + (1−2H)u + 4u^2 + (−1−2H)u^3 + (1+w)u^4`; the lane re-derived the
identity by random exact evaluation and proved positivity by Bernstein coefficients on
128 subintervals, with minima exactly `634043429/125829120000` and
`43535731167/8388608000000`. The grid positivity and the support cut
`−0.00989657… > −9897/10^6` of P079 (line 245) were recomputed.
Correct.

**`C7`/`C8` transfer (P047, line 149; premise `C7_C8_TRANSFER`) and the `C12` unions
(P078, line 242).** The reflected `C7` lies in `C8` with slack `3/125` and the two
targets are `8189/2500` apart; the `C12` union with the marker hexagon has squared
diameter `0.3952979… < 3953/10000`, and the other ten profiles `0.301984… ≤ 9437/31250`.
Correct.

**Case partition (P057–P058, lines 178–183; `[file:CASE_PARTITION]`).** The 15,000 atoms
of `check_case_partition.py` were classified by a decision function written here from
the text of P051 and P057; exactly one of the thirteen predicates holds for each atom,
and the assignment agrees with the author’s. The case list is exhaustive and disjoint.

### Step 3, admission (`PROOF.md` §7, lines 223–248; premise `ROOT_ADMISSION`)

The lane wrote its own admission (`admission_check.py`): the chart
`ξ_(i,k) = e_(i,k)·(c − (U−L)(1,1)/2 − p_i)` with `(u_i, v_i)` axes for labels 11 and 13
and Cartesian axes otherwise, `L` taken as its enclosure, every class polygon clipped to
the physical centre box, and every direction specification (slot, free, gate, above,
below, wall, gate 9, exit 9) mapped to the root arcs through the quarter-turn lifts.
All eleven roots admit all seventeen labels; the parent profiles of the eleven roots are
pairwise distinct; the smallest margin is exactly `0`, at label 1, where a closed root
arc end coincides with a closed gate end (sound, both sets being closed); the largest
clipped target diameter squared is `0.4635` for the wall roots and `0.4395` off the
wall. The wall lemma that `run_adm.py` uses (lines 17–18) was verified: for a side
direction in `[−45°, 45°]` the half-extent along `x` is `(cos|θ| + sin|θ|)/2`,
increasing in `|θ|`, so a square in `x ≥ 0` with centre `x < 53/100` has
`cos|θ| + sin|θ| < 53/50`, and `(1+2t−t^2)/(1+t^2) > 53/50` at `t = 31/1000` gives
`|θ| < 2 atan(31/1000)`. See finding 1.

### Step 4, the thirteen trees (`PROOF.md` §7, lines 250–279; premises `LOCAL_CHECKER_SOUNDNESS`, `LOCAL_CERTIFICATE_IMPORT`, `SELECTOR_LOGIC`)

The eleven root certificates and the two window trees are checked by the rules of
`WX/SPEC_v3.0.md`. §3 below records the lane’s reading of those rules.
The lane replayed `JQ` whole with a checker of its own (`jq_leaf_check.py`): one node,
seventeen labels, `S_floor = S_ref = R`, a window with centres (schema `wx-cert-3`),
26,781 polynomial forms, three `opt` declarations and 33 `ind` declarations with 70
indicator variables, one step on the form `0` with 48,209 terms and a centre at every
base variable. The root conditions hold (parent null, empty assumptions, side interval
`[R, R]`, the root box equal to the window box, and `sin Ab^± ≥ ±α_i` with positive
cosines for every label, with the centres); the start store is not empty; every `opt`
declaration has its seven other options excluded and every `ind` declaration has its
unlisted options excluded by the test of SPEC 4.7; no term violates (T1) to (T4); the
remainder has 42,417 monomials of degree at most 5; the centred rule gives
`ℓ ≈ 0.0069450 ≥ value = 3455339/552809052 ≈ 0.0062505 > 0`, and `ℓ` equals the
`zero_step_L` of the author’s stored report `WX/acceptance/JQ_v1_jQTwn0_C1.json` to the
last of its roughly 2,500 digits.
So `F(root)` is empty for `JQ`: no feasible configuration at side `R` has its positions
in the root box and its directions in the root arcs, and by P086 (line 266) none at any
side `S ≤ R` either.
The other twelve certificates were not replayed (§0).

The statement each tree proves is the `(ANN)` of SPEC §0 for its window, and for a root
closed as infeasible the proof of the SPEC’s theorem gives more: `F(root) = ∅` for the
root region (box and arcs), which is what the admission needs, since the root arcs are
larger than the window arcs (for the four free-direction labels 3, 4, 15, 17 the root
arcs have half-angle `2 atan(4147/10000) ≈ 0.78634 > π/4`, so every direction has a
representative in them, while the window radius `7/10` would not).
The proof text’s P086 (line 266) states the enlargement from side `L` to side `R`
correctly: positions and directions are fixed in the corner-at-origin chart, pair
separations do not change, and the right and top walls only weaken.

### Step 5, rigidity (`PROOF.md` §8, lines 281–346; premises `G20S_PHYSICAL`, `WALL_CONTRADICTION`)

The chain is `JG` terminal → `G20S` window → tube `T1` → `HW` window → tube `T2` → the
sixteen-square entry → seventeen finite rounds → normalized stopped contraction → zero
core → square 8 at `(L−1/2, L−1/2)` with axes `(1,0)`, `(0,1)` → two wall contacts →
contradiction with the strict inset of the normalization.
The hand-overs are verified in §4. The derivation of the parallel-pair rows (P098–P107,
lines 301–331) was re-derived by hand: with `n_i = R(−ε)n_m`, `n_j = R(ε)n_m` and
`Δ = X_m n_m + τ_m Jn_m`, each of the two retained alternatives gives
`cos(ε)X_m ∓ sin(ε)τ_m ≥ (1 + cos 2e + sin 2e)/2 = cos^2 e + sin e cos e`, which is
P100; P102–P103 follow from `cos e ≥ 1 − e^2/2`, `sin e ≥ e − e^3/6`, `tan e ≤ e + e^3`
on `[0, 1/10]`; P104 follows by applying the first-order Taylor remainder
`‖R(μ)n − n − μJn‖ ≤ μ^2/2` to `d_w` and the crude `‖R(μ)n − n‖ ≤ |μ|` to `δ_h`; the
constant `E` of P105 collects exactly the resulting terms; and P106–P107 are the two
signed rows with the McCormick products.
A random test of 28,326 instances found no violation (`parallel_row_check.py`). The
normalization argument of P110 is logically valid as the record
`continuation/THEOREM.md` (lines 77–121) states it: with `R = max|h_j| > 0` the
normalized core attains `1`, the 52 rows are necessary after normalization for every
`0 < R ≤ 1/5000`, the five rounds of bounds give
`max|x_j| ≤ 159201934153319/200000000000000 < 1`, and so `R = 0`. The seventeen rounds,
the 52-row gate and the continuation were not replayed here.
The final contradiction is correct: with zero core deviation, label 8 (the top-right
square, file centre `(R−1/2, R−1/2)`) sits at `(L−1/2, L−1/2)` with axis-parallel sides
in the frame `[0,L]^2`, so it touches the walls `x = L` and `y = L`, while P021 put the
normalized packing strictly inside them.

## 3. The Checkers’ Acceptance Rules Against What the Proof Needs

**`SPEC_v3.0.md`.** The lane read every lemma with its proof and tested each numerically
(`spec_lemmas_numeric.py`, no failure): the separating-axis lemma of 4.5 (every pair of
disjoint unit squares satisfies one of its eight options), the corner polynomial
identity of 4.5, the dictionary identity `be − al = si·Y/(1+co)` of 4.6, Lemma P in all
three forms (P+, P−, Pk) within their preconditions, the `Ps` concavity bound, the
`h_lo` bound of 4.7 on an arc inside one quadrant, the arc facts of 4.2 (`slo`, `shi`,
`clo`, `chi`, `chord`, `tan`), the wall support facts of 4.8, the two analytic
inequalities of §8 (`asin x ≥ x`, `sin x ≥ x − x^3/6`), the raw remainder rule of §5 as
a lower bound, and the chord inequality `sin x + sin y − sin(x+y) ≥ 0`. The lane found
no false statement. The points that carry the soundness are: the store bounds of §3 are
over-approximations (`C_i ≥ min` of the endpoint cosines by concavity, the raw rule
bounds `x^2` by `[−a^2, a^2]` rather than `[0, a^2]`, which is weaker and therefore
sound); the exclusion test of 4.7 is strict and uses `h_lo = 1/2` whenever the quadrant
condition fails, which is always valid since `|cos| + |sin| ≥ 1`; the `ind` mechanism of
4.10 needs only that unlisted options hold nowhere on `F(N)`, which the exclusion gives,
and the guard rule (T3) makes every corner polynomial of a listed option enter only
multiplied by its own indicator, so the term lemma holds at the lifted point; the
centred rule is the raw rule after an exact change of variables; store entries are
accepted only from certified values of the same round or by loosening, so nothing proves
itself; the root test of §8 uses `asin x ≥ x` in the direction that enlarges the root
arc, and the terminal test uses `sin x ≥ x − x^3/6` in the direction that shrinks it.
SPEC §11 (lines 823–862) correctly argues that `(ANN)` for `S_floor ≤ S ≤ S_ref` implies
it for every `S ≤ S_ref`, because feasibility only weakens as `S` grows and no window,
tube or reference datum depends on `S`.

**`wxcheck_v30.py`.** The lane read the code paths that decide acceptance against the
text: `StoreEnv.h_lo` and `excluded` (lines 1664–1700) implement 4.7 literally,
including the conjugation of the relative endpoints for the reversed ordered pair;
`declare_ind` (1842–1860) tests exactly the unlisted options; `check_term_rules`
(1880–1898) enforces (T1)–(T3) with the guard keyed to the option’s own index;
`lower_bound` and `lower_bound_centred` (2061–2229) combine like monomials and multiply
intervals factor by factor, including repeated variables; `accept_store` (2333–2409)
accepts each entry only by loosening or by a certified value of the round;
`terminal_failure`, `root_failure` and `child_failure` (2441–2710) implement §§6–8 with
the window and tube centres.
The lane’s own `JQ` checker, written from the text alone, computes the same `ℓ` as this
program, which is strong evidence that the two readings of §§3–5 agree on an instance
that exercises the centred rule, the indicators, the guard rule, the squares, the
sign-free multipliers and the exclusion test with relative arcs.

**The capture checkers.** The acceptance rule of a class certificate (`exact_classes.py`
`check_row`, `validate_classes` lines 266–323; `exact_restricted.py` `validate_fixed`
lines 195–267 and the exemptions) matches `CLASS_FORMAT.md` and `RESTRICTED_CHECKER.md`
and the class-row lemma’s hypotheses: strict symmetry of mirrored classes, the lift
rules of the angle gates, the slab exemption only where the restriction says, and the
final strict integer test `M·q_β < p_β·Γ`. The lane did not run them.

## 4. Hand-overs Between the Steps

`handover_check.py` (no failure): the terminal of `JG_exact_v2.json` has no centre map
and equals the `G20S` window exactly (core `1/5`, radius `1/10`,
`ξ_(2,1) ∈ [−39/125, 0]`, `ξ_(13,2) ∈ [−1/5, 28/125]`), which is P092; the `G20S` tube
`T1` cut by `ξ_(2,1) ≤ 0` lies in the `HW` window, and without the cut it does not
(`ξ_(2,1)` reaches `1/100`), which is P094; the `HW` tube `T2` (positions `1/250`,
angles `1/500`, `ξ_(2,1) ∈ [−8/25, 1/250]`, `ξ_(11,2) ∈ [−1/5, 1/20]`,
`ξ_(13,2) ∈ [−1/5, 3/40]`) cut by `ξ_(2,1) ≤ 0` lies in the sixteen-square entry of P095
(core `1/200`, angles `1/400`, `a ∈ [0, 8/25]`, `b ∈ [−1/20, 1/5]`, `z ∈ [−1/5, 3/40]`),
and without the cut it does not.
The retained cut `ξ_(2,1) ≤ 0` is justified by P087: on a right wall end
`ξ ≤ L − R + ε < 0` for the normalized packing, since `R − L − ε > 0` (§1). The stored
acceptance reports of `G20S` and `HW` record sixteen labels, `S_floor = 4` and schema
`wx-cert-2`, and P094’s `S ≥ 4` from area satisfies their floor.
The chart `c − (U−L)(1,1)/2` of the admission and the corner-at-origin frame of the
trees are the same frame, and the side enlargement `L → R` of P086 needs no translation.

## 5. The Fifteen Premises

| Premise | Status here | Basis |
| --- | --- | --- |
| `ALGEBRAIC_ENDPOINT` | proved | own Krawczyk isolation and ninety-place enclosure (§1) |
| `UPPER` | proved | own interval and ideal-membership check of the construction at `L` (§2, step 1) |
| `ENDPOINT` | proved | read; a translation preserves everything claimed (§2) |
| `CHARGE_SEMANTICS` | correct as stated; rows not rerun | the class-row lemma and the checkers read; byte-identity of three checker files with this project’s copies (§2) |
| `FRAME_ASSIGNMENT` | proved | every literal fact and the counting recomputed (§2) |
| `C7_C8_TRANSFER` | proved | the geometry recomputed (§2) |
| `WALL_PARTITION` | proved | disjoint and exhaustive by inspection; triggers recomputed (§2) |
| `ROOT_ADMISSION` | proved | own admission of all eleven roots, distinct profiles, the wall lemma verified (§2, step 3; finding 1) |
| `SELECTOR_LOGIC` | not independently proved | the 84 clauses were read in `SELECTED_ORIGINAL_MAP.json` and `THEOREM_MANIFEST.json`; the lane’s admission used, for each root and label, the class region the selection names, and did not check that each listed alternative would also suffice |
| `LOCAL_CHECKER_SOUNDNESS` | proved as specified | every lemma of SPEC 3.0 read, proved and tested; the checker’s acceptance paths read (§3) |
| `LOCAL_CERTIFICATE_IMPORT` | one of thirteen reproduced | `JQ` replayed to the last digit; the other twelve not replayed (§2, step 4) |
| `G20S_PHYSICAL` | argument correct; computation not rerun | the row derivation re-derived and tested, the normalization argument read in its record (§2, step 5; finding 2) |
| `WALL_CONTRADICTION` | proved | read; label 8 identified in the reference file (§2, step 5) |
| `KEY_W_ELIMINATION` | proved | the slot, lifts and gaps recomputed (§2) |
| `COARSE_LOOSE_CAPACITY` | proved | diameters, inclusions and the quartic recomputed (§2) |

No premise was found false.

## 6. Findings

Grades: blocking, major, minor, note.
File and line are in the source at the pin.

1. **Minor. The wall lemma of the root admission is not in the proof text.** The step
   that a unit square in `x ≥ 0` whose centre has `x < 53/100` has its side direction
   within `2 atan(31/1000)` of the wall direction is used by the admission of the wall
   roots and is stated only as a comment in `PKT/scripts/run_adm.py`, lines 17–18;
   `PROOF.md` P079–P080 (lines 244–248) do not carry it.
   The author’s `KNOWN_ISSUES.md` §1 item 1 lists it.
   The lane verified the argument (§2, step 3): it is correct, including at the
   quarter-turn representatives, because the half-extent `(cos|θ| + sin|θ|)/2` is
   invariant under quarter turns.
   Suggested repair: state the lemma and its proof in P079 or in a record bound to
   `ROOT_ADMISSION`.

2. **Minor. P110 compresses the normalization argument.** `PROOF.md` line 340 (P110) says
   that a nonzero core “could be rescaled to normalized maximum 1, contradicting that
   strict contraction”.
   The contradiction needs the 52 normalized rows to be necessary for every radius
   `0 < R ≤ 1/5000`, not only at the entry radius, because the normalized packing is
   scaled by its own unknown `R`. The record states this
   (`AUTH/g20s-terminal-audit/full-stopped-propagation/continuation/THEOREM.md`, lines
   87–89: “necessary throughout the full padded slider domain for every
   `0 < R ≤ 1/5000`”), and the structure of the rows supports it (the error constants of
   P105 are at least quadratic in the deviation bounds, so after division by `R` they
   are increasing in `R`); the proof text does not say it.
   Suggested repair: one sentence in P110 naming the scale-uniform necessity and the
   record that proves it.

3. **Minor. The admission margins are not recorded, and one of them is zero.** The stored
   admission output is one line (`PKT/public_runs/admission/stdout.txt`, “PASS 11 exact
   root admissions, 17 labels each”; `KNOWN_ISSUES.md` §1 item 8). The lane’s own
   admission finds the smallest margin exactly `0` at label 1 in every root, where a
   closed root-arc end equals a closed gate end.
   This is sound because the class gates and the root arcs are both closed
   (`SPEC_v3.0.md` §2, line 87: the arc is a closed set of directions), but the fact and
   its justification should be visible.
   Suggested repair: print every margin with its label and kind, and state in P073–P080
   that containment is of closed sets in closed sets, so a zero margin is allowed.

4. **Note. The quarter-turn gap of P057 is given in an unnamed chart.** `PROOF.md` line
   179 gives the upper quarter-turn gap as `974949/14197000000`. That is the difference
   `−5803/14197 − (−408817/1000000)` in the chart lifted by `−π/2`; in the chart of the
   gate, where the exit end is `591183/1408817` and the lifted slot end is `4197/10000`,
   the same gap is `974949/14088170000`. Both are positive and the conclusion stands;
   the text should name the chart it measures in.

5. **Note. SPEC §11 names a terminal instance that the proof does not use.**
   `WX/SPEC_v3.0.md` lines 844–853 describe the terminal theorem as the instance
   `terminal/instances/box-relaxed/` with core within `1/100`, angles within `1/200`,
   `a ∈ [0, 1/4]`, `b ∈ [−1/20, 3/20]`, `z ∈ [−1/8, 3/40]`. The proof text uses the
   sixteen-square entry of P095 (core `1/200`, angles `1/400`, `a ∈ [0, 8/25]`,
   `b ∈ [−1/20, 1/5]`, `z ∈ [−1/5, 3/40]`), whose slider box is wider in `a` and `b`,
   and the padded domain of the continuation record.
   The SPEC’s section is advisory and nothing in the checker depends on it, but a reader
   following it looks for the wrong instance.

6. **Note. The evidence boundary.** Twelve of the thirteen trees and all 98 capture rows
   are accepted only by the author’s checkers, and the two tree checkers were written by
   sessions of one AI system from one specification (`KNOWN_ISSUES.md` §1 items 4–5).
   This review adds the soundness of the specification as read and tested, and one exact
   reproduction. It does not add a replay of the rest; an outside replay of at least the
   two window trees `G20S` and `HW` and of one capture row with a checker not derived
   from the author’s would close most of the remaining distance.

7. **Note. Two numbers of P090 and the tree sizes** (`PROOF.md` line 278: 416 nodes and
   93 option splits of `JPA_v5`; `KNOWN_ISSUES.md` §1 item 7: 113 or 110 nodes of `JG`)
   could not be checked here, since those trees were not read.
   They do not enter the argument.

## 7. Questions for the Author

1. Is there a written argument, separate from `run_adm.py`, that the eleven root
   regions’ direction specifications (slot, gate, exit, wall) are the images of the
   class gates under the quarter-turn lifts the admission uses, for the free-direction
   labels 3, 4, 15 and 17 in particular?
   The lane re-derived it, but the edition carries only the computation.

2. For the 52-row gate of `G20S_PHYSICAL`: which record proves that every one of the 52
   normalized rows is necessary for every `0 < R ≤ 1/5000` (finding 2), and does that
   proof cover the 152 separating alternatives individually, so that each pair’s two
   retained alternatives are the only ones possible on the padded entry?

3. The `JQ` certificate lists, for the 33 undecided pairs, exactly the options the
   exclusion test leaves (none of the listed options is itself excluded).
   Was the list produced from the same exclusion test the checker runs, or from a
   floating-point audit?
   The answer does not affect soundness, since the checker tests the precondition, but
   it affects what a reader may infer from the lists.

4. Would the author state in the proof text, at P086, that the enlargement of the
   container from `[0,L]^2` to `[0,R]^2` is applied to the eleven root trees only, and
   that the two window trees are applied at `S = L` with `S_floor = 4`? The text has
   both facts, but in different paragraphs (P086 and P094), and a reader can lose which
   cap applies where.

## 8. Checks Made Here

All programs are the lane’s own, under `scratchpad/math-overbeck/` of the review
session, run with the project interpreter (`python3 -I`); none imports or executes
anything from the source.
Outputs are abbreviated.

| Program | What it does | Result |
| --- | --- | --- |
| `root_isolation.py` | exact Krawczyk on the statement box, central-difference check of the hand-derived Jacobian, five refinements with outward rounding | `K(X) ⊂ int X`; `‖I − YJ‖ ≤ 4.985e-11`; `L = 4.675530093604550951634111270483146648767…`; `L < R < C < U`; `R − L − ε > 0`; 20-place bound true |
| `root_box.py` | module: the enclosure reused by the other checks | width of `L` about `1.2e-60` |
| `seed_packing_check.py` | the rational seed at side `R` | 68 walls `≥ 0`, minimum exactly `ε`, 14 flush; 136 pairs separated, 0 touching |
| `upper_at_L_check.py` | the construction of `UPPER_FORMULAS.md` at the algebraic root; intervals for strict facts, Gröbner reduction modulo `(F, G)` for equalities | first run, by corner and by first holding option: 272 clearances, 243 strict, 29 zero; 136 pairs, 114 strict, 22 tangent; rerun in P014’s convention after §10: 53 strict and 15 identity walls, 115 strict and 21 touching pairs; `FAILURES: 0` both times |
| `literal_checks.py` | 194 literal checks of §§3–6 and the case partition (listed in §2) | `FAILURES: 0` |
| `admission_check.py` | own admission of the eleven roots and profile distinctness | every root admitted; profiles distinct; smallest margin `0` at label 1 |
| `handover_check.py` | the three hand-overs of §8 and the stored reports of `G20S`, `HW` | `FAILURES: 0`; both cuts shown necessary |
| `spec_lemmas_numeric.py` | random tests of every lemma of `SPEC_v3.0.md` (first run exposed a test of Lemma Pk outside its precondition; corrected) | `FAILURES: 0` |
| `jq_leaf_check.py` | a complete checker for the one-node certificate `JQ` (§2, step 4) | all conditions pass; `ℓ ≈ 0.0069450 ≥ 0.0062505`; `ℓ` equals the stored `zero_step_L` exactly; 161 s |
| `parallel_row_check.py` | random test of P100–P106 | 28,326 instances, 0 failures |

The dyadic coefficients of the `JQ` forms, the decimal centres and the exact rational
arithmetic make the `JQ` replay a strict reproduction: no rounding enters anywhere.

## 9. Disclosure

The lane printed the first fourteen lines of the two earlier reviews to copy their form
before writing its own findings.
The earlier reviews have no front matter, so those lines contain, for the second review,
its verdict sentence (an accepting verdict that names a normalized 52-row gate, a
Krawczyk proof of the root box, a Gröbner-basis proof of the base-gap identities, an
option audit of 152 separating alternatives and an independent row builder).
The retained `README.md` of the candidate in this project, which the lane was allowed to
read, lists the programs of that review by name.
The lane therefore knew, before writing, that the second review was accepting and
roughly which computations it ran; it did not read either review’s body, findings or
questions until §10. The lane cannot exclude that its choice of a Krawczyk operator for
the root and of a Gröbner reduction for the exact equalities of the upper bound was
influenced by that sentence; both are the standard tools for those tasks, every other
check here (the literal facts, the admission, the hand-overs, the SPEC lemmas, the `JQ`
replay, the row derivation) was chosen from the source alone, and no result depends on
the choice of tool.

## 10. Comparison with the Earlier Reviews and `T-153`

This section was written after §§0–9, from the
[review of 12 October](review-2026-10-12-kleddamag-n17-candidate.md), the
[second review of 13 October](review-2026-10-13-overbeck-n17-candidate-second.md) with
its status addendum, the entry `T-153` in `packing/frontier/results.yaml` and the case
record `packing/frontier/n-017.md`. Nothing in §§0–9 was changed because of them; the
one check rerun afterwards is said so below.

**What this review confirms.** All three reviews accept with no mathematical defect
found, and all three draw the trust boundary at the same place: the authentic execution
of the capture rows and the tree runs, and checkers written by sessions of one AI
system. The root and `R − L = 4.8366·10^-17` agree to every digit the three print; the
first review argued the isolation from `ENDPOINT_AUDIT.md`, the second ran Newton and a
Krawczyk test about its Newton point (its addendum notes a sliver of the statement’s
rectangle so left out), and this lane’s Krawczyk step is on the statement’s rectangle
itself, so it closes that sliver as lane K3’s isolation did.
The wall lemma at `t = 31/1000` is verified by all three and its absence from the proof
text is raised by all three (the first review’s defect table and question 4, the
second’s SR-8, finding 1 here).
The three hand-overs of §8 are the same numbers in all three.
The coarse-capacity quartic: the first review’s Bernstein minima are exactly this
lane’s, and the second review’s exact minima `0.005043` and `0.005193` lie above them,
as they must. The least position margin of the admission, `R − L − ε = 4.32·10^-17` at
square 2’s right wall, is what both earlier reviews report; this lane sees the same
position margin and reports in addition the arc margin, which is exactly zero (finding
3). The second review re-derived the normalized 52-row gate with code of its own, which
the first review had left unread; this lane did not re-derive the 52 rows, so on that
step the second review’s work stands, and finding 2 here only asks the proof text to say
what that review and the continuation record establish.
The second review’s line-by-line check of the parallel-pair derivation (its gate
section, third item) and this lane’s hand derivation and random test agree.
Both earlier reviews name the two rigidity routes with different constants (`0.859` and
`0.796`; the first review’s second objection, the second’s SR-4); this lane noted it
only through `KNOWN_ISSUES.md` item 7 and confirms that the proof text uses the `0.796`
route.

**What this review contradicts.** Nothing in the mathematics.
Two numbers differ by convention.
§2 counts the upper construction’s pairs as “114 strict, 22 with a tangency” by the
first holding option found, while P014 and the second review count 115 strict and 21
identity pairs by the existence of a strictly separating axis; the difference is one
pair whose first holding option has a corner on the extension of a face line while
another axis separates the pair strictly.
After reading P014 the lane reran its count in P014’s convention, counting a pair as
strict when some axis separates it strictly and a wall contact per square and wall: 53
strict and 15 identity walls, 115 strict and 21 touching pairs, which are P014’s counts
exactly; the pair that moves is (2,4) in construction labels.
The smallest admission margin, `0` here against `4.32·10^-17` there, measures arcs here
and positions there.

**What the earlier reviews found that this lane missed.** From the first review: the
`LABELS.tsv` bindings of `file:SELECTED_CLAUSES` into a sibling folder and of
`file:C12_PROFILE_CAPACITY` into an earlier edition folder; the “high-first” sentence of
`F1_PROOF.md` line 5 (this lane read the file and let the author’s known-issues entry
stand for it). From the second review: SR-1 (no independent builder of the normalized
model carried in the edition), SR-2 (the full-gate review’s scripts not carried and its
byte count), SR-3 (the B6 prefix and the root-scale stop theorem unlabelled; the
division text written for an earlier slider box), SR-6 (surpluses of half a unit to 23
units on the capture budgets, and a public check that does not recompute them), SR-7
(`recompute_slice.py` and the Node checker hash) and SR-9 (`G20S_PHYSICAL` bundling the
two window trees). This lane read none of the files those findings rest on: the three
gate texts, `new_capture_check.py`, `recompute_slice.py` and the full-gate review
folder. The second review also recomputed all 98 capture budgets from their features and
re-decided the 9,000 rows of `FRAME_0917` from their recorded minima, which this lane
did not do.

**What this lane found that the earlier reviews did not.** Finding 4: the proof text’s
quarter-turn gap `974949/14197000000` is not the canonical-chart number
`974949/14088170000` that the first review computed in its §9; that review did not
remark the difference.
Finding 5, the stale terminal instance in SPEC §11. Finding 3’s zero arc margin.
The exact proof, by ideal membership modulo `(F, G)`, of every contact of the upper
construction, which the second review’s interval corroboration states it does not prove.
The replay of `JQ` with a checker written from the specification alone, reproducing the
stored `zero_step_L` to the last digit: the record’s replays of three trees (`T-153`’s
composition note) used the producer’s checkers, and the entry says an independent
implementation of the tree checker “would be an attribute beside the rung”; this lane’s
checker is that for a one-node tree only, since it implements no splits, no cuts, no
stored relative arcs and no terminal test.
The literal geometry of all 98 class files, the identity of the escape union across the
ten `C` files, and the case partition re-decided with a decision function of the lane’s
own, where the first review relied on the public check `partition`. For the first
review’s question 6, where the literal `C7` and `C8` polygons are: the lane found them
at
`local-research/claude-20261002/rerun-clean-20261011/design_classes/classes/C_L07.json`
and `C_L08.json` and used them in its admission; whether a packet label binds them by
hash it did not check.

**The record.** `T-153` stands at `V0/C1`, `S5`, with the two earlier reviews on file as
adversarial AI reviews, both accepting, and the complete capture recomputation and the
ten unreplayed trees priced as the unfinished parts of `C3`. This review is a third
adversarial AI read by the model family of the first, in a separately prompted lane with
no shared context, at a different tier and reasoning setting; it moves nothing, and what
it adds to the evidence is the exact contact proofs of the upper half, which `T-065`
already holds at `V3/C3`, and one tree decided by an independent implementation.
The entry now also names `T-154`, Fitzharding’s separate Lean proof of the same
equality; it is a different route and nothing here bears on it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
