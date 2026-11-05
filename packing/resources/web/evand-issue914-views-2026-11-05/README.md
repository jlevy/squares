# Evan Daniel’s Regularized Views at 175, 204, 268, 293, 303 and 304 at bb4cc78

Issue [#914](https://github.com/jlevy/squares/issues/914) names, beside six of its seven
certificates, a regularized display view at the same side, each with its SHA-256:
`s175_1105_regularized.cert`, `s204_trig1_regularized.cert`,
`s268_1105_regularized.cert`, `s293_1105_regularized.cert`,
`s303_1105_regularized.cert` and `s304_1105_regularized.cert`, first committed with the
certificates at
[evand/square-packing `bb4cc78e5b35103c1f177db55e9cf08974e66563`](https://github.com/evand/square-packing/tree/bb4cc78e5b35103c1f177db55e9cf08974e66563/search/packer/candidates)
(2026-11-05T18:29:13Z). This packet exists so that both maintained exact routes decide
each view as they decide the certificates, with the same gross and sharp controls; the
[certificates’ packet](../evand-issue914-2026-11-05/README.md) holds the import, its
claim record and the register’s citations.

## Retained Here

Nothing: the six views and the licence are the certificates’ packet’s copies, retained
there at the same pin. [acquisition/declaration.json](acquisition/declaration.json) pins
them against those copies (`identical_to`), `devtools.acquire_source --check` compares the
two, and `devtools.upper_bound_reports` reads each view from there and holds it to the
pinned SHA-256, each the digest #914 prints
([acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256)). The scope is
7 files of 249,378 bytes, all pinned.

## What the Views Claim

Each view’s header states exactly its certificate’s side, which
[acquisition/report.json](acquisition/report.json) admits at the side #914 prints. The
issue calls each a regularized view at the same side; at 303 it says the view needed the
regularizer fix of `39fb4f0` and that its box is 1.9e-32 larger than the KKT point’s side
$S^*$, inside the certificate’s side. The views claim no bound of their own.
[acquisition/claims.json](acquisition/claims.json), read from `main` `249bb82e7`, finds
each below its count’s house by its certificate’s margin and equal to its certificate, so
no view is smallest and none is a further report; the ledger of 5 November walks the
certificates alone.

## Exact Replay

`devtools.upper_bound_reports certify` decided every view and its duplicate-square and
outside-container controls on both maintained routes, each job in its own child process:
18 jobs, 1,237,776 pair decisions, 160.32 route CPU seconds, the longest job 13.91 seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). Every view
passed and every control was refused on both routes, and `check --replay` decided all 18
again. Every view clears every wall by exactly 5e-21 and every pair by at least 9.99e-21,
as its certificate does.

`devtools.upper_bound_reports sharp-controls` took each view to exact contact and 1e-30
past it (`receipts/sharp-controls-nNNN.json`, one per count), with the same seven controls
and expectations as the certificates’ packet: both routes accepted each at contact and
refused each past it, and refused a duplicated square.

The two routes share certificate parsing, half-angle conversion, `Fraction` arithmetic and
the separating-axis method, and read each view through the `evand-cert` reader. The
source’s checkers were not run.

## How Each View Sits Beside Its Certificate

`devtools.measure_identity` measured each certificate against its view, in the
certificates’ packet’s `measure/identity-nNNN.json`. A measurement for credit; it decides
nothing. Each pairs with its certificate by the optimal assignment with 3 to 8 squares
beyond 0.1 (largest 0.332 to 0.623), one to one by nearest centres at 175, 204, 268, 303 and
304 and not at 293. Each view is a candidate drawing for the regularization the adoption
at its count runs.

## Credit and Licence

MIT, copyright (c) 2026 Evan Daniel, by the licence the certificates’ packet retains.
`CREDITS.md` says the repository’s work was “Produced by Claude (Anthropic) in a single
session under human direction”. The views are Daniel’s regularizer’s, of his packings; the
bibliography key is the certificates’, **[Daniel issue 914 2026-11-05]**.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-issue914-views-2026-11-05 --checkout CHECKOUT
python -m devtools.acquire_source evand-issue914-views-2026-11-05 --check
python -m devtools.upper_bound_reports evand-issue914-views-2026-11-05 check-claims --write
python -m devtools.upper_bound_reports evand-issue914-views-2026-11-05 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports evand-issue914-views-2026-11-05 check --replay
python -m devtools.upper_bound_reports evand-issue914-views-2026-11-05 sharp-controls
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
