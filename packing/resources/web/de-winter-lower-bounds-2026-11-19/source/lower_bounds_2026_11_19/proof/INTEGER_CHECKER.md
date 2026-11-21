# Independent center-coverage check

The C++ program verifies one direction by covering the center domain with closed rectangles. The Python wrapper expands the symmetric measure with rational arithmetic. A primitive’s stated mass is shared equally among eight images, including duplicate images. Coincident rectangles are combined.

Coordinates use a lattice spacing of 2⁻³⁰. The center domain is rounded outward. Each source rectangle has separate inward and outward bounds. Its density is rounded down to a multiple of 2⁻³², and its total mass to a multiple of M⁻¹, with M = 2⁴⁸. For a rational tangent t = a/b, the oriented core has directions proportional to (b²−a²,2ab) and (−2ab,b²−a²). The exact half-plane threshold is rounded inward on the integer grid.

When the core contains an entire outward-rounded rectangle at every center of a box, the rectangle’s rounded-down total mass counts throughout. At a single center, floating-point clipping proposes vertices of an intersection. A proposed vertex counts only after exact signed 128-bit tests place it inside the inward-rounded rectangle and the core. The convex hull of accepted vertices has exact integer area. A missing vertex or a discarded nonnegative rectangle weakens the bound. All positive contributions use integer containment or exact areas. The wrapper checks the product range for each rectangle. Corner mass estimates never exceed the rectangle’s mass, so the absolute contribution to any interpolation sum is bounded by the sum of the rectangle masses.

## From four corners to all centers

For one rectangle R let K(p) be its intersection with the core centered at p. If p = Σλⱼpⱼ for box corners pⱼ, Minkowski addition gives ΣλⱼK(pⱼ) ⊆ K(p), by convexity of both the rectangle and the core. The planar Brunn–Minkowski inequality implies

    sqrt(area K(p)) ≥ Σ λⱼ sqrt(area K(pⱼ))

when every corner intersection has positive area. The same applies to its mass after multiplying area by a constant nonnegative density. A rectangle with a zero corner lower bound may be omitted.

Write vⱼ for the integer floor of the square root of its certified corner mass in units of M⁻¹. For a nonnegative integer a, squaring and using (x−a)² ≥ 0 gives the lower bound Σ λⱼ(2avⱼ−a²) in those units. The checker chooses a separately for each rectangle. Summing over all rectangles leaves an affine combination of four totals. Its minimum is at least the smallest of these totals. If that minimum plus the inherited full-rectangle masses reaches M, the whole closed center box passes. Otherwise the longer coordinate interval is bisected. A budget limit or unproved leaf cannot return PASS.

Archived receipts give node counts, leaf counts and the smallest accepted integer mass bound. Full reproduction requires Python 3 and a C++17 compiler with signed 128-bit integer support.

Reference for Brunn–Minkowski: R. J. Gardner, “The Brunn–Minkowski inequality”, Bulletin of the American Mathematical Society 39 (2002), 355–405. https://doi.org/10.1090/S0273-0979-02-00941-2

## The triangular checker

The octagon-gram kernel splits each closed center box along a diagonal. Consider one triangle with vertices p₀, p₁ and p₂. For a fixed source rectangle R let aᵢ be the integer floor of the square root of its certified intersection mass at pᵢ, in units of M⁻¹. If all three intersection masses are positive, Brunn–Minkowski gives an intersection mass of at least (λ₀a₀ + λ₁a₁ + λ₂a₂)² at the center λ₀p₀ + λ₁p₁ + λ₂p₂. Here each λ is nonnegative and their sum is one. The inclusion follows by taking the same convex combination of intersection points in the stationary rectangle and translating octagon. A row with a zero lower bound contributes zero to this triangle.

Summing the outer products aaᵀ over rectangles gives a positive semidefinite integer matrix H. At every barycentric point λ, the variable part of captured mass is bounded below by λᵀHλ. For any test barycentric point z, positive semidefiniteness implies λᵀHλ ≥ 2λᵀHz − zᵀHz ≥ 2 minᵢ(Hz)ᵢ − zᵀHz. Floating point nominates several test points, which are rounded to nonnegative integer barycentric weights summing to 65,536. The final lower bound uses only integer arithmetic and rounds downward. The smaller of the bounds from the two triangles covers the center box. The checker may use whichever of the two diagonals gives the larger whole-box bound. Mass from rectangles fully enclosed throughout the box is added once.

For exceptionally fine angular subdivisions the checker can replace a large-denominator central half-angle tangent t with a nearby rational t′. If the nominal half-angle tangent bin has width h and begins at l ≥ 0, the angle error from the chosen center is at most (h + 2|t′ − t|)/(1 + min(t′,l)²). This follows from the derivative of 2 arctan. The verifier rounds that error upward before constructing the common octagon. Standard-size bins retain their original rational center.
