# `s(11)` Lower-Bound Literature Audit, 2026-09-04

This is the durable source receipt for the literature and priority claims attached to
[`T-018`](../../../frontier/RESULTS.md), the first-party certificate proving
`s(11) >= 381/100`.
It records what was searched, what was found, and what changed in the frontier.
It does not turn a negative search result into proof of priority.

## Conclusion

No public source located through 2026-09-04 gives a lower bound for unrestricted
packing of eleven congruent unit squares in a square above Stromquist's 2003 value

```text
2 + 4/sqrt(5) = 3.7888543819...
```

The new `381/100 = 3.81` certificate therefore remains **apparently novel**: the first
located public improvement since 2003, not a claim of absolute priority.
The best-known upper construction remains Trump's 1979 packing at approximately
`3.877083590022814`, so the case is still open.

The search did change the repository's account of the method.
The broad argument is not a new weighted-cover principle.
Its lineage runs from integral unavoidable points and multi-lattice counting through
Nagamochi's explicitly scored point, segment, and area resources and Bentz's
"resource starvation" account.
The recent contribution of Burns and Massaccesi is the pure-atomic rational
direction-net certificate architecture and its LP construction; the new contribution
here is the `n = 11` instance and its generator.

## Search record

The adversarial review searched the retained full-text archive and frontier register,
then arXiv, Crossref, OpenAlex, Semantic Scholar citation chains, author pages, and
public packing catalogues.
The final reconciliation reran exact-value and topic searches including:

```text
"381/100" "unit squares" packing square
"100/381" square packing
"110000/145161" packing squares
"s(11)" "unit squares" packing lower bound
"11 unit squares" square lower bound packing 3.81
site:arxiv.org "packing unit squares" "11" square
"fractional" "unavoidable" square packing unit squares
"resource starvation" "unit squares" packing
```

The reciprocal and density forms matter because a packing source may normalize the
small square rather than the container.
The method terms matter because a prior result could anticipate the certificate
architecture without stating this exact bound.
Search rankings and index contents are mutable; the query strings are repeatable, but
this is not a byte-for-byte snapshot of a search engine.

## Sources that decide the record

| Source | What was checked | Effect on `T-018` |
| --- | --- | --- |
| [Stromquist 2003](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8) | Theorem 2 states `s(11) >= 2 + 4/sqrt(5)` | The published lower bound displaced by `381/100`; the repository's separate repaired proof remains the trusted route to the old value |
| [Friedman DS7](https://erich-friedman.github.io/papers/squares/squares.html) | The survey still gives the Stromquist lower bound | Corroborating historical survey, not a stronger result |
| [Leaps in Bounds](https://leapsinbounds.org/constants/square-packing-in-square-11/) | The live `s(11)` entry still lists lower `2 + 4/sqrt(5)` and upper about `3.8771` | Current public-catalogue corroboration; secondary and not proof evidence |
| [Trump 2023](https://trump.de/square-packing/Packing-11-squares.pdf) | The author's account of the 1979 upper construction | Confirms the upper-bound provenance; no global optimality proof |
| [Kingbird](https://kingbird.myphotos.cc/packing/squares_in_squares.html) | Current record catalogue and exact-construction provenance | Corroborates the upper record and open status; not a lower-bound source |
| [Abrahamsen–Stade 2024](https://doi.org/10.1109/FOCS61266.2024.00087) | A recent refereed paper states that the optimum for eleven freely rotating unit squares remains unknown | Independent current-status corroboration; it does not report a lower bound |

The primary papers, author note, catalogue capture, and their local reading copies are
indexed by [`packing/resources/README.md`](../../README.md).
Leaps in Bounds is retained here as a live-query reference rather than copied HTML: it
adds a current secondary cross-check, not a mathematical premise.

## Sources that decide the method attribution

| Source | Relevant antecedent |
| --- | --- |
| [Göbel 1979](https://ir.cwi.nl/pub/12685/12685D.pdf) | Finite unavoidable point sets: the integral hitting-set precursor |
| [Kearney--Shiu 2002](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v9i1r14) | Two unavoidable lattices and a dual counting argument |
| [Nagamochi 2005](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v12i1r37) | Nonnegative scores on points, line segments, and area, summed so every unit square consumes more than one unit |
| [Bentz 2016](https://arxiv.org/abs/1606.03746) | Explicitly names the family as resource-starvation arguments and summarizes point, segment, area, and moving-resource variants |
| [Bašić–Slivková 2018](https://people.dmi.uns.ac.rs/~bojan.basic/papers/square_pak%20new.pdf) | Formulates piercing numbers for admissible unit squares and connects them to `s(n)` |
| [Govindarajan–Nivasch 2015](https://arxiv.org/abs/1409.1194) | Gives the standard weighted-point/fractional-transversal terminology in general geometric hitting-set language; applying that name here is an inference |
| [Burns 2026](https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/) | Pure-atomic, exact-rational direction-net certificate for `n = 17` |
| [Massaccesi 2026](https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html) | LP-generated weights and the parameterization used by the retained control |

The Burns and Massaccesi source snapshots and replayable programs are retained under
[`n17-lower-bounds-2026`](../n17-lower-bounds-2026/README.md).

## Reconciliation into the repository

This audit supports the following record changes and no others:

- `n-011.md`, `T-018`, and `E-n011-fractional-certificate` cite this bounded search and
  keep the novelty label `apparently-novel`.
- The `n = 11` current lower endpoint is `381/100`; no other frontier endpoint changes
  as a consequence of this search.
- The review and portable proof package attribute the broad resource argument to the
  older literature and the recent certificate architecture to Burns and Massaccesi.
- The main 2026-08-22 `s(11)` survey carries a dated addendum instead of rewriting its
  historical 2026-08-25 snapshot.
- The recovered Trump 2023 author note is distinguished from the still-unretained 1979
  communication; older prose saying that the 2023 note was unavailable is corrected.

## Known gaps

The search did not exhaust subscription-only MathSciNet or zbMATH full text, every
thesis and proceedings volume, non-English or unindexed material, private
correspondence, or unpublished work.
Current catalogues can also lag new results.
Those gaps are why the record says **apparently novel** and why an archival release and
outside mathematical review remain worthwhile.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
