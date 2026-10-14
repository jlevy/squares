# Mathematical Review: Kleddamag’s Candidate Proof That `s(17) = L`

Reviewed 2026-10-12 from the public source
[`Kleddamag/the-seventeenth-square-candidate`](https://github.com/Kleddamag/the-seventeenth-square-candidate)
at pin `653b9589d` (version 1, candidate, 2026-10-12), by an AI agent: lane K2 of the
#557 intake, the mathematical-review lane, prompted separately from lane K1 (retention
and digests) and lane K3 (replays), sharing no context with either and blind to both.
The model is `claude-fable-5-1` at the tbd-strong tier, reasoning setting xhigh.
Lane K1’s clone did not exist when this lane started, so every file was fetched by the
GitHub contents API into this lane’s own scratch directory; nothing upstream was
modified, nothing was posted, and no upstream bytes are proposed for retention.
No heavy computation was run; §9 lists the exact one-line checks made here.

This review registers nothing and moves no bound.
It is the record’s first reading of the argument, written to the standard of the n = 11
optimality reviews (`T-060`, `T-112`): an adversarial read of the structure, aimed at
finding a gap in each step or showing there is none in what was read.

**In one line:** the argument is a five-step reductio in the shape of Ahmed’s n = 11
proof, built from this project’s charge and local-isolation recipes; every hand step I
could isolate re-derives (the class-row lemma’s four links, the frame counting, the
KEY_W elimination, the loose-role identities, the coarse-capacity quartic, the label-12
marker cover, the admission geometry, the three tube hand-overs, the endpoint
contradiction), and no mathematical defect was found in what was read; what the text
cannot discharge is what the source itself names, authenticity of 1,152 stored slice
executions and the fidelity of two large checkers written by one AI system, plus one
step of §8 (the validity of the normalized 52-row gate for every core radius) that no
final-round reader and not this review has read; so the claim enters the register at
`V0/C1`, `S5`, and reaches `V3/C3` only after the replays of §5.

## 0. What Was Read, Skimmed and Not Read

| Depth | Files |
| --- | --- |
| Read in full | `STATEMENT.md`, `STATEMENT_STATUS.md`, `README.md`, `OVERVIEW.md`, `PREMISES.md`, `KNOWN_ISSUES.md`, `AUDIT.md`, `KNOWN_LIMITS.md` (root), `READING_ORDER.md`, `CHANGELOG.md`, `CITATION.cff`, `CREDITS.md`; `PROOF.md` (all 116 paragraphs); `PKT/revision-v7/CLASS_ROW_LEMMA.md`, `NOTATION.md`, `GLOSSARY.md`, `ANALYTIC_ENVELOPES.md`, `FINITE_PARALLEL_DERIVATION.md`; the 15 premise rows of `PKT/OBLIGATIONS.json` and the top of `PKT/DEPENDENCY_GRAPH.json`; `PKT/ENDPOINT_AUDIT.md`, `INDEX_SAFETY.md`, `PUBLIC_ENTRYPOINTS.md`, `EQUIVALENCE.md`, `REVISION_SCOPE.json`, `RELEASE_CHECK_ASSESSMENT.json`, `CLASS_ROW_SOURCES_PUBLIC.json`, `FRAME_DISJOINTNESS_PUBLIC.json`, `EDITION.json`; the files of record `F1_PROOF.md`, `FRAME_L9.md`, `PROOF_BRIDGE_V2.md`, `coarse-capacity-R/PROOF.md`, `case-repair-S/PROOF.md`, `c7-c8-inherited-producer/PROOF.md`, `endpoint-normalization-producer/THEOREM.md`, `ENDPOINT_CASE_G_LEMMA.md`, `sixteen-square-corollary/producer/THEOREM.md` and its `independent-review/REVIEW.md`, `full-stopped-propagation/continuation/THEOREM.md`, `finite-entry-stop-pruning/entry-producer/PROOF.md`, `finite-stopped-contraction/independent-review/REVIEW.md`, `records/THEOREM_G20S.md`; `scripts/run_adm.py` and `scripts/adm.py` (every line); `SPEC_v3.0.md` sections 0–8 and 11 and `SPEC_v3.0_NOTES.md`; `EXPECT_G20S.json`, `EXPECT_HW.json`, `FROZEN_30.json`; the root file `JG_exact_v2.json` (header, window, arcs, terminal); the literal class files `L_3`, `L_4`, `KEY_W`, `C_12`, `FRAME_0917`, `FRAME_MARKER`, `E07A`, `CLASS_PS_L01_T09`, `SL11_T020`, `PW_11`, `Q_13`; `upper-packing-certificate.json`; `UPPER_FORMULAS.md`; the reader reports `REPORT_CHARGE_CORE.md`, `REPORT_ADMISSION.md`, `REPORT_ERRATA_2.md`, `REPORT_TERMINAL_2.md` |
| Skimmed | `CHECK.md` (levels, limits, the recomputation recipe), `THIRD_PARTY.md`, `EXACT_ENDPOINT_AND_CASES.json` (endpoint block, the 13 predicates, the KEY_W block), `runbook_public.json` (the 31 check names), `SMALL_CHECKS_PUBLIC.json` (the one-unit surpluses), `REVIEWS_PUBLIC.json`, `WINDOW_RECORDS.json`, `LABELS.tsv` (the rows cited below), `exact_classes.py` lines 160–510, `boolean_rule.py`, `integer_sweep.py`, `REPORT_COMPOSITION.md` (verdict, blocks K1–K4, the coverage table), the verdict lines of the other seventeen reader reports |
| Not read | `SPEC_v3.0.md` sections 9–10 and 12; `wxcheck_v30.py`, `wxcheck2_v30.js`, `h_report30.py`; `verify_classes_wb.js`; `exact_restricted.py`, `exact_general.py`; any tree certificate or acceptance JSON; any capture certificate, slice record, receipt or merge record; the 84 selected class files other than `CLASS_PS_L01_T09`; the other 10 root files; `full_gate_analytic_review.md`, `analytic_envelope_text.md`, `normalized_division_text.md`; the eleven region records and nine tree reviews; `check.py`, `replay_round2.py`, `fetch_large.py`, `recompute_slice.py`; the large files |

“Verified here” below means re-derived by hand from the literal files or recomputed in
exact rational arithmetic in this lane (§9). “Checked by a reader” means a reading copy
in the edition reports it; “computed by a public check” means one of the 31 checks that
lane K3 runs decides it.

## 1. The Statement

**L is Bidwell’s side.** From the statement’s own box midpoint `(t_0, b_0)` and the two
polynomials `F`, `G`, a 60-digit refinement gives
`L = 4.675530093604550951634111270483146648767…`, which is a root of the catalogue’s
degree-18 polynomial that the record holds in `n-017.md` (residual `2 × 10^-44` at 60
digits, against `2 × 10^-10` one unit of `10^-20` away), with tilt angles
`2 atan(t_*) = 39.80495897976780°` and `2 atan(b_*) = 36.62378638344659°`, the record’s
`tilt_angles_deg` to every printed digit.
The record’s verified ceiling `4.6755300936045509516342148538535054` lies `1.0 × 10^-22`
above L, and `R − L = 4.8366 × 10^-17` as `P011` prints.
So the statement’s L, the record’s certified endpoint (`E-n017-certified-endpoint`) and
the catalogue polynomial’s root (`E-n017-catalogue-polynomial-identity`) are one number.

