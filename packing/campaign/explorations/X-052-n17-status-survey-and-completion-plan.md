---
title: X-052 — The n = 17 Optimality Program on Every Front, and the Path to a Proof
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-052
  title: The n = 17 Optimality Program on Every Front, and the Path to a Proof
  date: '2026-10-09'
  author: Claude Fable 5.1 at max reasoning, W3 insight-iteration lane for the owner, synthesizing two Fable max mathematical reviews (global side and local side) and a Claude Opus 5.5 inventory of the record, issues, PRs and beads; not yet reviewed by the coordinator
  campaign: packing.squares
  brief: >-
    The owner asked for a full W3 exploration summary, end to end: a broad, detailed
    but concise technical survey of the current status of the s(17) = S* program on
    every front, followed by the most promising directions to complete the proof
    efficiently. It is written for tracker issue 405 and for the record. It reads main
    at 6a0499ba4 (the merge of PR 473, 9 October), the three review documents written
    for it on 9 October, and GitHub as of 17:00 UTC. It supersedes the status sections
    of X-051 and extends its directions; it certifies nothing, registers no round and
    changes no bound, verdict or census count.
  sources:
    - packing/campaign/explorations/X-051-n17-optimality-program-review.md
    - packing/campaign/explorations/X-048-n17-optimality-after-n11.md
    - packing/frontier/n-017.md
    - packing/frontier/results.yaml
    - docs/project/n17-optimality-explainer.md
    - packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-274-current-tail-b-replication/current-partition.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-259-current-admitted-residue/partition.json
    - packing/campaign/series/series-000-smoke-and-calibration/results/exp-247-n17-unique-state-cover/run-001/receipt.json
    - packing/campaign/explorations/X051-centre-survivors/centre-survivors.json
    - packing/hosted/n17-x048-session-168-certificates.yaml
    - packing/campaign/intake-watch.yaml
    - packing/campaign/result-requests.yaml
    - packing/campaign/issue-intake/n17-20261008/reconciliation.json
    - packing/campaign/ledger.md
    - packing/campaign/ideas.md
    - packing/campaign/hypotheses/H-261-n17-local-minimum-modulo-sliders.md
    - packing/campaign/hypotheses/H-325-n17-endpoint-state-cap-scan.md
    - packing/campaign/hypotheses/H-330-n17-no-mans-land-map.md
    - packing/campaign/hypotheses/H-337-n11-capture-positive-control.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-245-h265-n17-catalogue-polynomial.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-247-h266-n17-unique-state-cover.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-248-h268-n17-local-half-composition.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-275-h288-capture-cap-root-join.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-276-h289-numeric-cap-first-round.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-280-h291-centered-endpoint-hull-capacity.md
    - packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-311-h-319-c2-full-replay.md
    - docs/project/reviews/review-2026-10-05-guzhou-r071.md
    - docs/project/reviews/review-2026-10-05-n17-capture-r9.md
    - docs/project/reviews/review-2026-10-05-n17-stall-classification.md
    - docs/project/reviews/review-2026-10-03-n17-local-radius.md
    - docs/project/reviews/review-2026-10-03-n17-verifier-rewrites.md
    - docs/project/reviews/review-2026-10-02-n17-depth-width-wall-lemma.md
    - docs/project/reviews/review-2026-10-02-n17-local-half-composition.md
    - docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md
    - docs/project/reviews/review-2026-10-02-n17-widened-projection-scope.md
    - docs/project/reviews/review-2026-10-02-n17-kernel-adaptation-spec.md
    - docs/project/reviews/review-2026-10-02-n17-residue-process.md
    - docs/project/reviews/review-2026-10-02-n17-unique-state-cover.md
    - docs/project/reviews/review-2026-10-04-n17-streamed-verifier.md
    - docs/project/reviews/review-2026-10-07-n17-pr410-integration.md
    - docs/project/reviews/review-2026-10-08-n17-issue-pattern-reconciliation.md
    - docs/project/research/research-2026-10-07-n17-proof-interfaces-and-lp-contract.md
    - packing/devtools/verify_n17_kernel_certificate.py
    - packing/devtools/verify_n17_bb_certificate.py
    - packing/devtools/census_n17_certified.py
    - packing/devtools/reconcile_n17_issue_patterns.py
    - packing/src/sqpack/hull_kernel/producer.py
    - https://github.com/jlevy/squares/issues/405
    - https://github.com/jlevy/squares/issues/413
    - https://github.com/jlevy/squares/issues/472
    - https://github.com/jlevy/squares/issues/358
    - https://github.com/jlevy/squares/issues/367
    - https://github.com/jlevy/squares/issues/400
    - https://github.com/jlevy/squares/issues/445
    - https://github.com/jlevy/squares/issues/375
    - https://github.com/jlevy/squares/issues/419
    - https://github.com/jlevy/squares/pull/473
    - https://github.com/jlevy/squares/pull/461
    - https://github.com/jlevy/squares/pull/452
    - https://github.com/jlevy/squares/pull/410
  proposes: [H-341, H-342, H-343, H-344, H-345, H-346, H-347, H-348, H-349]
---
# X-052: The n = 17 Optimality Program on Every Front, and the Path to a Proof

**The proof of $s(17)=S^\ast$ has two real gaps, both measured now, and neither moved
this week: exclusion of the hard tail of the residue, where the engines in hand have
been run on four of 95 states, and capture of the family’s own state from its cells,
where the only engine in hand has been run for one round.** Everything else is in place
or priced. The bracket is verified at both ends.
The cover, the census and the transfer rules reproduce from independent code.
Sixty exclusions are admitted and leave 36,768 states in 4,683 orbits; 58 of the 60 rest
on one verifier implementation whose objects nobody can fetch.
The endpoint’s algebra, the local family theorem and the cap joins are exact and were
re-derived independently on 9 October without finding a defect.
A contributor has produced, with this repository’s own producer and verifier, twelve
kernel certificates that would remove 22 per cent of the residue for two CPU-hours of
replay, and the tracker does not mention them.

This report is the status survey the owner asked for, by front, with each claim labelled
by the kind of evidence behind it, followed by the corrections the two 9 October reviews
found in the record, the minimum set of mathematical results still needed, and a
sequenced plan in parallel lanes.
It supersedes the status sections of [X-051](X-051-n17-optimality-program-review.md) and
extends its directions; X-051’s analysis of the architecture, its relaxation results and
its foolproof-package table stand and are cited, not repeated.
Every number below is the 60-entry ledger’s on `main` at `6a0499ba4` unless a date says
otherwise. Numbers computed by the reviews rather than by a registered round are marked
*(review)* and the method is stated; [Evidence Status](#evidence-status-and-limits)
lists them all.

## 1. Where n = 17 Stands

The vocabulary, from the explainer and X-051, with one distinction added: *proved*
(exact hand argument, scope stated), *verified* (exact computation replayed
independently of its producer), *single-impl* (machine-verified by one implementation
only), *admitted* (a standing verifier’s full pass under the ledger’s rule),
*conditional* (true under a guard nothing yet delivers), *reported* (a source’s claim
not replayed here), *open*.

| Quantity | Value | Status |
| --- | --- | --- |
| Bracket | $4.66044275 < s(17) \le 4.6755300936045509516342148538535054$; gap $0.0150873$ | verified (T-093 `V3/C3`; T-065 `V3/C3`) |
| Target | $S^\ast$, the unique root of the catalogue’s irreducible degree-18 polynomial in $(4.667, 4.75)$, $S^\ast = 4.675530093604550951634111270\ldots$ | proved (exp-245), re-derived *(review)* |
| Caps | exclusion $U = 1169/250$, $U - S^\ast = 4.6991\times10^{-4}$; capture $U' = V = 935106018721/200000000000$, $V - S^\ast = 4.4905\times10^{-13}$ | verified (exp-275), re-derived *(review)* |
| Cover | 24 closed capacity-one cells; $\binom{24}{17} = 346{,}104$ states; 43,593 $D_4$ orbits; the family in one state with margin at least $0.002111$ | verified twice (exp-247; two independent recomputations) |
| Admitted exclusions | 60 entries: 2 of arity 6, 10 of arity 7, 8 of arity 8, 1 of arity 9, 39 whole states | admitted; W7 and A re-proved by second implementations, 58 single-impl |
| Residue | 36,768 states, 4,683 orbits, the family’s state among them | verified (census tool; recomputed *(review)* from the receipt and ledger) |
| Residue by $D_4$-Hamming distance from the family’s state, orbits / states | 0: 1 / 8 · 2: 95 / 744 · 4: 975 / 7,664 · 6: 1,942 / 15,268 · 8: 1,284 / 10,124 · 10: 385 / 2,956 · 12: 1 / 4 | verified *(review)*, agrees with exp-259 at 58 entries except the two distance-8 orbits Tail A and B removed |
| Hard tail, measured | per-state runs on 4 of the 95 distance-2 orbits: 1 closed, 1 incomplete at 7,000 s, 2 fixed points at 32 uniform bins | open; undersampled |
| Local family theorem | capture-target theorem at $r = 1/5000$ on $B_W'$, worst ratio $0.925931$; per-coordinate vector with floor $1/1216$, worst ratio $0.999368$, unregistered | proved with one review; replayed from `main` *(review)* in 10 s each |
| Capture | from the cells: one round (exp-276, 277, 280), nothing contracted; from a $1/1024$ box: pilot 2 met its falsifier; cells are 90 to 4,800 times the terminal radius away in every coordinate | open; no engine has a verdict from the real start point |
| Contributor certificates, unadmitted | #472: 12 kernel certificates, standing verifier full pass reported; #413: 38 rows; #358: 2 BB classes | reported; admission of #472 would leave 3,636 orbits / 28,528 states *(review)* |
| Custody | 204 admitted objects, 2,167,361,631 bytes, listed by digest; the release has 0 assets; three Session-184 release tags do not exist | the admitted census is not replayable from a fresh clone today |
| Composition | no checker reads cover, ledger, capture and local receipts together; caps are implicit ($U$) on every entry | absent |

**The two real gaps.** (1) The 4,682 non-endpoint residue orbits need certificates at a
cap at least $S^\ast$; the 95 distance-2 orbits are the hard core, and on the two
diagnosed ones the infeasibility is joint across at least 15 squares and invisible to
every pairwise or centre-only method.
(2) Every packing of side at most $U'$ in the family’s state must be shown to lie within
the terminal radii of the family in the exact root’s frame; no engine has contracted
anything from the cells, and the terminal region is $10^{-3}$ to $10^{-4}$ per
coordinate.

**The single biggest near-term lever.** Admit #472’s twelve kernel certificates (clean
replay, Rust parity, custody) and regenerate the BB-only #413 rows that have a wall cell
with the repository’s own kernel producer: about 12 CPU-hours for a residue of about
2,400 orbits, with the distance-2 tail at 94. It is the only exclusion lever in the
record that is priced, and it uses the standing admission path unchanged.

