# Plan: Others’ Results in the Results Register

**Date:** 2026-09-29

**Author:** Claude (agent), for the repository owner

**Status:** Active. The register for others’ results is on main (68903d852, 2026-09-29);
follow-ups remain open under think-z9wy (10 of 14 children, among them think-5xr9 and
think-nvbq).

**Workflow:** W7 pipeline improvement, following the W8 refresh of Session 161

## Summary

The results register holds this project’s results and three others’ (`T-015`, `T-016`,
`T-032`). Since 22 August 2026 about twenty results by others have moved a case here,
and each one is taken in, replayed, reviewed and registered in a case file, but none of
them has a register entry.
Their credit lives in bibliography prose and their verification state in evidence
entries, and no one view shows which results by others are verified, which are reported
and waiting on a replay or review, and who they are credited to.

The proposal: register others’ results in the same register, under the same `T-NNN`
identifiers and the same derived `V`/`C` rungs, with a typed attribution block that
names the original source, and a gate that fails when a result the case records act on
has no entry. The register then tracks two things separately for each result by others:
the result, credited to its authors as their source states it, and this repository’s
verification of it, which is the `C` rung and its evidence.

## What Enters the Register

The owner’s rule, 2026-09-29: track all of this project’s own results, and every result
that arose since this project began, whether it builds on this project’s work or not,
when there is something to codify, review or verify about it.
Not every result.

Stated so a checker can hold it:

1. **Every result of this project**, as now.
2. **Every result by others dated on or after 22 August 2026** (`RECENT_SINCE`, the day
   this project’s square-packing work began) **that the record acts on**: its bound is,
   or was, a case’s reported or verified lower bound, or this repository has replayed or
   reviewed it, or a replay or review of it is queued.
3. **An older result by others** only when it holds or held a verified field here, or is
   a machine audit of the literature, which is the standing practice (`T-004`, `T-008`,
   `T-011`, `T-015`, `T-016`).

Not registered, and kept where they are now (the case record, the retained packet):

- rungs of a ladder that the same release supersedes before anything is done with them
  (wand125’s same-day $3659/500$ and $147/20$ below $37/5$);
- publication records never replayed and never holding a field (Guzhou0806’s R042, R043,
  R050 and the R052 continuation; ahyangyi’s unretained `v1.1.1`);
- results below the standing verified bound that ask for no work (Evan Daniel’s
  $s(11) \ge 3040/797$, $s(12) \ge 35/9$ and $3920/997$);
- reports of already-known values that move nothing and have no review queued (Evan
  Daniel’s case-free $s(13) = 4$), unless the owner queues a review;
- 2026 results dated before 22 August that never held a verified field here (Brandwijk,
  Burns, MacIver, Mira’s and Fort’s sixteen-point sets, anabologyco-maker).

**Granularity.** One entry per source release and claim, where every part of the claim
stands at the same rung.
One entry may cover several $n$ through `scope`, as `T-019` does.
When the parts stand at different rungs, the entry splits, for example wand125’s
rectangle certificates into the replayed counts and the reported ones.
As replays land, counts move from the reported entry to the replayed one.

## The Backfill

Nineteen new entries, `T-037` to `T-055`, and attribution added to eight existing ones.
Rungs are as the records stand at `901dbc59`, derived by `check_results`.

