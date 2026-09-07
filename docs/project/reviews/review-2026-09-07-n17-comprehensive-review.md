---
title: Comprehensive Review of the n = 17 Record
description: A full audit of everything the repository holds about seventeen unit squares in a square, checked against the live sources on 7 September 2026 and, in a second pass, against three GitHub certificate repositories the first search missed; the repository's own bound stands but its novelty claim did not, with the Burns series reconciled, the stale bookkeeping named, and the lanes where the case can still move ranked by what they would cost and prove.
author: Claude Code
---
# Research: Comprehensive Review of the n = 17 Record

**Date:** 2026-09-07 (last updated 2026-09-07)

**Author:** Claude Code

**Status:** Complete

## Overview

This review asked three questions of the `n = 17` case.
Is the record current against the public sources?
Is everything the repository has done at `n = 17` captured, consistent, and closed out?
And, with `s(11)` having moved from `3.788854` to `3.81` this month, where can `s(17)`
still move?

Four read-only audits fed it, one each on the lower-bound lane, the upper-bound and
structure lane, the campaign and tracker records, and the live web.
The Burns-series reconciliation that prompted the review is applied in the same pull
request and is summarised in its own section below.

**Verdict.** The mathematics on record is current and sound: `s(17) ≥ 459/100 = 4.59`
(`T-019`, `V4/C4`) stands as the strongest bound found anywhere, published or not, and
Bidwell’s `4.67553009360455` is still the best known packing everywhere it is listed.
The currency check below has a hole, though: its corpus is arXiv, Crossref, OpenAlex,
Zenodo and the known authors’ sites, and it has never searched GitHub, where three
certificate repositories had been public since August, one of them past Massaccesi’s
`4.5058` nineteen days before `T-019` was registered.
None of the three reaches `4.59`, so the bound is not what needs correcting; `T-019`’s
novelty claim is, and the correction is applied in this pull request (see “Three GitHub
certificate repositories” below).
What is stale is the bookkeeping, and what is missing is on the upper side.
The case has never had an upper-bound result of its own: its verified ceiling is the
trivial `5`, `0.3245` above the packing, while the machinery that certified `s(29)`'s
packing by a Krawczyk enclosure has never been pointed at `n = 17`, which by the
repository’s own count is the cheapest unpromoted oblique case.
That, not another lower-bound rung, is where the largest formal movement at `n = 17` is.

## Currency against the sources

Checked live on 7 September 2026 against the holdings in
[`n-017.md`](../../../packing/frontier/n-017.md) and the
[5 September refresh](../../../packing/resources/web/literature-refresh-2026-09-05/README.md).

| Source | What it says for `n = 17` today | Against the record |
| --- | --- | --- |
| Kingbird catalogue | `4.67553009360455`, Bidwell 1998, “based on packing found by Pertti Hämäläinen in 1980”; the degree-18 polynomial byte-identical to the stored one | Same |
| Kingbird comparison page | Same polynomial; the live URL carries a double underscore (`squares_in_squares__compared.html`) | Same; URL corrected |
| Friedman’s `packing/squinsqu/` page | Retired to a one-line note handing the table to Kingbird | Page-shape change; no data |
| Friedman’s DS7 survey page | Green’s `(40√2 + 19)/17 ≈ 4.4452` and Bidwell’s `≈ 4.6756`; nothing from 2026 | Same |
| Massaccesi’s blog | No post after 21 August; the `n = 17` post now carries an edit note correcting its grid side from `3.9545` to `2.9545`, the transposition the archive README had already recorded; the bound `4.5058(?)` is unchanged | Text edit only; the refresh’s “article body unchanged” line predates it |
| Sam Burns’s site | Nothing on packing after 6 August | Same |
| Zenodo | Two records for “17 unit squares”, both Brandwijk’s of 18 July; `21422426` is still the last version | Same |
| arXiv | Rate-limited on every direct query; a web search found only the asymptotic papers already retained | Unreachable; no signal |
| UnitSquare | Release 1 only | Same |
| Wikipedia | Table ends at `n = 16`; prose gives Bidwell at `≈ 4.6756` | Consistent |

The live check reported the Massaccesi edit as dated 9 September 2026, two days after
the check itself; it is recorded here as found.

