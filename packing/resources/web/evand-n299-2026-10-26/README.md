# Evan Daniel’s s(299) Certificate at 1be69ca

This packet retains the certificate Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing/tree/6067db5bf4d41dab7f0e1475e9fa845c0c6d2133/search/packer/candidates)
adds at `1be69ca8a088035ccced0e279e40abea81e1d9f3` (authored and committed
2026-10-26T03:30:38Z). Issue [#824](https://github.com/jlevy/squares/issues/824), opened
21 minutes 40 seconds later at 03:52:18Z, reports it:

- **299, recorded as T-247:** `s299-1025.cert`,
  $s(299) \le 8901847717666168847717657266821/(5 \cdot 10^{29}) =
  17.803695435332337694\ldots$, which the issue prints rounded up at 12 places as
  17.803695435333: 1.92e-2 below the case’s house, the Kingbird catalogue’s
  $33/2 + \sqrt{7}/2 = 17.8228756555\ldots$ that T-101’s exact ceiling verifies, and below
  every report at 299.

T-247 registers it at `V0`/`C0`. The stage 4 review and the adoption at 299, with both
strong generators’ regularization and the flip of the new house in the same pull request,
are think-8hjz’s.

The source was read on 26 October 2026 from a blobless clone fetched at about 04:55Z,
whose head was `6067db5bf4d41dab7f0e1475e9fa845c0c6d2133` (committed 03:47:41Z), the
packet’s pin. The certificate’s bytes are the same at `1be69ca` and at the pin;
`f01779b`, between them, adds the source store’s prior facts at 299, which the packet
retains. GitHub’s activity log was not readable from this session, so no push time is
recorded.

## What the Author Claims

Issue #824 claims one new upper bound, the certificate’s exact rational side rounded up at
12 places, and prints the SHA-256 of `s299-1025.cert`. It says:

- **Checking.** The source’s `search/exact/verify_cert.py` (separating axes) and
  `verify_cert2.py` (polygon intersection) both print VALID; they share an author and
  the certificate format.
- **Local optimality: not established.** The source’s exact solver did not certify a KKT
  point, so the certificate dilates the binary64 packing by 1.78e-11. A corner–corner
  MILP linearization suggests a first-order descent the source did not realise; a lower
  nearby minimum may exist.
- **How it was found.** Chris Deotte’s s(334) packing (18.795715128, from his public
  Kaggle notebook `squares-in-squares-ftmc-milp-refill-22-311`), relaxed to 18.791043283;
  an L of 39 squares added for s(373) at 19.803695435; then a fault-line composition at
  299 of corner gadgets cropped from that 373 packing and an earlier s(299) of the
  source’s own (17.804000863), chained along a diagonal fault, side 17.803695435315; then
  the dilation.
- **Credit.** A new packing, “not a refinement of the register’s 33/2 + √7/2
  construction”, built by the source’s own implementation of Chris Deotte’s multi-gadget
  fault DP, with the request that Deotte be credited for the method and the start.
- **Side-only claims.** Two Kaggle per-puzzle leaderboard entries list sides below this
  one with no packing: 17.802718854399 for team Amin (23 October, also in Francisco
  Couzo’s `upper_bounds.json` as a reported bound) and 17.798169713703 for team Chris
  Deotte (25 October).

The certificate’s JSON report agrees with the issue on the solver: `cert_valid` is false
at its 80-digit point, `s299-1025.exact.txt`, where the pair (235, 281) overlaps by
0.711, so that point is no packing. The certificate is the dilation of the binary64
input, not of that point.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 10 files: 8 retained under [source/](source/) (137,844
bytes) and 2 pinned by digest.

| Retained under `source/search/packer/candidates/` | What it is |
| --- | --- |
| `s299-1025.cert` | the certificate, SHA-256 `1ad65a494df088a8…`, as the issue prints |
| `s299-1025.input.txt` | the binary64 packing it dilates, side 17.803695435314534 |
| `s299-1025.predescent.txt` | the packing before the source’s descent step |
| `s299-1025.exact.txt` | the exact solver’s 80-digit point, which overlaps and is no packing |
| `s299-1025.json` | the exact solver’s report |
| `s299-1025_prior.json` | the source store’s prior facts at 299, added by `f01779b` |

The six files are the whole `s299-1025` set at the pin, 129,275 bytes upstream.
The licence and `CREDITS.md` are retained beside them. Pinned by digest: the two exact
checkers the certificate’s header names, `search/exact/verify_cert.py` and
`verify_cert2.py`, against the identical copies the
[n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about 0.15 MB, so it is kept in Git.

## Report Order

The [ledger of 26 October for this import](../../../campaign/issue-intake/upper-bounds-issue824-20261026/README.md)
walks #824 from the starts frozen at `main` `9ebde24df`, where the Kingbird catalogue’s
closed form holds 299 in the reported lane and T-101’s exact ceiling in the verified
lane, and no register bound is pending adoption: recorded, 1.92e-2 below, a new packing.
The commit 21 minutes before the issue is the same author’s publication of the same file,
and nothing reached 299 between them, so no verdict depends on which dates it.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `9ebde24df` on 26 October
2026). The certificate is below the case’s verified ceiling, T-101’s exact certificate of
the catalogue packing, by 1.92e-02, and below the reported lane’s closed form. It is the
smallest report at 299. The case’s conjectured optimum, 17.82287565553229, is the
catalogue’s side; this side is below it.

Neither Kaggle entry the issue quotes is a report, since neither states a packing; both
are below this side.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-101’s certificate of the
house’s packing and against the source’s binary64 input, and wrote
[measure/identity.json](measure/identity.json). A measurement for credit; it decides
nothing. The house witness, a decimal centre-angle witness at the closed-form side, is not
a form the tool reads, and T-101’s certificate is the same packing at its rational
ceiling.

- **Against T-101:** no symmetry of the box pairs the two one to one by nearest centres.
  The optimal assignment, best under the mirror $y \mapsto s - y$, moves 124 of 299
  squares beyond 0.1 and 243 beyond 0.01 (largest 1.14) and turns 126 by up to 39.1
  degrees. The certificate has 83 tilted squares, 52 turned one way and 31 the other, at
  25.95 to 30.24 degrees; T-101’s packing has 38, all at 24.30 degrees. So it is another
  arrangement, as the issue says.
- **Against the source’s binary64 input:** one to one under the identity, none beyond
  1e-9 (largest 2.45e-11), the dilation the header names.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 267,306 pair decisions, 46.84 route CPU seconds, the longest job 59.72
seconds ([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)).
The certificate clears every wall by at least 4.99e-13 and every pair by at least
9.99e-13.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
1e-30 past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)). It lowered
the side by the least far-wall clearance, closed the least-gap pair by its gap, and moved
every square toward the nearer near wall by its least clearance. Both routes accepted all
three at contact with margin 0 and refused all three past it with margin −1e-30. It also
enlarged one square to its pair and one to its wall: both routes refused each at contact
for its shape alone, and 1e-30 past it for the overlap or the wall as well. Both refused a
duplicated square. The run took about 3 CPU minutes.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the certificate through the `evand-cert` reader,
whose line filter and corner construction are transcribed from Daniel’s checkers. The
source’s checkers were not run.