**The class.** `STATEMENT.md` lines 1–2 and `PROOF.md` `P002` quantify over seventeen
closed unit squares contained in the closed square `[0,S]^2`, independently rotated,
with pairwise disjoint interiors, tangencies and zero clearances allowed.
`SPEC_v3.0.md` §0 states feasibility the same way (every corner in `[0,S]^2`, disjoint
interiors), and the class files quantify over “every family of closed unit squares with
pairwise disjoint interiors”.
This is the record’s class (`n-017.md`: “unrestricted independent rotations with
disjoint interiors; boundary contact allowed”), and the lower-bound direction is the one
claimed: existence at side `S` implies `L ≤ S`, with existence at `L` making `L` the
minimum, not merely the infimum.
Uniqueness is not claimed and the text never uses it.

**Root isolation.** `ENDPOINT_AUDIT.md` states the argument: with `B` the
radius-`10^-12` box, `m` its midpoint, `A = DF(m)^-1`, `q` an interval bound on
`‖I − A·DF‖_∞` over `B`, `η = ‖A F(m)‖_∞`, the checks `q < 1`, `η + q·10^-12 < 10^-12`,
`η/(1−q) < 10^-58` show that `x ↦ x − A F(x)` maps the closed box into itself and
contracts, so it has one fixed point, which is the unique zero of `F` in `B` because `A`
is invertible.
That is the Newton–Kantorovich argument as it should be, and it needs only
that `DF` is Lipschitz on the convex box, which it is.
The side map `f(t) = (6+4t)/(1+2t−t²)` is monotone on the box (`f' < 0`), so its
enclosure is exact.
Uniqueness is claimed only inside the box; nothing in the proof needs
more.
The wide (`10^-50`) and tight (`10^-58`) enclosures both prove `L < R < C < U`; the
admission margins of §3.2 need only `R − L > 0` with room, which both give.

Verdict on §1: correct as stated.

## 2. The Five Steps

For each step: its hypotheses, which of the 15 premises and which of the 195 other
obligations it uses, what is proved in text and what is certified by computation, with
whose code, and where the trust boundary lies.
The 210 obligations are 15 mathematical premises, 50 base capture rows (two of them,
`C_7` and `C_8`, derived with no run of their own), 1 slab capture, 49 selected strict
budgets, 84 selected branch implications and 11 whole local roots.

### Step 1, upper bound (`PROOF.md` §1, `P006`–`P015`)

Premises `ALGEBRAIC_ENDPOINT`, `UPPER`. Text: the root gate, the construction formulas,
the 68 wall and 136 pair conditions reduced to `F = G = 0` identities and strict
interval bounds. Computation: the producers’ `endpoint-feasibility/check_endpoint.py`
(SymPy 1.14.0, public check `endpoint_upper`), their `check_endpoint_enclosure.py`
(standard-library `Fraction`, public check `endpoint_enclosure`, adapted from the
former, not independent), an independent reader’s program
`independent/endpoint_enclosure/` (39 checks, one mutated-coefficient control), and the
retained alternative construction `H256`, which is this project’s own
`packing/devtools/check_n17_endpoint_feasibility.py` and `exp-238` certificate byte for
byte (`THIRD_PARTY.md`). Trust boundary: SymPy for one check; everything else is
rational arithmetic.
This half is already decided in our record independently of the source
(`E-n017-certified-endpoint`, replayed here), so for the record’s purposes Step 1 needs
no replay of theirs.
Verdict: established.

### Step 2, capture (`PROOF.md` §2–§6, `P016`–`P071`)

Premises `ENDPOINT`, `CHARGE_SEMANTICS`, `FRAME_ASSIGNMENT`, `C7_C8_TRANSFER`,
`WALL_PARTITION`, `KEY_W_ELIMINATION`, `COARSE_LOOSE_CAPACITY`, `SELECTOR_LOGIC`; the 98
executed strict budgets (`FRAME_MARKER`, `FRAME_0506`, `FRAME_1114`, `FRAME_0917`,
`KEY_W`, `E07A`, `L_3`, `L_4`, `L_15`, `L_17`, ten `C_j`, sixteen `Q_j`, twelve `PW_j`,
`SL11_T020`, and 49 `CLASS_*` files); the two derived occupancies `C_7`, `C_8`; the 84
clauses. Text: the normalization (§2), the class-row lemma and its capacity, validity,
boundary and strictness links (§3), the frame and the distinct-parent profiles (§4), the
eleven-case decision list with its seams (§5), the selected implications and the
coarse-capacity lemma (§6). Computation: 98 statements, 18,000 rows for each of the 94
fixed shapes and 9,000 for the four folded frame statements (1,728,000 rows per checker
in 1,152 slices), decided by the producers’ Python checker (`exact_classes.py`, Python
integers and `Fraction` for decisions, a numba int64 segment tree for the sweep under an
absolute atom bound `< 2^50`) and their Node checker (`verify_classes_wb.js`, BigInt
decisions, a `Float64Array` tree under the same bound); merged structurally; every
stored row re-decided from its recorded numbers by the public check `provenance`; the
small exact facts (`frame`, `wall_triggers`, `loose_identities`, `capacity`,
`partition`, `selector`, `selection_binding`) by the producers’ scripts.
Both large checkers were written by sessions of one AI system from one specification
(`KNOWN_ISSUES.md` item 4). Trust boundary: (K1) that the sweep implements the class-row
semantics, read in full by two earlier AI readers for the Python side and by nobody for
the Node sweep (`REPORT_COMPOSITION.md` §(b) 1); (K2) that the 1,152 slices ran the
pinned sources on the pinned inputs on rented Linux machines, which `P035` and `P037`
state as a provenance assumption and which no reader can test from the edition.
Verdict: the structure is sound as read and every hand step re-derives (§3.1, §3.2); the
computational premises are unverified here.

### Step 3, admission (`PROOF.md` §7, `P072`–`P080`)

Premise `ROOT_ADMISSION` (with `ENDPOINT`, `FRAME_ASSIGNMENT`, `WALL_PARTITION`,
`KEY_W_ELIMINATION`, `COARSE_LOOSE_CAPACITY`, the four `L_k`). Text: the chart
`ξ_(i,k) = e_(i,k)·(c − (U−L)(1,1)/2 − p_i)`, affine in the class-frame centre `c` and
in `L`, so extremal at polygon vertices paired with enclosure endpoints; the
quarter-turn lift rule for directions; the label-12 slot cut at `ρ`; the gated label-9
support cut; the label-11 arcs.
Computation: `scripts/run_adm.py` with `scripts/adm.py` (public check `admission`),
written by the project’s ADMISSION reader, 7 KB in all, read here line by line; 11 roots
times 17 labels, exact `Fraction`s, one physical clip per Cartesian label.
Trust boundary: the chart conventions (reference file, the `p13` correction, the tilted
axes for labels 11 and 13) are re-derived in `adm.py` from `SPEC_v3.0.md` §1 rather than
taken from the tree generator, which is the right way round; the stored output is one
line, so the margins `P080` quotes are reproducible only by rerunning (`KNOWN_ISSUES.md`
item 8). Verdict: correct as read; the geometry is elementary and is re-derived in §3.2.

### Step 4, local trees (`PROOF.md` §7, `P081`–`P090`)

