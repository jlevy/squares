# Mishapolk’s Lower n = 204 Certificate at 12fc4667, Issue 719

This packet retains `certificates/n204.cert` from
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/blob/12fc46678fa8eefa3f156ff37dfffd84c8f3a580/certificates/n204.cert)
at `12fc46678fa8eefa3f156ff37dfffd84c8f3a580` (committed 2026-10-22T06:05:07Z), the
revision [issue #719](https://github.com/jlevy/squares/issues/719) pins.
It is the release’s second 204 file.
The issue names the other, `certificates/n-204.cert`, which the
[#719 packet](../mishapolk-issue719-2026-10-22/README.md) keeps as a derived fact and
the register holds as T-229.
Its header states
$s(204) \le 14808642830513087197802415708703/10^{30} = 14.808642830513087197802415708703$,
exactly $14809457954896291297/10^{30} \approx 1.4809 \times 10^{-11}$ below T-229’s
$882663895519250432/59604644775390625$.
The record registers it as T-231.

The source was read at 05:09Z on 23 October 2026 from a blobless clone, whose head stood
at `7b6366fb5e7643772541da21329cda4705be57d5` (2026-10-23T01:50:22Z).
The repository dropped this file at `3285fac` and holds none of its bytes at that head
([Source Custody](#source-custody)).

## What the Author Claims

- **The claim.** Polkovskyi’s comment on #719 of 2026-10-22T20:15:57Z
  ([issuecomment-6350348588](https://github.com/jlevy/squares/issues/719#issuecomment-6350348588)),
  answer 3, claims this file: “We claim the lower certified bound (1.48 × 10⁻¹¹ lower),
  which passed both of your exact routes.” It prints no side; the certificate’s header
  states it, and `acquisition/report.json` admits the certificate at that exact fraction.
- **Lineage.** His comment of 2026-10-23T01:52:40Z
  ([issuecomment-6355484781](https://github.com/jlevy/squares/issues/719#issuecomment-6355484781)),
  answer 2: the continuous SQP optimization of N = 204 “was initialized directly from
  Francisco Couzo’s #678 certificate (`n204.cert` in Couzo’s repository) in Couzo’s
  native unrotated coordinate frame”, not from Evan Daniel’s regularized T-225 view, which
  needs the box’s half turn. The measurement below agrees.
- **His checks.** The same comment, answer 1: this repository’s `sqpack/verify.py` was
  imported as a Python module in a batch harness. The harness parsed each certificate and
  called the module’s pair-overlap and containment routines in memory. The command line in
  the issue was shorthand for that wrapper. Evan Daniel’s `verify_cert.py` and
  `verify_cert2.py` were run as archived in Francisco Couzo’s repository at `6b7391d`.
  These statements are the author’s. Neither the harness nor those copies is in the
  pinned tree, and no source program ran here.
- **Not claimed.** No optimality, local rigidity or KKT condition.
- **AI assistance.** Issue #719 says Gemini assisted with solver scripting, precision
  checks and formatting.

## Source Custody

The pinned tree has no licence file, and its README states no reuse terms.
These bytes are retained under the author’s written grant on #719, answer 5 of his
comment of 2026-10-22T20:15:57Z. The comment says the MIT licence he added at `17cc220`
covers all certificates, catalogs, manifests and tooling, “enabling `jlevy/squares` to
retain and redistribute the raw certificate files in your packets”.
That `LICENSE` (Git blob `d81c9578741244f8da9f3602674a8d0516d26478`, SHA-256
`4761eb7dc9e50c13cd9a876e0a56dbe3db7b97064a354c0ac235c93293e4de0c`) reads “MIT License,
Copyright (c) 2026 Mykhailo Polkovskyi (Mishapolk)”, with the standard MIT permission and
warranty text.

**What custody rests on.** `17cc220`’s tree does not hold this file. `3285fac`
(2026-10-22T19:29:30Z) removed `certificates/n204.cert` when it sharded the certificates.
Its `certificates/0000-0999/n204.cert`, there and at every later commit through the head
read, `7b6366f`, holds `n-204.cert`’s bytes (blob `17e243a`), not these.
So the licence file sits in no tree beside this file, and retaining these bytes rests on
the comment’s written grant from the copyright holder, not on a licence in the pinned
tree. Its MIT terms are carried here as the comment states them.

`devtools.acquire_source` wrote the custody record from a sparse checkout at the pin,
from [acquisition/declaration.json](acquisition/declaration.json):
[acquisition/sources.json](acquisition/sources.json) is the record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
Its scope is four files, each bound to its Git blob at the pin:

| File | SHA-256 | Kept |
| --- | --- | --- |
| `certificates/n204.cert` | `9c5dabc8f2456b0c90650eac5794918c5e52ff90d9e817bd215c9816a88f3e7d` | retained, [source/certificates/n204.cert](source/certificates/n204.cert) |
| `certificates/n-204.cert` | `7c77ad00e36fdceedadeef0d6e256a6682a6974877ded0f97aa110cad918f4a3` | pinned by digest; T-229’s file, derived in the #719 packet |
| `README.md` | `d1b8a7da7c0e61e38ce558bedc54ca0429bdce7ef9bf1778890852b8e13c6378` | pinned by digest |
| `LEGAL_VICTORIES.jsonl` | `a89026eea1c199c5cf635b76e50e2e69cc5bb0c990bedd2f5021e4e276fd373b` | pinned by digest; it names `n-204.cert` at 204, not this file |

The retained file’s digest is the one the #719 packet’s custody record pins for it.
Its Git blob, `4117e9d894450ab7715ab76b3250aed453e68777`, is the same at `1851c2c` and at
the pin. The file is 206 lines and is stored as the source wrote it, uncompressed.

## Report Order

The repository is watched, so its certificates are reports from their first commit.
The path `certificates/n204.cert` first held other bytes: larger 204 sides at `8bb41af5`
(13 October) and `70a033f0` (14 October), which the record keeps through #593’s packets.
These bytes first appear at `1851c2c` (2026-10-22T05:29:48Z), a minute before #719 opened.
That commit also first published `certificates/n-204.cert`, the file the issue names.

The ledger keeps one claim of a report a count: the least side its commit states there
(#722’s review A, A2). So the
[ledger of 22 October for issue 719](../../../campaign/issue-intake/upper-bounds-issue719-20261022/README.md)
transcribes #719’s claim at 204 at this file’s side, with `n-204.cert` beside it at the
same commit. It records it below T-225, the case’s house when it was read.
T-229 stands as registered and adopted on `n-204.cert`, the issue’s named file, before
the author claimed this file on 22 October at 20:15:57Z. T-231 registers this file, by
the same author and from the same commit, and supersedes T-229 at 204. 105 is untouched.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `31584003e` (23 October 2026), and `check-claims` rebuilds it.

| Below | Holder | By |
| --- | --- | --- |
| T-229, the house since 23 October 2026 | Mykhailo Polkovskyi, of Francisco Couzo’s packing | $1.4809 \times 10^{-11}$ |
| T-225 (Daniel’s view at `0075967`) | Francisco Couzo, improved by Evan Daniel | $1.008 \times 10^{-8}$ |
| T-223 (#678) | Francisco Couzo | $1.147 \times 10^{-8}$ |
| T-228 (#675) | Francisco Couzo | $1.537 \times 10^{-6}$ |
| T-226 (#670) | Francisco Couzo | $1.587 \times 10^{-6}$ |
| T-186 (`70a033f`) | Mykhailo Polkovskyi, after Daniil Ostashev and PingYou Ltd | $2.040 \times 10^{-5}$ |

It is the smallest report at 204.

## Pose by Pose

[measure/identity.py](measure/identity.py) measures the certificate against the
packings the record credits, with the measures of the
[evand-regularized-2026-10-20](../evand-regularized-2026-10-20/README.md) packet’s
identity program, and writes [measure/identity.json](measure/identity.json).
A measurement, which decides nothing:

- **Against T-229.** Nearest centres pair the squares one to one under the identity.
  No square moves beyond $10^{-9}$: at most $2.02 \times 10^{-11}$, turning at most
  $5.2 \times 10^{-15}$°. It is T-229’s packing, re-solved to a side
  $1.48 \times 10^{-11}$ lower.
- **Against T-223**, Couzo’s #678 certificate, which the author names as the solve’s
  start: one to one under the identity, 60 squares beyond $10^{-3}$, 29 beyond
  $10^{-2}$ and 7 beyond a tenth, at most 0.237. Every square turns by less than 1° but
  one, square 38, which this packing releases and turns by 25.64°. That is T-229’s own
  measurement against T-223.
- **Against T-225:** one to one only under a half turn of the box, 67 beyond $10^{-3}$
  and 6 beyond a tenth, at most 0.273.
- The certificate tilts 77 squares, as T-229’s does.

## Exact Replay

`devtools.upper_bound_reports` reads the retained certificate by the `evand-cert`
adapter, with centres in $[0, S]^2$. It decides the certificate through the two exact
routes of `devtools.evand_arrangement_reports`: `sqpack`’s exact verifier and the
independent rational corner checker.
Each route tests all 20,706 pairs.
The positive passes both routes, and both routes refuse the duplicate-square and
outside-container controls: 124,236 pair decisions over the three jobs, 16.11 route CPU
seconds and 16.77 job wall seconds on 23 October 2026, the longest job 5.82 s
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)).
`check --replay` decided it again, in 17 s of wall.
Every wall clears by exactly $5 \times 10^{-21}$, and every pair by
$9.999999999999987 \times 10^{-21}$, the same on both routes.
Those margins are below the binary64 spacing of the coordinates, so the two gross
controls cannot tell an exact route from one that rounds.

**Sharp controls.** [receipts/sharp_controls.py](receipts/sharp_controls.py) writes
[receipts/sharp-controls.json](receipts/sharp-controls.json).
It takes the certificate to exact contact, then $10^{-30}$ past it, three ways:

- the side lowered by the least far-wall clearance;
- the least-gap pair closed along its separating normal;
- every square moved toward the nearer near wall by the least near-wall clearance.

Both maintained routes accepted each control at exact contact, with the margin exactly
0, and refused each $10^{-30}$ past it, with the margin exactly $-10^{-30}$. That is six
controls, about 32 CPU seconds in all.
`tests/test_upper_bound_reports_n204.py` holds the retained receipt to that, and runs
the kernel’s two sharp controls on the certificate again in the deep surface.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method. No source script ran here.
The `exact_verify` route decides through `sqpack/verify.py`, which the author says he
imported as a module, so the replay shares the producer’s named components.

**An independent route to the same side.** In the regularization runs of 22 October
after T-229’s adoption
([think-4h23-2026-10-23](../../../cases/regularized_drawings/think-4h23-2026-10-23/README.md)),
Evan Daniel’s exact solver ran here on T-229’s witness. It certified
$S_{\text{cert}} = 14808642830513087197802415708703/10^{30}$, this certificate’s side,
digit for digit.
That run is corroborating evidence, reached from the house witness by other code. It is
not a result of this project and takes no credit.

## What Is Not Established

A finite packing certifies an upper bound and nothing more.
No optimality, rigidity or KKT statement is replayed. No arrangement identity beyond the
measurement above is decided, and the source’s checkers were not run.

## Stage 4 Review

The register entry waits on its stage 4 mathematical review, `c-review-t231-math`
(think-tetq). That lane is prompted separately from the records lane that built this
packet. Its programs and receipts will be kept under `review/` here.

## Credit

The packing is Francisco Couzo’s. He first reported it in #670 and refined it in #675
and #678 (T-226, T-228, T-223), and his source credits Polkovskyi’s own construction as
the seed of its search.
Mykhailo Polkovskyi re-solved it to this side, starting from Couzo’s #678 certificate,
as his comment of 23 October says.
The bibliography key is **[Mishapolk n204 2026-10-22]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source mishapolk-n204-2026-10-22 --checkout CHECKOUT
python -m devtools.acquire_source mishapolk-n204-2026-10-22 --check
python -m devtools.upper_bound_reports mishapolk-n204-2026-10-22 check-claims --write
python -m devtools.upper_bound_reports mishapolk-n204-2026-10-22 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports mishapolk-n204-2026-10-22 check --replay
python resources/web/mishapolk-n204-2026-10-22/measure/identity.py --out resources/web/mishapolk-n204-2026-10-22/measure/identity.json
python resources/web/mishapolk-n204-2026-10-22/receipts/sharp_controls.py --out resources/web/mishapolk-n204-2026-10-22/receipts/sharp-controls.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
