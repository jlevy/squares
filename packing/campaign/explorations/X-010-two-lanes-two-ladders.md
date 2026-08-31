---
title: "X-010 — two lanes, two ladders: focusing the campaign on first-party theorems"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-010
  title: Two lanes, two ladders — focusing the campaign on first-party theorems
  date: '2026-08-31'
  author: Claude (agent), with the owner, in the interactive strategy session of 2026-08-31
  campaign: packing.squares
  brief: >-
    The owner asked three things: a survey of the mathematical strategy and where a
    significant first-party result is actually reachable given machinery the research
    queue predates; a re-examination of the contact-graph, chunking, and perturbation
    search agenda (X-003); and an account of where the last few years of progress on
    n <= 100 actually came from. The direction attached: pick a few lanes, be ambitious,
    and calibrate the ambition by proving the tools out incrementally. This document
    answers with two lanes and their ladders, corrects two premises the standing plan
    (X-009) rests on, and proposes agenda adjustments without enacting them.
  sources:
  - packing/frontier/README.md
  - packing/frontier/STATUS.md
  - packing/frontier/n-012.md
  - packing/campaign/agendas/agenda-009-pipeline-hygiene-and-the-search-reassessment.md
  - packing/campaign/explorations/X-003-stratified-chunk-enumeration.md
  - packing/campaign/explorations/X-008-the-residue-is-axis-aligned.md
  - packing/campaign/explorations/X-009-where-a-new-packing-is-reachable.md
  - packing/campaign/hypotheses/H-006-lp-dual-unavoidable-sets.md
  - packing/campaign/hypotheses/H-033-m2-minus-3-at-n61.md
  - packing/campaign/hypotheses/H-034-fractional-piercing-ceiling.md
  - packing/campaign/hypotheses/H-039-s12-proof-frontier.md
  - packing/campaign/hypotheses/H-044-chunk-expressibility-of-records.md
  - packing/campaign/hypotheses/H-049-squeezable-20-in-4x6.md
  - docs/project/research/research-2026-08-22-packing-11-unit-squares.md
  - packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md
  - packing/resources/papers/bentz-2016-optimal-packings-22-and-33.md
  - packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.md
  - packing/resources/papers/mcclenagan-2026-optimally-packing-large-square.md
  - packing/resources/papers/square-packing-good-squares-2504.09489.md
  - packing/resources/papers/square-packing-x06-wasted-area-2508.04603.md
  - packing/resources/web/kingbird-squares-in-squares.md
  - packing/cases/stromquist/printed_cover.py
  - packing/cases/stromquist/repaired_cover.py
  - packing/src/sqpack/exact_lp.py
  - packing/src/sqpack/chunks.py
  - packing/src/sqpack/contact_assembly.py
  - packing/src/sqpack/contact_realization.py
  - packing/atlas/enumerated/README.md
  - packing/atlas/enumerated/contact-scaffolds-size5.json
  - packing/witnesses/prospective/n-110.yaml
  - packing/devtools/check_nagamochi_bounds.py
  - packing/campaign/ledger.md
  proposes: []
---
# X-010 — Two Lanes, Two Ladders

**Date:** 2026-08-31

**Status:** Strategy synthesis from the interactive session of 2026-08-31, at the
owner’s request. It promotes nothing and adjudicates nothing; the agenda adjustments at
the end were proposed here and enacted the same day as agenda-010 (see that section’s
note). Unlike X-009 it used no sub-agents: every measurement below was taken first-hand
in this session and carries its replay path.

**Owns:** the two-lane sequencing argument and the two corrections.
The defect records D-404 and D-405 own the defects; the beads labeled `x-010` own the
work; the artifacts in `sources` own the measurements they carry.

## The Answer

