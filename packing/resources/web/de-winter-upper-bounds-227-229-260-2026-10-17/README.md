# Joost de Winter’s Three Upper Bounds of 17 October 2026

This packet retains the complete exact-witness replay inputs for the three claims in
[issue #668](https://github.com/jlevy/squares/issues/668). It records source custody
only. No source checker, mathematical replay or stage 4 review was run during
acquisition; source audit outcomes remain the author’s assertions.

## Source, Licence and Dates

| Field | Value |
| --- | --- |
| Repository | [JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing) |
| Retained revision | `9bf5d9be4d0ca13a1dbef7d7953032fe87d4e81d`, committed 2026-10-17T14:27:31Z |
| Original issue pin | `c95c4938f068ed44a1819ef973e770ec241aa567`, committed 2026-10-17T13:52:56Z |
| Publication | Source records date the claims 2026-10-17; the exact witnesses first appear in the original pin. Issue #668 was created 2026-10-17T14:06:25Z |
| Licence | MIT, copyright 2026 Joost de Winter; [LICENSE](source/LICENSE) retained |
| Retrieval | See [acquisition record](acquisition/sources.json) for the exact UTC retrieval time |
| Custody | [Declaration](acquisition/declaration.json), [SHA-256 manifest](acquisition/upstream-subtree.sha256), [inspection receipt](acquisition/custody-review.json) |

The original issue pin predates the licence.
A local Git comparison between the original pin and the retained revision changes only
the new `LICENSE` and two lines in the root `README.md`; every blob under `n227/`,
`n229/` and `n260/` is unchanged.
The retained successor therefore supplies the author’s published licence while
preserving the exact claimed witnesses and their checker dependencies.

## Complete Claim Inventory

| Count | Reported upper bound, rounded upward | Authoritative exact side and witness | Source record timestamp |
| --- | --- | --- | --- |
| 227 | `15.563796703670` | [records.json](source/n227/records.json), [exact JSON](source/n227/n227_exact.json.gz) | 2026-10-17T11:55:45.212086Z |
| 229 | `15.650174756949` | [records.json](source/n229/records.json), [exact JSON](source/n229/n229_exact.json.gz) | 2026-10-17T10:45:24.409375Z |
| 260 | `16.645778804182` | [records.json](source/n260/records.json), [exact JSON](source/n260/n260_exact.json.gz) | 2026-10-17T09:59:54.987687Z |

The source compares these with catalogue commit
`804eff369193b698d497a9c06847059eb9de0470` and sides `15.57106781186547`,
`15.65685424949238` and `16.65685424949238`, respectively.
These are reported feasible upper bounds, with no optimality, uniqueness or exhaustive
worldwide novelty claim.
All three belong to one Young-corner/slipped-ribbon construction family; the 229-square
packing descends from the 260-square packing.
The source audit also mentions retired 507/553 claims and composites 965/969/1097; it
explicitly excludes them from its three-result inventory.
No comparison with later reports or current house adoption is decided here.

## Credit and Shared Dependencies

The source names Joost de Winter, with numerical search, rational witness construction,
checker implementation and figures produced by OpenAI Codex agents under his direction.
The issue reports 25 workers in the 17 October session, at most six concurrent, and
subsequent Claude replay and publication preparation.
It credits prior comparison packings through this repository’s case pages and catalogue
pin; that lineage remains part of later registration.

Each count directory is self-contained for its documented `verify_all.py` entry point:

- `records.json` identifies that count’s authoritative `nN_exact.json`, its SHA-256,
  exact rational side and upward decimal bound.
- `verify_all.py` reads those two files and imports `certify` from `verify_exact.py`,
  `check` from `verify_polygon_exact.py` and `check` from `verify_polygon_clipping.py`.
- The three implementations use Python 3.10 or later and standard-library modules only.
  Their shared inputs include the exact rational witness and Python `Fraction`. The
  first two use separating-axis projection; the third uses polygon clipping and exact
  intersection area. They were authored within one AI-assisted campaign.
  Neither the retained source nor this acquisition establishes independent outside
  authorship.
- Source `audit/` summaries and receipts report the third checker, corrupted-input
  controls and analytic area tests.
  They are retained historical evidence, not results reproduced here.

No other repository is needed for the documented per-count replay.
Figure regeneration separately needs NumPy, SciPy and CairoSVG and is outside this
packet.

## Retained and Omitted Material

`devtools.acquire_source` retained 44 upstream files, 492,606 logical bytes: the
licence, root README and, for each count, its README, checksum list, claim manifest,
authoritative witness, source check receipt, four replay scripts and five audit files.
The three witnesses use deterministic archive gzip under the repository’s data policy.

The equivalent `nN_record.cert` exports are pinned by digest only: three files, 218,991
bytes. Their authoritative exact JSON counterparts are retained.
The upstream checksum lists mention intentionally omitted files; acquisition’s own
manifest defines this packet’s bounded scope.

PNG/SVG figures, topology comparisons, proof PDFs, proof ZIPs, floating-point coordinate
illustrations, baseline packings, rendering scripts, rendering receipts and
visualization instructions are omitted and pinned by the upstream commit only.
No bulk proof archive is required by the retained replay entry point.

## Custody Check

From `packing/`, with the project interpreter and external scratch configured:

```bash
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  de-winter-upper-bounds-227-229-260-2026-10-17 --check
```

The acquisition receipt records the check outcome.
This check validates declarations, retained bytes, compression metadata and manifest
coverage. It does not establish any geometric claim or upgrade an evidential rating.
Decompress each authoritative JSON to its original filename in an external scratch copy
before a separately authorized future source replay.

## Exact Replay

Added on 20 October 2026 for the stage 4 replay (think-8xr0), with the import
declaration [acquisition/report.json](acquisition/report.json) that
`devtools.upper_bound_reports` reads through its `center-basis-json` adapter.
The adapter reads each witness’s exact rational side and, for each square, its rational
centre and basis $(c, s)$. It takes the half-angle tangent $t = s / (1 + c)$ and refuses
a basis that is not exactly the rotation $t$ gives, so no float is read.
Each side is the `certified_side_exact` its `records.json` states, and each printed
bound is that side rounded up at twelve places.

Each certificate goes through the maintained two-route kernel: `sqpack`’s exact witness
verifier and the independent rational corner checker, each deciding every wall and every
pair over $\mathbb{Q}$.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on two workers.
Every positive passes both routes, and both routes refuse every control.
Every positive clears every wall by $10^{-9}$ exactly and every pair by more than that,
at least $1.003$, $1.002$ and $1.030 \times 10^{-9}$ at 227, 229 and 260.
The 9 jobs made 512,562 pair decisions in 425.22 route CPU seconds and 489.54 job wall
seconds, summed; the longest job took 71.04 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs, and `check --replay` decided all nine
jobs again and held each to its retained row.
After the merge with `main` at `d588ad987` the same day, `check --replay` decided all nine
again in 116 seconds of wall on one process, and `check-claims` rebuilt the frozen
comparison equal.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code, and the source’s three checkers were not run.

## Compressed Files

| Stored file | Origin | Git blob of stored file | SHA-256 of decompressed source |
| --- | --- | --- | --- |
| `source/n227/n227_exact.json.gz` | upstream | `f315925aa11ddfb40963f5d162f62fc19520da25` | `5aa22dd00127aab5acef37ad993027e1e577d890f3dd5abdf7513d97775b981a` |
| `source/n229/n229_exact.json.gz` | upstream | `6da4f04eabbaae26f85063dd67015c65a4b9df0d` | `edb3ef2eed16e561c379350ac28882078e17717882ddc8284b67b794fef8111b` |
| `source/n260/n260_exact.json.gz` | upstream | `a8200a1e84f6729688e4a656ba1412308bc49f50` | `56ddfa73d992f52baee9ebc16a2c1bffed221e740f46dd7cd4ba456db93e2b9c` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
