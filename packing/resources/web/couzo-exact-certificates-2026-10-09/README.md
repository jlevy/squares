# Francisco Couzo’s Exact Certificates at 02f9690

[Issue #476](https://github.com/jlevy/squares/issues/476) reports six exact rational
packings, at n = 132, 237, 263, 267, 270 and 303, from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/02f969075f79d5e13fa21e09e381a44e8647b452/certificates)
at `02f969075f79d5e13fa21e09e381a44e8647b452` (tree
`a11227bc2ecbc9b22af11ea4f4a0dd2c9bc62866`, committed 2026-10-09T20:28:52Z, parent
`2d32a6e`). The commit holds 65 certificates, one per packing in the repository; this
packet retains all 65 and compares each with the record.

| n | Exact side of the certificate | Rounded up at 16 places | The issue prints |
| --- | --- | --- | --- |
| 132 | `11986954193640392741450366579623/1000000000000000000000000000000` | 11.9869541936403928 | 11.986954193641 |
| 237 | `3975917726395155753617729398543/250000000000000000000000000000` | 15.9036709055806231 | 15.903670905581 |
| 263 | `7488939206954142477014939239/447356905819500000000000000` | 16.7404126538191566 | 16.740412653820 |
| 267 | `4209703817487065565108620335551/250000000000000000000000000000` | 16.8388152699482623 | 16.838815269949 |
| 270 | `16936720031121015799532991452837/1000000000000000000000000000000` | 16.9367200311210158 | 16.936720031122 |
| 303 | `2239680490686779486489623667067/125000000000000000000000000000` | 17.9174439254942359 | 17.917443925495 |

Each certificate gives `n` unit squares, each a rational centre in $[0, S]^2$ and a
rational $t = \tan(\theta/2)$, in a square of the stated side, in Evan Daniel’s format.
Each exact side rounds up, at the 12 places the issue prints, to the side it prints.
The source calls five of the six exact optima from Evan Daniel’s exact contact solver
and the one at 263 a rational witness, its decimal packing with centres scaled apart by
$1 + 10^{-12}$. All six were first committed in the pinned commit.
The sources were retrieved at 2026-10-10T09:58Z.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json)
is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.

The repository states no licence: its tree has no licence file, and neither `README.md`
nor `certificates/README.md` states reuse terms.
The 65 certificates under `source/certificates/` are retained as factual data under the
owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md)); the two READMEs and the 65
decimal pose files `nN.txt` are pinned by digest only, and no prose or program is
copied. The other 59 certificates are each held to the side, rounded up at 12 places,
that the source’s own `certificates/README.md` table prints.
Seven of them, at 108, 127, 131, 155, 180, 228 and 306, are byte-identical to the issue
#451 certificates first committed in `ffd900d` (the
[issue-451 packet](../couzo-exact-refinements-2026-10-08/README.md), T-128), and four, at
84, 86, 105 and 175, to the follow-up certificates of `2d32a6e` (the
[follow-up packet](../couzo-followup-refinements-2026-10-08/README.md), T-130); the
other 54 were first committed here.

## Exact Replay

Only the retained certificates enter geometry decisions, through the maintained two-route
kernel of `devtools.evand_arrangement_reports` that the issue-399, issue-465 and Couzo
follow-up imports used: `sqpack`’s exact witness verifier and the independent rational
corner checker, each deciding every wall and every pair over $\mathbb{Q}$ after an exact
half-angle conversion. The replay covers the declared roster of 17 counts: the six the
issue reports and the eleven cheapest of the others, 68, 84, 86, 102, 103, 105, 106, 108,
110, 127 and 131, whose jobs take seconds each. Each count runs a positive job, a
duplicate-square control and an outside-container control, each in its own child
process.

All 17 positives pass both routes, and both routes refuse all 34 controls, each on the
overlap or the wall it was built to break.
In every positive both routes find the same least wall clearance and least pair gap: at
every count but 263 the wall clearance is exactly `1/200000000000000000000`
($5 \times 10^{-21}$) and the pair gap just under $10^{-20}$; at 263, the rational
witness, they are $10^{-15}$ and $1.58 \times 10^{-12}$. The 51 jobs made 1,486,686 pair
decisions in 338.07 route CPU seconds and 958.00 job wall seconds, summed; the longest
job took 99.13 seconds, and the two-worker run 8 minutes 32 seconds of wall time.
Other lanes held the machine at a load average of 10 to 15 on four cores throughout, so
the walls overstate the work and the route CPU seconds do not.
A serial `check --n 68 84 --replay` reproduced those six jobs apart from timing in 11.0
seconds. [receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)
keeps every deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. No source program ran here, and the other 48 certificates were not replayed.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes every certificate against the
record as it stood when the issue was read (`main` at `657cc4861`, 10 October 2026), and
`check-claims` rebuilds it, each case ceiling from its holder’s own retained packet.
The six the issue reports:

| n | Case ceiling, holder | Below it by | Other pending reports at the count | Smallest |
| --- | --- | --- | --- | --- |
| 132 | 11.9913278876915015, Evan Daniel’s exact optimum of Couzo’s packing (T-098) | $4.37 \times 10^{-3}$ | T-131 (#465) above by $1.45 \times 10^{-4}$; #470 prints 11.986956226066, above by $2.03 \times 10^{-6}$ | this certificate |
| 237 | 15.9036762351891381, Gupta’s refinement of SQUISH (T-127) | $5.33 \times 10^{-6}$ | #481 prints 15.902989220874966, below by $6.82 \times 10^{-4}$; #470 above | #481 |
| 263 | 16.7404196795387766, SQUISH (T-116) | $7.03 \times 10^{-6}$ | #481 prints 16.733166007899882, below by $7.25 \times 10^{-3}$; #470 above | #481 |
| 267 | 16.8388319611168389, Ryan Xu (T-125) | $1.67 \times 10^{-5}$ | #470 prints 16.838828608296, above by $1.33 \times 10^{-5}$ | this certificate |
| 270 | 16.9378072284460292, Evan Daniel (T-119) | $1.09 \times 10^{-3}$ | T-130 (#460) above by $2.99 \times 10^{-6}$; #481 prints 16.929780126241173, below by $6.94 \times 10^{-3}$; #470 above | #481 |
| 303 | 17.9203123729203498, SQUISH (T-113) | $2.87 \times 10^{-3}$ | #481 prints 17.913065462738533, below by $4.38 \times 10^{-3}$; #470 above | #481 |

A side a report prints, and does not retain here, is compared at its printed places: one
unit in the last place below it where the report says it rounded up, and one unit either
way where it does not.
Issue #476 quotes Mishapolk’s sides at 132 and 267 as 11.986956226077 and
16.838828608311; the record compares the 12-place ceilings Mishapolk’s own README
prints, 11.986956226066 and 16.838828608296. Either way the certificate is smaller.

The 59 certificates the issue does not name are imports of their own
(`result-import.md`, stage 1), compared here and registered by no entry of this
import:

- **Equal to the case ceiling, 23.** At 106, 110, 152, 156, 172, 177, 181, 182, 206,
  210, 240, 241, 259, 268, 269, 271, 273, 297, 301, 304, 305 and 307 the side is exactly
  Evan Daniel’s exact optimum of Couzo’s packing (T-098), and at 208 exactly Gupta’s
  certificate (T-127). At 106, 152 and 177 the exact algebraic sides T-121, T-122 and
  T-123 report are smaller still, by about $10^{-19}$; at 259, 269, 305 and 307 issue
  #481’s printed sides are smaller.
- **Below the case ceiling, 11: the byte-identical earlier certificates.** At 108, 127,
  131, 155, 180, 228 and 306 the certificate is T-128’s, and at 84, 86, 105 and 175
  T-130’s, so each ties the register entry already pending there.
- **Above the case ceiling, 5.** At 68 by $8.80 \times 10^{-20}$ (Rehwaldt, T-118), 102
  by $1.35 \times 10^{-3}$ and 103 by $2.43 \times 10^{-2}$ (Ryan Xu, T-125), 272 by
  $5.57 \times 10^{-5}$ (Evan Daniel, T-119), and 292 by $5.96 \times 10^{-11}$
  (Rehwaldt, T-117). The source itself marks 102, 103 and 272 superseded.
- **Beyond the horizon, 20.** At 332, 336 to 341, 369, 373 to 379 the side is below the
  current tracked beyond-horizon row, by $4.45 \times 10^{-12}$ up to
  $4.00 \times 10^{-4}$ (at 378; $4.29 \times 10^{-5}$ at 375).
  At 327, 335, 342, 364 and 372, the rational witnesses, it is above Couzo’s own earlier
  decimal report by about $1.8 \times 10^{-11}$.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The source’s statements that five of the six lie within about $10^{-19}$ of their KKT
points and that a corner-to-corner search finds no first-order descent in any branch
are the author’s, and were not replayed here.
Novelty, local or global optimality and rigidity are not established, and no review of
the replay has been made.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificates are kept as
factual data and nothing of the source is relicensed.
The issue asks that the starting packings be credited: Mishapolk’s at 132 (#470), Nate
Chaoweeraprasit’s SQUISH packings at 237, 263 and 303 (237 through Siddharth Gupta’s
refinement, #438), Ryan Xu’s at 267 (#432) and Evan Daniel’s at 270 (#399).
The search used David Ellsworth’s `refine_packing` and Evan Daniel’s `fq`, and Evan
Daniel’s exact contact solver wrote the five exact optima.
The issue states that the search code and the request were written with Claude (Claude
Code) under the author’s direction, and the pinned commit names Claude as co-author.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-exact-certificates-2026-10-09 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-exact-certificates-2026-10-09 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-exact-certificates-2026-10-09 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-exact-certificates-2026-10-09 check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job directory,
and `register-plan` prints the record entries the import needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
