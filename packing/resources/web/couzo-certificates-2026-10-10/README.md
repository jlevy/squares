# Francisco Couzo’s Exact Certificates at 3ef7634

[Issue #488](https://github.com/jlevy/squares/issues/488) reports six exact rational
packings, at n = 132, 175, 209, 237, 270 and 305, from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/3ef76349025bf4bfa99c9c3600bcc273f4c33e02/certificates)
at `3ef76349025bf4bfa99c9c3600bcc273f4c33e02` (tree
`2978a99cdbb71c3221956d59b9606c3a7a40ad94`, committed 2026-10-10T13:52:27Z, parent
`9bf90e7`). The issue was filed at 2026-10-10T14:08Z.

| n | Exact side of the certificate | Rounded up at 16 places | The issue prints |
| --- | --- | --- | --- |
| 132 | `11986953587254420950497823747297/1000000000000000000000000000000` | 11.9869535872544210 | 11.986953587255 |
| 175 | `860445045293269576081339809497/62500000000000000000000000000` | 13.7671207246923133 | 13.767120724693 |
| 209 | `14946223226446451055256712327571/1000000000000000000000000000000` | 14.9462232264464511 | 14.946223226447 |
| 237 | `99393435047986448060704927533/6250000000000000000000000000` | 15.9029496076778317 | 15.902949607678 |
| 270 | `2116221919192669947792003526953/125000000000000000000000000000` | 16.9297753535413596 | 16.929775353542 |
| 305 | `8975569886103498772971256586313/500000000000000000000000000000` | 17.9511397722069976 | 17.951139772207 |

Each certificate gives `n` unit squares, each a rational centre in $[0, S]^2$ and a
rational $t = \tan(\theta/2)$, in a square of the stated side, in Evan Daniel’s format.
Each exact side rounds up, at the 12 places the issue prints, to the side it prints.
The source calls all six exact optima from Evan Daniel’s exact contact solver.

## What the Commit Changes

The [issue-476 packet](../couzo-exact-certificates-2026-10-09/README.md) retained all 65
certificates of `02f9690`. Two commits follow it.
`9bf90e7` removes 102, 103 and 272, which the source marks superseded.
The pinned commit adds one certificate and changes eight:

- **Added, 1:** 209.
- **Changed and named by the issue, 5:** 132, 175, 237, 270 and 305.
- **Changed and not named by the issue, 3:** 303, inside the case corpus, and 338 and
  340, beyond it.

The other 54 certificates of the pin are unchanged since `02f9690`: 68, 84, 86, 105,
106, 108, 110, 127, 131, 152, 155, 156, 172, 177, 180, 181, 182, 206, 208, 210, 228,
240, 241, 259, 263, 267, 268, 269, 271, 273, 292, 297, 301, 304, 306, 307, 327, 332,
335, 336, 337, 339, 341, 342, 364, 369, 372 to 379. The issue-476 claim record already
compares each. This packet pins each one by digest and names the issue-476 copy as
`identical_to`. `acquire_source --check` compares those bytes again on every run.
In all, the commit holds 63 certificates.
Each one’s SHA-256 starts with the 16 hex digits that the `certificates/README.md` table
prints for it.

All nine added or changed certificates were first committed in the pinned commit.
The sources were retrieved at 2026-10-10T16:44Z.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
74 files, 2,610,667 bytes.

The repository states no licence: its tree has no licence file, and neither `README.md`
nor `certificates/README.md` states reuse terms.
The nine certificates under `source/certificates/` (360,513 bytes) are retained as
factual data under the owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md)). The two READMEs and the
nine changed decimal pose files `nN.txt` are pinned by digest only.
No prose or program is copied.
The certificates at 303, 338 and 340 are each held to the side, rounded up at 12 places,
that the source’s own `certificates/README.md` prints: 17.917365675353, 18.907150436394
and 18.939701150684.

## Exact Replay

