# Joost de Winter’s Nineteen Packings Beyond 324, 17 October 2026

This packet retains the exact rational certificates behind
[issue #666](https://github.com/jlevy/squares/issues/666): nineteen packings of n unit
squares in a square beyond this project’s case corpus, at n = 464 and at eighteen counts
from 509 to 1568.
It records source custody. The exact replay is described below.

## Source, Licence and Dates

| Field | Value |
| --- | --- |
| Repository | [JoostdeWinter/joostdewinter.github.io](https://github.com/JoostdeWinter/joostdewinter.github.io), folder `square-packing-above-324` |
| Retained revision | `643dc9ad4d3dbd71a9a05558c7f6116b809ba930`, committed 2026-10-17T14:27:33Z |
| Issue pin | `b3152f526f23bc3ae450e51b6e906841233086d1`, committed 2026-10-17T07:03:15Z; issue #666 was opened at 07:06:07Z |
| Licence | MIT, copyright 2026 Joost de Winter, added in the retained revision; [LICENSE](source/square-packing-above-324/LICENSE) retained |
| Retrieval | See the [acquisition record](acquisition/sources.json) for the exact UTC retrieval time |
| Custody | [Declaration](acquisition/declaration.json), [SHA-256 manifest](acquisition/upstream-subtree.sha256) |

The issue pin and `b9cdc16` carry the same folder tree, `83563a8b35cb`.
The retained successor `643dc9a` adds only `LICENSE` and four lines of `README.md` to the
folder, which release all of its files under the MIT licence.
Every certificate is byte-identical between the issue pin and the retained revision.

## Complete Claim Inventory

The issue and the source’s [records.txt](source/square-packing-above-324/records.txt)
state each side rounded up at twelve places from the exact side in line 1 of its
certificate, against the record of 17 October 2026:

| n | Reported side | Record then | Certificate |
| ---: | --- | --- | --- |
| 464 | 21.988813022694 | 21.989992144499 (Couzo, 14 October 2026) | [n0464.cert](source/square-packing-above-324/n0464.cert) |
| 509 | 22.994328036438 | 23 (grid) | [n0509.cert](source/square-packing-above-324/n0509.cert) |
| 555 | 23.993653790591 | 24 (grid) | [n0555.cert](source/square-packing-above-324/n0555.cert) |
| 603 | 24.995268064197 | 25 (grid) | [n0603.cert](source/square-packing-above-324/n0603.cert) |
| 654 | 25.996103908965 | 26 (grid) | [n0654.cert](source/square-packing-above-324/n0654.cert) |
| 706 | 26.998712100405 | 27 (grid) | [n0706.cert](source/square-packing-above-324/n0706.cert) |
| 760 | 27.995949340329 | 28 (grid) | [n0760.cert](source/square-packing-above-324/n0760.cert) |
| 817 | 28.998488480775 | 29 (grid) | [n0817.cert](source/square-packing-above-324/n0817.cert) |
| 875 | 29.998783733108 | 30 (grid) | [n0875.cert](source/square-packing-above-324/n0875.cert) |
| 935 | 30.995955854834 | 31 (grid) | [n0935.cert](source/square-packing-above-324/n0935.cert) |
| 998 | 31.998349747355 | 32 (grid) | [n0998.cert](source/square-packing-above-324/n0998.cert) |
| 1061 | 32.996048342114 | 33 (grid) | [n1061.cert](source/square-packing-above-324/n1061.cert) |
| 1128 | 33.998294117981 | 34 (grid) | [n1128.cert](source/square-packing-above-324/n1128.cert) |
| 1196 | 34.998294118334 | 35 (grid) | [n1196.cert](source/square-packing-above-324/n1196.cert) |
| 1266 | 35.996046404219 | 36 (grid) | [n1266.cert](source/square-packing-above-324/n1266.cert) |
| 1339 | 36.997865207179 | 37 (grid) | [n1339.cert](source/square-packing-above-324/n1339.cert) |
| 1413 | 37.999463832123 | 38 (grid) | [n1413.cert](source/square-packing-above-324/n1413.cert) |
| 1489 | 38.997600184483 | 39 (grid) | [n1489.cert](source/square-packing-above-324/n1489.cert) |
| 1568 | 39.999336626159 | 40 (grid) | [n1568.cert](source/square-packing-above-324/n1568.cert) |

These are reported feasible upper bounds, with no optimality, rigidity or local-minimum
claim.
Later reports by Francisco Couzo (#672, #675 and #678) are smaller at 464, 555, 603, 654,
706, 760, 817, 935 and 998; the import declaration lists them, and the intake ledger
of 18 October 2026 records each report in the order it reached this repository.

## Credit and Shared Dependencies

The source names Joost de Winter.
It states that the packings use the staircase-rectangle and four-block method of
Arslanov, Mustafin and Shangitbayev (Electronic Journal of Combinatorics 28(4), P4.22,
2021): two compressed tilted components and two aligned grids per packing. The n = 464
packing also uses a six-square patch from the author’s n = 422 construction.
It states that the numerical search and refinement were performed with GPT-6 Astra
under his direction, and that the certificates and checks were produced with Claude
(Anthropic).

Each certificate is in Evan Daniel’s text format: line 1 gives n and the exact side, and
each further line gives a square’s centre and $t = \tan(\theta/2)$, all rational.
The source’s [check.py](source/square-packing-above-324/check.py) uses the Python
standard library and exact rationals: every corner strictly inside the container, and
every pair whose centres are closer than $\sqrt{2}$ separated along one of the four edge
normals.
The issue reports that it accepts all nineteen, and that the decimal JSON poses pass the
same test at 80 digits. Both checks share one author and the separating-axis method.
They are the source’s assertions; acquisition ran no source program.

## Retained and Omitted Material

`devtools.acquire_source` retained 23 files, 6,564,793 bytes: the licence, the README,
`records.txt`, `check.py` and the nineteen certificates. No file reached the gzip rule;
the certificates are not one of its data suffixes.
The nineteen decimal-pose JSON copies and the 10.6 MB `before_after.svg` comparison
figure are pinned by digest only: 20 files, 13,990,776 bytes.
The authoritative exact certificates are retained, and the figure is not a proof input.

## Custody Check

From `packing/`, with the project interpreter:

```bash
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  de-winter-above-324-2026-10-17 --check
```

This check validates the declaration, the retained bytes and the manifest.
It establishes no geometric claim and raises no evidential rating.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
