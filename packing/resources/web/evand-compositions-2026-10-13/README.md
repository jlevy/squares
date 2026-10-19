# Evan Daniel’s Two-Piece Compositions at 231d41d: 339, 364 and 375

[Issue #584](https://github.com/jlevy/squares/issues/584) reports three exact rational
packings from Evan Daniel’s two-piece composer, every one beyond the $n \le 324$ case
corpus, for the record’s beyond-horizon list, in
[evand/square-packing](https://github.com/evand/square-packing/tree/231d41df7a03fccd89aa6e9ef5a540348a8214cc/search/packer/candidates).
The issue names commit `231d41df7a03fccd89aa6e9ef5a540348a8214cc` (tree
`a311a33ef6c781b3b358602b63e3c02151401b8d`, committed 2026-10-13T14:24:04Z) with the
SHA-256 of each certificate, and the packet pins it.
The head when the sources were retrieved, at 2026-10-14T07:01Z, was `622cd2e`, which
holds the same twelve files and the same two checkers.
The issue was filed at 2026-10-13T14:31:16Z and has not been edited.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 339 | `1892689890035674158973360842897/100000000000000000000000000000` | 18.926898900357 | 18.9268989003567416 |
| 364 | `19583782203950834292109305759091/1000000000000000000000000000000` | 19.583782203951 | 19.5837822039508343 |
| 375 | `19882451030481246819527281665997/1000000000000000000000000000000` | 19.882451030482 | 19.8824510304812469 |

Each certificate gives `n` unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in an open square of the stated side, in the format of issues
#375, #489 and #552; `devtools.upper_bound_reports` reads it through its `evand-cert`
adapter. Each side is the exact KKT point the solver found, scaled by $1 + 10^{-20}$
about the origin corner, and the issue prints it both exactly and rounded up at 12
places. All three were first committed in the pinned commit.

Through Friedman’s L-step the issue also states $s(403) \le 20.583782203951$ and
$s(414) \le 20.882451030482$, as corollaries for which it asks no rows.
The packer log at the pin records further compositions it withdraws as beaten by the
L-step, at 325 and 326, and a certified 414 that the 375 corollary beats; the issue
reports none of them.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
18 files, 690,116 bytes.

| Upstream path | Bytes | SHA-256 |
| --- | --- | --- |
| `search/packer/candidates/comp2_n339.cert` | 54643 | `c09a12a5242f7ac759a4ef30c1d64fb813cef4419344c3c9459af30cf2a7801c` |
| `search/packer/candidates/comp2_n364.cert` | 59800 | `f79b2d23b730d3b118b14d7995607410068a6b5b3db6929e2f0cfda8e522bf4a` |
| `search/packer/candidates/comp2_n375.cert` | 65115 | `06438617618f35e202eff4f9d295076e9838df05b76a38ee04d763d9052d097e` |

For each count the packet retains four files: the `.cert` certificate, the 80-digit KKT
point it was rounded from (`.exact.txt`), the binary64 packing that point was solved
from (`.input.txt`), and the solver’s report (`.json`). It also retains `LICENSE` and
`CREDITS.md`, 14 files and 454,778 bytes in all.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, are
pinned by digest against the identical copies the
[issue-399 packet](../evand-new-arrangements-2026-10-07/README.md) retains, and were not
run; `search/exact/README.md` is pinned against the
[issue-489 packet’s](../evand-record-hunt3-2026-10-10/README.md) identical copy, and the
packer’s working log, `search/packer/PACKER.md` (213,524 bytes), by digest only.

## Exact Replay

Only the three certificates enter geometry decisions, through the maintained two-route
kernel of `devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and
the independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on one worker.

All three positives pass both routes, and both routes refuse all six controls, each on
the overlap or the wall it was built to break.
In every positive the two routes find the same least wall clearance, at least
$5.00 \times 10^{-21}$, and the same least pair gap, just under $10^{-20}$, as the issue
states. The nine jobs made 1,160,892 pair decisions in 477.89 route CPU seconds and
755.18 job wall seconds, summed; the longest, the duplicate-square control at 364, took
108.47 seconds. The one-worker run took 12 minutes 49 seconds of wall time with the
machine at a load of 9 to 11. A fresh serial `check --replay` decided all nine jobs
again, equal to the retained rows apart from timing, in 8 minutes 39 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code, and the third exact route
(`devtools.check_half_angle_area`) has not read these certificates.
No source program ran here.

## Against the Record

No case record holds these counts, so [acquisition/claims.json](acquisition/claims.json)
compares each certificate with the grid and with every report the record tracks or has
pending at the count, frozen at `main` `aeef99ef0` (14 October 2026); `check-claims`
rebuilds it.
Francisco Couzo’s sides are compared at the 12 places he prints, rounded up,
and the 364 row of his extended-range reports at its 15 places, as that row does.

| n | Tracked beyond-horizon row | Below it by | Other reports at the count | Smallest |
| --- | --- | --- | --- | --- |
| 339 | 18.929433883808, Francisco Couzo’s #506 certificate (verified) | $2.53 \times 10^{-3}$ | #583 (Couzo) 18.927383638495, above by $4.85 \times 10^{-4}$; #586 (Couzo) 18.925319360704, **below** this side by $1.58 \times 10^{-3}$ | #586 |
| 364 | 19.597249391207239, Couzo’s extended-range report (reported) | $1.35 \times 10^{-2}$ | none | this certificate |
| 375 | 19.906335145009, Couzo’s #506 certificate (verified) | $2.39 \times 10^{-2}$ | #561 (Couzo) 19.901618621328, above by $1.92 \times 10^{-2}$; Couzo’s `4596670` `certificates/n375.cert`, in no issue, 19.893906534236, above by $1.15 \times 10^{-2}$ | this certificate |

Couzo’s #586 cites this issue as the side it improves at 339. His `n375.cert` is
byte-identical at `4596670` and at his head `b85dee2`, fetched here to scratch; its
exact side rounds up to the 12 places the issue quotes.
His head’s 364 certificate states 19.597249391226, above.
No other open report of the 14 October intake names these counts.
The certificates are $7.3 \times 10^{-2}$, $0.416$ and $0.118$ below the grid sides 19,
20 and 20.

With every requested count beyond the corpus, the release has no register entry.
Its sides are dated beyond-horizon rows, one each in `beyond_horizon_claims` of
`source-coverage.yaml`, as issue #506’s are: keyed on the count and this source, with
the 12-place side the issue prints, and no case record, register row, selected bound or
atlas entry. A row there must equal its source’s reparsed claim byte for byte, so
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the three claims alone, and the source’s coverage entry names it as its `claims_record`.
At 364 and 375 the rows would supersede Couzo’s; at 339 the row would supersede his #506
row and stand above #586 until that is registered.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The source states three things about each exact point: positive KKT multipliers on its
load-bearing contacts, the smallest $1.0 \times 10^{-8}$ at 339, $1.0 \times 10^{-6}$ at
364 and $7.6 \times 10^{-4}$ at 375; a reduced Hessian positive semidefinite modulo
exact flat motions, 203, 190 and 164 of them; and a first-order MILP that finds no
descent in any corner-to-corner branch.
Those are numerical evidence, as the source itself says, and were not replayed here.
Novelty, local or global optimality and rigidity are not established, and neither are
the side identities the issue states (364 as $s(146) + 7$, 375 as $s(88) + 10$ to 13
digits).

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`. The issue states that the composer, the search, the checks and the request
were done with Claude (Claude Code), directed and reviewed by Evan Daniel.
All three are two-piece compositions in the style of David Ellsworth’s s(171) and Daniil
Ostashev’s #562 and #575 compositions: a rectangle of unit squares whose sides differ by
an integer in each of two opposite corners, and aligned squares filling the rest.
The issue asks that the packings the pieces came from be credited:

- 339: two pieces cut from Daniil Ostashev’s s(304) of #575, 67 and 68 squares in
  $(h + 7) \times h$ rectangles, each re-optimised as a rectangle;
- 364: BuddenPing’s (PingYou Ltd’s) s(146), #566’s exact refinement of Robert Barnett’s
  #505, whole in one corner, and Thomas Schadt’s $s(50) = 53/7$ in the other;
- 375: a 69-square $(h + 2) \times h$ crop of Nate Chaoweeraprasit’s (SQUISH) s(88) and
  a 118-square $(h + 1) \times h$ crop of Ryan Xu’s s(129).

The issue says that at 364 and 375 the side is an older packing’s side plus an integer,
so these are new arrangements of known pieces, not new local structure.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-compositions-2026-10-13 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-compositions-2026-10-13 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-compositions-2026-10-13 check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`register-plan` prints the record entries the import needs: here an evidence entry, a
source row and three beyond-horizon rows.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
