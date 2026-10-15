# Francisco Couzo’s Exact Certificates at 337078c

[Issue #506](https://github.com/jlevy/squares/issues/506) reports exact rational
packings at n = 304 and 305, inside the case corpus, and at n = 338, 339, 344, 375, 376,
378, 379, 380 and 381, beyond it, from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/337078ca3e05153aceb099237b175cf64af5748a/certificates)
at `337078ca3e05153aceb099237b175cf64af5748a` (tree
`2766f6aa08b1d252634eb2f00df8f6a941a1e264`, committed 2026-10-11T17:29:19Z, parent
`f311f08`). The issue was filed at 2026-10-11T18:06Z.

| n | Exact side of the certificate | Rounded up at 16 places | The issue prints |
| --- | --- | --- | --- |
| 304 | `8964782973424250487190982671787/500000000000000000000000000000` | 17.9295659468485010 | 17.929565946849 |
| 305 | `3590093296427542454697714045223/200000000000000000000000000000` | 17.9504664821377123 | 17.950466482138 |
| 338 | `18906436500551825926629088515923/1000000000000000000000000000000` | 18.9064365005518260 | 18.906436500552 |
| 339 | `3785886776761532431054552189923/200000000000000000000000000000` | 18.9294338838076622 | 18.929433883808 |
| 344 | `9497176622471721177242628290181/500000000000000000000000000000` | 18.9943532449434424 | 18.994353244944 |
| 375 | `38166979981362750351336743477/1917328312988500000000000000` | 19.9063351450084560 | 19.906335145009 |
| 376 | `4977569146721136045070070348659/250000000000000000000000000000` | 19.9102765868845442 | 19.910276586885 |
| 378 | `4985635444338702633332804918119/250000000000000000000000000000` | 19.9425417773548106 | 19.942541777355 |
| 379 | `9976786354769287275075680724899/500000000000000000000000000000` | 19.9535727095385746 | 19.953572709539 |
| 380 | `19987440766555387551986240574787/1000000000000000000000000000000` | 19.9874407665553876 | 19.987440766556 |
| 381 | `1999266328846356482088565989631/100000000000000000000000000000` | 19.9926632884635649 | 19.992663288464 |

Each certificate gives `n` unit squares, each a rational centre in $[0, S]^2$ and a
rational $t = \tan(\theta/2)$, in a square of the stated side, in Evan Daniel’s format.
Each exact side rounds up, at the 12 places the issue prints, to the side it prints.
The source calls ten of them exact optima from Evan Daniel’s exact contact solver, and
the one at 375 a rational witness: its decimal packing with centres dilated by
$1 + 10^{-11}$, the issue says. The certificate’s side exceeds the side `n375.txt` prints
by $1.89 \times 10^{-10}$, which that dilation gives for a box of side about 19.9 and
$1 + 10^{-12}$ does not; the certificates README’s general description still says
$1 + 10^{-12}$.

## What the Commit Changes

The [issue-488 packet](../couzo-certificates-2026-10-10/README.md) pinned `3ef7634`.
Two commits follow it, both on 11 October:

- `f311f08` (03:39:54Z) adds 308, 343 and 380 and changes 175, 340, 376, 378 and 379;
- `337078c` (17:29:19Z), the pin, adds 344 and 381 and changes 304, 305, 338, 339, 375,
  376, 378, 379 and 380.

Against `3ef7634` that is 15 certificates, five added and ten changed, and this packet
retains all 15:

- **Named by the issue, 11:** 304, 305, 338, 339, 344, 375, 376, 378, 379, 380 and 381,
  each first committed in the pin.
- **Not named by the issue, 4:** 175 and 308, inside the case corpus, and 340 and 343,
  beyond it, each first committed in `f311f08` and unchanged by the pin.

