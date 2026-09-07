# Research: Public Sources for Square-Packing Records Beyond `n = 100`

**Date:** 2026-09-07

**Author:** Joshua Levy, with Claude Fable 5.1 assistance; web survey delegated to a
Claude Opus agent and re-checked against the retained catalogue pages

**Status:** Complete for the question asked.
Phase 0 of
[the atlas expansion plan](../specs/active/plan-2026-09-07-atlas-expansion-to-324.md),
bead `think-4yup`, under epic `think-0juv`.

## Overview

The known-best atlas stops at `n = 100`, and the prospective source map stops at
`n = 324`. Before widening either, the plan needs to know which public sources carry
geometry above 100, what each one’s reuse terms are, and whether any authority makes a
completeness claim for `325..400` that would justify building that range.
This document answers those three questions and records the negatives, so a later pass
starts from an audit rather than from an assumption.

Every fetched page was treated as data.
Reuse-terms findings were re-read by the coordinator; the values quoted for `325..400`
and the provenance-comment structure were checked against pages and files already
retained under `packing/resources/`.

## Questions to Answer

1. Which public sources carry coordinate-bearing geometry for `n > 100`, and which of
   them are primary?
2. What reuse terms does each state?
3. Is there any dense, authoritative coverage of `325..400`, or a completeness claim for
   it, comparable to the catalogue’s statement for `n ≤ 324`?

## Scope

Public web catalogues, dataset releases, code repositories, encyclopedias, integer
sequence databases, and 2020–2026 preprints.
Not in scope: private communications, unpublished solvers, or any request to a source
author.

## Findings

### The dense catalogue above 100 exists exactly once

The Kingbird catalogue at `kingbird.myphotos.cc/packing/`, maintained by David Ellsworth
on Erich Friedman’s original compilation, is the only source that collects, dates,
attributes, and serves machine-readable geometry for records above `n = 100`. Its flat
grid lists 135 cases above 100, of which 116 beat the trivial grid: 111 in `101..324`
(largest non-trivial `n = 307`) and five isolated records above 324 (626, 1453, 1765,
1850, 2043). The main page’s HTTP last-modified date is 2026-05-16; the sub-pages are
dated 2026-02-09.

Three further pages on the same site carry family members above 324: the rigid-packings
page, the Göbel-squares page, and the Göbel-strips page.
Together they give 40 distinct `n ≥ 325` with rendered geometry, up to `n = 9465` on the
Göbel-squares page, a Göbel square with side `49 + (69/2)√2`, and `n = 2135` on the
Göbel-strips page. Two values the survey first counted, 2938 and 3047, sit only in HTML
comments on the strips page and are not rendered; the archive pass of 2026-09-07 caught
that, and all three pages are now retained under `packing/resources/web/`.

The per-`n` asset pattern is `square-<n>.svg`, with page-specific variants (`b`, `_r0`,
`_r1`) that must be read from the page rather than guessed; there is no directory index.
Each SVG carries the side as a high-precision DTD entity with a closed-form comment, the
full geometry, and a leading provenance comment naming the discoverer, date, the pattern
extended, and often a link.
The retained `n = 29` provenance SVG under `packing/resources/papers/` has exactly that
structure, so the parser this repository already has is the right starting point.
The HTML pages print exact radicals and, for degree three and above, a minimal
polynomial; the largest degree observed is 62, at `n = 1453`.

Reuse terms: none stated anywhere that was checked, including the site root, a `LICENSE`
path, a `license.html` path, and the GitHub fork of Friedman’s site, which carries no
packing data. This agrees with the repository’s 2026-08-26 review and with
`sources.json`’s `license_status: no-express-reuse-terms-found`.

### Everything else is sparse, capped, or a different problem