Premises `LOCAL_CHECKER_SOUNDNESS`, `LOCAL_CERTIFICATE_IMPORT`; the 11 whole-root
obligations. Text: the leaf inference (`P082`–`P085`), the side-cap transfer (`P086`),
the flush-wall offset `ε` (`P087`), the reuse rules (`P088`), the eleven conclusions
(`P089`). Computation: eleven certificates (`JQ` one node; `JG_v2` 110 nodes by the
proof text and 113 in one report, one terminal leaf; `JPA_v5` 416 nodes; `JPWS_v4` 110
nodes; the others between) accepted by the two frozen checkers `wxcheck_v30.py` and
`wxcheck2_v30.js` against `SPEC_v3.0.md`, run three times by the producers, with the
post-check `h_report30.py` enforcing that the root node equals the named region and that
an `EMPTY` conclusion has zero terminal leaves.
Trust boundary: the specification’s soundness (read here, §3.3 below finds no hole in
sections 0–8 and 11), the two checkers’ fidelity to it (K3, written by sessions of one
AI system, five AI audits of the text, their agreement being evidence about slips of
programming and not about the text), and the runs themselves (K4; 4.8 GB of certificates
in the release, not run by any reader of the final round).
Guzhou0806 ran a checker of his own on two of the thirteen trees in an earlier state;
neither his checker nor his report is in the edition.
Verdict: the inference rules are sound as read; the runs are unverified here.

### Step 5, rigidity (`PROOF.md` §8, `P091`–`P112`)

Premises `G20S_PHYSICAL`, `WALL_CONTRADICTION` (with `ENDPOINT`, `ALGEBRAIC_ENDPOINT`,
`LOCAL_CHECKER_SOUNDNESS`); the trees `G20S` (679 nodes) and `HW` (579 nodes).
Text: the chain `JG → G20S → T1 → HW → T2 → sixteen-square entry → finite stage →
transfer → normalized contraction → core zero → square 8 touches two walls`.
Computation: the two trees; 17 finite rounds (12,929 rows, 1,564 exact dual bounds); the
two raw-to-root transfers and the two stop lemmas; the normalized prefix, the five-round
and sixth-round `B6` ancestry and the five stopped rounds; all replayed by the public
checks `finite_1`–`finite_4`, `finite_join`, `normalized_*`, `root_stops`,
`root_stop_binding`, `entry_transfer`, `entry_binding`, `small_entry`,
`root_chart_transfer`, `analytic_gate`, with the producers’ scripts and the review
scripts `independent_model.py` (a second row builder that shares the remainder formulas,
`KNOWN_LIMITS.md` row f). Trust boundary: the necessity of the rows is analytic and is a
premise independent of agreement between builders (`P097`); `REPORT_TERMINAL_2.md`
re-derived the finite rows, the stop cuts and both transfers by hand and found no gap;
the normalized 52-row gate’s validity for every core radius `0 < R ≤ 1/5000` rests on
`full_gate_analytic_review.md` and the earlier `g20s-terminal-audit` reviews, which the
final-round reader did not read (`REPORT_TERMINAL_2.md` line 23: “The rest of
G20S_PHYSICAL | NOT READ”) and which this review did not read either.
Verdict: the hand-overs and the endpoint contradiction re-derive (§3.3); the normalized
gate is the one step of the proof whose written justification I have not seen.

## 3. The Three Hardest Places

### 3.1 The class-row lemma (premise `CHARGE_SEMANTICS`, `PROOF.md` §3, `CLASS_ROW_LEMMA.md`)

**The statement, restated.** A certificate fixes a container of side `L_cert`, parents
of side `A`, sites with nonnegative integer feature weights, a budget `M` and a charge
scale `Γ`; a class file fixes closed convex centre polygons times closed tan-half gates
(with their quarter-turn lifts and declared symmetry images), thresholds `t_j ≥ 0` and a
bound `β`. For a pose `p` put `τ(p) = min{t_j : p ∈ E_j}`, or `1` if no class contains
`p`. The claim: for every finite family of closed unit squares with pairwise disjoint
interiors in the side-`C = L_cert/A` square centred at `c`, `Σ_p τ(p) < β`.

**The four links, as I re-derived them.**

1. *Capacity.* Each parent `p` receives one closed core `K_p` strictly inside its open
   parent; open parents of interior-disjoint squares are disjoint, so the cores are
   pairwise disjoint and every site lies in at most one core.
   A threshold feature with coefficients `a_j` and threshold `k` therefore fires on at
   most `⌊Σ a_j / k⌋` cores, and a winning-mask feature whose masks pairwise share a
   site fires on at most one.
   With nonnegative weights, `Σ_p χ(K_p) ≤ M`. No count of squares enters; touching
   squares cost nothing, since a site on a common boundary is in no core.
   (`exact_classes.py` lines 198–224 recompute exactly this `M` and refuse a certificate
   whose stated `budget_units` differs or whose absolute Möbius sum reaches `2^50`;
   verified by reading.)
2. *Row validity.* A row is an angle interval `I = [a, b]` in `u = tan(φ/2)` with a core
   direction `θ` and core side `B < A`. The checker tests at both ends that
   `A − B·max(cos δ + |sin δ|) > 0` for `δ = θ − φ`, and `cos δ + |sin δ|` increases
   with `|δ|` on `[0, π/4]`, so the core lies strictly inside the parent for every `φ`
   in the row. Concavity of `cos φ + sin φ` puts every legal centre in the closed
   envelope `[r, L_cert − r]^2`. Fixed rows chain from `u = 0` to exactly `u = 1` (a
   quarter turn, which is every square since side directions are a quarter turn apart);
   `mirror_x` and `orbit` rows must reach beyond `tan(π/8)`, and a pose beyond the rows
   is replaced by its mirror image, whose direction `π/2 − φ` has
   `u' = (1−u)/(1+u) < tan(π/8)`; the core is then reflected back into the original
   parent, and the class union and charge are invariant under the symmetry
   (`check_mirror`, lines 228–251, verified by reading).
3. *Closed boundaries and the class level.* For a centre on an arrangement edge, take
   generic centres in one checked adjacent cell converging to it with a constant
   site-hit pattern; every hit persists in the closed limiting core, which remains
   strictly inside the parent, and monotonicity of the Boolean features gives
   `χ(K_q) ≥ m(Q)`. The cell level `R(Q,I)` is the largest threshold among high classes
   that *meet* the closed product `cl(Q) × I`, else the least threshold among low
   classes that *contain* the whole product in one slot image, else `1`. Then `R ≥ τ(p)`
   for every `p ∈ cl(Q) × I`: a containing high class meets, so `R` is at least its
   threshold; if no high class meets, no high class contains `p`, every recognized low
   class contains `p`, so the minimum over all containing classes is at most the minimum
   over the recognized ones; and `R = 1 ≥ τ` when nothing is recognized.
   Overlapping classes, a parent in several high slots, and classes of threshold exactly
   `1` (kind `0`, which fall to the default) are all on the safe side.
4. *Strictness.* Every cell test is weak (`m(Q)·q ≥ p·Γ` by integer cross-products,
   `check_row` line 489 region); the one strict step is `M·q_β < p_β·Γ` (line 293). One
   integer unit of surplus suffices, and eight statements have exactly that surplus
   (`SMALL_CHECKS_PUBLIC.json`).

Together: `Γ Σ τ(p) ≤ Σ χ(K_p) ≤ M < βΓ`. The lemma is the Burns–Massaccesi–Levy charge
argument with class-dependent thresholds in place of one requested minimum, and it is
sound as stated.

