# Packings of unit squares in a square, n > 324

Nineteen packings of n unit squares in a square, each with a smaller side than the value recorded by [the Squares Project](https://jlevy.github.io/squares/) on 17 October 2026. From n = 509 to n = 1568, each packing fits in a square of side below the integer ⌈√n⌉, where the record was the integer grid.

| n | side, rounded up | Squares Project, 17 October 2026 |
|---:|---|---|
| 464 | 21.988813022694 | 21.989992144499 (Francisco Couzo) |
| 509 | 22.994328036438 | 23 |
| 555 | 23.993653790591 | 24 |
| 603 | 24.995268064197 | 25 |
| 654 | 25.996103908965 | 26 |
| 706 | 26.998712100405 | 27 |
| 760 | 27.995949340329 | 28 |
| 817 | 28.998488480775 | 29 |
| 875 | 29.998783733108 | 30 |
| 935 | 30.995955854834 | 31 |
| 998 | 31.998349747355 | 32 |
| 1061 | 32.996048342114 | 33 |
| 1128 | 33.998294117981 | 34 |
| 1196 | 34.998294118334 | 35 |
| 1266 | 35.996046404219 | 36 |
| 1339 | 36.997865207179 | 37 |
| 1413 | 37.999463832123 | 38 |
| 1489 | 38.997600184483 | 39 |
| 1568 | 39.999336626159 | 40 |

## Files

- `nNNNN.json`: centre (x, y) and counter-clockwise angle in degrees of each unit square; the container is [0, side]².
- `nNNNN.cert`: exact certificate. Line 1 gives n and the side; each further line gives x, y and t = tan(angle/2), all rational.
- `check.py`: exact checker that uses only the Python standard library, run as `python3 check.py *.cert`.
- `records.txt`: the sides and the recorded values.
- `before_after.svg`: each packing beside the record it improves.

## Verification

`check.py` accepts all 19 certificates: every corner lies inside the container, and every pair of nearby squares is separated along an edge normal, decided in exact rational arithmetic. The printed coordinates in the JSON files pass the same test at 80 digits. The smallest clearances lie between 10⁻³⁵ and 10⁻¹¹.

## Construction

The packings use the staircase-rectangle and four-block method of Arslanov, Mustafin and Shangitbayev (Electronic Journal of Combinatorics 28(4), P4.22, 2021): two compressed tilted components and two aligned grids. The n = 464 packing also uses a six-square patch transferred from the n = 422 construction.

## AI assistance

The numerical search and refinement were performed with GPT-6 Astra under the direction of Joost de Winter. The certificates and checks were produced with Claude (Anthropic).

## Licence

All files in this folder are released under the MIT licence (see `LICENSE`).

Joost de Winter, Delft University of Technology
