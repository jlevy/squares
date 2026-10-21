# Evan Daniel’s s(271) Certificate

[Issue #664](https://github.com/jlevy/squares/issues/664) reports an exact rational
packing of 271 unit squares, in
[evand/square-packing](https://github.com/evand/square-packing/tree/757b40bc6c5f681033ff1572177d408afbf26dfe/search/packer/candidates).
The packet pins the commit the issue names,
`757b40bc6c5f681033ff1572177d408afbf26dfe` (tree
`205fdb1d8838747d2f2fc455436e7f6461e70139`, committed 2026-10-17T04:29:03Z), which adds
the eight n = 271 files.
The issue was filed at 2026-10-17T04:30:51Z, 108 seconds later.
The sources were retrieved on 19 October 2026, when the branch head was `3a9948c`; no
later commit changes the certificate.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 271 | `16948947733713657510723401112423/1000000000000000000000000000000` | 16.948947733714 | 16.9489477337136576 |

The certificate, `s271_ex1.cert`, gives 271 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in the format of
issues #375, #489, #552, #584, #596, #606 and #659.
The commit also holds the 80-digit KKT point it was certified from
(`s271_ex1.exact.txt`), the binary64 packing that point was solved from, the solver’s
report, a summary of the record the author compared against (`s271_ex1_prior.json`), a
regularized view of the same packing at the same side (`s271_ex1_regularized.cert`,
21 angle groups) with its report, and the source’s comparison with #561’s packing
(`s271_ex1_vs_prior.json`). The claim rests on `s271_ex1.cert`.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse blobless checkout at the pin,
from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
18 files, 765,595 bytes, of which 13 files and 260,746 bytes are retained.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/s271_ex1.cert` | `292bd36495a6a4dacd293da5319d8c4c54cd6658` | 43090 | `48abf7ca68909c42e0aaa5215d4d578f4cdba29d6188775012ae24636e02d680` |
| `search/packer/candidates/s271_ex1_regularized.cert` | `1f4f1841d7d007f0dcaec656063832afd99bb4f4` | 42892 | `4d4d4e25604b2c492047b44144249e3d69be53db061ab51e26dab39e8fb12160` |

Both digests are the ones the issue prints.
Beside the two certificates the packet retains the KKT point, the binary64 input, the
solver’s and the regularizer’s reports, the prior-record summary and the comparison with
#561, with `LICENSE`, `CREDITS.md`, the root `README.md`, and
the format and packer READMEs.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, are
pinned by digest only. They are byte-identical to the copies the
[n155 packet](../evand-n155-explorer-2026-10-17/README.md) retains, and were not run.
The packer’s working log (`search/packer/PACKER.md`), the basin explorer
(`search/packer/explore.py`) and the exact solver (`search/exact/exactsolve.py`) are
pinned by digest only.

The regularized view’s report, `s271_ex1_regularized.json`, says `"by": ["Francisco
Couzo"]`, as the n155 and n236 views’ reports do; here it agrees with the issue’s credit
to Couzo’s #561 packing, but the same field on the other two views reads as the
regularizer’s default rather than a statement of credit. It is retained as the source wrote it.
[The author’s comment on #669 of 20 October 2026](https://github.com/jlevy/squares/issues/669#issuecomment-6302893217)
says it is no credit here either: the field was a bug in his tooling, which took it from
the record holder at that count in his 5 October batch instead of from the packing drawn,
fixed at `a435c97`, and he names `s271_ex1` among the affected views.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as the issue-606 and issue-659 imports did: `sqpack`’s exact
witness verifier and the independent rational corner checker, each deciding every wall
and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
The count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on one worker.

The positive passes both routes, and both routes refuse both controls.
Every positive clears every wall by at least $5.00 \times 10^{-21}$ and every pair by at
least $9.99 \times 10^{-21}$.
The 3 jobs made 219,510 pair decisions in 103.33 route CPU seconds and 119.55 job wall
seconds, summed; the longest job took 45.41 seconds.
`certify --workers 1` took 124 seconds of wall time on 19 October 2026, on a four-core
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

| Report at 271 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-186`, the case ceiling | Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, PingYou Ltd, Mishapolk | $4.46 \times 10^{-5}$ |
| `T-161` (#561) | Francisco Couzo | $4.46 \times 10^{-5}$ |
| `T-174` (PR #574) | PingYou Ltd | $4.46 \times 10^{-5}$ |
| `T-151` (#500) | Nate Chaoweeraprasit (itsnaka) | $1.69 \times 10^{-4}$ |

The certificate is below every report the record holds or has pending at 271.
**In report order** (the owner’s rule of 14 October), #664 is the latest report at 271,
and the 18 October ledger
([upper-bounds-20261018](../../../campaign/issue-intake/upper-bounds-20261018/README.md))
records it, below the standing side by at least $4.46 \times 10^{-5}$.

## Lineage

The issue says the author’s basin explorer (`search/packer/explore.py`: fixed-side
perturbation moves and re-polish) started from the register’s witness for 271 as one of
52 counts in a test run, and that the improvement came 90 seconds in, from one move that
swaps the tilt angles of two neighbouring squares, followed by a re-polish;
`exactsolve.py` certified the point.
It calls the packing a refinement of Francisco Couzo’s #561 packing, not a new
construction, and asks that #561 and Nate Chaoweeraprasit’s SQUISH packing it refines
(#500) be credited. It also calls it a different local minimum: the load-bearing tilt
angles match #561’s group for group within 0.12°, except that four squares near 31.7° to
32.0° in #561 are three here, and under its matching 59 load-bearing squares move by more
than $10^{-4}$ and 2 by more than $10^{-2}$.
That is the source’s statement. The [review of 19 October 2026](../../../../docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md) measured it pose by pose: it pairs one to one with #561’s packing under the identity, three squares moving beyond a tenth (at most 0.197), so in this record’s terms it continues Couzo’s arrangement rather than refining it.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The source states that its KKT point is a local minimum, strict modulo 54 exact flat
motions, with 259 corner-to-corner contacts, no corner-to-corner MILP descent and 4
rattlers. Those are numerical evidence at 80 digits, as the source says, not interval
proofs, and were not replayed here.
Novelty, local or global optimality and rigidity are not established.
The regularized view has the same exact side; it is the source’s display view, not a
separate claim, and was not replayed.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which states that the work was done with Claude (Anthropic) under human
direction and without peer review. The pinned commit names Claude Opus 5.5 as co-author
and says the submission was approved by Evan Daniel.
The issue asks for the credit name “Evan Daniel (GitHub @evand)” and that Couzo’s #561
packing and Chaoweeraprasit’s SQUISH packing it refines be credited.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-n271-2026-10-17 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n271-2026-10-17 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n271-2026-10-17 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n271-2026-10-17 check --replay
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 1` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs; the records
pull request of 19 October registers it as `T-219`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