**Objections tried and why they fail.** (a) *A square at the end of the row range.* The
representative direction `φ ∈ [0, π/2)` has `u = tan(φ/2) ∈ [0, 1)`; the square at
`u = 1` (direction `π/2`) is the square at `u = 0`, both rows are closed, and the slot
gates lie strictly inside `(−1, 1)` with their quarter-turn lifts tested on closed
intervals, so no square and no gate end falls between rows.
(b) *A pose whose centre is in no checked cell.* The envelope argument puts every legal
centre in `Env`, and `slabs_of` is generous by one slab each side; the CHARGE_CORE
reader proved the index formulas and asserted on every sampled slab that a region with a
nonempty interval lies in its range.
(c) *A parent in two cores.* A parent has exactly one core per row; different parents
may use different rows.
(d) *The 4/4/0 statements.* With thresholds `{4, 4, 0}` and default `1`, the minimum
score and the earlier high-first score coincide whenever the low classes are empty,
which is the only case the proof uses; `F1_PROOF.md` line 5 still says “high-first”,
which `KNOWN_ISSUES.md` item 1 flags.
(e) *The frame pairs.* The identity `Σ τ = 17 + N(high)/4 − N(low)/8` needs the high and
low unions disjoint, which `FRAME_DISJOINTNESS_PUBLIC.json` records (4, 4 and 12 strict
separations) and the public check `frame` recomputes; `P041` now states `q = 0` first,
the fix `REPORT_ERRATA_2.md` F1 asked for.

**Where the risk is.** Not in the mathematics, which I accept, but in three things the
text itself names. First, the proof of the lemma is spread over five pinned sources
(`CLASS_ROW_SOURCES_PUBLIC.json`: `RC`, `HF`, `CR`, `PY`, `CC`), none writing it out
whole (`KNOWN_ISSUES.md` item 2); the CHARGE_CORE reader assembled and re-derived it,
and so did I. Second, K1: the sweep and cell arithmetic that realize link 3 for
`5 × 10^9` cells per row were tested by brute force on 9 rows of 3 certificates (2,496
pose evaluations) and read in full for the Python side only; the Node sweep source has
been read by nobody at the needed level.
Third, K2: the lemma’s hypothesis “authentic complete execution on the bound inputs” is,
in the text’s own words, a provenance assumption (`P037`). The record’s own route cannot
read these certificates: `n-017.md` says the native parent-core verifier models only
`k`-of-`m` threshold atoms, and these files add weighted thresholds, winning masks and
class levels.

Verdict: the bridge from rows to packings holds; what remains is that the rows were
decided as recorded.

### 3.2 The root-admission geometry (§7), distinctness (§4) and the seams (§5)

**Re-derived from the literal files.**

- *The frame.* `FRAME_MARKER` (orbit, bound 17) forces one of eight images of the
  hexagon `M` occupied; the hexagon’s bounding box is
  `[537/250, 316/125] × [2.547…, 3.047…]`, squared diagonal `493/1250 < 1` (verified),
  so capacity one by inscribed open disks; `M` is invariant under `x → U − x`, so one
  further common reflection puts the occupant’s representative in `[0, π/4]`, and
  `ρ = 207107/500000` covers it because `ρ² + 2ρ − 1 = 309449/250000000000 > 0`
  (verified). The two pair statements give `17 + m/4 − t/8 < 137/8`, hence `t ≥ 2m ≥ 2`
  for integers; `FRAME_0917` with `h ≥ 5` gives `N(V) > 2h − 9 ≥ 1`, so `N(V) ≥ 2`, and
  capacity one of each clipped component (`L9` clipped to the physical box has squared
  diagonal `≈ 0.4627 < 1`) gives exactly one parent in `L9` and one in `L17`, distinct
  from the marker since `V` and `M` are separated (verified arithmetic; the separations
  are the `frame` public check).
- *KEY_W.* The file has `M` at `4`, the low union `E` at `0` on three slots whose
  centres all lie in `L9`: `[30651/100000, 44941/100000]` on all of `L9`, and
  `[0, 613/2000]`, `[−55059/144941, 0]` on the wall column `x ≤ 53/100`. Bound 20 with
  the marker occupied forces a low occupant, which is the unique `L9` parent; off-wall
  only the first slot can hold it; its lifts by `±90°` leave `[0, 1)`, so the
  representative `t_9 ∈ [30651/100000, 44941/100000]`. The lower exit
  `t_9 ≤ 61301/200000` misses it by `1/200000` and the high atom `t_9 > 44941/100000` is
  impossible (verified).
- *Loose roles.* `AQ = [−131/250, 53/100] × [24137/10000, 13/5] ⊂ L9` with `x ≤ 53/100`,
  so off-wall it is empty, including its boundary; each `L_k` (`M` at 4, `S_k` and `AQ`
  at 0, bound 20) then forces `S_k` occupied; the clipped `S_3` has squared diagonal
  `1097067164761/4·10^12 ≈ 0.2743` (from `L_3`’s polygon and the physical clip,
  reproduced to six digits), so one parent; `S_4`, `S_15`, `S_17` likewise by the quoted
  constants.
- *Coarse capacity.* The identity
  `(1+u²)²[1 − aw − bH + b(a+b)/2] = (1−w) + (1−2H)u + 4u² + (−1−2H)u³ + (1+w)u⁴` holds
  (expanded here), and the wall-strip derivation is right in both orderings: when the
  owner `A` is nearer the wall, `|Δy| ≤ H − d` and the other square’s support is at
  least `1/2`; when `B` is nearer, `f(φ) = h_B(n) + b·h_B(e_y)` is a positive sinusoid
  between its breakpoints `0, α, π/2`, hence concave there, with endpoint values
  `d + b/2` and `1/2 + bd` whose difference `(1−b)(a+b−1)/2 ≥ 0`, so `f ≥ 1/2 + bd` and
  the same inequality `aw + bH − bd ≥ 1` follows without tying `B`’s angle to `A`’s. On
  128 equal subintervals all five Bernstein coefficients are positive for both parameter
  pairs, with minima `634043429/125829120000` and `43535731167/8388608000000`, exactly
  the quoted values (verified).
  Coarse 17’s clipped squared diagonal `1851391155161/4·10^12 ≈ 0.4628` (reproduced to
  six digits).
- *The escape set `X` of the `C` files.* From `C_12`’s literal file: slots 1–2 are the
  two angular exits on `L9` (`[0, 613/2000]` and `[−5803/14197, 0]`), slot 3 is `AQ`
  with a recut arc, slots 4–9 are the three coarse regions with arcs beyond `±1/20`. The
  gated role 9 misses slot 1 by `1/200000` and the back-lift of slot 2 by
  `974949/14088170000` (verified: `4197/10000 − 591183/1408817`); `AQ` is empty; a gated
  loose role with `|τ_k| < 1/20` has no lift in `[1/20, ρ]` or `[−ρ, −1/20]`; and coarse
  capacity forbids a second parent there.
  So `X` is empty and each bound-20 `C_j` forces its target.
- *Label 12.* `C_12`’s marker class is four slots: the right strip of the hexagon, its
  bottom strip, its top trapezoid, and the whole hexagon with arc `[0, 558609/2000000]`;
  the target is `[20889/10000, 3111/1250] × [25971/10000, 2997/1000]` with arc
  `[558609/2000000, 4494109/10^7]`. A point of the hexagon with representative in
  `[0, ρ]` is in one of the four marker slots or in the target (verified case by case),
  so an empty target puts the marker parent at score 4 and the budget forces the target;
  the farthest pair of the union is a target corner and a hexagon vertex at squared
  distance `0.39522 < 3953/10000` (verified), so target 12’s occupant is the marker
  parent, and its slot may be cut at `ρ` because the `−90°` lift of a representative in
  `[0, ρ]` is negative.
