# Proof status: 6, 10, 13, 22, and 33 squares

The complete minimum-side theorems are checked for **all five square counts**:

- `SquarePackingArchive.Records.Square6.s6_eq_three : IsMinimumSide 6 3`.
- `SquarePackingArchive.Records.Square10.s10_eq_goebel : IsMinimumSide 10 (3 + Real.sqrt 2 / 2)`.
- `SquarePackingArchive.Records.Square13.s13_eq_four : IsMinimumSide 13 4`.
- `SquarePackingArchive.Records.Square22.s22_eq_five : IsMinimumSide 22 5`.
- `SquarePackingArchive.Records.Square33.s33_eq_six : IsMinimumSide 33 6`.

The initial configurations and geometric lemmas cover arbitrary rotations. The
packing arguments start with interior-disjoint squares; where a proof needs
closed-disjoint squares, an explicit scaling theorem supplies them.

The integrated theorems are included in `formal/SquarePackingArchive/Audit.lean`.
Their axiom checks allow only `propext`, `Classical.choice`, and `Quot.sound`.

## Why six squares need side three

The checked proof follows Stromquist's nine-point argument. An eight-point
perimeter set ensures every square contains a point other than the center.
Geometry prevents adjacent perimeter points from being the sole points of two
different squares. A finite counting argument then forces one square to contain
exactly the center and one neighboring point.

After a rotation or reflection, that square must contain four points of a
second, eight-point unavoidable set. Only four points remain for the other five
squares, a contradiction. The proof handles arbitrary rotations and touching
squares: a hypothetical packing with side below three is first transformed into
a closed-disjoint family fitting side three.

The final theorem is in `formal/SquarePackingArchive/Records/Square6Exact.lean`.

## Why ten squares need side 3 + √2 / 2

The proof follows Stromquist's point-ownership argument. An initial ten-point
unavoidable set assigns a different point to each square in a hypothetical
smaller packing. Replacement configurations force the four side squares to
contain points on eight specified segments.

For any choice of those eight points, Lean proves that they, the four corner
points, and the center form an unavoidable set. The eight boundary points belong
to the four side squares; the four corner points belong to four other squares.
Only the center remains for two squares, contradicting disjointness.

The proof checks all eight segment parameters independently. Its triangle
coverage and boundary arguments handle arbitrary rotations. The fixed
replacement configurations include both rotated inner points, with their
ownership proved separately.

The rotated inner points also appear in
[Stromquist's October 1984 manuscript](https://walterstromquist.com/papers/squares1.pdf).

The final theorem is in `formal/SquarePackingArchive/Records/Square10Exact.lean`.
The [generated coverage proofs](generated-geometric-covers.md) are reproducible
and checked by Lean, not trusted as external certificates.

## Why thirteen squares need side four

The proof follows Bentz's point-set and counting strategy. The initial
sixteen-point set forces two corner-restricted squares. Replacement lemmas
then give points owned by those squares. In every adjacent or non-adjacent
case, a further unavoidable set has too few points left for the other squares.

Lean checks 32 non-adjacent and 13 adjacent coverage certificates. The proof
uses corrected auxiliary point sets and an eight-point replacement grid for
the moving point in case R1. The
[13-square formalization notes](bentz-13-formalization.md) explain the changes
and include exact counterexamples to two printed auxiliary sets.

The final theorem is in `formal/SquarePackingArchive/Records/Square13Exact.lean`.

## Layouts

Every catalogued square count has coordinates in the viewer. Grid constructions
are generated from manifest recipes; the 5- and 10-square constructions use exact
numbers in Q(√2). Every generated layout is checked for containment and pairwise
non-overlap using exact arithmetic during the archive build.

An uncatalogued count displays a labelled **basic grid bound**, not a best-known
record. `gridBaseline` in the manifest supplies the common proof and supported
range. The matrix shows a Lean-verified upper bound; the viewer uses the same
grid size and links to `Records.GridBounds.grid_hasPacking`. The generated Lean
audit checks each integer instance. These bounds remain outside the historical
claims and do not change record counts or exact-coverage graphs.

## Sources

- Walter Stromquist, [Packing 10 or 11 Unit Squares in a Square](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8).
- Wolfram Bentz, [Optimal Packings of 13 and 46 Unit Squares in a Square](https://doi.org/10.37236/398).
- Wolfram Bentz, [Optimal Packings of 22 and 33 Unit Squares in a Square](https://arxiv.org/abs/1606.03746).
