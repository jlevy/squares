# Francisco Couzo’s Issue 670: the In-Corpus Certificate at 204

Francisco Couzo’s [issue #670](https://github.com/jlevy/squares/issues/670), opened
2026-10-17T18:05:06Z, asks to register 73 upper bounds for n = 204 and 330 to 993, each
the exact rational side of a certificate in
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/23aff0c6f992271e1ad13a148d44f392c4b386c0)
at `23aff0c6f992271e1ad13a148d44f392c4b386c0` (committed 2026-10-17T18:00:09Z) rounded up
at 12 places.
This packet retains the one row in the n ≤ 324 case corpus, s(204), registered as T-226.
The 72 rows beyond the corpus are think-f28n’s, and follow #715’s import.

| n | Exact side of the certificate | Issue’s print, rounded up | SHA-256 |
| --- | --- | --- | --- |
| 204 | `45044217780850246618141/3041751595240000000000` | 14.808644417690 | `f317d0c0b04b947b9199ed47c998ff221d05e4d01849b942545364a173bc73dc` |

The certificate gives 204 unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in Evan Daniel’s certificate format, which the header names.
Its per-count JSON, `certificates/n204.json`, names its digest and exact side and credits
the seed to Mykhailo Polkovskyi (Mishapolk), search job 105412 (`hop`).

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
Retained: `source/certificates/n204.cert`, the certificate the issue links, and `source/certificates/n204.json`, 2 files, 22,075 bytes.
The repository states no licence for its data or prose, so the certificates and their
JSON are retained as factual data under the owner decision of 9 October 2026 recorded in
[known-best-packings/README.md](../known-best-packings/README.md).
Pinned by digest only: the root `README.md` and `upper_bounds.json`, the certificate
directory’s `README.md`, `manifest.json` and `SHA256SUMS`, and the source’s exact checker
`verify_bound_certificate.py` with its MIT licence `BOUND_VERIFIER_LICENSE.txt`, which are
byte-identical to the copies the [issue-678 packet](../couzo-issue678-2026-10-18/README.md)
retains and were not run.
The issue’s 72 other certificates and the rest of the tree are pinned by the commit alone.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, by the declaration-driven importer
`devtools.upper_bound_reports` ([acquisition/report.json](acquisition/report.json)):
`sqpack`’s exact witness verifier and the independent rational corner checker, each
deciding every wall and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process.
The positive passes both routes, and both routes refuse both controls. In the positive a square touches the box, a least wall clearance of exactly 0, which the closed box allows, and every pair clears by at least $5.47 \times 10^{-11}$. The 3 jobs made 124,236 pair decisions in 10.22 route CPU seconds, on one worker on 22 October 2026.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method. No source program ran here, and the entry
awaits a stage 4 review (think-0nse).

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record on `main` at `d7923b8d`, 22 October 2026: above the case’s house best packing,
Couzo’s own #678 certificate (T-223), by $1.58 \times 10^{-6}$; above Evan Daniel’s view
of that packing (T-225) by the same; above Couzo’s #675 by $5.05 \times 10^{-8}$; below
Mykhailo Polkovskyi’s refinement T-186, which held the case when #670 was reported, by
$1.88 \times 10^{-5}$.
The [18 October ledger](../../../campaign/issue-intake/upper-bounds-20261018/README.md)
recorded it in report order, after T-186 and before #675; #678 and T-225 came later, each
smaller. So T-226 enters superseded.
Measured pose by pose in the
[issue-672 packet’s measurement](../couzo-issue672-2026-10-17/measure/identity.json),
#675’s packing is this one under the identity (5 squares beyond a tenth, at most 0.143),
Couzo’s own sequence; no regularization is recorded.

## Credit

Francisco Couzo, whose issue keeps every seed, construction and certificate credit in
the source’s manifest; the per-count JSON credits the seed to Mykhailo Polkovskyi.
The source discloses OpenAI Codex assistance with its checker.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-issue670-2026-10-17 --check
python -m devtools.upper_bound_reports couzo-issue670-2026-10-17 check-claims
python -m devtools.upper_bound_reports couzo-issue670-2026-10-17 certify --jobs-dir "$TMPDIR/jobs" --workers 1
python -m devtools.upper_bound_reports couzo-issue670-2026-10-17 check --replay
python -m devtools.upper_bound_reports couzo-issue670-2026-10-17 register-plan
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
