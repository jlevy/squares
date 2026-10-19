# Kevin Fang’s Direct Certificates at 078789a: 380 to 814

No issue reports these certificates.
Kevin Fang’s
[TheSnakeFang/squarepack-certs](https://github.com/TheSnakeFang/squarepack-certs/tree/078789a4cfd36f915f1bfbe76d742413d79b2965),
which the record last pinned at `c75bebd` for issue #484
([fang-two-wedge-certificates-2026-10-10](../fang-two-wedge-certificates-2026-10-10/README.md)),
moved eleven commits to `078789a4cfd36f915f1bfbe76d742413d79b2965` (tree
`89b612b787b7a2004e26cc217011b0999dc5b092`, committed 2026-10-13T06:57:58Z), still the
head when the sources were retrieved, at 2026-10-14T09:20Z.
Two of those commits add fourteen direct square packings, one per folder `nNNNN/`:
`e646c47` (2026-10-12T19:06:24Z) eight and `c284cd0` (2026-10-13T00:05:31Z) six.
No later commit touches either set of folders, so the bytes pinned here are the bytes
first published.

| n | Form | First commit | The source prints, rounded up | Rounded up at 16 places | Below the grid by |
| --- | --- | --- | --- | --- | --- |
| 380 | 20² − 20 | `e646c47` | 19.976775433974195 | 19.9767754339741947 | $2.32 \times 10^{-2}$ |
| 381 | 20² − 20 + 1 | `e646c47` | 19.976969740405508 | 19.9769697404055079 | $2.30 \times 10^{-2}$ |
| 382 | 20² − 20 + 2 | `c284cd0` | 19.989479729399675 | 19.9894797293996742 | $1.05 \times 10^{-2}$ |
| 421 | 21² − 21 + 1 | `e646c47` | 20.986150316947159 | 20.9861503169471583 | $1.38 \times 10^{-2}$ |
| 422 | 21² − 21 + 2 | `c284cd0` | 20.988436524095744 | 20.9884365240957433 | $1.16 \times 10^{-2}$ |
| 463 | 22² − 22 + 1 | `e646c47` | 21.986880406196935 | 21.9868804061969348 | $1.31 \times 10^{-2}$ |
| 464 | 22² − 22 + 2 | `c284cd0` | 21.991709536768996 | 21.9917095367689951 | $8.29 \times 10^{-3}$ |
| 507 | 23² − 23 + 1 | `e646c47` | 22.997807183348823 | 22.9978071833488225 | $2.19 \times 10^{-3}$ |
| 508 | 23² − 23 + 2 | `c284cd0` | 22.994733849702143 | 22.9947338497021427 | $5.27 \times 10^{-3}$ |
| 553 | 24² − 24 + 1 | `e646c47` | 23.998811020144984 | 23.9988110201449836 | $1.19 \times 10^{-3}$ |
| 601 | 25² − 25 + 1 | `e646c47` | 24.998914572427130 | 24.9989145724271294 | $1.09 \times 10^{-3}$ |
| 651 | 26² − 26 + 1 | `e646c47` | 25.991547815274380 | 25.9915478152743798 | $8.45 \times 10^{-3}$ |
| 758 | 28² − 28 + 2 | `c284cd0` | 27.996346242823117 | 27.9963462428231168 | $3.65 \times 10^{-3}$ |
| 814 | 29² − 29 + 2 | `c284cd0` | 28.999873603982716 | 28.9998736039827155 | $1.26 \times 10^{-4}$ |

Each certificate gives `n` unit squares, each a rational centre in $[0, S]^2$ and a
rational $t = \tan(\theta/2)$, in a square of the stated side, in Evan Daniel’s format;
`devtools.upper_bound_reports` reads it through its `evand-cert` adapter.
The source prints each side rounded up at 15 places, in its README’s table and in the
folder’s `NOTES.md`, which the first commit already held, and each exact side rounds up
there to the side printed.
The exact sides are fractions of 39 to 77 digits, each stated in full in
[acquisition/claims.json](acquisition/claims.json).
The grid’s side at each count is $\lceil \sqrt{n} \rceil$.

The other nine commits build the theorem of Fang’s note, *Packing n² − n + 1 unit
squares in a square of side less than n, for every n ≥ 15* (draft v0.6, 2026-10-13):
squeezable rectangles, the composites of its gluing lemma and a theorem inventory for
$15 \le n \le 64$. That content is another packet’s subject, retained from the same
commit under bead think-0esw, and nothing here rests on it.

## Retained Here

`devtools.acquire_source` wrote the packet from a blobless clone checked out at the pin,
from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
122 files and 5,152,308 bytes in scope, of which 93 files and 3,060,676 bytes are
retained.

At the root the packet retains the licence, `ATTRIBUTION.md`, `README.md`,
`CHANGELOG.md`, `VERIFICATION.md`, the source’s whole-tree `MANIFEST.sha256` and its
standalone checker `verify.py`, with `tools/rectcheck.py` and the notice of
`tools/verify_cert_daniel.py`. In each of the fourteen folders it retains the
certificate in two formats, the author’s notes, the folder’s `SHA256SUMS` and the
outputs of the two checkers each folder records.
`nNNNN.cert` is Evan Daniel’s text format and the certificate this import decides;
`nNNNN.cert.json` is the same packing in SQUISH’s JSON layout, stored compressed below.

Three kinds of file are pinned by digest only.
The fourteen drawings, `nNNNN.svg` (987,862 bytes), and the fourteen 40-digit
centre-origin exports in David Ellsworth’s format, `nNNNN.txt` (1,100,369 bytes), bear
on no claim here, and the exact certificate is retained in two formats.
`tools/verify_cert_daniel.py` is Evan Daniel’s `verify_cert.py`, copied unchanged, and
is pinned against the identical copy the
[issue-399 packet](../evand-new-arrangements-2026-10-07/README.md) retains.
`verify.py` and `tools/rectcheck.py` were read and are retained as the source’s
checkers. No source program was run.

The folders `n0308/`, `n0343/` and `n0344/` are unchanged since `c75bebd` and stay in
the issue-484 packet. The theorem bundle (`theorem/`, `composites/`, `rectangles/`,
`third_party/` and `tools/glue.py`) is out of scope, as is `.gitignore`.

`read_facts` admits each count only where its `.cert` and its `.cert.json` state the
identical exact packing, side and every pose, through two separate adapters.
The packet’s tests also hold every file of each folder, retained or pinned, to the
SHA-256 the folder’s own `SHA256SUMS` gives.

## Exact Replay

All fourteen certificates entered geometry decisions here, through the maintained
two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`’s exact witness
verifier and the independent rational corner checker, each deciding every wall and
every pair over $\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on one worker.

All fourteen positives pass both routes, and both routes refuse all 28 controls, each on
the overlap of squares 0 and 1 or the wall square 0 was moved through.
In every positive both routes find the least wall clearance exactly $2^{-65}$
($2.71 \times 10^{-20}$), and the least pair gap the source’s own `verify_output.txt`
prints, from $7.14 \times 10^{-21}$ at 758 to $4.09 \times 10^{-20}$ at 463.
The 42 jobs made 12,168,762 pair decisions in 6,206.59 route CPU seconds and 7,310.06
job wall seconds, summed; the longest, the outside-container control at 758, took
496.24 seconds, and no job at 814 took more than 385.76, under the kernel’s 600-second
job timeout. No job timed out.

| n | Positive, wall / route CPU s | Duplicate-square control | Outside-container control | Least pair gap |
| --- | --- | --- | --- | --- |
| 380 | pass, 109 / 75 | refused, 97 / 75 | refused, 82 / 78 | $2.33 \times 10^{-20}$ |
| 381 | pass, 96 / 75 | refused, 138 / 72 | refused, 118 / 71 | $1.79 \times 10^{-20}$ |
| 382 | pass, 79 / 71 | refused, 71 / 68 | refused, 73 / 67 | $1.58 \times 10^{-20}$ |
| 421 | pass, 102 / 100 | refused, 114 / 110 | refused, 109 / 104 | $1.59 \times 10^{-20}$ |
| 422 | pass, 112 / 108 | refused, 112 / 106 | refused, 99 / 93 | $9.28 \times 10^{-21}$ |
| 463 | pass, 130 / 117 | refused, 132 / 114 | refused, 144 / 112 | $4.09 \times 10^{-20}$ |
| 464 | pass, 150 / 115 | refused, 133 / 113 | refused, 127 / 113 | $3.20 \times 10^{-20}$ |
| 507 | pass, 137 / 129 | refused, 133 / 130 | refused, 136 / 131 | $1.81 \times 10^{-20}$ |
| 508 | pass, 137 / 132 | refused, 141 / 138 | refused, 129 / 126 | $1.66 \times 10^{-20}$ |
| 553 | pass, 148 / 146 | refused, 145 / 143 | refused, 181 / 150 | $1.27 \times 10^{-20}$ |
| 601 | pass, 197 / 180 | refused, 176 / 173 | refused, 170 / 167 | $1.36 \times 10^{-20}$ |
| 651 | pass, 212 / 208 | refused, 225 / 221 | refused, 228 / 225 | $4.01 \times 10^{-20}$ |
| 758 | pass, 387 / 278 | refused, 494 / 277 | refused, 496 / 276 | $7.14 \times 10^{-21}$ |
| 814 | pass, 386 / 344 | refused, 352 / 347 | refused, 374 / 328 | $2.95 \times 10^{-20}$ |

The jobs ran in two one-worker `certify` runs on 14 October 2026.
The nine at 380, 381 and 382 were the first nine of a run over all fourteen counts,
begun at 09:29:38Z and stopped at 09:44:12Z, as its first 421 job started, when the
roster was cut to those three; the 33 at the other eleven counts ran from 16:32:40Z to
18:20:44Z, 108 minutes of wall and 93 of CPU, after the owner set a replay budget, at a
load of 2 to 14.
`certify --finished` assembled the receipt from all 42 outputs, admitted as any receipt
is. Each job’s child process decides one count and one control from the packet alone,
so its output does not depend on the roster, and the nine earlier outputs equal the rows
of the three-count receipt they first formed.
A fresh serial `check --replay` decided all 42 jobs again, equal to the retained rows
apart from timing, in 102 minutes 47 seconds of wall and 98 minutes of CPU, from 18:21:25Z, at a load of 1 to 8.
The receipt would exceed the kernel’s ceiling on uncompressed evidence, so it is kept as
one file a count, `receipts/exact-certification-nNNN.json.xz`, each keeping every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code. No source program ran here.

## Against the Record

No case record holds these counts, so [acquisition/claims.json](acquisition/claims.json)
compares each certificate with the grid, with every beyond-horizon row the record
tracks and with every other report at the count, frozen at `main` `f73e9de13`
(14 October 2026); `check-claims` rebuilds it.

- **380 and 381.** The record tracks Francisco Couzo’s rows from issue #506
  (`couzo-certificates-2026-10-11`), at 19.987440766556 and 19.992663288464, both
  verified. The certificates are below them by $1.07 \times 10^{-2}$ and
  $1.57 \times 10^{-2}$.
- **382.** The record tracks no row; the certificate is below the grid’s 20 by
  $1.05 \times 10^{-2}$.
- **The other eleven.** The record tracks no row, and no report of the 14 October intake
  names them. Each certificate is the smallest side the record knows at its count.

Three issues filed after these commits report sides at 380, 381 and 382, each printed
rounded up at 12 places except #582’s, which is exact:

| n | This certificate | Row on `main` | #582, Miles Gray | #583, Couzo | #586, Couzo | Smallest |
| --- | --- | --- | --- | --- | --- | --- |
| 380 | 19.976775433975 | 19.987440766556 | | 19.973553606628 | 19.961611078672 | #586 |
| 381 | 19.976969740406 | 19.992663288464 | 19.985624661051481 | 19.974977397657 | | #583 |
| 382 | 19.989479729400 | | | 19.988600568289 | 19.987713157610 | #586 |

This certificate’s column is its side rounded up at 12 places.
#582 was filed at 2026-10-13T11:38:11Z, #583 at 14:11:17Z and #586 at 17:37:01Z; #589
repeats #582 and was closed by its author 20 seconds after filing.
At 381, #582’s side is above this certificate’s by $8.66 \times 10^{-3}$.
Couzo’s sides are below it: by $3.22 \times 10^{-3}$ and $1.52 \times 10^{-2}$ at 380,
$1.99 \times 10^{-3}$ at 381, and $8.79 \times 10^{-4}$ and $1.77 \times 10^{-3}$ at
382\. The couzo lane’s packet `couzo-certificates-2026-10-13` keeps #586’s exact sides
and #583’s at 381; this record compares all three issues by their prints, which decide
every relation here.

**Report order.** Under the owner’s report-order rule (think-abi1), a watched
repository’s publication is reported at its first commit.
The certificates at 380 and 381, from `e646c47`, came before all three issues and are
below the rows then standing, and the certificate at 382, from `c284cd0`, came first at
its count, so each is recorded.
At 381, #582 is above this certificate and is not recorded; Couzo’s #583 and #586 are
below it at all three counts and are recorded after it, by the couzo lane.
#583 and #586 say their packings at 380 to 382 continue Fang’s arrangements and ask that
his construction credit be kept, and #582 grew its 381 from Fang’s and Daniel’s packings
of 343.

**507 and 508.** The certificate at 508 has a side $3.07 \times 10^{-3}$ below the one
at 507, and dropping one square from a packing of 508 packs 507, so
$s(507) \le 22.994733849702143$ as well.
That consequence settles no case, so it has no entry of its own
([result-import.md](../../../campaign/result-import.md#stage-1-triage)); the 507 row
keeps its own certificate’s side, and this paragraph names the consequence.

The rows would be dated beyond-horizon rows, one each in `beyond_horizon_claims` of
`source-coverage.yaml`, as issue #596’s are: keyed on the count and this source, with
the 15-place side the source prints, and no case record, register row, selected bound or
atlas entry. A row there must equal its source’s reparsed claim byte for byte, so
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the fourteen claims alone, and the source’s coverage entry names it as its
`claims_record`. The records lane, which registers in report order, sets each row’s
disposition and assurance.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
No exact form, local minimality or optimality is claimed by the source or established
here, and no review of the replay has been made.
Every note says its packing was not analytically optimised, and Couzo’s smaller
continuations at 380 to 382 show that better packings lie nearby there.

## Credit and Licence

Kevin Fang wrote the source. `verify.py`, `tools/rectcheck.py` and the shell scripts are
under the MIT licence (`LICENSE`); `ATTRIBUTION.md` and the README release the
certificates, text files, tables and drawings in the `nNNNN` folders under CC0 1.0.
`tools/verify_cert_daniel.py` is Evan Daniel’s, under the MIT licence its notice
carries.

Each packing was found by a time-budgeted penalty search from a two-wedge seed in the
$k^2 - k + 1$ family of Arslanov, Mustafin and Shangitbayev (Electronic Journal of
Combinatorics 28(4), P4.22, 2021, doi 10.37236/8586).
Each folder’s `NOTES.md` names its seed: Francisco Couzo’s packing of 342 squares for
380 and 381, and through 381 for 421; Evan Daniel’s improved packing of 343 from issue
#489 (`hunt3_n343.cert`) for 382; and for the other ten a parametric seed, built from
line lengths and angles rather than from an earlier packing.
The certificate format is Evan Daniel’s and the JSON layout SQUISH’s (Nate
Chaoweeraprasit). The source discloses that the search, the verifier and the bundle
were written and run with Claude (Anthropic), directed and reviewed by Kevin Fang.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source fang-direct-certificates-2026-10-13 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-direct-certificates-2026-10-13 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-direct-certificates-2026-10-13 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-direct-certificates-2026-10-13 check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 1` writes a new receipt from a fresh job directory
for the declared `replayed` counts, and `register-plan` prints the record entries the
import needs: an evidence entry, a source row and fourteen beyond-horizon rows, and no
register entry.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/n0380/n0380.cert.json.gz` | upstream | `a965594a0202a16277cbb82abef3ebf6525236ef` | `a4a163dada5460c2ba89d60590b6c49d4bd13eb90599a5d5002571133e131873` |
| `source/n0381/n0381.cert.json.gz` | upstream | `ca8e9bb83e68f029b5699466ba238c76e8832813` | `11553e5c2fcc3eb980d40f8b4632fd02f23abaf8fa9b9bc7254dfd1f78199cf4` |
| `source/n0382/n0382.cert.json.gz` | upstream | `3d958078f9d896abfe4d228861c2507c7af30c05` | `8954c9a45d9b2697ffe90ff95c07d81a3b0e9df1b7933eafddb38b644e33c0f7` |
| `source/n0421/n0421.cert.json.gz` | upstream | `2b46a38974d101f05e0e9db3ff63c24c89270467` | `52bc731cccfaa2529da5e5b4910458f8c84162c1994ddca0fbc10005c353ca44` |
| `source/n0422/n0422.cert.json.gz` | upstream | `5af711b739f36f694b836161b5be28017e500ef0` | `b9522d45c6891e51ab60ed044efb26a5b29305ce6c73e2f2c7f82f0686e45099` |
| `source/n0463/n0463.cert.json.gz` | upstream | `ad5b736dd8a8be5c0b40ee9cb91f25e84957ef5b` | `a82e84c69f756c027e1e789d5cc9e33f43280ac07bec89340b12b5e7204054f6` |
| `source/n0464/n0464.cert.json.gz` | upstream | `91362f0ccf935e233344139b82f025d658d0734b` | `d72986d42997ff3bbc67d74b21d7b8a6e058970550d9a97ecfc72d82a7d078be` |
| `source/n0507/n0507.cert.json.gz` | upstream | `b9e8344efb9bba3d3b3d6fd08a2143e18be1b121` | `5dce9a2be6b168d969d9f5b19fc7a606e5bdd58231bbb66315e66ddff7f17222` |
| `source/n0508/n0508.cert.json.gz` | upstream | `acfce42ef1c804571ef3372db7da62e1a3c55a16` | `dcb2721c5e55a943acc2e03256f9f8adae8a6abbcf94f9ffa6707ee6484345e0` |
| `source/n0553/n0553.cert.json.gz` | upstream | `dede6440d3fb24c9bbd8efb256eadb3672fa3de3` | `3165e669ae9400ec9d66fda28b4c235061d8a874421510a53a81c7a032fd7431` |
| `source/n0601/n0601.cert.json.gz` | upstream | `38a308d3d65e0fce5e1f7e0e0c6457a5fd37b6b0` | `c78130e53e871e0c7646613af75ea9eedda9d7ba1f311f3594c2df4e59b901be` |
| `source/n0651/n0651.cert.json.gz` | upstream | `4a451fb7f96e91d51d61168f24fa3f74e606c693` | `13183aac16035cb21b9d0e3c5426c1cdb09964082e9728343e551873c4a2ca82` |
| `source/n0758/n0758.cert.json.gz` | upstream | `b05311adc72f8f1c9b687769f7f8877704406e68` | `4db838c9ffca7280f061b096f4595851622663011b79119f7473964d5afb9df3` |
| `source/n0814/n0814.cert.json.gz` | upstream | `516a4160f6a8c9318536fac388b9811e167c6d73` | `12d753f9baf567c40bb29cddbe1083d72de3895e638880f9d695870f63fd2508` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
