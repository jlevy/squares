# Francisco Couzo’s Exact Certificate at 237, 4e4c8ce

[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/58a783368d4b7e70bb800f0009ea9ca03e578739/certificates)
publishes an exact rational packing of 237 unit squares that no issue reports.
This packet pins it at `58a783368d4b7e70bb800f0009ea9ca03e578739` (tree
`01cd91c65212b6a3336504c6c00adb90066caf8c`, committed 2026-10-15T01:25:11Z), the head of
`master` when retrieved at about 02:45Z.
The certificate `certificates/n237.cert` was first committed in `4e4c8ce` (“Update all
verified bounds for n < 1024”, 2026-10-15T00:31:53Z), with the same bytes at
`certificates/best/n237.cert`, and `58a7833` leaves both unchanged.

[Issue #607](https://github.com/jlevy/squares/issues/607), filed by the same author at
2026-10-14T23:18:36Z and not edited since 23:27Z, reports a different file at 237:
`submissions/2026-10-14/certificates/n237.cert` at `43ac7d2`, printed as
15.902603638284. That issue’s import is think-qik6, on its own branch.

| n | Exact side of the certificate | Rounded up at 16 places | Printed by | Requested |
| --- | --- | --- | --- | --- |
| 237 | `7951301819129798440089572127137/500000000000000000000000000000` | 15.9026036382595969 | the certificates README: 15.902603638260 | no issue |

## What the Commits Change

`4e4c8ce` turns the repository’s certificate directory into an index of the best
certificate the author could verify at every count through 1023:
`certificates/best/` holds 515 finite witnesses with a manifest of credits and receipts,
most of them other authors’ certificates (PR #574, #593, #606 and others), and
`certificates/` gains copies of many of them.
The index has a certificate at 149 counts inside the case corpus.
At 147 of them the file is another report’s certificate, credited to it, or is no
smaller than the smallest earlier report; 16 of those are PR #574’s rational enclosures
of closed-form records, which the 14 October ledger decided.
Two are the author’s own and smaller than every earlier report: this certificate at 237,
and `certificates/n211.cert`, unchanged since `487b058` (think-nj7h).
`58a7833` adds exact Göbel square and strip constructions over $\mathbb{Q}(\sqrt 2)$ as
upper bounds at many counts; the author claims no discovery for them, and inside the
corpus they equal closed forms the record holds.

`certificates/n237.json` calls this certificate an exact optimum, seeded from Mykhailo
Polkovskyi’s issue-593 certificate (its `seed_certificate` states #593’s side,
T-183’s) and found by the author’s `fq` search (job 100230) from an external seed file.
It is 2.40e-11 below the #607 certificate, which #607 says also continues #593.
The index credits Francisco Couzo, with construction credit Nate Chaoweeraprasit
(itsnaka).

## Retained Here

`devtools.acquire_source` wrote the packet from a blobless clone with a sparse checkout
at the pin, from the declaration in
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
13 files, 2,213,004 bytes.

The repository states no licence for the author’s files: the tree has no licence file,
and neither `README.md` nor `certificates/README.md` states reuse terms.
`BOUND_VERIFIER_LICENSE.txt` is Evan Daniel’s MIT licence, covering the author’s checker
`verify_bound_certificate.py`, not the certificates.
The certificate under `source/certificates/` (33,742 bytes) is retained as factual data
under the owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md)).
The three READMEs, the identical copy `certificates/best/n237.cert`, the metadata
`certificates/n237.json`, the decimal packing `n237.txt` and its drawing, the author’s
index files (`certificates/best/manifest.json`, `certificates/best/SHA256SUMS`,
`upper_bounds.json`), the checker and its licence are pinned by digest only.
No prose or program is copied.

## Exact Replay

Only the retained certificate enters geometry decisions.
It goes through the maintained two-route kernel of `devtools.evand_arrangement_reports`
by `devtools.upper_bound_reports certify`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion.
A positive job, a duplicate-square control and an outside-container control each ran in
its own child process, with one worker.

