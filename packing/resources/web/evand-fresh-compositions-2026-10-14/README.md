# Evan Daniel’s Fresh-Pass Compositions at 622cd2e: 365, 370 and 460

[Issue #596](https://github.com/jlevy/squares/issues/596) reports three exact rational
packings from a fresh pass of Evan Daniel’s two-piece composer, every one beyond the
$n \le 324$ case corpus, for the record’s beyond-horizon list, in
[evand/square-packing](https://github.com/evand/square-packing/tree/622cd2e21407700fe8d5ac5943af820725107921/search/packer/candidates).
The issue names commit `622cd2e21407700fe8d5ac5943af820725107921` (tree
`b8724f1ff1bdabaf8a525efa0f74c02c11e20b48`, committed 2026-10-14T06:50:09Z) with the
SHA-256 of each certificate, and the packet pins it; it was still the branch head when
the sources were retrieved, at 2026-10-14T08:28Z. The issue was filed at
2026-10-14T06:51:07Z and has not been edited.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 365 | `19621320343559642573398746289751/1000000000000000000000000000000` | 19.621320343560 | 19.6213203435596426 |
| 370 | `19767730746254604158720695152869/1000000000000000000000000000000` | 19.767730746255 | 19.7677307462546042 |
| 460 | `10979984841510246567080095841227/500000000000000000000000000000` | 21.959969683021 | 21.9599696830204932 |

Each certificate gives `n` unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in an open square of the stated side, in the format of issues
#375, #489, #552 and #584; `devtools.upper_bound_reports` reads it through its
`evand-cert` adapter.
Each side is the exact KKT point the solver found, scaled by $1 + 10^{-20}$ about the
origin corner, and the issue prints it both exactly and rounded up at 12 places.
All three were first committed in the pinned commit.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
18 files, 804,613 bytes.

| Upstream path | Bytes | SHA-256 |
| --- | --- | --- |
| `search/packer/candidates/fresh_n365.cert` | 63670 | `2d03e6bfd6993488adbf5d851d5b77feb0cd9a5dbe722f690932abe096d1e8ed` |
| `search/packer/candidates/fresh_n370.cert` | 59814 | `7cfb9102add6ccce5575176e2012178733db6393f969091d2d5acdb20f31a69b` |
| `search/packer/candidates/fresh_n460.cert` | 81919 | `3b2c3916e21079ba171cead7b7de2d65535e74b4560d48dc1e5c058c3a894d6d` |

For each count the packet retains four files: the `.cert` certificate, the 80-digit KKT
point it was rounded from (`.exact.txt`), the binary64 packing that point was solved
from (`.input.txt`), and the solver’s report (`.json`). It also retains `LICENSE`,
`CREDITS.md` and `search/exact/README.md`, 15 files and 521,230 bytes in all.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, are
pinned by digest against the identical copies the
[issue-399 packet](../evand-new-arrangements-2026-10-07/README.md) retains, and were not
run; the packer’s working log, `search/packer/PACKER.md` (276,881 bytes), is pinned by
digest only.

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
$5.00 \times 10^{-21}$, and the same least pair gap, just under $10^{-20}$. The nine
jobs made 1,441,590 pair decisions in 654.96 route CPU seconds and 822.92 job wall
seconds, summed; the longest, the outside-container control at 460, took 153.56 seconds.
The one-worker run took 13 minutes 54 seconds of wall time with the machine at a load of
4 to 7. A fresh serial `check --replay` decided all nine jobs again, equal to the
retained rows apart from timing, in 18 minutes 27 seconds at a load of 7 to 10.
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
The record tracks no beyond-horizon row at 365, 370 or 460, issue #584’s and
issue #506’s included, and no other open report of the 14 October intake names them, so
each certificate is the smallest side the record knows at its count.
The sides are $0.379$, $0.232$ and $4.0 \times 10^{-2}$ below the grid sides 20, 20 and
22\.

The issue compares each side with a bound it derives by Friedman’s L-step ($n$ squares
in side $s$ give $n + 2\lfloor s \rfloor + 1$ in side $s + 1$), which the record holds
as no row. Each side is below that bound, by $1.28 \times 10^{-2}$ at 365
($s(293) + 2 = 19.634146341463$), $1.04 \times 10^{-2}$ at 370
($s(298) + 2 = 19.778174593052$) and $1.64 \times 10^{-3}$ at 460 (issue #586’s
$s(380) + 2 = 21.961611078671$).

At 365 the issue states the side is $s(26) + 14 = 14 + 7/2 + 3/\sqrt{2}$. Measured here,
the certificate’s side less $35/2$ squares to $9/2$ plus $8.3 \times 10^{-19}$, which is
what the $1 + 10^{-20}$ scaling of that sum leaves, and a test holds it within
$1 + 10^{-18}$.

The rows would be dated beyond-horizon rows, one each in `beyond_horizon_claims` of
`source-coverage.yaml`, as issue #584’s are: keyed on the count and this source, with
the 12-place side the issue prints, and no case record, register row, selected bound or
atlas entry. A row there must equal its source’s reparsed claim byte for byte, so
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the three claims alone, and the source’s coverage entry names it as its `claims_record`.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The source states three things about each exact point: positive KKT multipliers on its
load-bearing contacts, the smallest $7.9 \times 10^{-7}$ at 365, $2.3 \times 10^{-6}$ at
370 and $7.5 \times 10^{-8}$ at 460; a reduced Hessian positive semidefinite modulo
exact flat motions, 156, 184 and 202 of them; and a first-order MILP that finds no
descent in any corner-to-corner branch.
Those are numerical evidence, as the source itself says, and were not replayed here.
Novelty, local or global optimality and rigidity are not established.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`. The issue states that the composer, the search, the checks and the request
were done with Claude (Claude Code), directed and reviewed by Evan Daniel.
All three are two-piece compositions as in #584, from a pass over the packings posted in
#586 and #593: a rectangle of unit squares whose sides differ by an integer in each of
two opposite corners, and aligned squares filling the rest.
The issue asks that the packings the pieces came from be credited:

- 365: the register’s s(199) (Nate Chaoweeraprasit, SQUISH) whole in one corner and
  Erich Friedman’s s(26) whole in the other;
- 370: Francisco Couzo’s s(175) (#488) whole in one corner and a 38-square
  $(h + 2) \times h$ rectangle from the author’s own rectangle search in the other, both
  moved by the polish;
- 460: an 81-square $(h + 6) \times h$ crop of Nate Chaoweeraprasit’s (SQUISH) s(306)
  (#481) and a 130-square $(h + 7) \times h$ crop of Francisco Couzo’s s(380) (#586).

The issue says that at 365 the side is an older packing’s side plus an integer, so it is
a new arrangement of known pieces, not new local structure.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-fresh-compositions-2026-10-14 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-fresh-compositions-2026-10-14 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-fresh-compositions-2026-10-14 check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`register-plan` prints the record entries the import needs: an evidence entry, a source
row and three beyond-horizon rows.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
