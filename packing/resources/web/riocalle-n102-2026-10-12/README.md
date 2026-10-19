# Rio Calle’s n = 102 Layout at 8313686

[Issue #529](https://github.com/jlevy/squares/issues/529) reports a packing of 102 unit
squares in a square of side 10.605828696455852, from
[riocalle/my-repo](https://github.com/riocalle/my-repo/tree/831368623f2d4dcef2e9434fd85c3e154083c97d).
This packet pins the commit the issue names, the repository’s only commit,
`831368623f2d4dcef2e9434fd85c3e154083c97d` (tree
`4895d7e92c462b4f13478c23a4bec75df4bbd8f5`, committed 2026-10-12T04:23:19Z), retrieved
at 2026-10-12T08:03Z.

The source publishes no exact certificate.
Its layout, `n102_s10.605828696455852.txt`, gives the side in a header line, `# s = …`,
and for each square its centre in $[0, s]^2$ and its rotation in radians, each as a
decimal with 18 significant digits.
The author’s exact certificate comes from a private search engine and cannot be
replayed, so the record’s exact certificate is derived here from the layout.

## Retained Here

The tree has no licence file and its README states no reuse terms, so the packet keeps
no upstream byte. [acquisition/sources.json](acquisition/sources.json) binds all eleven
files of the tree to their Git blobs at the pin and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) to their
SHA-256 digests. What the packet keeps is derived: the exact certificate as a rational
Witness/v2, [facts/n-102.yaml.gz](facts/n-102.yaml.gz), which
`devtools.upper_bound_reports derive` writes only from a checkout that yields this
packet’s acquisition record, and which names the digest of the layout it was read from.

| Upstream path | Bytes | SHA-256 | What it is |
| --- | --- | --- | --- |
| `n102_s10.605828696455852.txt` | 7484 | `d9531b5cb08b6c30ea540a7e2793ed661fa24f2eaa48bcfcd055062f08eca1bb` | The layout the issue reports |
| `n102_s10.605828696455852.json` | 8086 | `f5b97045a54c7879e1abe13c7c74a06b149c3ec18b2674ba7ba7f4988ba5e22b` | The same layout as JSON |
| `n102_s10.605828696455852_submission.svg` | 32157 | `404ce3c2efc4bb20085628095275d3e168da7856c610978aa75b542e3969fd25` | The same layout drawn, with each pose as data attributes |
| `verify_exact.py` | 2968 | `8f2f7cdc3a98c7c6a33585e8b40b38e226eb155de86d2e65982e351610e2aff4` | The author’s 60-digit decimal checker |
| `earlier/n102_s10.605828708.*` | | in the manifest | The author’s earlier layout and drawings |
| `README.md`, `n102_s10.605828696455852.png` | | in the manifest | Author prose and drawing |

Read in scratch, the JSON and SVG copies state the same 102 binary64 triples as the
`.txt`, in the same order.

## The Exact Certificate

`devtools.upper_bound_reports` reads the layout through its `calle-txt` adapter.
Every decimal is read exactly as printed, and the side is the printed
`10.605828696455852`, with no dilation.
Each square’s half-angle tangent $t = \tan(\theta/2)$ is the exact tangent of the
printed angle rounded down at 40 places, decided by an outward-rounded interval
enclosure (`half_angle_tangent_radians`). That turns each square by less than
$2 \times 10^{-40}$ radians from the printed angle, far below the layout’s margins.
The certificate is then the source’s centres and side and these tangents, and nothing of
the author’s checking is believed.

## Exact Replay

The certificate was decided by the maintained two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$. A positive job, a duplicate-square control and an outside-container
control each ran in its own child process on one worker.

The positive passes both routes, and both refuse both controls.
The two routes find the same least wall clearance, $2.002066 \times 10^{-12}$, and the
same least pair gap, $1.932818 \times 10^{-12}$: the margins the issue states, now
exact. The three jobs made 30,906 pair decisions in 39.06 route CPU seconds and 96.84 job
wall seconds, summed; the longest took 32.78 seconds. The one-worker run took 1 minute
48 seconds of wall time with the machine at a load of about 15, and a fresh serial
`check --replay` decided all three jobs again, equal to the retained rows apart from
timing, in 2 minutes 20 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code. The third exact route
(`devtools.check_half_angle_area`), which imports neither route’s parsing or deciding
code, decided the certificate again with six controls in the stage 4
[review of 12 October](../../../../docs/project/reviews/review-2026-10-12-upper-bound-imports-528-529.md),
agreed with both routes at every number they share, and derived the fact again from
the pinned layout with its own reader and arithmetic; its credit measurements are
below.

The author’s `verify_exact.py`, read first (it imports only `json`, `sys` and `decimal`,
reads the file it is given and writes nothing), was run with the project interpreter in
isolated mode on the pinned `.txt` and JSON, from a scratch directory outside this
repository. Both runs print the least wall clearance $2.002 \times 10^{-12}$ and the least
pair gap $1.932 \times 10^{-12}$ over 931 close pairs, and `LEGAL`. It computes cosines and
sines at 60 digits and rounds, so it is a diagnostic and not an exact check.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at layer 4’s head `dead83f0e` (12 October 2026), which carries `main` at
`ad00d7f84` and the open adoption layer; `check-claims` rebuilds it, each exact side from
its holder’s own packet.

| Report | Its side | This certificate |
| --- | --- | --- |
| The case’s house on layer 4: Evan Daniel’s regularization of Ryan Xu’s packing (T-146) | 10.6058286964315784 | above it by $2.43 \times 10^{-11}$ |
| Ryan Xu’s certificate (T-125), the case’s house on `main` | 10.6058286965106059 | below it by $5.48 \times 10^{-11}$ |
| Evan Daniel’s degree-8 exact side of the earlier configuration (T-120) | 10.607174680176051125… | below it by $1.35 \times 10^{-3}$ |

So the certificate is a finite upper bound the record already beats: T-146, registered
on 10 October 2026 and confirmed at V3/C3, is smaller, and it is the house at 102 once
the adoption layer merges. The issue compares with T-125 only, and its margin to T-125 is
right. T-120 is the exact algebraic side of a different design, the one this count’s
record held before Ryan Xu’s: its decimals agree to 18 places with T-098’s rational side,
Evan Daniel’s exact optimum of Francisco Couzo’s packing of 26 September 2026. It says
nothing about this arrangement, whose exact side nobody has computed. The README’s valley bottom, $s = 10.605828696431638$, is the
author’s report for which no layout is published; it is not certified here, and it is
above T-146’s side by $6.0 \times 10^{-14}$.

## Against Ryan Xu’s Packing

Measured for the credit with the third exact route’s own `arrangement_gap` and
`patch_lineage` (`devtools.check_half_angle_area`, called from a scratch driver and not
changed), against Ryan Xu’s certificate (T-125) and Evan Daniel’s regularization of it
(T-146):

| Against | Best symmetry | Squares moved beyond $10^{-9}$ ($10^{-3}$, $10^{-2}$, $10^{-1}$) | Largest move | Largest turn (sine); turned beyond $10^{-6}$ | Reappearing by pose ($10^{-9}$); to the eye ($10^{-1}$) |
| --- | --- | --- | --- | --- | --- |
| T-125 | a half turn | 62 of 102 (61, 42, 19) | 0.494 | 0.683; 11 | 40; 86 |
| T-146 | a quarter turn | 61 of 102 (59, 44, 25) | 0.494 | 0.683; 11 | 41; 78 |

Every square of this packing is matched one to one to a square of Ryan Xu’s under a half
turn of the box, and 40 of them land within $10^{-9}$ of their match, none turned: the
issue’s count. The other 62 moved, 19 of them by more than a tenth of a unit and the
largest by 0.494, and 11 turned. So this is a different arrangement of Ryan Xu’s design, as
the issue says, and not a refinement of Ryan Xu’s packing in the sense the record uses for
re-equilibrated packings, where no square moves beyond a tenth. The issue’s further
split, 39 squares within 0.05 and 23 beyond, of which 7 move by up to half a unit, was
not reproduced at those scales.

## What Is Not Established

The author’s private exact certificate, the claim that the valley bottom is the optimum
of the arrangement, and the history of how the layout was found are the author’s. No
local or global optimality is established. The certificate establishes a finite upper
bound only.

## Credit

The issue asks for the credit name Rio Calle (University of New Hampshire), and credits
Ryan Xu with the design and width first (T-125, published 8 October 2026 at 00:03 UTC). The
README says the author’s own engine (GPU simulated annealing, an exact LP finish and a
beam search of structural edits) found the arrangement from scratch about ten hours
later, without reading a published layout, and that it shares Ryan Xu’s design but is a
different arrangement: with Ryan Xu’s turned a half turn, 40 of the 102 squares coincide.
The first report, Davidebyzero/packing_squares_in_squares__tools issue 6, was opened on
2026-10-08T17:34:14Z. The issue and README state AI assistance: the author designed and
directed the project and its experiments, and Claude wrote and ran the search, the exact
finishing step, the refinement search and both checkers.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source riocalle-n102-2026-10-12 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports riocalle-n102-2026-10-12 derive --checkout CHECKOUT --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports riocalle-n102-2026-10-12 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports riocalle-n102-2026-10-12 check --replay
```

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-102.yaml.gz` | receipt | `b0f57cc4bf65242b7dfe8cc34199076905935b7d` | `92bb96ed5b8bca955517e969e85701e1d0cde92a92e674e415cb5b5f2a58c32c` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