- *`C7`/`C8`.* `E07A`’s target `[−1/2, 3501/5000] × [19879/5000, 26/5]` with arc
  `±751411/10^7` reflects in `x → U − x` to `[19879/5000, 647/125] × …`, inside the
  quoted `C8` target, and the two centre projections are separated by `8189/2500`
  (verified from `E07A`; `C8`’s literal not read).
- *The wall lemma of `run_adm.py` lines 17–18.* A unit square in `x ≥ 0` with centre
  `x < 53/100` has `(cos|θ| + sin|θ|)/2 ≤ x`, so `cos|θ| + sin|θ| < 53/50`; at
  `t = 31/1000`, `(1 + 2t − t²)/(1 + t²) = 1.06002… > 53/50` (verified), and the
  function increases on `[0, π/4]`, so `|θ| < 2 atan(31/1000)`. In the endpoint frame
  the left wall is at `(U−L)/2 > 0`, so the lemma applies a fortiori.
- *The gated-9 support cut.* `x_9 ≥ (cos θ_9 + sin θ_9)/2` for `θ_9` in the first
  quadrant; the support is concave on the arc, so its minimum is at a gate end, and the
  root box’s left end `−9897/10^6` sits `4.3 × 10^-7` below it.
- *The lift rule.* `interval_in_arc` requires some quarter-turn lift of the whole slot
  inside the root arc; a square with some side direction in the slot then has a side
  direction in the arc, which is all `F(root)` asks (`SPEC` §0: one side direction per
  square, feasibility independent of the choice).
- *Seams.* Every target, trigger, root box and root arc is closed; the decision list’s
  13 predicates are conjunctions of comparisons of one coordinate with a rational;
  `x_9 =
  53/100` and `y_9 = 129/50` belong to `JQ`, `y_9 = 13/5` to `JPWS` (whose loose labels
  use the through-`13/5` `Q` statements because `AQ` may then be occupied), `JPW13`
  needs `y_9 > 13/5` strictly because the `L` files’ `AQ` is closed at `13/5`; `t_9`
  endpoints belong to `JPA`; `τ_k = ±1/20` belong to the signed branches.
  The ADMISSION reader’s 15,000-atom check and the public check `partition` decide this
  with four mutation controls.

**Not re-derived here, and decidable by lane K3’s cheap public checks:** the 29 wall
triggers (`wall_triggers`), the 84 selected clauses’ trigger containments and the `L_k`
extra premises (`selector`, `selection_binding`), the per-root 136 pairwise target
separations and 17 capacities (`extra.py`, inside `admission`), the 12 and 4 frame
separations (`frame`), the identity of the pair statements’ low unions with the
`FRAME_0917` bonus unions, and the inclusion `S17 ⊂ L17`.

**Strongest objection.** The admission is only as deep as the endpoint enclosure: its
smallest position margin, `R − L_hi − ε = 4.32 × 10^-17` at every flush right or top
wall end (labels 2, 6, 7, 8, 15, 17), exists because the reference file leaves
`ε = 5.17 × 10^-18` at each wall and `L` is `4.84 × 10^-17` below `R`. That is a
property of the construction, not an error, and the wider `10^-50` enclosure still
leaves it positive (`ENDPOINT_AUDIT.md`, probe `wide_probes/admission`); but a reader
who replaces `L` by its rounded display, or `R` by `L`, loses the step, which is what
`P086`–`P087` warn against.
The second objection is documentary: the only written argument for the admission
geometry is `PROOF.md` `P073`–`P079` plus a two-line comment in a script
(`KNOWN_ISSUES.md` item 1), and `F1_PROOF.md`, bound as a file of record for this
premise, is about the loose roles.

Verdict: no gap found; the geometry is elementary and re-derives; the premise without a
separate written proof is this one, and its risk is low because every number it rests on
is a finite exact computation that two of the 31 public checks decide.

### 3.3 The hand-overs into the rigidity theorem (§8)

**Checked end for end against the literal windows.** `JG_exact_v2.json`’s terminal is
sixteen labels at `|φ_i| ≤ 1/10` and position radius `1/5`, with
`ξ_(2,1) ∈ [−39/125, 0]` and `ξ_(13,2) ∈ [−1/5, 28/125]`, and label 4 free; that equals
`EXPECT_G20S.json`’s window.
`G20S` is a sixteen-label tree with `S_floor = 4`, so its (ANN) applies to the
normalized packing at side `L` once `L ≥ 4`, which the area of sixteen unit squares
gives. Its tube `T1` is `HW`’s window with `ξ_(2,1)` up to `1/100`; the configuration is
the same, so `ξ_(2,1) ≤ 0` from `G20S`’s window is retained and it lies in `HW`. `HW`’s
tube `T2` (core `1/250`, angles `1/500`, `ξ_(2,1) ∈ [−8/25, 1/250]`,
`ξ_(11,2) ∈ [−1/5, 1/20]`, `ξ_(13,2) ∈ [−1/5, 3/40]`), with the cut retained again, lies
in the sixteen-square entry (core `1/200`, angles `1/400`, `a ∈ [0, 8/25]`,
`b ∈ [−1/20, 1/5]`, `z ∈ [−1/5, 3/40]`) under `a = −ξ_(2,1)`, `b = −ξ_(11,2)`,
`z = ξ_(13,2)`. Every one of these numbers matches between `P092`–`P095`, the two EXPECT
files and `THEOREM_G20S.md` §2 and §4. Neither hand-over holds without the retained cut,
as `P094` says.

**The chart.** The capture side works in `F_U`; the trees and the terminal theorem in
the corner-at-origin chart of `[0,S]^2`; they differ by the one fixed translation
`(U−L)/2` stated in `P019`, `P076` and the root file’s `frame` field, which I confirmed
reads “a class-frame point `c` corresponds to `c − (U − S*)/2`”. The trees are proved at
`S = R` and applied at `S = L < R` by enlarging only the container (`SPEC` §11), with no
translation. The sixteen-square theorem is applied at actual `S = L`, never at `R`; the
input is stated against the rational reference and the conclusion against the exact-root
reference (`P111`), and the transfer between them keeps the same raw slider when
bounding the axis change, which is what makes the error `10^-17` rather than the width
of the slider box (`entry-producer/PROOF.md`, “Exact transfer”; the `−T0/3` correction
of `p13` is load-bearing, as REPORT_TERMINAL_2’s control shows).
`a* ≥ 0` is not read off a transferred interval but follows from square 2’s right wall
and `S ≤ S*`.

**The contradiction.** With the core zero, nonslider square 8 sits at `(L−1/2, L−1/2)`
axis-parallel and touches `x = L` and `y = L`; the normalized packing lies in
`[d, L−d]^2`, `d = (L−S_0)/2 > 0`; a common dihedral image moves which walls are touched
and nothing else. A conclusion “`S = L`” alone would be a tautology for the normalized
packing; the wall contact is what excludes `S_0 < L`. This is the same finishing
mechanism as the n = 11 proof’s endpoint argument, which the record reviewed for
`T-060`, and it is right.

