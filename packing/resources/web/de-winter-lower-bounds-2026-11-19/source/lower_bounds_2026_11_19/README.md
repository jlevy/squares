The newest results, their comparisons and the reproduction commands are in [FOLLOWUP.md](FOLLOWUP.md).

# Square packing improvements below 325 squares

This packet includes 34 direct rectangle-measure lower bounds and 71 lower bounds from new corner measures. The direct values are in `lower_bounds.csv`. The family values are in `corners/bounds.csv`. For the family results, the new corner argument is checked here and the original global coverage is inherited from Hosono’s reported T-180 result. See `corners/PROOF.md` for the exact change and verification scope.

Each row in `lower_bounds.csv` gives a lower bound on the least board side that can contain the indicated number of independently rotated unit squares. A larger lower bound rules out more board sizes. The exact comparisons in each case include the author's prior work and submitted issue 1039 where applicable.

## Why the certificates work

On the board of the claimed side, the certificate places a nonnegative rectangle measure with total mass strictly below the number of squares. Every contained unit square captures at least one unit of mass. The boundaries of these squares have measure zero, so a packing would use more mass than the measure contains. The same obstruction applies to smaller boards by containment.

The checker covers all orientations and centers. In an angle interval centered at orientation θ₀, bound its absolute angle deviation by σ. In the coordinates of θ₀ the octagon defined by |u| + σ|v| ≤ 1/2 and |v| + σ|u| ≤ 1/2 lies in every unit square of that interval centered at the origin. This follows from |sin t| ≤ |t| and |cos t| ≤ 1. The checker moves this octagon through every permitted center. Each cell passes once its certified lower bound for captured mass reaches one. It subdivides unsettled angle intervals and uses the reflection and quarter-turn symmetry of the measure. The integer area calculation and its Brunn–Minkowski interpolation argument are described in `proof/INTEGER_CHECKER.md`.

## Reproduce

Run `python3 verify.py` for the exact comparisons, measure construction, digests and complete coverage of the recorded angle intervals. Run `python3 verify.py --n 114 --replay --workers 4` to replay the strongest direct 114-square result. Run `python3 verify.py --replay --workers 4` to recompile the C++17 checker and repeat every center subdivision, including negative controls with quarter-strength weights. Python 3.10 or later and a C++17 compiler supporting 128-bit integers are needed for full replay. All source measures and the new per-angle receipts are included.

## Credit and benchmarks

Joost de Winter after Hiroaki Hosono. Hosono developed the source measure constructions. De Winter's earlier search packages developed and reweighted the rectangle measures and integer verifier. This continuation used Codex for numerical search, mathematical derivation and certificate construction. The per-case manifest identifies the input measure and its SHA-256. Original license notices are in `notices/`.

SquareMath revision 1015fc175fa4e2c01f912d915d784100e36d3bab. Local proof packets have not been submitted by this search.

- https://squaremath.org/frontier.html
- https://github.com/jlevy/squares/issues/1039
- https://github.com/wand125/square-packing

The command `python3 corners/verify.py --independent` also exercises a second implementation of the hardest reflected direction of each family.

## Packing upper bounds

The upper directory contains three-predicate rational verification of the smaller packing certificates in upper/improvements.csv. The comparison includes earlier private certificates. The changes there refine the numerical sides of existing layouts. Upper bounds that change only beyond twenty decimal places appear in upper/precision_only.csv when present. Coordinates, credit and license are included.

The constructions directory rebuilds the winning central-strip measures with rational arithmetic from their original sources.

A ranked table of all direct improvements and the provenance of the leading result is in RESULTS.md.
