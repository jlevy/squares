# Francisco Couzo’s 304 Certificate at fa6237e, No Issue

This packet imports `certificates/best/n304.cert` from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/blob/fa6237e288cf3fc53b53fc43438c91f3f59c40e9/certificates/best/n304.cert)
at `fa6237e288cf3fc53b53fc43438c91f3f59c40e9` (committed 2026-10-23T18:59:39Z, “Land the
Kaggle intake certificates and restore held records below 324”), the first commit on any
ref that holds these bytes (blob `953dc2e5`; the path held other bytes, blob `1a0be085`,
from `4e4c8ce` of 15 October). GitHub’s activity log records it pushed at
2026-10-23T23:38:42Z with `efef7d1` and `964ee2b`, the commit
[issue #763](https://github.com/jlevy/squares/issues/763) names, and the record dates it
by that push, as it dates every commit a later push made public. The file is unchanged
at `964ee2b` and at the head `1c17153`.

#763 does not claim 304: its README selects counts credited to Couzo, and this one is
credited to another author’s notebook. No issue reports it, so it is a report from its
publication (the owner, 14 October 2026). Its header states
$s(304) \le
42654421699169959072564987841514227093543746926117736119087439/2379353056489745832681562849107891444171481219500000000000000
= 17.92689890339264\ldots$, which the source prints rounded up as 17.926898903393,
2.53e-3 below T-186, the case’s house best packing. T-241 registers it as reported, at
`V0`/`C0`; the case is unchanged.

## Retained Here

Nothing: the certificate is the [issue-763 packet](../couzo-issue763-2026-10-23/README.md)’s
copy, retained there for this import. [acquisition/declaration.json](acquisition/declaration.json)
pins it against that copy (`identical_to`), and `devtools.acquire_source --check` compares
the two. `devtools.upper_bound_reports` reads it from there and holds it to the pinned
SHA-256, `c8433dd798aef6f190790c6c78c63b4ab5c26baabe372405f8ff9029d175231d`.
Also pinned by digest: the root `README.md`; `certificates/best/README.md` (157 KB) and
`certified_bounds.json` (8.8 MB), which print the side and the credit;
`certificates/best/manifest.json` (14 MB, SHA-256 `31b0caef…`), whose `witnesses/304`
entry holds the provenance the credit defers to, and which the issue-763 packet retains
at `964ee2b` with that entry identical; and the verifier’s
licence, `BOUND_VERIFIER_LICENSE.txt`, against the
[18 October packet](../couzo-issue678-2026-10-18/README.md)’s copy.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the
manifest.

## What the Author Claims

- **The catalogue row,** `certificates/best/README.md` at the pin:
  “| [304](n304.cert) | 17.926898903393 | Kirill Tymchishin (kirilltym), Kaggle “CPU
  Alternating Reclosure” v3; earlier construction credits in its source notices; earlier
  seed and construction credits retained in provenance |”.
  `acquisition/report.json` admits the certificate at that print.
- **His check,** `certified_bounds.json` at the pin: the same credit, with `"valid": true`,
  4297 pairs tested, and the arithmetic backend “GMP exact rationals via gmpy2 2.3.2”.
- **The provenance the credit defers to.** The catalogue says “Source, construction, seed
  and certificate credits are retained in manifest.json”. That manifest’s `witnesses/304`
  entry gives the packing’s source as Tymchishin’s notebook “CPU Alternating Reclosure”
  v3 (run 361239073, Apache-2.0, `witness_dilation` 1+1e-10). It names the notebook’s
  `previous_source` as Mykhailo Polkovskyi’s `n304.cert` at
  `Mishapolk/square-packing-records@70a033f` (#593), credited “Mykhailo Polkovskyi
  (Mishapolk)” with `construction_credit` “Nate Chaoweeraprasit (itsnaka)”, and its
  `previous_reference.seed_credit` as “Mykhailo Polkovskyi (Mishapolk)”. That certificate’s
  SHA-256, `72fa0c89…`, is the one the
  [mishapolk-kkt-refinements-2026-10-14 packet](../mishapolk-kkt-refinements-2026-10-14/README.md)
  pins: T-186’s packing, the house at 304. The manifest’s first checker is this project’s
  `sqpack/verify.py`. The notebook’s own source notices
  (`submissions/kaggle-public-portfolio-20261022/SOURCE_NOTICES.md`) are in no commit of
  the source.

These statements are the author’s. No source program ran here.

## Report Order and the Record

The [ledger of 24 October for this import](../../../campaign/issue-intake/upper-bounds-evand-20261024/README.md)
records this certificate first at 304, 2.53e-3 below T-186, and Evan Daniel’s later
certificate of the same packing (T-242, the
[evand-kaggle-descents-2026-10-24 packet](../evand-kaggle-descents-2026-10-24/README.md))
after it, 3.04e-9 below.
[acquisition/claims.json](acquisition/claims.json), read from `main` `2ec489d1` on 24
October 2026, places it below T-186, #593 and T-175 by 2.53e-03, below T-152 and T-174 by
2.67e-03, below T-151 by 2.76e-03, and below T-098 and T-056 by 7.75e-03: the smallest
report at 304 when read.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, 276,336 pair decisions,
40.35 route CPU seconds ([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)).
It clears every wall by exactly 1e-15, below the binary64 spacing of coordinates near 18,
and every pair by at least 8.18e-11.
The program [sharp_controls.py](../evand-kaggle-descents-2026-10-24/receipts/sharp_controls.py)
of the evand-kaggle-descents packet then took it to exact contact and 1e-30 past it, three
ways: the side lowered by the least far-wall clearance, the least-gap pair closed by its
gap, and every square moved toward the nearer near wall by its least clearance. Both
routes accepted each at contact with margin 0 and refused each past it with margin
−1e-30 ([receipts/sharp-controls.json](receipts/sharp-controls.json)).
The two routes share certificate parsing, half-angle conversion, `Fraction` arithmetic and
the separating-axis method. The source’s checkers were not run.

## Pose by Pose

Measured by the evand-kaggle-descents packet’s
[measure/identity.json](../evand-kaggle-descents-2026-10-24/measure/identity.json), a
measurement for credit that decides nothing:

- **Against T-186.** Nearest centres pair this packing with the house’s one to one under
  no symmetry. The optimal assignment, best under the diagonal reflection
  $(x, y) \mapsto (y, x)$, keeps 250 of the 304 squares within 0.1 of the house’s and
  moves the other 54 beyond it (largest 1.13), turning squares by up to 26.0°. The 250
  within and the 54 beyond are one assignment, read from either side. That fits the
  lineage the manifest states, a re-closure of Polkovskyi’s packing: with 54 squares
  beyond a tenth it is another arrangement at the record’s threshold, found from the
  house’s, not a refinement of it.
- **Against Daniel’s copy.** Evan Daniel’s binary64 copy of “the public Kaggle packing at
  17.9268989004” is this packing to 2.05e-9, of the order of the manifest’s witness
  dilation of 1+1e-10, which moves a centre by at most about 2.5e-9 in this box.

## What Is Not Established

A finite packing certifies an upper bound and nothing more.
No KKT, local-minimum, rigidity or optimality statement is replayed. The manifest’s
provenance is read here; the notebook’s own source notices, which hold any earlier
construction credits of the notebook itself, are not published, and are not read. Whether
the notebook started from Polkovskyi’s certificate is the manifest’s statement, which the
measurement above fits but does not decide.

## Credit and Licence

Credit Kirill Tymchishin’s packing, as the source credits it, after Mykhailo Polkovskyi’s
packing (the notebook’s previous source and seed) and Nate Chaoweeraprasit’s construction
(the construction credit of Polkovskyi’s certificate), as the source’s manifest states the
chain; certified by Francisco Couzo, who claims no refinement of it. Evan Daniel’s later
certificate of the same packing says its finder is unknown and its earliest public copy is
kozykappa’s notebook; both authors are asked.
The repository states no licence for its data or prose. The certificate is retained by
the issue-763 packet, on the presumption of permission that Couzo’s submission of that
source carries (the owner, 24 October 2026, think-cnn7; licence follow-up think-m8f4), and
certificates are factual data under the owner decision of 2026-10-09.
The bibliography key is **[Couzo n304 2026-10-23]**, credited *Couzo after Tymchishin,
Polkovskyi, Chaoweeraprasit, Levy*; Levy because the manifest’s first checker is this
project’s `sqpack/verify.py`, as for #763.

## Questions for the Author

Drafted in think-l49q for Francisco Couzo, on #763 or wherever the coordinator posts:

1. Did Tymchishin’s notebook start from Polkovskyi’s `70a033f` packing, as your manifest’s
   `previous_source` and `seed_credit` say, and what does Chaoweeraprasit’s construction
   credit cover in it?
2. Is Kirill Tymchishin the finder of the packing at 304, which Evan Daniel’s source calls
   of unknown finder, with kozykappa’s notebook its earliest public copy?

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-n304-2026-10-23 --checkout CHECKOUT
python -m devtools.acquire_source couzo-n304-2026-10-23 --check
python -m devtools.upper_bound_reports couzo-n304-2026-10-23 check-claims --write
python -m devtools.upper_bound_reports couzo-n304-2026-10-23 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports couzo-n304-2026-10-23 check --replay
python resources/web/evand-kaggle-descents-2026-10-24/receipts/sharp_controls.py --packet couzo-n304-2026-10-23 --n 304 --out resources/web/couzo-n304-2026-10-23/receipts/sharp-controls.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
