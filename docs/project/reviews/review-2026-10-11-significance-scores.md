# Significance Scores Wrapped Up: The 48 Drafts Confirmed, Three Scores Changed, and the Working Rules Collected

**Verdict: every draft significance score in the register as it stood on 11 October,
`T-001` to `T-146`, is now confirmed or changed by a review, and the five pairs the
process review of 1 October left unexplained are resolved by the three rules of
`epistemics.md`.** Forty-eight entries carried a score set by the lane that registered
them, from `T-037` to `T-055` (session 161), through the issue intakes `T-056`, `T-057`
and `T-061`, the tools and source intakes `T-058`, `T-059` and `T-064`, the registering
lanes of 1 to 3 October (`T-065`, `T-068`, `T-070`, `T-073` to `T-079`, `T-081`,
`T-087`), and the import lanes of 7 and 8 October (`T-117` to `T-127`). Each was
compared with the entries nearest it, by kind, count and technique; 46 keep their score
and two change (`T-053`, `S4` to `S3`; `T-065`, `S3` to `S2`). The process review’s pair
of `T-063` against `T-016` is settled by moving `T-063` from `S1` to `S3` beside `T-002`
and `T-016`; the 2 October review of $s(60)$ had confirmed `T-063` at `S1` and left only
`T-053` against `T-062` to this pass.
A consistency pass over all 146 entries found no other pair whose difference the
rationales do not explain, and lists the explanations.
The working rules that scorers have been citing from inside rationale fields are
collected below as one proposed paragraph for `epistemics.md`; this review does not edit
that file.

This is lane S of the 2026-10-11 intake pass (bead `think-qh3s`), written on 2026-10-11
by an AI agent (Claude, at extra-high reasoning effort), prompted separately from the
registering lanes and from the 11 October final reviews, with no shared context.
It registers nothing, moves no bound and changes no rung.
A significance score guides reading order and never changes validation behaviour.

## Scope and Evidence