## 2. Status by Front

### 2.1 Bounds and the lower-bound lineage

| Claim | Status | Evidence | Concern |
| --- | --- | --- | --- |
| $s(17) > 18641771/4000000 = 4.66044275$ (T-093, Guzhou0806 R071) | verified `V3/C3/S2`: both source checkers replayed over 5,114 intervals, 227 ledger rows reproduced by a code-free sweep | [n-017](../../frontier/n-017.md), [R071 review](../../../docs/project/reviews/review-2026-10-05-guzhou-r071.md) | one event-cell method; the native route cannot read weighted and winning-subset features, so no method-distinct decision |
| Lineage T-041 (Kleddamag 4.66001, 27 Sep) → T-043 (R068 4.66044, 28 Sep) → T-093 (R071, replayed 5 Oct) | verified | PRs 236, 241, 362 | none |
| R071’s charge cannot prove any $T \ge T' = 4.660442775$: the obstruction parent’s open charge $999{,}880{,}603 < M/17 = 1{,}000{,}026{,}408.47$ with $M = 17{,}000{,}448{,}944$; runway $T' - T = 1/40000000 = 2.5\times10^{-8}$ | verified *(review)*, exact integers | R071 review; `root_and_caps.py` | none; a further counting step needs a new charge |
| Charge floors at the cap (H-262) and any single $D_4$-symmetric linear floor leave at least 30,966 orbits | refuted / proved ceiling | exp-243 | asymmetric and nonlinear floors untested; H-338 is the state-conditioned version |

Remaining obligation: none on this front for the optimality proof.
The gap $S^\ast - 4.66044275 = 0.0150873$ is closed by exclusion and capture, not by
counting; the cap ladder (H-326) would move the verified bound by about
$5.1\times10^{-3}$ if every residue orbit closed at $V_1 = S^\ast - 10^{-2}$, and its
certificates do not enter the optimality proof.

### 2.2 Upper construction, exact endpoint and algebra

