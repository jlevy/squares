# Fibonacci Torus Source Review

Searches on 7 October 2026 (Pacific time) did not locate a full public manuscript titled
*The Fibonacci Geometry of Eleven Squares*. The supplied first page attributes it to
“PINGYOU LTD.” Its publication date, version, bibliography, author identities and proof
contents remain unverified.
Exact-title, title-fragment, author/title, distinctive-term, arXiv and Zenodo searches
returned no matching manuscript.
This is a retrieval result, not evidence that the manuscript does not exist.
No correspondence was sent.

## The Torus Precedent and Its Boundary Limitation

Andrew V. Reztsov and Ian H. Sloan, *On 2D packings of cubes in the torus*, *Proceedings
of the AMS* 125(1), 17–26 (1997), [DOI](https://doi.org/10.1090/S0002-9939-97-03930-0),
supplies a directly relevant precedent.
The complete journal text is readable in
[Sloan’s author upload](https://www.researchgate.net/publication/239919977_On_2D_packings_of_cubes_in_the_torus).
The AMS article and PDF returned HTTP 403; the direct ResearchGate PDF was unavailable.

Theorem 1.1 concerns axis-parallel squares of side $1/\lambda$ in the standard unit
torus, with pairwise intersection area zero and $\lambda>2$:

$$N_2(\lambda)=\lfloor\lambda\lfloor\lambda\rfloor\rfloor.$$

The upper bound permits arbitrary centres; a cyclic lattice attains it.
Section 4 uses $F_1=F_2=1$ and centres $(k/F_\ell,\{kF_{\ell-2}/F_\ell\})$. For
$\ell=2t+1$, their maximal square side is $F_{t+1}/F_{2t+1}$. The relative count deficit
against $N_2$ at that side tends to $\alpha^2/(1+\alpha^2)=0.276393\ldots$, where
$\alpha=(\sqrt5-1)/2$. The text identifies $\ell=5$, $F_5=5$ as the sole extremal
Fibonacci lattice. These statements concern that particular lattice family and norm, not
the supplied manuscript’s quotient rings.

**Consequence derived here:** after scaling, square tori admit eleven unit squares at
side $11/3$, and seventeen at $17/4$. Each finite square-container packing periodizes,
so the torus problem is a necessary relaxation.
These feasible torus examples put a ceiling on any lower bound obtained solely by
proving that relaxation infeasible.
They lie below both current finite-container targets.
An independently rotating torus model includes these axis-parallel examples and inherits
the same obstruction.

A useful torus reduction must therefore preserve additional information: the existence
of two perpendicular seams that avoid all square interiors, the effects of cutting
objects at those seams, or a proved restriction on which periodic configurations can
arise from near-optimal bounded packings.
A labeling or arithmetic identity alone does not supply this implication.

## Erdős #106: Formulation, Prior Work and Current Reports

| Primary source | What it supports | Limitation |
| --- | --- | --- |
| [Erdős–Graham, 1975, author PDF](https://www.math.ucsd.edu/~ronspubs/75_06_squares.pdf), printed p. 120 | The conjecture concerns the maximum **total perimeter of arbitrary-sized squares** inside a unit square: $F(k^2+1)=4k$. Dividing by four gives the modern side-sum form $f(k^2+1)=k$. The authors attribute it to Erdős roughly forty years earlier and credit Newman for $k=2$ by personal communication. | Their asymptotic construction does not disprove the $k^2+1$ conjecture. |
| [Baek–Koizumi–Ueoro, arXiv:2411.07274v2](https://arxiv.org/abs/2411.07274v2), submitted/revised November 2024 | Proves the side-sum conjecture when all squares are parallel to the container; determines the more general axis-parallel extremal function. | Does not cover independent rotations. |
| [Sprite143’s construction repository](https://github.com/Sprite143/erdos-106-counterexample) | Reports seventeen unequal squares, sixteen axis-parallel and one tilted, with exact side sum $2190452873/547596200>4$. Provides rational data and separate separating-axis and clipping verifiers. | The inspected README calls it a candidate awaiting human refereeing. Its code was not executed in this source review. |
| [John Seamons, Zenodo 21938978](https://zenodo.org/records/21938978), v2, 14 August 2026 | Reports an independent $k=5$, $n=26$ rational construction with side sum $4471148/894225>5$; acknowledges Sprite143’s earlier $k=4$ construction. | Private-review and independent-discovery statements are the author’s reports. The package was not replayed here. |
| [Community database, current raw data](https://raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml), row 106 | Retrieved data labels the problem “disproved (Lean)”. | Its dates remain 2025-08-31 and its separate `formalized` field says `no`. Those metadata do not establish the proof, date or attribution. The live Bloom page and forum returned 403; the searchable June 2026 copy still says open. |

The supplied manuscript’s rational-counterexample claim could be a separate
construction, a rediscovery, or an account of prior work.
Its unseen bibliography and witness are needed to distinguish these possibilities.
No retrieved source connects PINGYOU LTD to the two constructions above.
The shared number seventeen does not identify the same optimization problem as seventeen
congruent unit squares in the smallest square.

## Exact Algebra and Methods That Can Transfer

[Walter Trump’s three-page author manuscript](https://trump.de/square-packing/Packing-11-squares.pdf)
is dated 27 February 2023, updated 5 March.
It documents the 1979 incidence construction, the angle calculation and side
$3.8770835900228141773\ldots$, and claims rigidity within that arrangement.
Its angle equation is already algebraic of degree eight.
The public text does not establish the supplied manuscript’s claimed Galois group or a
Fibonacci origin for the endpoint.
The repository’s [n11 record](../../../packing/frontier/n-011.md) separately registers
global optimality;
[H-265](../../../packing/campaign/hypotheses/H-265-n17-catalogue-polynomial-identity.md)
already identifies the certified n17 endpoint with the irreducible degree-18 catalogue
polynomial. Repeating elimination alone would not advance either global proof.

The following priorities are research judgments, not results established by these
sources. They retain
[X-048’s](../../../packing/campaign/explorations/X-048-n17-optimality-after-n11.md)
emphasis on checked occupancy, compatibility and terminal capture.

| Priority | Transferable mechanism | Necessary bridge or falsifier |
| --- | --- | --- |
| 1 | Record seam and wall incidence alongside periodic displacement labels; derive a relation between two or more square domains. | Must preserve every bounded packing in the declared parent and remove a checked region that the current unary relaxation admits. Test the $11/3$ and $17/4$ torus examples as controls for omitted seams. |
| 2 | Use finite-field pair orbits to compress an already justified geometric constraint system. | Every group action must preserve the metric, square orientations, walls and all constraint colors, or carry them covariantly. A label permutation that changes an inequality invalidates that quotient. Count reduction without geometric pruning is only an efficiency result. |
| 3 | Use contact graphs and exact active-constraint matrices to organize local charts and terminal capture. [Borcea–Streinu–Tanigawa](https://arxiv.org/abs/1110.4660) gives generic periodic body-and-bar rigidity criteria. | Squares have unilateral contacts and special, nongeneric geometry. Generic bar counts cannot replace exact one-sided cones. A complete normalized representative theorem must precede a global contact census. |
| 4 | Use algebraic elimination after a geometrically necessary contact pattern has been isolated. | Retain real-root intervals, SAT branch signs, wall inequalities and a complete cover of alternatives. An eliminant or Galois group without that cover identifies candidates only. |
| 5 | Use periodic cell deformation to generate constructions. [Kallus–Elser–Gravel](https://arxiv.org/abs/1003.3301) incorporates cell parameters into divide-and-concur search. | The repository already surveys this mechanism. Accept only a new certified bounded packing or a measured useful boundary-aware seed; a denser periodic cell alone does not improve the target. |
| 6 | Use translation-surface or cut-and-project descriptions to propose orientation and contact families. | Require an explicit reconstruction preserving congruence, nonoverlap and containment, then a necessity theorem if used for lower bounds. Until then these are family generators, with no demonstrated global implication for n17. |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
