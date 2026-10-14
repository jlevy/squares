# Daniil Ostashev’s Cut-Out and Composition Packings at fe43a64

[Issue #562](https://github.com/jlevy/squares/issues/562) reports new packings of 129,
204 and 303 unit squares from
[dostashev/square-packing](https://github.com/dostashev/square-packing/tree/fe43a64ecf2581cdbd11830e8a5be0989746c5d3)
at commit `fe43a64ecf2581cdbd11830e8a5be0989746c5d3` (tree
`2f9b1db8d4e1cf8db4056aaa6f1ee94cad6a2f9a`, committed 2026-10-12T17:19:33Z), which the
issue names with the SHA-256 of its six files.
The packet pins that commit; the sources were retrieved at 2026-10-14T06:54Z. The issue
was filed at 2026-10-12T19:10:14Z and has not been edited.

| n | The issue prints, rounded up | Rounded up at 16 places | First committed |
| --- | --- | --- | --- |
| 129 | 11.87001385040446434457885353928463864242 | 11.8700138504044644 | `fe43a64` (2026-10-12T17:19:33Z) |
| 204 | 14.80866323438695656647099008094596479529 | 14.8086632343869566 | `fc4bec4` (2026-10-12T14:25:07Z) |
| 303 | 17.90995829106990798159574108139873608005 | 17.9099582910699080 | `97af0a5` (2026-10-12T14:51:10Z) |

Each certificate, `records/n0NNN.sqcert`, gives a rational side and, for every unit
square, a rational centre in $[0, S]^2$ and a rational $t = \tan(\theta/2)$, in the
`.sqcert` format the [issue-501 packet](../dostashev-records-2026-10-11/README.md)
describes and `devtools.upper_bound_reports` reads through its `sqcert` adapter.
Each exact side is the 60-digit `claimed_s` of its header times $1 + 10^{-60}$, as the
header says and a test holds, and the issue prints it rounded up at 38 places.

## Which Revision

The head has moved since the issue named `fe43a64`. Commit `883aa4b`
(2026-10-12T20:25:20Z) rewrote the 129, 204 and 303 files in canonical form, moving
aligned loose squares into the corner blocks they can slide into, and the head when the
sources were retrieved, `b909e1b` (issue #575), keeps those rewrites.
Read with the same adapter, each rewritten certificate states exactly the side of the
file the issue names, so this packet keeps the bytes the issue names and its digests.
The [issue-575 packet](../dostashev-merged-bands-2026-10-13/README.md) pins the rewrites
by digest.

The README at the pin also prints $s(176) \le 13.808663234386957$, a composition the
issue does not ask for: Francisco Couzo has improved it from this packing (#561), and
#575 reports a smaller 176 of the author’s own.
Its certificate is retained and compared below, and was not replayed.

## Retained Here

The repository is MIT-licensed (`LICENSE`, Copyright (c) 2026 Daniil Ostashev), and its
README says the licence covers the verification code and the record packings and
certificates.
`devtools.acquire_source` wrote the packet from a checkout at the pin, from
the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest,
each of its 52 files, 1,456,157 bytes, bound to its Git blob at the pin.
Ten files are retained byte-identical under `source/`, 564,351 bytes:

| Upstream path | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- |
| `records/n0129.sqcert` | 62899 | `6ee26567f49a700822840807ea97947647bcdbf110e656041c0e2fe970624e72` | The n = 129 certificate |
| `records/n0204.sqcert` | 105235 | `9d6261e7bbd83ddb8aee29e6f713c403e07d07e3e436f51ec09037b3c241ffa0` | The n = 204 certificate |
| `records/n0303.sqcert` | 151314 | `f8c22f3c00cf40bab8e6edd33ccd58f99f4837d5ccad717bbb1ef964986c3f58` | The n = 303 certificate |
| `records/n0176.sqcert` | 87500 | `e14b16cd4bdd68e4716617ca561ab3462614eab75eed9a8407f6aee6b31a6053` | The unrequested 176 certificate |
| `records/n0NNN.sqpk` |  | in the manifest | The 60-digit decimal packings of the four |
| `README.md`, `LICENSE` |  | in the manifest | Author prose and the licence |

The other 42 files are pinned by digest only.
Thirty-six, the 155, 156 and 211 records, the author’s C++ GMP checker, its tests, the
mpmath cross-check and the driver, are unchanged since `c3d17ab` and are compared with
the identical copies the issue-501 packet retains.
The six files at 175, 232 and 264 are issue #528’s, unchanged since `a8db6ff`, and that
import (think-em0b) retains them.
No source program ran here.

## Exact Replay

Only the retained certificates at 129, 204 and 303 enter geometry decisions, through the
maintained two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`’s exact
witness verifier and the independent rational corner checker, each deciding every wall
and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on one worker.

All three positives pass both routes, and both routes refuse all six controls, each on
the overlap or the wall it was built to break.
In every positive the two routes find the same least wall clearance, at least
$5.00 \times 10^{-21}$, and the same least pair gap, at least $4.99 \times 10^{-21}$,
which comes from the $1 + 10^{-20}$ scaling of the load-bearing squares that the issue
describes. The nine jobs made 448,290 pair decisions in 363.99 route CPU seconds and
447.45 job wall seconds, summed; the longest, the 303 positive, took 85.77 seconds.
The one-worker run took 7 minutes 38 seconds of wall time with the machine at a load of
10 to 14. A fresh serial `check --replay` decided all nine jobs again, equal to the
retained rows apart from timing, in 7 minutes 4 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code, and the third exact route
(`devtools.check_half_angle_area`) has not read these certificates.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record at `main` `aeef99ef0` (14 October 2026); `check-claims` rebuilds it, each case
ceiling from its holder’s own packet.

| n | Case ceiling, holder | Below it by | Other reports at the count | Smallest |
| --- | --- | --- | --- | --- |
| 129 | 11.8720298490811800, Ryan Xu’s packing in Evan Daniel’s regularization (T-146) | $2.02 \times 10^{-3}$ | #593 prints 11.8700138504044652 | this certificate |
| 204 | 14.82287565553229 = 27/2 + √7/2 in the catalogue; verified at 14.82287565553230 by Evan Daniel’s exact ceiling (T-101, T-155) | $1.42 \times 10^{-2}$ | #593 prints 14.8086632343869571 | this certificate |
| 303 | 17.9130654627385324, Nate Chaoweeraprasit’s packing in Evan Daniel’s regularization (T-146) | $3.11 \times 10^{-3}$ | #593 prints 17.9099582910699091 | this certificate |
| 176, not requested | 13.8128562532770564, Nate Chaoweeraprasit (T-151) | $4.19 \times 10^{-3}$ | #561 (Couzo) 13.807637227056, #575 and #593 are each smaller, by $1.03 \times 10^{-3}$, $1.28 \times 10^{-2}$ and $1.28 \times 10^{-2}$ | #575 or #593, undecided at #593’s print |

Every other register upper bound at these counts with a retained reader was rebuilt here
and is larger than the certificate at its count: T-101, T-113, T-115, T-125 and T-127 at
129, and T-098, T-113, T-134, T-136 and T-138 at 303. T-056 and T-092 at 303 print
larger sides and have no reader.

Issue #593 (Mishapolk) prints a 16-place side at each count, below which the frozen
record finds each certificate by $5 \times 10^{-16}$ to $1.1 \times 10^{-15}$, with the
print read as one unit either way.
Those prints are binary64 renderings rather than its certificates’ sides.
Its certificates at `Mishapolk/square-packing-records` `46f638c`, fetched here to
scratch with the SHA-256 the issue prints and read with this importer’s Evan
Daniel-format adapter, state at 129, 204 and 303 exactly the sides of these certificates
rounded up at 30 places, above them by $3.6 \times 10^{-31}$, $3.5 \times 10^{-32}$ and
$2.6 \times 10^{-31}$. No other open report of the 14 October intake names 129, 204 or
303, and no open pull request moves a bound at them.

## What Is Not Established

The issue states that each side is the exact first-order optimum of its contact
topology: nonnegative KKT multipliers at a 60-digit solution, with the load-bearing
squares scaled by $1 + 10^{-20}$. That is the author’s report of local optimality, not a
bound, and nothing here checks it.
Neither the author’s C++ checker nor the mpmath cross-check ran here.
The certificates establish finite upper bounds only, and nothing here decides whether
129 is a placement of Ryan Xu’s packing, which the issue says it is not.

## Credit

The issue credits Daniil Ostashev with the three packings and leaves the pieces’
acknowledgement to the record.
It says 204 and 303 are new arrangements: two copies of a new rectangle packing, 44 unit
squares in an $(h + 3) \times h$ rectangle at 204 and 62 in an $(h + 6) \times h$
rectangle at 303, in opposite corners with aligned squares filling the rest.
Both rectangles came from the GPU soft-to-rigid search of #528, after Yohei Nakajima’s
idea, started from corner staircases.
129 is a cut-out: a 163-square $(h + 3) \times h$ rectangle cut from the s(302) house,
Nate Chaoweeraprasit’s packing in Evan Daniel’s regularization, re-optimised as a
rectangle, less its three rightmost unit columns.
Its aligned blocks are laid out like Ryan Xu’s s(129), and its tilted squares sit in a
different band. The README credits this project’s fixed-angle linear program and Ryan
Xu’s certificate construction as methods.
The issue states AI assistance: an AI-assisted research loop the author drives with his
own ideas, the rectangle library and composition being his, in which AI agents wrote and
ran the search, composition and verification code, and an agent’s check of the library
against the register found 129.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source dostashev-compositions-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports dostashev-compositions-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports dostashev-compositions-2026-10-12 check --replay
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