The other 53 certificates of the pin are unchanged since `3ef7634`: 68, 84, 86, 105, 106,
108, 110, 127, 131, 132, 152, 155, 156, 172, 177, 180, 181, 182, 206, 208, 209, 210, 228,
237, 240, 241, 259, 263, 267, 268, 269, 270, 271, 273, 292, 297, 301, 303, 306, 307, 327,
332, 335, 336, 337, 341, 342, 364, 369, 372, 373, 374 and 377.
This packet pins each one by digest and names the retained copy as `identical_to`: the
issue-488 packet’s at 132, 209, 237, 270 and 303, and the
[issue-476 packet’s](../couzo-exact-certificates-2026-10-09/README.md) at the other 48.
`acquire_source --check` compares those bytes again on every run.
In all, the commit holds 68 certificates.
For every one of them the `certificates/README.md` table prints the 16 hex digits its
SHA-256 starts with, its exact side, and that side rounded up at 12 places, and all three
agree with the file.

The sources were retrieved at 2026-10-11T20:36Z.

## Retained Here

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
85 files, 3,066,594 bytes.

The repository states no licence: its tree has no licence file, and neither `README.md`
nor `certificates/README.md` states reuse terms.
The 15 certificates under `source/certificates/` (771,778 bytes) are retained as factual
data under the owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md)). The two READMEs and the 15
changed decimal pose files `nN.txt` are pinned by digest only.
No prose or program is copied.
The certificates at 175, 308, 340 and 343 are each held to the side, rounded up at 12
places, that the source’s own `certificates/README.md` prints: 13.767119024199,
17.998459831024, 18.939649632892 and 18.993870589750.

## Exact Replay

Only the retained certificates enter geometry decisions.
They go through the maintained two-route kernel of `devtools.evand_arrangement_reports`,
which the issue-476 and issue-488 imports also used: `sqpack`’s exact witness verifier and
the independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion.
The replay covers all 15 certificates the two commits add or change, the four the issue
does not name among them.
Each count runs a positive job, a duplicate-square control and an outside-container
control, each in its own child process.

All 15 positives pass both routes.
Both routes refuse all 30 controls, each on the overlap or the wall it was built to
break. In every positive the two routes find the same least wall clearance and the same
least pair gap: exactly `1/200000000000000000000` ($5 \times 10^{-21}$) and just under
$10^{-20}$ for the 14 exact optima, and exactly `1/1000000000000000` ($10^{-15}$) and
$7.05 \times 10^{-12}$ for the rational witness at 375.
The 45 jobs made 5,234,106 pair decisions in 2,540.17 route CPU seconds and 5,568.25 job
wall seconds, summed; the longest job, the positive at 379, took 287.72 seconds.
The run used one worker on a machine shared with four other import lanes, at a load
average between 9 and 20 on four cores, so the wall times are about twice the CPU times.
`certify --workers 1` decided 42 jobs in 90 minutes, from 20:39Z, and was then stopped by
the session’s limit on a background command; the three jobs at 381 were decided by the same
`decide-job` command it runs, in 6 minutes, and `certify --finished` assembled and
admitted the receipt from all 45 job outputs, as it admits any.
A fresh serial `check --n N --replay`, run once per count, decided all 45 jobs again,
equal to the retained rows apart from timing, in 75 minutes 16 seconds summed over the
15 counts.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. The third exact route, `devtools.check_half_angle_area`, is a separate review
lane and did not run here. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes every certificate against the
record as it stood when the issue was read (`main` at `3a5a91a90`, 11 October 2026).
`check-claims` rebuilds it, each case ceiling from its holder’s own retained packet and
each issue-476, T-130, T-136, T-138, T-140, issue-484 and issue-489 side from its own
packet. The two the issue reports inside the corpus:

| n | Case ceiling, holder | Below it by | Other pending reports at the count | Smallest |
| --- | --- | --- | --- | --- |
| 304 | 17.934650018390681724105084929881, Evan Daniel’s exact optimum of Couzo’s packing (T-098) | $5.08 \times 10^{-3}$ | #476 equals the case ceiling; #500’s exact side, 17.9296570421708801 rounded up, above by $9.109 \times 10^{-5}$ | this certificate |
| 305 | 17.952959459015527962875662582531, Evan Daniel’s exact optimum of Couzo’s packing (T-098) | $2.49 \times 10^{-3}$ | #500’s exact side, 17.9505448539256365 rounded up, above by $7.837 \times 10^{-5}$; T-140 (#488), and Hunt 3’s `hunt3_n305` of the same side, above by $6.73 \times 10^{-4}$; T-136 (#481) above by $7.30 \times 10^{-4}$; #476 equals the case ceiling | this certificate |