**Rules applied.** The three rules of
[`epistemics.md` → Significance and Novelty](../../../epistemics.md#significance-and-novelty):
the score is of the claim, what the result establishes if it is correct; the registering
lane drafts and the reviewing lane confirms, and `by` then names the review; a score
follows the claim, not the frontier, so a later result that supersedes an entry does not
lower it. The anchors `S1` to `S5` are read as written: bookkeeping or a routine
consequence; a citable detail that changes no theorem; a substantive case result or
machine audit; a reusable technique, bound family or resolved disputed value; movement
on a central open case.

**Read in full.** Every `significance` block of `T-001` to `T-146` at the branch head
before this pass, dumped to one table by a script written for this review (id, kind,
scope, score, `scored`, `by`, rationale, credit, novelty, supersession).
The claims, compositions, notes and `next_rung` of the entries under review and of their
comparators (`T-011`, `T-016`, `T-022`, `T-044`, `T-046`, `T-056`, `T-057`, `T-058`,
`T-059`, `T-061`, `T-063` to `T-065`, `T-081`, `T-087`, `T-088`, `T-117` to `T-120`,
`T-124` to `T-127`, `T-038`, `T-042`, `T-048`, `T-053`). The significance passages of
the reviews that scored the neighbours: the
[process review of 1 October](review-2026-10-01-result-import-process.md), the
[$s(60)$ geometric-premises review](review-2026-10-02-evand-s60-geometric-premises.md)
(section 8), the [Couzo review of 5 October](review-2026-10-05-couzo-6042c56.md)
(section 12), and the three 11 October final reviews
([lower bounds](review-2026-10-11-final-lower-bounds.md) F1-2,
[upper bounds](review-2026-10-11-final-upper-bounds.md),
[asymptotic and grading](review-2026-10-11-final-asymptotic-and-grading.md)).
`devtools/rung_prose.py` and `devtools/check_rung_figures.py`, which hold a rationale to
the rung rule and to its quoted figures.

**Measured here.** The margins that decide the upper-bound line were read from the case
records’ own side histories, not from the rationales: `T-117` lowers $n = 105$ from
$10.806077865540567$ to $10.80607786551970463\ldots$, about $2.1 \times 10^{-11}$, and
$n = 292$ from $17.597249391199519$ to $17.597249391156465\ldots$, about
$4.3 \times 10^{-11}$; `T-118` lowers $n = 68$ from $8.798795237222592$ to
$8.79879523721828390\ldots$, about $4.3 \times 10^{-12}$; `T-119` lowers $n = 266$ from
$16.82306208283780$ to $16.8230287507564760$, about $3.3 \times 10^{-5}$; `T-125` lowers
$n = 102$ from $10.607174680176051$ to $10.6058286965106059$, about
$1.3 \times 10^{-3}$; `T-126` holds $n = 51$ at $(16 + 5\sqrt{2})/3 = 7.69035593\ldots$,
about $0.0104$ below the $7.70079923541702$ that `T-101` held.
The other margins quoted are the registering entries’ own, or the grading review’s, and
are cited as such.

**Not opened.** No certificate, packet or checker: this review scores claims the record
already holds at the rungs it holds them, and the mathematics behind each rung is the
business of the reviews those entries name.

**Ran**, from `packing/` with the project interpreter: the dump scripts; the rewrite
script, which replaced the 50 `significance` blocks named below and no other byte of
`results.yaml` (`git diff -U0` shows changes only on `score`, `rationale`, `scored` and
`by` lines); `devtools.check_results` (146 results, every structural check passes);
`devtools.validate_schemas`; `devtools.check_rung_figures` (all quoted figures and
fraction-decimal claims agree); `devtools.render_results --update`, which changed the
three rescored rows of `RESULTS.md`; and `packing-validate --records` before and after
the edits.

## The Five Pairs

| Pair | Before | Resolution |
| --- | --- | --- |
| `T-062` ($s(60) = 8$) against `T-051` to `T-053` | S3 against S4 | `T-053` moves to `S3`. The technique’s first instances, `T-051` (the exhaustive zero-margin cover) and `T-052` (line mass on the grid lines), hold `S4` as reusable techniques; `T-053`, `T-062`, `T-066` and `T-067` are single-count instances of the recipe, substantive case results at `S3`; the family $s(k^2 - 4) = k$ is `T-081`’s claim and carries its `S4` there. The draft’s grounds, that the case went from open to solved and that three siblings make a bound family, do not survive the rules: every exact value closes a case, and a bound family in the `S4` sense is one argument at every $k$. |
| `T-061` ($+3.9 \times 10^{-9}$ at $n = 11$) against `T-022` | S2 against S5 | Both kept. Both spend the slack of an existing certificate at the central case, and the difference is what each step changes: `T-022`’s $2.6 \times 10^{-5}$ changed the case’s stated gap and proved the dilation-limit theorem that `T-024`, `T-026` and `T-033` reuse; `T-061` changes no stated digit of the gap and proves nothing new, so it sits with `T-078` and `T-093`, the other slack-spending steps at `S2`. |
| `T-065` (Bidwell’s packing certified) against `T-011` (Trump’s) | S3 against S2 | `T-065` moves to `S2`. Both certify a long-standing reported packing exactly and move no reported bound; `T-098` and `T-101`, exact certificates of 125 catalogue packings that took 75 verified ceilings off the integer grid, are `S2` on the same ground. The draft’s `S3` rested on the verified ceiling leaving the grid, which is a fact about this record’s verification, not about the claim. |
| `T-063` ($s(61) = 8$) against `T-016` | S1 against S3 | `T-063` moves to `S3`. Both are one-line monotone corollaries; the score is of the claim, and `T-063`’s claim settles a case, as `T-002` and `T-016` carry their premises’ `S3` to the counts they move and `T-144` carries five counts at `S3`. The derivation’s triviality is already recorded in `composition` and `next_rung`. The alternative, lowering `T-002` and `T-016` to `S1`, was rejected: their scores are confirmed, their claims moved cases, and the `S1` anchor fits an entry that establishes nothing the record did not hold, as `T-129` does. |
| `T-044`, `T-046`, `T-056` against `T-019`, `T-020` | S3 against S4 | All three kept at `S3`. `T-019` and `T-020` earned `S4` for the first certificates of a new generator displacing published values, and `T-020` itself set further sizes from it at `S3`; ten, 48 or 49 certificates are further sizes, whoever runs the generator. A bound family in the `S4` sense is one argument at every count (`T-064`, `T-081`), not many certificates or packings; `T-056`’s source publishes no method. |

## The Drafts

Three scores change:

| Entry | From | To | Ground |
| --- | --- | --- | --- |
| `T-053`, $s(45) = 7$ | S4 | S3 | the third instance of `T-052`’s technique; one score with `T-062`, `T-066`, `T-067`; the family is `T-081`’s |
| `T-063`, $s(61) = 8$ | S1 | S3 | a corollary scores the claim it states at its own count, as `T-002` and `T-016` do; it settled a case |
| `T-065`, Bidwell’s packing certified | S3 | S2 | an exact certificate of a packing already reported, as `T-011`, `T-098` and `T-101` are |

Forty-six drafts keep their score, each with a rationale that now states the comparison,
`scored: '2026-10-11'` and `by` naming this review:

| Entries | Score kept | Compared with |
| --- | --- | --- |
| `T-037` | S5 | `T-018`, `T-022`, `T-024` to `T-026` (S5, smaller movements at $n = 11$); `T-061` (S2) |
| `T-038`, `T-040`, `T-041`, `T-043` | S3 | `T-032`, `T-015` (the precedent, read as the rubric reads it: a result by others takes the score its claim would take from anyone); `T-047` (S4, the one technique by others whose reuse spans the register); `T-133`, `T-145` (a technique at one count, S3 with the technique noted) |
| `T-039` | S3 | `T-043` (S3, new content at one count); `T-042`, `T-093` (S2, an unchanged charge refined); the two days it held the field do not enter |
| `T-042` | S2 | `T-093`, `T-078` (S2, slack spent); `T-043` (S3); its same-day supersession no longer grounds the score |
| `T-044`, `T-045`, `T-046` | S3 | `T-019`, `T-020` (S4); `T-047` (S4); `T-068`, `T-070`, `T-074` (S3) |
| `T-047` | S4 | `T-017`, `T-051`, `T-052` (S4, the other techniques scored once at their first instance) |
| `T-048` | S3 | `T-073` (S3, another kind within Tokoharu’s framework); `T-047` (S4, the framework) |
| `T-049`, `T-050` | S3 | `T-017` (S4); `T-079`, `T-095`, `T-021`, `T-034` (S3) |
| `T-051`, `T-052` | S4 | `T-053`, `T-062`, `T-066`, `T-067` (S3, instances); `T-064`, `T-081` (S4, families); `T-073` (S3) |
| `T-054`, `T-055` | S2 | each other; `T-066` (S3, a second route at a new count) |
| `T-056`, `T-057` | S3 | `T-092`, `T-113` to `T-116`, `T-135`, `T-136` (S3, new packings); `T-098`, `T-101`, `T-146` (S2); `T-019`, `T-020` (S4) |
| `T-058` | S2 | `T-003` (S2, the other method limit) |
| `T-059` | S2 | `T-004` (S3, a machine audit of a published proof that had none) |
| `T-061` | S2 | `T-022` (S5); `T-078`, `T-093` (S2) |
| `T-064`, `T-081` | S4 | each other; `T-084`, `T-086` (S3, families re-proving values held) |
| `T-068`, `T-070`, `T-073` to `T-077` | S3 | `T-045`, `T-069`, `T-071`, `T-072` (S3, the same certificate kinds at other counts); `T-080` (S3, the replay of `T-073`’s own counts at $n = 101$ to $105$) |
| `T-078` | S2 | `T-061`, `T-093` (S2); `T-079`, `T-095` (S3) |
| `T-079` | S3 | `T-095` (S3); `T-078` (S2) |
| `T-087` | S3 | `T-007`, `T-083` (S3, published general lower bounds registered as floors) |
| `T-117`, `T-118` | S2 | `T-098`, `T-137`, `T-139` (S2, re-solves at the scale of rounding, measured above); `T-127`, `T-128` (S3) |
| `T-119`, `T-125`, `T-126`, `T-127` | S3 | `T-128`, `T-130`, `T-131`, `T-135` (S3, new or re-arranged packings); `T-117`, `T-137` (S2); `T-120` to `T-123` (S2, an exact form alone) |
| `T-120` to `T-123` | S2 | `T-098`, `T-139` (S2); `T-126` (S3, a new arrangement in exact form) |
| `T-124` | S2 | `T-012` to `T-014` (S3, rigidity proved); `T-036`, `T-112` (S3, optimality statements) |

`T-062`’s block is rewritten too, at `S3`, to close the question its 2 October review
left open; it was not a draft.

## The Consistency Pass

Every pair of entries with the same kind of claim and different scores, over `T-001` to
`T-146`, and what explains the difference:

| Pair | Scores | Explained by |
| --- | --- | --- |
| `T-002`, `T-016` against `T-063` | S3, S1 | no longer differ: `T-063` is `S3` |
| `T-064`, `T-081` against `T-084`, `T-086` | S4, S3 | a family that settles open cases against families whose values were already held as proved |
| `T-004` against `T-059` | S3, S2 | a machine audit of a published proof that had none, against a same-implementation replay of row minima of a certificate the record had already decided in full |
| `T-005` against `T-085` | S2, S3 | an erratum changing no theorem, against a lemma’s failure that removed the proof of 287 case floors |
| `T-003`, `T-058` | S2, S2 | consistent: method limits bound nothing about $s(n)$ |
| `T-012` to `T-014` against `T-124` | S3, S2 | rigidity proved at famous cases with new machinery, against reported non-strict local minima under a convention |
| `T-023` against `T-031` | S3, S2 | both case exclusions at $n = 11$ that move no bound, both reviewed, both superseded by `T-060` and keeping their scores; the rationales ground `T-023` in what it showed about a counting argument and `T-031` in a tree that cannot close. The difference is explained only by what each showed about the method; recorded as finding F-4 and not changed |
| `T-033` against `T-024`, `T-026` | S3, S5 | the same mechanism at the same case, but `T-033`’s value was below the public bound when it was established, so it was not movement; its rationale says so |
| `T-019`, `T-020` against `T-021`, `T-027` to `T-030`, `T-034` | S4, S3 | `T-020`’s calibration, applied in each rationale |
| `T-088`, `T-089` against `T-128`, `T-130`, `T-134` | S2, S3 | an optimization of a packing already reported, against packings refined or searched to new optima; `T-088`’s $1.1 \times 10^{-5}$ sits in the magnitude band the grading review gives `S3`, and the line is drawn by kind (finding F-5) |
| `T-098`, `T-101`, `T-117`, `T-118`, `T-137`, `T-139`, `T-146` | S2 | consistent: re-solves, regularizations and precision refinements of credited packings |
| `T-056`, `T-092`, `T-113` to `T-116`, `T-119`, `T-125` to `T-128`, `T-130`, `T-131`, `T-134` to `T-136`, `T-138`, `T-140`, `T-141` | S3 | consistent: new or re-arranged packings moving case ceilings |
| `T-009` against `T-011`, `T-065` | S3, S2 | the first interval certificate for a bound of this kind, against exact validations of reported packings |
| `T-007`, `T-083`, `T-087` | S3 | consistent: published general lower bounds, the score the theorem’s |
| `T-017`, `T-047`, `T-051`, `T-052`, `T-010` | S4 | the techniques scored once at their first instance, and the repair of the flagship case’s proof |
| `T-036` against `T-112` | S3, S3 | consistent |

Where `S3` is kept for a tiny refinement, the rationale now says why: `T-125`’s and
`T-127`’s ranges reach $10^{-7}$ at their smallest counts, but each is a packing moved
to a new optimum, which is the kind the line scores `S3`; `T-117`, `T-118`, `T-137` and
`T-139`, re-solves at the scale of rounding, are `S2`. No `S3` is kept for a re-solve.

Entries scored at registration before the draft rule existed and carrying no draft mark,
`T-021`, `T-027` to `T-030` and `T-034` to `T-036`, were read in the pass and are
consistent with it; their blocks were not rewritten (finding F-2).

## Proposed for `epistemics.md`

The working rules below are applied in rationales from `T-015` on and nowhere stated as
policy. They are offered to the owner as one paragraph under Significance and Novelty;
this review does not add it.

> **How the anchors are applied.** A result by others takes the score its claim would
> take from anyone; the replay and review here are confirmation, not significance.
> A technique is scored once, at its first instance (`T-017`, `T-047`, `T-051`,
> `T-052`); further sizes, rungs or counts from the same generator or certificate kind
> are case results at `S3` unless they bring a new technique, and a technique reused at
> one count is `S3` with the technique noted (`T-133`, `T-145`). A bound family at `S4`
> is one argument at every count (`T-064`, `T-081`), not many certificates; a family
> that re-proves values already held is `S3` (`T-084`, `T-086`). A step that spends an
> existing certificate’s slack, by rescaling, a finer net or catalogue, or rebuilt
> cores, with no new atom, rule or weight, is scored by what it changes: `S2` when the
> case’s stated gap does not change at the precision the record states it (`T-042`,
> `T-061`, `T-078`, `T-093`); a new atom, rule or weight at one count is `S3` (`T-039`,
> `T-043`, `T-079`, `T-095`). Movement on a central open case is `S5` when it changes
> the case’s stated gap (`T-018`, `T-022`, `T-024` to `T-026`, `T-037`). An upper bound
> by a new or re-arranged packing that lowers a case’s best side is `S3`; an exact
> re-solve, regularization, precision refinement or exact closed form of a packing the
> record already credits is `S2` (`T-011`, `T-065`, `T-088`, `T-098`, `T-101`, `T-117`,
> `T-137`, `T-146`), and custody alone is `S1` (`T-129`). A derived entry scores the
> claim it states at its own counts, at most its premise’s score (`T-002`, `T-016`,
> `T-063`); a second route to a value the record holds at `V3` or above is `S2`
> (`T-054`, `T-055`). A reported result is scored as its claim, as a replay would score
> it.

## Findings

All non-blocking.

**F-1, record: the synopsis’s glance rows are stale at three entries.** `SYNOPSIS.md`
prints `S4` for `T-053`, `S1` for `T-063` and `S3` for `T-065`. The renderer that
rewrites it, `devtools.render_results_headline`, is a write this lane may not make; the
records lane runs it when the lanes merge, and `packing-validate --records` reports the
drift until then.

**F-2, record: eight scores predate the draft rule and name no review.** `T-021`,
`T-027` to `T-030` and `T-034` to `T-036` were scored by their registering sessions
before `epistemics.md` said a registration score is a draft, and their `by` does not say
draft. They are consistent with the pass and were not rewritten.
If the owner wants every `by` to name a review, these eight can take this review’s name
without a change of score.

**F-3, record: the three truncated `by` values are gone.** `T-056`, `T-057` and `T-061`
had `by: issue #227 intake …`, which YAML read as the one word `issue` (`think-nr59`);
each now names this review and the intake it confirms.

**F-4, judgement: `T-023` against `T-031`.** Two case exclusions at $n = 11$ that move
no bound differ by one rung of significance on grounds about the method each showed.
Both are reviewed scores and both results are superseded by `T-060`, so the rules keep
them; the owner may prefer one score for the two.

**F-5, judgement: `T-088` and `T-089` sit on the kind side of the upper-bound line.**
Their steps, $1.1 \times 10^{-5}$ and $6.8 \times 10^{-5}$, are in the magnitude band
the 11 October grading review gives `S3`, but each optimizes a packing already reported
rather than moving it to a new arrangement, and the line in this record is drawn by
kind. Kept at `S2`, as their 5 October review confirmed them.

## Disposition

The rescored register and the re-rendered `RESULTS.md` are in this lane’s commit, with
this review mapped in `docs/project/document-map.yaml` as a retained review.
No `epistemics.md`, case record, synopsis or evidence file was edited.
`packing-validate --records` passes apart from the synopsis rows F-1 names.
The score gates nothing: no rung, status or bound moves with this review.

## Status, 14 October

Two reviews of the pull request that carries this review (#563, reviews A and B of 14
October) found the following, and this section records them rather than rewriting the
findings above.

- **Corrected in place.** The summary attributed the `T-063`/`T-016` pair to the 2
  October review of $s(60)$; it is the 1 October process review’s (its table of five
  pairs). The kept-score table listed `T-080` as the same kind at other counts; it is the
  replay of `T-073`’s own counts.
  The proposed paragraph’s second-route rule now reads “at `V3` or above”: as first
  written it would have moved `T-154`, a second route to `T-153`’s value at `V0`, from
  `S5` to `S2` without anyone deciding to.
- **Corrected in the register.** Seven statements in the new rationales of `T-040`,
  `T-052`, `T-063` (two), `T-073`, `T-081` and `T-117`, and the standing that `T-043`’s
  and `T-046`’s rationales stated in the present tense.
  No score changes.
- **Not read by this pass.** `T-147` to `T-156` were registered after it.
  `T-147` to `T-152` carry scores their import reviews confirmed.
  Three remain drafts: `T-154` (`S5`, “draft for the owner”), and `T-155` and `T-156`
  (`S1`, the registering lane’s). `T-155` gives exact regularized sides of credited
  packings, so under the proposed paragraph it would read `S2`, beside `T-098`, `T-117`
  and `T-146`, and `T-156`, derived from it, at most that; their reviewing lane decides
  (`think-7j5d`).
- **Found after the consistency pass.** `T-150` (`S2`) against `T-152` (`S3`): both
  refine packings the record already credits, with no square moved beyond a tenth of a
  unit. The 12 October `think-qh3s` note put the pair to the owner (#543); the
  consistency table above stops at `T-146` and does not explain it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