| Claim | Status | Evidence | Concern |
| --- | --- | --- | --- |
| 17 unit squares fit in side $4675530093604551/10^{15}$ (rational witness) | verified; re-verified *(review)* with an own exact SAT: 17 squares inside, no overlaps, minimum separation $1.03\times10^{-17}$, no touching pair | exp-235 | strictly interior, so a ceiling and not the endpoint |
| The exact endpoint is feasible at the chart root; $s(17) \le 4.6755300936045509516342148538535054$ (T-065) | verified: 36 exact identities and 168 interval bounds, independent audit; consistent *(review)*: at the root-box midpoint, exactly the 21 recorded contact pairs and 15 wall anchors, no violation beyond $10^{-18}$ | exp-237 (two implementations), exp-238 | the register’s T-065 claim text still says the catalogue identity is unproved ([Section 3](#3-corrections-to-the-record)) |
| $S^\ast$ is a root of the catalogue’s degree-18 polynomial, irreducible over $\mathbb{Q}$ (H-265) | proved; re-derived *(review)*: one degree-18 factor, exactly four real roots in $(-3,-2)$, $(4.667,4.75)$, $(4.75,5)$, $(5,6)$; $S^\ast$ is the unique root in $(4.667,4.75)$, enclosed to width $6\times10^{-44}$ | [exp-245](../series/series-000-smoke-and-calibration/experiments/exp-245-h265-n17-catalogue-polynomial.md) | “the correct ordered root” is unambiguous and should be stated as such in the final statement |
| Gensane–Ryckelynck’s decimal $4.6755300960455$ is wrong: $P = 56.9$ there against $-2.2\times10^{-5}$ at the catalogue decimal | verified | n-017 | none |
| Chart identity $S = (6+4t)/(1+2t-t^2)$, $t = \tan(\theta/2)$; at $S^\ast$ the smaller root $t^\ast = 0.36204389331432338$ gives $\theta = 39.8049589797678^\circ$; $F'(t^\ast) = -1.234 < 0$ | verified *(review)* | H-288 | the second $t$-root ($\theta \approx 76^\circ$) is excluded by the exp-237 box |
| Cap join: $0 < V - S^\ast \le 10^{-12}$, $V \le U$, $\sigma = (U-S^\ast)/2 = 2.3495\times10^{-4}$; first-order feasible radius along $-\omega_{11}$ is $0.083$ at $U$ and $7.9\times10^{-11}$ at $U'$ | verified (exp-275, 25 controls); re-derived *(review)* | [exp-275](../series/series-000-smoke-and-calibration/experiments/exp-275-h288-capture-cap-root-join.md) | the explainer’s “about $2\times10^{-10}$” uses the $10^{-12}$ allowance; immaterial |
| Whether the certified configuration is the pictured packing contact for contact | open | n-017 | irrelevant to optimality |

Remaining obligation: none mathematical.
Two registration decisions: restate T-065’s claim text (the identity is proved; the
decimal is a ceiling on $S^\ast$), and write the final statement with $S^\ast$ as “the
unique root of $P$ in $(4.667, 4.75)$”.

### 2.3 Cover and census

| Claim | Status | Evidence | Concern |
| --- | --- | --- | --- |
| 24 strictly convex closed cells inside $[1/2, U-1/2]^2$, $D_4$-invariant about $(U/2, U/2)$, union area exactly $844561/62500 = (U-1)^2$, 20 positive-area pair overlaps, no triple | verified *(review)* from the exp-247 receipt’s polygons alone, importing nothing | [exp-247](../series/series-000-smoke-and-calibration/experiments/exp-247-h266-n17-unique-state-cover.md), `cover_census_check.py` | none |
| Capacity one: interior cells by squared diameter $29377/31250 = 0.940064$ (axis) and $2502024804841/3369608000000 = 0.742527$ (diagonal); wall cells by the depth-width lemma at $(d,w) = (79/100, 79/100)$, $(911/1000, 529/750)$, $(93/100, 257/375)$ | proved and verified; the lemma re-derived *(review)*; a 600-start numeric attack per cell reaches best gaps $-0.0116$, $-0.0036$, $-0.0035$ below the review’s exact maxima, and the two refused controls give $+0.0023$ and $+0.0290$ | [wall lemma review](../../../docs/project/reviews/review-2026-10-02-n17-depth-width-wall-lemma.md) | the unique-state review calls $29377/31250$ a squared diameter of $0.969569$; $0.969569$ is the diameter (cosmetic) |
| Burnside: fixed 17-subsets $346{,}104, 0, 0, 0$ and $660$ per reflection; $348{,}744/8 = 43{,}593$; brute-force canonical forms agree | verified three times | exp-247; two review scripts | none |
| The family lies in exactly one state, margin $\ge 0.002111$; square 6 in a declared box | verified with one review | exp-247 `unique_state` | square 6’s full freedom at side $\le S^\ast$ is discharged by the exclusion of the distance-2 states, not separately: a linked obligation, not an independent one |
| Existential closed-cell assignment: every packing of side $\le U$ in $[0,U]^2$ realises a state; overlaps give several states, harmless for exclusion | proved | lemma review §3 | none |
| Residue 36,768 / 4,683, endpoint untouched; W7 alone 133,152 states / 16,701 orbits, A 110,448 / 13,897, SW9 43,772 / 5,499; the 39 whole-state entries remove 304 states | verified *(review)* by independent containment code; the census tool on this worktree agrees | `census_n17_certified` | none |

Remaining obligation: none.
The front is finished at the evidential level a foolproof package needs, short of Lean
for the wall lemma (H-333).

### 2.4 Exclusion certificates and the trusted computing base

What a certificate proves, and on what premises, is reviewed in X-051 §2.3 and the
[kernel adaptation spec](../../../docs/project/reviews/review-2026-10-02-n17-kernel-adaptation-spec.md);
the global-side review found no gap in the ownership induction’s grammar and confirmed
transfer by containment and $D_4$ as a one-line proof.

| Component | Lines | Passed the admitted objects | Independent checks | Risk |
| --- | ---: | --- | --- | --- |
| Cover checker | 1,437 | one tool | five review scripts, the lemma review, the review’s own script | low |
| Census consumer | — | one tool | two review `transfer_count` scripts, the review’s containment code, the contributor’s own counts | low |
| Kernel verifier `verify_n17_kernel_certificate.py` | 1,751 | the standing verifier; W7 also by lane R3’s separate verifier | 34-case mutation suite refused by the Python and the Rust verifier; Rust port (PR 410) with receipt parity on 7 certificates; three closed-cover defects found and fixed on 3 October | **58 of 60 admissions rest on one implementation**, and its early versions had unsound branches |
| BB verifier `verify_n17_bb_certificate.py` | 1,321 | the standing verifier; A also by lane R4’s separate verifier | 16 mutants, 9 doctored certificates | one admitted object; `think-t41a` (source-cell enclosure) open for external intake |
| Hand lemmas | — | — | wall lemma reviewed and attacked numerically; transfer and monotone embedding are one-line | low |
| Custody | — | — | 204 objects / 2.17 GB listed by SHA-256; release `data/n17-x048-session-168-certificates-v1` has 0 assets; tags `…conditional-owned-hull-v1`, `…numeric-cap-readiness-v1`, `…tail-a-dependencies-v1` return 404 | **every admission is a receipt, not a replayable object** |

Verifier versions, read from the ledger and `git ls-tree` on this worktree: the ledger
lists seven verifier revisions; every kernel admission since exp-251, Tail A and B
included, was passed by `kernel-streamed` (commit `601bbf110`, blob `1ad706c21`),
`dirty: false`. `main`’s kernel verifier is blob `be8135f6e`, three commits later
(`836e919e0`, `90d6e4c94`, `90cd2528e`: centred-cap support with a 48-vertex hull
allowance and a sound Y-range prefilter whose measurement round exp-298 ended invalid),
and **no ledger listing names it**; under the ledger’s own rule, no receipt from current
`main` can admit an entry until a listing with a review pointer exists.
The BB verifier moved the same way: listed `651c2615c`, `main` blob `e6e400e7f` after PR
452, and every contributor BB receipt names `9dcc05bc…`, an unlisted intermediate.

Remaining obligation: a verifier listing for `be8135f6e` (a review of three commits);
custody of the 204 objects (H-336); Rust parity on all 60 (H-335); the BB header
enclosure guard for every external BB intake (`think-t41a`).

### 2.5 The hard tail: what was actually tried

The 95 distance-2 orbits (744 states) are the one-square moves of the family’s state
that survive the ledger; 22 of the 117 moves are excluded by admitted sub-patterns.
The exhaustive record of attempts on them:

| Attempt | Instrument | Result |
| --- | --- | --- |
| H-273 float survey, all 95 | `survey_n17_residue --distance 2` | no placement at $U$ in 95 searches; sampled best penetration $9.1\times10^{-3}$; unresolved by design |
| u8 = mask 3078077 | 17-owner kernel, SW9 adaptive recipe, 7,000 s | **closed** in 572 s, verified in 277 s, admitted ([exp-257](../series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md)) |
| u1 = mask 1900509 | same | incomplete at 7,001 s, not a fixed point |
| m1964767 | 17-owner kernel, N1 recipe, 32 uniform bins | fixed point after 8 rounds; consistency-limited |
| m851903 | same | fixed point after 2 rounds (88 s); consistency-limited |
| exp-303 contact rank, exp-304 envelope windows, exp-308 four-corner cardinality, exp-312 saved-pose incircles, exp-313/314 projections | necessary-condition filters | all 95 survive each |
| centre-only relaxations (W2 review, X-051 §3.1; replayed and extended *(review)*) | exact rational centres in each state’s own cells | all 95 survive with exact witnesses; see [2.6](#26-relaxations) |

Everything else in Sessions 184 to 186 (the fifteen `criterion_missed` rounds exp-285,
286, 287, 291, 292, 293, 295, 297, 300, 301, 303, 304, 305, 308, 312 and the five
accepted conditional rounds exp-288, 296, 299, 302, 307) worked on the family’s own
state at the numeric cap under a guard on owner 0 at $\tau = 53/128$: capture work that
never touched a tail state.

**Finding.** X-051 §2.2(3) says the 95 “resist the pairwise kernel at every row width”.
The evidence is two fixed points at 32 uniform bins, one incomplete adaptive run and one
closure. The adaptive recipe that closed 26 of 29 counted H-275 draws has run on two of
the 95, never at the 2,304-row cap or past a 7,000 s ceiling.
**The hard tail is undersampled, not measured.** The consistency-limited diagnosis
(every owner at least 63 per cent supported on 100 float-sampled poses) is a strong
reason to expect m1964767 and m851903 to resist pairwise propagation, and says nothing
about the other 91.

**Why the two diagnosed states resist.** Their structure is three full walls, five
squares on a wall of length $3.676$, whose neighbours fail to clear each other by
$0.011$ to $0.018$; the family resolves the same crowding by tilting one square per full
wall (square 13 at $39.8^\circ$, square 16 at $-36.6^\circ$), and a one-square move
breaks the pattern that makes the tilts consistent.
The float survey places a 14-cell sub-pattern of m1964767 and finds m851903’s minimal
infeasible sub-pattern at arity 15: whatever excludes them needs at least 15 squares
jointly.
A pairwise cut removes a pose only when every partner pose collides with it, and
an ownership induction has no owned points for most side cells from the seed.

**Margins.** Float penetrations at $U$ for distance-2 states are $0.009$ to $0.012$ of a
side, the same order as W7’s ($9.0\times10^{-3}$) and A’s ($8.8\times10^{-3}$), both of
which closed, and ten to twenty times the cap slack $4.7\times10^{-4}$; the engines’
resolution floors ($10^{-3}$ at $1/512$ rows; the BB chord error $gx^2/2$) are below
these margins. What is missing is reach, joint facts about orientation-dependent extents
along full walls, not resolution.

Remaining obligation: 95 distance-2 orbits (94 after #472), with per-state verdicts on
four; the engines’ stall fraction on the *current* residue is unmeasured.

### 2.6 Relaxations

| Claim | Status | Evidence | Concern |
| --- | --- | --- | --- |
| Every distance-2 representative, the first eight included, has exact rational centres in its own cells pairwise at distance $\ge 1$, accepted by `build_model` and `check_primal`; minimum squared distance over all 96 retained vectors $501001/500000$ | determined (W2 review; replayed *(review)* in 40 s with an independent point-in-cell test) | X-051 §3.1, [`centre-survivors.json`](X051-centre-survivors/centre-survivors.json) | registration only (H-328, blocked on an OR-1 tool) |
| No weighted-vertex or SOS certificate of any order, with or without a ball, exists for any of the 2,024 cell triples: each has a product vertex with all three squared distances $\ge 562823713/423200000$, a feasible point of its encoded system | determined (exact) | X-051 §3.2, PR 464 | none |
| **The centre-only relaxation is loose by a factor of at least three, not tight.** Maximising the minimum pairwise centre distance over centres in their own cells, then rounding to a $10^{-6}$ grid pulled inward and certifying in exact rationals: every distance-2 state admits exact centres pairwise at least $1.0305$ apart (worst, mask 3062655; median slack $0.0835$; the family’s own state $1.102$), against a true infeasibility margin of about $0.01$ of a side | determined *(review)*, exact witnesses for all 95 and the endpoint control | `centre_relaxation_slack.py`, `exact_slack_witnesses.py` | a strengthening that keeps only centre information cannot come within that factor; the information that excludes these states is the orientation-dependent extent of a square ($1/2$ on edge normals, $\sqrt2/2$ on diagonals) |
| Pairwise orientation coupling at the relaxation optimum is weak: at centre distance $1+\delta$ with $\delta \approx 0.03$ to $0.12$ the relative orientation is confined to $4^\circ$ to $17^\circ$ mod $\pi/2$ and the separating normal to within $14^\circ$ to $27^\circ$ of the connecting direction | derived *(review)* | same | a per-pair orientation argument is not the mechanism either |

What can still bite: joint branching on orientations with wall coupling (the BB;
B2-aimed splits reached closing depths 12 to 14 on arity-7 crowds; its tree size on 15
to 17 squares is unmeasured); ownership induction with closed half-cell branch
predicates (C5), the one grammar change aimed at the diagnosed mechanism, never built; a
state-conditioned charge (H-338), unbuilt.
What cannot: any centre-only relaxation; any pairwise consistency pass at any row width
on the two diagnosed states; a per-pair orientation argument at the relaxation’s
optimum.

### 2.7 Contributor and external work

| Source | What exists | Status here | Projected residue if admitted *(review)* |
| --- | --- | --- | --- |
| **wand125, [#472](https://github.com/jlevy/squares/issues/472)** (9 Oct, unlabelled, no maintainer reply) | 12 arity-8/9 kernel certificates made with `check_n17_subpattern` mode A, each passed by `verify_n17_kernel_certificate` in full (blob `1ad706c21`, the listed `kernel-streamed`); 411,682,476 bytes; producer 139–1,065 s and verifier 147–1,618 s each, 6,794 s summed; hosted on the contributor’s releases with HostedData/v1 manifests; receipts carry `dirty: true`, a wrapper revision and one hand-edited `directory` field each | reported; not in #405, `result-requests.yaml` or `intake-watch.yaml` | **3,636 orbits / 28,528 states** ($-1{,}047$ / $-8{,}240$); distance partition after: 2: 94/736 · 4: 940/7,384 · 6: 1,639/12,880 · 8: 799/6,296 · 10: 162/1,220; row 23 (m935012) removes the distance-2 orbit 1965787; row 34 is contained in admitted `s182-m7844815`, which it subsumes; the contributor’s 58-ledger figures 3,638 / 28,544 reproduce exactly |
| **wand125, [#413](https://github.com/jlevy/squares/issues/413)** (38 rows) | 2 BB standing-FULL (rows 1, 2, at unlisted `9dcc05bc…`); 2 parallel-node (3, 4); 20 fast-verifier only; 11 kernel FULL (= #472); 3 computed (15, 27, 33; row 33 about 480 GB as BB, now being retried with the kernel producer) | reported; the maintained `reconcile_n17_issue_patterns` hard-codes 33 rows and refuses the roster | all 38: 2,345 / 18,360; rows 1–2 alone: 4,641 / 36,452 |
| **wand125, [#358](https://github.com/jlevy/squares/issues/358)** | C1, C2 (arity 7, BB/v1, 552 objects / 400 MB), contributor FULL at `9dcc05bc…`; maintained C2 replay INCOMPLETE at 480 s on the RSS-monitor timeout (exp-311, H-319), not on memory; `think-b0ef` holds the repair | reported | 21 orbits / 148 states alone; nothing beyond the 38 rows’ union |
| **wand125, [#367](https://github.com/jlevy/squares/issues/367), [#400](https://github.com/jlevy/squares/issues/400), [#445](https://github.com/jlevy/squares/issues/445)** | B2/B2d branching (trees 11× and 14× smaller on C1/C2, 30,822 against 41,958 nodes on A); parallel standing driver and an independent Rust BB checker; node-lifetime defect, fixed by PR 452 | B2 unadopted (`think-x4v4`); driver and Rust BB checker unreviewed; #445 closed | — |
| Everything reported (38 rows + C1/C2 + m6177056) |  |  | **2,343 / 18,344**; by distance 2: 94/736 · 4: 835/6,556 · 6: 990/7,768 · 8: 361/2,824 · 10: 61/448 · 12: 1/4; the first eight untouched |
| **Guzhou0806 / N17 project** | R071 → T-093; PR 408/409 merged 9 Oct; PR 402 superseded, its hull-pull repair on `main` as `917163641`; external executor on `think-juy9` | current verified lower bound | — |
| **Kleddamag** | T-041 and the earlier rungs; untagged $4.6601$ (below verified); a “full-proof research checkpoint” (global anchors, one-square pose atlas, joint geometry, fixed-angle LP, conditional exclusions, no bound), read 5 Oct | recorded in `intake-watch.yaml`; the only known external attempt at the global proof, not evaluated against this program | — |
| **evand** | #375 n17 exact certificate, expressly held (`think-00e3`); #419 degree-18 exact form, Lean feasibility | integration via PRs 403/435 (#403 is now MERGEABLE/CLEAN with 31 checks passing) | — |
| Mira, MacIver, Burns/Massaccesi, anabologyco-maker, ahyangyi | historical lower bounds below the verified one | recorded in n-017 | — |

The routing fact of the month, from #472: twelve of twelve arity-8/9 selector flags with
wall cells closed under the kernel in minutes with certificates of tens of megabytes,
where the same patterns as BB certificates run to tens or hundreds of gigabytes.
Kernel arity-8/9 sub-pattern: producer 2–18 min, verifier 2–27 min, 10–66 MB, 2–465
orbits each. Whole-state kernel: 0.44 CPU-hour median, 8 states each.
BB arity 7: $10^5$ to $10^6$ nodes at 37 ms per node to verify; arity-8 crowds up to
$10^8$ nodes.

Remaining obligation for admission of #472: a clean-worktree full replay (about 1.9
CPU-hours at the contributor’s timings) under a listed verifier blob, Rust parity on all
twelve (minutes each), objects hosted under a manifest the census can read and check
byte for byte, an admission round; the endpoint-state control (none of the twelve
touches the family’s state).
Mathematically nothing more: the verifier binds the cover’s 24 polygons, the cap and the
mask, and derives closure itself; the producer’s identity is irrelevant to soundness,
and the format and frame are those of 59 admitted entries.

### 2.8 Capture

Capture must show that every packing of side $\le U'$ in the family’s state, placed in
$C(U')$ with the cells in the $U$ frame, has its 45 non-slider coordinates within $r_j$
of $F(w)$ in the exact root’s frame (angles as H254 lifts) and square 6 in `side-S2`.

| Item | Run | Showed | Status |
| --- | --- | --- | --- |
| Two-cap design | H-288 / exp-275 | at $U$ the feasible set extends $0.08$ along $-\omega_{11}$; at $U'$ about $8\times10^{-11}$ | verified |
| From the cells at $U'$ | exp-276 / 277 / 280: one round of 16 owner updates (175 s), fresh replay, 49 root-relative intervals, centred control PASS_STALL | every owner’s orientation interval whole, every position its cell, all four terminal predicates false | readiness only; **one round ever run** |
| From a $1/1024$ box at $U'$ | pilots 1 and 2, 14 + 17 rounds, up to 4,664 live rows | no two-sided position extent moved; wall-fed one-sided bounds converged to $-1.26\times10^{-4}$ (the $2^{-12}$ pull); turn ranges $2\times10^{-3}$ to $2.8\times10^{-2}$, fixed across row widths | falsifier met; R9 leaves readings A (row-driven, needs $\ge 290$ row widths) and B (box-set fixpoint) open, B favoured by every number |
| Hull-pull repair ($2^{-12} \to 2^{-18}$ first) | `917163641`, 7 Oct | fixture recession $1.22\times10^{-4} \to 2.2\times10^{-6}$ | **merged on `main`** (`FINE_HULL_PULL = 1/2^{18}` in `producer.py`; ancestor of `6a0499ba4`) |
| n11 positive control through the n17 producer (H-337) | exp-268: first round only | 11 owner updates, readiness | 15-round contraction control **not run**; runnable now |
| R9 stage 1 (angle ranges at 2× and 4× rows from the box) | not run | — | open |

**Quantified gap** *(review, from the record’s slopes and the pilots’ receipts)*:

| Start → target | Angle factor (bisections) | Position factor (halvings) |
| --- | --- | --- |
| cells ($\pi/4$; cells $0.7$–$0.97$) → $r = 1/5000$ | 3,900 (11.9) | 3,500–4,800 (≈12) |
| cells → $1/1216$ vector (angles $8.2\times10^{-4}$, $\omega_{11}$ $4.4\times10^{-3}$) | 960 (9.9); $\omega_{11}$: 180 | 1,000 (10) |
| cells → widened LP region (angles $5\times10^{-3}$, centres $10^{-2}$) | 157 (7.3) | 70–97 (6.5) |
| pilot-2 end → $1/1216$ vector | 2–33 | 1.2–3 |
| pilot-2 end → widened region | 0.4–5.6 (axis squares inside; 9, 10, 16 not) | inside |

Even the widened terminal theorem leaves seven bisections in every angle and six
halvings in every position from the cells.
The no-man’s-land, direction by direction, with $\kappa_j$ the fixed-feature LP slope
and $d_j = m/\kappa_j$ the displacement at which a margin $m$ above $U'$ becomes
visible: $-\omega_{16}$ ($\kappa = 0.0155$) needs $d = 0.65$ at $m = 10^{-2}$ and
$0.065$ at $m = 10^{-3}$; $-\omega_{11}$ ($0.0876$) $0.114$ and $0.011$; $+\omega_{13}$
($0.102$) $0.098$ and $0.0098$; the stiffest, $-\omega_{12}$ ($0.71$), $0.014$ and
$0.0014$. So at $m = 10^{-2}$ every angle direction has
$d_j \ge 0.014 > 5\times10^{-3}$, outside the widened box; only at $m \lesssim 10^{-3}$,
the kernel’s measured loss floor at $1/512$ rows, do the stiff directions fall inside.
The soft block directions ($-\omega_{16}$, $-\omega_{11}$, $+\omega_{13}$) need a
non-margin argument between $5\times10^{-3}$ and $0.01$ to $0.07$ rad under any
plausible $m$: the feature-flip atlas (H-339) or a bigger terminal theorem along those
directions.

Routes, assessed: (a) pairwise ownership induction from the cells, the n11 engine
(contracted at n11 in 14 rounds), untested from the real start point at n17; the n11
control (H-337) and a 15–20-round cell-seeded run decide it for hours of CPU. (b)
Box-seeded pilots: four runs agree with reading B; low value until (a) is answered.
(c) Dual-sheet patch certificate over the feature-forced region (H-329): sound in
principle, exact rational duals per direction patch plus interval Hessian bounds, apex
needing no subdivision; risks are dual degeneracy at the apex (optimal face of dimension
about 17), the unknown softest *direction* on $S^{15}$, and feature forcing established
only conditionally (H-278); the interval machinery exists (exp-263, 267, 269), the
direction-patch certifier and the patch counter do not.
(d) Branch and bound over angles with Taylor-at-centre fixed-feature LP bounds,
second-order convergent, closing when the bound exceeds $U'$ and stopping inside the
terminal region: the only candidate with a soundness story for the
cells-to-feature-forced bridge; node count unknown, a Knuth estimate is “days of build,
minutes to run”. (e) Feature-flip atlas (H-339): extends the LP region to about
$2\times10^{-2}$; the inner edge of (d), not a bridge.
(f) Interval Newton or Krawczyk on the family: the wrong tool for an inequality
statement (it certifies uniqueness of the tight-contact *equality* system), with the
same conditioning; right inside (c) for the parametric dual solve.
(g) A larger ratio-test radius: capped by the C7 constants at about $1/4391$ uniform and
$1/1216$ per coordinate; a finer curvature lemma buys at most 2–4×.

Remaining obligation: the whole of it.
Nothing has contracted from the cells; the terminal target is $10^{-3}$ to $10^{-4}$; no
capture receipt computes the conversion allowances $E_j$ the composition needs.

### 2.9 The local family theorem

| Claim | Status | Evidence | Concern |
| --- | --- | --- | --- |
| Capture-target theorem: a packing of side $s \le S^\ast$ in the family’s state, concentric in the cover frame, with its 45 non-slider coordinates within $r_j$ of the family’s at the exact root, has its slides in $B_W'$, the sixteen squares other than 6 exactly at $x^\ast(w)$, and $s = S^\ast$ | proved with one review; exact certificates C1–C4, C6–C11 (exp-244 on $B_W$, exp-248 run-002 on $B_W'$): 45 lifts, rank 45, 125 options negative with Taylor margins, per-cell affine duals ($2^{-44}$ dyadics) on 93 cells, ratio test; replayed from `main` *(review)*: worst $0.925818092269$ ($B_W$), $0.925931049178$ ($B_W'$), 10 s each | [exp-248](../series/series-000-smoke-and-calibration/experiments/exp-248-h268-n17-local-half-composition.md), [recipe review](../../../docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md), [composition review](../../../docs/project/reviews/review-2026-10-02-n17-local-half-composition.md) | hand lemmas 1–6 have one AI review; lemmas 2 and 5 and the curvature bound now have a second derivation *(review)*; no defect found |
| Slide coverage (H-268): $a \in [0, 23/200]$, $b \in [b^\ast, 37/500]$, $z \in [-49/1000, 0.0241]$ with square 6 in its cell | verified (exact/outward, 3 controls); replayed at $R = 9/2048$ *(review)*, 8 s | exp-248 run-001 | the separation lemma is sharp; a widened neighbourhood needs new coverage |
| Per-coordinate vector: floor $1/1216$ on $B_c$, $\omega_{11}$ at $85/19456$, $u_{11}$ at $33/19456$, $\omega_8/\xi_8$ at $71/77824$, $\omega_{16}$ at $67/77824$ | component, unregistered; replayed *(review)*: worst $0.999316555505$ (109 cells) and $0.999368209930$ (117 cells); slide coverage at $9/2048$ certifies $B_c$ | [local radius review](../../../docs/project/reviews/review-2026-10-03-n17-local-radius.md), H-340 | $1/1152$ fails because $\omega_{11}$’s radius would exceed the slide radius: the ceiling of this recipe is about $8\times10^{-4}$ per coordinate, $4\times10^{-3}$ in $\omega_{11}$ |
| Uniform floors: $0.87815254$ at $1/5000$, $1.7564$ at $1/2500$, $4.2888$ at $1/1024$; $5000 \times 0.87815 = 4390.8$, so the “$1/4391$” figure is right | verified *(review)* | `check_n17_local_radius scan` | **exact only relative to the recipe’s C7 curvature constants**; a different curvature lemma changes $K$; a signed-second-order lemma was modelled at $\le 2\times$ in floats |
| What sets the scale: the $-\omega_{11}$ certificate’s $\ell_1$ mass is 1,421 (support on all 52 rows; the review’s 1,439 is the point-program dual at the worst $1/5000$ vertex) against $K_{\text{pair}} \approx 9.7r^2$, more than half of it the angle–position cross term; $\kappa_\infty = 1/175.8$ | computed *(review)* from the exp-248 certificates | — | the tilted block’s co-rotation with the 9/11 face open is the soft mode; the dual-sheet route removes the bilinear remainder by treating positions exactly at fixed angles, which is why it reaches about 50× further |
| H-261 “unresolved as worded” | the 5/6-exchanged witness is a relabelled family member ([Section 3](#3-corrections-to-the-record)) | `family_sat.py` *(review)* | not a packing off the family; the claim is not refuted |

Remaining obligation: register H-340; compute the allowances $E_j$ (frame, basis, angle
chart, $u^\ast$ enclosure) that the capture receipt must deliver with $R_j + E_j \le
r_j$; write the composition; a second implementation of the local checker.

### 2.10 Composition, frames, $D_4$, sliders and caps

| Item | Status | Note |
| --- | --- | --- |
| Centred-container lemma: $P \subset C(s) \subset C(S^\ast) \subset C(U') \subset C(U)$; translate by $-(\sigma,\sigma)$; spans $S^\ast \Rightarrow s \ge S^\ast$ | proved (hand, sole-Astra; read *(review)*: correct) | supersedes the composition review’s corner embedding; the centred one is what $D_4$ preserves; stating capture in the $U$ frame removes the “$2r$ doubling” worry |
| $D_4$ action and labels: the family’s orbit has size 8, trivial stabiliser; the canonicalising action is $f_1 = (U-y, U-x)$, not $r_3$ | verified (exp-315 refusal, exp-316 pass with 810 rows) | a reflection negates tilts, so the H254 lift transports with the mask; the composition must carry the group element |
| Slider premises: $a \ge 0$; $b \ge b^\ast$ and $z \le z^\ast$ from the sharp 9/11 and 11/13 separation lemma; square 6’s premise is `side-S2` at any orientation | verified (exp-248; lemma proved by the review) | a widened neighbourhood needs new slide coverage |
| Cap monotonicity: a certificate at $U$ holds at every smaller cap; a centred cap keeps the cells in the $U$ frame | proved | the composed argument must read the state in the centred placement |
| $u^\ast$ enclosure: allowance $E_u M_i + \lVert u^\ast \rVert_1 E_i$ charged to capture | stated; no receipt computes it | part of the composition checker (H-334, H-347) |
| Composition checker | absent | the n11 composer pattern applies; pin mathematical identities, not timing fields |

### 2.11 The n = 11 analogy and formalisation

|  | n = 11 (T-060) | n = 17 | Transfers? |
| --- | --- | --- | --- |
| Endpoint | isolated pose, degree-8 root | 3-slider family plus free square 6, degree-18 root | no: quotient by sliders, a state premise, square 6 by cell (handled) |
| Local theorem | 128 feature branches × 33 coordinates; two-radius $1/256$; worst ratio $0.6765$ | 52 rows × 45 coordinates at the moving base point; $1/5000$ uniform, $1/1216$ per coordinate; worst $0.9259$ / $0.9993$ | yes, same recipe and curvature formula; radius 8–20× smaller |
| Soft slope $\kappa_\infty$ | $0.0518$ | $1/175.8 = 0.0057$ | 9× softer |
| Capture | 14 root rounds from the cells, 3 closed-predicate splits, 2 CPU-hours replay | one round from the cells; box pilots stall; no split ever needed because nothing moved | **no**: the n17 analogue of the root node has not been run to a verdict |
| Exclusions | 2,180 cases, mostly counting-mode fields | 60 admissions, 4,683 orbits open | other half of this report |
| Formalisation | one Lean theorem `ElevenSquare.optimality`, statement audited as exactly $s(11) = T$; 13,308 `native_decide` axioms | none | realistic at n17: the hand layer (wall lemma, centred container, separation, $D_4$ transfer, recipe lemmas 1–6) and perhaps the endpoint feasibility (204 rational interval obligations); reflecting 2 GB of certificates through `native_decide` is far beyond the n11 effort |

The honest comparison: n17’s local theorem is weaker in radius by an order of magnitude
at the same time as its capture start point is the same cell scale, so the bridge is two
orders of magnitude longer than n11’s.

### 2.12 Record, documentation and process health

Briefly, since the inventory holds the detail.

- **Explainer drift.** `docs/project/n17-optimality-explainer.md` (last edited 6 Oct)
  says 58 / 36,784 / 4,685 at lines 251 and 382; X-048’s current selection and
  `SYNOPSIS.md`’s Session-184 narrative say the same.
  `main` has carried 60 / 36,768 / 4,683 since `533dd42c6` (9 Oct, 09:22 UTC).
- **Register wording.** T-065’s claim in `results.yaml` and `RESULTS.md` still says “No
  identity with the catalogue’s degree-18 polynomial is proved”; exp-245 proved it on 2
  October; `think-yjgk` (open since 5 Oct, “close when PR 347 merges”) never landed the
  text.
- **Tracker.** #405’s latest comment says the landing added no census admission; Tail A
  and B reached `main` with it.
  #405 does not mention #472, the BC-423/426 held closures (`think-yg80`, two closures
  that passed standing FULL and await an owner ruling), Kleddamag’s research checkpoint,
  or the missing verifier listing; it still says #403 and #442 conflict with `main`
  (both are MERGEABLE/CLEAN) and lists #413 at 33 rows.
- **Intake records.** `result-requests.yaml` titles #413 “27 sub-pattern exclusions” and
  has no #472 entry; `intake-watch.yaml` does not watch `wand125/square-packing` or
  `wand125/square-packing-tools`, where the objects live (PR 466 adds them, unmerged);
  the maintained reconciliation tool hard-codes 33 rows (an OR-1 tool change).
- **Beads.** 16 program beads in progress with no update in more than 48 hours, several
  contradicting the record (`think-1qms` wants to import R071, verified since 5 Oct;
  `think-jhgi` calls itself merge-blocking for a stack that merged; `think-dvcs` is in
  progress for a pilot whose outcome is known; `think-geid` open though refuted;
  `think-98mg` and `think-lyh9` continue conditional propagation X-051 says to stop).
  Only 44 beads carry `n-17`; 142 are related.
- **OR-18.** About 314 MB of tracked JSON landed with the 9 October stack
  (`think-1111`); the other half of OR-18, the 204 unhosted objects, has no bead with a
  current count.
- **CI and caps.** `main`’s post-merge surface is green (run 37926227254); a 192 MiB
  snapshot cap and merge-readiness work occupied most of the tracker’s last six comments
  before 9 October. OR-3 and OR-14: the gates run beside the research.

## 3. Corrections to the Record

Each was found by one of the 9 October reviews or the inventory; evidence is named so
the coordinator can apply it.

| # | Item | What the record says | What is true | Evidence | Where to fix |
| --- | --- | --- | --- | --- | --- |
| C1 | H-337 and the hull-pull repair | X-051 §2.5, §7 and H-337: “the compression pull repair has an external executor but no merged repair”; H-337 blocked on it | `FINE_HULL_PULL = 1/2^{18}` is in `packing/src/sqpack/hull_kernel/producer.py`; commit `917163641` (7 Oct) is an ancestor of `6a0499ba4` (`git merge-base --is-ancestor`); exp-276 already calls the producer repaired | `git`, `producer.py` line 68 | H-337 `instrument_ready` → true with a dated note (done here); `think-juy9` is discharged on `main` |
| C2 | H-261’s “counterexample” | the composition review and the explainer present the family with squares 5 and 6 exchanged as a packing meeting every premise outside $B_W'$ | for $a = 1$ and $a = 1.07$ the exchanged configuration is, as a set of 17 squares (exact rational corners), the family member $w = (0,0,0)$ with square 6 on the bottom wall at $x = x_5^\ast - a$, inside square 6’s box; the claim is not refuted; what fails is that the certified box does not cover the labelled slider domain, which is disconnected ($a \in [0, 0.115] \cup [1, 1.074]$ at $z = 0$) | `family_sat.py` *(review)*; X-048’s 5 October note already says “the same family relabelled” | H-261 dated note (done here); the explainer’s H-261 paragraph |
| C3 | H-330’s falsifier | “at most two directions with $d_j$ above the terminal radius” at the margin H-325 reports | at $m = 10^{-2}$ every angle direction has $d_j \ge 0.014 > 5\times10^{-3}$; the claim can hold only if $m \lesssim 10^{-3}$, the kernel’s loss floor at $1/512$ rows, exactly where the engines stop seeing anything; the map is worth making with $m$ as the variable | the scope review’s slopes; [2.8](#28-capture) | H-330 dated note (done here); re-scope before any round |
| C4 | The tail “resists at every row width” | X-051 §2.2(3) | four per-state runs exist: one closure, one incomplete, two fixed points at 32 uniform bins; the adaptive recipe has run on two of the 95 and never at the 2,304-row cap | exp-257, stall classification | read as “undersampled”; H-343 measures it |
| C5 | The “exact floor” near $1/4391$ | local-radius review, X-051: “an exact floor, and no finer curvature lemma buys more than a factor of two” | exact relative to the recipe’s C7 constants; a finer lemma was modelled at $\le 2\times$ in floating point | `scan` replay *(review)* | wording, no consequence |
| C6 | T-065’s register wording | `results.yaml` line 5830, `RESULTS.md`: “No identity with the catalogue’s degree-18 polynomial is proved” | exp-245 proved the identity on 2 October; n-017’s prose says so | exp-245 | the T-065 claim text, under the result-import procedure (`think-yjgk`) |
| C7 | Stale counts | explainer lines 251 and 382, X-048 line 127, SYNOPSIS Session-184 narrative: 58 / 36,784 / 4,685 | 60 / 36,768 / 4,683 on `main` since `533dd42c6` | census tool on this worktree | the explainer when next touched; X-048’s current selection |
| C8 | Tracker census claim | #405 latest comment: “No exclusion, census admission, T item or optimality claim was added” | Tail A (`s184-tail-a-m3096311`) and Tail B (`s184-tail-b-m3096315`) reached `main` with the landing: 58 → 60 entries | `git show 3213d651b:…certified-sub-patterns.yaml` (58) vs `533dd42c6` (60) | #405 |
| C9 | #413 and #472 in the tracker | 33 rows, “eighteen fast-only and eleven computed”, union 2,234 / 17,604; row 23 computed | 38 rows (2 + 2 + 20 + 11 + 3); union 2,338 / 18,408; row 23 kernel FULL-reported; #472 absent | #413 body, #472 | #405, `result-requests.yaml`, the `n-17` label on #472 |
| C10 | “The dual-sheet instrument has never been built” | X-051 §2.2, explainer | true of the direction-patch certifier and the patch counter; the interval machinery for box patches and cones exists (exp-263, 267, 269) and is the base to build on | exp-263/267/269 | H-329 notes |
| C11 | Explainer’s “first-order feasible radius about $2\times10^{-10}$ at $U'$” |  | $7.9\times10^{-11}$ with the actual cap | `root_and_caps.py` *(review)* | immaterial |
| C12 | PR state in the tracker | #403 “fails CLS and conflicts with main”; #442 “conflicts with main” | #403 `c1d3aab9` MERGEABLE/CLEAN, 31 checks pass; #442 and the intake stack CLEAN (#469 UNSTABLE) | `ghx pr view`, 9 Oct 16:40 UTC | #405 |

No soundness defect was found in the endpoint, the local theorem, its composition, the
cap join, the cover, the census, the transfer rules or the kernel grammar.

## 4. The Minimum Set of Remaining Mathematical Results

For $s(17) = S^\ast$, with the cover, the census, the transfer rules, the two-cap
design, the local family theorem and the hand lemmas as they stand, exactly these
remain:

1. **Exclusion of every non-endpoint residue orbit at a cap at least $S^\ast$.** 4,682
   orbits (36,760 states) today; 3,635 after #472; about 2,340 after everything
   reported. Any cap in $[S^\ast, U]$ serves; $U$ is what every engine uses; a state
   feasible at $U$ but not below $S^\ast$ needs its certificate at $U'$. The family’s
   own state cannot be excluded at any cap $\ge S^\ast$ and is item 2. Square 6’s full
   freedom is discharged by the distance-2 exclusions inside this item.
2. **Capture of the family’s state.** Every packing of side $\le U'$ in that state, read
   in the centred placement with the group element carried, has its 45 non-slider
   coordinates within $r_j - E_j$ of the family in the exact root’s frame, and square 6
   in `side-S2`; equivalently a terminal theorem large enough that an engine reaches it
   from the cells, plus the engine.
3. **The conversion allowances $E_j$** (frame, basis, angle chart, $u^\ast$ enclosure),
   computed exactly, so that items 1 and 2 compose with the local theorem.

Nothing else is mathematics: custody, two-verifier parity, the composition checker, the
verifier listing and Lean are assurance, and the cap ladder is a separate lower-bound
result that the proof does not use.
Item 1 is priced for all but its hard core; item 2 has no priced engine; item 3 is a
slice of work.

## 5. Directions to Completion

### 5.1 Ranked

Costs are for the first decision each direction yields, in CPU-hours and agent-hours;
“information” is what the record gains whichever way it goes.

| # | Direction | Mechanism | Establishes | Falsifier / early kill | Prerequisite | Cost | Information |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Admit #472 and convert the BB-only #413 wall rows to kernel certificates** (H-341, H-342) | clean-worktree full replay of the twelve under a listed verifier, Rust parity, hosting under a repository manifest, an admission round; then `check_n17_subpattern` mode A on every BB-only row with a wall cell, including row 33 | residue 4,683 → 3,636 → about 2,400 orbits; distance-2 tail 95 → 94 | a full-mode refusal or a parity disagreement; a kernel stall on most BB rows | a verifier listing for `be8135f6e` (or a replay at `1ad706c21`); an OR-18 hosting decision | #472: ~2 CPU-h, ~4 agent-h; conversions: ~10 CPU-h, ~6 agent-h | the largest exclusion movement available; the kernel-versus-BB routing rule confirmed or refuted on 20 more patterns |
| 2 | **Measure the hard tail** (H-343) | the SW9 adaptive recipe (64 bins, floor $1/512$, 2,304-row cap, 2-hour ceiling) on all 94 remaining distance-2 representatives and a uniform 60-orbit sample of the rest; every stall classified with the support/domains diagnostics | the real size of the hard tail and the per-state stall fraction on the current residue | fewer than half of the 94 close: the tail is a grammar problem; more than half: a throughput problem | none; zero build | ≤ 300 CPU-h, ~6 agent-h | replaces an inference from four runs by a measurement of 154 |
| 3 | **Decide the capture engine from the real start point** (H-337 then H-345) | the n11 positive control through the repaired producer (15 rounds), then 20 rounds of the n17 producer from the family’s cells at $U'$ | whether the n11 engine is dead at n17 or merely never started | n11: worst extent above $0.9$ of round 0 at round 15 kills the producer; n17: no turn range or wall-fed bound moves by 10 % in 20 rounds confirms reading B from the cells | none (the repair is merged) | 2–4 + 5–20 CPU-h, ~4 agent-h | ends a question that consumed three sessions of box-seeded argument |
| 4 | **Terminal theorem by exact dual sheets** (H-340 first, then H-329’s patch counter and sphere slope minimum, then the exact build; H-339 after) | register the $1/1216$ vector; count optimal bases over 2,000 sampled directions at four radii; find the least directional slope on $S^{15}$ by random directions; then the patch certifier with Krawczyk duals and interval Hessians | a terminal region 25–50× larger in angle as a list of exact rational duals, the foolproof form | a negative sampled slope; Chao1 above $10^5$ with unsaturated singletons; random-direction slope minimum below $5\times10^{-3}$ per rad | exp-244’s kernel and duals; H-278 extended to the box; the exact zero-turn LP equality (hand, needs review) | 15 s (H-340); counter: one slice, minutes of LPs, ~12 agent-h; exact build: one slice plus review, ≤ 1 CPU-day, ~30 agent-h | fixes the inner edge of the bridge; the only lever that enlarges the target rather than the engine |
| 5 | **Price the outer bridge: Knuth estimate of an angle branch and bound with Taylor-at-centre LP bounds** (H-346) | branch on angles and feature choices; bound each box by the fixed-feature LP at the centre plus an interval second-order remainder ($\approx 0.3\rho^2$ sampled); close above $U'$; leaf = the widened region or the $1/1216$ vector | whether the cells-to-feature-forced bridge is a computation of $10^6$, $10^8$ or $10^{12}$ nodes | estimate above $10^8$ at the widened leaf | 4 (for the leaf), or the $1/5000$ leaf as a pessimistic stand-in | days of build (~25 agent-h), minutes to estimate | the only priced candidate for the outer bridge; decides whether capture is engineering or mathematics |
| 6 | **The foolproof package** (H-336, H-335, H-334, H-347, H-348, H-333; the verifier listing; T-065 wording) | host the 204 objects; Rust parity on every kernel admission; a composition checker reading cover, ledger with per-entry caps, capture and local receipts; exact $E_j$; a second local-theorem checker; Lean for the three short lemmas | the proof becomes a checkable object; the trusted base is listed in one place | an accepted mutant; a failed fetch; $E_j \ge r_j/10$ | an owner decision on hosting | custody ~20 CPU-h + decision; parity a day of two workers; checker 20–40 agent-h; $E_j$ 10–20 agent-h; local checker 20–30 agent-h; Lean 10–30 agent-h | nothing mathematical moves; without it every admission is a receipt |
| 7 | **Closed half-cell branch predicates (C5)** (H-344) | halve a side cell along its long axis into closed children, each with a seed core; a consumer rule that admitted children cover the parent, seams included; test on m1964767, m851903, m1949551 | an engine for consistency-limited states | both children of each state stall as the parent did | the verifier accepts n11’s predicate grammar; the n17 node and consumer do not | one build slice plus review (1–2 weeks); runs 2–4× a parent | the only grammar change aimed at the diagnosed mechanism |
| 8 | **Cap scan read as margin versus direction** (H-325; H-330 with $m$ as the variable) | whole-state kernel and BB on the family’s state at $S^\ast - \{2, 5, 10, 15\}\times10^{-3}$; the fixed-feature LP slopes against the margin found | the margin the engines see on the hardest state; prices the cap ladder and the bridge | a stall at $1.5\times10^{-2}$ | the producer accepts a cap below the root box (one-line check) | 4–8 CPU-h, ~4 agent-h | one number nobody has; mostly informs capture |
| 9 | **Kernel closure of the 69 flagged, uncertified classes** (H-349) | `check_n17_subpattern` mode A with adaptive rows on every selector flag the census tool projects (2,163 orbits / 16,900 states if all closed, overlapping the reported set) | more residue removed by the engine that works | fewer than 80 % close in 30 minutes each | none | tens of CPU-h | the stall fraction of the kernel on the current flags |
| 10 | B2 on interior crowds and the ten smallest-margin tail sub-patterns (H-331); decomposability survey (H-327); state-conditioned charge (H-338) | as registered | reach of the BB and of counting on the tail | as registered | H-327 first | 20–60 CPU-h; 5–15 CPU-h; 20 agent-h | medium; cheap |
| 11 | Cap ladder (H-326) | exclude every residue orbit at $V_1 = S^\ast - 10^{-2}$ | $s(17) > V_1$, $+5.1\times10^{-3}$ over R071 | a 30-orbit pilot with fewer than 27 closures | 8 and most of 1–2 | 100–4,000 CPU-h | a verified bound; its certificates do not enter the proof; worth the measurement, not the campaign, until 1–2 have shrunk the residue |

### 5.2 Parallel lanes with disjoint deliverables

| Lane | Hypotheses | Deliverable | Owner skill | First week |
| --- | --- | --- | --- | --- |
| A. Admission and census | H-341, H-342, H-349; H-332 re-scoped to the kernel route for C1/C2 and rows 1–2 | regenerated ledger, census and partition receipts; a verifier listing for `be8135f6e`; the reconciliation tool reading 38 rows | engineering, admission review | #472 replay and parity; label and answer #472; rows with wall cells queued |
| B. Hard tail | H-343, H-327, H-331, H-344, H-338 | per-state verdicts and a stall classification of the current residue; the C5 grammar build | kernel producer, BB, diagnostics | all 94 distance-2 representatives launched under the adaptive recipe |
| C. Capture engine | H-337, H-345, H-325, H-330 (re-read), H-346 | an engine decision from the real start point; the margin-versus-direction map; a priced outer bridge | capture producer, LP | H-337 and H-345 launched; H-346 build started |
| D. Terminal theorem | H-340, H-329, H-339, H-347 | registered terminal radii; patch count and slope minimum; the exact patch certificate; exact $E_j$ | exact LP, intervals, review | H-340 registered; patch counter written and run |
| E. Assurance | H-336, H-335, H-334, H-348, H-333; T-065 wording; explainer and tracker refresh | hosted objects; two-verifier parity on all 60; the composition checker; a second local checker; Lean for three lemmas; a record that matches `main` | custody, verifiers, Lean | hosting decision taken; parity run on the seven objects in hand plus #472’s twelve |

Lanes A, B and E share the kernel verifier and the census tool but write disjoint
artifacts; C and D share exp-244’s duals and nothing else.
OR-2 and OR-6: three to five sub-agents at a time, one per lane, each with a slice of a
day or less to a falsifiable verdict.

### 5.3 Critical path, with the uncertainty stated

```text
week 1   A: #472 admitted; wall rows queued      C: H-337, H-345 verdicts     D: H-340 registered, patch counter
week 2   A: ~2,400 orbits                        C: H-346 estimate            D: slope minimum, go/no-go on H-329
         B: 154 per-state verdicts, stall fraction known                      E: hosting, parity on 60 + 12
weeks 3-6  B: kernel/BB/C5 on what is left (priced after week 2)
         C+D: either an engine that reaches the terminal region, or a bridge BB with a node count
weeks 6+  E: composition checker reads everything; the statement is emitted or a named orbit is open
```

What is priced: lane A to about 2,400 orbits (two weeks); lane B’s measurement (two
weeks of CPU); lane D’s patch counter and H-340 (one week); lane E except the hosting
decision. What is not priced, and is the honest uncertainty: the hard core of the tail
after lane B (if the two diagnosed states are typical, 15-square joint infeasibility
with no engine beyond C5 and the BB, both unmeasured at that arity), and the outer
bridge of capture (H-346 is the pricing step; if its estimate is above $10^8$ nodes at
the widened leaf, capture needs a new idea, most likely a terminal theorem along the
three soft directions that no current instrument produces).
Order of magnitude for existing engines: about $10^3$ CPU-hours reduce the residue to a
few hundred orbits; those few hundred, and capture, are the mathematical problem.

### 5.4 What to stop

- Centre-only relaxations of any kind, at any order, with or without a ball: determined
  (X-051 §3, [2.6](#26-relaxations)); retire `think-dvcs` with its known outcome and
  `think-geid` as refuted.
- Conditional propagation inside one owner-0 guard as a route to the tail (fifteen
  misses, no consumer; `think-98mg`, `think-lyh9`).
- Box-seeded kernel capture pilots (R9 stages 1–2) before H-337 and H-345 have run.
- BB certificate replays, and 480 GB acquisitions, for patterns the kernel closes; BB
  only for genuinely interior crowds.
- Treating a local radius above $10^{-3}$ as reachable by the ratio recipe.
- A new reconciliation document per merge gate; the tracker and the explainer are the
  two living documents, and the explainer should be regenerated from the census tool.

## 6. Candidate Hypotheses

Nine new registry files, H-341 to H-349, each with `derived_from: [X-052]`, for the
directions H-325 to H-340 do not cover; three dated corrections to existing files
(H-261, H-330, H-337), none of which changes a frozen criterion of a registered
experiment.

| Id | Claim | Mechanism | Falsifier | Expected information | Limits |
| --- | --- | --- | --- | --- | --- |
| [H-341](../hypotheses/H-341-n17-issue-472-kernel-admission.md) | #472’s twelve kernel certificates pass a clean-worktree full replay under a listed verifier and Rust parity, bind to the exp-247 cover at $U$, and their admission reproduces 3,636 orbits / 28,528 states with the distance-2 tail at 94 | same format and frame as 59 admitted entries; the verifier derives closure itself | a full-mode refusal, a parity disagreement, or a census mismatch | $-1{,}047$ orbits; the admission path exercised on external objects | custody and a verifier listing are prerequisites, not mathematics |
| [H-342](../hypotheses/H-342-n17-kernel-conversion-of-bb-rows.md) | at least two thirds of the BB-only and computed #413 rows that contain a wall cell close under `check_n17_subpattern` mode A with adaptive rows within 30 minutes each, with certificates under 100 MB | wall-anchored crowds give the ownership induction owned points from the seed | fewer than two thirds close | about 1,000 orbits more; the kernel-versus-BB routing rule | interior crowds stay with the BB |
| [H-343](../hypotheses/H-343-n17-hard-tail-adaptive-measurement.md) | at least half of the 94 distance-2 representatives not covered by #472 close under the 17-owner kernel with the SW9 adaptive recipe within 2 hours each, verified in full | the recipe closed 26 of 29 counted draws on a different frame | fewer than 47 of 94 | the size of the hard tail and the stall fraction on the current residue | per-state closure is a tail method; a uniform 60-orbit sample of the rest is the control |
| [H-344](../hypotheses/H-344-n17-half-cell-branch-predicates.md) | with closed half-cell branch predicates and a consumer rule that admitted children cover the parent, the kernel closes both children of at least two of m1964767, m851903 and m1949551 within 4× the parent’s time | halving a side cell gives every child a seed core, which the consistency-limited stalls lack | both children of each state stall | an engine for consistency-limited states | unbuilt; seams must be in both children |
| [H-345](../hypotheses/H-345-n17-cell-seeded-twenty-round-capture.md) | 20 rounds of the repaired producer from the family’s cells at $U'$ reduce at least one owner’s turn range or wall-fed position extent by 10 % of its round-1 value | the n11 root node contracted from its cells in 14 rounds | nothing moves by 10 % in 20 rounds | whether the kernel route is dead at n17 or never started | says nothing about reaching the terminal region |
| [H-346](../hypotheses/H-346-n17-angle-bb-knuth-estimate.md) | an angle-and-feature branch and bound with Taylor-at-centre fixed-feature LP bounds on the family’s state at $U'$ has a Knuth estimate below $10^8$ nodes to the widened leaf | second-order-convergent bounds remove the cluster problem near the family | estimate above $10^8$ | a price for the outer bridge | an estimate, not a run; the leaf depends on H-329 |
| [H-347](../hypotheses/H-347-n17-exact-conversion-allowances.md) | the conversion allowances $E_j$ for all 45 coordinates compute exactly and are below one tenth of the $1/1216$ vector’s $r_j$ | the allowances are linear in the root-box width and the frame offset | any $E_j \ge r_j/10$ | the terminal target the capture receipt must actually deliver | part of the composition’s receipt format |
| [H-348](../hypotheses/H-348-n17-second-local-theorem-checker.md) | an independent checker of the local theorem’s certificate data, rational linear algebra only, reproduces the four worst ratios and refuses 20 doctored certificates | the certificate is a few hundred kilobytes of dyadics and rows; the check is the ratio inequality | a disagreement or an accepted mutant | the local half rests on two implementations | the hand lemmas stay hand lemmas |
| [H-349](../hypotheses/H-349-n17-flagged-class-kernel-closure.md) | at least 80 % of the 69 flagged, uncertified selector classes close under `check_n17_subpattern` mode A with adaptive rows within 30 minutes each | the engine that closed every arity-8/9 flag it was given this week | fewer than 56 of 69 | the kernel’s stall fraction on the current flags and about 1,500 orbits | overlap with the reported set is counted, not assumed |

Corrections applied to existing files: H-337 reads as open (the instrument exists;
`instrument_ready` was false on a stale premise); H-330 carries a note that its
threshold is predicted refuted by its own slopes unless $m \lesssim 10^{-3}$ and should
be re-scoped with $m$ as the variable before any round; H-261 carries a note that the
exchanged witness is a relabelled family member and the claim is not refuted.

## Evidence Status and Limits

W3 certifies nothing.
This report registers no round, verifies no certificate, changes no bound, verdict,
count or frontier field, and touches no bead or issue; the coordinator publishes.
The computations marked *(review)* were run on 9 October from a read-only worktree at
`6a0499ba4` with the project interpreter, their scripts and outputs retained beside the
reviews and not in the repository; they are review evidence, not registered rounds, and
a registered replay (H-328’s pattern, under OR-1) is the way to make any of them a
verdict.

| Kind | Items |
| --- | --- |
| Computed in the reviews, exact rationals | the four real roots and the isolation of $S^\ast$ to $6\times10^{-44}$; $U - S^\ast$, $V - S^\ast$, $\sigma$, the first-order radii; the RF-7 obstruction arithmetic; the rational witness (own SAT); the family’s 21 contacts and 15 anchors and the 5/6 exchange identity; the cover’s convexity, $D_4$ invariance, Burnside and brute-force orbit counts, inclusion–exclusion area; the ledger residue, marginals and distance partition; the #472, #413 and #358 projections and the contributor-figure reproductions; the exact slack witnesses ($\ge 1.0305$) for all 95 distance-2 states and the endpoint; the $-\omega_{11}$ dual mass 1,421 |
| Replayed in the reviews from `main` with the repository’s unchanged instruments | exp-244 and exp-248 run-002 (10 s each); the $1/1216$ and capture-form compositions; the slide coverage at $9/2048$; the uniform floors; X-051’s 96 centre survivors (40 s) |
| Numeric, in the reviews | the wall-lemma attack (600 Nelder–Mead starts per cell); the max-min centre-distance optima before exact rounding; the orientation-coupling bounds |
| Derived by hand in the reviews | the curvature bound, the ratio argument, Lemma 1/2 logic, the Kantorovich remark, the no-man’s-land table from the record’s slopes, the gap factors, the characterisation of the diagnosed stalls |
| Computed in this report | the census tool on this worktree (60 / 36,768 / 4,683, 6.3 s; 69 classes with `in_ledger: null`); `git merge-base --is-ancestor 917163641 HEAD`; the verifier blobs by `git ls-tree`; the commit list since `f0ec5b6` |
| Read from the record and GitHub | every other count, verdict, cost, PR and issue state (16:30–17:20 UTC, 9 October) |
| Derived here, needing review | the two-gap framing; the minimum-set statement; the ranking, the lanes and the critical path; the stop list |
| Not done | any registered experiment; any certificate verification (no admitted object is in place); any network sweep of external repositories (`make intake` was not run); any change to the explainer, the register or a bead |

Limits. The #472 projections are containment projections of masks the contributor named;
they become census facts only after the admission round.
The tail characterisation rests on two diagnosed states; the other 91 are unmeasured.
Agent-hour costs are estimates from this week’s receipts, which are lower bounds.
The lanes assume the hosting decision is taken; without it lane E cannot start and every
admission in lanes A and B remains a receipt.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
