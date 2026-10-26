# C702: continuous reductions of the common-line configuration

All labels below refer to the twelve actual owners in the original C702 order

\[
(1,2,12,16,32,192,256,1536,6144,8192,16384,32768).
\]

Write O=Q₀, V=Q₁, K=Q₅, A=Q₆, W=Q₇, N=Q₈, I=Q₁₀ and T=Q₁₁. The two northeast singleton owners are Q₃ and Q₄. All owned points are strict, all squares have side a>1 and disjoint open interiors, and every wall used is a real wall of [0,4]².

## 1. The only surviving auxiliary alternative

Theorem A in `MERGED-RIGHT-PATTERN-4.md` gives

\[
(1.95,1.95)\in A.
\]

Its owned anchors are A's (1.65,1.65),(2,1.74),(1.74,2). The four excluded points (1,1.65),(1,1.74),(1.65,1),(1.74,1) belong to V or O, respectively, by their established strict singleton segments.

Theorem 11 in `OTHER-GEOMETRY.md` then proves that W must strictly own F₅=(2,2.26). If it excluded F₅, its owned vertical marker pair and the four excluded endpoints F₄,F₅,F₈,F₉, together with the excluded actual marker (3.086,2), would force (1.95,1.95) into W as well. The owners of F₄,F₈,F₉ and the marker are A,I,Q₄,I. This contradicts the disjointness of A and W.

Thus only W's exact auxiliary label 65568 remains. The other variable auxiliary owners A,N,T retain respectively their labels 8208,2050,16392, without F₅. No auxiliary covering assumption is used.

## 2. The merged square owns an additional inward point

Apply Theorem A after the half-turn (x,y)↦(4−x,4−y), now to W. Its three strict anchors (2.35,2.35),(2,2.26),(2.26,2) become the theorem's southwest anchors. The theorem's four foreign points map back to

\[
(3,2.35),\quad(2.26,3),\quad(2.35,3),\quad(3,2.26).
\]

The first and fourth belong to the actual right-top singleton Q₄, whose strict segment contains {3}×[2.26,2.88]. The second and third belong to the actual top-right singleton Q₃, whose strict segment contains [2.26,2.88]×{3}. They are distinct from W. The all-angle conclusion is therefore

\[
(2.05,2.05)\in W\quad\text{strictly}. \tag{1}
\]

This step requires neither the side cap a≤1.001 nor any orientation assumption.

## 3. Actual top and left wall advances

Theorem 4 of `C981-WALL-CYCLES.md` applies to T under

\[
(X,Y)=(4-y,4-x).
\]

The exact data are:

| Standard wall datum | Original point | Actual owner |
|---|---|---|
| Owned (.914,2) | (2,3.086) | T |
| Owned (1,2.4) | (1.6,3) | T |
| Excluded (1,1.74) | (2.26,3) | Q₃ |
| Excluded (.76,1.87) | (2.13,3.24) | Q₃ |
| Excluded (1.65,2.35) | (1.65,2.35) | N |

The actual top wall y≤4 becomes X≥0. The theorem gives (X,Y)=(1,2.8), hence

\[
(1.2,3)\in T\quad\text{strictly}. \tag{2}
\]

The older all-angle wall-reach theorem, retained in the original common geometry, applies to the actual merged square N. It owns (.914,2),(1,2.4), and excludes (1,1.74) in V and (1.74,2) in A. Its real wall is x≥0. The resulting strict point is

\[
(1,2.56)\in N. \tag{3}
\]

Merging the northwest marker into N does not invalidate this application: the older wall theorem's two excluded points are exactly the two displayed points, and neither is owned by N. Its exact parameter checks are .82<14/17, .74²+.26²<1, and .56²+.74²<1.

## 4. Two further points of the paired northwest corner

The actual paired corner K owns (1,3) by the established corner theorem. Use (2) and (3) as genuine foreign points for Theorem 5 of `OTHER-GEOMETRY.md`.

For the horizontal completion, take local coordinates (ξ,η)=(1−x,y−3). The strict point (1,3) becomes the origin, T's (1.2,3) becomes (−.2,0), and N's (1,2.56) becomes (0,−.44). The actual top wall becomes η≤1. Set q=.2,p=.44,r=.6. The three exact checks are

\[
p^2+q^2=.2336<1,\qquad p^2+r^2=.5536<1,\qquad q+r=.8<2\sqrt2-2.
\]

Therefore

\[
(.4,3)\in K\quad\text{strictly}. \tag{4}
\]

For the vertical completion, take (ξ,η)=(y−3,1−x). The same origin is used; N's point becomes (−.44,0), T's point becomes (0,−.2), and the actual left wall becomes η≤1. Set q=.44,p=.2,r=.38. Then

\[
p^2+q^2=.2336<1,\qquad p^2+r^2=.1844<1,\qquad q+r=.82<2\sqrt2-2.
\]

This gives

\[
(1,3.38)\in K\quad\text{strictly}. \tag{5}
\]

In particular K supplies the full strict segments [.4,1]×{3} and {1}×[3,3.38], while T supplies [1.2,1.74]×{3}. Each segment is attributed to its one actual owner.

## 5. Complete continuous exclusion

The reductions above leave a single actual auxiliary configuration. It is now excluded by two strict-point theorems:

| Actual square | Completed theorem | Forced strict point |
|---|---|---|
| A=Q₆ | Theorem 1 in `C702-DUPLICATE-POINT.md` | (1.30,1.93) |
| N=Q₈ | Theorem N in `C702-N-STRICT-POINT.md` | (1.30,1.93) |

The A theorem uses its genuine strict central marker, elbows and crosspoints, the actual O/V singleton supports, the foreign central markers, and the entire segment from (2.05,2.05) to (2.35,1.65) in W. The new W point is established in Section 2 above.

The N theorem uses its original two markers and owned (1,2.26), the strict A crosspoint (1.5,2), the actual V segment from (.76,1.87) to (1,1.74), the paired northwest corner point (1,3), and the full top segment [1.2,1.74]×{3} in T. Section 3 above supplies the new endpoint (1.2,3). Every exclusion comes from its identified actual owner.

The same point therefore lies strictly in two distinct actual open squares, contradicting their disjoint interiors. **This completes the exclusion of the original C702 family, including every auxiliary alternative.** Both point theorems cover every orientation and permitted tangency, with no angle subdivision or numerical enclosure.

The older N wall advance and both additional K completions in Sections 3–4 remain valid reusable consequences. The final duplicate-point contradiction needs the new W point and the top-wall completion, but does not need those additional reaches. The two outer long-chord conclusions from Theorems 1 and 2 of `OTHER-GEOMETRY.md` also remain valid; the duplicate point completes the case without a further central chord estimate.