The live check’s corpus is arXiv, Crossref, OpenAlex, Zenodo and the known authors’
sites; it has never searched GitHub.
GitHub held three certificate repositories the check never saw: Mira’s exact
sixteen-point certificates (github.com/Mira-acc/17squares), Stanislav Fort’s exact
sixteen-point certificate (github.com/stanislavfort/17squares), and anabologyco-maker’s
weighted fractional certificate (github.com/anabologyco-maker/square17-lower-bound), all
public since August 2026. They are addressed below in “Three GitHub certificate
repositories.”

No numerical claim at `n = 17` has changed at any source the refresh indexes since the 5
September refresh; GitHub, which the refresh does not index, held values it never saw.

## The lower-bound lane

The bound is `s(17) ≥ 459/100`, from a 1184-atom weighted fractional unavoidable-set
certificate at `B = 9977/10000` on the 181-direction net, total mass `423327/25000`,
least covered mass `200009/200000`, decided by the exact event-cell sweep and by the
interval branch and bound on the doubled net, which agree on that least value to the
digit. Two rungs are retained below it, `451/100` and `229/50`, and two superseded
results are kept for provenance: Massaccesi’s `22529/5000` (`T-015`, `C3`) and the
sixteen-point `4426213/1000000` (`T-001`).

What the record itself names as outstanding:

- **No `C5` review artifact exists for `T-019`**, and none for `T-001`; `T-015`’s
  method-distinct `C4` is moot now that `T-019` holds `C4` at a larger side.
- **The covering-value rows for `n = 17` have no raw run.** Both rows in
  `covering-values.yaml` carry `site_set: unrecorded` and null site, row and round
  counts. The `4.58` row is “converged per X-013” with no stop reason; the `4.59` row is
  `converged: false`, “Not recorded”, so its objective `16.9303` stands as an upper
  bound only. Nothing was ever attempted above `459/100` at `n = 17`.
- **Two defects stay open**: `D-423` (the green17 Lemma 4 boundary, non-strict in two
  sources and strict in a third) and `D-428` (the `n = 17` successor validator never
  ties the rebuilt chain spine to the carried boundary).
- **The `n = 18` probe at `117/25` is unresolved**: three site sets returned a
  restricted optimum of exactly `18.000000` and the run stopped on cost, leaving “the
  covering value is at least 18” and “the optimum sits on a degenerate vertex”
  unseparated.

The headroom, and a discrepancy in how it is stated:

| Quantity | Value | Where |
| --- | --- | --- |
| Runway to the method ceiling `5B = 4.9885` | `0.3985` | `RESULTS.md`, `SYNOPSIS.md`, `n-017.md` |
| Runway to the packing-side cap `4.6710` (X-014) | `0.0810` | `CERTIFICATE-REACH.md` row 17 |
| Gap to the best known packing | `0.0855` | `n-017.md` |
| Mass margin of the `4.59` rung | `0.066920` | `RESULTS.md` |
| Mass margin of the `4.58` and `4.51` rungs | `0.034265`, `0.406380` | `RESULTS.md` |

The three prose statements quote the structural runway and never the cap, which is a
factor of five smaller; the reach table itself lists `limited by` as `cap` in two places
and `packing` in a third, and its attainment ratio `0.98171` divides by the packing.
Margin is not monotone in the side, which the record already says: a better site set at
a higher side can reopen it.
The record’s standing judgement is that a further rung is not worth spending at `n = 17`
because a larger `n` is strictly easier at the same side, and nothing found here
overturns that. What it does add is that the `4.59` run’s convergence is simply not
known, so whether `4.59` is a wall or a stopping point is an open measurement, not a
settled one.

## The upper-bound and structure lane

The best known packing is held as a catalogue report and nothing more.
Its source asset, Ellsworth’s `square-17.svg`, is deliberately not retained
(`known-best-packings/sources.json`: no express reuse terms found), so the witness
`W-known-best-n017` carries centres and angles transcribed to between 32 and 100 digits,
a tolerance-bounded feasibility receipt at `1e-8`, and the degree-18 minimal polynomial,
whose root lies within `9.52e-16` of the catalogue side.
The Gensane–Ryckelynck decimal that disagrees from the ninth digit is resolved in the
catalogue’s favour by that evaluation; whether the paper’s decimal is a slip is still
open on the source side.
The only verified upper-bound evidence is the grid, `5`.

The rigidity screen finds the retained configuration not rigid: two of seventeen squares
admit a feasible translation of about `0.0715`. The record draws no consequence for
improvability, and rightly, since the screen is sound in one direction only and the
coordinates are a finite-precision transcription.