**Strongest objection: the normalized contraction.** `P110` and
`full-stopped-propagation/continuation/THEOREM.md` argue: if `R = max|h_j| > 0`,
normalize the 45 core coordinates by `R`, keep `a, b, z` unscaled, and use “the pinned
normalized 52 geometric inequalities, necessary throughout the full padded slider domain
for every `0 < R ≤ 1/5000`”, plus 192 product-hull rows and three stop rows; five rounds
of exact weak duality then give `max|h_j/R| ≤ 159201934153319/200000000000000 < 1`,
contradicting `max = 1`. For a row linear in `h` to survive division by `R` with the
sliders unscaled, its constant-plus-slider part must vanish identically along the
three-slider family at the exact root (the “exact root base-gap identities” for the 11
unique-owner and 8 parallel contact pairs) and its remainder must be `O(R²)`; the
theorem names these inputs and the `full-gate` review as accepted, but neither
`PROOF.md` §8 nor `CLASS_ROW_LEMMA.md`’s companions derive them, and the last reader of
record stopped before this step (`REPORT_TERMINAL_2.md` line 23). This is the one link
of the whole proof whose written justification I have not seen; it is not a gap I found,
it is a step I could not check.
Its arithmetic (`normalized_prefix`, `normalized_five_rounds`, `normalized_sixth_round`,
`normalized_finish`) is in the 31 public checks, so lane K3 can confirm the duals; the
necessity of the rows is for a reader of `full_gate_analytic_review.md`,
`analytic_envelope_text.md` and `normalized_division_text.md`.

**Second objection, documentary.** Two routes finish the same step with different
constants: `records/THEOREM_G20S.md` proves step 3 by the `box-wide` terminal instance
(ratio `0.859`, 8 rounds), while the proof text composes the sixteen-square stopped
contraction (ratio `0.796`, 17 + 5 rounds).
The claim of `G20S_PHYSICAL` says the former is an alternative and not an extra step,
which is consistent; but the file bound as `file:NORMALIZED_RIGIDITY` and the file bound
to the premise disagree about which route is of record (`REPORT_COMPOSITION.md` line 66;
`KNOWN_ISSUES.md` item 7).

Verdict: the hand-overs are correct and exact; the terminal theorem’s finite stage,
transfers and stops are re-derived by a reader of record and look right to me; the
normalized gate is open to reading.

## 4. The Fifteen Premises

| Premise | Written proof | Complete as written | Standard or novel | Assessment and risk |
| --- | --- | --- | --- | --- |
| `ALGEBRAIC_ENDPOINT` | `ENDPOINT_AUDIT.md`; receipts and two programs | Yes | Standard (Newton–Kantorovich) | Agrees with the record’s own root; low |
| `UPPER` | `P012`–`P015`, `UPPER_FORMULAS.md`; two constructions, one ours | Yes | Standard | Decided in our record independently; nil |
| `ENDPOINT` | `endpoint-normalization-producer/THEOREM.md` §1–2; `P017`–`P021` | Yes | Standard (the n = 11 finishing mechanism) | Re-derived; nil |
| `CHARGE_SEMANTICS` | `CLASS_ROW_LEMMA.md` with pointers into five sources; `REPORT_CHARGE_CORE.md` §(2) | Yes once assembled; not in one place (`KNOWN_ISSUES` 2) | Standard core (Burns–Massaccesi–Levy charge) with a novel class-level and closed-boundary layer | Mathematics re-derived; the risk is K1 and K2, not the lemma |
| `FRAME_ASSIGNMENT` | `FRAME_L9.md`; `P039`–`P042` | Yes, given the four rows and the frame separations | Novel composition of standard counting | Arithmetic re-derived; the union identities and separations are a public check |
| `C7_C8_TRANSFER` | `c7-c8-inherited-producer/PROOF.md`; `P047` | Yes | Standard reflection | Containment verified from `E07A`; low |
| `WALL_PARTITION` | `F1_PROOF.md`, `PROOF_BRIDGE_V2.md` (application), `P049`–`P060` | Yes; one “high-first” sentence to reconcile | Novel case design, standard steps | Re-derived; low |
| `ROOT_ADMISSION` | **None separate**: `P073`–`P079` and a script comment (`KNOWN_ISSUES` 1) | The computation is complete; the prose is not | Standard geometry | Re-derived in §3.2; low mathematical risk, the one documentary gap the source admits |
| `SELECTOR_LOGIC` | Tables only (`S6_ACTIVATION*.json`, `PER_BRANCH_…json`); `P062`–`P071` | Yes as a finite selection | Bookkeeping | Three readers covered 36 + 24 + 24 clauses; a public check binds the 84; low |
| `LOCAL_CHECKER_SOUNDNESS` | `SPEC_v3.0.md` §2–8, 11 (lemmas with proofs); two checkers | Yes for the text; the checkers are code | Novel engine (branch-and-contract with indicator lifting and SOS leaves), standard lemmas | Text sound as read; the risk is fidelity of two same-author checkers (K3) |
| `LOCAL_CERTIFICATE_IMPORT` | Records and the post-check; `P086`–`P089` | Yes | Bookkeeping plus the side-cap transfer (`SPEC` §11) | Side-cap argument re-derived; the runs are K4 |
| `G20S_PHYSICAL` | Sixteen-square `THEOREM.md`, `ANALYTIC_ENVELOPES.md`, `FINITE_PARALLEL_DERIVATION.md`, normalized `THEOREM.md`; `P092`–`P110` | The finite stage yes; the normalized gate’s necessity is not written in the proof packet | Builds on this project’s core-stress recipe; the stopped normalized contraction is novel | The one step not read by anyone of record in the final round, §3.3 |
| `WALL_CONTRADICTION` | `ENDPOINT_CASE_G_LEMMA.md`; `P111`–`P112` | Yes | Standard | Re-derived; nil |
| `KEY_W_ELIMINATION` | `case-repair-S/PROOF.md`; `P049`, `P053` | Yes | Standard | Re-derived from the literal `KEY_W`; nil |
| `COARSE_LOOSE_CAPACITY` | `coarse-capacity-R/PROOF.md`, `PROOF_BRIDGE_V2.md`; `P065`–`P066` | Yes | Novel wall-strip lemma, elementary | Identity and Bernstein tables recomputed exactly; nil |

The premise without a separate written proof is `ROOT_ADMISSION` (`KNOWN_ISSUES.md` item
1, `PREMISES.md` row 8). Its risk is the lowest kind this proof carries: every quantity
it needs is a rational number in a pinned file, the script that decides it is 7 KB and
was written by a reader rather than a producer, and the two hand steps are three lines
each and verified here.
The premise I would rank riskiest on the written evidence is `G20S_PHYSICAL`, for the
reason in §3.3; the premises riskiest on the computational evidence are
`CHARGE_SEMANTICS` (through K1 and K2, which all 191 capture-side obligations inherit)
and `LOCAL_CHECKER_SOUNDNESS` (through K3).

## 5. The Computations

What a full independent replay of each kind would establish, and what it would not.

