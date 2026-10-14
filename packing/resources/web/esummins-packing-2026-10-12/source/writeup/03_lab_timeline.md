# The s(11) lab, in detail: the timeline, the stuck points, and the drawing loop

*Living document, edited in place. Written 2026-09-09 from the on-disk record (LOG.md, attempts/REGISTRY.md, the
coordinator's dated memory in `writeup/sources/lab_memory_log.md`, docs/budget.md, docs/residue_ledger.md,
docs/paper/outline.md). Every timeline claim carries an attempt id (A###) and a date; every mathematical claim its
status tag ([T] proved in the notes, [L] Lean-checked, [C] certificate-backed, [P] pending compute, [S] supported,
[M] measured). Quotations are verbatim from the record; where the record does not carry a sentence verbatim the text
says so and leaves a bracket for the PI to fill.*

## 0. What this document is and how to read it

This is the third of three documents about a laboratory that ran for twenty-five days (2026-08-16 to 2026-09-09) on
one desktop, with one human and one AI coordinator directing a stream of AI attempt agents, against a problem that
had been open since 1979: is 3.877083590022814 the smallest square that holds eleven unit squares, and is the known
packing the only way to reach it? `01_summary.md` says what was proved and why it matters in plain language;
`02_mathematics.md` states the lemmas and how they compose. This document is about the *process*: what was tried in
what order, what died and why, where the AI got stuck, what the human saw that unstuck it, what the human got wrong
and how the machine said so, and what the two together produced that neither would have alone.

It is written for people who study how AI systems and mathematicians work together. The PI's own statement of the
purpose (2026-09-09) is the brief for this document: "documentation of the workflow between us (how we use SVGs to
visualise situations so I can provide feedback/insight/checks that you fold back in, creating a fast, intuitive
iteration loop)", showing "how and why AI couldn't do it alone, and how I built systems to allow me to fill in those
gaps", and how the interaction produced "a composite greater than the sum of its parts".

How to read it. Section 1 sets the scene. Section 2 is the timeline, phase by phase, with a table per phase listing
attempts, verdicts and negatives; it is the reference the rest of the document points into. Section 3 is the
heart: one subsection per stuck/unblock episode, each in the same shape (what the AI was doing, the sign it was
stuck, what the PI saw and said, what changed, the measured effect). Section 4 describes the visualisation loop as a
system: the drawing rules and the misreading each one prevents, the galleries, the reading sheet, the status board,
cycle times. Section 5 is the honest division of labour with evidence. Section 6 puts numbers on the composite.
Section 7 is the status on 2026-09-09 at midday and what would justify the claim that the rest is compute.

Two conventions. "Kill" means a region of hypothesis space certified empty; a "node" or "cell" is such a region
with one or more squares conditioned to boxes of centre and tilt; "alive" means the relaxation could not refute it
yet. Nothing is called a success here that the registry does not record as done-success or a certificate PASS;
the attempts that failed are listed with the same care as those that succeeded, because the PI asked for that from
the start (2026-08-31: "appendices publishing every off-critical-path investigation (negative results as
first-class output)").

## 1. The setting

### 1.1 The problem

Pack n unit squares into the smallest square. s(11) was the smallest open case: Trump's 1979 packing (six uprights
and five squares at a common tilt of 40.18°) gives the upper bound 3.877083590022814, an algebraic number of degree
8, and Stromquist's 2003 lower bound 2 + 2·sqrt(4/5) = 3.788854 had stood for 23 years (A01, 2026-08-16). The lab's
target from the first week was not a better bound but the theorem: s(11) equals the octic root exactly, and the
packing is unique up to symmetry. The problem is continuous (eleven centres and eleven tilts, 33 coordinates plus
the side), so no finite case list exists in advance; every argument has to manufacture its own finiteness.

### 1.2 The PI

The PI is a recreational mathematician with a mechanical-engineering background, passing familiarity with higher
mathematics, and no professional research experience (docs/paper/outline.md §8). What the PI did not do: write a
proof, run a linear program, touch Lean. What the PI did do, per the record: choose the problem and the standard;
supply the load-bearing decomposition (§3.1); refuse prices; read drawings of configurations and say which square
can move where; and, when the AI's pictures were wrong, say so. The coordinator's memory file on 2026-09-05 records
the working characterisation: "The PI ... contributes most where spatial/physical intuition applies — the places the
AI is comparatively blind", and "Every breakthrough of the k0 week came from the PI looking at a concrete
configuration or a concrete enumeration of cases and seeing a move or a constraint the certificates and censuses
could not express. Abstract residue statements ... produced no traction; pictures and case lists did."
(`writeup/sources/drawing_rules.md`.)

### 1.3 The AI lab