Issue #500, SQUISH’s Mondrian packings from which both start, was filed the same day.
Its exact sides are read from its own packet
([`squish-500-fourth-request-2026-10-11`](../squish-500-fourth-request-2026-10-11/README.md))
through the importer’s `[SQUISH fourth request 2026-10-11]` reader, so the two margins
above are exact; the issue’s 15-digit prints are those sides cut, not rounded, and the
record was first frozen against them (within one unit of the print either way) before
that packet existed, with the same relations. The other reports of 11 October share no
count with this release: #501 is at 155, 156 and 211, #503 at 207, #504 at 153 and #505
at 146 and 261.

Beyond the corpus there is no case record. Each requested side is compared with the grid,
with the beyond-horizon row the source register tracks as current at its count, and with
every retained certificate there; each is the smallest, and
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the nine for `check_source_coverage`:

| n | Current beyond-horizon row | Below it by | Other reports, below each by |
| --- | --- | --- | --- |
| 338 | 18.908632939046573, Couzo (`couzo-extended-range-reports-2026-10-08`) | $2.20 \times 10^{-3}$ | #488 $7.14 \times 10^{-4}$; #476 $2.20 \times 10^{-3}$ |
| 339 | 18.930103647693699, Couzo (same) | $6.70 \times 10^{-4}$ | #476 $6.70 \times 10^{-4}$ |
| 344 | 18.994450514277401521114135796864, Evan Daniel’s Hunt 3 (#489), verified | $9.73 \times 10^{-5}$ | #484 (Fang) $1.14 \times 10^{-3}$; #470 prints 19.002369297056, $8.02 \times 10^{-3}$ |
| 375 | 19.907024692022954, Couzo (`couzo-extended-range-updates-2026-10-08`) | $6.90 \times 10^{-4}$ | #476 $6.47 \times 10^{-4}$ |
| 376 | 19.920279652318701, Couzo (`couzo-extended-range-reports-2026-10-08`) | $1.00 \times 10^{-2}$ | #476 $1.00 \times 10^{-2}$ |
| 378 | 19.946861170999796, Couzo (`couzo-extended-range-updates-2026-10-08`) | $4.32 \times 10^{-3}$ | #476 $3.92 \times 10^{-3}$ |
| 379 | 19.957538882118669, Couzo (`couzo-extended-range-reports-2026-10-08`) | $3.97 \times 10^{-3}$ | #476 $3.97 \times 10^{-3}$ |
| 380 | none | | the grid’s 20, $1.26 \times 10^{-2}$ |
| 381 | none | | the grid’s 20, $7.34 \times 10^{-3}$ |

The current rows’ decimals, as the register holds them, are compared within one unit of
their last place either way, and Hunt 3’s at 344, which is its exact side, as a side
rounded up. Issue #476’s and #488’s certificates beyond the corpus are retained but are
no register row.
The issue’s “before” column quotes the author’s own latest earlier certificate at each
count except 344: `3ef7634`’s at 338, `02f9690`’s at 339 and 375, and `f311f08`’s at
376, 378, 379 and 380, which the certificates README at `f311f08` prints as
19.914264379786, 19.942703712927, 19.953573157088 and 19.988234448072 (380 then a
rational witness). Those are not the rows the register tracks, so its margins are smaller
than the ones above. No packet retains the `f311f08` versions, and think-a4wq holds the
`02f9690` update of the tracked rows.

The four certificates the issue does not name are each an import of their own
(`result-import.md`, stage 1). This import compares them here, and the 12 October import
registered none of them:

- **175.** Below the case ceiling, 13.7688992766137689 (Ryan Xu, T-125), by
  $1.78 \times 10^{-3}$, and below T-140 (#488) by $1.70 \times 10^{-6}$, T-130 (#460)
  and the issue-476 certificate by $3.61 \times 10^{-5}$ and T-138 (#470) by
  $3.61 \times 10^{-5}$. It was the smallest side known at 175 when this import read
  it, and the source’s standing table calls it best known. Daniil Ostashev’s #528
  (T-158), registered and adopted as the house on 12 October 2026, is
  $2.94 \times 10^{-3}$ below it. The author asked on 14 October for it to be imported,
  and `T-185` registers it, superseded by `T-158`
  ([The 175 Certificate, 14 October](#the-175-certificate-14-october)).
- **308.** Below the grid’s 18 by $1.54 \times 10^{-3}$ and Kevin Fang’s T-135 (#484)
  by $8.50 \times 10^{-4}$; Evan Daniel’s T-141 (#489) is smaller by
  $1.90 \times 10^{-4}$, and the source marks this one superseded.
- **340, beyond the horizon.** Below the current tracked row, Couzo’s
  18.939879629586962, by $2.30 \times 10^{-4}$, and below the issue-488 and issue-476
  certificates by $5.15 \times 10^{-5}$ and $9.82 \times 10^{-5}$.
- **343, beyond the horizon.** Below the grid’s 19 by $6.13 \times 10^{-3}$ and Fang’s
  #484 by $1.03 \times 10^{-3}$; Hunt 3’s verified row, 18.978232523635611…, is smaller
  by $1.56 \times 10^{-2}$, and the source marks this one superseded.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The issue says all eleven pass Evan Daniel’s `verify_cert.py` and this repository’s
`sqpack` verifier; those runs are the author’s, and neither program of the source ran
here. Novelty, local or global optimality and rigidity are not established.
The stage 4 review of 12 October 2026
([review-2026-10-11-upper-bound-imports-506.md](../../../../docs/project/reviews/review-2026-10-11-upper-bound-imports-506.md))
replayed the kernel at 304, 305, 344 and 381, decided all eleven requested certificates
on the third exact route and measured the lineage the issue states.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificates are kept as
factual data and nothing of the source is relicensed.
The issue asks that the constructions each started from be credited.
At 304 and 305 they are Nate Chaoweeraprasit’s SQUISH Mondrian packings (#500), improved
by Evan Daniel’s `fq` at 304 and by the author’s search cycle with David Ellsworth’s
`refine_packing`, basin hopping and LP at 305. At 344 it is Kevin Fang’s 344 (#484),
improved by the author’s basin hopping. 338, 339, 375, 376, 378, 379, 380 and 381 each
start from one of the author’s smaller packings with an L-shaped border row added and
squares removed: 338 and 375 from his 303, itself from SQUISH’s (#401); 339 and 376 from
his earlier 304; 378 from 306; 379 from 342; and 380 and 381 from his 343 and 344, both
from Kevin Fang’s 344. Those searches used his basin hopping (CPU and GPU) and LP, Evan
Daniel’s `fq` and David Ellsworth’s `refine_packing`. Evan Daniel’s exact contact solver
wrote the ten exact optima.
The issue states that the search code and the request were written with Claude (Claude
Code), directed and reviewed by the author.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-certificates-2026-10-11 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-11 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-11 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-11 check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 1` writes a new receipt from a fresh job directory,
and `register-plan` prints the record entries the import needs.

## The 175 Certificate, 14 October

On 14 October 2026 at 16:38Z the author answered on #506 that the unnamed 175 certificate
should be imported (“sure, import it”). Under the owner’s per-count rule it was decidably
below every earlier report at 175 when it was first committed, on 11 October, so it is
recorded, and Daniil Ostashev’s #528 (`T-158`), $2.94 \times 10^{-3}$ below it, supersedes
it. [register-plan-n175.yaml](register-plan-n175.yaml) is the register entry, written by
hand since this packet’s declaration requests only the counts the issue names; the
certificate, its replay and its comparison are the ones above.
The records pull request of 15 October registers it as `T-185`, at V0/C0, with the
regularization of `T-140` below.
Measured against `T-140` by
[`compare_lineage.py`](../mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py),
every centre lies within 0.0113 of that certificate’s and 137 of 175 within $10^{-3}$: the
same arrangement, Ryan Xu’s as the author refined it, moved.
[review/compare_lineage-output.txt](review/compare_lineage-output.txt) is what it printed,
against `T-140`’s certificate and against `T-158`’s, another arrangement.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
