# Exact Certificate Refinements — PingYou Ltd

This supplement to [PR 574](https://github.com/jlevy/squares/pull/574) provides 60
tighter square-packing certificates. Fifty-eight complete packings attain known
construction values in algebraic number fields; N146 and N261 have tighter exact
rational realizations of their existing separation constraints. Each new side is
strictly smaller than its named submitted predecessor. These improvements include
reductions in certification padding.

The [claims](claims.json) identify the cases, exact expressions, predecessor hashes
and verification evidence. The
[source release](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1)
contains the full coordinates and portable checkers; the
[HostedData manifest](../../../hosted/pingyou-algebraic-refinements-2026-10-13.yaml)
records the archive size and checksum. The earlier
[v2 submission](../pingyou-numerical-refinements-2026-10-13/README.md) and
[exact N153/N302 supplement](../pingyou-exact-153-302-2026-10-13/README.md) remain
available.

## Results and Coverage

| Certificate family | Cases | Result |
| --- | ---: | --- |
| Diagonal, strip and collar constructions over Q(sqrt(2)) | 48 | Exact attainment, including N66's sliding construction |
| Other quadratic, quartic and cap constructions | 8 | N18, N53, N54, N107, N151, N178, N234 and N299 |
| N70 return and its N207 composition | 2 | Exact degree-five realizations |
| N146 and N261 inherited separation constraints | 2 | Strictly tighter rational certificates |

The N53 enclosing side lies in Q(sqrt(7)), but its complete coordinate certificate
uses a degree-eight field to close the final two-square cap. N151 uses a
biquadratic field because its two 45-degree squares remain part of the packing.
Coordinate-field degree is therefore distinguished from the degree of the side.
The archive's `CONSTRUCTION-NOTES.md` gives the physical reconstruction and cap
closure equations.

The audit accounts for all 147 counts from the v2 submission. The archive's
`COVERAGE-147.json` records the individual dispositions and source attribution.

| Disposition of the original submission | Count | Action |
| --- | ---: | --- |
| Verified improvements in this supplement | 59 | Replace the named predecessor certificates |
| Further algebraic reconstruction remains open | 82 | Retain the existing rational submissions |
| Exact rational endpoints already submitted | 2 | Keep N50 and N171 |
| Exact algebraic endpoints already published | 2 | Keep N153 and N302 |
| Older radical constructions are dominated | 2 | Keep the stronger N204 and N264 submissions |

N261 was submitted separately before this update. Its tighter rational certificate
joins this PR here, bringing the cumulative request to 148 distinct counts. It is
outside the original 147-count denominator.

## Verification

Extract the archive and enter `pingyou-algebraic-refinements-2026-10-13/`. With
Python 3.12 or later, run:

```sh
python3 VERIFY.py
```

The independent checker verifies the declared real root, every unit-square frame,
all four containment inequalities per square and every unordered pair. It computes
separating axes from the coordinates and compares the attained side exactly with
the predecessor. Across the 60 cases this covers 9,103 squares, 36,412 wall
inequalities and 917,302 pairs. The wrapper also checks that each native Witness/v2
encoding decodes to the same side, centers and frames.

To replay the native encodings with an installed Squares Project checkout, use its
Python 3.14 environment:

```sh
/path/to/squares/packing/.venv/bin/python VERIFY.py --checkout /path/to/squares
```

The archive retains per-case verification receipts and the current-public
comparison. Strict comparisons use exact certificate sides; rounded catalog
displays do not establish an improvement.

## Scope and Attribution

These are complete feasible upper bounds and certificate refinements. They do not
claim 60 new nominal records or establish global optimality. Maintainer intake and
acceptance remain pending.

PingYou Ltd requests credit for the certificate refinements. Original construction
authors, preceding refiners and source/tool authors retain their per-case roles in
`credits.json`. The native schema and verifier retain the Squares Project's
upstream license. No blanket license over third-party geometry or source material
is added by this submission.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