## What Is Not Established

- **No review yet.** The stage 4 mathematical review, by a strong-tier lane sharing no
  context with this one, has not run; it and the adoption are think-8hjz’s.
- **Local optimality**, which the issue itself says is not established.
- **The lineage** from Deotte’s s(334) packing: the author’s statement. No Deotte packing
  is retained here, and the source’s earlier s(299) is not published.

## Credit and Licence

MIT, copyright (c) 2026 Evan Daniel. `CREDITS.md` says the repository’s work was
“Produced by Claude (Anthropic) in a single session under human direction”, and the
certificate’s commit carries a Co-Authored-By trailer naming Claude. The packing is Evan
Daniel’s, by his implementation of Chris Deotte’s multi-gadget fault-line DP from a start
the issue credits to Deotte’s public Kaggle s(334) packing; the bibliography key is
**[Daniel n299 2026-10-26]**, “Daniel after Deotte”.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-n299-2026-10-26 --checkout CHECKOUT
python -m devtools.acquire_source evand-n299-2026-10-26 --check
python -m devtools.upper_bound_reports evand-n299-2026-10-26 check-claims --write
python -m devtools.upper_bound_reports evand-n299-2026-10-26 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports evand-n299-2026-10-26 check --replay
python -m devtools.upper_bound_reports evand-n299-2026-10-26 sharp-controls
python -m devtools.measure_identity --n 299 '#824=packet:evand-n299-2026-10-26' \
  'T-101=evand-cert:resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-299.cert' \
  'input=binary64-xyd:resources/web/evand-n299-2026-10-26/source/search/packer/candidates/s299-1025.input.txt' \
  --out resources/web/evand-n299-2026-10-26/measure/identity.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