The machinery for a formal ceiling exists and has never been aimed here:

- `T-009` certified `s(29)`'s packing by a Krawczyk enclosure at relaxation `1e-20`,
  through `sqpack.promote`; the witness schema admits an interval-enclosure scalar with
  `krawczyk` and `interval-newton` operators today.
- `X-004` counted the unknowns left after eliminating centres: six at `n = 29`, two at
  `n = 11`, **three at `n = 17`**. By that measure `n = 17` is the cheapest oblique case
  not yet promoted, and the integer-relation route is open too, since the minimal
  polynomial is published.
- The contact-structure atlas holds only `n = 11` and `n = 29`; `n = 17` appears only as
  a calibration chunk (three angle classes, three contact components, eleven contact
  edges, five free squares) with its narrow partition not established.

No result, hypothesis, agenda or bead has ever targeted an `n = 17` upper bound.
The one search hypothesis, `H-020`, was refuted as designed: the annealer returned the
`5 × 5` grid on every seed, and which component failed is still open.

## The Burns series, reconciled

The reconciliation is applied alongside this review; the details are in the
[addendum packet](../../../packing/resources/web/burns-n17-series-addendum-2026-09-07/README.md).

- Burns’s lower-bound post, proof note and verifier were already archived byte for byte;
  the live copies are identical.
  His introduction post, the coordinates file behind his near-record arrangement, its
  five figures and the two post images were not, and now are.
- His own 268-atom certificate had never been replayed here, only Massaccesi’s derived
  copy. It replays unchanged (`E-n017-burns-source-replay`), and re-encoded in the
  repository’s schema it is accepted by the exact sweep at least mass `10003/10000`
  (`E-n017-burns-control-decision`). It is retained as the control the campaign named
  three times and never built: a published control whose least covered mass is not `1`.
- The interval route does not decide that control, and the reason is worth keeping.
  Burns’s grid places a column at exactly `1/2 + (L - 1)/7 = B`, so a centre on the
  domain boundary has an atom column exactly on its far edge; closed membership counts
  it in the sweep, while no outward-rounded enclosure can close a region edge that lies
  on the domain edge, and the search returns the seam as undecided.
  A refusal, not an acceptance, and confined to direction `0`; Massaccesi’s grid has a
  margin and is decided whole.
- His near-record arrangement is checked as data: eleven axis-aligned squares and six at
  `39.6319°`, side `4.677648294965133`, a root of his quintic, `0.002118` above Bidwell.
  The contact graph is not reconstructed; `think-t5va` holds that.
- The `[Burns–Massaccesi n17]` resource is now named on the `n = 17`, `18` and `19` case
  files, as `BC-151` deferred.
  The reported lane stays at Nagamochi, following the precedent that kept Green’s survey
  value out of it; whether the lane should mean best-in-print or best-replayed is
  `think-ss2a`’s decision and is not made here.

## Three GitHub certificate repositories

The currency check’s corpus never included GitHub.
It should have: three certificate repositories for `s(17)` were public there before this
review was written, and one of them held a public bound above Massaccesi’s for nineteen
days before `T-019` was registered.
The user found all three on 7 September 2026; they are cloned under `attic/`, archived
under
[`packing/resources/web/n17-github-certificates-2026/`](../../../packing/resources/web/n17-github-certificates-2026/)
with replay scripts, and carried in `frontier/evidence.yaml` under source key
`[GitHub n17 certificates 2026]`.

| Date | Author | Value | Type | Status here |
| --- | --- | --- | --- | --- |
| 18 Jul 2026 | Brandwijk | `89/20 = 4.45` | Exact, 16 points | Already tracked (Zenodo record `21422426`), unchanged |
| 6 Aug 2026 | Burns | `4.4811` | Weighted | Replayed and verified (`E-n017-burns-source-replay`) |
| 10 Aug 2026 | Mira | `4.450837` | Exact, 16 points | Superseded by the same repository’s 11 Aug commit; not independently replayed |
| 11 Aug 2026 | Fort | `4.456575` | Exact, 16 points | Replayed here, valid (`E-n017-fort-point-certificate-replay`) |
| 11 Aug 2026 | Mira | `4.468292` | Exact, 16 points | Replayed here, valid (`E-n017-mira-point-certificate-replay`) |
| 13 Aug 2026 | anabologyco | `4.57` | Weighted, exact-orientation | Superseded by the same repository’s v0.2.0 |
| 16 Aug 2026 | anabologyco | `9141/2000 = 4.5705` | Weighted, exact-orientation | Source-backed only; not decidable here (`E-n017-anabologyco-weighted-certificate`) |
| 21 Aug 2026 | Massaccesi | `22529/5000 = 4.5058` | Weighted | Retained (`T-015`, `C3`) |
| 4 Sep 2026 | This repository | `459/100 = 4.59` | Weighted | Current bound (`T-019`, `V4/C4`) |

