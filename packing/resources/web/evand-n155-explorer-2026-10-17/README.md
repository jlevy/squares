# Evan Daniel’s n155 Basin-Explorer Upper Bound

This packet retains the single upper-bound claim in
[issue #669](https://github.com/jlevy/squares/issues/669), its two exact certificates
and the complete standalone checker dependencies.
This is source custody only: no source verifier, mathematical replay or stage 4 review
was run during acquisition.

## Source and Dates

| Field | Value |
| --- | --- |
| Source | [evand/square-packing](https://github.com/evand/square-packing) |
| Pin | `59326b86291b76c39d843f3f156e8f25fa0f6e3f` |
| Source publication | 2026-10-17T14:48:34Z, the first commit containing `s155_ex2.cert`; author and committer dates agree |
| Issue publication | 2026-10-17T14:49:46Z |
| Licence | MIT, copyright 2026 Evan Daniel; [LICENSE](source/LICENSE) retained |
| Retrieval | Exact UTC time in [acquisition/sources.json](acquisition/sources.json) |
| Custody | [Declaration](acquisition/declaration.json), [manifest](acquisition/upstream-subtree.sha256), [inspection receipt](acquisition/custody-review.json) |

## Complete Claim Inventory

The one reported result is

`s(155) <= 2590452188930112807053435932173/200000000000000000000000000000`,

exactly `12.952260944650564035267179660865`, reported as the upward-rounded bound
`12.952260944651`. Both certificates state this same side:

| Certificate | Role | SHA-256 |
| --- | --- | --- |
| [s155_ex2.cert](source/search/packer/candidates/s155_ex2.cert) | Original rational packing | `a1a3b6e7c2ce4d7de79efc2e07fc0bf53616dc44b732a2849b4dc4d8f7e2c4cc` |
| [s155_ex2_regularized.cert](source/search/packer/candidates/s155_ex2_regularized.cert) | Source’s regularized display view at the same side | `ab3c0b93aa205a907da5387cc119df11164c0a6d63b49b81332d7ce77910a897` |

The display view is not a second bound.
The source reports 17 angle groups after its own regularization; that is not a claim
that this repository’s strong regularizers have run.

Issue #669 compares with Daniil Ostashev’s T-149, approximately `12.952425406958`, and
reports a different local minimum reached from that packing.
The retained `s155_ex2.json`, `s155_ex2_prior.json` and `s155_ex2_vs_prior.json` record
the author’s numerical KKT, second-order, contact and matching diagnostics.
The 80-digit numerical side begins `12.952260944650564035137657…`; it is distinct from
the exact rational certificate side above.
These diagnostics are numerical source assertions, not interval proofs, independent
review or proof of global optimality.
Comparison against the current register and other pending reports remains intake work.

## Credit and Disclosure

The issue names Evan Daniel and explicitly asks for Daniil Ostashev’s T-149 packing to
be credited as the search start.
It describes 18 basin-explorer moves followed by re-polishing and numerical exact
solving, with the improvement found 75 minutes into the test run.
The [source credits](source/CREDITS.md) disclose Claude (Anthropic) under human
direction and state that nothing has been peer reviewed.
The pinned commit records Claude Opus 5.5 as co-author.

One source metadata inconsistency is preserved: `s155_ex2_regularized.json` contains
`by: ["Francisco Couzo"]`, while the issue and `s155_ex2_prior.json` identify Daniil
Ostashev’s packing as the start.
Acquisition does not rewrite that field or decide whether it is stale metadata.
Registration should preserve the issue’s explicit lineage and resolve the conflicting
field before using it as attribution evidence.
The author resolved it in
[his comment on #669 of 20 October 2026](https://github.com/jlevy/squares/issues/669#issuecomment-6302893217):
the field was a bug in his tooling, which took it from the record holder at that count in
his 5 October batch instead of from the packing drawn, fixed in
`search/packer/candidate.py` at `a435c97`. He names `s155_ex2` among the affected views
and asks that the field be read as no credit at all; the issue’s credit line stands.

## Exact Replay Dependencies

Both [verify_cert.py](source/search/exact/verify_cert.py) and
[verify_cert2.py](source/search/exact/verify_cert2.py) are standalone programs importing
only `sys` and `fractions.Fraction`. Each consumes a certificate path directly; no
numerical solver, compiled engine, network source or external repository is required for
these replay entry points.

Both parse the same rational centre and tangent-half-angle format.
The first checks strict wall clearance and pair separation along square face normals,
with a circumscribed-disc shortcut.
The second constructs rational vertices and checks polygon containment and edge
intersections, with the same disc shortcut.
The source reports acceptance of both certificates by both checkers.
It explicitly states shared authorship and format; their different geometry methods do
not establish outside independent authorship.
The programs were read as source and were not imported or executed during acquisition.

## Retained and Omitted Material

`devtools.acquire_source` retained 15 files, 186,330 bytes:

- `LICENSE`, `CREDITS.md`, root `README.md`, and the exact-format and packer READMEs.
- Both standalone exact checker programs.
- All eight `s155_ex2` candidate files: original certificate, 80-digit numerical
  coordinates, binary64 input, solver report, prior-packing report, regularized
  certificate, regularized report and comparison report.

The chronological `search/packer/PACKER.md`, discovery `explore.py` and numerical
producer `search/exact/exactsolve.py` are digest-only lineage pins: three files, 498,347
bytes. They are not dependencies of the two completed-certificate checkers.
Their full numerical/search dependency closure, unrelated candidate families, run
directories, site assets and other bulk data are omitted and commit-pinned only.
This packet makes no claim to reproduce discovery, numerical optimization, the
prior-packing comparison or regularization itself.
No retained data file crosses the repository’s 1,000-line compression threshold.

## Custody Check

From `packing/`, using the project interpreter and external scratch:

```bash
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  evand-n155-explorer-2026-10-17 --check
```

The [inspection receipt](acquisition/custody-review.json) records the command and
outcome. The check establishes the manifest, file bytes and declaration contract only.
A later replay and dedicated review must separately establish any geometric verdict or
evidential upgrade.

## Exact Replay

Added on 19 October 2026 for the stage 4 replay (think-8kx2, think-0lu6), with the import
declaration [acquisition/report.json](acquisition/report.json) that
`devtools.upper_bound_reports` reads.
The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion.
The count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on one worker.
The positive passes both routes, and both routes refuse both controls.
Every positive clears every wall by at least $5.00 \times 10^{-21}$ and every pair by at least
$9.99 \times 10^{-21}$.
The 3 jobs made 71,610 pair decisions in 43.29 route CPU seconds and 86.75 job wall
seconds, summed; the longest job took 29.99 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code; the source’s own checkers ran separately, below.

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `14fd9e27f` (19 October 2026), each side rebuilt from its own retained
packet or read from its print:

| Report at 155 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-174`, the case ceiling | Daniil Ostashev, improved by PingYou Ltd | $1.64 \times 10^{-4}$ |
| `T-149` (#501) | Daniil Ostashev | $1.64 \times 10^{-4}$ |

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n155-explorer-2026-10-17 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n155-explorer-2026-10-17 check --replay
```

## The Source’s Own Checkers

Added on 23 October 2026. The source’s two checkers, as this packet retains them, ran
unchanged, each in its own `python -I` child process under CPython 3.14.7, on both certificates and
on three controls of each: square 2 replaced by square 1; square 1 moved $S + 2$ to the
right, outside the box; and the side lowered by the least right or top wall clearance
plus $10^{-30}$, so that one square crosses the wall by exactly $10^{-30}$.
Both checkers accept both certificates and refuse all six controls with an `INVALID` verdict, 16 runs
in 2.4 CPU seconds.
`verify_cert.py` prints the least wall clearance as $5.000 \times 10^{-21}$ on each certificate and the least pair separation
as $1.000 \times 10^{-20}$ on each.
[receipts/source-checker-replay.json](receipts/source-checker-replay.json) keeps both
checkers’ digests, each certificate’s and each control’s digest, and every run’s exit
status and output. `devtools.evand_source_checkers check` holds it to the packet,
rebuilding each control from its certificate.

These are the author’s programs, so their acceptance is evidence from the same
implementation and moves no rung: the confirmation rests on the two routes above.
The two checkers share their author, their parse and their format, so neither is
independent of the other.
A run of the same two checkers on the four certificates of #669 and #674 on 18 October
2026 was not kept; this one replaces it.

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.evand_source_checkers check
uv run --frozen --all-extras --group dev python -m devtools.evand_source_checkers run --scratch "$TMPDIR/evand-controls"
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
