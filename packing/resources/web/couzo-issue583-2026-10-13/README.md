# Francisco Couzo’s Exact Certificates at 4596670 (Issues #570 and #583)

[Issue #583](https://github.com/jlevy/squares/issues/583), filed at 2026-10-13T14:11Z,
reports exact rational packings from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/45966700cf15d3f42e064fd6da51fcb9a5def2be/certificates)
at `45966700cf15d3f42e064fd6da51fcb9a5def2be` (committed 2026-10-13T13:53:57Z).
[Issue #586](https://github.com/jlevy/squares/issues/586), filed at 17:37Z, pins
`b85dee2` and replaces seven of them; the
[b85dee2 packet](../couzo-certificates-2026-10-13/README.md) retains the successors and
#583’s 302 and 381, which `b85dee2` keeps byte for byte.
This packet retains the seven certificates of #583 that `b85dee2` replaced, because the
per-count ledger of 14 October (`packing/campaign/issue-intake/upper-bounds-20261014/`,
on the intake branch) records #583 at 211, 241, 339, 379, 380 and 382, and issue #570 at
154 by this commit’s `certificates/n154.cert`.

[Issue #570](https://github.com/jlevy/squares/issues/570), filed 2026-10-12T23:19Z, pins
`1b31bc907d2d881c6962739b6b40cd10b1cd5a9c`, which GitHub does not serve.
Its 154 certificate has the SHA-256 the issue states, `5335cb3b…`, which is the digest
of `certificates/n154.cert` here.
Its 379, printed as 19.953542593650 with SHA-256 `ac463682…`, is in no reachable commit
of the source and is not retained anywhere.

| n | Exact side of the certificate | Printed by | Later at b85dee2 (#586) |
| --- | --- | --- | --- |
| 154 | `12922499814642397493692375652931/10^30` | #570 and #583: 12.922499814643 | 12.921206577133 |
| 211 | `5735936523425659529936799651/382560041700500000000000000` | #583: 14.993558914123 | 14.993558913975 |
| 241 | `56654293892568867634658195801/3543746727775500000000000000` | #583: 15.987117095169 | 15.987117095151 |
| 339 | `4247372425158980137376328899/224403568199500000000000000` | #583: 18.927383638495 | 18.925319360704 |
| 379 | `3990706306320510429876555652417/2 × 10^29` | #583: 19.953531531603 | 19.953531362123 |
| 380 | `71405320581108789876116351057/3574993313028500000000000000` | #583: 19.973553606628 | 19.961611078672 |
| 382 | `94198950843216391147752843823/4712633609411500000000000000` | #583: 19.988600568289 | 19.987713157610 |

Each side rounds up to the issue’s 12-place print.
[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
case record and every other report at its count, and
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the four beyond the case corpus.

## Retained Here

`devtools.acquire_source` wrote the packet from a clone checked out at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
93 files, 2,888,625 bytes, the root `README.md` and the `certificates` directory.

The repository states no licence.
The seven certificates under `source/certificates/` (303,367 bytes) are retained as
factual data under the owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md)). The other 64 certificates
of the commit are pinned by digest against byte-identical copies that other packets
retain, 302, 375, 376 and 381 among them in the b85dee2 packet; 344, an intermediate
certificate that no report names and that `b85dee2` replaced, is pinned by digest only.
The two READMEs and the per-certificate metadata files are pinned by digest only. No
prose or program is copied.
Since 22 October 2026 the packet also retains the commit’s `certificates/n378.cert`
(46,595 bytes), added from the same pin at 19:10Z: no issue names it, and the history
walk of Couzo’s watched publications records it as a report from the commit
([Rows Beyond the Corpus from the Commit](#rows-beyond-the-corpus-from-the-commit)).
The packet now retains 8 files, 349,962 bytes.

## Exact Replay

The seven certificates go through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as the b85dee2 packet’s do: `sqpack`’s exact
witness verifier and the independent rational corner checker, each deciding every wall
and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
Each count runs a positive job, a duplicate-square control and an outside-container
control, each in its own child process.

All seven positives pass both routes, and both routes refuse all 14 controls.
In every positive the two routes find the same least wall clearance and least pair gap:
exactly $5 \times 10^{-21}$ and just under $10^{-20}$ for the exact optima at 154 and
379, and exactly $10^{-15}$ for the rational witnesses, whose least pair gaps are
$8.35 \times 10^{-12}$ at 211, $1.20 \times 10^{-12}$ at 241, $6.81 \times 10^{-12}$ at
339, $7.45 \times 10^{-11}$ at 380 and $9.70 \times 10^{-11}$ at 382. The 21 jobs made
2,019,354 pair decisions in 696.74 route CPU seconds and 709.36 job wall seconds,
summed; the longest job took 54.35 seconds.
`certify --workers 1` decided them in 12 minutes 9 seconds of wall from 11:30Z on 14
October.
A fresh serial `check --replay` decided all 21 jobs again, equal to the retained
rows apart from timing, in 13 minutes 4 seconds of wall from 11:42Z.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. No source program ran here.

## Against the Record

At 154 the certificate is 6.66e-05 below the case’s ceiling, Evan Daniel’s #552 (T-160),
and 1.29e-03 above #586’s. At 211 and 241 it is below the case’s ceilings (T-149 and
T-098) by 2.78e-03 and 1.02e-03, and below Daniil Ostashev’s #575 by 1.35e-04 and
1.72e-05; #586 refines both arrangements to sides 1.49e-10 and 1.88e-11 smaller, and
Mishapolk’s #593 states #586’s sides there.
Beyond the corpus, each is below the issue-506 row it was reported against, and #586 is
smaller at every count; at 339 Evan Daniel’s #584 is also smaller.

## Rows Beyond the Corpus from the Commit

Since 22 October 2026 the commit’s `certificates/n378.cert`, which neither #570 nor #583 names, is a row of its own, as the source `couzo-4596670-2026-10-13`: a publication in a watched repository is a report from its first commit (the owner, 14 October 2026), and the [history walk of Couzo’s watched publications](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) records it in report order.

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares this publication a release with no issue, `franciscouzo/square-packing@4596670`, and reads the rows the history walk records from [acquisition/watched-release.json](acquisition/watched-release.json), which `declare-rows` writes from the walk.

Each certificate was first committed at the commit itself ([receipts/first-commits.json](receipts/first-commits.json)).

**It is verified.** The filtered two-route decision of `devtools.couzo_678_replay`, reused unchanged, accepts every packing on both routes (875 candidate pairs of 71,253, and every corner against every wall), and every side is its header side rounded up at 12 places. **All six controls are refused by both routes.** The positive decisions took 0.5 CPU seconds ([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)). No square touches the box and no pair touches: every wall clears by at least $1.00 \times 10^{-15}$ and every pair by at least $5.32 \times 10^{-12}$. Every side is below Göbel’s classical construction at its count ([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) walks every count from 325 to 1024 in report order from starts frozen at `main` `a97b712b9` and records it. **It is superseded on entry**, by Couzo’s b85dee2. It supersedes first Couzo’s 93570ef row.

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record the source register reads them from, as the source `couzo-4596670-2026-10-13`.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The issue says every certificate passes this repository’s `sqpack.verify` at `562fdbd`
and Evan Daniel’s `verify_cert.py` at `31523f8`; those runs are the author’s, and
neither program of the source ran here.
Novelty, local or global optimality and rigidity are not established.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificates are kept as
factual data and nothing of the source is relicensed.
At 154 the packing continues Evan Daniel’s arrangement of #552; at 211 and 241 Daniil
Ostashev’s of #575; 339 and 379 continue the author’s L-border constructions of #506,
and 380 and 382 Kevin Fang’s published arrangements (TheSnakeFang/squarepack-certs).
The issues state that the search implementation, the verification orchestration and the
issues used OpenAI Codex, that earlier search work used Claude Code, and that the author
directed the work.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-issue583-2026-10-13 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-issue583-2026-10-13 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-issue583-2026-10-13 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-issue583-2026-10-13 check --replay
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
