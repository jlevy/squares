# Exact Polynomial Collection: Mathematical Review

**Date:** 2026-10-07

**Reviewers:** GPT-6 Astra (two independent mathematical lanes), with GPT-5.6 Sol source
collection and integration under Joshua Levy’s oversight.

**Disposition:** The retained source polynomials pass algebraic checks.
The review establishes no additional geometric feasibility, verified bound, or global
optimum.

## Scope and Evidence

The [continuation plan](../specs/active/plan-2026-10-06-exact-side-values.md) starts
from PR 403’s delivered register implementation.
The new
[source packet](../../../packing/resources/web/kingbird-exact-side-facts-2026-10-07/README.md)
retains pinned SVG facts at $n = 55,71,83,126$ and a complete bounded extraction of
printed integer polynomials from retained Kingbird comparison articles and explicit
thematic locators. The [generated register](../../../packing/frontier/exact-values.json)
now records 270 exact current sides and 162 historical entries; 54 current sides remain
numeric.

The historical corpus contains 201 source occurrences and 182 distinct triples of count,
historical printed side and coefficient array, with no unparsed rows.
Every occurrence was matched to the literal equation at its retained line range and
independently expanded with SymPy.
All arrays are primitive with positive leading coefficient and their declared degrees
agree. Twenty-one pairs match current entries.
Another 161 become historical entries; one additional main-catalogue entry gives 162 in
the register.
Attribution, source locators and per-occurrence invalid/fixed flags survive
that projection.

Historical entries comprise 152 superseded sides, three source-invalid proposals, and
seven beyond the current $n = 1\ldots324$ frontier.
The latter concern five counts: 1453, 1765, 1850, 2043 and 2135. Each polynomial is
checked at its own side.
This extraction is complete for the declared retained corpus; it is not an exhaustive
literature theorem about which other polynomials exist.

## Independent Algebraic Checks

One reviewer checked all 126 historical pairs of degree at most 12 with independent
SymPy factorization over $\mathbb{Q}$, exact Sturm root counts in the printed-side cell,
and exact opposite endpoint signs.
All passed (1.64 s locally).

The second reviewer independently replayed all 222 retained finite-field factor patterns
for the 56 higher-degree pairs, checking primality, squarefreeness, degree sums and
intersections of subset-sum factor degrees.
All intersections exclude every proper rational factor degree; no saved irreducibility
flag was trusted (26.43 s). For all 182 saved intervals, exact endpoint signs and a
separate Möbius-transform/Descartes argument independently established uniqueness (1.48
s). For an interval $(A/D,B/D)$ and degree $d$, the latter counts sign variations in
$D^d(1+t)^dP((A+Bt)/(D(1+t)))$; exactly one variation and opposite endpoint signs
establish exactly one interior root.

The retained instrument is `devtools.audit_historical_side_polynomials`. It uses
independent symbolic/finite-field arithmetic and source parsing, with negative controls
for reducibility, altered equations and intervals containing zero or two roots.
It runs at PR and records/full checkpoints, alongside the builder’s own complete replay.
These timings are individual review measurements, not final-tier or hosted-runtime
promises.

## The Degree-672 Polynomial at n = 83

The pinned SVG facts, frontier record and register have identical 673-integer
coefficient arrays: degree 672, primitive content 1, and maximum coefficient length 724
digits. Independent modular factorization gave:

| Prime | Irreducible factor degrees | Remaining possible proper rational factor degrees |
| --- | --- | --- |
| 100003 | 1, 1, 3, 75, 145, 447 | 46 |
| 100019 | 2, 16, 16, 34, 272, 332 | 2: 2 and 670 |
| 100043 | 1, 5, 6, 7, 8, 11, 11, 252, 371 | 0 |

The leading coefficient survives reduction and the reductions are squarefree.
An integer factor would reduce to a factor with a permitted degree at every prime; the
empty intersection therefore proves irreducibility over $\mathbb{Q}$. The independent
factorization replays took 228.98 s, 241.93 s and 368.34 s respectively.
Those deep checks are review evidence; routine admission replays the same exact
certificate with faster modular arithmetic rather than repeating the independent SymPy
factorization.

