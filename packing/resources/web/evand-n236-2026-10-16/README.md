# Evan Daniel’s s(236) Certificate

[Issue #659](https://github.com/jlevy/squares/issues/659) reports an exact rational
packing of 236 unit squares, in
[evand/square-packing](https://github.com/evand/square-packing/tree/5ad00693899ef50ccf6502f0346187cc422cc914/search/packer/candidates).
The packet pins the commit the issue names,
`5ad00693899ef50ccf6502f0346187cc422cc914` (tree
`52a60db559f7510d9d419418372ea4a26c2c3440`, committed 2026-10-16T14:03:49Z), which adds
the eight n = 236 files.
The issue was filed at 2026-10-16T14:05:14Z, 85 seconds later.
The sources were retrieved on 19 October 2026, when the branch head was `3a9948c`; no
later commit changes the certificate.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 236 | `7930967195303679308621899285697/500000000000000000000000000000` | 15.861934390608 | 15.8619343906073587 |

The certificate, `s236_bm3c.cert`, gives 236 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in the format of
issues #375, #489, #552, #584, #596 and #606.
The commit also holds the 80-digit KKT point it was certified from
(`s236_bm3c.exact.txt`), the binary64 packing that point was solved from, the solver’s
report, a summary of the record the author compared against (`s236_bm3c_prior.json`), a
regularized view of the same packing at the same side (`s236_bm3c_regularized.cert`, six
angle groups) with its report, and the source’s comparison with #481’s packing
(`s236_bm3c_vs_prior.json`). The claim rests on `s236_bm3c.cert`.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse blobless checkout at the pin,
from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
18 files, 715,732 bytes, of which 13 files and 225,971 bytes are retained.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/s236_bm3c.cert` | `89c11db9f6111f2797d57cc6bba936fb2292501c` | 34474 | `21dbf6792bec64b06ab5fc1d6ac56a17432f971431100fdbe63e92d23bc091c9` |
| `search/packer/candidates/s236_bm3c_regularized.cert` | `125ed84393fffaa8093b7e4a68e2a6a6792dae67` | 32686 | `abae0c5240f986373a4c49f860004ba3b187495579b4f88d41bfec0d9015a546` |

Both digests are the ones the issue prints.
Beside the two certificates the packet retains the KKT point, the binary64 input, the
solver’s and the regularizer’s reports, the prior-record summary and the comparison with
#481 (stored compressed, below), with `LICENSE`, `CREDITS.md`, the root `README.md`, and
the format and packer READMEs.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, are
pinned by digest only. They are byte-identical to the copies the
[n155 packet](../evand-n155-explorer-2026-10-17/README.md) retains, and were not run.
The packer’s working log (`search/packer/PACKER.md`), the basin explorer
(`search/packer/explore.py`) and the exact solver (`search/exact/exactsolve.py`) are
pinned by digest only.

The regularized view’s report, `s236_bm3c_regularized.json`, says `"by": ["Francisco
Couzo"]`, as the n155 and n271 views’ reports do; the issue credits the packing to
itsnaka’s composition and the author’s search, and the field reads as the regularizer’s
default rather than a statement of credit. It is retained as the source wrote it.
[The author’s comment on #669 of 20 October 2026](https://github.com/jlevy/squares/issues/669#issuecomment-6302893217)
confirms that reading: the field was a bug in his tooling, which took it from the record
holder at that count in his 5 October batch instead of from the packing drawn, fixed at
`a435c97`. He names `s236_bm3c` among the affected views and asks that the field be read
as no credit at all.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as the issue-606 import did: `sqpack`’s exact
witness verifier and the independent rational corner checker, each deciding every wall
and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
The count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on one worker.

The positive passes both routes, and both routes refuse both controls.
Every positive clears every wall by at least $5.00 \times 10^{-21}$ and every pair by at
least $9.99 \times 10^{-21}$.
The 3 jobs made 166,380 pair decisions in 70.45 route CPU seconds and 104.2 job wall
seconds, summed; the longest job took 45.11 seconds.
`certify --workers 1` took 111 seconds of wall time on 19 October 2026, on a four-core
host shared with other lanes at a load average of about 8.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `14fd9e27f` (19 October 2026), and `check-claims` rebuilds it, each
side from its own retained packet:

| Report at 236 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-146`, the case ceiling | Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel | $2.02 \times 10^{-3}$ |
| `T-174` (PR #574), staged for adoption | PingYou Ltd | $2.02 \times 10^{-3}$ |
| `T-136` (#481) | Nate Chaoweeraprasit (itsnaka) | $2.02 \times 10^{-3}$ |

The certificate is below every report the record holds or has pending at 236.
**In report order** (the owner’s rule of 14 October), #659 is the latest report at 236,
and the 18 October ledger
([upper-bounds-20261018](../../../campaign/issue-intake/upper-bounds-20261018/README.md))
records it, below the standing side by at least $2.02 \times 10^{-3}$.

## Lineage

The issue says the packing came from a replication test of #481: the author rebuilt
#481’s Mondrian composition from Kingbird’s s(152)_r2 corner piece and the register’s
s(88) (itsnaka, #422), in opposite corners of a box of side s(88) + 6, and his basin
explorer (fixed-side perturbation and re-polish, 45 minutes on one core) descended below
#481’s side; `exactsolve.py` certified the point.
It asks that itsnaka’s SQUISH composition (#481) be credited for the construction, and
calls the result a different local minimum from #481’s: 209 load-bearing squares move by
more than $10^{-4}$ and 20 by more than $10^{-2}$ under its matching, and no tilt angle is
shared. That is the source’s statement. The [review of 19 October 2026](../../../../docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md) measured it pose by pose: against the view of #481’s packing the case held, the best one-to-one assignment moves ten squares beyond a tenth and keeps 226 within one, another arrangement of #481’s design.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The source states that its KKT point is a local minimum, strict modulo 92 exact flat
motions, with 114 corner-to-corner contacts, no corner-to-corner MILP descent and 18
rattlers. Those are numerical evidence at 80 digits, as the source says, not interval
proofs, and were not replayed here.
Novelty, local or global optimality and rigidity are not established.
The regularized view has the same exact side; it is the source’s display view, not a
separate claim, and was not replayed.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which states that the work was done with Claude (Anthropic) under human
direction and without peer review. The pinned commit names Claude Opus 5.5 as co-author
and says the commit and post were approved by Evan Daniel.
The issue asks for the credit name “Evan Daniel (GitHub @evand)” and that itsnaka’s
#481 composition be credited for the construction.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-n236-2026-10-16 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n236-2026-10-16 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n236-2026-10-16 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n236-2026-10-16 check --replay
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 1` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs; the records
pull request of 19 October registers it as `T-218`.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/search/packer/candidates/s236_bm3c_vs_prior.json.gz` | upstream | `ecec1f9d2b8e6bb3ee408094dd27133879b10e3a` | `c9913cfccc54653689b030bde3a77805af89aed2ea9827c8169684fbf1fae0d5` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
