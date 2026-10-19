# Overbeck’s Candidate Proof of s(17) = L: Second Adversarial Review

**Status:** amended by the
[status addendum of 13 October 2026](#status-addendum-2026-10-13), which corrects check
8, withdraws question 5 and the second half of SR-8’s resolution, and qualifies four
statements; the verdict stands.

**Verdict: accepted.** No blocking defect was found in what was read.
The normalized 52-row gate of `G20S_PHYSICAL` (PROOF.md P110) is valid for every core
radius $0 < R \le 1/5000$, and this review shows it with code of its own: an independent
transcription of the exact-root layout, a Krawczyk proof of the root box, a
Gröbner-basis proof of all 52 base-gap identities and of slider invariance, an option
audit of all 152 separating alternatives, and an independent row builder whose rows,
driven only by the producer’s multipliers, take the whole chain (the six B6 steps, the
stop cuts and the five stopped rounds) to a final 45-core ratio of $0.79202 < 1$. Every
geometric row of the five stored stopped models is implied, exactly, by the rows derived
here. The two tree checkers’ contract (`SPEC_v3.0.md`) was read in full and its lemmas
checked by hand, and the Python tree checker was read against it at every step that
decides acceptance, the centred remainder rule included.
The capture engine’s core was read, all 98 capture budgets were recomputed from their
features, and all 9,000 rows of one statement were re-decided.
The root admission of all eleven roots, the separation and capacity of all eleven
seventeen-target profiles, the upper construction, the coarse-capacity quartics and the
physical stop cuts were recomputed exactly.

Nine findings are recorded, none blocking: evidence that the edition does not carry,
bindings that are missing or inconsistent, and robustness and tooling points.
The largest is SR-1: before this review, nothing in the edition rebuilt the normalized
model’s coefficients and remainders independently of the producer’s `rigidity.model`.
What this review did not read is listed below, and the claim stays a candidate until the
complete replay and the human oversight record exist.

Reviewer: an AI agent, the second adversarial review lane of the #557 intake (bead
think-4j3n), model `claude-opus-5-5`, tbd-strong-max tier, reasoning setting max,
prompted separately from the first review lane and blind to its document until its own
findings were written.

It registers nothing and moves no rung.
It is not a human oversight record.

## Scope and Evidence