Concentrate on two lanes, each a ladder whose bottom rungs are cheap and yield a result
on their own, and whose top rungs are named theorems.
Lane A is the proof lane: turn the T-4 instrument into a general unavoidable-set
certifier and falsifier, machine-check the published proofs nobody has ever
machine-checked, then climb to bespoke lower bounds at `n = 12` and the `m = 8` case of
Bentz’s conjecture at `n = 61`. Lane B is the structural lane: reprice the chunk-level
enumeration the queue stopped on an untraceable figure, then climb X-003’s pipeline to a
restricted-class optimality certificate at `n = 11` — the first theorem of Stromquist’s
Theorem 3 shape since 1984 if it lands, and the proposer corpus `BC-090`’s gated search
needs either way.

Everything else is parked with a stated reason, not silently.

Two facts pick these lanes and no others.
First, the field’s division of labor: all twelve record movements of 2024–2026 are upper
bounds from stochastic search (Schadt, Ellsworth, Hajba, the UnitSquare Project, at
`28 <= n <= 88`), the newest mathematics in the archive is asymptotic and disjoint from
`n <= 100` (Bui’s `O(x^0.6)` waste bound, arXiv 2508.04603, and McClenagan’s independent
proof, arXiv 2602.01484), and the exact-value lane has not moved since Bentz 2016: of
the 65 open cases, 63 carry Nagamochi’s one 2005 closed form as their best proved lower
bound, `n = 12` carries a bound proved about `n = 11` and inherited by monotonicity, and
`n = 11` carries this repository’s own H-041 certificate.
The upper-bound lane at small `n` is the one thing the field is currently good at; the
proof lane has been unattended for a decade.
Second, the machinery inventory: the two places this repository is ahead of everyone are
exact certification (fields, intervals, the exact LP with its own phase 1, the T-4
certifier-falsifier pair) and structural description (the chunk census, the scaffold
orbit machinery, X-008’s axis-aligned-residue theorem about the corpus).
The lanes are where those assets point.

## Correction One: the Gap Ranking Ranks a Great Deal (D-404)

`BC-088`’s entry states that the gap between best known and proved lower bound “is about
0.5 for every open case” and that “ranking by that gap ranks nothing.”
Measured over all 65 open cases — `devtools/gap_ranking.py`, added with this document —
the spread is a factor of ten and the ranking is structured:

| `n` | best known | proved lower | gap | form |
| ---: | --- | ---: | ---: | --- |
| 97 | `10` | 9.944272 | 0.0557 | `10² − 3` |
| 78 | `9` | 8.937254 | 0.0627 | `9² − 3` |
| 61 | `8` | 7.928203 | 0.0718 | `8² − 3` |
| 11 | 3.877084 | 3.788854 | 0.0882 | `4² − 5` |
| 96 | `10` | 9.888194 | 0.1118 | `10² − 4` |
| 77 | `9` | 8.874008 | 0.1260 | `9² − 4` |
| 60 | `8` | 7.855655 | 0.1443 | `8² − 4` |
| 95 | `10` | 9.831761 | 0.1682 | `10² − 5` |
| 45 | `7` | 6.830952 | 0.1690 | `7² − 4` |
| 76 | `9` | 8.810250 | 0.1898 | `9² − 5` |
| 32 | `6` | 5.795832 | 0.2042 | `6² − 4` |
| 12 | `4` | 3.788854 | 0.2111 | `4² − 4` |
| … |  |  |  |  |
| 51 | 7.700799 | 7.164414 | 0.5364 | annealing record |

The head of the table is exactly the `k = m² − n` staircase: the three open members of
the `k = 3` line, then `n = 11`, then the `k = 4` line in descending `m`. The “about
0.5” cases are the mid-range annealing and strip records — the subset `BC-088` was
looking at. A narrow gap is not a difficulty estimate (Nagamochi’s bound is simply
tighter relative to `m` at large `m`), but which stratum of this table a case sits on is
precisely what a proof-lane sequencing decision needs, and the entry’s claim erased it.
The impression was conservative — it understated available signal — and it cost
direction, not soundness.
Replay: `uv run --frozen python -m devtools.gap_ranking` from `packing/`.