The three exact sixteen-point certificates, Mira’s two and Fort’s, are the strongest
integral (unweighted) bounds on record, above both Brandwijk’s and this repository’s own
green17 `4.426213`.

**Mira** (`github.com/Mira-acc/17squares`) posted an exact sixteen-point
strictly-unavoidable-point certificate for `s(17) > 4.450837` on 10 August 2026, then a
second on 11 August for `s(17) > 4.468292`, adding strict triangle-piercing leaves: a
strict form of the classical triangle lemma, that a unit square whose centre lies
strictly inside a triangle with all sides shorter than 1 contains a vertex in its
interior. The later certificate is a 122,626,747-node exact pose-space subdivision with
`t = tan(theta)` ranging over `[-1, 1]`, one byte per node, exact integer comparisons,
three independent checkers (a fast C++ one, a Boost bigint C++ one, and a pure-Python
integer one), and a LaTeX paper and PDF. Replayed here with the pure-Python checker:
valid over all 122,626,747 nodes in 3 min 34 s, and both published hashes matched
(`E-n017-mira-point-certificate-replay`); the two C++ checkers were not run, Boost being
absent from the container.
The repository is credited to a language model (GPT-5.6 Pro) working under human
direction and is not peer reviewed; it cites Friedman, Stromquist, Ellsworth and Fort,
and not Brandwijk, Burns or Massaccesi.
The first, 10 August certificate was not extracted from the archive and was not
independently replayed; it is superseded within the same repository by the second.

**Stanislav Fort** (`github.com/stanislavfort/17squares`) posted `s(17) > 4.456575` on
11 August 2026 on the same architecture as Mira’s, without the triangle-piercing leaves:
a 21,696,657-node exact subdivision over a different set of sixteen rational points.
The author’s README states the work was done by a language model (GPT-5.6-Sol) and that
he cannot vouch for it; a GitHub Action runs the checkers on every push.
Replayed here with the pure-Python checker: valid in 20 s
(`E-n017-fort-point-certificate-replay`); the two C++ checkers, which need Boost, were
not run.

**anabologyco-maker** (`github.com/anabologyco-maker/square17-lower-bound`) posted a
weighted fractional unavoidable-set certificate between 13 and 17 August 2026: 71 D4
orbits expanded to 560 atoms on the 1/4000 grid, total mass `16.994734834452`, claiming
`s(17) >= 9141/2000 = 4.5705` (tag v0.2.0, 16 August; v0.1.1 of 13 August claimed
`4.57`). Its verifier is architecturally unlike this repository’s: no shrunken square
and no direction net.
Instead it decides an exact orientation partition: 1,344,862 event polynomials, an exact
Bernstein prefilter discarding 1,194,331 of them, Sturm chains on the remaining 150,531
giving 148,937 open orientation cells, one exact rational `t = tan(theta/2)` audited per
cell, 278,950,150 subthreshold runs all proved outside the feasible region, and endpoint
audits at `theta = 0` and `theta = pi/4`. A Lean 4 layer carries `native_decide`
theorems over the finite checks, including all 148,937 cells, in an 8.5-hour build; the
event-completeness layer and the measure argument are not formalised.
Its README states the certificate was built with GPT-5.6 Sol Pro and audited and
formalised by “Claude Fable 5 (Anthropic)”, with peer review pending.
Replayed here only in part (`E-n017-anabologyco-weighted-certificate`): its `SHA256SUMS`
verified over all 76 entries, and its certificate-arithmetic and Bernstein-filter Python
stages both pass; the Sturm, endpoint and coverage stages need `g++` with
Boost.Multiprecision, absent from the container and not installed at the user’s
decision, and Lean is absent too.
This repository’s own verifier cannot decide it either: the 560 atoms re-encoded into
`sqpack.fractional` at side `9141/2000` with the 181-direction net are refused at least
cell mass about `0.0245` at direction `0`, because the source places atoms exactly one
unit from the container walls, which a wall-touching closed unit square captures on its
boundary and which this repository’s shrunken square cannot reach at all.
That refusal is an artefact of the reduction, not evidence against the source.