The positive passes both routes, and both routes refuse both controls.
Both routes find the same least wall clearance, exactly `1/200000000000000000000`
($5 \times 10^{-21}$), and the same least pair gap, just under $10^{-20}$, the margins of
an exact optimum written at 20 places.
The three jobs made 167,796 pair decisions in 50.9 route CPU seconds and 65.48 job wall
seconds, summed; the longest job took 22.07 seconds.
`certify --workers 1` ran from 02:54:23Z to 02:55:33Z on 15 October on a four-core
machine shared with five other lanes, at a load average near 13.
A fresh `check --replay` decided all three jobs again, equal to the retained rows apart
from timing, in 66 seconds from 02:56:16Z.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. The third exact route, `devtools.check_half_angle_area`, is a separate review
lane and did not run here.
No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) compares the certificate with the case
record and every other report at 237, as `main` stood at `22a67ce4a`, after #614 adopted
T-183 as the house at 237. Each side is exact, read from its own packet; #607’s was
first compared at its print, rounded up, until the records lane of 15 October registered
its packet as T-189 and read it exactly. That lane also added T-056, which the
declaration had left out, and froze the record at `c4c690a3e`, with T-140 as the house;
every relation is the same at both.

| Report | Holder | Side | This certificate is below by |
| --- | --- | --- | --- |
| Case T-183 (#593) | Chaoweeraprasit, improved by Couzo, Polkovskyi | 15.902705057866 | 1.01e-4 |
| #488, T-140 | Couzo | 15.9029496076778317 | 3.46e-4 |
| #561, T-161 | Couzo | 15.902947773658 | 3.44e-4 |
| PR #574, T-174 | PingYou Ltd | 15.902947773658 | 3.44e-4 |
| T-056 | Couzo | 15.911191683008479 (printed) | 8.59e-3 |
| T-098 (#375) | Daniel | 15.911191683002 | 8.59e-3 |
| T-115 (#401) | Chaoweeraprasit | 15.903676235191 | 1.07e-3 |
| T-127 (#438) | Gupta | 15.903676235189 | 1.07e-3 |
| T-134 (#476) | Couzo | 15.903670905581 | 1.07e-3 |
| T-136 (#481) | Chaoweeraprasit | 15.902989220875 | 3.86e-4 |
| #505 | Barnett | 15.903670905778 | 1.07e-3 |
| #470 | Polkovskyi | 15.90367623519 | 1.07e-3 |
| #573 | Polkovskyi | 15.90294960768 | 3.46e-4 |
| #607, T-189 | Couzo | 15.9026036382835755 | 2.40e-11 |

The certificate is the smallest at 237.
[review/compare_lineage-output.txt](review/compare_lineage-output.txt) measures it
against #593’s, #607’s and #488’s packings with
`mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py`: 195 of its 237 squares
are within $10^{-3}$ of #593’s and all within 0.066, as its metadata’s seed says, and
T-190 lists it as a regularization of T-183. Under a reflection of the box, 217 are
within $10^{-6}$ of #607’s and all within 0.076; that measurement decides no credit.

A publication in a watched repository is a report from its first commit, here
2026-10-15T00:31:53Z, after #607 (filed 2026-10-14T23:18:36Z; its certificates were
first committed at `43ac7d2`, 19:15:09Z).
Under the per-count rule ([stage 1](../../../campaign/result-import.md#several-reports-at-one-count))
it is strictly stronger than every earlier report, so it is recorded after #607’s, as
T-190.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The author’s index reports that his checker and this repository’s `sqpack` verify at
`37e6757` accept it; those runs are the author’s, and no program of the source ran here.
Its metadata’s “exact optimum” is the author’s word; local or global optimality,
rigidity and novelty are not established.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificate is kept as
factual data and nothing of the source is relicensed.
#607 asks that its 237 be credited as a continuation of Mykhailo Polkovskyi’s
issue-593 certificate, and this certificate’s metadata names the same seed; the index
names Nate Chaoweeraprasit (itsnaka) as the construction’s origin.
Evan Daniel’s optimizer, contact solver and verifier and this repository’s exact
verifier were used.
The pinned files state nothing about AI assistance; #607, the day before, states that
OpenAI Codex assisted search and verification orchestration, that earlier search work
used Claude Code, and that the author directed the work.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-n237-2026-10-15 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-n237-2026-10-15 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-n237-2026-10-15 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-n237-2026-10-15 check --replay
uv run --frozen --all-extras --group dev python resources/web/mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py couzo-n237-2026-10-15 237 mishapolk-records-2026-10-14 couzo-certificates-2026-10-14 couzo-certificates-2026-10-10
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`register-plan` prints the record entries the import needs; no record is edited here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
