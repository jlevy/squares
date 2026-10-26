**Title:** New upper bounds for 683 values of n in [1184, 3775] — Karimi two-strip construction (exact rational certificates)

Hello, and thank you for maintaining this catalogue.

I would like to register 683 improved upper bounds for s(n), n in [1184, 3775].
In 85 of these cases the current entry is the trivial grid ⌈√n⌉.

**Construction.** In a box of side S just below an integer K, two strips of squares
tilted by a small angle are attached to the walls: one strip of rows on the bottom wall
and one strip of columns on the right wall; the rest is an axis-parallel grid.
Consecutive rows in a strip touch (vertical pitch cos a, horizontal shift sin a), so
a strip of m rows gains one square per grid column when m(1 − cos a) ≥ sin a + (K − S).
All angles have rational tan(a/2), so every coordinate is an exact rational.

**Certificates.** Format `n S` header, then `x y t` per square with t = tan(θ/2), all
exact rationals — the same format as this repository. Every file passes
`verify_bound_certificate.py` / `check_packing.py` from this repository
(VALID, closed container).

**Data:** Zenodo record {DOI} (certificates, table of new vs previous sides, code).

A few examples:

| n | previous best | new side |
|---|---|---|
| 1184 | 34.909679 | 34.908235 |
| 1813 | 43.000000 | 42.992495 |
| 1987 | 45.000000 | 44.985304 |
| 2342 | 48.988287 | 48.900000 |
| 2343 | 48.988287 | 48.900000 |
| 2344 | 48.988287 | 48.900000 |

**Credit:** Mohsen Karimi (ORCID 0009-0004-1055-8267). The code was written with the
assistance of Claude (Anthropic) under my direction.

Best regards,
Mohsen Karimi