What is new for this record, against what stood before today: the strongest integral
sixteen-point certificates are now Mira’s and Fort’s, and the strict triangle-piercing
leaf is a certificate ingredient this repository’s own sixteen-point work does not use.
anabologyco’s exact-orientation weighted verifier, with no shrink and a Lean 4 layer,
provides a source-reported formalization of the finite-check layer toward the
proof-assistant-checked (`V5`) direction named for `T-015` and `T-019`. It is not a
formalized `s(17)` theorem: event completeness and the measure argument remain outside
Lean, and the Lean build has not been replayed here.
`T-019`’s novelty claim and movement figure need the correction recorded as item 10 in
Bookkeeping below. Burns, Mira, Fort and anabologyco disclose model assistance and state
that their results have not undergone independent peer review.
Fort additionally says he cannot personally vouch for correctness.

What this repository’s tools can and cannot do with them: the shrink in
`sqpack.fractional`’s reduction is why its own verifier refuses anabologyco’s
certificate, an artefact of the reduction rather than a finding against the source, and
nothing here re-derives the certificate under an unshrunk verifier.
The two exact sixteen-point certificates, Mira’s and Fort’s, are candidates for a
genuinely independent decision: this repository’s green17 interval audit takes an
arbitrary side through its `--side` flag and an arbitrary point set through the `points`
argument of its audit function, and could re-decide either one as a second
implementation distinct from all three of Mira’s own checkers; that re-decision was not
run today.

Worth citing, worth learning from, and where each now lives in this record:

- **Cited.** All three repositories are named on the `n = 17`, `18` and `19` case files
  and in three evidence entries under the source key `[GitHub n17 certificates 2026]`;
  the root README’s `T-019` entry now credits every 2026 bound that came close, with its
  author and date; the proof-strategy catalogue cites them at entries 18
  (machine-checked proof, now `adjacent` on the strength of anabologyco’s Lean layer),
  21 (the strict triangle-piercing leaf and the exact pose-space subdivision format) and
  22 (the exact orientation partition as a second way to decide a weighted measure); and
  the search-strategy catalogue’s entry 16 records Burns’s learned search and its
  near-record basin.
- **Learned.** Four ideas are portable: Mira’s strict triangle-piercing leaf, an
  orientation-free discharge for integral certificates; the one-byte-per-node exact
  subdivision certificate with pure-integer checkers, a format small enough to hand to a
  proof assistant; anabologyco’s exact orientation partition, which needs no shrunken
  square, so it has no containment loss and no `5B` ceiling and can place atoms on the
  wall lines; and the operational habits around them, Fort’s checker run on every push
  by a GitHub Action, Mira’s byte-identical regeneration of the tree from a
  deterministic generator, and anabologyco’s process-isolated coverage ranges.
- **Not adopted, and why.** None of the three changes a bound here.
  What they change is the target list: an unshrunk exact-orientation verifier would be a
  third decision procedure for the retained certificates and the only route to deciding
  the `4.5705` atoms here; a Lean layer over `T-019`’s finite checks is now a
  demonstrated shape rather than a hope; and the two sixteen-point certificates are the
  natural first inputs to a green17-audit re-decision.
  Each is a bead, none was run today.

## Bookkeeping

The tracker is behind the record.
Beads whose work is done and narrated in the ledger but never closed: `think-a0h6`,
`think-5j8d`, `think-sapq` (`BC-147` to `BC-149`, the `H-052` completion), `think-6q88`,
`think-bagn`, `think-xycf` (`BC-150`, `BC-151`, `BC-155`, the `4.5058` adoption that
`T-019` displaced a day later), and `think-iye2` (the green17 exact ceiling, which
`X-015` already calls retired).
Recommendations never picked up: `X-015`’s call to re-scope or close `BC-115`
(`think-w8hh`), which the Burns control now partly answers, since it is the second
consumer that bead wanted; `H-027`, `H-028` and `H-045` registered against `n = 17` on
23 August with zero rounds; and `think-d4hm`, the angle-compressibility pilot on the
`n = 17` witness. Blocked on a decision rather than on work: `think-ss2a`.

