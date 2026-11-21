# Small additional gains from thin edge strips

The reference is the original archive posted on [issue 1039](https://github.com/jlevy/squares/issues/1039). Each row uses its stated orientation coverage and exact transfer, together with the spare mass of its certificate. All strip estimates below hold for arbitrary orientations.

Write S for the side proved in the source, u for its transfer scale and m for its margin. Let μ be its eightfold symmetric rectangle measure on the L-board, where L = uS + 2m. Pull back the measure restricted to the central square by the map x ↦ ux + (m,m), obtaining a measure ν on the S-board. Every unit square contained there captures mass at least one. Indeed, the transfer in the source places a certified core inside its image. The weight of each stored source rectangle is the total weight across its eight copies. The central crop has the same dimensions in all copies up to interchange.

Let M be an upper bound on the total mass of ν. For a source rectangle of weight w and original dimensions a and b, write d = w/(ab). Let A and B be its clipped side lengths in the central source square. Its contribution to M is dAB. In the pulled-back measure, its rectangles have dimensions A/u and B/u, and their eight densities sum to u²d. Copies with zero clipped area can be omitted.

For any unit square Q and its concentric square ρQ of the same orientation and side ρ, the discarded part lies in four edge strips of width (1−ρ)/2 each. Every straight slice of a rectangle has length at most its diagonal, which is at most the sum of its side lengths. Integrating along slices perpendicular to each edge gives

    ν(Q) − ν(ρQ) ≤ C(1−ρ),    C = 2u Σ d(A+B).

The computation rounds each term of C upwards to a multiple of 10⁻⁹ and the total M upwards to a multiple of 10⁻¹⁸. The input weights and all arithmetic are rational.

For a proposed count n with M < n, take ρ = 1 − (999/1000)(n−M)/(nC). Let R = 1.414213562373096, whose square exceeds two, and T = R + (S−R)/ρ. Suppose n unit squares could fit in T. Contract the board around its center by ρ and center it in the S-board. This leaves margin (1−ρ)R/2 on each side. Around each contracted tile put a concentric unit square at its original orientation. Its added half-width on either coordinate is at most (1−ρ)√2/2, so each such unit square fits in S. Each contracted tile must therefore cover mass at least 1−C(1−ρ). Their interiors are disjoint, their boundaries have zero mass, and together they would capture strictly more than M. This contradiction proves s(n) ≥ T. The table rounds T down to 18 decimal places.

Run `python3 followup/mass_reserve/verify.py` to regenerate every claim from the attached source and check the comparisons against other results in this archive. Its SHA-256 is pinned in the verifier. The original source includes its own full verifier. Extract the inner `lower-bounds-56.zip` and run its `verify.py` to check the inherited orientation certificates and transfers.
