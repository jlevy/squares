# Portable Custody and Scalar Replay

[The first-party checker](check.py.txt) reconstructs the custody and scalar decisions in
this packet. It uses Python’s standard library and reads the contributor’s programs only
as retained bytes and JSON strings.
It never imports or executes them, invokes Git, fetches a URL, or writes to the
checkout.

From `packing/`, with the project’s Python 3.14 environment:

```bash
uv run --frozen python resources/web/de-winter-1042-public-replay-2026-11-20/replay/check.py.txt \
  --repo .. --self-test
```

`--repo` accepts another checkout root.
If omitted, the checker searches its own ancestors for the comparison table.
The `.py.txt` suffix follows the archived-checker convention; pass the file directly to
Python. Apply the project’s memory guard when running locally.
The prepared replay used a 90-second and 0.35-GiB ceiling.

## Inputs and Checks

The three compressed files here preserve the original preparation inputs.
Their contents, rather than a checkout at a particular Git revision, determine the
replay.

- `issuecomment-7022143149.api.json.gz` contains the original official API response.
  Its digest matches `source_api_sha256` in the existing acquisition manifest.
  The checker compares the comment identity, posting and edit times, exact body, decoded
  base85 ZIP, all four uncompressed members and every computed manifest field.
  Retrieval time and the historical base revision remain acquisition metadata; they are
  validated as a dated timestamp and revision string, not recomputed.
- `earlier-classification.json.gz` contains the 139-row classification used by the
  original scalar run.
  The checker also proves that its ordered `n`, `report`, `kind` and exact `value`
  projection equals those same four reports in the checkout’s current classification.
  Later classification verdicts and case-lane baselines do not enter this historical
  scalar comparison.
- `later-1060-D.csv.gz` contains the original decompressed Attachment D table.
  It must equal the checkout’s current retained table byte for byte after decompression.

Using exact `Fraction` arithmetic, the checker reconstructs every scalar receipt row,
including the full original claim and source specification, stated endpoint gain, mass
inequality, same-count predecessor, earlier monotone floor, same-report parent and later
endpoint comparison.
It compares the complete reconstructed JSON structure and types and the exact 155-row
TSV. Only `summary.wall_seconds` and `summary.peak_rss_bytes` are removed from the
historical receipt for comparison.
Other fields, including unexpected fields, must match.
The two original measurements are printed separately from this replay’s new cost.
No original receipt is rewritten.

`--self-test` adds nine bounded controls: duplicate JSON keys, a non-improving endpoint,
a mass equal to the square count, a changed row disposition, a changed summary, a
boolean replaced by an integer, an undeclared telemetry-like field, the permitted change
to exactly the two declared measurements, and an unexpected ZIP member.
Seven controls reject changed data, one rejects an unsafe ZIP inventory, and one
confirms the declared measurement exclusion.

Inputs have compressed and decompressed size limits.
JSON rejects duplicate keys; the ZIP must contain exactly the four expected members,
with bounded sizes and no absolute or parent-relative paths.
No archive member is extracted to disk.
The original ZIP’s digest is checked before opening its compressed members.

## Scope

A passing run reproduces 155 endpoint gains, 94 stated mass inequalities, 61
`family_cut` dependency labels, 148 primary rows, seven same-report consequences and 153
strictly higher later endpoints.
It does not establish the measures’ coverage, the correctness of any contributor
program, current case standing, theorem validity or registration readiness.
The maintained `devtools.lower_bound_claims` walk separately handles current case lanes.

The source and comparison inputs below are exact historical bytes.
The original acquisition and scalar execution measurements remain in the packet.
The initial portable replay completed with worker and guard exit zero under normal
pressure; its separate supervisor evidence is held by the intake coordinator.

| Compressed file | Origin | Git blob of uncompressed original | SHA-256 of uncompressed original |
| --- | --- | --- | --- |
| `issuecomment-7022143149.api.json.gz` | Original official GitHub API response | `1ee531ab5c804fb808796d8f8d56246e76bb0c57` | `aa7143e402295d82c009e511ed8df176c5b9c678aa4037f7aa7bbc7700740c0d` |
| `earlier-classification.json.gz` | Original 139-row scalar comparison basis | `e905ac70bac5afd525665d7c38e6540e6c030b71` | `d6bd03d641defd596b2550f62b25fb5945a2df7a7e270303521085a94b8ca74b` |
| `later-1060-D.csv.gz` | Original Attachment D scalar comparison basis | `3110257ab9aa6eaa70fcedf6bff84bb6e1a05f86` | `81e11c944fd64f80fb59314f75c2969a5bf4cba433e74fc94995dc8b7bc3ca42` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