| Group | Entry | Result | Rung | Holds a case bound |
| --- | --- | --- | --- | --- |
| Building on this project | `T-037` | Kleddamag, $s(11) > \frac{31}{8}$ | `V4/C4` | yes |
|  | `T-038` | Kleddamag `v1.0.0`, $s(17) > \frac{461300}{99853}$ | `V4/C3` | no |
|  | `T-039` | Guzhou0806 R052, $s(17) > \frac{231001}{50000}$ | `V4/C3` | no |
|  | `T-040` | Kleddamag `v1.1.0`, $s(17) > \frac{232001}{50000}$ | `V4/C3` | no |
|  | `T-041` | Kleddamag, $s(17) > \frac{466001}{100000}$ | `V4/C3` | no |
|  | `T-042` | Guzhou0806 R067, $s(17) > \frac{233009}{50000}$ | `V4/C3` | never held |
|  | `T-043` | Guzhou0806 R068, $s(17) > \frac{116511}{25000}$ | `V4/C3` | yes |
|  | `T-044` | wand125 point certificates, $n = 26, 29, 39\text{–}41, 52, 53, 55, 56, 68\text{–}72$ | `V4/C3` | yes |
|  | `T-045` | wand125 rectangle certificates, replayed: $n = 27, 28, 31, 32$ | `V4/C3` | yes |
|  | `T-046` | wand125 rectangle certificates, reported: 48 counts, $n = 18\text{–}95$ | `V0/C0` | yes, reported lane |
| Crediting this project second-hand | `T-047` | Tokoharu, $n = 11, 26\text{–}31$ | `V4/C3` | yes |
| Independent | `T-048` | wand125, $s(50) \ge \frac{37}{5}$ (its source credits Evan Daniel and Tokoharu) | `V0/C0`, replay running | yes, reported lane |
|  | `T-049` | Evan Daniel, $s(12) \ge \frac{15680}{3951}$ | `V4/C4` | yes |
|  | `T-050` | Evan Daniel, $s(21) \ge \frac{5000}{1001}$ | `V4/C3` | no |
|  | `T-051` | Evan Daniel, $s(32) = 6$ | `V4/C3` | yes |
|  | `T-052` | Evan Daniel, $s(21) = 5$ | `V4/C3` | yes |
|  | `T-053` | Evan Daniel, $s(45) = 7$ | `V4/C3` | yes |
|  | `T-054` | wand125, point-only $s(45) = 7$ | `V4/C3` | second certificate |
|  | `T-055` | wand125, point-only $s(21) = 5$ | `V0/C0`, replay running | second certificate |
| Before this project | `T-004`, `T-006`, `T-007`, `T-008`, `T-011`, `T-015`, `T-016` | Bentz, Nagamochi, Trump, Massaccesi | unchanged | varies |
| Building on this project | `T-032` | Guzhou0806 R012 and Mira | unchanged | no |

The register holds 55 entries, 27 of them others’.
Intake adds one to three a week at the current pace.
The reported entries derive `C0`, not `C1`: the reviews that read them are recorded on
the replay entries, not as an `external_review` on the report entries.

## Schema

Two additions, both optional to a reader, so the contracts stay `ResultsRegister/v1` and
`Bibliography/v1`, and one derived value.

**`attribution`**, required on every `previously-published` result and refused on
`apparently-novel` and `confirmed-novel` ones:

```yaml
attribution:
  source_keys: ['[Guzhou0806 n17 R068]']
  published: '2026-09-28'
```

The credit line, the authors and the lineage are read from the bibliography entries the
keys resolve to, never restated here, so the credit on an original result has one home.
`published` may be a year alone for a source that carries no date (Trump’s 1979
packing). `published` is the date the result entered its source, which can precede the
date this record first saw it (Evan Daniel’s $s(12)$, in his repository from 25 August
and first seen here on 27 September).

**`lineage`** on each bibliography entry cited by an attributed result dated on or after
22 August 2026: `builds-on-project` (the source credits this project’s certificates,
data or pipeline), `credits-project` (the source credits it as inspiration or
second-hand and brings its own method), or `independent`. It is typed because the
`credit` string is prose that `build_bound_citations` declines to parse.
A test holds the two together: a credit that reads “after … Levy” is `builds-on-project`
or `credits-project`, and one that does not is `independent`. That test would have
caught the four $n = 17$ credit gaps the W8 inventory found.