Only the retained certificates enter geometry decisions.
They go through the maintained two-route kernel of `devtools.evand_arrangement_reports`,
which the issue-399, issue-465 and issue-476 imports also used.
The two routes are `sqpack`’s exact witness verifier and the independent rational corner
checker. Each decides every wall and every pair over $\mathbb{Q}$ after an exact
half-angle conversion.
The replay covers all nine certificates the commit adds or changes.
Each count runs a positive job, a duplicate-square control and an outside-container
control, each in its own child process.

All nine positives pass both routes.
Both routes refuse all 18 controls, each on the overlap or the wall it was built to
break. In every positive the two routes find the same least wall clearance, exactly
`1/200000000000000000000` ($5 \times 10^{-21}$), and the same least pair gap, just under
$10^{-20}$. The 27 jobs made 1,899,504 pair decisions in 388.0 route CPU seconds and
393.15 job wall seconds, summed.
The longest job, the outside-container control at 340, took 25.21 seconds, and the
two-worker run took 3 minutes 30 seconds of wall time.
A fresh serial `check --replay` decided all 27 jobs again, equal to the retained rows
apart from timing, in 6 minutes 42 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. The register entry would cite the six requested certificates.
Each was also decided by the third exact route,
`devtools.check_half_angle_area decide-imports`, which reads the certificate with its
own parser and decides containment by each square’s half-extent and overlap by exact
clipping. That route accepts all six and reaches the required outcome on all 36 of its
controls. It finds the same least wall clearances as both maintained routes and a least
Euclidean distance between squares of $1.00 \times 10^{-20}$ at every count.
Run as `decide-imports --imports '#488' '#489'` with `--upstream` for both packets,
which also holds each retained certificate to its bytes fetched at the pin, it found no
disagreement across the ten certificates of the two imports, in 19 seconds on two
workers. The third route does not read the certificates at 303, 338 and 340, which no
entry cites. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes every certificate against the
record as it stood when the issue was read (`main` at `af17208c0`, 10 October 2026).
`check-claims` rebuilds it, each case ceiling from its holder’s own retained packet and
each issue-476, T-130 and T-131 side from its own packet.
The six the issue reports:

| n | Case ceiling, holder | Below it by | Other pending reports at the count | Smallest |
| --- | --- | --- | --- | --- |
| 132 | 11.9913278876915015, Evan Daniel’s exact optimum of Couzo’s packing (T-098) | $4.37 \times 10^{-3}$ | #476 above by $6.06 \times 10^{-7}$; #470 prints 11.986956226066, above by $2.64 \times 10^{-6}$; T-131 (#465) above by $1.46 \times 10^{-4}$; #489 prints 11.985680198845808811522231964102, below by $1.27 \times 10^{-3}$ | #489 |
| 175 | 13.7688992766137689, Ryan Xu (T-125) | $1.78 \times 10^{-3}$ | T-130 (#460) and #476, the same certificate, above by $3.44 \times 10^{-5}$; #470 prints 13.767155163551, above by $3.44 \times 10^{-5}$ | this certificate |
| 209 | 14.9496179522003981, Gupta’s refinement of SQUISH (T-127) | $3.39 \times 10^{-3}$ | #481 prints 14.946223654487920, above by $4.28 \times 10^{-7}$; #470 above | this certificate |
| 237 | 15.9036762351891381, Gupta’s refinement of SQUISH (T-127) | $7.27 \times 10^{-4}$ | #481 prints 15.902989220874966, above by $3.96 \times 10^{-5}$; #476 above by $7.21 \times 10^{-4}$; #470 above | this certificate |
| 270 | 16.9378072284460292, Evan Daniel (T-119) | $8.03 \times 10^{-3}$ | #481 prints 16.929780126241173, above by $4.77 \times 10^{-6}$; #476 and T-130 (#460) above by $6.94 \times 10^{-3}$ and $6.95 \times 10^{-3}$; #470 above | this certificate |
| 305 | 17.9529594590155280, Evan Daniel’s exact optimum of Couzo’s packing (T-098) | $1.82 \times 10^{-3}$ | #481 prints 17.951196144147385, above by $5.64 \times 10^{-5}$; #476 equals the case ceiling | this certificate |

A side a report prints, and does not retain here, is compared at its printed places.
Where the report says it rounded up, the side may be up to one unit in the last place
below the print. Where it does not say, the side may be one unit either way.
Three other pending reports share no count with this release: #483 is at n = 70 alone,
#484 at 308, 343 and 344, and T-128 at eight counts from 105 to 306, none of them here.

Issue #489, filed 39 minutes after this one, reports a smaller side at 132. The
[Hunt 3 packet](../evand-record-hunt3-2026-10-10/README.md) retains it.
The Hunt 3 commit the issue names, `c013f43`, has a timestamp of 13:46:56Z, five minutes
before this pin’s. It holds a certificate at 305 that issue #489 does not name, and that
certificate’s exact side is this one’s,
`8975569886103498772971256586313/500000000000000000000000000000`. The two certificates
are the same arrangement up to a quarter turn of the box.
Matched square by square by the third route’s `arrangement_gap`, 271 of the 305 lie
within $10^{-9}$ of their counterparts and the other 34 within $1.77 \times 10^{-2}$;
the Hunt 3 solver report lists 3 free squares and 44 exact flat motions at that point.
The Hunt 3 packer log at the next commit, `76a529b`, says that this issue was filed
before `c013f43` was pushed and that both packings descend from SQUISH’s through `fq`.
It drops 305 as Couzo’s.

The issue quotes Mishapolk’s side at 132 as 11.986956226077. The record compares the
12-place ceiling that Mishapolk’s own README prints, 11.986956226066. Either way the
certificate is smaller.

The three certificates the issue does not name are each an import of their own
(`result-import.md`, stage 1). This import compares them here and registers none of
them:

- **303.** Below the case ceiling, 17.9203123729203498 (SQUISH, T-113), by
  $2.95 \times 10^{-3}$, and below the issue-476 certificate by $7.83 \times 10^{-5}$.
  Issue #481’s printed 17.913065462738533 is smaller by $4.30 \times 10^{-3}$, and the
  source marks this one superseded.
- **338 and 340, beyond the horizon.** Below the current tracked beyond-horizon rows,
  Couzo’s own decimal reports of 18.908632939046573 and 18.939879629586962, by
  $1.48 \times 10^{-3}$ and $1.78 \times 10^{-4}$. They are also below the issue-476
  certificates by $1.48 \times 10^{-3}$ and $4.67 \times 10^{-5}$. The grid’s 19 is
  above both.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The source says each of the six lies within about $10^{-19}$ of its KKT point.
It also says the corner–corner MILP finds no first-order descent in any branch.
Those statements are the author’s and were not replayed here.
Novelty, local or global optimality and rigidity are not established, and no review of
the replay has been made.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificates are kept as
factual data and nothing of the source is relicensed.
The issue asks that the starting packings be credited: Nate Chaoweeraprasit’s SQUISH
packings from #481 at 209, 237, 270 and 305, Mishapolk’s at 132 (#470) and Ryan Xu’s at
175 (#432). They were improved by Evan Daniel’s `fq` (132, 175, 209, 237 and 305), the
author’s basin hopping (175 and 270) and David Ellsworth’s `refine_packing` (132, 175
and 270). Evan Daniel’s exact contact solver wrote all six exact optima.
The issue states that the search code and the request were written with Claude (Claude
Code) under the author’s direction.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-certificates-2026-10-10 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-10 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-10 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-10 check --replay
uv run --frozen --all-extras --group dev python -m devtools.check_half_angle_area decide-imports --workers 2 --imports '#488' '#489'
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
