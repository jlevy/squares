# Francisco Couzo’s Issue 675: 77 Certificates at c6da0fc7

Francisco Couzo’s [issue #675](https://github.com/jlevy/squares/issues/675), opened
2026-10-18T06:02:11Z, a follow-up to #672, asks to register 79 upper bounds for n = 204
and 419 to 998, each the exact rational side of a certificate in
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/c6da0fc7524d667bf3d224559724ba9b60762e60)
at `c6da0fc7524d667bf3d224559724ba9b60762e60` (committed 2026-10-18T05:46:00Z) rounded up
at 12 places.
This packet retains the one row in the n ≤ 324 case corpus, s(204), registered as T-228.
Since 22 October it also retains the 76 certificates the issue’s 78 rows beyond the
corpus read, recorded as dated beyond-horizon rows ([Beyond the Corpus](#beyond-the-corpus)).

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
Retained: every certificate the issue links, `source/certificates/best/nN.cert`, 77
files, with the root per-count JSON `certificates/nN.json` at each of the 79 counts, 156
files, 7,991,120 bytes (2.81 MB as Git’s zlib stores them): the 204 pair at 01:24Z on 22
October for T-228, and the rest from the same pin at 04:41Z. The root JSON describes the
root certificate of its count, which is the `best/` file at every count but 992 and 995.
The repository states no licence for its data or prose, so the certificates and their
JSON are retained as factual data under the owner decision of 9 October 2026 recorded in
[known-best-packings/README.md](../known-best-packings/README.md).
Pinned by digest only: the root `README.md` and `upper_bounds.json`, the certificate
directory’s `README.md`, `manifest.json` and `SHA256SUMS`, and the source’s exact checker
`verify_bound_certificate.py` with its MIT licence `BOUND_VERIFIER_LICENSE.txt`, which are
byte-identical to the copies the [issue-678 packet](../couzo-issue678-2026-10-18/README.md)
retains and were not run.
The rest of the tree is pinned by the commit alone.

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

## Beyond the Corpus

The issue’s 78 rows from 419 to 998 read 76 `certificates/best/nN.cert`, each first
committed at the pin, sixteen minutes before the issue
([receipts/first-commits.json](receipts/first-commits.json)); 992 and 995 are the 993 and
996 certificates less their last square, at the same side, and are decided as such:
removing squares from a packing leaves a packing.

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) reads every
certificate a row beyond the corpus names from this packet once `acquire_source --check`
holds it, and decides it with the filtered two-route decision and the six controls of
[`devtools.couzo_678_replay`](../../../devtools/couzo_678_replay.py), reused unchanged:
route `sqpack` through `sqpack.witness` and `sqpack.verify`’s exact predicates, route
`independent` through `devtools.check_rational_witness_independent`’s, over every corner
against every wall and every pair whose centres are closer than √2 by exact comparison.
A unit square’s interior lies in the open disc of radius √2/2 about its centre, so no
other pair can overlap; both routes check that every square is a unit square whose corner
mean is that centre. The [18 October packet](../couzo-issue678-2026-10-18/README.md#exact-replay)
states the six controls.

**All 78 rows are verified.** Every printed side is its header side rounded up at 12
places, and both routes accept every packing: 142,270 candidate pairs of 23,086,008, and
every corner against every wall. 64 touch the box and 8 have touching pairs, 795 in all,
which the closed contract allows; elsewhere the least pair gap is between 1.0e-12 (at 641)
and 2.9e-09. **All 456 controls of the 76 certificates are refused by both routes.** The
positive decisions took 90.3 CPU seconds;
[receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json) keeps every
row’s side, both routes’ counts, least clearance, least gap and failures, the controls,
and the per-count JSON’s seed credit. The maintained all-pairs kernel,
`devtools.evand_arrangement_reports`’s two routes with no filter, decided every pair at
998: 497,503 pairs in 105.0 CPU seconds; both routes accept it, and their least pair gap
and wall clearance equal the filtered decision’s exactly
([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json)). The all-pairs replay
of every row, about 4 CPU-hours for the three Couzo packets at that rate, is not run; the
filtered route is the replay of record, as for #678 and #715. Every side is below Göbel’s
classical construction at its count, by 1.00e-05 at 919 or more
([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The [backlog ledger of 22 October](../../../campaign/issue-intake/upper-bounds-backlog-20261022/README.md)
walks every report at these counts from the 18 October ledger’s starts, frozen at `main`
`804eff369`, and records all 78. Each is superseded on entry by the next report the walk
records at its count: Couzo’s #678 (54) and #715 (6), and Darius Muglich’s #686 (18).
[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record
the source register reads them from.

## Credit

Francisco Couzo, whose issue keeps every seed, construction and certificate credit in
the source’s manifest; the per-count JSON credits the seed to Mykhailo Polkovskyi.
The source discloses OpenAI Codex assistance with its checker.
Beyond the corpus the per-count JSON credits Joost de Winter’s seeds or constructions at
21 counts, Fang’s rectangle and gluing with PingYou Ltd’s square input at 813 and 931, and
Couzo’s at most of the rest; those statements are the source’s.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-issue675-2026-10-18 --check
python -m devtools.upper_bound_reports couzo-issue675-2026-10-18 check-claims
python -m devtools.upper_bound_reports couzo-issue675-2026-10-18 certify --jobs-dir "$TMPDIR/jobs" --workers 1
python -m devtools.upper_bound_reports couzo-issue675-2026-10-18 check --replay
python -m devtools.upper_bound_reports couzo-issue675-2026-10-18 register-plan
python -m devtools.beyond_horizon_replay check --issue 675
python -m devtools.beyond_horizon_replay check --issue 675 --replay --workers 2
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
