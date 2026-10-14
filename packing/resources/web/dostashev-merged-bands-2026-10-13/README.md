# Daniil Ostashev’s Merged-Band Packings at b909e1b

[Issue #575](https://github.com/jlevy/squares/issues/575) reports new packings of 176,
211 and 241 unit squares and, since an edit of 2026-10-13T04:13Z, of 304, from
[dostashev/square-packing](https://github.com/dostashev/square-packing/tree/b909e1b74cda50906e12b4373e010ddee39e47e4).
The edited issue names commit `b909e1b74cda50906e12b4373e010ddee39e47e4` (tree
`e2e293d66e4a4439d78da9a184df3688da5ec7de`, committed 2026-10-13T03:03:29Z) with the
SHA-256 of its eight files, and the author’s comment of the same minute says the 176,
211 and 241 files are unchanged from `b572f10`, the commit the issue first named.
The packet pins `b909e1b`, the head when the sources were retrieved at
2026-10-14T06:54Z.

| n | The issue prints, rounded up | Rounded up at 16 places | First committed |
| --- | --- | --- | --- |
| 176 | 13.79587231843640726331185405391207744387 | 13.7958723184364073 | `e54ac1b` (2026-10-12T23:06:00Z) |
| 211 | 14.99369418658324657063591818176125142354 | 14.9936941865832466 | `b572f10` (2026-10-13T00:41:41Z) |
| 241 | 15.98713424905084041461665739745571396866 | 15.9871342490508405 | `b572f10` (2026-10-13T00:41:41Z) |
| 304 | 17.92942775807517496566632613898911486244 | 17.9294277580751750 | `b909e1b` (2026-10-13T03:03:29Z) |

Each certificate, `records/n0NNN.sqcert`, is in the `.sqcert` format the
[issue-501 packet](../dostashev-records-2026-10-11/README.md) describes, read through
the `sqcert` adapter of `devtools.upper_bound_reports`. Each exact side is the
`claimed_s` of its header times $1 + \delta$ for the `delta` the header states, as a
test holds. The issue gives $\delta = 10^{-60}$ for all four, and so do the headers at
176, 211 and 241; the 304 header states a 59-digit optimum and $\delta = 10^{-59}$, and
its side is that optimum times $1 + 10^{-59}$.

The 211 certificate replaces, in the author’s repository, the issue-501 packing that
T-149 registers; the issue says it is a different packing, not a refinement of that one.
By the import process it is a new claim, and T-149 keeps its own.

## Retained Here

The repository is MIT-licensed (`LICENSE`, Copyright (c) 2026 Daniil Ostashev), and its
README says the licence covers the verification code and the record packings and
certificates.
`devtools.acquire_source` wrote the packet from a checkout at the pin, from
the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest,
each of its 56 files, 1,844,269 bytes, bound to its Git blob at the pin.
Ten files are retained byte-identical under `source/`, 656,939 bytes:

| Upstream path | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- |
| `records/n0176.sqcert` | 89349 | `f70f484dfeb7057fd23c57859eac8d77bc4554e3d6aa6df1425ae5cdd2e9ef39` | The n = 176 certificate |
| `records/n0211.sqcert` | 109351 | `7d35edaac371fd7b2a32517bd52dd0fd8b58d9ae9642008112496f80b58bf310` | The n = 211 certificate |
| `records/n0241.sqcert` | 123345 | `8d67da52a9445c38f28f5cea24169bcd3a421c39db581a5a5bf779c0d4cdf962` | The n = 241 certificate |
| `records/n0304.sqcert` | 154893 | `b87d0c9df7336872a2e0c26b761a1d7030b8850c2cf385bec43126f62c270c71` | The n = 304 certificate |
| `records/n0NNN.sqpk` |  | in the manifest | The 60-digit decimal packings of the four |
| `README.md`, `LICENSE` |  | in the manifest | Author prose and the licence |

The other 46 files are pinned by digest only.
Thirty-four, the 155 and 156 records, the author’s C++ GMP checker, its tests, the
mpmath cross-check and the driver, are unchanged since `c3d17ab` and are compared with
the identical copies the issue-501 packet retains.
Twelve are the 129, 175, 204, 232, 264 and 303 records of issues #528 and #562, which
`883aa4b` (2026-10-12T20:25:20Z) rewrote in canonical form; read with the same adapter
from a checkout at the pin, each rewritten certificate states exactly the side of the
file its issue names, and those files are retained by
[issue 562’s packet](../dostashev-compositions-2026-10-12/README.md) and by issue 528’s
import. No source program ran here.

## Exact Replay

Only the retained certificates enter geometry decisions, through the maintained
two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`’s exact witness
verifier and the independent rational corner checker, each deciding every wall and every
pair over $\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on one worker.

All four positives pass both routes, and both routes refuse all eight controls, each on
the overlap or the wall it was built to break.
In every positive the two routes find the same least wall clearance, at least
$5.00 \times 10^{-21}$, and the same least pair gap, at least $4.99 \times 10^{-21}$ and
just under $5 \times 10^{-21}$ at 176 and 304, as the issue reports.
The twelve jobs made 675,186 pair decisions in 480.19 route CPU seconds and 656.86 job
wall seconds, summed; the longest, the outside-container control at 304, took 89.14
seconds. The one-worker run took 11 minutes 9 seconds of wall time with the machine at a
load of 9 to 12. A fresh serial `check --replay` decided all twelve jobs again, equal to
the retained rows apart from timing, in 11 minutes 34 seconds.
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
The other reports are compared at the places they print: Francisco Couzo’s round up at
12 places, and #593’s 16 places state no rounding, so its side may be one unit either
way.

| n | Case ceiling, holder | Below it by | Other reports at the count | Smallest |
| --- | --- | --- | --- | --- |
| 176 | 13.8128562532770564, Nate Chaoweeraprasit (T-151) | $1.70 \times 10^{-2}$ | #561 (Couzo) 13.807637227056, above by $1.18 \times 10^{-2}$; the author’s own `fe43a64` 176, above by $1.28 \times 10^{-2}$; #593 prints 13.7958723184364072, undecided | this certificate or #593, undecided at #593’s print |
| 211 | 14.9963367213363157, the author’s own issue-501 packing (T-149) | $2.64 \times 10^{-3}$ | #583 (Couzo) 14.993558914123, #586 (Couzo) 14.993558913975 and #593 14.9935589139740060, each below this side by $1.35 \times 10^{-4}$ | #586 or #593 |
| 241 | 15.988132439524990848590591447359, Francisco Couzo’s packing in Evan Daniel’s exact optimum (T-098) | $9.98 \times 10^{-4}$ | #583 15.987117095169, #586 15.987117095151 and #593 15.9871170951502393, each below this side by $1.72 \times 10^{-5}$ | #586 or #593 |
| 304 | 17.9295659468485010, Francisco Couzo’s refinement of Nate Chaoweeraprasit’s packing (T-152) | $1.38 \times 10^{-4}$ | #593 prints 17.9294277580751746, $3.7 \times 10^{-16}$ below this side | #593 at its print; this certificate measured exactly (below) |

Every other register upper bound at these counts with a retained reader was rebuilt here
and is larger than the certificate at its count: T-101 at 176, T-098 at 211, 241 and
304, and T-151 at 304. T-056 and T-057 print larger sides and have no reader.

At 211 and 241, Francisco Couzo’s #583 and #586 say they continue this author’s
arrangements, and are smaller.
Issue #593’s certificates at `Mishapolk/square-packing-records` `46f638c`, fetched here
to scratch with the SHA-256 the issue prints and read with this importer’s Evan
Daniel-format adapter, state at 211 and 241 exactly the sides of Couzo’s `b85dee2`
certificates, the #586 sides, so those two are one exact side.
At 176 and 304 the same certificates state these certificates’ sides rounded up at 30
and 29 places, $9.2 \times 10^{-31}$ and $8.9 \times 10^{-31}$ above them: #593’s
16-place prints are binary64 renderings, not its sides, and measured exactly this
certificate is the smallest at 176 and 304. Francisco Couzo’s head `b85dee2` holds
13.807637226803 at 176 and T-152’s side at 304, both above.
No other open report of the 14 October intake names these counts, and no open pull
request moves a bound at them.

## What Is Not Established

The issue states that each side is the exact first-order optimum of its contact
topology, with nonnegative KKT multipliers at a 60-digit solution reached by two routes
that agree, and the load-bearing squares scaled by $1 + 10^{-20}$. That is the author’s
report of local optimality, not a bound, and nothing here checks it.
Neither the author’s C++ checker nor the mpmath cross-check ran here.
The certificates establish finite upper bounds only; whether each is a new arrangement,
as the issue says, is not measured here.

## Credit

The issue credits Daniil Ostashev with the four packings and asks that the seeds’
authors (Francisco Couzo, Evan Daniel, Joost de Winter) and the composition pieces’
sources be acknowledged.
At 176, 211 and 241 a packing whose tilted squares form two bands was re-hardened on a
GPU with every square soft and the box held (soft-to-rigid, after Yohei Nakajima’s
idea), and the bands merged into one V:

- 176, from the author’s earlier composition of #528’s 38-square piece and #562’s
  44-square piece, a V of 63 tilted squares;
- 211, from Evan Daniel’s exact optimum of Joost de Winter’s packing, bands of 48 and
  25, a V of 76;
- 241, from Evan Daniel’s exact optimum of Francisco Couzo’s packing, the case’s house,
  bands of 47 and 32, a V of 85.

At 304 the same re-hardening relaxed the author’s composition of a 55-square
$(h + 8) \times h$ piece and a 68-square $(h + 7) \times h$ piece, from 17.939518, as
its aligned blocks shifted; its two tilted bands stay separate.
The README at the pin also states that Couzo improved the author’s 156 and first 176,
each from the author’s packing; those are Couzo’s claims.
The issue states AI assistance: an AI-assisted research loop the author drives with his
own ideas, merging the bands through the junction being his; AI agents wrote and ran the
search and verification code, and an agent extended the move from his compositions to
published two-band packings.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source dostashev-merged-bands-2026-10-13 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports dostashev-merged-bands-2026-10-13 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports dostashev-merged-bands-2026-10-13 check --replay
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