**Whether a result holds a case bound** is derived, not declared: yes when some $n$ in
its scope has a reported or verified bound that cites one of its evidence entries.
A result that does not was superseded, or is a second certificate for a value another
holds. The renderer prints it; nothing stores it.

One consequence follows from the citation rule `build_bound_citations` already has: a
register entry that carries a replay performed here confirms the external bound it
replays, so the atlas citation lines for those bounds gain “(confirmed T-NNN)”. Their
credit text is unchanged.

No new identifier space.
Others’ results continue `T-NNN` from `T-037`, as `T-015`, `T-016` and `T-032` already
do. One namespace keeps a single lookup for every `T-NNN` the reader tier cites, which
`check_results` already resolves.
A separate prefix was considered and rejected: `R0NN` is Guzhou0806’s release naming,
and `X-NNN` is taken.

## Verification of Results by Others

The existing axes already separate the two things the owner asked to track.
`V` is the strongest verification anywhere, whoever ran it; `C` is what this repository
has done. A reported result enters at `V0/C0`, or `V0/C1` once a review is recorded on
it, with a `notes` field saying what the source reports running and a `next_rung` naming
the replay and the review it waits on.
A complete replay raises it to `V4/C3`, a second method to `C4`, and a mapped review
artifact to `C5`, by the same derivation this project’s own results use.

One refinement is left to the owner.
When a source ships a receipt of its own passing run (wand125’s `completion-audit.json`,
Guzhou0806’s replay receipts), recording that run as an evidence entry performed by the
source author would derive `V4/C0`: machine checked by its authors, not yet here.
That reads truer than `V0` for those results, but it requires the evidence schema to
accept a passing replay status on an entry this repository did not perform, which it
does not now do.

## Gates

- **Coverage.** `check_results` fails when a case’s reported or verified lower bound
  cites an evidence entry from a source dated on or after 22 August 2026 that no
  register entry cites.
  This is the rule of the second item above, made mechanical; before the backfill it
  flagged 23 evidence ids.
- **Attribution.** Every attributed result’s source keys resolve in `bibliography.yaml`,
  and each has a `lineage`.
- **Credit consistency.** The test described under Schema.
- **Reader tier.** `check_readme`’s New Results rule is unchanged: it keys on
  `apparently-novel` and `confirmed-novel`, so others’ results stay out of New Results.

## Rendering

`RESULTS.md` groups entries by origin: this project’s results, then results by others
building on this project, crediting it second-hand, independent of it, and published
before it began; within each group, the entries awaiting replay or review come first.
Each row carries the credit line from the bibliography, the published date, `V`/`C` and
whether the result holds a case bound.

README’s “Results by Others” keeps its prose, and gains the generated all-sources table
the W8 refresh proposed (`think-ti71`), rendered from the register instead of from the
case files, so the table and the register cannot disagree.

## Process

Intake of a result by others then follows the same lifecycle as a result of this
project’s: register at intake (`V0/C0`), raise the rung as the replay and review land,
and record supersession by letting the case records move.
The documentation pass (`packing/campaign/documentation-pass.md`, new-result
publication) gains one step: register the result, or extend the entry that already
covers its release.

## Staging

1. The `attribution` and `lineage` fields, the three gates, and the renderer.
2. The backfill, in the same pull request, since the coverage gate fails without it.
3. The README table from the register, and the intake step in the documentation pass.

It lands as a pull request stacked on the W8 refresh (`think-m7zb`), which is stacked on
jlevy/squares#241.

## Open Questions for the Owner

1. The source-run refinement above: `V4/C0` for reported results with a retained source
   receipt, or `V0` until this repository replays them.
2. Whether Evan Daniel’s case-free $s(13) = 4$ should enter with a review queued.
3. `T-017`’s claim to be “the first lower bound specific to $n = 12$ in the retained
   corpus”: the corpus now holds Evan Daniel’s earlier certificate.
   The default is to annotate the claim “reached independently” and keep
   `apparently-novel`, since the search that supported it was sound when made.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