Adopting Friedman DS7 Table 2’s Trevor Green bounds (think-s1pc) would narrow ~20
mid-table gaps — `n = 17` from 0.513 to 0.230 — and touches nothing at the head of the
table; `n = 31` is the one size where the frontier’s stored bound is better than the
table’s.

## Correction Two: the Enumeration Price Misread Its Artifact (D-405)

`BC-092` was stopped and folded into `BC-090` on “`9.3e9` raw orbit work at `n = 5`.”
That figure appears in X-009, agenda-009, session-049, and the ledger, with no artifact
path beside it — and the artifact says the opposite of what the stop decision took from
it. Session-051 found it by finding its tool (`devtools/price_contact_enumeration.py`):
`atlas/known-best/contact-enumeration-pricing.json` records
`raw_orbit_image_upper_work = 9,296,855,040` at `n = 5` as the price of the *legacy
labeled* route, and its own decision rule at `n = 5` is `enumerate-isomorph-free` —
which reaches the same 11,013 canonical orbits without that work.
(This document’s first version said no artifact existed: a text grep for “9.3e9” cannot
find a record storing the exact integer.
D-405 carries both layers.)
What the scaffold atlas separately records
(`packing/atlas/enumerated/contact-scaffolds-size5.json`): 1,533,696 topology-coloring
candidates at size five collapsing to 11,013 orbits — a measured 139× symmetry quotient
— with 1,705,312 orbit-action images as the work performed.
Two further facts the stop decision did not price: the local realizability prefilter
(`sqpack.contact_realization`) exists and screens scaffolds before any LP is spent, and
`MAX_SCAFFOLD_SIZE = 5` is a typed refusal in `contact_assembly.py`, a constant rather
than a measured wall.

What survives the correction: X-003’s own caution.
Chunk-level stage-1 combinatorics is `8^C(5,2) ≈ 1e9` raw before partition and skeleton
factors, and X-003 already required a finite bound, an orbit count, and an omission
control before implementation.
Applying the measured quotient alone brings `1e9` to `~7e6` before the prefilter —
tractable — but that is an extrapolation from size-five scaffolds, not a measurement.
So the honest statement is narrower than either document’s: the fold of `BC-092` into
`BC-090` is unproved in both directions, and repricing it is a bounded piece of work
(Lane B, rung 0) rather than a settled conclusion.

## Lane A — the Proof Lane

**The ambition:** the first new proved value of `s(n)` since Bentz 2016 — `s(61) = 8` or
`s(12) = 4` — and, on the way, results nobody has: the first machine-verified proofs in
this subject, verified lower bounds past Nagamochi at sizes untouched since 2005, and
the first theorem specific to `s(12)`.

**Why this lane fits this repository.** T-4 is already a proof-lane result produced by
exactly this method: `printed_cover.py` exhibits a strict escaping pose against
Stromquist’s printed Figure 14, and `repaired_cover.py` certifies the repaired cover
exactly over `Q(sqrt 5)` — 2,645 lines whose one defect is being hard-wired to one
figure of one paper.
The published record is checkable and has never been checked: no unavoidable-set proof
in this literature has ever been machine-verified, and this project’s audit hit rate on
printed proofs is one exact gap in Stromquist and four recorded defects in El Moumni’s
route to `s(7)`.

The ladder, each rung a result by itself:

- **A0 — the instrument.** Generalize the certifier: a declared resource system (points,
  weighted points, segments with length thresholds, threshold charges, Bentz-style
  moving families) over `sqpack.field` scalars or rational intervals, a box family at a
  declared container side, a replayable cover certificate.
  Exit: the Stromquist pair replayed through the general instrument — printed refuses,
  repaired certifies, byte-stable.
  The falsifier search half is think-yrvm’s known-answer triple.