| Kind | Size | Replay establishes | Replay does not establish |
| --- | --- | --- | --- |
| `check.py` levels 0–2 (41 checks, 31 of them the producers’ public checks; ~4 min on the author’s Mac; untested on Linux) | 7,118 files, 22,013 pins, 12 large files | File identity against `MANIFEST.sha256`; the cheap exact facts (upper bound, tight enclosure, partition, admission, capacity tables, frame separations, wall triggers, loose identities, selector binding, dependency graph); every stored capture row re-decided from its recorded minima (`provenance`); every rigidity dual bound (`finite_*`, `normalized_*`, `root_stops`, `entry_*`, `small_entry`); the third tree execution equal to the second | That any capture row’s minimum is what the certificate gives (no sweep is run); that any tree is accepted (only stored `PASS` lines are read); the necessity of the rigidity rows |
| Capture certificates (98 statements, 1,728,000 rows per checker) | 1,152 slices; “many machine-hours” (`CHECK.md`) | With the producers’ checkers: that the stored rows reproduce (`same-implementation`), closing K2 for the rows replayed; with a new checker written from `CLASS_ROW_LEMMA.md` and the file formats: an `independent-implementation` decision of the 98 strict budgets, closing K1 for the rows replayed | The class-row lemma itself (a theorem, read in §3.1); the selected clauses’ logic |
| Tree certificates (13 trees, 4.8 GB in the release) | Python checker and Node checker; the author’s second execution took one night on one machine | With the frozen checkers: that each certificate is accepted (`same-implementation`), closing K4; with a checker written from `SPEC_v3.0.md` (Guzhou0806 has one; so could this project): an `independent-implementation` decision, closing K3 for the trees replayed | The specification’s soundness (a text, read here); the admission into the roots |
| Rigidity finite stage and contraction | 12,929 rows, 1,564 + 460 + 92 bounds; seconds to minutes | That the saved dual multipliers prove the saved bounds on the saved rows (`check.py`), and, with `independent_model.py`, that a second builder reconstructs the same rows from the geometry | The analytic necessity of the rows, and in particular of the normalized 52-row gate for every `R` (§3.3) |

**The minimum set of replays that moves the record’s rungs.** Under
[epistemics.md](../../../epistemics.md), a compound claim takes the minimum rung of its
load-bearing parts, and `C3` needs confirming-origin machine evidence with a
certificate, a replay command and a passing replay, plus one control path, for every
such part. The upper half already stands at `V3/C3` here.
For the lower half, the minimum is:

1. `check.py` levels 0–2 with the 12 large files, to `PASS`, on this project’s Linux
   host (it has never run off macOS), recording the `MANIFEST.sha256` digest against the
   release notes;
2. all 98 capture statements, every row, with at least one of the two producers’
   checkers (the Python one is the one whose core two readers have read), from the
   carried `certificate.json` and `classes.json` bytes, comparing every row minimum and
   cell count with the carried receipts;
3. all 13 tree certificates with at least one frozen checker and the post-check
   `h_report30.py`, confirming the root node equals the pinned region, zero terminal
   leaves for the ten `EMPTY` roots, and the `JG` terminal equal to `EXPECT_G20S`’s
   window;
4. one mutated-input control per kind (a certificate with one weight raised, a tree with
   one multiplier made negative), refused.

That is `same-implementation` confirmation; it earns `V3/C3` and the register would
print *confirmed, reproduced with the producer’s code*. An `independent-implementation`
mark needs a sweep and a tree checker written here from the texts, which is a project,
not a replay.

**Which of lane K3’s samples matter most**, in order: (i) the eight one-unit-surplus
statements of `SMALL_CHECKS_PUBLIC.json` (`Q_6`, `Q_7`, `Q_16`, `PW_6`, `C_10`,
`CLASS_PSS_L02_T15`, `CLASS_PS_L14_T17`, `CLASS_PS_L06_T17_ENDm_H4T4`), every row, in
both checkers, because one unit is the whole margin; (ii) `FRAME_1114`, strict by half a
unit (`REPORT_FRAME.md` C2), and the other three frame rows plus `KEY_W`, because every
branch rests on them; (iii) `JG_v2` (110 nodes, the only `TUBE`), `JQ` (one node) and
the two hand-over trees `G20S` and `HW`, with both checkers, because the tube route is
the one that cannot be cross-checked by any other branch; (iv) the eleven `admission`,
`partition`, `frame`, `capacity`, `wall_triggers`, `loose_identities`, `selector` and
`selection_binding` checks, which decide every literal number §3.2 did not re-derive;
(v) `recompute_slice.py` on a few slices of (i) against the carried slice records, which
is the only test of authenticity available short of the full sweep.

## 6. Defects

No blocking defect was found in the mathematics read.
The items below are the defects and weaknesses found, each with its place.

| Blocking | Where | What |
| --- | --- | --- |
| No | `PKT/scripts/run_adm.py` lines 17–18; `PROOF.md` `P073`–`P079`; `KNOWN_ISSUES.md` item 1 | The wall-direction lemma for label 9 in the wall branches exists only as a script comment and assertion; the admission geometry has no written proof outside the proof text. Verified here; to be written in v1.1. |
| No | `PKT/revision-v7/PROOF.md` `P110`; `g20s-terminal-audit/full-stopped-propagation/continuation/THEOREM.md`; `REPORT_TERMINAL_2.md` line 23 | The normalized 52-row gate’s validity for every `0 < R ≤ 1/5000` (base-gap identities and `R`-scaling with unscaled sliders) is cited as accepted and derived nowhere in the proof packet; no final-round reader read it. Not a found gap; an unread step. |
| No | `records/THEOREM_G20S.md` §4 step 3 versus `LABELS.tsv` row `file:NORMALIZED_RIGIDITY`; `KNOWN_ISSUES.md` item 7 | Two routes with different constants (`0.859`, `0.796`) finish the same step; the file bound to the premise proves it by the route the text does not use. |
| No | `PKT/revision-v7/LABELS.tsv` row `file:SELECTED_CLAUSES` | Bound to `research/…/current-author-20261012i/…/runtime/SELECTED_ORIGINAL_MAP.json`, a sibling folder of the packet, not the packet’s own copy; `file:C12_PROFILE_CAPACITY` is bound into `public-edition-BK-20261011/revision-v4/`. Harmless if the bytes are identical (the six copies have one size), but the edition says every carried file keeps one path. |
| No | `review-repair-O/F1_PROOF.md` line 5 | Says “high-first counting implication” where the proof text uses the minimum score; equivalent when the low classes are empty, which is the only use. |
| No | `PROOF.md` `P090` | “93 option splits” for `JPA_v5` is in no machine report (the report says 135 splits); `P080`’s admission margins are in no stored output (`KNOWN_ISSUES.md` item 8). |
| No | `PROOF.md` `P035`, `P037`; `KNOWN_LIMITS.md` rows c, d | Execution authenticity of the 1,152 slices and the 26 tree runs is an assumption; the edition cannot show which bytes a past run read. This is the trust boundary, correctly declared, and it is what the replays of §5 close. |
| No | `REPORT_COMPOSITION.md` §(b) | Four blocks have no final-round reader at the needed level: the capture-checker core (K1), execution authenticity (K2), the residue of the tree checkers (K3), the tree arithmetic (K4). An audit-coverage gap, not a mathematical one. |
| No | `OVERVIEW.md` “checked” paragraph; `KNOWN_ISSUES.md` items 4–5 | “Two independently written exact checkers” were written by sessions of one AI system from one specification; producer and reviewer are often the same system. Correctly disclosed; it limits what the internal audit can mean. |
| No | tracking issue #557 (ours) | The title says n = 18; the source is n = 17. |

## 7. The Record

**The rungs now.** Nothing here has been replayed; this review is a qualifying read with
no defect found and stated conditions.
By [epistemics.md](../../../epistemics.md) the result enters at `V0`, declared with
`notes` explaining that the source’s own replays and internal audit are retained in the
source and not here, exactly as `T-060` entered on 2026-09-29; and at `C1` once this
review is on file as the `external_review` of the reported-evidence entry, state
`informally-verified`, with the note that the premises `CHARGE_SEMANTICS` (through K1,
K2), `LOCAL_CHECKER_SOUNDNESS` (through K3, K4) and the normalized gate of
`G20S_PHYSICAL` were not re-proved and no computation was replayed.
Status: *reviewed*.

**After each planned step.**

