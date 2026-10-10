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
    - docs/project/research/research-2026-10-09-n17-family-cell-audit.md
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
    - https://github.com/jlevy/squares/pull/475#pullrequestreview-5473799813
  proposes: [H-341, H-342, H-343, H-344, H-345, H-346, H-347, H-348, H-349]
---
# X-052: The n = 17 Optimality Program on Every Front, and the Path to a Proof

**The proof of $s(17)=S^\ast$ has two real gaps, both measured now, and neither moved
this week: exclusion of the hard tail of the residue, where per-state runs have reached
three of its 95 distance-2 orbits and none has closed, and capture of the family’s own
state from its cells, where the only engine in hand has been run for one round.** The
bracket is verified at both ends.
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
found in the record, a sufficient set of remaining mathematical results, and a sequenced
plan in parallel lanes.
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
| Hard tail, measured | per-state runs on 4 distance-2 orbits: u8 closed and so left the residue; of the surviving 95, u1 incomplete at 7,001 s, m1964767 and m851903 fixed points under 32 uniform bins; none of the 95 has ever closed per state | open; undersampled |
| Local family theorem | $r = 1/5000$ on $B_W'$, worst ratio $0.925931$; on $B_c$, cube-form floor $1/1216$, worst $0.999316555505$ (109 cells), and capture-form floor $11/32768$, worst $0.999368209930$ (117 cells) | proved with one review; anisotropic vectors unregistered, distinct retained receipts ([2.9](#29-the-local-family-theorem)) |
| Capture | from the cells: one round (exp-276, 277, 280), nothing contracted; from a $1/1024$ box: pilot 2 met its falsifier; the cells’ half-widths are 35 to 3,900 times the terminal radii in every coordinate ([2.8](#28-capture)) | open; no engine has a verdict from the real start point |
| Contributor certificates, unadmitted | #472: 12 kernel certificates, standing verifier full pass reported; #413: 38 rows; #358: 2 BB classes | reported; admission of #472 would leave 3,636 orbits / 28,528 states *(review)* |
| Custody | 204 admitted objects, 2,167,361,631 bytes, listed by digest; the release has 0 assets; three Session-184 release tags do not exist | the admitted census is not replayable from a fresh clone today |
| Composition | no checker reads cover, ledger, capture and local receipts together; caps are implicit ($U$) on every entry | absent |

**The two real gaps in the proposed route.** (1) The 4,682 non-endpoint residue orbits
need exclusions at root-joined caps above $S^\ast$, or terminal theorems implying
$s \ge S^\ast$; the 95 distance-2 orbits are the hard core.
On the two diagnosed ones, exact witnesses defeat the encoded cell-membership and
centre-distance relaxations; float deletion search reports an arity-15 candidate for
m851903; and support sampled from 100 float poses suggests weak pairwise propagation
under that configuration.
(2) Every target packing of side at most $S^\ast$ in the family’s state, normalized
concentrically in $C(S^\ast)$, must be shown to lie within the terminal radii of the
family in the exact root’s frame; no engine has contracted anything from the cells, and
the terminal region is $10^{-3}$ to $10^{-4}$ per coordinate.

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
| The declared family lies in exactly one state, margin $\ge 0.002111$; square 6 in a declared box | verified with one review | exp-247 `unique_state` | arbitrary square-6 freedom requires its own argument or the alternative-state exclusions; the restricted audit below supplies one argument on a smaller slider box |
| Existential closed-cell assignment: every packing of side $\le U$ in $[0,U]^2$ realises a state; overlaps give several states, harmless for exclusion | proved | lemma review §3 | none |
| Residue 36,768 / 4,683, endpoint untouched; W7 alone 133,152 states / 16,701 orbits, A 110,448 / 13,897, SW9 43,772 / 5,499; the 39 whole-state entries remove 304 states | verified *(review)* by independent containment code; the census tool on this worktree agrees | `census_n17_certified` | none |

The
[restricted free-square audit](../../../docs/project/research/research-2026-10-09-n17-family-cell-audit.md)
fixes the other sixteen squares exactly to the endpoint family, with $a\in[0,3/25]$,
$b\in[0,3/40]$, $z\in[-1/20,1/40]$ in the $U$ cover frame.
Exact squared-distance bounds on eleven closed polygon pieces exclude square 6 from all
seven alternative unoccupied cells, at every orientation: the worst bound is
$409960561/423200000<1$, so the radius-$1/2$ incircles overlap.
Capacity one excludes the sixteen occupied cells, forcing its centre into `side-S2`.
This deduction is scoped to that exact skeleton and slider box; it does not cover
perturbed cores, all of $B_W'$, outer capture or any remaining global state.
The maintained verifier and its report retain the arithmetic for review; downstream
admission remains separate.

Remaining obligation on cover and census: none, short of Lean for the wall lemma
(H-333).

### 2.4 Exclusion certificates and the trusted computing base

What a certificate proves, and on what premises, is reviewed in X-051 §2.3 and the
[kernel adaptation spec](../../../docs/project/reviews/review-2026-10-02-n17-kernel-adaptation-spec.md);
the global-side review found no gap in the ownership induction’s grammar and confirmed
transfer by containment and $D_4$ as a one-line proof.

| Component | Lines | Passed the admitted objects | Independent checks | Risk |
| --- | ---: | --- | --- | --- |
| Cover checker | 1,437 | one tool | five review scripts, the lemma review, the review’s own script | low |
| Census consumer | — | one tool | two review `transfer_count` scripts, the review’s containment code, the contributor’s own counts | low |
| Kernel verifier `verify_n17_kernel_certificate.py` | 1,751 | the standing verifier; W7 also by lane R3’s separate verifier | 34-case mutation suite refused by the Python and the Rust verifier; Rust port (PR 410) with receipt parity on 7 certificates, *reported* by the contributor and not replayed; three closed-cover defects found and fixed on 3 October | **58 of 60 admissions rest on one implementation**, and its early versions had unsound branches |
| BB verifier `verify_n17_bb_certificate.py` | 1,321 | the standing verifier; A also by lane R4’s separate verifier | 16 mutants, 9 doctored certificates | one admitted object; `think-t41a` (source-cell enclosure) open for external intake |
| Hand lemmas | — | — | wall lemma reviewed and attacked numerically; transfer and monotone embedding are one-line | low |
| Custody | — | — | 204 objects / 2.17 GB listed by SHA-256; release `data/n17-x048-session-168-certificates-v1` has 0 assets; tags `…conditional-owned-hull-v1`, `…numeric-cap-readiness-v1`, `…tail-a-dependencies-v1` return 404 | **every admission is a receipt, not a replayable object** |

Verifier versions, read from the ledger and `git ls-tree` on this worktree: the ledger
has eight verifier listings across seven commits; every kernel admission since exp-251,
Tail A and B included, was passed by `kernel-streamed` (commit `601bbf110`, blob
`1ad706c21`), `dirty: false`. `main`’s kernel verifier is blob `be8135f6e`, three
commits later (`836e919e0`, `90d6e4c94`, `90cd2528e`: centred-cap support with a
48-vertex hull allowance and a sound Y-range prefilter whose measurement round exp-298
ended invalid), and **no ledger listing names it**; under the ledger’s review rule, no
receipt from current `main` should admit an entry until a listing with a review pointer
exists. That bar is the review rule, not a mechanical refusal: the census checks a
receipt’s verifier path and uncommitted flag and does not resolve its version.
The BB verifier moved the same way: the ledger lists blobs `4224262c7` (`bb-review-r4`)
and `f1e2268d6` (`bb-enclosure-retry`); `main`’s blob is `e6e400e7f` after PR 452
(SHA-256 `10db91c2…`); and every contributor BB receipt names the SHA-256 `9dcc05bc…`,
which is blob `c69f1ec08`, `main`’s BB verifier from 4 to 8 October and unlisted.

Remaining obligation: a verifier listing for `be8135f6e` (a review of three commits);
custody of the 204 objects (H-336); Rust parity on all 60 (H-335); the BB header
enclosure guard for every external BB intake (`think-t41a`).

### 2.5 The hard tail: what was actually tried

The 95 distance-2 orbits (744 states) are the one-square moves of the family’s state
that survive the ledger.
The other 22 of the 117 move orbits are excluded: 21 by admitted sub-patterns (11 by W7,
10 by `s182-bc425-t1`) and one, u8, by its own whole-state certificate
(`s182-bc428-u8`). The exhaustive record of attempts at distance 2:

| Attempt | Instrument | Result |
| --- | --- | --- |
| H-273 float survey, all 95 | `survey_n17_residue --distance 2` | no placement at $U$ in 95 searches; sampled best penetration $9.1\times10^{-3}$; unresolved by design |
| u8 = mask 3078077 | 17-owner kernel, SW9 adaptive recipe, 7,000 s | **closed** in 572 s, verified in 277 s, admitted as `s182-bc428-u8` ([exp-257](../series/series-000-smoke-and-calibration/experiments/exp-257-h275-n17-unsampled-strata.md)); so not one of the 95 |
| u1 = mask 1900509 | same | incomplete at 7,001 s, not a fixed point |
| m1964767 | 17-owner kernel, N1 recipe, 32 uniform bins | fixed point after 8 rounds; consistency-limited |
| m851903 | same | fixed point after 2 rounds (88 s); consistency-limited |
| exp-303 contact rank, exp-304 envelope windows, exp-308 four-corner cardinality, exp-312 saved-pose incircles, exp-313/314 projections | necessary-condition filters | all 95 survive each |
| encoded centre-distance relaxations (W2 review, X-051 §3.1; replayed and extended *(review)*) | exact rational centres in each state’s own cells | all 95 survive with exact witnesses; see [2.6](#26-relaxations) |

Of the fifteen `criterion_missed` rounds of Sessions 184 to 186, four (exp-303, 304, 308
and 312) are the necessary-condition filters in the table above and ran on all 95. The
other eleven (exp-285, 286, 287, 291, 292, 293, 295, 297, 300, 301 and 305) and the five
accepted conditional rounds (exp-288, 296, 299, 302 and 307) worked on the family’s own
state at the numeric cap under a guard on owner 0 at $\tau = 53/128$: capture-side work.

**Finding.** X-051 §2.2(3) says the 95 “resist the pairwise kernel at every row width”.
The evidence on the surviving 95 is two fixed points at 32 uniform bins and one
incomplete adaptive run; the one per-state closure at distance 2, u8, took its orbit out
of the 95. No surviving distance-2 orbit has ever closed per state.
The adaptive recipe that closed 26 of 29 counted H-275 draws has run on one of the 95
(u1), at SW9’s 1,152-row cap and a 7,000 s ceiling, never with the cap raised.
**The hard tail is undersampled, not measured.** The consistency-limited diagnosis
(every owner at least 63 per cent supported on 100 float-sampled poses) is a strong
reason to expect m1964767 and m851903 to resist pairwise propagation, and says nothing
about the other 93.

**Why the two diagnosed states resist.** Their structure is three full walls, five
squares on a wall of length $3.676$, whose neighbours fail to clear each other by
$0.011$ to $0.018$; the family resolves the same crowding by tilting one square per full
wall (square 13 at $39.8^\circ$, square 16 at $-36.6^\circ$), and a one-square move
breaks the pattern that makes the tilts consistent.
The float survey reports a placement of a 14-cell sub-pattern of m1964767 and an
arity-15 deletion-search candidate for m851903 on which numerical search failed.
Neither failed search nor deletion-minimality proves infeasibility; placing one 14-cell
subset does not bound the size of other infeasible subsets.
A rigorously infeasible subset of size $k$ would give an upper bound on minimum
infeasible arity, not a lower bound on the arity of any certificate.
The current evidence suggests joint geometric obstruction without establishing its
minimum arity. A pairwise cut removes a pose only when every partner pose collides with
it, and an ownership induction has no owned points for most side cells from the seed.

**Margins.** Float penetrations at $U$ for distance-2 states are $0.009$ to $0.012$ of a
side, the same order as W7’s ($9.0\times10^{-3}$) and A’s ($8.8\times10^{-3}$), both of
which closed, and ten to twenty times the cap slack $4.7\times10^{-4}$; the engines’
resolution floors ($10^{-3}$ at $1/512$ rows; the BB chord error $gx^2/2$) are below
these margins.
These diagnostics motivate testing joint facts about orientation-dependent
extents along full walls; they do not establish that resolution or another configuration
could never help.

Remaining obligation: 95 distance-2 orbits (94 after #472), with per-state runs on three
and no closure; the engines’ stall fraction on the *current* residue is unmeasured.

### 2.6 Relaxations

| Claim | Status | Evidence | Concern |
| --- | --- | --- | --- |
| Every distance-2 representative, the first eight included, has exact rational centres in its own cells pairwise at distance $\ge 1$, accepted by `build_model` and `check_primal`; minimum squared distance over all 96 retained vectors $501001/500000$ | determined (W2 review; replayed *(review)* in 40 s with an independent point-in-cell test) | X-051 §3.1, [`centre-survivors.json`](X051-centre-survivors/centre-survivors.json) | registration only (H-328, blocked on an OR-1 tool) |
| No weighted-vertex or SOS certificate of any order, with or without a ball, exists for any of the 2,024 cell triples: each has a product vertex with all three squared distances $\ge 562823713/423200000$, a feasible point of its encoded system | determined (exact) | X-051 §3.2, PR 464 | none |
| **The encoded centre-distance relaxation has slack.** Maximising the minimum pairwise centre distance over centres in their own cells, then rounding to a $10^{-6}$ grid pulled inward and certifying in exact rationals: every distance-2 state admits exact centres pairwise at least $1.0305$ apart (exact worst, mask 3079037, slack $0.03049$; exact median slack $0.0821$; the family’s own state $1.102$), against float penetrations of about $0.01$ of a side, a ratio of about three | the slack witnesses exact *(review)* for all 95 and the endpoint control; the ratio of about three is a heuristic comparison of an exact centre slack with a float penetration, not determined | `centre_relaxation_slack.py`, `exact_slack_witnesses.py`; the float max-min worst, mask 3062655 ($0.0302$), has an exact witness at $0.0453$ | these witnesses leave at least $0.0305$ of slack in the encoded distance constraints; joint wall and pose constraints can carry further information, including the orientation-dependent extent of a square ($1/2$ on edge normals, $\sqrt2/2$ on diagonals) |
| Pairwise orientation coupling at the relaxation optimum is weak: at centre distance $1+\delta$ with $\delta \approx 0.03$ to $0.12$ the relative orientation is confined to $4^\circ$ to $17^\circ$ mod $\pi/2$ and the separating normal to within $14^\circ$ to $27^\circ$ of the connecting direction | derived *(review)* | same | per-pair supports need not share one simultaneous choice of poses |

What can still bite: joint branching on orientations with wall coupling (the BB;
B2-aimed splits reached closing depths 12 to 14 on arity-7 crowds; its tree size on 15
to 17 squares is unmeasured); ownership induction with closed half-cell branch
predicates (C5), the one grammar change aimed at the diagnosed mechanism, never built; a
state-conditioned charge (H-338), unbuilt.
Exact witnesses preclude exclusion by the encoded cell-membership and pairwise-distance
systems, including sound SOS hierarchies of those systems.
They do not preclude stronger constraints in centre variables obtained by eliminating
orientation, or joint pose compatibility: $\forall(i,j)\,\exists$ compatible poses does
not give one simultaneous pose assignment.
Wall-aware constraints already distinguish the models: centres $(1/2,13/10)$ and
$(13/10,1/2)$ have squared distance $32/25>1$, but containment forces both squares
axis-parallel and their $4/5$ coordinate gaps force overlap.
This illustrates the scope, without excluding a survey state.
Support sampled from 100 float poses at 32 uniform bins motivates a bounded test of
stronger relations on the two diagnosed states; it does not rule out every pairwise
configuration. See [5.5](#55-bounded-candidates-from-the-mathematical-review).

### 2.7 Contributor and external work

| Source | What exists | Status here | Projected residue if admitted *(review)* |
| --- | --- | --- | --- |
| **wand125, [#472](https://github.com/jlevy/squares/issues/472)** (9 Oct; labelled `n-17` at 17:12 UTC, no maintainer reply at 18:00 UTC) | 12 arity-8/9 kernel certificates made with `check_n17_subpattern` mode A, each passed by `verify_n17_kernel_certificate` in full (blob `1ad706c21`, the listed `kernel-streamed`); 411,682,476 bytes; producer 139–1,065 s and verifier 147–1,618 s each, 6,794 s summed; hosted on the contributor’s releases with HostedData/v1 manifests; receipts carry `dirty: true`, a wrapper revision and one hand-edited `directory` field each | reported; not in #405, `result-requests.yaml` or `intake-watch.yaml` | **3,636 orbits / 28,528 states** ($-1{,}047$ / $-8{,}240$); distance partition after: 2: 94/736 · 4: 940/7,384 · 6: 1,639/12,880 · 8: 799/6,296 · 10: 162/1,220; row 23 (m935012) removes the distance-2 orbit 1965787; row 34 is contained in admitted `s182-m7844815`, which it subsumes; the contributor’s 58-ledger figures 3,638 / 28,544 reproduce exactly |
| **wand125, [#413](https://github.com/jlevy/squares/issues/413)** (38 rows) | as edited at 17:04 UTC: 2 BB standing-FULL (rows 1, 2, at `9dcc05bc…`, the SHA-256 of unlisted blob `c69f1ec08`); 2 parallel-node (3, 4); 21 fast-verifier only (row 27 moved here in that edit); 11 kernel FULL (= #472); 2 computed (15, 33; row 33 about 480 GB as BB, now being retried with the kernel producer) | reported; the maintained `reconcile_n17_issue_patterns` hard-codes 33 rows and refuses the roster | all 38: 2,345 / 18,360; rows 1–2 alone: 4,641 / 36,452 |
| **wand125, [#358](https://github.com/jlevy/squares/issues/358)** | C1, C2 (arity 7, BB/v1, 552 objects / 400 MB), contributor FULL at `9dcc05bc…` (blob `c69f1ec08`); maintained C2 replay INCOMPLETE at 480 s on the RSS-monitor timeout (exp-311, H-319), not on memory; `think-b0ef` holds the repair | reported | 21 orbits / 148 states alone; nothing beyond the 38 rows’ union |
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

Capture for optimality concerns target packings $P$ with $s\le S^\ast$, normalized
concentrically in $C(S^\ast)$ with cells kept in the $U$ frame.
It must place their 45 non-slider coordinates within $r_j$ of $F(w)$ in the exact root’s
frame (angles as H254 lifts), with square 6 in `side-S2` and all other terminal premises
established. The search at $U'>S^\ast$ supplies an outer domain containing $P$; it may
also contain translated endpoint packings outside $C(S^\ast)$. A leaf $L$ must prove
$P\cap L\subseteq T$, where $T$ is the terminal theorem’s domain, rather than forcing
its $C(S^\ast)$ premise on every outer-node packing.

| Item | Run | Showed | Status |
| --- | --- | --- | --- |
| Two-cap design | H-288 / exp-275 | at $U$ the feasible set extends $0.08$ along $-\omega_{11}$; at $U'$ about $8\times10^{-11}$ | verified |
| From the cells at $U'$ | exp-276 / 277 / 280: one round of 16 owner updates (175 s), fresh replay, 49 root-relative intervals, centred control PASS_STALL | every owner’s orientation interval whole, every position its cell, all four terminal predicates false | readiness only; **one round ever run** |
| From a $1/1024$ box at $U'$ | pilots 1 and 2, 14 + 17 rounds, up to 4,664 live rows | no two-sided position extent moved; wall-fed one-sided bounds converged to $-1.26\times10^{-4}$ (the $2^{-12}$ pull); turn ranges $2\times10^{-3}$ to $2.8\times10^{-2}$, fixed across row widths | falsifier met; R9 leaves readings A (row-driven, needs $\ge 290$ row widths) and B (box-set fixpoint) open, B favoured by every number |
| Hull-pull repair ($2^{-12} \to 2^{-18}$ first) | `917163641`, 7 Oct | fixture recession $1.22\times10^{-4} \to 2.2\times10^{-6}$ | **merged on `main`** (`FINE_HULL_PULL = 1/2^{18}` in `producer.py`; ancestor of `6a0499ba4`) |
| n11 positive control through the n17 producer (H-337) | exp-268: first round only | 11 owner updates, readiness | 15-round contraction control **not run**; runnable now |
| R9 stage 1 (angle ranges at 2× and 4× rows from the box) | not run | — | open |

**Quantified gap** *(review, from the record’s slopes and the pilots’ receipts)*. Every
factor from the cells is a half-width over a radius: an angle ranges $\pi/4$ either
side, a position half its cell’s extent ($0.35$ to $0.485$; the cells are $0.7$ to
$0.97$ across). The first version of this table divided full cell extents by the radii,
which doubled every position factor.

| Start → target | Angle factor (bisections) | Position factor (halvings) |
| --- | --- | --- |
| cells (angles $\pi/4$; position half-widths $0.35$–$0.485$) → $r = 1/5000$ | 3,900 (11.9) | 1,750–2,425 (10.8–11.2) |
| cells → cube-form $1/1216$ vector (angles $8.2\times10^{-4}$, $\omega_{11}$ $4.4\times10^{-3}$) | 960 (9.9); $\omega_{11}$: 180 | 430–590 (≈9) |
| cells → widened LP region (angles $5\times10^{-3}$, centres $10^{-2}$) | 157 (7.3) | 35–49 (5.1–5.6) |
| pilot-2 end → cube-form $1/1216$ vector | 2–33 | 1.2–3 |
| pilot-2 end → widened region | 0.4–5.6 (axis squares inside; 9, 10, 16 not) | inside |

Even the widened terminal theorem leaves about seven bisections in every angle and five
to six halvings in every position from the cells.
The no-man’s-land, direction by direction, with $\kappa_j$ the fixed-feature LP slope
and $d_j = m/\kappa_j$ the displacement at which a margin $m$ above $U'$ becomes
visible: $-\omega_{16}$ ($\kappa = 0.0155$) needs $d = 0.65$ at $m = 10^{-2}$ and
$0.065$ at $m = 10^{-3}$; $-\omega_{11}$ ($0.0876$) $0.114$ and $0.011$; $+\omega_{13}$
($0.102$) $0.098$ and $0.0098$; the stiffest, $-\omega_{12}$ ($0.71$), $0.014$ and
$0.0014$. So at $m = 10^{-2}$ every angle direction has
$d_j \ge 0.014 > 5\times10^{-3}$, outside the widened box.
At $m = 10^{-3}$, the kernel’s measured loss floor at $1/512$ rows, the stiff directions
fall inside, but six still exceed $5\times10^{-3}$ ($-\omega_{16}$, $-\omega_{11}$,
$+\omega_{13}$, $-\omega_9$, $+\omega_{10}$, $-\omega_{13}$); at most two exceptions
needs $m \le 0.102 \times 5\times10^{-3} \approx 5\times10^{-4}$, below that floor.
The soft block directions ($-\omega_{16}$, $-\omega_{11}$, $+\omega_{13}$) need a
non-margin argument between $5\times10^{-3}$ and $0.01$ to $0.07$ rad under any
plausible $m$: the feature-flip atlas (H-339) or a bigger terminal theorem along those
directions.

Routes, assessed: (a) pairwise ownership induction from the cells, the n11 engine
(contracted at n11 in 14 rounds), untested from the real start point at n17; the n11
control (H-337) and a 15–20-round cell-seeded run test the specified configuration for
hours of CPU. A threshold miss is a budget decision unless a fixed point or invariant is
proved. (b) Box-seeded pilots: four runs agree with reading B; low value until (a) is
answered. (c) Dual-sheet patch certificate over the feature-forced region (H-329): sound
in principle, exact rational duals per direction patch plus interval Hessian bounds,
apex needing no subdivision; risks are dual degeneracy at the apex (optimal face of
dimension about 17), the unknown softest *direction* on $S^{15}$, and feature forcing
established only conditionally (H-278); the interval machinery exists (exp-263, 267,
269), the direction-patch certifier and the patch counter do not.
(d) Branch and bound over angles with a valid affine LP lower model and certified
remainder, closing when the bound exceeds $U'$ and stopping inside the terminal region:
a candidate for the cells-to-feature-forced bridge, subject to the localization
obligations below; node count unknown, a Knuth estimate is “days of build, minutes to
run”. (e) Feature-flip atlas (H-339): extends the LP region to about $2\times10^{-2}$;
the inner edge of (d), not a bridge.
(f) Interval Newton or Krawczyk on the family: the wrong tool for an inequality
statement (it certifies uniqueness of the tight-contact *equality* system), with the
same conditioning; right inside (c) for the parametric dual solve.
(g) A larger ratio-test radius: the C7 constants set the uniform threshold near
$1/4391$; $1/1216$ is the largest composed cube-form floor found in the retained search,
not a universal ceiling.
Per-square slide coverage and the $1/1152$ vector at a larger slide radius remain
untried ([5.5](#55-bounded-candidates-from-the-mathematical-review)).

For (d), a dual sheet $L_B\le v$ valid on the whole angle box must retain its affine
variation:

$$\inf_B v\ge L_B(c)+\min_{\delta\in B-c}g_B^T\delta-R_B.$$

Subtracting only a quadratic remainder from the centre LP value is unsound when the
first derivative is nonzero.
A certified quadratic error can apply to the retained affine model.
Prove dual feasibility throughout the box and cover all basis or separating-feature
changes, or use an outer relaxation retaining angle increments.
Root nodes must retain every cell-allowed slider position and unresolved feature
alternative. The scope review’s narrow slider box cannot be imposed without a proved
target-valid implication or complete branching.
Each terminal leaf must establish all premises for every target packing in $P\cap L$,
including slide coverage and universal centre bounds.
Bounding both signs of each required coordinate over the full outer relaxation is a safe
sufficient localization method.
Inherited $C(S^\ast)$ containment and consequences such as $a\ge0$ apply conditionally
on $P$; they need not hold for all outer packings at $U'$. One nearby optimizer supplies
no universal bound.

Remaining obligation: the whole of it.
Nothing has contracted from the cells; the terminal target is $10^{-3}$ to $10^{-4}$; no
capture receipt computes the conversion allowances $E_j$ the composition needs.

### 2.9 The local family theorem

| Claim | Status | Evidence | Concern |
| --- | --- | --- | --- |
| Capture-target theorem: a packing of side $s \le S^\ast$ in the family’s state, concentric in the cover frame, with its 45 non-slider coordinates within $r_j$ of the family’s at the exact root, has its slides in $B_W'$, the sixteen squares other than 6 exactly at $x^\ast(w)$, and $s = S^\ast$ | proved with one review; exact certificates C1–C4, C6–C11 (exp-244 on $B_W$, exp-248 run-002 on $B_W'$): 45 lifts, rank 45, 125 options negative with Taylor margins, per-cell affine duals ($2^{-44}$ dyadics) on 93 cells, ratio test; replayed from `main` *(review)*: worst $0.925818092269$ ($B_W$), $0.925931049178$ ($B_W'$), 10 s each | [exp-248](../series/series-000-smoke-and-calibration/experiments/exp-248-h268-n17-local-half-composition.md), [recipe review](../../../docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md), [composition review](../../../docs/project/reviews/review-2026-10-02-n17-local-half-composition.md) | hand lemmas 1–6 have one AI review; lemmas 2 and 5 and the curvature bound now have a second derivation *(review)*; no defect found |
| Slide coverage (H-268): $a \in [0, 23/200]$, $b \in [b^\ast, 37/500]$, $z \in [-49/1000, 0.0241]$ with square 6 in its cell | verified (exact/outward, 3 controls); replayed at $R = 9/2048$ *(review)*, 8 s | exp-248 run-001 | the separation lemma is sharp; a widened neighbourhood needs new coverage |
| Cube-form vector: floor $1/1216$ on $B_c$, $\omega_{11}=85/19456$, $u_{11}=33/19456$, $\omega_8,\xi_8=71/77824$, $\omega_{16}=67/77824$ | component, unregistered; retained worst $0.999316555505$, 109 cells | [cube-form receipt](X048-session-168-pilots/receipts/local-radius/ratio-composition-1216.json), H-340 | largest composed floor demonstrated by this search; $1/1152$ exceeds the retained slide radius, leaving a larger-radius composition untested |
| Capture-form vector: ordinary angles $1/1024$, ordinary positions $11/32768$ (obtained by rounding $1/3072$ upward to the retained dyadic grid), $\omega_{11}=249/65536$, $u_{11}=97/65536$, $\xi_8=13/16384$, $\xi_3,\eta_8=39/65536$ | component, unregistered; retained worst $0.999368209930$, 117 cells, minimum $11/32768<1/1216$ | [capture-form receipt](X048-session-168-pilots/receipts/local-radius/ratio-composition-capture.json) | a different anisotropic vector; its ratio does not certify a uniform $1/1216$ floor |
| Uniform floors: $0.87815254$ at $1/5000$, $1.7564$ at $1/2500$, $4.2888$ at $1/1024$; $5000 \times 0.87815 = 4390.8$, so the “$1/4391$” figure is right | verified *(review)* | `check_n17_local_radius scan` | **exact only relative to the recipe’s C7 curvature constants**; a different curvature lemma changes $K$; a signed-second-order lemma was modelled at $\le 2\times$ in floats |
| What sets the scale: the $-\omega_{11}$ certificate’s $\ell_1$ mass is 1,421 (support on all 52 rows; the review’s 1,439 is the point-program dual at the worst $1/5000$ vertex) against $K_{\text{pair}} \approx 9.7r^2$, more than half of it the angle–position cross term; $\kappa_\infty = 1/175.8$ | computed *(review)* from the exp-248 certificates | — | the tilted block’s co-rotation with the 9/11 face open is the soft mode; the dual-sheet route removes the bilinear remainder by treating positions exactly at fixed angles, which motivates testing the proposed enlarged region |
| H-261 “unresolved as worded” | the 5/6-exchanged witness is a relabelled family member ([Section 3](#3-corrections-to-the-record)) | `family_sat.py` *(review)* | not a packing off the family; the claim is not refuted |

Both anisotropic receipts use $B_c=[0,4/25]\times[-1/128,11/100]\times[-13/200,1/30]$
and slide radius $R=9/2048$. Composition requires $\max_j r_j\le R$ and
$B_{\rm slide}(R)\subseteq B_{\rm local}=B_c$: the local box must contain the
slide-coverage output.
The dated H-340 correction states this inclusion explicitly.

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
| Local theorem | 128 feature branches × 33 coordinates; two-radius $1/256$; worst ratio $0.6765$ | 52 rows × 45 coordinates at the moving base point; $1/5000$ uniform, cube-form floor $1/1216$; worst $0.9259$ / $0.9993$ | yes, same recipe and curvature formula; radius 8–20× smaller |
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
  says 58 / 36,784 / 4,685 at lines 59, 251, 382 and 441; X-048’s current selection and
  `SYNOPSIS.md`’s Session-184 narrative say the same.
  `main` has carried 60 / 36,768 / 4,683 since `533dd42c6` (9 Oct, 09:22 UTC).
- **Register wording.** T-065’s claim in `results.yaml` and `RESULTS.md` still says “No
  identity with the catalogue’s degree-18 polynomial is proved”; exp-245 proved it on 2
  October; `think-yjgk` (open since 5 Oct, “close when PR 347 merges”) never landed the
  text.
- **Tracker.** #405’s latest comment said the landing added no census admission, though
  Tail A and B reached `main` with it, and that #403 and #442 conflict with `main` (both
  are MERGEABLE/CLEAN); an edit at 17:12 UTC added correction notes on both points (C8
  and C12, applied). #405 does not mention #472, the BC-423/426 held closures
  (`think-yg80`, two closures that passed standing FULL and await an owner ruling),
  Kleddamag’s research checkpoint, or the missing verifier listing, and lists #413 at 33
  rows.
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
| C3 | H-330’s falsifier | “at most two directions with $d_j$ above the terminal radius” at the margin H-325 reports | at $m = 10^{-2}$ every angle direction has $d_j \ge 0.014 > 5\times10^{-3}$; at $m = 10^{-3}$, the kernel’s loss floor at $1/512$ rows, six directions still exceed $5\times10^{-3}$; the claim can hold only if $m \lesssim 5\times10^{-4}$, below that floor, where the engines see nothing; the map is worth making with $m$ as the variable | the scope review’s slopes; [2.8](#28-capture) | H-330 dated note (done here); re-scope before any round |
| C4 | The tail “resists at every row width” | X-051 §2.2(3) | per-state runs exist on four distance-2 orbits: u8 closed and so left the residue; of the surviving 95, u1 is incomplete at 7,001 s and m1964767 and m851903 are fixed points under 32 uniform bins; no surviving distance-2 orbit has ever closed per state, and the adaptive recipe has run on one of the 95 (u1), at SW9’s 1,152-row cap | exp-257, stall classification | read as “undersampled”; H-343 measures it |
| C5 | The “exact floor” near $1/4391$ | local-radius review, X-051: “an exact floor, and no finer curvature lemma buys more than a factor of two” | exact relative to the recipe’s C7 constants; a finer lemma was modelled at $\le 2\times$ in floating point | `scan` replay *(review)* | wording, no consequence |
| C6 | T-065’s register wording | `results.yaml` line 5830, `RESULTS.md`: “No identity with the catalogue’s degree-18 polynomial is proved” | exp-245 proved the identity on 2 October; n-017’s prose says so | exp-245 | the T-065 claim text, under the result-import procedure (`think-yjgk`) |
| C7 | Stale counts | explainer lines 59, 251, 382 and 441, X-048 line 127, SYNOPSIS Session-184 narrative: 58 / 36,784 / 4,685 | 60 / 36,768 / 4,683 on `main` since `533dd42c6` | census tool on this worktree | the explainer when next touched; X-048’s current selection |
| C8 | Tracker census claim | #405 latest comment: “No exclusion, census admission, T item or optimality claim was added” | Tail A (`s184-tail-a-m3096311`) and Tail B (`s184-tail-b-m3096315`) reached `main` with the landing: 58 → 60 entries | `git show 3213d651b:…certified-sub-patterns.yaml` (58) vs `533dd42c6` (60) | #405: applied, a correction note added to the latest comment at 17:12 UTC |
| C9 | #413 and #472 in the tracker | 33 rows, “eighteen fast-only and eleven computed”, union 2,234 / 17,604; row 23 computed | 38 rows: 2 + 2 + 21 + 11 + 2 since #413’s edit at 17:04 UTC made row 27 fast-verified (2 + 2 + 20 + 11 + 3 before it); union 2,338 / 18,408; row 23 kernel FULL-reported; #472 absent | #413 body and edit history, #472 | #405, `result-requests.yaml`; the `n-17` label was added to #472 at 17:12 UTC |
| C10 | “The dual-sheet instrument has never been built” | X-051 §2.2, explainer | true of the direction-patch certifier and the patch counter; the interval machinery for box patches and cones exists (exp-263, 267, 269) and is the base to build on | exp-263/267/269 | H-329 notes |
| C11 | Explainer’s “first-order feasible radius about $2\times10^{-10}$ at $U'$” |  | $7.9\times10^{-11}$ with the actual cap | `root_and_caps.py` *(review)* | immaterial |
| C12 | PR state in the tracker | #403 “fails CLS and conflicts with main”; #442 “conflicts with main” | #403 `c1d3aab9` MERGEABLE/CLEAN, 31 checks pass; #442 and the intake stack CLEAN (#469 UNSTABLE) | `ghx pr view`, 9 Oct 16:40 UTC | #405: applied, update notes added to the latest comment at 17:12 UTC |

No soundness defect was found in the endpoint, the local theorem, its composition, the
cap join, the cover, the census, the transfer rules or the kernel grammar.

## 4. A Sufficient Set of Remaining Mathematical Results

It suffices to show that every closed-cell state is either excluded at a root-joined cap
or captured into a terminal theorem implying $s\ge S^\ast$. The proposed route uses the
existing family theorem for the endpoint state and exclusions for the rest:

1. **Exclusion of the non-endpoint residue.** 4,682 orbits (36,760 states) in this
   snapshot; 3,635 after #472; about 2,340 after everything reported.
   An entry may use its own positive rational centred cap $V_K\le U$ with an exact join
   proving $V_K>S^\ast$. If its minimum side $m_K$ lies in $(S^\ast,U']$, any rational
   $V_K\in(S^\ast,m_K)$ suffices.
   Feasibility at the chosen operational cap $U'$ therefore need not require another
   local theorem. In this route, a state with $m_K=S^\ast$ cannot be excluded above the
   root and requires a terminal argument.
   Optimality does not require one equality mask or uniqueness of optimal packings.
   Each centred-cap certificate also needs a listed verifier with centred-cap support;
   in the surveyed snapshot only the unlisted kernel blob `be8135f6e` has it.
   The family’s own state cannot be excluded at a cap $\ge S^\ast$. Alternative
   assignments of free square 6 must be covered by these exclusions or a geometric audit
   on their full applicable domain; §2.3’s exact-skeleton audit covers only its stated
   smaller slider box.
2. **Capture of the family’s state.** For every target packing with $s\le S^\ast$ in
   that state, normalize concentrically in $C(S^\ast)$, carry the group element and use
   state-induced labels.
   Every terminal leaf $L$ must prove $P\cap L\subseteq T$ for these target packings
   $P$. The current theorem’s premises include the slider domain, square 6 in `side-S2`
   and bounds on all 45 non-slider coordinates within $r_j-E_j$ of the family in the
   exact root’s frame. Searching the outer $U'$ domain is sufficient if it retains $P$;
   inherited $C(S^\ast)$ premises apply to $P$, without requiring them of every
   outer-node packing. The exchanged 5/6 configuration is the family relabelled; fixed
   labels give a disconnected slider domain.
3. **Exact conversion allowances $E_j$** (frame, basis, angle chart, $u^\ast$
   enclosure), so that the capture bounds compose with the local theorem.

There is a geometric existence argument for smaller caps, but no numerical gap or
prover-completeness conclusion: for a fixed closed-cell assignment, containment at
$s\le U$ and orientations modulo square symmetry give a compact feasible set.
A nonempty such set with no packing at $s\le S^\ast$ has attained minimum above
$S^\ast$; an empty set is already impossible at $U$. Finitely many such states have a
positive common gap, hence some common rational cap above the root excludes them
geometrically. Whether the current prover can certify this remains open; per-entry caps
are allowed by the existing interface.

Custody, two-verifier parity, the composition checker, verifier listings and Lean supply
assurance. The below-root cap ladder is a separate lower-bound result; above-root
exclusions can contribute to this sufficient route.
The hard tail and capture engine remain unpriced after the proposed bounded
measurements.

## 5. Directions to Completion

### 5.1 Ranked

Costs are for the first decision each direction yields, in CPU-hours and agent-hours;
“information” is what the record gains whichever way it goes.

| # | Direction | Mechanism | Establishes | Falsifier / early kill | Prerequisite | Cost | Information |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Admit #472 and convert the BB-only #413 wall rows to kernel certificates** (H-341, H-342) | clean-worktree full replay of the twelve under a listed verifier, Rust parity, hosting and an admission round; then mode A on BB-only rows with a wall cell, recording actual seed ownership, cell type and propagation | projected residue 4,683 → 3,636 → about 2,400 orbits; distance-2 tail 95 → 94 | a full-mode refusal, parity disagreement or kernel stalls on most tested rows | verifier listing or replay at `1ad706c21`; OR-18 hosting decision | #472: ~2 CPU-h, ~4 agent-h; conversions: ~10 CPU-h, ~6 agent-h | tests wall-cell presence as a routing predictor; corner anchoring differs from unsplit side cells, and small interior cells can own seed regions |
| 2 | **Measure the hard tail** (H-343) | SW9 adaptive recipe with cap 2,304 and a 2-hour production ceiling on all 94 distance-2 representatives plus a uniform 60-orbit draw from distance at least 4; report closed, verified fixed-point, timeout and unresolved outcomes separately | bounded closure rates in the tested strata and diagnostic evidence for follow-up | fewer than 47 distance-2 closures misses the production budget criterion; the sampled-rate conjunct must also hold; neither outcome diagnoses the whole method | H-341’s partition; zero build | ≤ 308 CPU-h production plus verification at 2,304 rows, unmeasured; ~6 agent-h | weight strata for a residue-wide orbit estimate and orbit sizes for a literal state-weighted estimate |
| 3 | **Test capture from the real start point** (H-337 then H-345) | n11 positive control through the repaired producer for 15 rounds, then 20 rounds from the n17 family’s cells at $U'$ | contraction of the specified configuration within its budget | n11 or n17 threshold miss stops this configuration; less than 10 % movement is not a proved fixed point or rejection of the architecture | none (repair merged) | 2–4 + 5–20 CPU-h, ~4 agent-h | bounded comparative evidence; capture into the terminal region is a separate obligation |
| 4 | **Terminal theorem by exact dual sheets** (H-340, then H-329, H-339) | freeze the actual anisotropic vector; sample directional optima as diagnostics; run a small certified patch pilot before pricing the full cover; for every surviving feature branch and angle patch provide a valid dual lower bound at least $S^\ast$ or prove infeasibility | an exact terminal cover if the relaxation and patch certification succeed | a certified deficient optimum rejects that relaxation at the point; rank, conditioning and coverage failures leave regions unresolved; floating richness alone is not a patch-cost threshold | exp-244 machinery; H-278 extended to the box; reviewed zero-turn LP equality | H-340 ~15 s; pilot one slice, ~12 agent-h; full-build CPU budget set after measured coverage | report proved coverage, unresolved regions and rank failures; Chao1 counts estimate a lower bound on category richness, not a certification-patch upper bound |
| 5 | **Price the corrected outer bridge** (H-346) | retain an affine LP lower model and certified remainder; keep all cell-allowed sliders and feature alternatives until proved localization; prove $P\cap L\subseteq T$ for target packings ([2.8](#28-capture)) | empirical pricing for this complete angle-and-feature design | require estimates below $10^8$ at the widened leaf and $10^{10}$ at the cube-form $1/1216$ leaf under the declared uncertainty rule; overlapping uncertainty stays unresolved | certified leaf plus root-to-leaf localization design; a smaller-radius leaf is a separate design | days of build (~25 agent-h); probe cost measured on that design | report maxima, dispersion, independent batches and feature coverage; floor hits, LP failures, censored probes and incomplete branching yield truncated-tree pricing, not proof-tree cost |
| 6 | **The foolproof package** (H-336, H-335, H-334, H-347, H-348, H-333; the verifier listing; T-065 wording) | host the 204 objects; Rust parity on every kernel admission; a composition checker reading cover, ledger with per-entry caps, capture and local receipts; exact $E_j$; a second local-theorem checker; Lean for the three short lemmas | the proof becomes a checkable object; the trusted base is listed in one place | an accepted mutant; a failed fetch; $E_j \ge r_j/10$ | an owner decision on hosting | custody ~20 CPU-h + decision; parity a day of two workers; checker 20–40 agent-h; $E_j$ 10–20 agent-h; local checker 20–30 agent-h; Lean 10–30 agent-h | nothing mathematical moves; without it every admission is a receipt |
| 7 | **Closed half-cell branch predicates (C5)** (H-344) | halve a side cell along its long axis into closed children, each with a seed core; a consumer rule that admitted children cover the parent, seams included; test on m1964767, m851903, m1949551 | an engine for consistency-limited states | fewer than two of the three states have both children verified closed within each child’s 4× ceiling; a failed consumer control rejects the instrument | the verifier accepts n11’s predicate grammar; the n17 node and consumer do not | one build slice plus review (1–2 weeks); runs 2–4× a parent | the only grammar change aimed at the diagnosed mechanism |
| 8 | **Cap scan read as margin versus direction** (H-325; H-330 with $m$ as the variable) | whole-state kernel and BB on the family’s state at $S^\ast - \{2, 5, 10, 15\}\times10^{-3}$; the fixed-feature LP slopes against the margin found | the margin the engines see on the hardest state; prices the cap ladder and the bridge | a stall at $1.5\times10^{-2}$ | the producer accepts a cap below the root box (one-line check) | 4–8 CPU-h, ~4 agent-h | one number nobody has; mostly informs capture |
| 9 | **Kernel closure of the 34 flagged, uncertified classes on no contributor roster** (H-349) | `check_n17_subpattern` mode A with adaptive rows on the 34 of the census tool’s 69 selector flags that are $D_4$-identical to no contributor pattern | at most about 200 orbits more: 198 if all 34 close after everything reported (2,343 → 2,145) | fewer than 28 of 34 close in 30 minutes each | none | ≤ 17 CPU-h of production plus verification | the kernel’s stall fraction on flags no contributor has run |
| 10 | B2 on interior crowds and small-margin candidates (H-331); decomposability survey (H-327); state-conditioned charge (H-338) | numerical subsets are candidates; certify infeasibility before assigning arity conclusions | tested reach of BB and counting on the tail | each bounded configuration’s declared criterion | H-327 with minimal-versus-minimum correction | 20–60 CPU-h; 5–15 CPU-h; 20 agent-h | an infeasible $k$-subset bounds minimum infeasible arity above by $k$; float failure supplies no such bound |
| 11 | Cap ladder (H-326) | exclude every residue orbit at $V_1 = S^\ast - 10^{-2}$ | $s(17) > V_1$, $+5.1\times10^{-3}$ over R071 | a 30-orbit pilot with fewer than 27 closures | 8 and most of 1–2 | 100–4,000 CPU-h | a verified bound; its certificates do not enter the proof; worth the measurement, not the campaign, until 1–2 have shrunk the residue |

**Directions 1 and 9 are not additive** *(review)*. Of the census tool’s 69 flagged
classes, 30 are direction 1’s own targets (7 #472 masks and 23 H-342-eligible #413
rows), 4 are rows 1–2 or C1/C2 (H-332) and 1 is row 5. After #472 and every
H-342-eligible row the residue is 2,353 orbits, and all 69 flagged classes take it only
to 2,145, a net of 208; the 1,491 orbits they would remove after H-341 alone (3,636 →
2,145) are mostly H-342’s patterns.
The two directions’ combined ceiling after H-341 is 2,145 orbits, which is why H-349 is
scoped to the 34 classes on no roster.

The dual obligation in direction 4 is branchwise:
$v(\theta)=\min_f\sup_{\lambda\in D_f(\theta)}\lambda^Tb_f(\theta)$. One adequate
feasible dual sheet per patch and surviving branch suffices; a weak sheet does not
refute the LP, and proving every feasible sheet exceeds the target is unnecessary.
The dated corrections to inherited H-327, H-329 and H-340 supply the arity,
dual-quantifier and slide-box obligations in §2.5, here and §2.9; instrument builds must
carry them through.

Floating active-row sets need not be independent bases at degeneracy.
Several bases can represent one dual sheet, and one sheet can require several
certification patches, so the richness counts remain diagnostics.
For H-346, price each leaf with at least four independent 500-probe batches and the
predeclared empirical 95 per cent intervals over batch means: both upper endpoints must
meet their thresholds, lower endpoints above either threshold reject that conjunct, and
overlap stays unresolved.
Small empirical error can still miss a rare expensive subtree; this is pricing evidence.
Only probes accounting for all children and ending in validated leaves can support the
proof-tree estimate.

### 5.2 Parallel lanes with disjoint deliverables

| Lane | Hypotheses | Deliverable | Owner skill | First week |
| --- | --- | --- | --- | --- |
| A. Admission and census | H-341, H-342, H-349; H-332 re-scoped to the kernel route for C1/C2 and rows 1–2 | regenerated ledger, census and partition receipts; a verifier listing for `be8135f6e`; the reconciliation tool reading 38 rows | engineering, admission review | #472 replay and parity; answer #472; rows with wall cells queued |
| B. Hard tail | H-343, H-327, H-331, H-344, H-338 | per-state verdicts and a stall classification of the current residue; the C5 grammar build | kernel producer, BB, diagnostics | all 94 distance-2 representatives launched under the adaptive recipe |
| C. Capture engine | H-337, H-345, H-325, H-330 (re-read), H-346 | a bounded contraction result from the real start point; the margin-versus-direction map; corrected bridge pricing | capture producer, LP | H-337 and H-345 tested; H-346 localization and affine-bound design reviewed |
| D. Terminal theorem | H-340, H-329, H-339, H-347 | registered terminal radii; certified-patch pilot and slope diagnostics; exact patch certificate; exact $E_j$ | exact LP, intervals, review | H-340 registered; small certification pilot measured |
| E. Assurance | H-336, H-335, H-334, H-348, H-333; T-065 wording; explainer and tracker refresh | hosted objects; two-verifier parity on all 60; the composition checker; a second local checker; Lean for three lemmas; a record that matches `main` | custody, verifiers, Lean | hosting decision taken; parity run on the seven objects in hand plus #472’s twelve |

Lanes A, B and E share the kernel verifier and the census tool but write disjoint
artifacts; C and D share exp-244’s duals and nothing else.
OR-2 and OR-6: three to five sub-agents at a time, one per lane, each with a slice of a
day or less to a falsifiable verdict.

### 5.3 Critical path, with the uncertainty stated

```text
week 1   A: #472 admitted; wall rows queued      C: H-337, H-345 verdicts     D: H-340 registered, patch pilot
week 2   A: ~2,400 orbits                        C: H-346 estimate            D: coverage and slope diagnostics
         B: 154 bounded per-state outcomes, stratum rates known                      E: hosting, parity on 60 + 12
weeks 3-6  B: kernel/BB/C5 on what is left (priced after week 2)
         C+D: either an engine that reaches the terminal region, or a bridge BB with a node count
weeks 6+  E: composition checker reads everything; the statement is emitted or a named orbit is open
```

What is priced: lane A to about 2,400 orbits (two weeks); lane B’s measurement (two
weeks of CPU); lane D’s certification pilot and H-340 (one week); lane E except the
hosting decision.
What is not priced, and is the honest uncertainty: the hard core of the
tail after lane B (if the diagnosed numerical candidates are typical, the current search
points to joint obstruction across many squares, with C5 and the BB both unmeasured at
that arity), and the outer bridge of capture (H-346 is the pricing step; if the
corrected design is too expensive at either leaf, that design or budget is rejected,
with a larger terminal theorem along the mixed soft modes one candidate).
The projected $10^3$ CPU-hours to reduce the residue to a few hundred orbits assumes
that measured closure rates extend to the remaining states; neither that projection nor
successful capture is established.

### 5.4 What to stop

- Further exclusion attempts on the witnessed cell-membership and pairwise-distance
  systems, including their sound hierarchies, unless the constraints change
  ([2.6](#26-relaxations)); retire the corresponding stale work with its scoped outcome.
  Stronger wall-aware, orientation-eliminated or joint-pose constraints remain eligible
  for bounded pilots.
- Conditional propagation inside one owner-0 guard as a route to the tail (eleven
  misses, no consumer; `think-98mg`, `think-lyh9`).
- Box-seeded kernel capture pilots (R9 stages 1–2) before H-337 and H-345 have run.
- BB certificate replays, and 480 GB acquisitions, for patterns the kernel closes; BB
  only for genuinely interior crowds.
- Re-running the same failed radius/slide composition unchanged; a larger slide radius
  or per-square coverage is a distinct, untested configuration.
- A new reconciliation document per merge gate; the tracker and the explainer are the
  two living documents, and the explainer should be regenerated from the census tool.

### 5.5 Bounded candidates from the mathematical review

These are conditional design candidates, not active funded experiments or new registry
claims. Each needs a frozen domain, resource ceiling and accept rule before launch.

- **Joint pose relations.** The earlier flag-B calibration already retained a complete
  binary-network selection for all 96 rows at 16 bins/two rounds
  ([X-048](X-048-n17-optimality-after-n11.md)). Stronger consistency on those same
  relations cannot remove their witnessed supports.
  Audit the current diagnosed states first.
  A stronger pilot must share centre subdomains and common separator poses along wall
  chains, or add justified higher-arity relations.
  The cheapest predicate is simultaneous three-owner feasibility, sharing the middle
  owner’s centre and angle across both contacts and covering every separating feature.
  Killing one tuple does not exclude a row with replacement support.
  Use complete outer pose domains and exact local exclusions; sampled poses cannot
  exclude the continuous domain.
  Price separator width and table memory before joins; large infeasible-subset arity
  alone says nothing about that width.
  Accept certified contraction or exclusion beyond the old relations with the endpoint
  retained; stop the configuration if outer relations remain satisfiable without useful
  contraction or exceed its memory ceiling.
  Relations derived from saved seventeen-owner nodes inherit the full induction history
  and cannot become original-cell arity-three exclusions without independently justified
  restrictions.
- **Mixed-mode terminal polytopes.** Reuse the exact signed-coordinate support solves in
  `check_n17_local_minimum`, recovering mixed rays from their active rows.
  On the same homogeneous quotient cone, finite attained angular supports
  $a_{j,\pm}=\max\{\pm d_j:A_Pz\ge0,\sigma\le1\}$ already give normalized angular growth
  $1/\max_{j,\pm}a_{j,\pm}$; another 32-facet solve duplicates that information.
  Compare these rays with the differently constrained widened LP, then test a rational
  change of coordinates and a terminal polytope elongated along the soft mixed modes.
  Certify bounds across the root interval, moving sliders and feature branches: the
  point solve at midpoint and centroid sliders is diagnostic.
  Restored contact or wall rows change the slider quotient, so retain one-sided tangent
  inequalities at physical boundaries or rebase at the actual slide.
  Cover the 13/14 offset-sign seam by closed branches, and use the two-row
  absolute-value reduction at cooriented faces
  ([branch analysis](../../../docs/project/reviews/review-2026-10-01-n17-first-order-branches.md)).
  A ray of a weakened model need not integrate to a packing.
  Accept only a certified extension with feature forcing, slide coverage, strict
  whole-region remainder bounds and measured capture benefit.
  A failed bound rejects this widening.
  The cheaper precursor is per-square slide coverage using the actual radius vector; the
  retained $1/1152$ proposal at a larger slide radius also remains untried.
- **Above-root cap ladder.** On a small fixed set of stalled non-endpoint states,
  compare the same engine and budget at rational caps $V_k\downarrow S^\ast$, each
  exactly root-joined.
  Retain the first verified closure and its cap.
  A state that stalls at $U$ but closes above the root contributes directly to
  optimality; failure only rejects this cap change for the tested engine.
  H-326’s below-root ladder has a different lower-bound purpose.
- **Alternative-assignment cuts.** If occupied $i$ and vacant $j$ in a surviving mask
  $K$ give an already admitted exclusion $K'=(K\setminus\{i\})\cup\{j\}$ at a cap
  covering the current domain, the square assigned to $i$ cannot have its centre in
  $C_j$: reassignment would realize $K'$. Prune $C_i\cap C_j$ using a complete branch
  cover of the nonconvex remainder; closed exterior half-planes safely overcover strict
  polygon exteriors. Carry the cap and $D_4$ transport, using only previously admitted
  exclusions to avoid circularity.
  First enumerate swaps on the endpoint and diagnosed states, then measure domain or
  seed-core improvement.
  Stop if overlaps give no useful cuts or contraction.
  Consumer/verifier support is required before admitting any resulting closure.

## 6. Candidate Hypotheses

Nine new registry files, H-341 to H-349, each with `derived_from: [X-052]`, for the
directions H-325 to H-340 do not cover; three dated corrections to existing files
(H-261, H-330, H-337), none of which changes a frozen criterion of a registered
experiment.

| Id | Claim | Mechanism | Falsifier | Expected information | Limits |
| --- | --- | --- | --- | --- | --- |
| [H-341](../hypotheses/H-341-n17-issue-472-kernel-admission.md) | #472’s twelve kernel certificates pass a clean-worktree full replay under a listed verifier and Rust parity, bind to the exp-247 cover at $U$, and their admission reproduces 3,636 orbits / 28,528 states with the distance-2 tail at 94 | same format and frame as 59 admitted entries; the verifier derives closure itself | a full-mode refusal, a parity disagreement, or a census mismatch | $-1{,}047$ orbits; the admission path exercised on external objects | custody and a verifier listing are prerequisites, not mathematics |
| [H-342](../hypotheses/H-342-n17-kernel-conversion-of-bb-rows.md) | at least two thirds of the BB-only and computed #413 rows that contain a wall cell close under `check_n17_subpattern` mode A with adaptive rows within 30 minutes each, with certificates under 100 MB | wall-cell presence is an empirical predictor; record actual seed ownership and propagation, distinguishing corners, unsplit sides and small interior cells | fewer than two thirds close | up to about 1,300 orbits more (3,636 → 2,353 if all 24 eligible rows close); the kernel-versus-BB routing rule | interior crowds stay with the BB |
| [H-343](../hypotheses/H-343-n17-hard-tail-adaptive-measurement.md) | at least half of the 94 distance-2 representatives not covered by #472 close under the 17-owner kernel with SW9’s adaptive recipe and its row cap raised to 2,304, within 2 hours each, verified in full, and a 60-orbit draw from the rest closes at a rate within 2× of theirs | the recipe closed 26 of 29 counted draws on a different frame | fewer than 47 of 94 close, or the sampled closure rate falls outside the factor-of-two band | budgeted closure rates for distance 2 and the sampled distance-at-least-four stratum | separate verified fixed points from timeouts and unresolved outcomes; weight strata and orbit sizes for broader estimates |
| [H-344](../hypotheses/H-344-n17-half-cell-branch-predicates.md) | with closed half-cell branch predicates and a consumer rule that admitted children cover the parent, the kernel closes both children of at least two of m1964767, m851903 and m1949551 within 4× the parent’s time | halving a side cell gives every child a seed core, which the consistency-limited stalls lack | fewer than two states have both children verified closed within the per-child ceiling; a failed consumer control rejects the instrument | an engine for consistency-limited states | unbuilt; seams must be in both children |
| [H-345](../hypotheses/H-345-n17-cell-seeded-twenty-round-capture.md) | 20 rounds of the repaired producer from the family’s cells at $U'$ reduce at least one owner’s turn range or wall-fed position extent by 10 % of its round-1 value | the n11 root node contracted from its cells in 14 rounds | nothing moves by 10 % in 20 rounds | whether this configuration contracts within the budget | a threshold miss proves neither a fixed point nor architectural impossibility; reaching the terminal region is separate |
| [H-346](../hypotheses/H-346-n17-angle-bb-knuth-estimate.md) | corrected angle-and-feature branch and bound at $U'$ estimates below $10^8$ nodes to the widened leaf and $10^{10}$ to the cube-form $1/1216$ leaf | affine variation retained; certified remainder and $P\cap L\subseteq T$ for target packings | either threshold missed under the declared uncertainty rule; overlapping uncertainty unresolved | empirical pricing of this bridge design | complete features and target-conditional terminal premises required; truncated probes price only truncated trees |
| [H-347](../hypotheses/H-347-n17-exact-conversion-allowances.md) | the conversion allowances $E_j$ for all 45 coordinates compute exactly and are below one tenth of the $1/1216$ vector’s $r_j$ | the allowances are linear in the root-box width and the frame offset | any $E_j \ge r_j/10$ | the terminal target the capture receipt must actually deliver | part of the composition’s receipt format |
| [H-348](../hypotheses/H-348-n17-second-local-theorem-checker.md) | an independent checker replays fixed certificate data for the two uniform-radius and two distinct anisotropic cases and refuses 20 doctored certificates | exact rational linear algebra and whole-cell quadratic residual bounds | a disagreement or an accepted mutant | the local half rests on two implementations | bind each actual vector and slider box; generating fresh duals is not fixed-data replay, and vertex-only product checks are insufficient |
| [H-349](../hypotheses/H-349-n17-flagged-class-kernel-closure.md) | at least 80 % of the 34 flagged, uncertified selector classes on no contributor roster close under `check_n17_subpattern` mode A with adaptive rows within 30 minutes each | the engine that closed every arity-8/9 flag it was given this week | fewer than 28 of 34 | the kernel’s stall fraction on flags no contributor has run, and at most about 200 orbits net of everything reported | the other 35 of the 69 are H-341’s, H-342’s or H-332’s targets, or row 5; the net is counted at each admission, not assumed |

Corrections applied to existing files: H-337 reads as open (the instrument exists;
`instrument_ready` was false on a stale premise); H-330 carries a note that its
threshold is predicted refuted by its own slopes unless $m \lesssim 5\times10^{-4}$ and
should be re-scoped with $m$ as the variable before any round; H-261 carries a note that
the exchanged witness is a relabelled family member and the claim is not refuted.

## Evidence Status and Limits

The original W3 survey registered no round, replayed no admitted certificate and changed
no bound, verdict, count or frontier field.
Its computations marked *(review)* were run on 9 October from a read-only worktree at
`6a0499ba4` with the project interpreter; those original scripts and outputs were
retained beside the reviews outside the repository.
They are review evidence, not registered rounds.
The review-C revision retains a maintained checker and report for the restricted
family-cell deduction, including root and capacity-one-cover checks; this changes no
global admission or capture verdict.
The original census and GitHub snapshot stays pinned to the dates and revision above.

| Kind | Items |
| --- | --- |
| Computed in the reviews, exact rationals | the four real roots and the isolation of $S^\ast$ to $6\times10^{-44}$; $U - S^\ast$, $V - S^\ast$, $\sigma$, the first-order radii; the RF-7 obstruction arithmetic; the rational witness (own SAT); the family’s 21 contacts and 15 anchors and the 5/6 exchange identity; the cover’s convexity, $D_4$ invariance, Burnside and brute-force orbit counts, inclusion–exclusion area; the ledger residue, marginals and distance partition; the #472, #413 and #358 projections and the contributor-figure reproductions; the exact slack witnesses ($\ge 1.0305$) for all 95 distance-2 states and the endpoint; the $-\omega_{11}$ dual mass 1,421 |
| Replayed in the reviews from `main` with the repository’s unchanged instruments | exp-244 and exp-248 run-002 (10 s each); the $1/1216$ and capture-form compositions; the slide coverage at $9/2048$; the uniform floors; X-051’s 96 centre survivors (40 s) |
| Added after mathematical review C, exact scoped deduction | [restricted family-cell audit](../../../docs/project/research/research-2026-10-09-n17-family-cell-audit.md): root enclosure, occupied-cell membership, capacity one and eleven incircle-distance bounds, using shared endpoint/cover routines; exact sixteen-square core and the stated smaller slider box only, not an independent implementation or global exclusion |
| Numeric, in the reviews | the wall-lemma attack (600 Nelder–Mead starts per cell); the max-min centre-distance optima before exact rounding; the orientation-coupling bounds |
| Derived by hand in the reviews | the curvature bound, the ratio argument, Lemma 1/2 logic, the Kantorovich remark, the no-man’s-land table from the record’s slopes, the gap factors, the characterisation of the diagnosed stalls |
| Computed in this report | the census tool on this worktree (60 / 36,768 / 4,683, 6.3 s; 69 classes with `in_ledger: null`); `git merge-base --is-ancestor 917163641 HEAD`; the verifier blobs by `git ls-tree`; the commit list since `f0ec5b6` |
| Read from the record and GitHub | every other count, verdict, cost, PR and issue state (16:30–17:20 UTC, 9 October; the later GitHub facts dated in the text come from the W2 review’s reads, 17:30–18:15 UTC) |
| Derived here, needing review | the two-gap framing; the sufficient-route statement; the ranking, the lanes and the critical path; the stop list |
| Not done by this survey | any registered experiment; any admitted-certificate replay; any network sweep of external repositories (`make intake` was not run); any change to the explainer or frontier register |

Limits. The #472 projections are containment projections of masks the contributor named;
they become census facts only after the admission round.
The tail characterisation rests on two diagnosed states; of the other 93 surviving
distance-2 orbits, u1 has one incomplete run and 92 have none.
Agent-hour costs are estimates from this week’s receipts, which are lower bounds.
The lanes assume the hosting decision is taken; without it lane E cannot start and every
admission in lanes A and B remains a receipt.

**W2 review.**
[Factual review A](https://github.com/jlevy/squares/pull/475#pullrequestreview-5473799813)
(9 October, reads from 17:30 to 18:15 UTC against this report’s first version and `main`
at `6a0499ba4`) confirmed the numbers above except the following, which this version
corrects:

- **Hard tail** (the lead, §1, §2.5, C4, H-343, ideas.md): u8 closed and was admitted as
  `s182-bc428-u8`, so it is not one of the 95. Per-state runs reach three of the 95 (u1
  incomplete; m1964767 and m851903 at fixed points), none has closed, and the adaptive
  recipe has run on one of them.
  The 22 excluded distance-2 orbits are 11 by W7, 10 by `s182-bc425-t1` and 1 by u8’s
  own certificate.
- **H-349** is re-scoped to the 34 flagged classes on no contributor roster, at most
  about 200 net orbits; 35 of the 69 are H-341, H-342 or H-332 targets or row 5, so
  directions 1 and 9 are not additive ([5.1](#51-ranked)). H-342’s eligible set is 24
  rows, listed once each, worth up to 1,283 orbits rather than about 1,000.
- **Capture distance** (§1, §2.8) is restated on half-widths, 35 to 3,900; “90 to 4,800”
  divided full cell widths by radii and missed the table’s own 70.
- **H-330** (§2.8, C3, H-330’s notes): at most two exceptions needs
  $m \lesssim 5\times10^{-4}$, not $10^{-3}$.
- **Row cap** (§2.5, direction 2, H-343): SW9’s recipe caps rows at 1,152; 2,304 is a
  raised cap whose one run ended INCOMPLETE at 12,000 s. H-343’s worst case is 308
  CPU-hours plus verification, its confirm rule now carries the draw conjunct, and its
  prerequisites include H-341.
- **Verifier blobs** (§2.4, §2.7): the BB listings are `4224262c7` and `f1e2268d6`;
  `651c2615c` is a kernel blob; `9dcc05bc…` is the SHA-256 of blob `c69f1ec08`. The
  ledger has eight listings across seven commits, and the bar on `main`’s unlisted
  verifier is the review rule, not a census refusal.
- **Sessions 184 to 186** (§2.5, §5.4): exp-303, 304, 308 and 312 ran on all 95; the
  owner-0-guard misses are eleven, not fifteen.
- **Centre relaxation** (§2.6): the exact worst is mask 3079037; 3062655 is the float
  worst.
- **Evidence labels** lowered: the fifteen-square deletion-search candidate (float; no
  certified infeasibility or minimum arity), the pairwise claim on the diagnosed states
  (sampled support), the factor of three (a heuristic ratio), and PR 410’s
  seven-certificate parity (reported).
- **Dated GitHub facts**: C8 and C12 were applied to #405 at 17:12 UTC; #472 was
  labelled `n-17` at 17:12 UTC; #413 was edited at 17:04 UTC (2 + 2 + 21 + 11 + 2); the
  explainer’s stale counts are also at lines 59 and 441.
- **§4** records the state-induced labelling convention and centred-cap support in the
  surveyed snapshot. The subsequent mathematical review replaces the unnecessary $m_K>U'$
  premise with $m_K>S^\ast$ and certified per-entry caps.

**Mathematical review C, 9 October.** The revised plan retains affine variation and
root-to-terminal localization in H-346; treats capped runs and Knuth estimates as
bounded evidence; scopes the centre-model stop rule; distinguishes both anisotropic
receipts; and states the correct branchwise dual and slide-box inclusion obligations.
Inherited H-327/H-329/H-340 wording is corrected in this PR; the instruments must carry
those obligations through.
Capture leaves use $P\cap L\subseteq T$ for target packings normalized in $C(S^\ast)$
inside the outer $U'$ search.
The restricted family-cell audit and §5.5’s candidates add no global exclusion or
capture. The review’s fresh local-recipe runs corroborate the retained ratios, with
last-digit differences around $10^{-12}$, but generated new proposals followed by
internal replay; H-348 must replay fixed certificate data independently.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