- **A1 — audit Bentz `m = 4`.** Section 3 of Bentz 2010 (`s(13) = 4`) is ~126 transcript
  lines, the smallest published proof on the `m² − 3` line.
  Encode and check it.
  Either outcome is a result: the first machine-verified published proof of an `s(n)`
  value, or a printed gap found and repaired — T-4’s precedent, one level up.
- **A2 — past Nagamochi at the Green sizes.** DS7 Table 2’s non-trivial lower bounds at
  ~23 open cases rest on “T. Green, 2000, private communication”: there is no primary to
  read, so certifying sets of our own is the only route by which the frontier can ever
  adopt values there. First targets `n = 17, 18` (Green `≈ 4.4452` against Nagamochi
  `≈ 4.1623`), where DS7’s Figure 34 sketches the shape.
  Every certified value above the closed form moves a verified lane untouched since
  2005\.
- **A3 — the first theorem about `s(12)`.** The best known lower bound for `s(12)` is a
  theorem about a different problem.
  Any bespoke certified bound above `2 + 4/√5 ≈ 3.7889` is the first result specific to
  `n = 12` — a continuum of publishable outcomes between nothing and the full
  `s(12) = 4`, with the low end genuinely reachable.
  The mathematical shape: eleven resources unavoidable at side `> 2 + 4/√5`, found by
  counterexample-guided synthesis — A0’s certifier and think-yrvm’s falsifier as the
  loop, H-006’s LP duals as the candidate generator, H-039 as the registered target.
  An H-034-style fractional-piercing diagnostic at `n = 12` (is `τ* > 11` at side
  `4 − ε`?) tells us early whether pure points can suffice or thresholds and segments
  are forced, and is itself a result about the method.
- **A4 — the peaks.** `s(61) = 8` via H-033: `s(m² − 3) = m` is proved for
  `m = 3, 4, 5, 6, 7` and conjectured for all `m ≥ 3` in Bentz 2016 — a stated
  conjecture, five proved predecessors, the third-narrowest gap in the corpus, and a
  route (encode `m = 7` machine-readably, substitute `m = 8`, falsify each failed
  forcing step before inventing a resource) that is H-033’s registered instrument.
  And `s(12) = 4` — strictly stronger than the proved `s(13) = 4`, which is why it is
  last and not first. Cautions that stand: `n = 12` opens the `k = 4` line, which has no
  proved member and a falsified first index (`s(5) = 2 + √2/2 < 3`); and the `n = 11`
  report’s calibration — do not point a rigorous solver at `s(11)` — is not disturbed by
  anything here.

## Lane B — the Structural Lane

**The ambition:** a restricted-class optimality theorem at `n = 11` — “no packing
expressible as at most `K` chunks with at most two tilt classes beats Trump’s side,”
certified per stratum by exact or interval LP with a coverage certificate over the
symmetry quotient and an omission control on the label generator.
Stromquist’s Theorem 3 (no `0°/45°` packing reaches Trump’s side) is the only theorem of
that shape, from 1984. As a side product, the stratum atlas is the proposer information
`BC-090`’s gated search instrument needs — which contact shapes and angle-class
structures carry records — so the lane feeds the search block without betting on it.

**Why the lane is alive despite BC-092’s stop.** The stop rests on D-405’s figure.
The description side is strong: X-008 proved the corpus’s whole inexpressible residue is
axis-aligned — all 295 tilted components are already inside the grammar — so the
grammar’s coverage question is about axis-aligned polyominoes only.
The generation side has never been run, and its prerequisite stack is further along than
the queue assumed: the orbit machinery is built and measured (139× at size five), the
realizability prefilter is built, the glued-row and sweep designs are specified
(think-vnm5, think-dh4b), and — decisive for the peak — `sqpack.exact_lp` exists,
tested, with its own phase-1 feasibility construction, which is the D-021 fix X-003
named as the prerequisite for certified per-stratum optimality.

The ladder:

- **B0 — reprice.** Chunk-level stage-1, priced in counted LP solves (D-126) with the
  measured quotient and the prefilter applied and an omission-control design stated.
  Output: a go/no-go number for the enumerator, replacing the impression.
  If the number says no, the lane stops at B1 having cost one pricing exercise.
- **B1 — the H-044 verdict.** Are the standing records chunk-expressible at `K ≤ 6` with
  at most two free squares?
  Refutation-first and search-free: measurable from archived geometry.
  The instrument is `chunks.py`’s census upgraded from conservative component-finding to
  the registered exact-cover minimization with typed refusals.
  A refutation kills the ansatz before an enumerator exists — X-003 registered it first
  for exactly that reason.
- **B2–B4 — the pipeline.** Stage-1 enumerator with omission control (think-sfzh), glued
  equality rows validated on the `n = 5`/`n = 10` proved controls (think-vnm5), the
  class-angle sweep driver under X-003’s ranking rule — no stratum triage on aligned
  side values, every survivor gets its sweep (think-dh4b).
- **B5 — the certificate.** The restricted-class statement, gated on one measurement
  this session could not take: exact-LP cost at the full `n = 11` cell scale (T-2’s
  float LP is 1.28 ms there; the exact pivot cost is unmeasured and decides exact versus
  interval certification per stratum).

## Parked, and Why

- **The annealing race (`BC-090`).** Stays exactly as X-009 gated it: no target until an
  instrument beats exp-011’s measured grid-return at `n = 17`. Beating Schadt at
  Schadt’s method with less tuned machinery is the lowest-yield use of this repository;
  Lane B is how a search attempt gets a differential if one is ever taken.
- **`n = 90` / H-049.** A clean finite question (20 squares squeezable in `4 × 6`) and
  it stays registered and queued — but it is an upper-bound construction in the crowded
  lane, not a focus.
- **`BC-089`’s remainder** (think-d0j1, think-3nc4, the `n = 53` refusal).
  Recognition work that finishes on its own momentum; it is between-slices filler, not a
  lane.
- **The asymptotic lane.** Two independent 2025–2026 proofs of `O(x^0.6)` show it active
  and competitive, and nothing here contributes differentially; H-037 stays parked.
- **Full-`n` generative enumeration.** Even after D-405’s correction, nothing suggests
  square-level enumeration at target sizes; B0 prices the chunk level only.

## Weak Points Where Effort Pays Disproportionately

1. **The A0 instrument.** Every rung of Lane A stands on it, and it is a generalization
   of code that already works, not new mathematics.
2. **The escaping-pose falsifier** (think-yrvm).
   The inner loop of synthesis and the audit tool for every published set; its
   known-answer triple is already specified.
3. **One measurement: exact-LP cost at the `n = 11` cell.** Gates B5’s route and costs
   an afternoon.
4. **The square-subsystem selector** (think-mvrq).
   Turns `--strategy interval-existence` from checker-not-built into a generic
   certifier; serves both lanes and the `BC-089`/`BC-090` boundary.
5. **The field seam.** `cases/stromquist` carries a bespoke `Q(√5)` embedding beside
   `sqpack.field`; A0 should consume the shared field layer or record why not — a
   duplicate-arithmetic seam is where a certifier defect would live.
6. **Queue trust.** The gap ranking is now a tool rather than an impression (D-404); 25
   `in_progress` beads from long-closed sessions still distort the ready queue (hygiene
   bead filed).

## Proposed Agenda Adjustments — Enacted Same Day as Agenda-010

*(This section proposed; the owner then directed the mapping, and
[agenda-010](../agendas/agenda-010-two-lane-overnight-run.md) now carries it: the
committed rungs as `BC-093`–`BC-100` with a mid-run checkpoint, the peaks as
`BC-101`–`BC-105` tentative behind it, budgeted to a nine-hour overnight wall.
The numbered proposals below are retained as written.)*

1. Close agenda-009 on its own terms: `BC-089`’s remainder proceeds on think-d0j1;
   `BC-090` and `BC-091` keep X-009’s gates and narrowing untouched.
