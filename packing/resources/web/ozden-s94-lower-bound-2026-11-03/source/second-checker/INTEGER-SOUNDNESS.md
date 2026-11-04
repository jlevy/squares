# Independent integer verifier

The decisive implementation is `independent.py` (exact preparation and independent rational clipping oracle) plus `intcheck_final.cpp`. The other C++ files are retained development experiments. No claimant geometry or preparation code is imported by these implementations. The claimant's preparation code is imported only by the separate adversarial test of its own checker.

## Representation and admission

Set S = 2^42. An integer v denotes v/S. The front end uses Python `Fraction` for JSON values, admission, D4 expansion, densities, rational directions and centre domains. It checks both shrink conditions, all other mathematical premises, and the implementation limits below. All lower rectangle coordinates are rounded up, upper coordinates down, and densities down. Thus the represented measure is a pointwise lower measure. Each original orbit is expanded by four rotations of the representative and four rotations of its diagonal reflection, with density w/(8 area), including coincident copies.

The core half side H/S is rounded down from B/2. Its direction is *not* approximated: c=C/D, s=T/D, C²+T²=D². The centre domain is expanded by taking floor(S L/2) and ceil(S U). The integer midpoint and the larger distance to each endpoint describe a box containing its entire interval. Children [lo,mid] and [mid,hi] cover their parent.

The rounded lower measure need not itself retain exact D4 symmetry. Symmetry is used only for the original exact measure: the lower measure proves coverage on the quadrant, and invariance of the original measure then transfers that coverage to all required centres and reflected orientations.

## Geometry

For r>0 the vertical section of the intersection of [x,X]×[y,Y] with the rotated rectangle of half sides a,b has signed length

    eta(z) = min(Y, (aD-Cz)/T, (bD+Tz)/C)
           - max(y, (-aD-Cz)/T, (-bD+Tz)/C).

This is a concave function: it is the minimum of the nine pairwise upper-minus-lower affine functions. At any integer abscissa the implementation rounds each upper expression down and each lower expression up. The resulting signed integer length is a lower bound for eta. Between consecutive abscissae the chord joining those lower values is below eta, by concavity. Therefore the integral of max(0,eta) is at least the chord's integral whenever that integral is positive, and at least zero otherwise. The implementation sums these positive trapezoids, rounding each area down to units 1/S. The chosen abscissae are endpoints, rounded square vertices and rounded crossings with horizontal rectangle edges; their accuracy is irrelevant to the inequality. A bounding-box crop is a superset of the rotated rectangle and does not change its intersection with the axis rectangle. At r=0 the overlap product is computed directly, rounded down.

For a vertical or horizontal rectangle edge the same slab inequalities give an interval of parameters. Rounding its upper end down and lower end up gives a lower length; the opposite roundings give an upper length. Empty intervals contribute zero. The axis case is handled directly. All quantities and comparisons are integers, including signed floor division.

## Bounds over a centre box

If the box radii are dx,dy, the code takes bu=ceil((C dx+T dy)/D) and bv=ceil((T dx+C dy)/D). The eroded rotated rectangle at the midpoint with half sides H-bu,H-bv is in every translated core; the dilated one with H+bu,H+bv contains every translated core. Rectangles certified inside every core are replaced by a rounded-down constant mass. Rectangles certified disjoint from every core are dropped. Both classifications are exact integer slab tests; an additional exact axis bounding-box disjointness test is used. The remaining rectangles form the boundary list.

For translation in x, the derivative of overlap area is left-edge length minus right-edge length, almost everywhere; for y it is bottom minus top. Lower lengths in the eroded core and upper lengths in the dilated core give signed intervals enclosing these derivatives over the entire box. Densities multiply the interval endpoints with directed integer rounding. Summation and max(abs(lower),abs(upper)) give Gx,Gy, rounded upward. Thus

    F(p) >= F(midpoint)_lower - ceil(Gx dx/S) - ceil(Gy dy/S).

