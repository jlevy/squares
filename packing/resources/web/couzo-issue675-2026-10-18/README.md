# Francisco Couzo’s Issue 675: the In-Corpus Certificate at 204

Francisco Couzo’s [issue #675](https://github.com/jlevy/squares/issues/675), opened
2026-10-18T06:02:11Z, a follow-up to #672, asks to register 79 upper bounds for n = 204
and 419 to 998, each the exact rational side of a certificate in
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/c6da0fc7524d667bf3d224559724ba9b60762e60)
at `c6da0fc7524d667bf3d224559724ba9b60762e60` (committed 2026-10-18T05:46:00Z) rounded up
at 12 places.
This packet retains the one row in the n ≤ 324 case corpus, s(204), registered as T-228.
The 78 rows beyond the corpus are think-pvav’s, and follow #715’s import.

| n | Exact side of the certificate | Issue’s print, rounded up | SHA-256 |
| --- | --- | --- | --- |
| 204 | `101859759444979981360793459/6878398651426000000000000` | 14.808644367227 | `761af9ec961d812a313b9b119845af6f8d2befa79ca770d0d919a09673a97543` |

The certificate gives 204 unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in Evan Daniel’s certificate format.
The issue links `certificates/best/n204.cert`; the root `certificates/n204.cert` at the
pin is the same Git blob, and its per-count JSON, `certificates/n204.json`, names the
same digest and credits the seed to Mykhailo Polkovskyi (Mishapolk), search job 107960
(`slp`).

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
Retained: `source/certificates/best/n204.cert`, the certificate the issue links, and `source/certificates/n204.json`, 2 files, 23,284 bytes.
The repository states no licence for its data or prose, so the certificates and their
JSON are retained as factual data under the owner decision of 9 October 2026 recorded in
[known-best-packings/README.md](../known-best-packings/README.md).
Pinned by digest only: the root `README.md` and `upper_bounds.json`, the certificate
directory’s `README.md`, `manifest.json` and `SHA256SUMS`, and the source’s exact checker
`verify_bound_certificate.py` with its MIT licence `BOUND_VERIFIER_LICENSE.txt`, which are
byte-identical to the copies the [issue-678 packet](../couzo-issue678-2026-10-18/README.md)
retains and were not run.
The issue’s 78 other rows and the rest of the tree are pinned by the commit alone.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, by the declaration-driven importer
`devtools.upper_bound_reports` ([acquisition/report.json](acquisition/report.json)):
`sqpack`’s exact witness verifier and the independent rational corner checker, each
deciding every wall and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process.
The positive passes both routes, and both routes refuse both controls. In the positive a square touches the box, a least wall clearance of exactly 0, which the closed box allows, and every pair clears by at least $1.20 \times 10^{-12}$. The 3 jobs made 124,236 pair decisions in 10.07 route CPU seconds, on one worker on 22 October 2026.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method. No source program ran here, and the entry
awaits a stage 4 review (think-0nse).

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record on `main` at `d7923b8d`, 22 October 2026: above the case’s house best packing,
Couzo’s own #678 certificate (T-223), by $1.53 \times 10^{-6}$; above Evan Daniel’s view
of that packing (T-225) by the same; below Couzo’s #670 (T-226) by $5.05 \times 10^{-8}$
and T-186 by $1.89 \times 10^{-5}$.
The [18 October ledger](../../../campaign/issue-intake/upper-bounds-20261018/README.md)
recorded it in report order, after #670; #678 and T-225 came later, each smaller. So
T-228 enters superseded.
Measured pose by pose in the
[issue-672 packet’s measurement](../couzo-issue672-2026-10-17/measure/identity.json),
this packing is #670’s under the identity (5 squares beyond a tenth), and #678’s is one to
one with it (none beyond a tenth, at most 0.085): Couzo’s own sequence, so no
regularization is recorded.

## Credit

Francisco Couzo, whose issue keeps every seed, construction and certificate credit in
the source’s manifest; the per-count JSON credits the seed to Mykhailo Polkovskyi.
The source discloses OpenAI Codex assistance with its checker.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-issue675-2026-10-18 --check
python -m devtools.upper_bound_reports couzo-issue675-2026-10-18 check-claims
python -m devtools.upper_bound_reports couzo-issue675-2026-10-18 certify --jobs-dir "$TMPDIR/jobs" --workers 1
python -m devtools.upper_bound_reports couzo-issue675-2026-10-18 check --replay
python -m devtools.upper_bound_reports couzo-issue675-2026-10-18 register-plan
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
