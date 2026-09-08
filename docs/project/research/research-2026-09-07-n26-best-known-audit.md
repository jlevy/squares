# n = 26: Best-Known Upper-Bound Search

Search and retrieval window: 2026-09-07 PDT, extending into 2026-09-08 UTC. Problem:
pack 26 congruent unit squares, with arbitrary orientations and disjoint interiors, into
the smallest square container.

Friedman’s construction remains the smallest publicly reported n = 26 square-container
packing identified in this search:

$$
U=\frac{7+3\sqrt2}{2}=5.6213203435596425732025330863145\ldots.
$$

The current primary record table gives this value and attributes the packing to Erich
Friedman in 1997. Newly located repositories with commits in September 2026 retain it.
No retrieved paper, record announcement, source-coordinate entry, or numerical-search
result supplies a smaller n = 26 candidate.
This supports retaining *best known as of the sources checked on September 7, 2026*. It
does not establish global optimality or absence of unpublished or unindexed work.
See
[Ellsworth’s record table](https://kingbird.myphotos.cc/packing/squares_in_squares.html).

## Primary Record and Construction Sources

Friedman’s active [Packing Center](https://erich-friedman.github.io/packing/) directs
readers seeking squares in squares to David Ellsworth’s catalogue.
Ellsworth supplies the n = 26 formula, historical attribution, and
[coordinate-bearing SVG](https://kingbird.myphotos.cc/packing/square-26b.svg).
The catalogue contains improvements for other counts dated in 2026, but the n = 26 entry
gives no separate recent review date.
This audit uses its retrieval date rather than inferring an update date from a
search-engine crawl.

The
[first survey version, published March 6, 1998](https://www.combinatorics.org/files/Surveys/ds7/ds7v1-1998.pdf),
includes the n = 26 improvement.
Its construction packs $2a^2+4a+b^2+1$ squares in side $a+3/2+b/\sqrt2$; substituting
$a=2,b=3$ gives 26 and $U$. The
[2000 version, Section 3](https://www.combinatorics.org/files/Surveys/ds7/ds7v2-2000/ds7-2000.html),
repeats the construction.
The [2009 author copy](https://erich-friedman.github.io/papers/squares/squares.html)
retains it. These versions document the history of one source, not independent
contemporary record searches.
The journal’s
[version history](https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS7/versions?inline=1)
dates the five editions to 1998, 2000, 2002, 2005, and August 14, 2009.

Ellsworth’s
[historical comparison table](https://kingbird.myphotos.cc/packing/squares_in_squares__compared.html)
gives these n = 26 predecessors:

| Attribution in the catalogue | Container side | Comparison with $U$ |
| --- | --- | --- |
| Göbel, 1979 | $5+\sqrt2/2=5.70710678118654\ldots$ | Larger |
| Stenlund, early 1980 | $5/2+9\sqrt2/4=5.68198051533946\ldots$ | Larger |
| Stromquist, 1984 | Root of $s^3-14s^2+67s-112=0$, $5.65062919143938\ldots$ | Larger |
| Friedman, 1997 | $(7+3\sqrt2)/2=5.62132034355964\ldots$ | Standing value |

The historical year labels above are the catalogue’s attribution.
The [memo reconstruction](research-2026-09-07-stromquist-n26-verification.md) resolves
the supplied Stromquist construction and its comparison with $U$.

## Other Catalogue Routes to Twenty-Six Squares

The catalogue also exposes
[square-26.svg](https://kingbird.myphotos.cc/packing/square-26.svg),
[square-26b.svg](https://kingbird.myphotos.cc/packing/square-26b.svg), and
[square-26c.svg](https://kingbird.myphotos.cc/packing/square-26c.svg).
The third SVG declares the same $U$ and uses seven tilted and nineteen aligned squares.
It is an equal-side control with a different arrangement from the nine-tilted-square
construction used in the current search specification.
Its geometry has not been independently replayed in this review.
Reconstructing and verifying it is a concrete prerequisite for testing that additional
arrangement; it does not itself lower the record.

Deleting squares from a larger packing also deserves a precise limit.
The [current catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
lists sides $5+\sqrt2/2$ for 27 squares, approximately $5.82444461667405$ for 28, and
$5.93383346267692$ for 29. Its introductory rule assigns the trivial side 6 to omitted
counts 30 and 31. All exceed $U$. For any parent packing with at least 32 squares, area
gives a container side at least $\sqrt{32}>U$: exactly,

$$
U^2=\frac{67+42\sqrt2}{4}<32,
\qquad 2\cdot42^2=3528<3721=61^2.
$$

Thus simply deleting squares while keeping a listed parent’s enclosing square cannot
improve $U$. This does not exclude cropping or re-enclosing the surviving twenty-six
squares, or moving them afterward.
The [source-score comparison](../../../packing/cases/stromquist/n26-source-scores.json)
records this scope alongside the numerical candidate comparisons.

## Recent Repositories and Candidate Results

| Primary project and dated snapshot | n = 26 evidence | Scope of this audit |
| --- | --- | --- |
| [chelokot/square-packing-archive](https://github.com/chelokot/square-packing-archive/tree/753079eb37d8d16225a5dc1f56e493a3c3b243f4), commit September 5, 2026, 21:42:12 UTC | [Manifest](https://github.com/chelokot/square-packing-archive/blob/753079eb37d8d16225a5dc1f56e493a3c3b243f4/archive/manifest.json) lists Friedman 1997 and exact $U$. [Configuration](https://github.com/chelokot/square-packing-archive/blob/753079eb37d8d16225a5dc1f56e493a3c3b243f4/archive/configurations/square-26-tracker.json) records exact $\mathbb Q(\sqrt2)$ coordinates imported September 5 from Ellsworth’s SVG. | The manifest reports a Lean check dated September 6, 2026. The [theorem source](https://github.com/chelokot/square-packing-archive/blob/753079eb37d8d16225a5dc1f56e493a3c3b243f4/formal/SquarePackingArchive/Records/Square26Tracker.lean) states `HasPacking 26 U`. Source and metadata inspected; Lean was not replayed here. This is feasibility evidence at $U$, with no optimality claim or improved side. |
| [EvanOman/squares-in-squares](https://github.com/EvanOman/squares-in-squares/tree/1004f62cdb2a283ab386c7da54f11871e3bd71d7), commit September 3, 2026, 01:49:39 UTC | [Square data](https://github.com/EvanOman/squares-in-squares/blob/1004f62cdb2a283ab386c7da54f11871e3bd71d7/site/data/squares.json) records $U$, decimal `5.621320343559643`, 26 coordinate triples, `proven:false`, and Friedman 1997. | Imports `square-26b.svg` from Ellsworth. The decimal is a floating representation of the same exact expression, not an improvement. This is a recent reuse of the primary table. |
| [forloopcodes/least-space-squares](https://github.com/forloopcodes/least-space-squares/tree/6a5646dec9d89a5f750adcf488c769b60fe5ccf9), commit September 3, 2026, 04:25:56 UTC; repository pushed September 6 | [Cached coordinates](https://github.com/forloopcodes/least-space-squares/blob/6a5646dec9d89a5f750adcf488c769b60fe5ccf9/data/best_packings.json) give side `5.621320343794426`, approximately $2.35\times10^{-10}$ above $U$, from a 45-degree $3\times3$ block with an offset. | Its [benchmark](https://github.com/forloopcodes/least-space-squares/blob/6a5646dec9d89a5f750adcf488c769b60fe5ccf9/results/benchmark.md) includes a 60-second numerical search for n = 26 and reports a match at displayed precision. Its longer benchmark omits n = 26. Its geometry checks use a stated $10^{-9}$ tolerance; this audit does not adopt them as exact certificates. |
| [DavidRickmann/SquarePacking](https://github.com/DavidRickmann/SquarePacking/tree/b17b9a1d1098e910e64da132d14fd511a749e6f0), commit July 19, 2026, 00:36:37 UTC | The README’s worked examples retain Friedman 1997 for n = 26 and report a class-A local-rigidity result. | No smaller n = 26 packing is presented there. The rigidity assertion has not been independently reviewed or replayed in this search and supplies no global-optimality conclusion. |
| [steventhornton/sqpack](https://github.com/steventhornton/sqpack), repository pushed May 27, 2026 | Its [known-best data](https://github.com/steventhornton/sqpack/blob/main/sqpack/data/known_best.json) gives `5.62132034355964` for n = 26. | The file cites Ellsworth. Its published tree contains solver code and this reference table, with no retrieved improved n = 26 result. |

These recent projects establish that the same n = 26 value is in current circulation.
Their explicit dependence on Friedman and Ellsworth prevents treating them as several
independent surveys of the literature.
The chelokot archive’s new record claims concern n = 68 and 69, and it describes its
historical catalogue as incomplete.

The retained source data include the
[MinMax Arena JSON](https://minmaxarena.com/data/tilted-squares-in-square.json)
underlying its
[n = 26 entry](https://minmaxarena.com/en/problems/tilted-squares-in-square/p18-n26-v1).
The archived response gives `generatedAt: 2026-09-08T00:34:07.581Z` and the record gives
`recordedAt: 2026-09-02T18:06:21.856Z`. The site uses the reciprocal convention:
maximize the common square side inside a unit container.
Its integer score `31646327699330128` represents a squared side, not a unit-square
container side. Recomputing the smallest squared side from the nine tilted half-edge
vectors gives

$$
R=\frac{1977895481208133}{62500000000000000}<\frac1{U^2}.
$$

Specifically, $R=4[(62895084/10^9)^2+(62895074/10^9)^2]$; the aligned squares are
slightly larger. The score-implied normalized container side is approximately
$5.6213203992203053755>U$. The JSON attributes its reference bound to Ellsworth’s SVG of
Friedman’s 1997 construction and describes its submitted record as that construction on
the site’s coordinate grid.
The [reusable scalar checker](../../../packing/cases/stromquist/n26_source_scores.py)
and its [exact results](../../../packing/cases/stromquist/n26-source-scores.json) retain
these comparisons. The exact score comparison does not depend on accepting the site’s
feasibility claim. No independent all-pair geometry replay of this submission was
performed. The
[source archive](../../../packing/resources/web/n26-best-known-2026-09-07/README.md)
retains the JSON and recent repository extracts.

## Papers and Announcements Checked

| Primary publication or announcement | Date supported by the source | Relevance to n = 26 |
| --- | --- | --- |
| [Gensane and Ryckelynck, *Improved Dense Packings of Congruent Squares in a Square*](https://link.springer.com/article/10.1007/s00454-004-1129-z) | Online October 20, 2004; July 2005 journal issue | Announces improvements for 11, 29, and 37 squares and an alternative for 18. The [archived text](../../../packing/resources/papers/gensane-ryckelynck-2005-improved-dense-packings.raw.md) has case discussions for 11, 17, 18, 29, and 37, with no n = 26 improvement. |
| [Kearney and Shiu, *Efficient Packing of Unit Squares in a Square*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v9i1r14) | February 11, 2002 | Full paper checked for transfer to 26 squares. Theorem 2 applies at parameter 5, but its upper estimate exceeds 6. The explicit seed constructions and their stated extensions supply no improvement on $U$; details below. |
| [Arslanov, Mustafin, and Shangitbayev, *Improved Packings of n(n−1) Unit Squares in a Square*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v28i4p22) | November 5, 2021 | Its [full paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v28i4p22/pdf/) includes 26 unit squares in a $4\times8$ rectangle, used as a component in larger constructions. This is not an n = 26 square-container record. |
| [Bui, *Square Packing with O(x^0.6) Wasted Area*](https://arxiv.org/abs/2508.04603) | August 6, 2025, first arXiv submission | Asymptotic large-square construction. No explicit improved n = 26 packing was identified in the checked source. |
| [McClenagan, *Optimally Packing a Large Square by Unit Squares*](https://arxiv.org/abs/2602.01484) | February 1, 2026, first arXiv submission | Asymptotic wasted-area theorem, not a reported n = 26 record. |
| [UnitSquare Results, Release 1](https://www.hmbelvedere.com/) | July 29, 2026 | Announces six upper improvements, for 68, 69, 103, 105, 110, and 131 squares. No n = 26 claim. Verification assurances remain source-reported in this search. |
| [Joost de Winter, *Improved Packings of 68, 126 and 206 Unit Squares in a Square*](https://www.researchgate.net/publication/411979559_An_improved_packing_of_206_unit_squares_in_a_square) | Author-uploaded August 14, 2026; constructions dated August 7–14 | Announces those three counts. No n = 26 improvement. Search-index rendering of the author-uploaded source inspected; the [existing source record](../../../packing/resources/web/de-winter-improved-packings-2026/README.md) documents conflicting live revisions and unavailable coordinates. |

Kearney and Shiu’s
[Theorem 2, printed page 2](../../../packing/resources/papers/kearney-shiu-2002-efficient-packing-unit-squares.pdf),
applies to every positive integer parameter, so a large-size restriction does not
exclude 26 squares. At parameter 5 it gives $s(26)<5+3/10^{1/3}+3/10^{2/3}$, whose right
side exceeds 6 and is weaker than $U$. Section 4’s Pell seeds have parameters
$2,8,42,\ldots$; its separate symbol $k=5$ belongs to parameter 8, hence 65 squares.
Extending the parameter-2 seed gives $s(26)\le5+1/\sqrt2$, larger than $U$ by
$(3-2\sqrt2)/2>0$. Section 5’s seeds, from Equation (10), are $1,12,55,\ldots$; the
stated interpolation gives no better result at parameter 5. Section 6 refines parameter
43, or 1850 squares.
This checks the published constructions and transfer rules, without exhausting their
possible modifications.

The current [MathWorld table](https://mathworld.wolfram.com/SquarePacking.html) also
gives exact $U$ and no optimality asterisk for n = 26. It is secondary corroboration and
cites Friedman and Ellsworth.
Its September 2, 2026 footer links the site’s general update page; that date should not
be assigned to the n = 26 article or record.
The printed `5.6214...` is coarse display text; comparisons should use its exact
expression.

## Consistency with the Lower-Bound Record

The [n = 26 case](../../../packing/frontier/n-026.md) distinguishes the independently
verified interval

$$
1+\sqrt{17}\le s(26)\le U
$$

from Green’s stronger reported lower bound $2\sqrt2+(27+2\sqrt{10})/13\approx5.3918$.
Friedman’s DS7 Theorem 9 at $k=5$ and Table 2 give that report, but the proof cited as
private communication has not been recovered.
It cannot replace the verified lower bound on that evidence alone.

The accompanying [DS7 audit](../../../packing/devtools/audit_ds7_lower_bounds.py)
compares the named theorem and table candidates across all 324 case records.
It preserves exact identities separately from opaque table decimals and leaves every
verified-bound field unchanged.
Two source discrepancies require explicit treatment:

- The printed Table 2 expression for n = 82–85 exceeds the elementary grid upper bound
  10, despite displaying approximately 9.2667. It is excluded; the separate Theorem 9
  specialization supplies the reported value $(247+94\sqrt2)/41$.
- The literal Theorem 10 specialization at $k=4$ gives a stronger n = 19–20 lower bound
  than the same survey’s table.
  The source states no restriction explaining the difference.
  The specialization is retained as a report, with this unresolved source caveat and no
  promotion to a verified theorem.

These corrections concern the completeness and interpretation of source records.
They do not change the n = 26 upper bound or establish new packing theorems.

## Search Coverage and Remaining Limits

The web search combined the problem names “packing unit squares in a square,” “congruent
squares,” and “squares in squares” with `26`, `n=26`, `s(26)`, “twenty-six,” “improved,”
“new record,” and years 2025–2026. Numeric searches used `5.621320`, `5.6213`, `5.62`,
and `5.61`. Broader queries sought algorithm and record announcements from 2015–2026.
The checked results led to journal and author sources, arXiv, Friedman and Ellsworth,
recent GitHub projects, and the MinMax leaderboard.
Source-engine crawl labels were not treated as publication dates.

Additional exact queries included `"26" "square packing" "new" "2024"`,
`"26" "square packing" "record" "2026"`,
`"5.621320" -site:github.com -site:kingbird.myphotos.cc -site:reddit.com`, and
`"unit squares" "26" site:arxiv.org`. The search also paired 26 with German
`Einheitsquadrate` and `Quadrat`, French `carrés unité` and `carré`, Russian
`единичных квадратов` and `квадрат`, and Japanese `正方形`, `パッキング`, and `単位正方形`;
supplementary phrases included `упаковка квадратов` with `Фридман`, and `empilement`
with `26 carrés`. These scoped searches found no new primary record; they do not
constitute a complete search of the corresponding language literatures.

The GitHub repository search `square packing in:name,description`, sorted by most
recently updated, screened the first 40 returned repositories and led to the recent
projects above. README and tree inspections excluded BaloghMartin/SquarePacking, whose
objects have varying sizes; BillyChern/Packing-Unit-Square, which studies the Meir–Moser
rectangle problem; and brifl/square-packing, whose retrieved tree contains only README,
license, and ignore files.
Additional README-index queries used `"5.621320"` and `n26 squares`. GitHub’s index did
not even return the known recent README for the exact numeric query, so zero results
provide no assurance of global absence.

Other recurring false matches concerned packing 26 unequal circles while maximizing
total radius, packing consecutive squares of sides 1 through 26, covering rather than
disjoint packing, axis-parallel problems, square packing in a circle, and asymptotic
results without an explicit 26-square construction.
These variants were excluded from the record comparison.
For example, Simonis and O'Sullivan's
[*Almost Square Packing*](https://citeseerx.ist.psu.edu/document?doi=4e6803943b6c8351ec2fd56cb979f1dc3a8616cb&repid=rep1&type=pdf)
has an n = 26 result for unequal rectangles $1\times2,\ldots,26\times27$ in a
rectangular container.
[MacIver’s lower-bound and proof-mechanism work](../reviews/review-2026-09-07-maciver-square-packing.md)
is reviewed separately and does not supply a smaller n = 26 upper packing.

This audit did not contact authors, search private correspondence, or exhaust every
repository and database.
Several checked projects obtain their reference data from the same catalogue, and search
indices can omit fresh work.
A new credible source claiming a side below $U$, or supplying coordinates potentially
below it, is sufficient to reopen the record review; exact containment, unit-edge,
all-pair non-overlap, and side comparison must precede adopting that candidate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