This follows by integrating the bounded derivatives along horizontal and vertical segments inside the box. The overlap function is Lipschitz. The erosion area gives a second lower bound. Their maximum is a lower bound.

If a line is exceptional for an almost-everywhere derivative statement, the same endpoint inequality follows by continuity from nearby lines. The finite rectangle densities ensure the required Lipschitz continuity.

Derivative bounds from a parent remain valid in a child. New inside rectangles have zero derivative throughout that child, and newly dropped rectangles have zero contribution there. Replacing inside mass by a smaller constant changes no derivative. Hence the child's reduced function has the same derivatives as the parent's on the child. Each axis may use the smaller of its own and its inherited bound. No arbitrary deletion is used with this inheritance argument.

A box is accepted only if its integer lower bound is at least S. All other terminating conditions refuse. A VERIFIED direction means every leaf was accepted. No sampled point alone can accept a direction. Floating point appears only in CPU-time formatting.

## Exact division and overflow limits

The final optimized floor division handles denominators S and 2S by arithmetic right shift on this Apple clang/ARM target. For b=C,T,D it precomputes R=floor(2^64/b) using integer division. For nonnegative a it computes q=floor(aR/2^64), then adds floor((a-qb)/b) using a 64-bit division. This is exactly floor(a/b): the first quotient never exceeds it, and the residual correction supplies precisely the missing quotient. For negative a it negates the quotient and subtracts one when there is a nonzero remainder.

The admitted experiment has L<10, B<1, precisely Dnet=83/120000 and indices 0..599, maximum expanded density <2^16, and sum of expanded density times vertical rectangle edge length <2^14 (the horizontal sum is equal by D4). These are checked exactly by the front end. In a root or descendant box dx,dy<2.5S, bu,bv<4S, and all rectangle offsets have magnitude <10S. The numerators passed to non-power-of-two division have magnitude <2^82. Positive divisors C,T,D are <2^35 and >2^24; T=0 is handled separately. Thus R<2^40, aR<2^122, and the residual before the 64-bit division is <2^54. Both signed and unsigned 128-bit intermediates are safe, and the residual cast to 64 bits is exact. These division results are <2^58 in magnitude. Weighted area and penalty products are below 2^110. The signed derivative sums, including rounding by at most one unit per term, are below 2^57; centre/inside mass sums are below 94S plus an inconsequential integer bound. All stored signed 64-bit values are safe. At fixed-point area nodes, only positive chord sums contribute, and these are bounded by twice the rectangle section height; negative intermediate lengths also fit comfortably in 64 bits.

`division_test.cpp` checks 599,800 signed floor divisions across all 600 directions against direct signed 128-bit division. `test_kernels_final.py` compares 2,500 area lower bounds and both edge-length intervals with independent exact rational polygon clipping and exact rational slab clipping, including axes, very thin rectangles and the endpoint direction. These tests support the implementation audit; the inequalities above carry the proof.

In particular, the coarse upper bounds on 128-bit weighted products do not by themselves justify their 64-bit quotients: those quotients fit because each weighted rectangle mass is at most its original orbit mass divided by eight, and the sum is below 94. Derivative quotients fit by the independently checked global density-times-edge-length bound; each interval endpoint adds at most one grid unit of rounding per term. These sharper bounds justify every cast after a power-of-two division as well.

## Reproduction

From the grading directory, with the supplied Python environment:

    clang++ -std=c++17 -O3 -mcpu=native -Wall -Wextra -o work/intcheck_final work/intcheck_final.cpp
    python3 work/exact_audit.py
    ./work/intcheck_final work/full.txt > work/full.jsonl

Only one computation runs at a time. Check that the output has exactly the requested indices once each, and that every verdict is VERIFIED. A truncated or partly refused output is not a certificate. `exact_centres.json` and `mutant_results.json` retain the independent exact point evaluations; these are evidence about values, separate from the whole-domain verification.