The saved interval uses the full 318-place decimal centre and radius $10^{-308}$. Its
endpoint signs are $(+,-)$ and uniqueness is independently checked.
The root agrees with the source’s 100-significant-digit side, Daniel’s retained KKT
value, and the frontier’s 14-decimal side.
The source’s `Root[...,27]` index is **stated, not independently counted**; the register
explicitly records that limit.
The polynomial does not itself prove that the pictured geometry realizes the root or
that the packing is optimal.

## Current Systems and Historical Branches

The retained $n = 55$ SVG contains seven contact/stationarity equations in
$s,a,b,c,d,e,f$. The $n = 71$ SVG contains six contact equations in $s,a,b,c,d,e$.
Neither prints a univariate side polynomial for the current packing.
Their elimination and physical real-branch selection remain `think-phh8` and
`think-1blg`.

At $n = 71$, both historical polynomial sides pass exact root/irreducibility checks:
`8.96326750850139` (degree 8) and `8.96028765944389` (degree 4). Neither is the current
side `8.9440715575703155…`. The octic equals the exact norm of the source’s quartic over
$\mathbb{Q}(\sqrt2)$; current-side and perturbed-constant controls are refused.
The source cells separately retain Cantrell’s October 2005 and DeVincentis’s April 2014
attribution.

At $n = 126$, three historical polynomial sides remain historical.
The retained SVG supplies no current polynomial/system and its side differs from both
the current reported record and Daniel’s KKT point.
Their agreement/branch obligations belong to `think-1atr`; the source absence is a
bounded negative finding.

At $n = 259$, a historical degree-12 root `16.60255251726339` is smaller than the
current side, but its own source cell says “Invalid due to micro-overlaps.”
The following fixed degree-8 packing has side `16.60257141234448`, which is larger than
the current record. These are different rows and neither improves the current bound.
At $n = 210$, invalid and fixed occurrences of the same algebraic pair retain their
separate flags instead of inheriting a neighboring row’s status.

## Findings Corrected

| Finding | Correction and regression |
| --- | --- |
| An isolating centre was truncated to 60 digits beside a $10^{-308}$ radius | Retain the full centre; exact endpoint and unique-root checks |
| A rational approximation could substitute for a radical exact form | Independently derive and match its exact minimal polynomial |
| Source identity could be bypassed with a longer decimal | Check source coefficients independently of reported precision |
| The same polynomial could select an alternate conjugate | Require the catalogue side and the certified root to agree |
| A linear root reached a logarithm of a zero second derivative | Handle exact linear roots explicitly |
| Decimal error bounds could round inward | Round certified bounds upward |
| Admission could transplant a polynomial to a different destination side | Recheck destination-side agreement before writing |
| Spaced equations or nearby thematic credit could be skipped/mixed | Parse all retained integer equations and delimit enclosing source cells |
| Invalidity was read from a preceding row | Preserve source flags per occurrence and classify each pair from its own cell |
| Saved modular hints could be treated as verdicts | Replay prime, squarefree and factor-degree constraints, with arithmetic overflow guard |
| Degree was inferred after state classification | Infer degree before selecting integer/rational state |
| Source quotations could become live Markdown/math | Render literal escaped quotations in HTML and Markdown |

Exact interior-sign comparisons are justified inside an already certified unique-root
interval with opposite endpoint signs.
They avoid repeated high-precision bisection without weakening ordering, equality,
endpoint or conjugate checks.
The initial register replay dropped to 31.67 s locally; the final corpus is larger and
receives its own validation measurement.

## Remaining Obligations

The
[plan’s complete bead map](../specs/active/plan-2026-10-06-exact-side-values.md#remaining-work-and-beads)
assigns all 54 numeric-only counts, seven missing/weak KKT seeds (six individual seed
lanes plus the claimed $n = 177$ lane), independent contact rederivations, exact radical
witnesses and optional $n = 83$ source-index counting.

Closed earlier beads claim eleven polynomial identifications and a generic contact
producer, but their referenced commits/output are absent from the delivered branch,
advertised remotes and registered local worktrees.
PR 403 contains four delivered commits; its originating Claude session is inaccessible.
`think-s6np` must recover or reproducibly rebuild those outputs before `think-ohhz`
admits any claim. The required upstream KKT inputs are digest-pinned but not retained.
This is a missing-delivery dependency, not a mathematical negative.

Source parsing, algebraic certification, geometric branch realization and global
optimality remain separate obligations.
No lower bound, verified upper bound, optimality status or verification rung moves in
this collection update.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