| Source | Coverage above 100 | Terms | Reading |
| --- | --- | --- | --- |
| UnitSquare Project, `hmbelvedere.com`, release 2026-07-29 | four values: 103, 105, 110, 131 | CC BY 4.0 in the page’s dataset metadata | primary but narrow; parents are Kingbird cases; interval receipts not public |
| Thomas Schadt, GitHub `Squares-packing_S-29-_New-Record` | none; `n = 29` only | MIT | the GPU annealer behind many 2025–2026 records has no public artifact; its results reach the record only through catalogue provenance comments |
| Friedman, Packing Center “Squares in Squares” | none; the page is now a one-sentence redirect to Ellsworth | none | the last data-bearing snapshot, 2023-05-30, covered `n ≤ 89` as images |
| Friedman, EJC dynamic survey DS7 | none; the abstract bounds it at `n ≤ 100` | author-held copyright, no licence statement | still the citable authority for lower-bound machinery and pre-2009 provenance |
| Ellsworth’s SVG re-edit of DS7 on the same site | `n ≤ 100` plus a few figures | none stated | derivative of DS7 |
| Wikipedia, “Square packing” | prose only | CC BY-SA 4.0 | its only catalogue link is Kingbird |
| OEIS A005842 | not this problem | OEIS terms | consecutive squares of sides `1..n`, not unit squares |
| Packomania | none | — | circles only |
| arXiv 2020–2026 | no table beyond 100 found | various | asymptotic results and small-`n` optimality proofs only |

No permissively licensed source gives dense geometry above `n = 100`. CC BY covers four
values, MIT covers one, and the 111-case catalogue carries no terms.

### `325..400` has five values and no completeness claim

| `n` | Side | `⌈√n⌉` | Page |
| ---: | --- | ---: | --- |
| 331 | `18 + √2/2` | 19 | Göbel strips |
| 335 | `16 + 2√2` | 19 | rigid packings |
| 369 | `19 + √2/2` | 20 | Göbel strips |
| 373 | `17 + 2√2` | 20 | rigid packings |
| 376 | `10 + (14/2)√2`, as the page prints it | 20 | Göbel squares |

The two rigid-page values were confirmed in the retained copy of that page.
The catalogue’s completeness statement covers only `n ≤ 324`; above it the site lists
family members and isolated records and says nothing about the cases between them.
So there is no authority for calling a grid at, say, `n = 350` the best known packing.

The Göbel strip family, side `k + √2/2`, and the Göbel square family, side
`a + 1 + (b/2)√2` at `n = 2(a+1)a + b²`, are stated as closed-form constructions on
those pages, so they are constructive for every `n` they cover.
This repository already builds Göbel-family cases from Friedman DS7’s statement of the
rule rather than from any catalogue file, which keeps them outside the retention policy.

## Key Insights

- **324 is a source boundary, not a convenience.** The gapless map to 324 exists because
  one sentence on one page vouches for every unpictured case.
  Nothing vouches for `325..400`.
- **The fetch-and-derive route is the only dense route.** For `101..324` the choice is
  between the catalogue’s numerical facts under the existing retention policy, or 123
  empty cards. There is no licensed alternative to find.
- **Provenance is richer in the SVG than on the page.** The entity value carries 30 to
  50 digits and the comment carries the discoverer and date, which is what a generated
  frontier record’s `found_by` and `found_year` fields need.
- **The frontier above 100 lives on the web.** No 2020–2026 paper tabulates it.
  A record that exists only as a catalogue entry has no second source to reconcile
  against, which raises the value of the machine reparse in Phase 1.

## Recommendations

1. Build `101..324` under the derived-facts retention precedent, as the plan’s `D2`.
2. Do not open Phase 6 on this survey.
   If the owner wants `325..400` anyway, the honest form is grids plus the two Göbel
   families regenerated from their closed forms, with every card carrying an explicit
   “no source vouches for this as best known” provenance, and the five listed values
   retained as catalogue-derived facts.
3. Archive the Göbel-squares and Göbel-strips pages under `packing/resources/web/` with
   the same procedure as the other catalogue pages, so the family statements have a
   retained source. Done on 2026-09-07.
4. Parse `found_by`, `found_year`, and the closed-form comment from each SVG’s
   provenance block during the fetch-and-derive pass, and type them as `catalogue`
   provenance.

## References

- [Atlas expansion plan](../specs/active/plan-2026-09-07-atlas-expansion-to-324.md)
- [Retention policy](../../../packing/resources/web/known-best-packings/README.md)
- [Prospective source map](../../../packing/atlas/prospective/README.md)
- Retained catalogue pages under `packing/resources/web/kingbird-squares-in-squares*.md`
- Survey working notes: session-099 scratch, not retained

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
