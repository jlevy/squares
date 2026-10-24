# Friedman unavoidable-point formalization

The formal layer models both forms of an unavoidable-point argument. A closed
unavoidable set pierces every unit square in the target container. Scaling the
container and point set proves that the corresponding points lie in square
interiors at every strictly smaller side length. A finite pigeonhole theorem
then bounds a packing by the number of piercing points.

Lean checks this reduction in `SquarePackingArchive.Unavoidable`, including the
strict inequalities introduced by scaling. No discretization or numerical
tolerance is involved.

The geometric layer covers the three ingredients used by Friedman's proofs of
`s(5)` and `s(8)`. The corner lemma normalizes arbitrary frame signs by quarter
rotations and checks inverse frame coordinates algebraically. The side-strip
lemma excludes every way both adjacent piercing points could lie outside a
rotated square. The reusable triangle theorem proves Friedman's Lemma 3: when
the center lies in a triangle whose three sides have length at most one, the
square contains a triangle vertex. Its proof classifies points by the four
closed regions cut out by the square diagonals, derives an opposite pair from
the barycentric center equation, and closes the metric contradiction exactly.

The corner and side-strip lemmas are parameterized rather than tied to the
four-point example. A corner target may have any coordinates at most one. A
side strip carries its row origin, height, gap, and a frame inequality that
can be discharged exactly for the rational grids used by later historical
claims. This shared interface is intended for the `s(8)`, `s(15)`, `s(24)`,
and `s(35)` unavoidable configurations.

Lean partitions the container center region into four corners, four side
strips, and two central triangles. The four points at the corners of the
central square are therefore unavoidable. Scaling and finite pigeonhole give
the matching lower bound for five squares. Together with the separately
verified Göbel construction, this proves
`IsMinimumSide 5 (2 + Real.sqrt 2 / 2)` without numerical tolerances.

For `s(8)`, Lean checks Friedman's seven rational piercing points at
`(0.9,1)`, `(1.5,1)`, `(2.1,1)`, `(1.5,1.5)`, `(0.9,2)`, `(1.5,2)`, and
`(2.1,2)`. The proof exhaustively partitions every possible center into four
corners, six perimeter strips, and six internal triangles. The unavoidable
set and finite pigeonhole theorem give `IsLowerBound 8 3`; the ordinary
three-by-three grid with one square removed supplies the matching packing.
Thus `SquarePackingArchive.Records.Square8.s8_eq_three` kernel-checks the exact
historical result.

The formal geometry library also checks Friedman's Lemma 4. A unit square
whose center lies in a `1 × 0.4` rectangle contains one of the four rectangle
vertices. The proof normalizes the frame orientation and exhausts the 81
possible triples of escape directions for the four vertices. Translation
invariance is proved separately, so the theorem applies to such a rectangle
at arbitrary real coordinates. This is the additional geometric ingredient
needed by Friedman's historical `s(15)=4` construction.

The `s(15)` formalization now includes the fourteen rational historical points
and all ten interior triangles, reduced by horizontal and vertical
reflections to three barycentric base cases. The two remaining central cells
are discharged by the translated rectangle theorem. This proves coverage of
the full inner square `[1,3]²`. The perimeter partition is now complete as well:
the bottom edge uses gaps `0.6, 0.8, 0.6`, and the left edge uses gaps
`0.8, 0.4, 0.8`. The side-strip inequality handles all these gaps for every
frame, while the corner lemma covers the four corners. Exact index permutations
transport both edge arguments to the opposite sides. The resulting unavoidable
set yields `IsLowerBound 15 4`; the grid construction proves the matching upper
bound, completing `SquarePackingArchive.Records.Square15.s15_eq_four`.

For `s(24)`, the formalization uses Friedman's twenty-three rational points
from Theorem 5. Eight base triangles and exact index permutations cover the
interior by reflections; the shared boundary-pair theorem covers the side
strips, and the corner lemma completes the partition. The resulting
`SquarePackingArchive.Records.Square24.s24_eq_five` proves `IsMinimumSide 24 5`.