Inconsistencies found across documents, for the record:

1. `CERTIFICATE-REACH.md` names `n = 17`’s limit `cap` in two tables and `packing` in a
   third, and its ratio uses the packing.
2. The `0.3985` runway is quoted three times without the `0.0810` cap that supersedes
   it.
3. `n-017.md`’s case-level evidence list omits the two entries that support its own
   verified bound; `n-018` and `n-019` follow the same pattern for theirs.
4. The `4.58` row’s convergence rests on `X-013` alone, which itself hedges.
5. The `s(11)` research report still carries “reconcile the two published values for
   `s(17)`” as an open item and says they agree to nine decimals; they agree to eight
   and the reconciliation is done.
6. The frontmatter tilt `-36.6238°` and the witness’s `+53.3762°` are the same angle
   modulo `90°`, and no document says so.
7. `E-translation-escape-not-rigid` lists 89 cases in scope against the 84 its own text
   counts, including three screened rigid and two it says are excluded.
8. The witness receipt reports a pair gap of `0.0` where the screen reports `-7.4e-34`
   for the same configuration.
9. The refresh packet’s “Massaccesi’s article body is unchanged” is now stale.
10. `T-019`’s claim, its significance rationale and its novelty basis quote `4.5058` as
    the best prior public value and `0.0842` as the movement past it, where `4.5705` and
    `0.0195` are the facts; corrected in this pull request.
11. The literature-refresh method’s corpus has no code-hosting sites.

## Where `n = 17` can still move

Ranked by what a result would prove against what it would cost, with the `s(11)` lesson
in mind: the ladder there moved because the generator, the two verifiers and the review
artifacts were built first, and the case then paid for itself.

1. **A formal ceiling for Bidwell’s packing.** The largest movement available at
   `n = 17` is `0.3245`, from `5` to the enclosed side, and it is an upper-bound
   promotion of the kind `T-009` already made at `n = 29` with twice the unknowns.
   The inputs are in hand: the witness coordinates, the angle classes, the published
   polynomial as a cross-check.
   What is missing is the contact graph, which the calibration chunk sketches but the
   atlas does not hold, and a decision on whether to reconstruct Ellsworth’s geometry
   from the retained digits rather than from the unretained SVG. This is the one lane
   where nothing structural stands in the way.
2. **Recover the `4.59` run’s stop reason, or run it again recorded.** This resolves the
   run’s stopping state; a converged restricted optimum describes only the tested sites.
   A converged column-generation run with a retained site set, row and round counts and
   a log, seeded with the retained atoms as at `n = 20`, could find a further rung
   inside the `0.0810` the cap allows or record a bounded negative for the tested sites.
   Either outcome is worth more than the present “not recorded”.
3. **Reconstruct the Burns basin** (`think-t5va`). The coordinates are retained and
   checked, the exact side is a root of a known quintic, and a second competitive
   topology at `n = 17` would be the first evidence on record that the landscape has
   more than one basin, which is what `H-020`’s calibration lane needs.
4. **Write `T-019`’s `C5` artifact.** The current bound is the only `S4` result at
   `n = 17` and its review-readiness is the last assurance step it lacks.
5. **Replay the two strongest external results independently.** anabologyco’s decisive
   stages (the Sturm partition, the endpoint audits, the coverage audit) need `g++` with
   Boost, absent from the container and not installed at the user’s decision, and Lean,
   also absent; replaying them, and re-deciding Mira’s sixteen points with this
   repository’s own green17 interval audit through its `--side` and `--points`
   arguments, an implementation distinct from all three of Mira’s own checkers, would
   put the two strongest external results at `n = 17` on this repository’s own footing
   rather than the source’s. anabologyco’s exact-orientation approach carries neither
   this repository’s shrink loss nor its `5B` ceiling; the current shrink/net
   packing-side cap does not apply unchanged to that method.
6. **Close the tracker**: the seven finished beads, `BC-115`’s re-scope, and the
   `think-ss2a` decision, each of which is a disposition rather than work.

What this review does not do: it does not change a bound, it does not reconstruct the
contact graph, and it does not decide the reported-lane rule.
For the current fixed-`B`, fixed-net certificate family, the packing-side cap leaves
`0.0810` of possible movement and rules out closing the case at Bidwell’s side.
That cap does not apply unchanged to the proposed unshrunk exact-orientation method.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