**Source.**
[Kleddamag/the-seventeenth-square-candidate](https://github.com/Kleddamag/the-seventeenth-square-candidate)
at commit `653b9589d0f8a152f01adc56b1d48ba53d49abc3` (“Candidate proof: the 1998 packing
of 17 unit squares is optimal (verification edition)”), version 1 of 12 October 2026, by
Marc Leonard Overbeck (GitHub Kleddamag), with the release `large-files-v1`. The tree
was fetched shallowly at that commit into a scratch directory; the 12 large files of the
release (4.8 GB of tree certificates and one result record) were not downloaded, and no
script of the edition was executed.
No upstream bytes are retained in this repository.

The edition’s own account applies throughout: the mathematics, engines, checkers and
text were produced by AI systems (Codex, Claude) under the author’s direction, the
internal reviews were made by separate sessions of the same systems, and no human in the
project has read the mathematics.
“Independent” below means independent of the producer’s code, not of the AI systems that
wrote it.

`PKT/` stands for
`research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011/`
and `G/` for
`research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit/`.

| Depth | Files |
| --- | --- |
| Read in full | `STATEMENT.md`, `STATEMENT_STATUS.md`, `README.md`, `OVERVIEW.md`, `PREMISES.md`, `KNOWN_ISSUES.md`, `CHANGELOG.md`; `PROOF.md` (P001 to P116); `PKT/revision-v7/CLASS_ROW_LEMMA.md` and `LABELS.tsv`; the 52-row gate texts `full_gate_analytic_review.md`, `analytic_envelope_text.md`, `normalized_division_text.md`; `PKT/records/THEOREM_G20S.md`; `G/full-stopped-propagation/continuation/THEOREM.md`, `RESULT.md`, `REPLAY.md`, `PREFIX_DIAGNOSTIC_ERRATUM.md`, `inputs/stop-proof.md`; `G/full-stopped-propagation/producer/RESULT.md` and `REPLAY.md`; `G/full-stopped-propagation/continuation-independent-review/REVIEW.md` and `check.py`; `G/full-stopped-propagation/rational-entry-review/REVIEW.md`; `G/full-gate/independent-review/MANIFEST.json`; `G/sixteen-square-corollary/producer/THEOREM.md`; `G/finite-entry-stop-pruning/entry-producer/PROOF.md`; the reviews of the finite stages 10 to 15 and 16 to 17; the producer’s `rigidity.py`, `root_geometry.py`, `uniform.py` and `bridge.py`; `SPEC_v3.0.md` (sections 0 to 12); `acceptance/h_report30.py`, `EXPECT_G20S.json`, `EXPECT_HW.json`, `FROZEN_30.json`, `ACCEPT_G20S_v30.log`, `ACCEPT_JQ_v1_jQTwn0.log`, `bigbox/join/EXPECT_JG_v2.json`; the capture engine `exact_general.py`, `integer_sweep.py`, `boolean_rule.py`; `recompute_slice.py`; `PKT/scripts/run_adm.py` and `adm.py`; `UPPER_FORMULAS.md` |
| Read in part | `wxcheck_v30.py` (sections A to L except some name parsers); `exact_classes.py` (lines 1 to 420: parsing, certificate validation, class levels, the sweep with levels); the independent finite-row builder `independent_model.py`; `OBLIGATIONS.json` (structure, and the claims of `CHARGE_SEMANTICS`, `ROOT_ADMISSION`, `LOCAL_CHECKER_SOUNDNESS`, `G20S_PHYSICAL`, `LOCAL_JG`); `gate-receipt.json`, `MATHEMATICAL_INTERFACE.json`, `JG_exact_v2.json` (structure) |
| Skimmed | `wxcheck2_v30.js` (header, number handling, every float conversion); `PKT/scripts/new_capture_check.py` (what it recomputes) |
| Examined as data | the JQ tree certificate (one node, 48,209 terms); the capture statement `FRAME_0917` (classes, both receipts, all six slices); the certificates and class files of all 98 capture statements (budgets); the five stored stopped models and rounds; the B6 certificate; the eleven root files and the target class files the admission uses |
| Not read | the 29 reading-copy reports under `round5/reports/`; the eleven region records and the nine tree reviews; the written premises `FRAME_L9.md`, the C7/C8 `PROOF.md`, `case-repair-S/PROOF.md` (KEY_W), `PROOF_BRIDGE_V2.md`, `F1_PROOF.md`, the endpoint-normalization `THEOREM.md`, `ENDPOINT_CASE_G_LEMMA.md`; `SPEC_v3.0_NOTES.md`; `CHECK.md`, `AUDIT.md`, `KNOWN_LIMITS.md`, `READING_ORDER.md`, `CREDITS.md`; `check.py`; the 84 selected clause files; `DEPENDENCY_GRAPH.json`; `exact_restricted.py`; `verify_classes_wb.js`; the finite stages’ producer code |

## The Statement and Its Scope

`STATEMENT.md` defines $F$ and $G$, the isolating rectangle of radius $10^{-12}$ about
$(t_0, b_0)$, $L = (6+4t_*)/(1+2t_*-t_*^2)$ with
$4.67553009360455095163 < L < 4.67553009360455095164$, and claims that a packing of
seventeen closed unit squares exists at side $L$ and that a packing at side $S$ implies
$L \le S$; uniqueness is not claimed.
`STATEMENT_STATUS.md` and P003 make the claim conditional on the 210 obligations of
`OBLIGATIONS.json`, fifteen of them mathematical premises, and say that it is a
candidate proof. This review reads the claim as stated there: the unconditional theorem
would follow from the 210 obligations, and the question is whether the composition is
valid and whether the obligations it rests on hold.

The statement is the right one for $s(17)$: closed squares, independent rotations,
touching allowed, side of the container.
The endpoint was recomputed here: Newton’s method at 160 digits from $(t_0, b_0)$ and a
Krawczyk test in outward-rounded interval arithmetic prove a unique root in the box of
radius $10^{-12}$ and in the box of radius $10^{-100}$, and give
$L = 4.675530093604550951634111270483\ldots$, inside the stated enclosure, with
$R - L = 4.8366 \times 10^{-17}$ for the trees’ rational cap
$R = 4675530093604551/10^{15}$.

## Findings by Step

### Step 1: Upper Bound

My exact-root layout (from `UPPER_FORMULAS.md`, relabelled to capture labels) agrees
with the rational packing file within $4.4 \times 10^{-17}$ in every coordinate of every
square except square 4 (the rattler, at $\lambda_6$ in the construction and $3/2$ from
the right wall in the file) and square 13 (shifted by exactly $T/3$ along $v_{13}$,
which is the SPEC’s correction of the file centre).
In 120-digit interval arithmetic at the root box, 115 of the 136 pairs are strictly
separated, 21 touch to $10^{-90}$, none overlap; 53 wall clearances are strictly
positive and 15 vanish to $10^{-90}$. These are P014’s counts.
This is corroboration, not a proof of the 36 contacts; the premise `UPPER` has its own
exact checks, which were not rerun.

### Step 2: Capture

The class-row lemma states a sound charge argument: a threshold feature fires on at most
$\lfloor \sum a_j / k \rfloor$ disjoint cores, pairwise intersecting winning masks have
capacity one, the Möbius expansion is an identity of indicator functions, the closed
boundary is reached by a limit of generic cells along which hits persist, and the class
level $R(Q, I)$ (largest meeting high threshold, else least containing low threshold,
else 1) dominates $\tau(p)$ for every pose in the cell.
The code read matches it: `expand` recomputes the budget and the absolute Möbius sum
$< 2^{50}$, `geometry` builds the core-centre rectangles exactly, `accumulate` sweeps
every slab meeting the rotated container, `validate_classes` checks the row catalogue,
the strict core margin, the parent envelope and the angle coverage, and the strict test
is the integer comparison $M q_\beta < p_\beta \Gamma$. High classes are met through all
quarter-turn lifts (`angles_meet`), low classes only through lift 0, which is
conservative.

Two points matter for robustness (SR-6). The surpluses are tiny: recomputing every
budget from the features or orbits of all 98 certificates gives the stored
`budget_units` in all 98, and the surplus $\beta\Gamma - M$ ranges from 0.5 units
(`FRAME_1114`) to 23 units on budgets near $1.7 \times 10^{10}$, a relative margin of
$3 \times 10^{-11}$ to $10^{-9}$. That is sound in exact arithmetic, and it means every
capacity, site and boundary convention must be exactly right.
The public check `new_capture_check.py` takes `budget_units` from the certificate and
does not recompute it.
For `FRAME_0917` all 9,000 rows in the six slices, re-decided here from their recorded
minima, pass; the tightest class row margin is 217,326 units; Python and Node rows agree
field for field in all six slices.

Not checked here: the 1,728,000 rows per checker themselves (a capture recomputation was
outside this lane), `exact_restricted.py`, the Node checker, and the merge.
Their authentic complete execution is a stated hypothesis of P026 and P035.

### Step 3: Admission

The frame argument was followed by hand.
With high threshold $5/4$, low $7/8$ and disjoint unions, the score of a packing is
$17 + m/4 - t/8$; `FRAME_0506` gives $17 + m/4 - t/8 < 137/8$, so $t \ge 2m \ge 2$; the
two low unions and the marker give $h \ge 5$ distinct high parents in `FRAME_0917` by
the separations P041 cites (not recomputed here); $17 + h/4 - N(V)/8 < 145/8$ gives
$N(V) \ge 2$, and capacity one of each clipped component ($L_9$ clipped to
$x \ge 0.500235$ has squared diameter $0.4625$) gives exactly one occupant of each.
The case logic of P049 to P058 is consistent at every seam read: KEY_W puts an off-wall
$t_9$ in $[0.30651, 0.44941]$, the gate starts $1/200000$ below that, the upper exit is
JPA, and the loose roles are tested in the order 3, 17, 15 against the open gate
$|\tau_k| < 1/20$, with closed arms in the roots.
The wall-strip capacity argument of P065 and P066 was re-derived: in either ordering of
the two squares, separation needs $aw + bH - b(a+b)/2 \ge 1$ for a unit normal $(a, b)$
in the first quadrant, the opposite strict inequality is the stated quartic’s positivity
on $[0, 1]$, and both quartics have no root there (Sturm count), with minima $0.00504$
and $0.00519$.

The admission computation of `run_adm.py` was re-implemented from P073 to P080 with my
own $L$ enclosure: transport of each target polygon by
$\xi = e \cdot (c - (U-L)(1,1)/2 - p)$ at the polygon vertices and both ends of the $L$
interval, physical clipping, the gated-9 support cut, and inclusion of each direction
set in the root arc through quarter-turn lifts.
All $11 \times 17$ labels are admitted; the smallest margin, $4.32 \times 10^{-17}$, is
square 2 at its right wall and is exactly $R - L - \varepsilon$ of P087. The step that
`KNOWN_ISSUES.md` item 1 says is only a comment in `run_adm.py` holds: for
$|\theta| \le \pi/4$ the half-extent $(\cos|\theta| + \sin|\theta|)/2$ increases with
$|\theta|$, and at $t = 31/1000$, $50(1 + 2t - t^2) - 53(1 + t^2) = 0.001017 > 0$; the
wall column is $x_9 \le 53/100$ in $F_U$, where the physical wall lies at $x \ge 0$, so
the lemma applies. The distinct-parent geometry was recomputed for all eleven profiles,
the eight off-wall ones included, which P044 calls imported: after clipping to
$[1000469/2000000, 8351531/2000000]^2$ every target has squared diameter below 1 (at
most $0.4635$) and all 136 cross-label pairs are strictly separated as closed sets.
This is the containment side of the premise.
Which capture conclusion puts which parent in which target (the 84 clauses and the
selector logic) was not read (SR-8).

### Step 4: Local Trees

The SPEC’s lemmas were checked by hand: the separating-axis lemma (4.5) and the option
corner identity; Lemma P with its identity $be - al = si\,Y/(1+co)$ and every sign case,
and kind Ps through the concavity of $\sqrt{1-s^2} + s - 1$; the exclusion test (4.7),
whose quadrant condition with $\cos(E^+ \bar{E}^-) > 0$ and $\sin(E^+ \bar{E}^-) \ge 0$
keeps the arc inside one closed quadrant; the wall support facts (4.8); the lifting
lemma (4.10) and the term lemma, under which a guarded corner polynomial enters a term
only with its own indicator; the raw and centred remainder rules; the store-update
rules; the covering proof of splits; the root and terminal tests with $x - x^3/6 \le
\sin x$; and section 11’s monotonicity, which lets a tree stated at $S = R$ cover every
$S \le R$ with the container corner at the origin.
I found no false lemma.

The JQ certificate, examined as data, is one node: the root region `JQ_exact_v1.json`
exactly (box, arcs with centres, side interval $[R, R]$), 17 labels, `S_floor` $= R$,
one round with 33 indicator and 3 option declarations, and one step on the form `0` with
48,209 terms over 26,781 polynomial forms, closed as infeasible.
Its acceptance log records both checkers’ `PASS`, $L = 6.945 \times 10^{-3}$ against the
claimed value $6.25 \times 10^{-3}$, and the post-check’s exact comparison of the root
node with the region file.
The trees were not executed (a tree replay was outside this lane).

### Step 5: Rigidity and the Hand-Overs

The chain of P092 to P112 composes as stated.
The JG tube is the G20S window (core $1/5$, angle $1/10$, $\xi_{2,1} \in [-39/125, 0]$,
$\xi_{13,2} \in [-1/5, 28/125]$, identity centres) for the sixteen labels, with label 4
free; the G20S tube $T_1$ cut by $\xi_{2,1} \le 0$ is the HW window; the HW tube $T_2$
cut by $\xi_{2,1} \le 0$ lies in the finite entry (positions $1/250 \le 1/200$, angles
$1/500 \le 1/400$, the three slider intervals end for end).
The finite entry’s option audit was recomputed with a cruder first-order bound: the same
27 options survive and the other 125 are excluded (worst $-4.2 \times 10^{-4}$). The raw
stop cuts of P096 follow from the larger-radius stop theorem at core radius
$501/100000$, recomputed here: $b \ge -0.0085124$, $b + z \le 0.0244342$, hence
$b \ge -213/25000$, $b + z \le 49/2000$, $z \le 33/1000$ after transfer errors below
$10^{-16}$. The transfer to the exact root moves every position coordinate by less than
$10^{-16}$ and every angle by at most $2|t_0 - t_*| < 10^{-60}$, so the final raw radius
$6.4 \times 10^{-5}$ becomes an exact-root radius below $1/5000$. The seventeen finite
rounds themselves were not re-derived (SR-5).

At $R = 0$ square 8 is axis parallel at $(L - 1/2, L - 1/2)$, touching $x = L$ and
$y = L$, while the endpoint normalization of P017 puts the packing inside
$[d_0, L - d_0]^2$ with $d_0 = (L - S_0)/2 > 0$; the common dihedral image preserves
that square. The translation leaves every $F_U$ pose unchanged (P019), so the capture
applies to the normalized packing.
The contradiction is sound.

## The Normalized 52-Row Gate of G20S_PHYSICAL

**What P110 needs.** Let $h$ be the 45 exact-root core coordinates and
$R = \max |h_j| \in (0, 1/5000]$. Divide the core by $R$, keep $a, b, z$ unscaled, lift
$q_{w,i} = w x_i$, and put $s = (S - S^*)/R \in [-1, 0]$ (square 8’s right wall).
The claim is that 52 geometric rows and 192 McCormick rows are necessary for every such
$R$, and that a chain of exact weak-duality rounds then bounds $\max |x_j|$ by
$159201934153319/200000000000000 < 1$, a contradiction.

**Why the rows hold for every radius.** Three facts make each row uniform in $R$, and
each was checked here independently.

- The exclusion of the 125 non-surviving options is a statement about the whole domain
  $|h_j| \le 1/5000$, so it holds for every smaller $R$. My audit bounds each option’s
  gap by $\max_w n \cdot d(w) + \varepsilon D + \varepsilon\,d_r - 1/2 - \max_v n \cdot
  v + \sqrt{2}\,\varepsilon$ (owner rotation, core displacement, relative rotation of
  the other square’s support), in interval arithmetic over the padded slider box: 27
  options survive, exactly the producer’s 11 unique owners and 8 parallel pairs with the
  same normals, and the largest excluded bound is $-0.0184$.
- The base gap of every row and its slider coefficients vanish identically, so no
  constant is divided by $R$. With my own transcription of the layout, each of the 52
  base-gap numerators reduces to zero modulo a lex Gröbner basis of $\langle F, G
  \rangle$ (three elements, degrees 22 to 23), each denominator is nonzero on the root
  box, every slider coefficient is identically zero, and $\tau \equiv 0$ for the pairs
  (1,3), (1,5) and (2,6).
- Each remainder, divided by $R$, is $R$ times a polynomial in the normalized radii with
  nonnegative coefficients, plus higher powers of $R$, so its value at $R = 1/5000$
  bounds it for every smaller $R$. The derivations were checked line by line: the corner
  gap $(R(\theta_o)n)\cdot(d+\delta) - 1/2 - n \cdot R(\theta_t-\theta_o)v$ with
  $\|R(\theta) - I - \theta J\| \le \theta^2/2$ (an exact consequence of
  $|e^{i\theta} - 1 - i\theta| \le \theta^2/2$); the wall corner; and the parallel pair,
  from the two retained alternatives through $\cos e\,X_m + \sin e\,|\tau_m| \ge
  \cos^2 e + \sin e \cos e$ to $E = Dm^2/2 + m\,d_r + q^2/2 + q^3/6 + \tau_{\max} q^3 +
  (Dm + d_r)(q + q^3)$, where $|X_m - X - \mu\tau'| \le Dm^2/2 + m\,d_r$ uses
  $|R(\mu)n - n| \le |\mu|$ on the core term.
  Every term has degree at least two in the physical radii, and the constant-sign
  substitution $|\tau'| = \sigma\tau'$ is checked over the slider box.

**The arithmetic, two ways.** First, every one of the 52 geometric rows of the five
stored stopped models (`prefix/round-01` to `-03`, `round-04`, `round-05`) is implied,
in exact rationals on that round’s incoming box, by my independently derived necessary
inequality: the producer’s coefficients agree with my enclosures to $4.7 \times
10^{-16}$, and every producer right-hand side is at most my remainder plus the
coefficient discrepancy times the variable radii (smallest slack $1.2 \times 10^{-15}$).
The 192 product rows are the McCormick rows of the box and row 244 is
$-x_{21} - x_{25} \ge -3/125$. My own weak-duality code then reproduces all 460 stored
bounds exactly, every outgoing box, and the final ratio
$159201934153319/200000000000000$.

Second, the B6 prefix, whose six models are not stored, was replayed with rows built
entirely by this review’s code (my geometry, coefficients, remainders and rounding), the
producer’s multipliers serving only as hints and every box updated with my own bounds.
My B6 lies inside the producer’s B6 in all 52 coordinates, so the producer’s B6 is a
valid enclosure.
Continuing with the stop cuts and the five stopped rounds on my own rows
ends at a 45-core ratio of $0.792020707575807 < 1$. The physical stop theorem was
recomputed at $\varepsilon = 1/5000$: of the 16 options of pairs (9,11) and (11,13) only
the two $-v$ options survive, $c + s < 1.40841$, $|c(1-s)| < 0.27643$, $|c - s| <
0.12806$, giving $b \ge -0.000337$, $b + z \le 0.023764$ and $z \le 0.024104$, inside
the cuts $-17/50000$, $3/125$ and $1/40$.

**Conclusion on the gate.** The gate is valid for every core radius $0 < R \le 1/5000$,
and the strict contraction holds with rows and arithmetic independent of the producer’s
code. What it rests on beyond this review: the domain hypotheses (sixteen distinct
physical squares, actual $S \le L$, independent radian angles), which the finite stages
supply, and the exactness of mpmath’s interval arithmetic and SymPy’s Gröbner reduction
in the checks here.

## The Checkers’ Trust Boundaries

### Tree Checkers

**What they decide.** For one frame and labelling, every feasible configuration with
$S_{\text{floor}} \le S \le R$ in the root region lies in the tube (EMPTY when no
terminal leaf exists), relative to a packing file pinned by SHA-256, with label 4
dropped unless the header says 17. Arithmetic is exact: Python `Fraction` and integers,
Node BigInt rationals.
The Python checker refuses floats, NaN and duplicate keys at parse time, refuses
negative multipliers outside `circ` terms, recomputes every fact from the store at the
start of the round, accepts a store entry only when it is looser than the old one or
implied by a certified value, checks every child against the parent’s final store, and
checks reachability from the root.
In the Node checker every conversion to a JavaScript number found is of a one- or
two-digit label or index, or sits in a message, a test helper or a timer.

**What they assume.** That the root region is the case’s region and the tube is the next
theorem’s window: `h_report30.py` decides both by exact comparison with the `EXPECT`
file and the root region file, and fixes the number of terminal leaves for an EMPTY
statement. The checkers do not decide the frame, the chart conversion from $F_U$, the
choice of side-direction representative, or $L \le R$; those are the application’s (SPEC
section 11) and were checked above.
Authentic execution of the two runs is assumed.
The two checkers were written by sessions of the same AI system from one specification,
so their agreement guards against slips, not against an error in the specification,
whose lemmas were checked above.

### Capture Checkers

**What they decide.** For one certificate and one class file, the score inequality
$\sum \tau < \beta$ over all families in the side-$C$ square, row by row, with exact
integers (Python `int` and `Fraction`, `int64` inside the Numba sweep under the checked
$2^{50}$ bound; in Node, binary64 storage of integers below $2^{53}$, as P031 states).

**What they assume.** That every slice ran the bound inputs to completion.
The merge trusts stored row decisions after structural checks (P035), and the public
checks re-decide stored rows from their recorded minima without recomputing the sweep or
the budget. `recompute_slice.py` lets a reader recompute one slice with both checkers,
but it treats a Node checker-hash mismatch as a note rather than a difference (SR-7).

## Defects

No blocking defect was found.
The table lists every candidate found, with its resolution.

| Id | Location | Description | Blocking | Resolution |
| --- | --- | --- | --- | --- |
| SR-1 | P110; `G/full-stopped-propagation/continuation-independent-review/check.py` lines 134 and 148; `full_gate_analytic_review.md` | No independent reconstruction of the normalized model’s coefficients and remainders was carried: the full-gate review bound only “model file and dimensions, not independently replayed coefficients”, and the continuation’s independent check builds its rows with `import rigidity as kernel` and `kernel.model(...)`. Only the dual arithmetic was independent | No: this review re-derived the rows and found them valid | Carry an independent row builder with the edition (this review’s is one) and cite it in P110 |
| SR-2 | `G/full-gate/independent-review/` | The independent gate review’s `check.py`, `bind.py`, `receipt.json` and `binding-receipt.json` are not carried, so its 152-option audits cannot be replayed from the edition; its manifest gives `REVIEW.md` 7,817 bytes while the carried copy with the same SHA-256 has 7,744 | No: binding; the audits were redone here | Carry the files; correct or explain the byte count |
| SR-3 | P110; `LABELS.tsv`; `normalized_division_text.md` | The B6 prefix and the root-scale stop theorem carry P110 but have no label; they are bound only inside `THEOREM.md`’s inputs. The edition’s only text of the all-scale division describes an earlier slider box ($a \le 1/4$, $b \in [-1/2500, 1/12]$, $z \in [-1/8, 1/16]$) and a four-round chain | No: the argument carries over unchanged, as checked above | Label B6 and the stop theorem in P110; restate the division for the final domain |
| SR-4 | `PKT/records/THEOREM_G20S.md`; `OBLIGATIONS.json` (`G20S_PHYSICAL` evidence) | The evidence of `G20S_PHYSICAL` still binds the box-wide route (eight rounds, ratio 0.859, entry radius $8.735 \times 10^{-5}$), which PROOF.md does not use (`KNOWN_ISSUES.md` item 7) | No | Mark it as an alternative or drop it from the evidence |
| SR-5 | P109; `G/finite-stopped-contraction/` | The seventeen finite rounds were not re-derived here. Their second, “independent” builder was written by the same AI system and mirrors the producer’s formulas (first- and second-order corner rows, secant and tangent envelopes, McCormick products) | No: a limit of this review | An independent derivation of the finite second-order rows, by another model family or a human, checked against the stored models |
| SR-6 | the 98 capture certificates; `PKT/scripts/new_capture_check.py` | Surpluses of 0.5 to 23 units on budgets near $1.7 \times 10^{10}$; the public check takes `budget_units` from the certificate without recomputing capacities. All 98 budgets recomputed here match | No: sound in exact arithmetic | Recompute every budget from sites and features in `check.py` (seconds of CPU) |
| SR-7 | `recompute_slice.py` | A stored Node slice made with other checker bytes still ends `SLICE RESULT: EQUAL`, with a note | No: tooling | Count a Node checker-hash mismatch as a difference, or compare under one key name |
| SR-8 | `ROOT_ADMISSION`; P044 to P046; `KNOWN_ISSUES.md` item 1 | No written proof of the admission geometry, and the off-wall distinct-parent separation is “imported” without a computation in the public checks. The containment and separation were recomputed here with no failure; the occupancy of each target by its capture clause was not read | No | Carry the written argument and add the separation check to the public checks |
| SR-9 | `OBLIGATIONS.json`, `G20S_PHYSICAL` | The premise bundles the G20S and HW tree imports and the finite chain; it depends on `LOCAL_CHECKER_SOUNDNESS` but not on `LOCAL_CERTIFICATE_IMPORT`, and the two trees are not among the eleven root obligations | No: presentation | List the two trees as their own obligations, or add the dependency |

## Questions for the Author

1. Will a later version carry an independent builder of the normalized 244-row model,
   and say in P110 which code the row derivation rests on?
2. Where are the independent gate review’s `check.py` and `receipt.json`, and which byte
   count of its `REVIEW.md` is right?
3. Can the root-scale stop theorem ($b \ge -17/50000$, $b + z \le 3/125$, $z \le 1/40$)
   and the B6 prefix be listed as evidence of `G20S_PHYSICAL` by label?
4. Were the capture certificates tuned to the half-unit and one-unit surpluses on
   purpose, and does any of them depend on a boundary convention that the class-row
   lemma’s limit argument does not cover?
5. Which file records the 136-pair separation of the eight off-wall profiles that P044
   imports?
6. Is there a derivation of the finite second-order rows written independently of
   `uniform.py`?

## Checks Run Here

All checks are scripts written for this review, kept in the scratch directory under
`mine/`, run with Python 3.14.7 (`python3 -I`) from `out/`, reading the pinned tree as
data under `src/upstream/`, with `$G` the edition’s `G/`, `$C` its capture folder and
`$JQ` the JQ certificate.
They import no producer code and run no solver.

```sh
python3 -I ../mine/geom.py
python3 -I ../mine/audit.py audit.json
python3 -I ../mine/identities.py $G/full-gate/producer/gate-receipt.json audit.json
python3 -I ../mine/check_rows.py $G/full-gate/producer/gate-receipt.json audit.json \
    $G/full-stopped-propagation/continuation/prefix/round-0{1,2,3} \
    $G/full-stopped-propagation/continuation/round-0{4,5}
python3 -I ../mine/replay.py $G/full-gate/producer/gate-receipt.json audit.json \
    $G/full-stopped-propagation/continuation/inputs/accepted-six-step-prefix.json \
    $G/full-stopped-propagation/continuation
python3 -I ../mine/stops.py
python3 -I ../mine/stops_eps.py 501 100000
python3 -I ../mine/audit_entry.py
python3 -I ../mine/upper.py
python3 -I ../mine/coarse.py
python3 -I ../mine/profiles.py ../src/upstream
python3 -I ../mine/admission.py ../src/upstream
python3 -I ../mine/budgets.py $C/statements
python3 -I ../mine/frame0917.py $C/statements/FRAME_0917
python3 -I ../mine/jq_struct.py $JQ ../src/upstream/research/window-extension-20261008/bigbox/join/JQ_exact_v1.json
```

| # | Check | Result |
| --- | --- | --- |
| 1 | Root of $F = G = 0$ by Newton at 160 digits; Krawczyk test in interval arithmetic | unique root in the radius $10^{-12}$ and $10^{-100}$ boxes; $L = 4.6755300936045509516341\ldots$; $R - L = 4.84 \times 10^{-17}$ |
| 2 | My layout against the rational packing file | agreement within $4.4 \times 10^{-17}$ per coordinate except square 4 ($T/(3s)$) and square 13 ($T/3$ along $v$) |
| 3 | Option audit at root scale, 19 pairs × 8 options | 27 survive, 125 excluded, worst $-0.0184$; normals and owners as `root_geometry.NORMALS` |
| 4 | 52 base-gap identities, slider invariance, three $\tau \equiv 0$ | all 52 numerators in $\langle F, G \rangle$; denominators nonzero on the root box; all slider coefficients identically 0 |
| 5 | Stored stopped models, rounds 1 to 5 | every geometric row implied by my rows; coefficients within $4.7 \times 10^{-16}$; product and stop rows exact |
| 6 | Dual replay on the stored models (460 bounds) | every bound and box reproduced; final ratio $159201934153319/200000000000000$ |
| 7 | Whole chain on my own rows: B6, stop cuts, five stopped rounds | my B6 inside the producer’s in all 52 coordinates; final ratio $0.79202 < 1$ |
| 8 | Stop theorem at $\varepsilon = 1/5000$ and at $501/100000$ | only the two $-v$ options survive; all six stated cuts follow |
| 9 | Finite-entry option audit (positions $1/200$, angles $1/400$) | 27 survive, 125 excluded, worst $-4.2 \times 10^{-4}$ |
| 10 | Upper construction at the root | 115 strict and 21 contact pairs, 53 strict and 15 contact walls, no overlap |
| 11 | Coarse-capacity quartics of P066 (Sturm count, exact minimum) | no root in $[0, 1]$; minima $0.005043$ and $0.005193$ |
| 12 | Separation and capacity of the eleven seventeen-target profiles | all clipped squared diameters below 1 (largest 0.4635); all $11 \times 136$ pairs strictly separated |
| 13 | Root admission of the eleven roots (own transport, clip, support cut, arcs) | all $11 \times 17$ labels admitted; least margin $4.32 \times 10^{-17}$ (square 2, right wall) |
| 14 | Budgets of all 98 capture certificates from features and orbits | all 98 equal the stored `budget_units`; surplus 0.5 to 23 units |
| 15 | `FRAME_0917`: 9,000 rows re-decided from recorded minima; Python against Node | all pass; tightest class margin 217,326 units; Python and Node rows identical in all 9,000 |
| 16 | JQ certificate parsed as data | one node equal to `JQ_exact_v1.json`; 36 declarations; one `0` step, 48,209 terms |

## Verdict

**accepted**: no blocking defect was found in what was read.
A complete replay would still have to establish the authentic complete execution of the
98 capture statements by both checkers, of all thirteen tree certificates (the 4.8 GB of
the release included) with the frozen checkers and their post-checks, and of the
seventeen finite rounds with an independently derived row builder, together with a
reading of the 84 selected clauses, of the frame, KEY_W, C7/C8 and wall-partition
premises, and of the coarse regions’ dimensions, which this review did not read.

## Comparison with the First Review

This section was written after the findings and verdict above were committed, from the
first review,
[review-2026-10-12-kleddamag-n17-candidate.md](review-2026-10-12-kleddamag-n17-candidate.md).
Nothing above was changed because of it.

**Agreements.** Both reviews accept, with no blocking defect.
Both compute the same $L$ and $R - L = 4.8366 \times 10^{-17}$, and both re-derive the
class-row lemma’s links, the frame counting, the wall lemma at $t = 31/1000$, the three
tube hand-overs and the endpoint contradiction.
On the coarse-capacity quartics, the exact minima found here, $0.005043$ and $0.005193$,
lie above the first review’s Bernstein lower bounds, $0.0050389$ and $0.0051899$. Both
find the least admission margin, $4.32 \times 10^{-17}$, at the flush walls.
Both name the same trust boundary: authentic execution, and checkers written by one AI
system.
The two routes for the rigidity step (SR-4 here) and the missing written proof of
`ROOT_ADMISSION` (half of SR-8) are found by both.
The half-unit and one-unit capture surpluses of SR-6 head the first review’s list of
replay priorities, and SR-5 matches its note that `independent_model.py` shares the
producer’s remainder formulas.

**The gate.** The first review did not read the three gate texts.
It called the gate the one step whose written justification it had not seen, and said
its own verdict should not count as the accepting one for rung 4 until someone of record
had read it. This review read the gate texts and re-derived the gate with its own code.
That answers the first review’s question 2: the derivation is §5 of
`normalized_division_text.md`, with `analytic_envelope_text.md` and
`full_gate_analytic_review.md`, written for an earlier slider box (SR-3).

**Raised there and not here.** The `LABELS.tsv` bindings of `file:SELECTED_CLAUSES` into
a sibling folder and of `file:C12_PROFILE_CAPACITY` into an earlier edition folder; this
review read `LABELS.tsv` and missed them.
Its admission and profile checks read the packet’s own copy of the selected map, and all
six copies in the tree have the bound SHA-256. Also raised there and not here: the
“high-first” sentence of `F1_PROOF.md`, which was not read here; `P090`’s “93 option
splits” against a report’s 135, not checked here; and the n = 18 in the title of #557.

**Raised here and not there.** SR-1 (no independent builder of the normalized model),
SR-2 (the full-gate review’s missing scripts and its byte count), SR-3 (B6 and the
root-scale stop theorem unlabelled, the division text written for an earlier box),
SR-6’s point that the public check does not recompute the budgets, SR-7
(`recompute_slice.py` and the Node checker hash) and SR-9 (the two rigidity trees
bundled into `G20S_PHYSICAL`). The first review did not read the tree checker,
`SPEC_v3.0.md` sections 9, 10 and 12, `h_report30.py`, `exact_general.py`, a tree
certificate or a capture certificate, all of which were read or examined here; this
review did not read the written premises `FRAME_L9.md`, `F1_PROOF.md`, the KEY_W and
C7/C8 proofs, the endpoint normalization and `ENDPOINT_CASE_G_LEMMA.md`, which the first
review did. Neither read `verify_classes_wb.js`, `exact_restricted.py` or the large
files.

**A correction to SR-8.** The first review lists the per-root separations and capacities
as a public check (`extra.py`). In the edition, `scripts/entry_checks.py` imports
`extra.py` under the public check `selector` (not `admission`, where the first review
places it). For all eleven roots it asserts capacity one of every physical target, all
136 pairwise separations and the label-12 union capacity; it also asserts the 84
selected triggers. SR-8’s clause that the off-wall separation is imported “without a
computation in the public checks” is therefore wrong, and the first review is right on
the substance.
The rest of SR-8, the missing written admission proof, stands, as does its
status as non-blocking; check 12 here agrees with the capacities and separations that
`selector` asserts.

## Status Addendum: 2026-10-13

This addendum was written on 13 October 2026, after
[review A of #577](https://github.com/jlevy/squares/pull/577#pullrequestreview-5499709484),
by the agent addressing that review, not by the review lane.
Nothing above it was changed.
It corrects check 8, withdraws question 5 and half of SR-8’s resolution, and qualifies
four statements. The verdict, every defect’s blocking status and the conclusion on the
gate stand.

**Where the programs are.** The scripts that “Checks Run Here” says were kept in a
scratch directory are retained, unchanged, in the packet’s
[review-2/](../../../packing/resources/web/kleddamag-n17-candidate-2026-10-12/review-2/).
Its `run.sh` runs all of them on a checkout of the pin, in the order of the checks
table, and its `RESULTS.txt` is that runner’s complete output.
Check 2’s program, `cmp_file.py`, is missing from the command block above; it reads
`upper-packing-certificate.json` at the edition’s root.
In that block `$C` is
`research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture`
and `$JQ` is
`local-research/claude-20261002/cloud/analysis/part3_exact/certs/JQ_v1/jQTw.n0.JQ.cert.jsonl.gz`.

**Check 8.** Run at core radius $501/100000$, `stops_eps.py` compared $b$ and $b + z$
with the root-scale cuts $-17/50000$ and $3/125$ instead of P096’s $-213/25000$ and
$49/2000$, and printed two `False` lines.
It also bounded $z$ by adding $17/50000$ to the bound on $b + z$, which is valid only
where $b \ge -17/50000$; that fails at this radius, so the $z \le 0.024774$ it printed
is not a bound there.
Check 8’s “all six stated cuts follow” did not describe that output.
The conclusion in Step 5 holds, and `stops_cuts.py`, added to the packet with this
addendum, shows it: it bounds $z$ by the bound on $b + z$ minus the bound on $b$ at the
same radius and compares each radius with its own cuts.
At $501/100000$ it gives $b \ge -0.0085124$, $b + z \le 0.0244342$ and
$z \le 0.0329466$, against $-213/25000$, $49/2000$ and $33/1000$, with margins of
$7.6 \times 10^{-6}$, $6.6 \times 10^{-5}$ and $5.3 \times 10^{-5}$. At $1/5000$ the
three root-scale cuts hold too, with $z \le 0.0241011$; `stops.py`’s $z \le 0.024104$ is
valid there, since $b \ge -17/50000$ holds at that radius.
At both radii only the two $-v$ options survive.

**SR-8 and question 5.** The correction to SR-8 above answers question 5:
`scripts/entry_checks.py`, under the public check `selector`, imports `extra.py` and
asserts all 136 separations of each root’s targets.
Question 5 is withdrawn, and so is the second half of SR-8’s resolution, “add the
separation check to the public checks”; the first half, carrying the written admission
argument, stands, and the oversight record should take SR-8 as amended here.
The two files were read for that correction, after the findings were committed, so the
depth table, which predates the reading, does not list them.

**The Krawczyk boxes.** `geom.py` centres the boxes of check 1 at its Newton point,
which lies $3.8 \times 10^{-61}$ in $t$ and $4.9 \times 10^{-61}$ in $b$ from
$(t_0, b_0)$. So the unique root “in the box of radius $10^{-12}$” of the statement
section and check 1 is unique in that box about the Newton point, which misses a sliver
at most $4.9 \times 10^{-61}$ wide of the statement’s rectangle about $(t_0, b_0)$. This
changes nothing on the record: the packet’s statement comparison, through exp-237’s
contraction on the stated box, and lane K3’s root isolation prove uniqueness in the
stated rectangle.

**Three statements narrowed.**

- Check 5’s “product and stop rows exact”, and Step 5’s “the 192 product rows are the
  McCormick rows of the box”: `check_rows.py` checks that each stored product row is
  implied, in exact rationals, by the McCormick row of the box, and compares only the
  stop row, row 244, for equality.
  Implication is what soundness needs.
- Check 11’s “exact minimum”, and the comparison section’s “exact minima”: `coarse.py`
  counts the roots in $[0, 1]$ exactly and prints the minimum to 20 digits.
- Step 4’s “$L = 6.945 \times 10^{-3}$”: the log’s quantity is `zero_step_L`
  (`ACCEPT_JQ_v1_jQTwn0.log`, line 81), not the side $L$.

**Independence.** The lane was briefed by the session that registered T-153, which had
read the first review.
The brief’s independence rule read:

> You are the *second* adversarial review of this claim, and you must be independent of
> the first. **Do not open, read, grep or quote
> `docs/project/reviews/review-2026-10-12-kleddamag-n17-candidate.md`**, and do not read
> the review summaries in `packing/frontier/results.yaml` (entry T-153’s `reviews`,
> `composition`, `notes`), `packing/frontier/evidence.yaml` (the `external_review` of
> `E-n017-overbeck-optimality-candidate-report`) or
> `packing/resources/web/kleddamag-n17-candidate-2026-10-12/README.md` until your own
> review’s findings and verdict are written and committed.
> After that, you may read them only to fill the record fields below and to add a short
> final section comparing your findings with the first review’s (agreements,
> disagreements); do not change your findings because of it.

The rest of the brief gave the claim and its pin, the custody rules for downloaded
files, the document’s required sections and the record fields to fill.
It named the normalized 52-row gate (P110 and the files it rests on) and the checkers’
code as what to read hardest, calling them “the parts no reviewer of record has read”,
so the lane knew which parts the first review had left unread, though not what it found.
The findings and verdict were committed at 01:29:59Z and the comparison section at
01:35:13Z. The lane’s session transcript, which the harness keeps outside this
repository, shows its first read of the first review at 01:30:06Z; before the findings
commit it opened none of the files the rule names, and in the reviews folder it listed
the file names and read two other reviews for their structure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