2. Draft agenda-010 as the two ladders: committed commitments A0, A1, B0, B1 (each exits
   in a result or a typed refusal at tier-S/M cost), with A2, A3 and B2–B5 behind them
   as `tentative` — agenda-009’s own pattern of hygiene-then-decide, applied to
   ambition.
3. Reopen `BC-092` only on B0’s number; until then its stopped state stands with D-405
   noted against its rationale.
4. Raise think-at4f and think-yrvm to the priority the ladder implies (done with this
   document); think-9m9x is sharpened to the Bentz-line route rather than the generic
   61/78/97 sweep.

## Corrections and Repairs Made With This Document

- `frontier/n-012.md` and the `n = 11` report no longer date the `s(m² − m) = m`
  counterexample boundary to Cleemann’s `m = 17`: the retained Kingbird archive records
  Hajba 2015 (`m = 16`), Arslanov 2019 (`m = 12`), and Cantrell February 2025 (`m = 11`,
  `n = 110`). The retained prospective witness screens clean numerically in this
  session: zero containment violation, worst pairwise separation `+7.3e-8`, side margin
  below 11 of `3.2e-3` — a screen, not a verification (think-7x19).
- `frontier/README.md`’s open-case provenance counts now match the records: 14
  hand-built, 10 annealing (nine of the ten dated 2024–2026; `n = 53` is Cantrell 2002),
  5 diagonal strips, 3 extensions, 2 unrecorded.
- X-009 carries a dated correction note for the two premises above; agenda-009’s
  `BC-088` and `BC-092` evidence fields point at D-404 and D-405.
- `devtools/gap_ranking.py` added (OR-1); its durable wiring is a filed bead.

## Addendum: the BC-098 Checkpoint (2026-08-31, 06:26Z)

The overnight run’s mid-run checkpoint, written with blocks 1 and 2 complete about three
and a half hours ahead of schedule.
Four measured facts replaced this document’s forward guesses:

- Both Lane A instruments exist with their controls green in a morning, not a night: the
  certifier core replays exp-016/exp-017 byte-stable, and the falsifier’s triple passes
  with the saturation caveat fixed in code.
- The stage-1 price came back harder than the ladder hoped: exhaustive chunk-level
  enumeration is out of reach above `K ≤ 3` (raw `4.357e20` at `K ≤ 6`; the `K ≤ 3`
  slice under X-008’s measured seatings prices at a `2.250e6` orbit floor), and Trump’s
  own ~five-chunk decomposition sits outside the exhaustive range.
  Lane B’s peak is therefore a `K ≤ 3` restricted-class statement or a pruned-canonical
  enumerator, not the class this document imagined.
- The exact LP at full cell scale costs ~1.4 s per pivot (58.8 s phase 1, 22.1 s phase
  2, first-hand), which decides B5’s route: sweep in float, certify winners exactly.
- D-405 gained a second layer: the 9.3e9 figure has an artifact, and the artifact’s own
  decision at `n = 5` is the isomorph-free route — this document’s first version
  repeated the no-artifact claim, and the amendment is recorded in the defect.

Resequencing: BC-101 (Green sizes) promoted behind BC-099 into the recovered wall;
BC-102 tonight only if wall remains, else the next run’s first slice; BC-103’s sizing
slice authorized as gate filler; BC-104 rescoped to the measured class; BC-105 narrowed
with it. The peaks did not move: the ladder’s direction survives its first contact with
measurement, but Lane B’s top rung is smaller than drawn.

## What This Document Does Not Establish

No mathematical claim is promoted, no hypothesis is adjudicated, and no agenda state is
changed beyond the correction pointers noted above.
The ladders name exits, not predictions: every rung’s negative outcome is a recordable
result, and the peaks are directions rather than commitments.
The `9.3e9` correction says the stop decision was unsupported, not that the enumeration
is affordable — B0 exists because neither is known.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
