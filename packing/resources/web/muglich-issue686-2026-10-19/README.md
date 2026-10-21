# Darius Muglich’s 100 Certificates in the Issue 686 Attachment, 19 October 2026

Darius Muglich (gfppoy) reports 100 upper bounds for n = 328 to 998 in
[jlevy/squares#686](https://github.com/jlevy/squares/issues/686), one exact rational
certificate for each count.
Every count lies beyond the n ≤ 324 case corpus, so no register entry records them: each
is a dated beyond-horizon row of the `muglich-issue686-2026-10-19` source in
[`source-coverage.yaml`](../../../frontier/source-coverage.yaml).
They establish upper bounds only.
The source claims no priority, rigidity or optimality, and decides none.

## Source and Credit

| Field | Value |
| --- | --- |
| Issue | [jlevy/squares#686](https://github.com/jlevy/squares/issues/686), opened 2026-10-19T20:43:04Z |
| Evidence | The attachment `01-squares-100-certificates-and-poses.zip`, at two addresses that serve the same bytes: [files/33685905](https://github.com/user-attachments/files/33685905/01-squares-100-certificates-and-poses.zip) and [files/33685972](https://github.com/user-attachments/files/33685972/01-squares-100-certificates-and-poses.zip) |
| Pin | 8,824,142 bytes, SHA-256 `6b711d6e80c9828497ba09d44673ee490c00ccae51b80587ec591d940722a874`, which the issue states; there is no commit or DOI |
| Bibliography key | **[Muglich issue 686 2026-10-19]** |
| Human credit | Darius Muglich, after the seeds and sources each case’s `provenance.json` names, Francisco Couzo’s certificates most often; `ATTRIBUTION.md` also credits Evan Daniel’s solver and workflow and the public contributions of Joost de Winter and Kevin Fang |
| AI assistance | The issue and the archive’s `ATTRIBUTION.md` state that OpenAI Codex assisted with optimization, orchestration, verification and packaging |
| Licence | The archive states none. On 20 October 2026 the author released his contributions under CC BY 4.0 ([comment 6302118274](https://github.com/jlevy/squares/issues/686#issuecomment-6302118274)), to the extent of his rights, and asked that the contributors each `provenance.json` names be credited beside him |
| Retrieved | 20 October 2026, through `NO_PROXY=github.com`, since the session proxy refuses `user-attachments` |

The archive does not offer these as 100 independent structures.
Its `ATTRIBUTION.md` says many cases are deletions, borders, crops or refinements of
other holders’ packings, and that the per-case `provenance.json` is authoritative for
each construction’s origin.
Of the 100 records, 47 cite Francisco Couzo’s repository, 13 of them naming him as the
construction’s credit; 62 mention a deletion, border or crop, and 27 classify their case
as dependent on another.
At n = 810 the certificate refines Couzo’s by about 6.33e-8, and the author asks that it
not be advertised as a new structure.

## Custody

`devtools.acquire_source` keeps only Git checkouts, and an issue attachment has none.
The packet therefore follows the one precedent for an attachment, SQUISH #401’s n153
certificate in [`squish-401-2026-10-07`](../squish-401-2026-10-07/README.md): derived
facts and the attachment’s address and digest, not the archive’s bytes.
Whether an attachment’s address and digest are an acceptable pin, and whether the
archive should now be retained under the author’s CC BY 4.0 grant, are the owner’s
decisions; the packet decides neither.

This packet retains:

- [`facts/`](facts/): one deterministic-gzip JSON fact per count, `n-NNN.json.gz`, with
  the certificate’s exact side and every square’s exact centre and half-angle tangent
  `t = tan(theta/2)`, in Evan Daniel’s certificate format’s order
- [`acquisition/sources.json`](acquisition/sources.json): the two addresses, the size
  and SHA-256 of the archive, `raw_asset_retained: false`, each certificate’s member
  path, size, SHA-256, exact side, the issue’s print and its fact’s path, and the path,
  size and SHA-256 of all 808 archive members
- [`acquisition/provenance.json.gz`](acquisition/provenance.json.gz): the 100 per-case
  `provenance.json` records, read as JSON and kept as attribution metadata, each with
  its member path; their original digests are in the archive manifest
- [`acquisition/issue-686.json`](acquisition/issue-686.json): the issue’s body as
  opened, which holds the printed sides
- [`acquisition/beyond-horizon-claims.json`](acquisition/beyond-horizon-claims.json):
  each count’s print, exact side and that side rounded up at 16 places, which
  `check_source_coverage` reads every row against
- [`receipts/`](receipts/): one complete exact replay receipt per count,
  `exact-replay-nNNN.json.xz`

No certificate, coordinate export, SVG, proof receipt, comparison table, checker or
other archive file is retained as bytes.
`verify_public.py`, the archive’s checker, was not run.

## Claims

Each certificate is `n S` followed by `n` rows `x y t`, every value an exact rational.
The issue prints each side rounded upward at 15 places, and every exact side lies in
`(P - 10^-15, P]` for its print `P`; the fact reader refuses a certificate that does
not. The
[20 October ledger](../../../campaign/issue-intake/upper-bounds-20261020/README.md)
takes the 100 claims in report order with the earlier reports at the same counts (#666,
#670, #672, #675 and #678) and records every one: each is decidably below the record on
`main` and every earlier report.

## Replay

`devtools.muglich_686_import certify` ran, for every count, a positive job and the two
kernel controls, one square replaced by a copy of another (overlap) and one square moved
outside the container, through the two exact routes of
`devtools.evand_arrangement_reports`: the native `sqpack.witness.exact_verify` and
`devtools.check_rational_witness_independent`. Both decide every pair and every wall
over the rationals, with no filter.
Each job ran in its own child process under `nice -n 10`, two at a time.

All 100 positives pass both routes, and both routes refuse both controls at every count:
300 jobs, 145,844,484 pair decisions, 29,169.55 route CPU seconds and 35,076.09 job wall
seconds, the longest job 397.51 seconds (a control at n = 993, on a shared host).
Every positive clears every wall by at least 5.000e-21 and every pair by at least
1.000e-12. The run went from 01:30Z to 06:28Z on 21 October 2026 in four resumed
batches; the first stopped at its two-hour limit after n = 757, and nothing was decided
twice. `check --n 328 --replay` decided n = 328’s three jobs again and matched its
receipt.

The two routes share certificate parsing, the half-angle conversion, Python `Fraction`
arithmetic and the separating-axis method.
The archive says its own two exact checkers come from Evan Daniel’s repository and share
the same representation; neither ran here.
Independent review and confirmation remain pending, so every row is `reported`.

## Commands

From `packing/`, with the project interpreter:

```shell
python -m devtools.muglich_686_import derive --archive ZIP --check
python -m devtools.muglich_686_import claims-record --check
python -m devtools.muglich_686_import check
python -m devtools.muglich_686_import check --n 328 --replay
```

`derive --check` rebuilds every fact, the provenance record and the manifest from a
local copy of the attachment, which it refuses unless its size and SHA-256 are the
issue’s. `check` holds the facts to the manifest and to the issue’s prints, the claims
record to its rebuild, and every receipt to its count’s fact; `--replay` decides the
selected counts again.
`certify --jobs-dir DIR --workers 2` resumes an interrupted replay: a count whose
receipt is admitted is skipped, and a finished job left in `DIR` is reused.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