The lab is a coordinator (Claude, in the role the record calls "advisor" or "coordinator") plus attempt agents,
one per attempt id. The division by model was set by the PI on 2026-08-26 and held to the end: "Both leads run on
Fable (PI: Opus hopeless at theoretical math; Opus/Sonnet subagents for coding only)" (LOG 2026-08-26). Theory
attempts (drain lemmas, basin theorems, the k0 reductions, the local certificate, the sideband lemma) ran on Fable;
chores (campaign shifts, galleries, corpus audits, verifier ports) on Opus; and after 2026-09-09 00:35 the rule was
extended to constructions: "RULE (PI): complex case-tree constructions go to Fable, not Opus" (memory log
2026-09-09). Traffic was terse by directive — one brief in, one report out, "detached compute, single blocking wait,
one final report" (LOG 2026-08-20) — and for the last two days agent messaging was broken entirely, so every
successor agent was briefed from disk (A174, A175 briefs: "Nobody can message this agent: everything it needs is on
disk").

The artefacts that made this workable: an append-only lab notebook (LOG.md, 7,834 lines by 2026-09-09); a registry
with one row per attempt carrying goal, method, status and a one-line outcome, where "done-negative" is a
first-class verdict with the reason recorded (attempts/REGISTRY.md, 192 rows); a residue ledger listing what is
left by family with a picture per family (docs/residue_ledger.md); one budget file that is the sole home of the
compute estimate (docs/budget.md); a dependency graph rendered as a scoreboard with colour = verification tier
(lean/depgraph.svg, `writeup/figures/lean_depgraph.svg`); and the galleries of §4.

### 1.4 The ground rules

Four rules were fixed early and never relaxed.

1. *Certificates only.* "PI STANDING DIRECTIVE: no 'trust me' steps — every compute step an exact certificate, ALL
   logic/theory in Lean" (memory log 2026-09-01). Every LP kill is an exact rational measure checked by a
   stdlib-Python verifier that shares no code with the emitter; every kill engine must fail to kill Trump (the
   "canary"); a float verdict is a measurement, never a result ("certification-in-the-loop, float classification is
   measurement-only", A38, 2026-08-28).
2. *Frozen verifiers.* `verify_case.py` (sha 521cb01f…) and `verify_param.py` (0c58485c…) were frozen on
   2026-09-04 and thereafter only ever copied byte-identical; new clauses went into versioned successors (v2 A117,
   v3 A135) that import the frozen file. Every attempt's close-out reports "frozen verifiers untouched".
3. *Lean deliverable.* The top-level statement is a Lean theorem with a named axiom roster that shrank from 16
   (A62, 2026-09-01) to 13 (A63) to 7 (A78) to 3 (A79, 2026-09-03); the 3.82 lower bound is an end-to-end Lean
   theorem (A64); the certificate checkers have Lean soundness proofs (A70, A75); two local certificates are kernel
   theorems (A139, 2026-09-07).
4. *n-general statements.* From 2026-09-06 every lemma is stated for general n where possible, and every worked
   example gets a line naming the lemma it instantiates ("the results of the s(11) proof are meant to be TOOLS that
   make solving unknown higher n easier", `writeup/sources/results-as-tools-for-higher-n.md`).

### 1.5 The machine and the cadence

One Windows desktop: i7-12700K (8 P-cores + 4 E-cores, 20 threads), 31.7 GB RAM, about six usable LP slots
(memory-bound), pagefile moved to a 100 GB file after a hard crash (memory log 2026-09-04). No cloud: the PI's
repeated refusal of cloud prices is itself an episode (§3.11). Interruptions of record: API session limits and OAuth
expiries that killed whole cohorts of agents on day one (LOG 2026-08-16, twice), a machine power-off mid-run
(A27, 2026-08-25), an OOM crash at nine workers (A29, 2026-08-26), a reboot on 2026-09-09 ~02:20 that killed
three running attempts and was recovered from disk state.

The cadence: 192 registry rows in 25 days; the busiest single day (2026-09-08) opened or closed A148 through
A167. Night shifts ran the trees while the PI slept (A123, A137, 2026-09-07/08); day shifts ran readings and
re-solves while the PI was reading pages. From 2026-09-08 the box was partitioned by the PI: "lab work confined to
the 16 P-core threads = logical CPUs 0-15 (affinity mask 0xFFFF); E-cores 16-19 are the PI's" (memory log
2026-09-08).

## 2. The timeline in phases

Each phase has a table: attempt, dates, what was tried, the registry verdict, and the one-line reason. Verdict
tags: CP = on the critical path of the proof as it stands; T = theorem banked; N− = a negative that redirected the
programme; N = a negative that closed a door. Where a phase's story is an episode in §3 the row points there.

### Phase I — foundations and the new bound (2026-08-16 to 08-20)

The lab opened with six agents in parallel and lost all of them twice to session limits on the first day (LOG
2026-08-16); the work survived on disk and was resumed. By the evening of the first day the lower bound had moved
for the first time since 2003.

| attempt | date | what was tried | verdict | one line |
|---|---|---|---|---|
| A01 | 08-16 | literature | done-success | bounds confirmed 3.788854 ≤ s(11) ≤ 3.8770835900228; no formalisation exists anywhere |
| A02 | 08-16 | reconstruct Stromquist's proof | done-success | not a pure point set but a case split; two errata; pure 10-point sets top out ~3.74 |
| A03 | 08-16 | Trump's packing exactly | done-success, CP | 60-digit coordinates, the octic, rational certificate, stdlib verifier |
| A04 | 08-16 | beat Trump by search | done-negative, N | 2,488 optima, Trump rediscovered 276×, nothing below; runner-ups 3.885618 and 3.886746 (both return in §3) |
| A05 | 08-16 | best 10-point unavoidable set | done-negative, N− | ceiling ~3.7505 < Stromquist: the point method is exhausted |
| A06 | 08-16 | Lean toolchain + checkers | done-success, CP | integer checkers; kernel-checked upper bound; Mathlib did not fit on disk |
| A07/A08 | 08-16..18 | covering-measure LP + exact verifier | done-success, CP | **s(11) ≥ 3.80, then 3.81, then 3.82** (7.6 M boxes, 107 s); ceiling τ*(3.83) = 11.000 |
| A09/A11 | 08-18 | angle-lattice MILP (PI idea) | finder yes / certifier no, N | finds Trump ab initio in 23–39 s from two angles; bound stuck at √11; no beat for any n ≤ 100 |
| A10 | 08-18 | angle-box LP sizing | sizing yes / B&B no, N− | mid-tilt band never dies: a ¼-weight fractional pinwheel holds τ = 11 at every box size |
| A12 | 08-18 | region-rank cuts | done-negative, N | every macroscopic region is integrally loaded; cuts are escaped by sliding |

Negatives that mattered: A05 closed the classical route; A10/A12 identified the adversary that recurs for the whole
lab — a fractional packing with quarter weights that no single-square relaxation can price. The AI's first
tendency of record appears here: the 3.82 bound "read as a finish line; the PI's standard was the theorem"
(outline §7).

### Phase II — trees at 3.84 and the pivot to optimality (2026-08-18 to 08-26)

| attempt | date | what was tried | verdict | one line |
|---|---|---|---|---|
| A13/A14 | 08-18 | case-LP branch and bound at 3.84 | done-negative, N− | three oracle bugs found (every hypothesis-node τ was an under-estimate); fixing corners never kills; 10⁵–10⁶ LPs |
| A15/A16 | 08-19 | Lovász ϑ′ on placement graphs | done-success (pilot) | ϑ′ kills every node the LP cannot, on graphs; not a bound on s(11) |
| A17–A20 | 08-19 | continuum kernel certificates | done-negative, N, with a theorem | A18 collapse theorem: every pair-free kernel class ≥ the LP value; A19 proved τ*(3.84) ≥ 11 exactly |
| A21 | 08-20 | structure at 3.88 | done-success, T | corner and side-zone occupancy certified above ŝ |
| A22 | 08-20 | local rigidity of Trump | done-success, CP | Krawczyk enclosure at 1e-50; every packing within 5e-4 has s ≥ ŝ |
| A23/A25 | 08-20 | the PI's wastage (dead-area) oracle and atlas | done-success, T | the integral pinwheel is dead at ŝ by area (4.5056 > 4.0318, exact); single squares strand ≤ 0.6 |
| A24/A27/A29 | 08-20..26 | composed tree at 3.84 | done-negative / PAUSED | 123/216 cells discharged, 179 certificates; A29 paused 08-26 as a fallback |
| A26 | 08-21 | the PI's wall-strip ledger | done-negative, N−, 3 theorems | counting works, charging dies on an exact zero (a flush wall square strands nothing) |
| A28 | 08-24 | Lean bridge lemma | done-success, CP | s(11) ≤ 3.877084 as a kernel-checked statement about ℝ² |

The pivot: on 2026-08-19 the PI observed that "3.84-lemmas are vacuous if Trump is optimal; proofs must live at
s′ = 3.877083590…" (LOG 2026-08-19), and on 08-26 asked whether finishing 3.84 was necessary at all; the answer
was no ("a container-side lower bound prunes no configuration cells of the exclusion program"), and A29 was paused
with its certificates on disk. It has not been resumed. The record bound stands at 3.82.

### Phase III — the endgame survey: six walls (2026-08-26 to 08-29)

Every route the AI proposed to the global theorem was piloted and priced, and every one hit a named wall. This is
the phase in which the AI worked mostly alone and produced mostly negatives.

| attempt | date | what was tried | verdict | the wall |
|---|---|---|---|---|
| A30 | 08-26 | critical-point exclusion as a coordinate cover | done-negative | c^33 ≈ 8e8 cells around every critical point; 1e5–5e7 CPU-h |
| A31/A32 | 08-26 | enumerate contact structures / B&B over partial structures | done-negative, N− | 4e29 structures; frontier ≥ leaves ~1e30; "any COMPLETE search that visits survivors of the current lemma set is dead" |
| A33 | 08-27 | tight variety; the PI's grain conjecture | mixed | grain conjecture refuted in range; **s(12) ≥ 3.90 certified** as a by-product |
| A34 | 08-27 | sparse SOS | done-negative, T | collapse theorem: any relaxation with cliques of m < n squares caps at s(m) |
| A35/A36 | 08-27 | the PI's escape-complex (semantic cells) | GO as tool | Trump's basin certified at radius 3.7e-3 = 7.56× A22, 12 minutes of compute |
| A37 | 08-27 | critical-point atlas | done-success, CP | 32 families collapse to 10 attractors; four A04 missed |
| A38 | 08-28 | far-field tree at ŝ | done-negative, N− | per-node LP decision cost at s0 is the wall: 0/60 nodes decided |
| A39–A42 | 08-28 | early certification, basin surgery, seam design, occupancy chain | mixed / NO-GO | Trump's basin grown to 6.55e-3; the occupancy family has zero forcing power (τ = budget exactly at every conditioning) |
| A43–A48 | 08-28..29 | bulk kills, FJ-Maxwell, interface charging, balanced wedges, corner majority, bridge cascade | negative, with theorems | the enumeration–certificate mismatch law and its seven faces |
| A49–A52 | 08-29..31 | flush-free critical-point hunts; span semigroups; two-field probe | mixed | 252/252 drains acquire flush; Prop 1: joint LPs over certified fields collapse to one |

The verdict the coordinator wrote on 08-26 after A30–A32 is the clearest statement of the AI's position at the end
of this phase: "The endgame s(11) = s* needs a family-kill mathematics that collapses the space itself ... not
better search." It did not have that mathematics. §3.1 is where it came from.

### Phase IV — the stratification (2026-08-29 to 09-01)

| attempt | date | what was tried | verdict | one line |
|---|---|---|---|---|
| A53 | 08-31 | **the PI's simple-square stratification (I-L20)** | done-success, CP | census 1110 tuples / 163 D4 classes; all k ≥ 7 empty; 32/33 k = 6 classes dead |
| A54 | 09-01 | the four stragglers | done-mixed | k ≥ 6 tier closed unconditionally; k5_11 and k5_16 characterised as "Trump's ghost with re-decorated boundaries" |
| A55 | 09-01 | k = 4 sweep | done-success, T | exactly sharp: a k = 4 class is empty iff contained in no open k = 5 class |
| A56 | 09-01 | s-parametric transfer to the whole window | done-success, T | 38/52 rows window-grade; the rest s0-only pending A61 |
| A57 | 09-01 | shadow trees on k5_11, k5_16 | running → paused/resumed repeatedly | the priced compute item of the lab; see budget.md |
| A58 | 09-01 | clear-corner teleport (CC-2) | done-success, T | k-maximal minimisers have every completable slot doubly met; k ≤ 3 corners are doubly crowded |
| A59/A60 | 09-01 | trump5 as a finite program | GO / running | residue contracts onto Trump at ratio 4.55 per level, lands in the basin at level 24 |
| A61 | 09-01 | window stragglers | running | converted 12 s0-only rows; k5_13 hung 40 CPU-h in an LP (§3.12) |

By the end of the phase "the ENTIRE remaining stratification problem localizes onto THREE k=5 classes — trump5
(provably alive, is Trump) + k5_11 + k5_16" (memory log 2026-09-01), plus every class with fewer pins, which the
k ≥ 1 machinery handles by containment, plus k0_00, the class with no simple square at all.

### Phase V — trust, Lean, and the k0 core (2026-09-01 to 09-03)

| attempt | date | what was tried | verdict | one line |
|---|---|---|---|---|
| A62/A63 | 09-01 | formal statement; hole closure | done-success, CP | 13 named axioms; three new HIGH holes found by writing the composition; Lemma B (λ-dilation) proved |
| A64/A68/A70/A75/A78/A79/A86/A93 | 09-02..04 | Lean waves | done-success, CP | 3.82 end-to-end in Lean; verifier soundness; census as a definition; roster 16 → 3 |
| A65 | 09-02 | Theorem U (one-square rigidity of Trump) | done-success, C | 11 re-insertion certificates PASS |
| A66/A71/A73/A74/A77/A80/A81 | 09-02..03 | pair certificates for corners4 | done-mixed, N− | a quantified verification wall: complete trees retain 0.75–0.86 per level; "PAIR-CERTIFICATE ROUTE CLOSED in this certificate form" |
| A67/A69/A72 | 09-01..02 | D4 rerun; the algebraic identity ŝ_A22 = ŝ; census clean-room | done-success | census independently re-enumerated and matched exactly; 12 definitional ambiguities pinned |
| A82 | 09-02 | side scan | done-mixed, T | the aliveness cliff is a step of exactly one at ŝ; first protected-class kills at 3.833212 |
| A83/A84 | 09-03 | contraction tube; protected trees | done-success, CP | tube reaches T = 0.0571 = the whole window at r = 6.5e-4; Lemma P-TREE |
| A85 | 09-03 | k0 route pricing (the PI's three cuts) | done-mixed, N− | 3,200–7,000 CPU-h; "NO ORDER-OF-MAGNITUDE CUT ALONG C1-C3" |
| A87 | 09-03 | DF-K0 (the PI's "derivative of s") | done-success, T | two-line proof in the selected form; H1 as a cover is astronomically dead |
| A88–A92 | 09-03..04 | FJ census, tilt floor, NOCRIT, frame census, blocked side | mixed | every count-based route to k0 dies; crowd certificate PASS only at depth 0.3 |

The PI's pushback drives this phase: the coordinator's 25–30 desktop-day quote for k0_00 (A84) was answered
with three cuts (A85), then with "the remainder must have exploitable structure" (memory log 2026-09-03, A87), then
with the diagnosis that emptied the whole corpus of "k0 critical points" (§3.11). None of it lowered the k0
price; all of it changed what the residue is (K0-BLOCKED: all four corners doubly met).

### Phase VI — the reading loop (2026-09-04 to 09-08)

The phase in which the drawings became the lab's main instrument. It begins with the shadow gallery and the PI's
sentence that organises it — draw the LP's dual support directly (§3.2) — and ends with 632 → 406 work-owing A57
nodes and a k0 residue of eleven converged-alive cells.

| attempt | date | what was tried | verdict | one line |
|---|---|---|---|---|
| A94–A99 | 09-04..05 | slot crowds, parametric emission, wall budget, exchange, k0 tree v2 | mixed | A96: parametric window certificates at 0.2 of one fixed side; A99: the "10× from three reductions" was never there |
| A100–A105 | 09-05..06 | protected-tier pricing; flood; rigidity drain; NOROOM; lock-free | mixed | tier 3,500–4,200 CPU-h; every K0-BLOCKED packing below 4 drains (A104: locks first appear at 4.000237) |
| A106/A107 | 09-06 | shadow diameter; **the shadow gallery** | done-success | 53 shadows explain 1,260 of 1,566 alive nodes; S02 = the PI's k7 pinwheel; S07 = a new exact minimum |
| A108/A122/A125 | 09-06..07 | S07, S33/S35/S38 exactly | done-success, T | S07 = 2 + 4√2/3 in Q(√2); S38 of degree 9; S33 smooth; basins certified |
| A109/A111/A112/A115 | 09-06 | crowd rows; load-path branching; region tree; corner rows | negative / mixed | rows re-price rather than forbid; "the k0 tree has zero logic kills today" |
| A113/A118/A121 | 09-06..07 | manifold distance; lane-count leaf; **reading validator** | mixed | all 18 `r` readings exactly right; 81/83 right panels are rearrangements, not snaps |
| A116/A119/A120/A126/A133/A134/A136/A138/A139 | 09-06..08 | the local certificate and its Lean closure | done-success, L | LocalDead for S07 and S02 as kernel theorems; 15 of 35 in-N nodes closed |
| A123/A124/A137/A149/A156 | 09-07..09 | night and day shifts on A57/A60 | done-success | 632 → 406 work-owing; exact-core re-solve certifies 28.6% of alive nodes; 180 kills for 46.7 CPU-h (A149) |
| A131 | 09-07 | **pin-clip** (from the Y0036 reading) | done-success | 132 recorded-open nodes clip to EMPTY in 4.1 s of CPU |
| A132/A135/A145 | 09-07 | **polygon core, exact cores** (from the Y0186 reading) | done-success | frozen verifiers take the core half-side verbatim — exact cores certifiable today |
| A140/A141/A143/A148 | 09-07..08 | k0 galleries v3/v4; K′ lane; corner-first root | mixed | s3_far certified dead; 47 k0 cells killed by the K′ lane; corner-first root not cheaper |
| A144/A161/A167 | 09-07..09 | **guard lines; chord-limited lane** (from Y0147, Y0842) | mixed | 86/448 supports violate a guard line; 27 + 11 new kills; 285 cells retired by exact two-crowd witnesses |
| A150/A154/A155/A159/A166 | 09-08..09 | four-corner product; R6 row; exact cell; near-miss joint; nearest-corner sub-tree | negative | the corner-first line closed from every side; the "free lunch" (C) leaf provably unavailable |
| A151/A160/A163 | 09-08 | the pinwheel basin as a union | done-mixed | first LIVE-LOW witnesses; the basin is a disjunction of boxes; transferred to k5_16 (52/54) and trump5 (42/54) |
| A152/A153/A157/A158/A164 | 09-08 | shrunk cell; cover number; undecided slots; slot split; wastage area | negative | five readings measured to their floor (§3.9) |
| A146/A114 | 09-06..07 | window closers | done-success | **the window layer is done: 52/52 rows full-window** |

### Phase VII — the cascade on l1_104 (2026-09-08 evening to 09-09 midday)

The current phase, and the test of the whole method on k0: take one converged-alive cell and force geometry to a
fixed point before any LP.

| attempt | date | what was tried | verdict | one line |
|---|---|---|---|---|
| A165 | 09-08 | the PI's cascade as an explicit case tree (Opus) | done-negative; **killed by the PI** at 00:35 | sound at every step; unclipped pair boxes drawn (§3.7); chain breaks at a shallow crosser |
| A168 | 09-09 | the cascade redone (Fable) | running → stopped 10:35 | every step a certified leaf; caught again unclipped at S2 (§3.7) |
| A169 | 09-09 | the PI's sideband lemma; Theorem B | done-success, T/L | sharp constant c; the lonely NO-family; Sideband.lean |
| A170 | 09-09 | certificate audit (the stock-core reversion) | done-success | 59 recovered PASSes; k0 prize zero; 46/161 rate unchanged |
| A171/A172 | 09-09 | the multibox invariant library; per-piece K′ | done-success | the clipping rule is now code with a guard; hull → pieces recovers a quarter of the clip (§3.7) |
| A173 | 09-09 | the lonely clip inside multibox | running | 13 of 146 A168 nodes killed by the clip alone (`notes/measure.md`) |
| A174/A175 | 09-09 | cascade takeover; the polygon-obstacle clip | running | A175: with polygon obstacles the recorded node root/D0/S1/B0 is DEAD (EmptyBox(H)) — pending re-normalisation of every node |

No k0 cell has been certified dead by the cascade as of 2026-09-09 midday. The eleven converged-alive cells stand
at eleven (docs/shadows/STATUS.md, generated 10:05).

## 3. The stuck/unblock episodes

Each subsection has the same five parts: what the AI was doing; the sign it was stuck (wasted compute, a wrong
reading, a false lemma); what the PI saw and said, quoted from the record; what changed; the measured effect.
The episodes are in date order except that the false readings (§3.9) and the process rules (§3.12) are grouped.

### 3.1 The stratification by simple squares (A53, 2026-08-31) — the load-bearing idea

*What the AI was doing.* The endgame survey of Phase III: six routes to the global theorem, each piloted with a
validated engine and each priced honestly at an impossible number. By 2026-08-28 the coordinator's own summary
read: "the s-hat far-field survey is COMPLETE, A30-A42 ... s(11) = s-hat requires an N6-class weapon vs the ghost's
equality manifold ... no known family works, each closed by an exact mechanism. Actionable now: A29 resume
(3.84), n=12 campaign, corpus write-up" (memory log 2026-08-28). The same three fallbacks — resume the 3.84 tree,
switch to n = 12, write up — recur in the coordinator's notes on 08-26, 08-27 (twice), 08-28 (twice) and 08-29.

*The sign.* The AI had proved the walls were real (the enumeration–certificate mismatch law, seven faces by A52)
and had no route around them. Its proposals for the next step were all retreats. Roughly 14 attempts in four
days had produced theorems and zero progress on the residue.

*What the PI saw and said.* On 2026-08-31 the PI proposed a decomposition of the whole configuration space by a
finite combinatorial label. The dispatch records it: "PI's decomposition: k = number of grid-locked doubly-flush
squares. Two leverages no prior branching had: skeletons are DISCRETE (exact rational grid slots, tiny census) and
non-Trump skeletons are F4-SHIELD-FREE; plus the measurable crux — the 1/4-ghost's power is built on full-box
symmetry, and residual-region LPs (skeleton pinned exactly, area deleted, L-shaped domain) have never been run.
Hazard flagged: k unstable under epsilon (near-grid squares strand ~epsilon) — patched by the k-maximality drain
selection" (LOG 2026-08-31). Note the shape of the idea: not a new certificate, but a way to make every existing
certificate stronger by pinning exact squares and deleting their area from the container; and note that the PI
flagged the soundness hazard (tolerance) in the same breath as the idea.

*What changed.* A53 (Fable) turned it into a census — the Young-form definition ("tiling grown in from a corner"),
1,110 skeleton 4-tuples in 163 D4 classes, k = 0..9, stable across the window — and ran the residual-region LPs.
"HEADLINE: residual-region guard LPs with EXACT skeleton pins break the 1/4-ghost. All 33 k=6 classes LP-dead
(typical tau = 4.000000 exactly = an integral 4-square blocking packing; 6 + 4 < 11)" (LOG 2026-08-31). The
adversary of A10/A12, the quarter-weight pinwheel that had held τ = 11 at every box size for two weeks, "is a
full-box-symmetry creature; residual regions kill it outright" (memory log 2026-09-01).

*Measured effect.* Within two days: k ≥ 7 empty unconditionally; 33/33 k = 6 classes dead (A54); 19/21 non-Trump
k = 5 dead; 8/14 k = 4 dead, exactly sharp (A55); 61 certified pin-sets covering every open class with k ≤ 4 by
containment. "THE TOP OF THE STRATIFICATION COLLAPSED, first decomposition where this ever happened" (memory log
2026-09-01). By 2026-09-07 all 52 stratum rows were certified on the whole window [3.82, s0] (A146). Everything
since has been about three k = 5 classes and the empty class k0_00. In the outline's attribution the idea is
listed first among the PI's contributions and called "the load-bearing idea of the whole proof"; the AI's part
was the definition audit (the PI's form was strictly stronger than the brief's, 1110/163 against 7204/944), the
census, the certificates and, later, the Lean definition (A78) and the clean-room re-enumeration (A72).
Generalises: any n; the census grows but is mechanical.

### 3.2 "Draw the LP support directly": the pinwheel shadow (A106/A107, 2026-09-06)

*What the AI was doing.* Running the A57 shadow trees on k5_11 and k5_16 and measuring their descent rates
(A96, 2026-09-04..06). The level-2 and level-3 rates kept moving as parents landed (1.54× → 2.76× → 2.43× →
2.36× → 1.55× → 1.11×); a fertility probe found that descent was clustered in a few parents (A96, 2026-09-06). The
AI's explanation was that a fertile box contains a local minimum and its proposal was a "basin switch": certify
a ball around each minimum and let the tree cover the complement.

*The sign.* A106 measured the premise and it was false: "none of the 145 open L2-L4 boxes contains a local minimum
(box-constrained min on the boundary; released flow leaves; median distance to a shadow square 0.32 = 9 r_basin)
... Boxes are alive because the LP relaxation ... cannot see the slack, NOT because they hold near-solutions"
(memory log 2026-09-06). The AI had been about to build basins around objects the boxes did not contain. The lab
law recorded from this: "an 'alive' box in a core-relaxed LP tree need not contain anything — check what the box
CAN reach before building basins around what it cannot."

*What the PI saw and said.* The PI asked for the LP's dual support at a fertile node, drawn as squares, and read
it: "PI read the A57 LP support and named the shadow: k7 packing = BL L-shape 3 + BR stacked 2 + TL 1 + TR 1 +
4-square PINWHEEL at one tilt (48.435 deg); direct SLSQP gives s* = 3.886746 = s-hat + 0.0097 ... A57's fertile
lineage Y0036 is this shadow" (memory log 2026-09-06). And the rule: "The LP dual support IS the shadow (PI: 'grab
the phase-space point near the dead end of the LP search') — draw it directly, not the hole witnesses." Figure:
`figures/pinwheel_k7_shadow.svg`, `figures/pinwheel_tilt_curve.svg`.

*What changed.* A107 (2026-09-06) drew the dual support of every alive node in the corpus, snapped it, released it,
and grouped the minima by value: "53 distinct shadows explain 1260 of the 1566 ALIVE-at-LP nodes"; S02 is the PI's
pinwheel (267 nodes, the whole deep tree); S01, half the alive nodes, minimises to a side of exactly 4.000 ("this
has room, not this is nearly feasible"); S07 is a packing nobody had seen, at 3.885618, which A108 proved exact the
same day (2 + 4√2/3, every coordinate in Q(√2), all five tilted squares at exactly 45° — the second-best known
packing of eleven squares). The gallery `docs/shadows/S01..S53.svg` (figures `gallery_S01.svg`, `gallery_S02.svg`,
`gallery_S07.svg`) became the object the PI reviewed; on 2026-09-06 the PI read S01–S06 at once ("S07 = Trump with
f0's corner no longer poking into the gap ...; S01 has a FREE CORNER -> already killed by the teleport lemma into
a higher-k class; ... S06 = the optimal n=5 packing (2+1/sqrt2) with a unit band = the s(10) optimum") and gave the
diagnosis that set the next week's direction: "the issue is turning teleport-lemma kills into kills in phase
space" (memory log 2026-09-06).

*Measured effect.* Two honest numbers. The per-node readings of the 83-page first pass produced 9 node kills, none
new (A121, 2026-09-07: all already found by A118's lane sweep; "a reading is a POINTER to a cell, never a fact about
the node"). But the pass's `i` rows — pages whose support had fewer than eleven squares — pointed at cells no queue
had reached, and 14 of 14 of them certified dead in A115's warm re-solve (2026-09-07), "seven of them level-1 cells
no queue would have reached". And the exact minima the gallery surfaced (S02, S07, then S33/S35/S38 via the PI's
2026-09-07 callout "S33/S34/S35 ... look FULLY LOADED") fed the local certificate A116–A139, which closed 15 of 35
in-N nodes (A136) and is a Lean theorem for two neighbourhoods (A139). The lesson the coordinator banked: "draw the
LP support directly at every fertile node (PI's rule) — it worked."

### 3.3 The Y0036 pinch and the Y0186 columns: pin-clip and polygon core (A131, A132/A135, 2026-09-07)

*What the AI was doing.* Deploying two geometric pre-filters at emission (T5′ tight core, T5″ tilt trimming,
A96 2026-09-06) and re-solving alive nodes at a 900 s cap (recheck96), which docs/budget.md ranked "the best
per-budget item on the board".

*The sign.* A124 (2026-09-07) graded the re-check by the campaign's own rule: "2 STRICT, 1 WEAK, 18 KNIFE ...
Fifteen CPU-hours rediscovered two known nodes and found no third. So docs/budget.md's ranking is backwards."
Meanwhile the trimming lever's live fire rate came in at 1.0% full kills against a projected 3.7% ("T5″ buys LP
tractability, not kills", A123).

*What the PI saw and said.* Two readings of two pages on 2026-09-07. On `k5_11_interior_Y0036` against the pin
bl10: "most drawn tilts are geometrically impossible at most centres" — checked exactly by the coordinator: "lower
half of the L1 box blocked at every tilt (tree logic-killed it); alive D2 bins feasible only in a top sliver ... the
mirror lean is impossible for the whole D02/D06 bin. T5″ cannot empty it (box corner survives)". On
`Y0186_D00_D00`: "a support column intrudes into every hypothesis pose" — checked: "in EVERY node 2 of the 5-8
weight-1 support columns overlap the hypothesis square at every pose (SAT gap -0.005..-0.029) yet clear the
AXIS-ALIGNED core K(a) by +0.003..+0.045; the tilted square protrudes ~0.21 beyond K(a) along the diagonals"
(memory log 2026-09-07). Figures: `figures/A131_pinclip_Y0036.svg`, `figures/a57_lp_support.svg`.

*What changed.* Two leaves, one per reading. The **pin-clip** (A131): shrink the centre box, per tilt sub-bin, to
the region where the conditioned square can clear each pin — four sinusoids in θ, rational in t = tan(θ/2), "no
epsilon at all"; it strictly dominates T5″ (all 159 of its empties plus 21) and, run over the stored corpus, "132
recorded-open A57 nodes killed by T5‴ geometry alone, in 4.1 s of CPU" (2026-09-07), 112 of them by a trim already
deployed but only ever run on new children. The **polygon core** (A132): replace the inscribed axis square K(a) by
K′(B) = ⋂ over the box of the hypothesis square, a convex polygon certified vertex by vertex; over 506 alive nodes
it excludes 22.3% of the dual-support columns carrying 35.7% of τ, and a quarter of that weight was the *pins'* —
the stored pin core half-side 0.49 against the exact 0.49293. A135 then found that "both frozen verifiers take the
core half-side a VERBATIM from the certificate and never recompute it", so the exact cores were certifiable with
no verifier change, no Lean change, and no re-verification of anything emitted.

*Measured effect.* The exact-core re-solve became the campaign's main lever: 46 of 161 decided alive nodes certified
dead (28.6%, A137 night of 2026-09-07/08, 15.5 CPU-h); A149's day lane drained the A57 ALIVE+FAIL population (93
kills) and trump5's (87 of 214, 40.7%) — 180 certified kills for 46.7 CPU-h; A144's control arm found "the
EXACT cores alone kill 15 of the 20, the deployed cores 0 of 6". Two drawing rules date from these pages: draw the
hypothesis square at the centre of its box and the centre of its tilt window, and draw all three cores of a
conditioned square in distinct styles (`writeup/sources/drawing_rules.md`, addenda of 2026-09-07). The ledger's
one-line summary: "Both leaks are the same lesson: use the exact pose set, not its axis-aligned shadow."

### 3.4 The pinwheel basin: f0's slide, the common-tilt grain, and the union (A151/A160/A163, 2026-09-08)

*What the AI was doing.* Growing the local certificate around S02 — Theorem LOCAL (A116): a neighbourhood N of a
known minimum is dead iff every leaf of a selection tree over the near pairs has chain minimum above s0 — one
coordinate at a time. A151 (2026-09-08) grew f1's box to ten times A116's volume with zero witnesses and concluded
"the limit is COMPUTE (wall caps), not geometry".

*The sign.* The basin's consumer count barely moved (72/32 → 96/42 of the 184 S02 nodes), and A151 had grown the
wrong square: "A151 grew f1 (compute-limited, no real packing found) but never f0 (forced-radius ordering)".

*What the PI saw and said.* Two readings on 2026-09-08, from the pinwheel drawing: "S02's f0: the basin should be
grown along f0's whole SLIDING SLOT (several contact graphs; a box hypothesis over poses does not care)"; and
"S02's second basin axis = the COMMON TILT of the grain f1/f2/f3 (A106's pinwheel tilt curve, min 3.886746 at
48.435 deg, rising both sides) -> cover it as a CHAIN of certified boxes along the curve (tilt steps ~2.5 deg,
centres moving with the tilt), f0's slide inside each" (memory log 2026-09-08). The PI's reading of the S02 panel, in the session transcript of 2026-09-08 (Claude Code session 8b20e315, not
copied into LOG.md at the time): "Doesn't that imply that the 10 square basin has universal coverage in the rattler
dimensions?" -- i.e. that a basin grown along f0's slide and the common-tilt grain covers every direction in which
the pinwheel can move without leaving the box hypothesis. The coordinator's answer and the chain construction above
followed within the hour.

*What changed.* A160 measured both directions exactly. f0 is a genuine rattler — "an exact one-parameter slide of
length 0.298419 along its own body axis at the fixed tilt 48.4351°, three contact graphs" — which is the PI's
diagonal slot exactly; but f3, which A116 had treated as "the strut", is the shadow's *most* load-bearing square
(Δs* 0.119), and BR(0,0) is a second rattler. Putting f0 into N as a fifth body was a net loss (consumers 96/42 →
15/8) and the tree capped. The common-tilt chain "works, is cheap, and buys almost nothing": 24 of 25 links certify
a 60°-wide shared-tilt range at a median 7 s a link, but its ceiling is the tilt *spread* of a node's support, and
f2's and f3's tilts bind independently. Independent per-square tilt slices certify "with zero failures in 348 s",
and then the load-bearing finding: the directions trade off — f2's upward slice with A151's grown f1 "is REFUTED BY
A LIVE-LOW WITNESS", a real partial packing of nine squares at side 3.869 < s0, "the first LIVE-LOW witnesses
anywhere in the A116 / A151 / A160 line". So "S02's basin is not a growable box but a UNION of differently shaped
certified boxes".

*Measured effect.* Consumers 114 of 184 in-N / 50 alive for ≈ 0.9 CPU-h of tree time (A160). A163 then carried
the union into the other two frames the pinwheel lives in — the PI's `k5_16_interior_Y1110` page had exposed that
every S02 certificate was in k5_11's frame — and measured the asymmetry: k5_16 52/54 certified (both refusals wall
caps), trump5 42/54 with nine live-low witnesses "because trump5 does not pin TL(0,0)"; consumers went from 0/0 to
38/21 (k5_16) and 3/3 (trump5) for 1.6 CPU-h. Rule banked: "a basin certificate is per (minimum, class frame) —
build it in every class frame the shadow appears in." What the AI could not have done alone here is the direction
of growth; what the PI could not have done is the witness that bounds it.

### 3.5 The corner-first tree and the doubly-met corner (A143/A150/A154/A155/A159/A166, 2026-09-07 to 09-09)

*What the AI was doing.* Pricing the k0_00 tree as A38's interior-first cover — 216 level-1 cells over a
fundamental triangle, one conditioned interior square per node — at 12,000 CPU-h (budget.md), and observing that
"the k0 tree has zero logic kills today (it never branches on corners)" (A113, 2026-09-06).

*The sign.* Every k0 cell that resisted did so at τ = budget exactly, converged, with a dual support that put a
single deep meeter in each corner (A115: "the room is always a single DEEP meeter, never an empty corner ... exactly
the K0-FREE teleport hypothesis"), and no row the AI could write charged it (A115, A154: the incidence rows
"price what the LP already wants to buy").

*What the PI saw and said.* On 2026-09-07 the PI proposed a different root: "the k0 tree already quotients D4 x S11
via an EXISTENTIAL interior-zone hypothesis ... The PI's alternative canonical choice = condition on the BL CORNER
INTRUDER (root lemma free for k0: K0-FREE dead by teleport, else every corner met by a tilted intruder; D4 -> one
corner). Wall-strong leaves (polygon core, clip, K′ lane) bite hardest there"; then the refinement "corner-first
root + DOUBLY-MET corner = condition on BOTH BL meeters ... pair cells nearly all geometry-killed (hook pairs
only survive)"; and a prediction: "ONE deep lineage = Trump's shadow entering via its single non-simple corner (TL
in trump5's frame; -> BL after D4); all other pair cells die" (memory log 2026-09-07). On 2026-09-08: "corner tree
v2 = condition on ALL FOUR corner intruders at once (K0-BLOCKED means all four met); each corner's band is narrow
... branch as a PRODUCT of band cells (D4 / 8)". The PI's reaction, in the session transcript of 2026-09-08 (Claude Code session 8b20e315): "holy fuck.... that
might actually be our 40x speed up" -- said of conditioning the tree on all four doubly-met corners at once, with
the candid follow-up in the same exchange, "Honestly I'm kind of mad neither of us noticed that until now". The
measured outcome (A143/A150/A154/A155, below) was smaller than the hope: the pad is a 2% effect, the four
conditioned corners buy LP slack, and the product branch priced out; the line closed as a tree and re-emerged as
the cascade of section 3.6.

*What changed, measured.* A143 (2026-09-07): the root is sound and the doubly-met geometry is real — "9,638 of
11,772 canonical pair cells (81.9 %) emptied by three exact prunes for 90 CPU-s" — but "a second conditioned
square at the SAME corner buys essentially no slack for a whole unit of budget" (η −0.08 at budget 9 against the
interior root's median −0.73), priced at 3,800–8,900 / 8,000–18,800 CPU-h against 12,000: "not cheaper". The PI's
identification of TL as Trump's one non-simple corner was "CONFIRMED", but the K0-WIDEN pad makes every Trump image
doubly met at every corner, so "that lineage can never die by K0-FREE, at any depth" — the terminal mechanism is
the basin landing, as in the interior tree. A150 (2026-09-08): four cores at four corners move η by a whole unit
(median −1.0, 7 converged kills, 7 certified once A166's certificate fix landed) — "the strongest level-1 LP in the
k0 lab" — but "the band is NOT narrow (206/216 cells; whole zone)" and the product is ≥ 4·10⁵ CPU-h. A154: the
counting row (R6) is A115's row verbatim and kills nothing. A155: the pad is a 2% effect and slabs make it worse.
A159: the PI's `l1_124` reading ("two squares can touch the corner but are mutually exclusive") is right at the
unwidened cell on 35 of 44 corners, 16 of them exactly tangent — and irrelevant at the widened box the window needs.
A166 (2026-09-09): the nearest-corner sub-tree the PI asked for is ONE sub-tree (the corner is TR for 117 of 119
open cells), the canary forced a second branch ("K0-BLOCKED says the corner box has two DISTINCT meeters; it does
not say either differs from the conditioned square"), and the free (C) leaf "is provably unavailable" — the two
conditions it needs are anti-correlated on every cell. Figures: `figures/A143_pair_survivors.svg`,
`figures/A155_band155_pad0_vs_padmax.svg`.

*Effect.* No k0 cell died, the k0 row did not move, and the corner-first line is closed from every side. What
survived is a rule that the cascade of §3.6 is built on — "spend a node's conditioning budget on cores that are
pairwise far apart, never on a second core at a corner that already has one" (A165: 1 core at a corner η −0.044;
2 at the same corner −0.083; 2 at one corner + an interior core 0.0000; 4 at 4 corners −1.0 to −6.0) — and the
lesson that the PI's predictions were "right in direction, wrong in consequence" three times running (A143, A159,
A166), each time because of an object the drawing did not show: the window pad, the widened box, the conditioned
square as its own corner's meeter.

### 3.6 The l1_104 reading: wastage, the right wall, and the cascade order (A164/A165/A168, 2026-09-08 to 09-09)

*What the AI was doing.* After the corner-first line closed, nothing on the eleven converged-alive k0 cells;
docs/shadows/k0v4/ had been drawn (A148) and every leaf had been run on it with no kill.

*What the PI saw and said.* On `docs/shadows/k0v4/l1_104.svg` (figure `figures/k0v4_l1_104.svg`), 2026-09-08:
"a WASTAGE argument (not lane): only one centre fits near the right wall below H, the upper-right pocket is too
short, so the right-wall strip is uncovered wherever that square goes." Then the cascade: "TR doubly met forces D
(deep, up-right of H) + S (shallow, up-left) -> two centres in the top strip -> top-wall chord row leaves one more,
which must poke into TL(0,0) with a min depth -> TL's second meeter forced along the left wall -> bottom-left band
holds one -> six squares in narrow forced boxes, large wastage, the other five cannot fit. = A150's mechanism (many
conditioned boxes buy LP slack) with the boxes FORCED by geometry instead of enumerated" (memory log 2026-09-08).

*What the drawings said back.* A164: the wastage leaf is sound and cheap and "fires on nothing" — on `l1_104` the
certified uncoverable area is 0.129 = 3.2% of the budget 4.03, all of it in the east wall strip the PI named:
"the PI's location is right, the count is not" ("only one square's centre can sit near the right wall" is false
unconditionally: seven 1-separated centres fit in x ≥ s0 − 1/2). A165: steps (a) and (b) confirmed and certified —
M(c) = 0 at all four corners, so "11 = 8 FREE corner meeters + H + exactly 2 further squares"; on 185 of 500 TR
cases the top-wall chord row gives β = 1 ("exactly the PI's sentence"); 434 of 500 cases are the PI's picture of
the pair — and step (c) breaks: by Lemma (TOP) a TL meeter must cross the top line but "its chord there may be
arbitrarily small", so the second TL meeter is a shallow crosser the row cannot charge. Spread cores at budget 6
kill 4 of 4; stacked cores at budget 8 buy nothing (η = 0.0000 on 3 of 3). Figure: `figures/A165_cascade_l1_104.svg`.

*The order, revised three times overnight.* 2026-09-09 ~00:30 (after killing A165, §3.7): the PI's first
branching order "(1) the right-wall square under H meeting BR (one centre fits), (2) the TR pair ... (3) the top
square the chord row leaves room for"; then "REVISED cascade order (supersedes): (1) the TR corner square D first;
(2) the second TR meeter S, limited by D, presses H down-right (re-clip H vs K′(S), K′(D)) which kills much of the
space for the right-wall square B under H; (3) BR's second meeter, greatly limited; (4) the two left corners last";
then the final form "(1) TR corner square D; (2) second TR meeter S (re-clip H vs D,S); (3) B = the right-wall
square under H, BR's deep meeter, as its own step; (4) BR's second meeter; (5) left corners last if needed." And
the rule that changed the object being branched on: "a corner's first meeter's region = the poses ADMITTING a
second meeter (coexistence, mutually clipped), not the bare corner-meeting region: D's region cut by the existence
of an S; B1's region cut by the existence of a second BR meeter that (because of the small gap above B1 below H)
cannot come from above or above-left" (memory log 2026-09-09 ~01:30). After A169 (§3.8) the partner window for B1
was pinned to one cell: "B1 (right-wall deep meeter under H) -> partner only from the (left, floor) cell".

*The directive.* The PI's reading of the first cascade results (2026-09-09) is recorded as a standing rule:
"doing more of this forcing geometry before LP is going to be necessary to getting it to complete in a reasonable
amount of time... it cuts down on the LP tree enough that it pays off massively on the backend"
(`writeup/sources/geometry-before-lp.md`). Evidence attached to the rule: "D step killed 54/82 cover boxes by
geometry; lonely rule 71/309 alive nodes in one pass at zero LP cost; per-piece K′ cut surviving poses of H and D
by ~20% more; LP side costs ~0.7 CPU-h per ALIVE kill (A149)". Every brief since states the forcing order
(container clip and per-piece K′ to a fixed point; lonely clip; coexistence cuts; all four corners at once; chord
rows from the grown cores; exact-core LP last) and forbids an LP at a node whose geometry has not reached a fixed
point.

*Measured effect so far.* The cascade has not closed `l1_104` (§7). What it has produced is the structure the k0
kill will use if it comes: the forced-box tree (A168, `figures/A168_cascade_l1_104.svg`,
`figures/A168_steps_l1_104_S3.svg`), the coexistence cut at piece granularity (A174), and the lonely clip (A173:
"13 of 146 A168 nodes killed by the clip alone").

### 3.7 The two unclipped cascades, the invariant library, K′ from pieces, and the axis-core defect (A165, A168, A171, A172, A175, 2026-09-08 to 09-09)

This is the episode the PI's brief singles out, because the failure was one the AI could not see in its own
output and the PI saw at once in the picture — twice, on two different agents, in twelve hours.

*First catch (2026-09-08, A165, Opus).* The coordinator's log: "PI caught A165 drawing unclipped pair boxes
(TRa/TRb pose unions overlapping H's core). RULE (again, now hard): in every multi-box node, clip every box against
every other core BEFORE drawing / rows / covers / LP; a box all of whose poses meet another core is empty (case
dies); draw K′ as the core, pose unions as thin outlines only." At 00:35 on 09-09: "A165 (Opus cascade) KILLED at
the PI's request (unclipped pair boxes; low faith in execution); redone as A168 (FABLE) ... RULE (PI): complex
case-tree constructions go to Fable, not Opus."

*Second catch (2026-09-09, A168, Fable).* "PI caught A168 (Fable) at S2: D's core escapes the container and overlaps
H's core; B1 clips H; S (the second TR meeter) not placed before moving to TL. Sent a stop-and-fix with a hard
INVARIANT: at every node, container clip + mutual clip to a fixed point, then the checker ASSERTS every K′ inside
the container and pairwise disjoint before any figure/row/LP ... Second agent to break the clipping rule — the
invariant must be code, not instruction."

*What changed.* A171 (2026-09-09 ~02:30) made the rule a library: `multibox.Node.normalise` (container clip per tilt
sub-bin, then mutual clip of every box against every other box's K′ to a fixed point, cores rebuilt after each
pass) and `assert_invariant` (exact rational K-CONTAINER, K-DISJOINT, POSE-CONTAINER, CLIP-FIXPOINT), with
`chord_rows`/`lane` refusing an un-normalised node. Run on A168's own S2 node it "fails 5 checks: D's centre rect
exceeds s − w_max/2 by 0.087938 (47.1 % of its poses leave the container) ... After normalise ... kept H 0.440792,
B1 0.942803, D 0.088172 — 91.2 % of D's box and 55.9 % of H's were never possible" — which is the size of the error
both cascades had been building on. Figures: `figures/A171_BR139_TRH-25_before.svg`, `figures/A171_BR139_TRH-25_after.svg`.

*The third catch, on the fix itself (2026-09-09 ~10:40).* "PI finding on A171: clipping a box's pose space must GROW
its K′ on the far side (intersection over fewer poses), and that growth is what propagates the cascade (D grows ->
clips H harder -> clips B1). A171's rebuild() formed K′ from the UNION HULL of the surviving pieces, losing most of
it." A172 rebuilt K′ as the certified exact intersection of the per-piece K′: on the same pieces the hull gave K′
areas H 0.658 / D 0.740, the pieces give 0.709 / 0.774; the fixed point then keeps H 0.358 (was 0.441) and D 0.072
(was 0.088) — "the hull was hiding a quarter of what the clip had already proved." Figure:
`figures/kprime_pieces_S2.svg`. "Rule: any clip/normalise loop must recompute cores from the PIECES, never from a
hull."

*The fourth catch (2026-09-09 ~12:30).* "DEFECT found by the PI reading A174's S3 page (H outlines crossing S and B
cores while kept H = 1.00): roles168.normalise clips against the other roles AXIS CORES only, never their K′
polygons -> no upstream propagation. Node l1_104 root/D0/S1/B0: A168 kept H/D/S/B 1/1/1/0.60 ALIVE; multibox poly
obstacles -> EmptyBox(H) = DEAD (pair leaf)." A175 was launched to route every node through the polygon clip and
re-normalise every recorded node. "RULE: multi-box clips must use K′ polygons (mode=poly), and pages must print
kept fractions so a non-propagating clip is visible."

*What this episode says.* Four defects in one construction, each invisible to the agent that produced it and to
every internal consistency check, each visible on a page to a reader who knows what a clipped box should look
like: a pose union crossing a core, a printed kept fraction of 1.00 beside an outline that crosses two cores. The
PI's response each time was not a patch but a system change: the rule became a brief instruction, then a library
with a guard, then a required line on every page. The `01_summary.md` phrase for it: "the loop corrects in both
directions".

### 3.8 The sideband lemma and the csc(θ) construction (A169/A173, 2026-09-09)

*What the AI was doing.* Building the cascade's corner steps with sampled facts: "the coordinator had only samples
(no disjoint pair with both centres beyond 1 in 81k draws) and an atlas whose thresholds (0.18/0.34/...) nobody had
derived" (A169). The atlas (`figures/two_meeter_atlas_v2.svg`) had been drawn overnight from a pitch grid.

*What the PI said.* "PI's LEMMA SIDEBAND (conjecture): a doubly-met corner box has at least one meeter with centre
within 1 of an adjacent wall (x <= 1 or y <= 1 at BL) and the other outside that band. Numeric: no disjoint pair of
meeters with both centres beyond 1" (memory log 2026-09-09). And a construction for the requirement on the first
meeter: "closed-form construction for the second meeter given a wall gap delta of the deep meeter: deepest
intrusion = a square flush with the side wall resting on the deep square, rotated by theta to fit the gap ->
intrusion in csc(theta), valid while sin(theta) <= delta; shallowest = cores whose corner just touches the top of
the gap. Expected: the allowable region is wildly small for flush deep squares and conservative delta."

*What the proof said back (A169, Fable, done-success).* Half right, sharpened, and the false half replaced by the
true statement. SIDEBAND (a) is a theorem "with constant c itself (1 unit, 1 + w widened) and no quadrant / no
bound on c" — but "within 1 of a wall" is FALSE at the widened box (two 45° diamonds at (1.01, 1.72) and
(1.72, 1.01), SAT gap 0.0078). Clause (b), "the other lies outside the band", is FALSE as stated (both centres can
have x < 1) and TRUE as "centres in DIFFERENT cells of the 2×2 grid at c", from an ℓ∞ separation of 1/√2 (Lemma
A2). The requirement became Theorem B: a second meeter exists iff one of four one-parameter support inequalities
holds; a pressed first meeter is lonely at every tilt; the slide threshold is exactly tan(θ/2) up to θ* = 56.76°;
the atlas's d* values "are pitch artefacts"; the widened-box partner exists iff θ < 17.35° or > 72.65°, "NOT the
12.8 deg of the mode-(a) guess". `Sideband.lean` (345 lines) proves A1, A2 and (a) and states Theorem B with clause
(P) proved. Figure: `figures/sideband_lemma.svg`.

*Measured effect.* Three rows for the cascade (R1 cell prune, R2 band/outside split, R3 the LONELY NO-family) and a
new clip: R3 "removes 54-74 % of the widened meeter poses at every tilt"; A173's per-piece lonely clip kills 13 of
146 A168 nodes with no LP (`figures/lonely_clip_S1.svg`); and the PI's single-cell pinning of B1's partner. The
shape of the exchange is the general one: the PI supplies a geometric statement with a mechanism attached (the
csc(θ) construction is a mechanism), the AI proves the sharp form, refutes the over-statement with an explicit
configuration, and hands back an n-general lemma with a Lean file.

### 3.9 The false readings — where the drawings refuted the PI, and why that mattered

The reading loop only works if it corrects in both directions. Roughly half of the PI's per-node readings of
2026-09-08 failed on exact tests, and every failure was written down with the witness that refuted it. The
common cause, four times out of six, was a *hairline meeter*: a square that reaches a cell by a clearance of
10⁻² or 10⁻³, invisible on a page drawn at container scale. The record, in the order the readings were made:

| page (figure) | the reading | what the exact test found | attempt |
|---|---|---|---|
| `k5_16_interior_Y1117` (`figures/a57v4_k5_16_interior_Y1117.svg`) | BR(0,1) singly met: a 55° grazer 0.003 into the cell should not count, so shrink the cell by the pin tolerance | "MY shrunk-cell argument was FALSE: four grazers through four faces block every admissible translate"; and "Y1117's BR(0,1) is a GENUINE 2-crowd (pairs with gap 0.24-0.33) — the PI's eye was wrong there" | A152 |
| the same page | the LP drops H + 3 into one pinwheel grain — price the grain by a cover number | the leaf is sound and LP-free and "kills nothing, and provably will not": F_out already holds ≥ budget points pairwise ≥ 1 apart on 322 of 322 nodes; Y1117's cover number is 8 against budget 5 | A153 |
| `c0_Y0076` (`figures/a57v4_c0_Y0076.svg`) | TL(0,0) singly met (A141 had it UNDECIDED with no free meeter sampled) | 400,000 draws: 14 free poses, the best clearing every core "by 1.1026e-2 at theta = 29.4420 deg"; "a free tilted square can reach a slot past H while clearing it by 1e-2 — invisible on a page" | A157 |
| the same page, the PI's second diagnosis | the LP is alive only because it counts a near-simple TL slot square AND H as meeters; split YES/NO on the slot box | the NO child is DEAD and certified ("c0_Y0076 provably places a square within 0.10 of the exact TL(0,0) slot centre"), the YES child "does not exist: 0 of 141 measured cells", and as an LP node it "lands exactly back on the knife edge" — the slot square removes one unit of dual packing and one unit of budget | A158/A158b |
| `c0_Y0959` (`figures/a57v4_c0_Y0959.svg`) | TR(0,1) singly met | H reaches into TR(0,1) by 0.12 and two disjoint grazers from below also meet it; "RULE for readings: 'met' = interior intersection, any depth; grazers from an adjacent region count" | memory log 2026-09-08 |
| `c0_Y0169` (`figures/a57v4_c0_Y0169.svg`) | TL(0,0) reachable by one square at a time; H's corner leaves under 1 of width for a band square | first half CERTIFIED (LANE_out = 0 on every piece), second half "false as stated": a free band pose survives beside H on every swept offset; the cell is a no-go by exact two-crowd witness | A161 T8, A167 |
| `l1_124` (`figures/k0v4_l1_124.svg`) | TR(0,0) cannot be doubly met — two squares can touch the cell but are mutually exclusive | right at the unwidened cell (0 of 28 recorded witnesses have both squares meeting the plain cell; 16 of 44 corners exactly tangent), and wrong at the widened box the window needs (30 of 44 corners have an exact realised two-crowd) — "the PI's reading is right about a different rectangle" | A159 |
| `l1_104` (`figures/k0v4_l1_104.svg`) | only one centre fits near the right wall | seven 1-separated centres fit in x ≥ s0 − ½; the certified waste sits exactly where the PI put it, at 3.2% of the budget | A164 |
| `k5_11_interior_Y0275` (`figures/a57v4_killed_k5_11_interior_Y0275.svg`) | a quadrilateral pocket with all sides < 1 and one firm side holds no square centre | "General lemma ... is FALSE (diamond in a 0.99-square at (0.25, 0.495) crosses 3 sides, misses the 4th, touches no vertex)"; the node was nevertheless pulled forward and certified dead by the exact-core re-solve (A149) | memory log 2026-09-08 |

Why the refutations mattered as much as the hits. Each one changed the drawings or the leaf, not just the
verdict: after Y1117 and c0_Y0076 the pages draw "the witnessed free meeters (the sampled disjoint pair, thin
outlines, with their depth into the cell printed) so that hairline meeters are visible" (drawing rules, 2026-09-08
addendum); after Y0275 the undecided band stopped being green ("A148 painted the UNDECIDED band pale green and the
PI read it as feasible" — it had overstated the free set by about a fifth); after l1_124 every page prints the pad
against which a lane verdict is stated; after c0_Y0169 the leaf that had "nothing to prove" was retired and the
285 no-go cells were closed by exact witnesses rather than left undecided. A121's validator, run over the PI's
whole first pass (83 pages, 219 items), put numbers on the reading types: "All 18 `r` readings exactly right"
(singly met corners, the reading type that works); of 64 `ns` (near-snap) items 6 genuine, 24 already exactly on
the cell, 26 flush along a wall — a new token `fl` was added rather than a re-drawn frame, because "the identity is
still the argmin" over all 784 relabellings the PI might have been using.

### 3.10 The earlier spatial reads: o012, the drains, and the price refusals (2026-09-03 to 09-06)

Before the galleries existed the same pattern ran on single configurations.

*o012 and the emptied corpus (2026-09-03).* A87's FJ-polish had produced "167 certified k0 FJ points" and the
coordinator had built a route on them. "PI diagnosis, confirmed: the 167 'certified k0 FJ points' (A87) are ALL
K0-FREE by teleport (0/167 genuinely K0-BLOCKED; o012 at 3.8972 = atlas fam13/14 (k1) lifted 4e-4 with a rattler
whose removal frees the TR slot) ... Lesson: the 'k0' label by exact simple-square count is NOT the proof's residue;
always filter by K0-BLOCKED" (memory log 2026-09-03). The outline calls this "the diagnosis of o012 as a k ≥ 1
point in disguise, which emptied the entire corpus of 'k0 critical points'". The residue was thereafter
K0-BLOCKED — every corner doubly met — and the PI's intuition "ghosts walk uphill; relaxing lands on simple squares
/ octagon family at 4+" (memory log 2026-09-03) became DF-K0 (A87, [T], a two-line proof in the selected form).

*The 3.985 record and the 3.9907 record (2026-09-05, 09-06).* Both were the lab's candidate counterexamples to the
drain conjecture below side 4. On the first: "PI shower correction: the 3.985 'interlock' record degenerates at the
SAME side into k5_10 ... align 4,5,6 (1e-4 moves; 6's TR 'nick' is a 1e-8 TANGENCY, not a block), slide 10 into the
cell below TL (0.38) and 7 into the TR corner (0.39). Lessons: tangency != block". On the second: "PI read the
figure and saw square 3's three contacts (sq 2 below, right wall, sq 8 upper-left) all permit a CCW rotation;
rotating 3 by 1.31 deg about its centre to axis-aligned is collision-free (2000-step SAT sweep), lifts its vertex
out of BR ... simultaneous snaps of 1,2,3,5,6,7,9 give a VALID packing at the same side with k = 7 ... Third time
the PI's spatial read beat the census (3.985 record, interlock, now 3.9907)." Both drains are drawn
(`figures/record3985_drain.svg`, `figures/strict_3p9907_drain.svg`) and the second became a tool (A102) that
drained 10 of the 12 strictly blocked packings on disk. The lesson banked: "strict K0-BLOCKED with floor-depth second
meeters is a ROTATION eta-disturbance, not just translation".

*The price refusals.* The outline (§6, §7) records the PI's "repeated refusals to accept a price ('Are you
kidding?'), which produced A85/A88/A89/A90 and the K0-BLOCKED filter instead of a compute purchase" and the AI's
tendency to "reach for cloud compute as soon as a tree was priced" (the coordinator's 2026-09-03 note: "cloud spot
~$500-1500 for everything, k0_00 alone ~$160-350 ... Decision pending with PI"). The PI's answers were a target
("~400 CPU-h all layers", 2026-09-04) that the machinery has never met (all-layers estimates ran 5,900–13,700 CPU-h
on 09-05 and ≈ 6,100 / 19,500 on the two routes by 09-08) and a direction: "PI rejected the volume-tree frame
('remainder must have exploitable structure')" (memory log 2026-09-03). That refusal is what turned the k0 problem
from a 12,000 CPU-h tree into the geometry programme of §3.5–3.8. [The "Are you kidding?" exchange itself is in the
outline's attribution list, not in LOG.md or the memory log; PI to confirm the date.]

### 3.11 The AI's own retractions

The record keeps the AI's wrong claims beside the PI's, for the same reason. The ones that cost compute or
direction:

- "each grid side yields a record floor" — retracted 2026-09-03: "k0_00 eta = 0.000 (root LP has no slack above the
  3.83 pure-LP ceiling) ... my 'free floors' claim retracted".
- "most boxes exclude immediately by nonzero gradient" (the H1 cover) — A87: "ADVISOR ERROR ... confused 'forall z
  exists descent direction' with 'exists one direction feasible on all of B'"; 1,448 cells, 0 kills.
- the η-law ("η ≤ −1 ⇒ certificate") — "ETA LAW RETRACTED (A60's second overfit, n=16)"; re-measured one-sided
  on A57 (A96, 2026-09-05: η = 0 ⇒ resister holds 15/15; η < 0 ⇒ certificate fails on 21%).
- "the 4.000002 barrier" for K0-BLOCKED packings — retracted twice (2026-09-03 against the 3.985 record; 2026-09-05
  "a search floor bounds what the search can SEE, not what exists").
- the mixed-sign V prune for corner pairs — "UNSOUND locally" (A85).
- A106's pin-clash prune (122/516 boxes "empty") — "NOT SOUND as a certificate as written ... a positive sample
  minimum does not prove the true minimum is positive"; the sound version (A96 route B) yielded 70.
- "four shallow corners are dead by area" — A89: "area alone never kills 4-shallow in the window (4(1-delta)^2 <= 4)".
- A161's "90 new" kills — 27 on re-check against the collector; "RULE: build populations from the STATUS collector,
  never from a campaign snapshot".
- A165's "they need the separation loop with more rounds, not a different core" — A170: "they needed the cores they
  were solved with" (a shared-machinery bug, `caselp.make_certificate` reverting exact cores to stock).
- the A60 "stalled" false alarm from a command-line regex (2026-09-03, "5th instance"), and the sixth
  "check-failed-read-as-negative incident (errored Get-Process read as 'finished') — rule: file-based wait
  conditions, verify a check produced output before believing it".

Two of these are of the same kind as the PI's false readings (a sampled minimum mistaken for a bound; a count
taken from a stale snapshot) and were caught by the same discipline: an independent test with a witness.

### 3.12 The process rules the PI imposed

Each rule below is quoted from the record with the incident that produced it.

- **No recursive deletes** (2026-09-06, "no-deletion rule"): A96 audited every file it had touched — "Exactly ONE
  existed ... REPLACED with a non-deleting check"; every attempt's close-out since reports "no recursive deletes,
  no pidfile deleted", and the status board `git mv`s dead pages to `killed/`, "never delete".
- **Frozen verifiers**: sha-pinned copies, versioned successors, "frozen verifiers untouched" in every report;
  the standing instruction that "kills are reproduced by REPLAYING certificates, never by re-emitting", after A112
  found that emission is wall-clock dependent.
- **Process ceilings and affinity** (2026-09-08): "BOX RULE (PI): lab work confined to the 16 P-core threads ...
  ceiling 16 lab python processes"; and the night-shift refusal that preceded it — A123 "correctly REFUSED the full
  A57 resume: the box already held 17-20 python processes ... 3x oversubscription would convert other campaigns'
  wall-capped nodes into spurious TIMEOUTs" — with the law "a campaign resume needs a process budget counted against
  the live box first; chores at '<= 2 each' add up".
- **The priority rule** (2026-09-09): "Prioritise work that enables the PI's next round of feedback: results of
  reading experiments (leaf pilots on named nodes), re-solves that answer a specific reading, and recomputing the
  residue (ledger, STATUS.md, the galleries) take precedence over naive tree solving ... the loop (draw → read →
  leaf → kill → redraw) is the lab's fastest source of kills, and it stalls when the board is stale or the LP slots
  are occupied by the bisection tree. The tree only converts at its measured rate; it does not learn"
  (`writeup/sources/feedback-priority-order.md`).
- **Geometry before LP** (2026-09-09): §3.6.
- **Aggressive optimisation testing** (2026-09-06): "wall-time is the primary limiting factor ... Every
  chore/campaign must be RESUMABLE ... Fire jobs that kill tiers/windows ... whenever the kill estimate is under ~2
  CPU-h — no need to ask" (`writeup/sources/aggressive-optimisation-testing.md`).
- **Kill agents whose pictures are wrong**: A165 killed at 00:35 on 2026-09-09 (§3.7); A168 stopped at 10:35 and
  A174 stopped at ~12:30 for the same class of defect; "complex case-tree constructions go to Fable, not Opus".
- **Two-stage LP protocol** (2026-09-06): "stage 1 LP at 240 s -> any node with eta <= -1e-3 goes straight to the
  frozen certifier ... stage 2 = only knife-edge nodes get 900 s ... Report kills as CERTIFIED passes, never LP
  verdicts" — the PI's answer to "more nodes at low timeout or fewer at high?" was fewer at the converging cap,
  and the asymmetric cost behind it: "a false ALIVE ... costs 8 children x ~850 s".
- **The sampled-check rule** (A111, 2026-09-06): "no number derived from an LP-free geometric rule is reported
  before dense random pose sampling confirms it", plus A96's refinement that "an acceptance-filtered sampled check
  must report how many samples SURVIVED the filter, not how many were drawn".
- **Git on the shared tree** (2026-09-04, after an autostash reset "clobbered 48 live tracked files of other
  campaigns for ~2 min"): "no rebase / autostash / reset on the shared tree while campaigns run — git fetch, plain
  merge if needed, push own paths only", and after the shared-index race of 09-07/08, "use `git commit -- <pathspecs>`,
  never add-then-commit".
- **CAP is never a verdict** (A117, A120, A124): a wall-capped run is recorded as CAP and the whole process tree is
  killed; "a FAIL that returns in under a second is a crash, not a verdict" (A114).

## 4. The visualisation loop as a system

The loop was not designed at the start; it was built in five days (2026-09-04 to 09-09) out of the PI's
corrections, and every part of it exists because a specific misreading happened first. This section lists the
parts, what each prevents, and how fast the loop ran.

### 4.1 What is drawn

The object is never a packing. It is the state of one node of a case tree: the container at the certified side
s0; the pinned squares of the class as exact squares; the conditioned square H as a *box* of centres and a window
of tilts, with the cores every pose must contain drawn inside it; and the LP's dual support — a fractional object
that never converges to a configuration — drawn as squares at their centres and tilts with opacity by dual weight,
overlaps allowed. The PI's phrase for why this is the right object is preserved in the outline: "the LP approach is
semi-Eulerian" — the relaxation lives on a field over the container, and a person can read a field drawn as
overlapping squares far better than a list of atoms. Four generations of page:

| version | date | attempt | what it added | what it was for |
|---|---|---|---|---|
| shadows v1 | 09-06 | A107 | the dual support snapped and released to a local minimum; 53 shadows; contact graph, flexes, rattlers | naming the families (S01 room, S02 pinwheel, S07) |
| shadows v2 | 09-07 | A107 | tilt hue removed, one sequential ramp by dual weight; H in cyan with a heavy outline "used nowhere else"; snapped slot squares recoloured; a one-line legend | the PI's rendering feedback: 47 mis-coloured squares in 33 entries |
| k0v3 / a57v3 | 09-07 | A140, A142 | the three cores of H in distinct styles; both cores on every pin; every impossible column labelled with which core it clears and which it meets; schematic objects as thin dashed outlines | the Y0186 columns, the Y0036 pinch |
| k0v4 / a57v4 | 09-08 | A148 | three panels in reading order — G GEOMETRY (certified feasible-centre region, pockets, guard lines, lane tags), S the LP SUPPORT, N the NEAREST PACKING at its own s* with s0 overlaid; a WHAT-TO-LOOK-FOR line; the verdict of every leaf already run; the disk bound | "less busy, impossible overlaps should not appear at all, notes on what each plot IS; the question is 'is there a shortcut that geo-kills the node without more LP'" (PI brief, 2026-09-07 22:40) |

Alongside the galleries, `docs/residue_map/` holds the family pictures (Trump, the pinwheel and its tilt curve,
S07 beside Trump, the drains, the two-meeter atlas, the sideband lemma, K′ from pieces), each generated by a script
that "checks every square for containment/disjointness/depth" before drawing it, because the first family pictures
had been drawn from unchecked coordinates. Every page and every figure copied into `writeup/figures/` comes from
one of these generators.

### 4.2 The drawing rules and the misreading each prevents

The rules are in `writeup/sources/drawing_rules.md`, each dated; here is what each one stops.

| rule (date) | the misreading it prevents |
|---|---|
| Draw H at the CENTRE of its box and the CENTRE of its tilt window, tilt printed (09-07) | a page drawn at a box corner or an extreme tilt shows a configuration the node may not contain; on Y0036 the box centre was itself infeasible and is drawn red-dashed for that reason |
| Never draw schematic objects (bins, cover cells, branch boxes) in the same visual language as bodies; bins = thin dashed outlines, no fill, labelled (09-07, "PI confusion on l1_153 panel 3") | reading a slot-census bin as a square |
| Inside each H draw THREE cores in distinct styles with a legend: the stock axis core the LP pruned against, the exact axis core, the polygon K′; label impossible columns with which core they clear (09-07) | believing a column is impossible when only the sloppy core says so — or possible when only the sloppy core admits it (the Y0186 leak) |
| Draw a near-packing at its own s* with s0's container overlaid dashed and a large banner "NOT realisable at s0" (09-07, c0_Y0171) | reading a side-4 shadow as a packing at 3.877 — "all 55 pages with an A107 shadow family have s* > s0" |
| Draw, per usable slot and corner, the witnessed free meeters with their depth into the cell printed; print the lane verdict with both bounds and M (09-08, "three PI slot readings refuted by grazers") | the hairline-meeter misreadings of §3.9 |
| Undecided = light grey stipple, never a green tint; only certified-feasible is green (09-08, Y0275) | reading the Lipschitz margin as free space; it overstated the free set by about a fifth |
| Keep the galleries LIVE: `status_gallery.py` collects every kill record, `git mv`s killed pages to `killed/`, writes STATUS.md; rerun at every pause (09-08) | reading a page that is already dead — A148 drew three dead A60 nodes as alive because their kills existed only as certificate files with no jsonl row |
| For cascades: one page per step (known before, forcing applied, boxes after), a final tree of cases; every "pin family" drawn BY GEOMETRY as a filled region with the forced box's K′ solid, pose unions thin, guard lines with chords printed, every region labelled with the leaf that produced it (09-09) | the unclipped-box defects of §3.7; "the PI wants to check the construction against the reading, not just the verdicts" |
| Print kept fractions on every multi-box page (09-09, A175) | a clip that does not propagate (kept 1.00 beside an outline that crosses two cores) |

### 4.3 The reading sheet

Each gallery carries a CSV with the automatic columns filled (τ, budget, η, converged, family, s*, the free area,
the disk bound, the lane tags, the impossible-column weights, the WHAT-TO-LOOK-FOR line) and four human columns
empty: `PI_reading`, `PI_shortcut`/`PI_load_path`, `PI_binding_contact`, `PI_drain_or_kill`. The PI writes in a
shorthand that A121 validated and A121's rules refined: `r <sq> <cell>` (a corner or slot reachable by one square
only — "the reading type that works", 18/18 exact), `ns` (near-snap), `i` (incomplete support, fewer than eleven
squares — the pointer that produced 14/14 certified k0 kills), `g` (a common-tilt grain, with its load path),
`st4` (four flush squares on a wall ⇒ side ≥ 4 — sound, "kills S50/S52/S53 as configurations, not nodes"), `fl`
(flush along a wall, added when 26 of 30 "far" near-snaps turned out to be flush displacements), `-` (the blue
snaps carry the row), `?`. The validator's one-line verdict on the first full pass, 83 rows: "the readings validate
the gallery but node kills are bottlenecked by M = 1 (the tree's own conditioned square may be the second meeter),
not by identification — PI's time is best spent on `g` rows, `?` rows, and pinned S rows; `ns` on K rows yields
nothing" (memory log 2026-09-07).

### 4.4 What the AI drew and what the PI read from it

The direction of information is asymmetric and the record shows it precisely. The AI draws what it has certified
(cores, regions, verdicts) and what the relaxation did (the support). The PI reads *mechanism*: which square can
slide, which corner is reachable by one square only, which pair is mutually exclusive, where the wastage lands,
which order forces which. The AI cannot see mechanism in its own output — A106's basins around nothing, the
unclipped boxes, the hull that lost a quarter of the clip — and the PI cannot see hairline clearances, window
pads, or the difference between a widened box and a unit cell. So the loop is: AI draws → PI reads a mechanism → AI
states it for a class, not a node, writes the soundness argument, builds the checker, runs it over the whole
population with a sample line and a canary → the drawing changes to show whatever refuted or confirmed it. The
outline (§6a) calls the population step the important one: "The AI states it for a class and a slot rather than a
node ... and runs it on the whole alive population" — every reading that became a leaf (pin-clip, polygon core,
lane, chord-limited lane, guard line, sideband, lonely clip) is a leaf over the corpus, not a fact about the page it
came from.

### 4.5 Cycle times

Measured from the timestamps in the memory log and the attempt reports.

- Reading → leaf → population result: the Y0036 reading (2026-09-07, daytime) → A131's exact clipper and 132
  backlog kills (the same day, 4.1 s of CPU for the sweep); the Y0186 reading → A132 (same day) → A135's "certifiable
  today" (same day) → A137's 46 certified kills (that night). The Y0842 reading (2026-09-08) → A161's 98
  certificates the same day. The sideband conjecture (2026-09-09 ~01:00) → A169's theorem and Lean file by ~12:00.
- Reading → refutation with witness: c0_Y0076 (2026-09-08) → A157's 400,000-pose screen the same day ("sampling
  decides a cell in 2 s; cover depth costs 35+ s and decided none"); l1_124 → A159 exact re-examination at 60 dps
  the same day.
- Page defect → rule → code: A165's unclipped boxes (2026-09-08 evening) → the hard rule (00:30) → A171's library
  (~02:30) → A172's per-piece fix (~12:00) → A175's polygon-obstacle fix (~12:30 dispatched).
- Gallery regeneration: v3 to v4 in one night (A148, 06:50); the status board reruns in minutes and moved 7 pages
  to `killed/` between 09-08 and 09-09 10:05.
- The whole loop, draw → read → leaf → kill → redraw, "ran dozens of times a day" (`01_summary.md`); the record
  shows fifteen PI readings on 2026-09-08 alone, each dispatched as or folded into an attempt within hours.

What bounds the cycle is not the AI's speed but two things the record names: the box (16 lab processes, and the
readings' experiments competing with the trees for LP slots — hence the priority rule), and the page's honesty (a
stale gallery or a green undecided band costs a reading).

## 5. What each party could and could not do alone

### 5.1 The AI alone

*What it could do, with evidence.* Build every piece of machinery in the record: the covering LP and its exact
verifier on day one (A07/A08, the first new bound in 23 years within hours); the Lean toolchain and the chain of
checker-soundness proofs that took the axiom roster from 16 to 3 in three days (A62–A79); the case-LP trees,
their parametric window certificates (A96: 0.2 of one fixed side), the campaign engineering (resumable shards,
sentinels, orphan reapers, commit gates); the clean-room re-derivations (A72 census, A73 Rust verifier, A129 the
net verifier as an independent decision procedure for both headline theorems); and a large number of theorems —
the collapse theorems (A18, A34), the mismatch law, Lemma B, P-TREE, DF-K0, K0-FREE, the contraction tube, Theorem
LOCAL, Theorem B — each with the counter-example that bounds it. It measured every negative to its floor: of the
164 registered attempts, 28 are done-negative and 46 done-mixed or split, each with a reason no successor has had
to rediscover (registry tally, 2026-09-09; ~15 rows have malformed status cells and are not counted).

*What it got wrong, invented, or could not see.* (i) It could not find the decomposition (§3.1): fourteen attempts
of walls, then three fallbacks it repeated for a week. (ii) It could not see mechanism in its own output: the
basin switch around boxes that contained nothing (A106), the k0 corpus of "critical points" that were all k ≥ 1
in disguise (§3.10), the unclipped boxes, the hull, the axis-core clip (§3.7) — every one a page the PI read in
seconds. (iii) It over-claimed by tolerance and by sample: the η-law, the "free floors", the 4.000002 barrier, the
122/516 prune, "90 new" (§3.11). (iv) It reached for cloud compute at every price (§3.10). (v) Its own
characteristic tendency of Phase I — to stop and publish the 3.82 bound — is recorded in the outline. What it did
consistently well was the thing the PI could not do at all: turn a sentence into a lemma with a checker and a
canary, and say no when the sentence was false.

### 5.2 The PI alone

*What the PI could do.* Choose the standard and hold it (certificates, Lean, uniqueness kept in the theorem, the
paper only when the proof exists). Supply the ideas the outline lists as n-independent: the stratification, the
basin-exclusion row, the U_k ladder, the contraction-tube direction, corner floors, the teleport count, rotation
stationarity, "the derivative of s is negative for all perturbations away from a known solution" (→ DF-K0),
"ghosts walk uphill", the contact-graph route, the wastage framing, the intrusion-depth dichotomy, the grain
menu, the cascade and its order, the sideband lemma. Read configurations: the o012 diagnosis, the two drains, the
Y0036/Y0186/Y0147/Y0842 readings that became leaves, and the four defects of §3.7. Refuse prices, and provide the
machine.

*What the PI could not do.* Anything that needed a proof, a certificate, a population, or a hairline. The record
has the PI wrong on Y1117, c0_Y0076's YES side, c0_Y0959, the second half of c0_Y0169, l1_124 at the widened box,
the count on l1_104, the quadrilateral lemma, the "one deep lineage" of the corner tree, the sideband constant and
its clause (b) (§3.9, §3.5, §3.8). None of these was a matter of insight; each was a quantity below the resolution
of a picture (a clearance of 10⁻², a pad of 0.0255, a box vs a cell) or a universal statement that one
configuration could refute. The PI also could not have run the experiment that decides a reading — 400,000 poses, a
60-digit interval check, an exact two-crowd witness — nor written the leaf that carries a reading from one page to
the 1,693 alive records.

### 5.3 The movement between them

The outline's description holds on the record: "Most critical-path steps are a PI idea formalised by the AI and
then priced by a chore, with the price feeding the next PI idea." The best-documented loops are the stratification
(idea 08-31 → census and kills 08-31 → sharpness 09-01 → window 09-07), the k0 residue (price 09-03 → three cuts →
"exploitable structure" → o012 → K0-BLOCKED → the corner-first line → the cascade), and the cascade itself (reading
09-08 → A165 → the clip rule → A168 → A171 → A172 → A175, with the PI reading each page as it landed). The
outline's summary of what neither had alone is the one this document can confirm with numbers: "a person with no
formal training who, after enough pages, can say which family a node belongs to, where its nearest minimum sits,
and which leaf will fire ... and a code base in which that intuition is falsifiable in minutes."

## 6. The composite: an honest assessment with numbers

*Kills by lever, on the record.* Geometric leaves born from readings: pin-clip 132 backlog nodes in 4.1 s of CPU
(A131), +17 A57 and +34 A60 at the exact pin core (A142); polygon core T5⁗ 64 nodes, 37 new (A132); exact-core
re-solve 46 of 161 alive nodes certified (28.6%, A137), then 180 certified kills for 46.7 CPU-h (A149: 93 A57, 87
trump5 at 40.7%); K′ lane 47 k0 cells plus s3_far (A141); slot lane 188 A57 + 56 trump5 records, of which only 7
were new to the corpus once folded (A137 — the honest figure); chord-limited lane 27 new (A161) + 13 (T5 retry) +
11 (A167); guard lines 2 LP kills, unemittable under the frozen chain (A144); the local certificate 15 of 35 in-N
nodes at 1.39 CPU-h per closure (A136); the lonely clip 13 of 146 cascade nodes (A173). The plain warm re-solve the
PI asked for on the k0 cells — no new mathematics — certified 22 of 216 level-1 cells plus 25 others for 29.8
CPU-h, "1,023–2,372 CPU-h off the frontier, a 34×–80× return" (A115), against the corner rows' 13.4 CPU-h for
nothing.

*CPU-hours saved, as the budget file records them.* Tight core −32% on A57 (19.6 → 13.3 wall-days); trimming and
clip together ≈ 10–11 wall-days; the parametric window 3.8× against a four-side grid (A99); A57's work-owing
population 632 → 406 in one night (A137) and 423 after A156's 339 kills for 28 CPU-h at 2–3 workers. Against this,
the honest re-price: A57 rose from ≈ 800 to ≈ 1,800 CPU-h when A149 counted the frontier id by id and added the
descent term the old figure lacked — "the node is now cheaper (283 s) but one ok child costs 3.76 nodes". The
theorem-route total on 2026-09-08 22:30 is ≈ 6,100 CPU-h (4,650–10,050), the tree route ≈ 19,500, the PI's target
400.

*The day the geometry started outpacing the LP.* 2026-09-07. A124's day shift measured the 900 s LP re-check, then
the budget's "best per-budget item", at "2 STRICT kills for ~15 CPU-h, against 54 genuine logic kills for zero from
the geometry sweep, with 55 more visible in the FAIL queue"; the same day A131's clip collected 132 kills in 4.1 s.
By the next night the emission hooks were killing "a quarter of children before any LP" (798 of 3,034, A137), the
measured level-2 geometry rate was 27.5% against the 13.7% the schedule credited, and A156 found the rate is "a
FRONTIER property, not a level property (41.6 % on children of alive L2/L3 nodes, 0.6 % on children of fresh LP
survivors)". The PI's directive of 2026-09-09 (§3.6) is the generalisation of that day.

*What did not work, counted.* Cover number 0 of 322 nodes (A153); wastage area 0 of 71 (A164); node crowd rows 0
of 18 (A109); corner rows 0 genuinely alive cells (A115); the R6 row 0 of 29 (A154); the four-corner product
≥ 4·10⁵ CPU-h (A150); the slot split 0 of 141 YES children (A158); the undecided slots 0 of 25 covers (A157); the
near-miss joint split 0 of 9 classes (A159); row-dropping 0 new kills for a soundness-relevant verifier change
(A96); the region tree 3 of 11 non-trivial regions (A112); the pair-certificate route closed for corners4 after
seven attempts (A66–A81). Each is a page in the ledger with its floor named, and several changed the drawings.

*The composite, stated plainly.* The AI's machinery produced the certified state — 3.82 ≤ s(11) in Lean, 52/52
window rows, three axioms, thousands of certificates — and every price. The PI's readings produced the levers that
moved the prices: the stratification took the problem from "any complete search is dead by 7–24 orders" to three
classes and a residue; the reading leaves of Phase VI took A57's alive population down by a third in a night and
supplied the only k0 kills there are (s3_far, the 47 lane cells). The refutations ran both ways at comparable
rates. Neither the theorems nor the leaves exist in the record without the other party's contribution in the same
episode, and the outline's phrase "a composite greater than the sum of its parts" is, on this record, a
description rather than a claim.

## 7. Status on 2026-09-09 at midday, and what remains

*Certified.* 3.82 ≤ s(11) ≤ 3.877083590022814, both ends Lean theorems [L]. Every stratum with k ≥ 1 is dead on
the whole window except Trump's class and its protected sub-skeletons, 52/52 rows [C]. Trump is rigid and locally
optimal [L]; the tube covers the window in the class direction [C]; S07, S33, S35, S38 are exact local minima with
certified basins [C], two of them LocalDead in the kernel [L]. TopLevel.lean has three named axioms:
`stratum_kill`, `trump_residual`, `a22_exact_structure`.

*Not certified, and not claimed.* No k0 cell has been killed by the cascade. The eleven converged-alive k0_00
cells stand at eleven (STATUS.md, 10:05). The cascade on `l1_104` is the test: A175 is re-normalising every
recorded node with polygon obstacles, on the strength of one recorded node (`root/D0/S1/B0`) that is DEAD under
the polygon clip and ALIVE under the axis-core clip; A173's lonely clip has killed 13 of 146 nodes; A174's
coexistence cut runs at piece granularity. Until a cell dies with a certificate, everything in this paragraph is
[P].

*The compute that remains, and what "compute-bound" would mean.* A57: ≈ 1,800 CPU-h / ≈ 15 wall-days at five
workers, with 406–423 work-owing nodes and the single unmeasured input (D_2) now measured at ≈ 0.11. The protected
tier: 3,800 CPU-h priced from two pilot classes, none of this week's levers yet applied to it. k0_00: 0 CPU-h on
the theorem route or 9,400–12,000 on the tree route. Lean: the certificate replays (multi-day desktop jobs), the
per-node YES bridges, Theorem B's remaining clauses, K0-O1 (the k1_00 tree, 200–300 CPU-h, paid once). The claim
that the rest is compute would be justified by exactly one event: a k0 cell certified dead by the same
geometry-then-LP machinery that closed the other classes, at a measured cost. `01_summary.md` says the same in
plain language; this document's contribution is that the machinery, the readings that built it, the defects the
PI caught in it, and the four days it took are all on the record, dated.

*Gaps in this record the PI can fill in place.* (1)-(2) The two session quotations in §3.4 and §3.5 were filled in by the coordinator from the
session transcript of 2026-09-08 (they were never copied into LOG.md); the PI may correct the wording. (3) "Are you kidding?" (§3.10) is in the outline's
attribution list without a date. (4) The PI's own account of how the stratification idea arose is asked for in the
outline's fill-in list and is not on disk. (5) The Y0036 reading is preserved in the coordinator's paraphrase, not
the PI's words. (6) The registry's status cells for about 15 rows are malformed (a `|` inside the outcome text) and
the tallies in §5–6 exclude them.
