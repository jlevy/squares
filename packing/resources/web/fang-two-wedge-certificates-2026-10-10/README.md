# Kevin Fang’s Two-Wedge Certificates: 308, 343 and 344

[Issue #484](https://github.com/jlevy/squares/issues/484) reports three exact rational
packings from
[TheSnakeFang/squarepack-certs](https://github.com/TheSnakeFang/squarepack-certs/tree/c75bebd87933416d3e1c7aba35ec733ea8ac7da0)
at `c75bebd87933416d3e1c7aba35ec733ea8ac7da0` (tree
`3616465b86f213af4c55a9089eba65d3ebafb963`, committed 2026-10-10T02:22:44Z, the
repository’s first and only commit), one per folder `n0308/`, `n0343/` and `n0344/`:

| n | Exact side of the certificate | Rounded up at 16 places | The issue prints |
| --- | --- | --- | --- |
| 308 | `496906684150483564257053639569689586211617178631487101147707692165192097/27606985387162255916575391130373464080218179016903156277167119960899584` | 17.9993098551627480 | 17.999309855162748 |
| 343 | `789017423383549575129979982295456201/41538374868278621028243970633760768` | 18.9949035292204970 | 18.994903529220497 |
| 344 | `262204097424407923560664994905454377606094204426897481135606818230728643/13803492693581127593573619627880932674597656005283617050019749892718592` | 18.9954892754308151 | 18.995489275430816 |

Each certificate gives `n` unit squares, each a rational centre in $[0, S]^2$ and a
rational $t = \tan(\theta/2)$, in a square of the stated side.
Each exact side rounds up, at the 15 places the issue prints, to the side it prints.
The sources were retrieved at 2026-10-10T09:58Z.

## Retained Here

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json)
is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.

The whole tree is in scope, 28 files.
The 25 retained are the licence, `ATTRIBUTION.md`, `README.md`, the author’s standalone
checker `verify.py`, and in each folder the certificate in three formats, the author’s
notes, the folder’s `SHA256SUMS` and the outputs of the two checkers the issue names.
`nNNNN.cert` is Evan Daniel’s text format and the certificate this import decides;
`nNNNN.cert.json` is the same packing in SQUISH’s JSON layout, stored compressed below;
`nNNNN.txt` is David Ellsworth’s 40-digit centre-origin export.
The three drawings, `nNNNN.svg`, are pinned by digest only. `verify.py` was read and is
retained as the source’s checker; it was not run.

`read_facts` admits each count only where its `.cert` and its `.cert.json` state the
identical exact packing, side and every pose, through two separate adapters.
The 40-digit exports are not read here.

## Exact Replay

Only the three `.cert` certificates enter geometry decisions, through the maintained
two-route kernel of `devtools.evand_arrangement_reports`: `sqpack`’s exact witness
verifier and the independent rational corner checker, each deciding every wall and every
pair over $\mathbb{Q}$ after an exact half-angle conversion. Each count runs a positive
job, a duplicate-square control and an outside-container control, each in its own child
process.

All three positives pass both routes, and both routes refuse all six controls, each on
the overlap or the wall it was built to break.
In every positive both routes find the least wall clearance exactly $2^{-65}$
($2.71 \times 10^{-20}$), and least pair gaps of $1.65 \times 10^{-20}$ at 308,
$5.03 \times 10^{-20}$ at 343 and $3.15 \times 10^{-20}$ at 344, the margins the
source’s own `verify_output.txt` files print.
The nine jobs made 989,562 pair decisions in 307.82 route CPU seconds and 680.92 job wall
seconds, summed; the longest job took 87.93 seconds, and the two-worker run 6 minutes 4
seconds of wall time.
Other lanes held the machine at a load average of 7 to 15 on four cores throughout, so
the walls overstate the work and the route CPU seconds do not.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record as it stood when the issue was read (`main` at `657cc4861`, 10 October 2026), and
`check-claims` rebuilds it:

- **308.** The case holds the grid’s 18 in both lanes, reported from the Kingbird
  catalogue and verified by `E-basic-grid-upper`.
  The certificate is below it by $6.90 \times 10^{-4}$. No other pending report names
  that count.
- **343 and 344.** Both lie beyond the $n \le 324$ case corpus, so no case record exists,
  and when the issue was read `source-coverage.yaml` held no beyond-horizon row at either
  count. The trivial bound there is the grid’s 19; the certificates are below it by
  $5.10 \times 10^{-3}$ and $4.51 \times 10^{-3}$.
  Mishapolk’s
  [square-packing-records README](https://github.com/Mishapolk/square-packing-records/blob/dd3da5c753c5ded6cb3b89476193b7b801005415/README.md),
  pinned by issue #470, prints 19.000000000007 at 343 and 19.002369297056 at 344, both
  above the grid; neither is in the issue’s own table.

The record keeps 343 and 344 as dated beyond-horizon rows, the form Francisco Couzo’s
$n = 375$ and $378$ reports take since
[pull request #479](https://github.com/jlevy/squares/pull/479): one row each in
`beyond_horizon_claims` of `source-coverage.yaml`, keyed on the count and this source,
with the side the issue prints, `assurance: reported` and
`disposition: tracked-outside-case-corpus`, and no case record, register row, selected
bound or atlas entry. A row there must equal its source’s reparsed claim byte for byte,
so [acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the two claims alone, and the source’s coverage entry names it as its `claims_record`.
The 308 claim is not in that record: until its case takes it in, no selected override
accounts for it.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
No exact form, local minimality or optimality is claimed by the source or established
here, and no review of the replay has been made.
The author reports that re-running the same search at $k = 16, 17, 18$ lands 0.01 to
0.09 above the Kingbird values, so better packings at 343 and 344 are likely nearby.

## Credit and Licence

Kevin Fang wrote the source. `verify.py` and its documentation are under the MIT licence
(`LICENSE`); `ATTRIBUTION.md` releases the certificates, text files and drawings in the
`nNNNN` folders under CC0 1.0. The packings belong to the $k^2 - k + 1$ two-wedge family
of Arslanov, Mustafin and Shangitbayev (Electronic Journal of Combinatorics 28(4), P4.22,
2021, doi 10.37236/8586), grown from David Ellsworth’s and Tej Stead’s packings of 273
and 307 squares on the Kingbird table; the certificate format is Evan Daniel’s and the
JSON layout SQUISH’s (Nate Chaoweeraprasit).
The source and the issue disclose that the search, the verifier and the bundle were
written with Claude under the author’s direction.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source fang-two-wedge-certificates-2026-10-10 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-two-wedge-certificates-2026-10-10 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-two-wedge-certificates-2026-10-10 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports fang-two-wedge-certificates-2026-10-10 check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job directory,
and `register-plan` prints the record entries the import needs.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/n0308/n0308.cert.json.gz` | upstream | `6d6fbd509d73f2574632a9adb4bd3d13847d2fe0` | `6243d1228132604df4dc7db71ea0dca895b2a1f759a03ed1089b00bdc141059a` |
| `source/n0343/n0343.cert.json.gz` | upstream | `a151dd42eb71794006d3c20ea09a24274ac2b3f3` | `088a62b71e1b50d56d08ae1c5ccec903b67f3bc2d09132b3611e296d0b6b17d7` |
| `source/n0344/n0344.cert.json.gz` | upstream | `364f449de973df210c7af6afa78fde4dc257da1c` | `8c9bede7674843f94ca8925d0431048eb061bbfe05e09379c60f6fadc5c2b04e` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
