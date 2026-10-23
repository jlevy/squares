# Evan Daniel’s n229 Dilation Bound: Opening Report

This packet retains one chronological version of the upper-bound claim in
[issue #674](https://github.com/jlevy/squares/issues/674). It is source custody only.
No source verifier, source control or stage 4 review was executed during acquisition.

## Source, Licence and Dates

| Field | Value |
| --- | --- |
| Source | [evand/square-packing](https://github.com/evand/square-packing) |
| Pin | `e0338c7becf95dbc7584b48d8868c0a1cd21079c` |
| Source publication | 2026-10-17T23:09:24Z; author and committer dates agree, and this commit adds the named certificate and input |
| Report publication | 2026-10-17T23:10:59Z |
| Licence | MIT, copyright 2026 Evan Daniel; [LICENSE](source/LICENSE) retained |
| Retrieval | Exact UTC time in [acquisition record](acquisition/sources.json) |
| Custody | [Declaration](acquisition/declaration.json), [manifest](acquisition/upstream-subtree.sha256), [inspection receipt](acquisition/custody-review.json) |

## Claim and Chronology

The single reported claim is
`s(229) <= 7825081627429265081627421439843/500000000000000000000000000000`, reported as
the upward-rounded bound `15.650163254859`.

The author’s
[later update](https://github.com/jlevy/squares/issues/674#issuecomment-6244298663) asks
to register its smaller side in place of this opening value.
That is retained separately in
[the 18 October update packet](../evand-n229-dilation-update-2026-10-18/README.md).
This packet preserves the original report; it does not treat the opening value as the
final requested bound.

| File | Role | SHA-256 |
| --- | --- | --- |
| [s229.cert](source/search/packer/candidates/s229.cert) | Exact rational certificate | `0366e8178e37d7c5b4baf002d35f4c1088b4e20ab8f90283d418f634c8af204d` |
| [s229.input.txt](source/search/packer/candidates/s229.input.txt) | Source binary64 packing | `7df8cd6fe3252fb8b015fea731229ef065130498014f1660aa0ccf435ee990fe` |

Both versions are dilation certificates for upper bounds only.
Neither the issue nor this acquisition establishes optimality or local minimality.
Comparison with the current register and other intake reports is separate work.

## Credit and AI Disclosure

The issue names Evan Daniel and asks for Francisco Couzo’s #672 packing to be credited
as the start, following Joost de Winter’s #668. It describes the same tilted structure
as #672, with upright squares rearranged; the update continues that lineage.
The issue’s stated comparison is against Couzo’s `15.650174740273`, after de Winter’s
`15.650174756949`, rather than against the older register alone.
Those are the author’s historical comparison statements, not a fresh standing check.

The retained [CREDITS.md](source/CREDITS.md) discloses Claude (Anthropic) working under
human direction and states no peer review.
The pinned certificate commit names Claude Opus 5.5 as co-author.
Both exact checkers share authorship and certificate format; algorithmic differences do
not establish outside independent authorship.

## Checker Dependencies and Source Assertions

The retained `search/exact/verify_cert.py` and `verify_cert2.py` each read the named
certificate directly and import only `sys` and `fractions.Fraction`. The first uses
separating axes; the second tests exact polygon containment and edge intersection.
Both use a circumscribed-disc shortcut.
No other repository, compiled engine, network data or numerical solver is required by
these standalone exact-replay entry points.

The source reports both accept this certificate and gives pair separation about
`1.0e-12` and wall clearance about `5.0e-13`. These are author-reported outcomes, not
acquisition measurements.
No per-claim corrupted-input or analytic control receipt accompanies the two claim
files. This packet claims no new controls or acceptance verdicts.

The retained `search/packer/dilate_cert.py` documents the construction: scale centres
and the box by approximately `1 + 10^-12`, keep unit square size, round coordinates to
rationals and replace each angle with a rational half-angle tangent.
The script imports only standard-library `argparse`, `math`, `sys` and `fractions`; it
is a numerical producer, separate from exact-certificate acceptance.
It was read as source and never executed here.

## Retained and Omitted Material

`devtools.acquire_source` retained nine files, 85,722 bytes: the licence, credits, root
and exact-format READMEs, both standalone checkers, dilation producer and this version’s
certificate and binary64 input.
No retained data file crosses the repository’s 1,000-line compression threshold.

No file is digest-only within this packet’s declared nine-file scope.

Other certificates, numerical search tools and their dependency closures, run histories,
site assets, figures and bulk source data are omitted and pinned by the source commit
only. The opening and updated pins also differ in unrelated site files; this packet does
not retain or review those changes.
It does not reproduce numerical search or independently certify the dilation argument.

## Custody Check

From `packing/`, with the project interpreter and external scratch configured:

```bash
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  evand-n229-dilation-2026-10-17 --check
```

The [inspection receipt](acquisition/custody-review.json) records the command and
outcome. The check establishes declaration, manifest and retained-byte consistency.
Geometric replay, dedicated review, registration and any house adoption remain separate.

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
Every positive clears every wall by at least $5.01 \times 10^{-13}$ and every pair by at least
$9.99 \times 10^{-13}$.
The 3 jobs made 156,636 pair decisions in 92.75 route CPU seconds and 140.22 job wall
seconds, summed; the longest job took 47.78 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code; the source’s own checkers ran separately, below.
The clearances are the dilation’s $10^{-12}$ margin, as the source describes it.

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `14fd9e27f` (19 October 2026), each side rebuilt from its own retained
packet or read from its print:

| Report at 229 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-155`, the case’s verified ceiling (the catalogue’s $10 + 4\sqrt{2}$ reported) | the Kingbird catalogue | $6.69 \times 10^{-3}$ |
| `T-196` (#668), printed | Joost de Winter | $1.15 \times 10^{-5}$ |
| #672, printed | Francisco Couzo | $1.15 \times 10^{-5}$ |

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n229-dilation-2026-10-17 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n229-dilation-2026-10-17 check --replay
```

## The Source’s Own Checkers

Added on 23 October 2026, and re-run the same day with a fourth control and a bare
child environment (review A6 and A8 of #747). The source’s two checkers, as this
packet retains them, ran unchanged on the certificate and on four controls of it: square 2 replaced by square 1;
square 1 moved $S + 2$ to the right, outside the box; the side lowered by the least right
or top wall clearance plus $10^{-30}$; and every square moved left and down by the least
left or bottom wall clearance plus $10^{-30}$.
In each sharp control one square crosses a wall by exactly $10^{-30}$, at the right or
top wall in the first and at the left or bottom wall in the second, where a checker
with a floating-point tolerance would accept it.
Each run is its own `python -I` child process under CPython 3.14.7, given an empty
environment, no standard input and a scratch working directory.
Both checkers accept the certificate and refuse all four controls with an `INVALID`
verdict, 10 runs in 2.6 CPU seconds.
`verify_cert.py` prints the least wall clearance as $5.010 \times 10^{-13}$ and the least pair separation
as $9.997 \times 10^{-13}$.
[receipts/source-checker-replay.json](receipts/source-checker-replay.json) keeps both
checkers’ digests, each certificate’s and each control’s digest, and every run’s exit
status and output. `devtools.evand_source_checkers check` holds the packet to its
acquisition manifest and reads the receipt back: it covers the packet’s certificates,
records every control, and records each certificate accepted and each control refused
by both checkers. It rebuilds no control;
[tests/test_evand_source_checkers.py](../../../tests/test_evand_source_checkers.py)
rebuilds each from its certificate and holds its digest to the receipt’s.

These are the author’s programs, so their acceptance is evidence from the same
implementation and moves no rung: the confirmation rests on the two routes above.
The register enters the run as `E-evand-674-n229-opening-source-checker-replay`, listed in T-198’s evidence.
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