- After the four replays of §5 pass here, with their receipts and one control each:
  `V3/C3`, *confirmed, reproduced with the producer’s code*, the composition note naming
  the capture rows and the trees as the parts that set the rung.
  A failed replay of any part leaves the result *incomplete* with
  `replay_status: failed`.
- After a second adversarial AI review by a distinct reviewer (another model family, or
  a lane prompted without this one’s context) whose latest verdict accepts, and a human
  oversight record by the owner naming `trust-boundary`, `certificate-meaning` and
  `ai-findings`: `V4/C4`. Until the normalized gate of §3.3 has been read by someone of
  record, I would not count this review’s verdict as the accepting one for rung 4; it
  accepts what it read and says what it did not.
- An `independent-implementation` mark, and any move toward rung 5, is the Lean
  formalization the source plans and has not started; nothing here depends on it.

**Whether the case status may move.** The schema admits only `proved` and `open` for
both fields. The precedent is the n = 11 record on 2026-09-29 (commit `3f840d072`):
`reported_status: proved`, `status: open`, the reported lower bound moved to the claimed
exact value with a note saying the claim was unverified, a priority note, and a register
entry at `V0/C1`, `S5`, kind optimality.
Following it: `n-017.md` takes `reported_status: proved`, keeps `status: open`, moves
`reported_lower_bound` to `L` (exact form the root of `F, G` in the stated box, or the
catalogue’s degree-18 polynomial, which the record already holds), `proved_by` Overbeck,
with a note quoting the source’s own words, “candidate proof, not an established
theorem”, and the AI assistance statement in the source’s terms; the verified lane stays
at `T-093`’s `18641771/4000000` and the `mathematics` blocker stays.
One judgement for the owner: the n = 11 source called itself a proof, this one calls
itself a candidate; the reported lane preserves the literal claim and does not endorse
it, so the precedent applies, but the note must carry the source’s own status words.

**Significance.** `S5` is right, and the rationale against the scale is this.
The anchor for `S5` is movement on a central open case.
n = 17 is, with n = 12, one of the two open cases below n = 18 (n = 13 to 16 are
proved), the case this project’s own lane has worked longest (its kernel certificates,
`T-042`, `T-043`, `T-093`, and some forty reviews), and the one the owner names as
central. The claim settles it exactly, at Bidwell’s 1998 side, closing the whole
`0.01508734360455` gap between the verified floor `4.66044275` and the certified
ceiling, where `T-093`’s step was `2.75 × 10^-6`. It is scored as `T-060` was on
2026-09-29, at `S5` while unverified, because the score is of the claim and not of its
rungs, and as `T-037` was, “by the rubric’s anchor, movement on a central open case”.
The method is a composition of this project’s charge and local-isolation recipes with
Ahmed’s proof shape; that lineage is the credit line’s business, not the score’s.

## 8. Questions for the Author

1. `PKT/revision-v7/LABELS.tsv`, row `file:SELECTED_CLAUSES`: the label binds
   `current-author-20261012i/…/runtime/SELECTED_ORIGINAL_MAP.json` rather than the
   packet’s `current-author-20261012t/…` copy.
   Are the six copies byte-identical, and is the binding intended?
   Same question for `file:C12_PROFILE_CAPACITY`, bound into
   `public-edition-BK-20261011/revision-v4/`.
2. `PROOF.md` `P110` and `full-stopped-propagation/continuation/THEOREM.md`: which
   document derives that the 52 normalized geometric rows are necessary for every
   `0 < R ≤ 1/5000` with the sliders unscaled, that is, the exact-root base-gap
   identities along the three-slider family and the `O(R²)` remainders?
   If it is `full_gate_analytic_review.md`, will v1.1 bind it as a file of record of
   `G20S_PHYSICAL` and summarize the argument in §8?
3. `records/THEOREM_G20S.md` §4 step 3 versus `LABELS.tsv` `file:NORMALIZED_RIGIDITY`:
   which route (`box-wide`, ratio `0.859`; or the sixteen-square stopped contraction,
   ratio `0.796`) is the one of record for `G20S_PHYSICAL`, and will v1.1 bind one?
4. `PKT/scripts/run_adm.py` lines 17–18 and 84–87, `PROOF.md` `P073`–`P079`: v1.1’s
   written admission geometry should state the lift rule (“some quarter-turn lift of the
   whole slot inside the root arc”), the label-12 cut at `ρ` and its precondition
   `a_lo > −ρ`, and the wall lemma, so that `adm.py` is a check of a text.
5. `review-repair-O/F1_PROOF.md` line 5: reconcile “high-first” with the minimum score,
   or state that the two coincide when the low classes are empty.
6. `NOTATION.md` row `E07A; C7/C8 transfer` and `EXACT_ENDPOINT_AND_CASES.json` block
   `C_legacy_exemption_absence`: no `C_7` or `C_8` statement folder exists; where are
   the literal `C7` and `C8` target polygons bound (the
   `c7-c8-inherited-producer/inputs/accepted.json` pin?), so that a reader can check the
   `19879/5000` and `647/125` containment from a carried file?
7. `PROOF.md` `P090`: “93 option splits” against the stored report’s 135; which is the
   number of record?
8. `CHECK.md`, “Where it was run”: `check.py` has run on one macOS machine only.
   Lane K3 will run it on Linux; which output differences besides `small_entry`’s
   regenerated hash would the author expect, and will a Linux `PASS` be recorded in
   v1.1?
9. `README.md`, “Licence”: our record retains digests, receipts and derived exact facts
   only, and runs the checks, which the current terms allow.
   Is a licence that permits retaining the proof text and class files planned after the
   first review round?
10. `KNOWN_LIMITS.md`, “The sealed record is not in this edition”: would the author
    publish the RFC 3161 timestamps and the git objects of the sealed record, so that
    the comparison records of the capture computation can be checked by a reader?
11. `KNOWN_LIMITS.md`, “Outside review so far”: may Guzhou0806’s checker and his report
    on `JQ` and `JPG15p_v5` be published, or may this project obtain them, since they
    are the only tree decisions by code written outside the project?

## 9. Checks Made Here

All in exact rational arithmetic with the project interpreter (`uv run --frozen` from
`packing/`, `python -I`), none over a second of CPU:

- `L` from the statement’s `(t_0, b_0)`, `F`, `G` by 60-digit refinement; residual of
  the record’s degree-18 polynomial at `L`: `2.06 × 10^-44`; angles `2 atan(t_*)`,
  `2 atan(b_*)`: `39.8049589797677950…°`, `36.6237863834465893…°`;
  `R − L = 4.8366 × 10^-17`.
- Wall-strip quartic: Bernstein coefficients on 128 equal subintervals for both
  parameter pairs all positive; minima `634043429/125829120000` and
  `43535731167/8388608000000`.
- `ρ² + 2ρ − 1 = 309449/250000000000`; hexagon bounding diagonal squared `493/1250`;
  `(1 + 2t − t²)·50 > 53(1 + t²)` at `t = 31/1000`; gate gaps
  `30651/100000 − 61301/200000 = 1/200000` and
  `4197/10000 − 591183/1408817 = 974949/14088170000`; the frame counting `t > 2m − 1`,
  `N(V) > 2h − 9`.
- From the literal class files: `AQ ⊂ L9`; the clipped `S_3` diagonal; the hexagon
  covered by `C_12`’s four marker slots and its target; the union diameter
  `0.39522 < 3953/10000`; `E07A`’s target reflected into the quoted `C8` target.

Nothing was downloaded from the release; no checker, tree or capture row was run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
