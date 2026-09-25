# Guzhou0806’s R052 Lower Bound for `s(17)`, Retrieved 2026-09-25

A third-party release claiming an exact computer-assisted lower bound on `s(17)`, the
least side of a square holding seventeen unit squares with disjoint interiors.
It is retained because it is numerically the strongest public claim for this case that
the record has seen, above the `461300/99853` now on the frontier, and because its
replay is cheap enough to repeat here.

Retaining it registers no result and moves no bound.
What the repository makes of it belongs to a review; this packet holds the source bytes,
the replay receipts and the native-route outcome that review will cite.

## Provenance

| Field | Value |
| --- | --- |
| Source | <https://github.com/Guzhou0806/n17-square-packing> |
| Commit | `3bf1095c68a28fb9b2750fb0bc99edd5c22b7a61`, `main` at retrieval |
| Tree | `8ece9cd1a4736bd2008b8955296f8140ce676897` |
| Committed | 2026-09-25T05:07:19Z |
| Retrieved | 2026-09-25, about 08:05Z |
| Certificate, gzip | `826b3eabb8f4881ad02f6e20df890c37f19bb5f5bf4a5e343d9c34441f878756` |
| Certificate, decompressed | `d77743eadf7f4bf9c424549a37a4296ea3b23fceee4af8e3d774a5a07e62e825` |
| Package `MANIFEST.json` | `2a74ea2efef6be4435b227746d3e48f93075160b77ee5a0563a2dc81996952aa` |
| Upstream CI | [run 36097241509](https://github.com/Guzhou0806/n17-square-packing/actions/runs/36097241509), all three jobs green |

The decompressed digest is the one the source pins in `SOURCE_PIN.json` and checks in
`verify.py`; the manifest digest is the one its own `verification/R052.json` records for
the final records check.

**Credit, as the source states it.** R052 was “produced by Guzhou0806 / N17 project
with AI assistance”, using enlarged point and threshold resources and strict inner
cores, and continues **Kleddamag**’s public mixed-certificate architecture.
`SOURCE_NOTICES.md` names Kleddamag’s `17-squares-certified-bound` v1.0.0 at
`a499e2c7` as the source of the architecture and the Python implementation, and says
the release does not claim to reinvent weighted covering or threshold charging.
It lists Mira-acc/17squares and this repository in the method lineage.
Final acceptance upstream was local, with non-proposer AI review; the source claims no
human peer review and no proof-assistant check.

The source also records that its maintainer was told Kleddamag holds an unpublished
internal strict bound of `4.62001`. It attributes that result to Kleddamag, states that
its proof is neither included nor verified in R052, and makes no priority claim.
Nothing here checks that report.

## The claim

$$
s(17) > \frac{231001}{50000} = 4.62002
$$

The container side is `L = 4613/1000` and the parent side is `A = 230650/231001`, so
the bound is `L/A`. Site coordinates have denominator `23065657750900000000`; weights
have denominator `10^12`.

| Quantity | Exact value |
| --- | ---: |
| Total budget `M` | 16990246659579 units |
| Minimum core charge `Γ` | 999426274093 units |
| `17Γ − M` | 2 units |
| Angle rows | 15,721 |
| Strict containment inequalities | 62,884 |
| Point orbits / physical points | 2,354 / 18,585 |
| Threshold orbits: two-of-three / three-of-five | 514 / 54 |
| Physical threshold groups | 4,504 |
| Resource columns | 2,922 |

`Γ` is exactly `⌊M/17⌋ + 1`, the least integer charge that makes the count work, and
the source’s ledger reaches it exactly, at rows 15555 and 15556. The certificate has no
slack beyond that integer rounding.

## Method

The same weighted covering with strict cores as Kleddamag’s release, with a larger
resource dictionary.
Point orbits under the eight square symmetries expand to 18,585 sites; 873 orbits,
6,901 sites, carry positive weight.
Two-of-three orbits (514) and three-of-five orbits (54) expand to 4,504 groups, of which
2,036 carry positive weight: 1,988 two-of-three and 48 three-of-five.
A group of `m` points with threshold `k` and weight `w` charges a core holding at least
`k` of its points, so disjoint cores draw at most `w⌊m/k⌋` from it.

The geometry comes from R050: the certificate records R050’s certificate digest and a
uniform scale `230650000000/230656577509`, and five of R050’s 15,706 rows are each split
into four, giving 15,721.
Each row `[a, b, t, B]` assigns a closed core of side `B` at half-tangent `t` to every
parent half-tangent in `[a, b]`.

Two source checkers sweep every row’s legal-centre domain exactly: a Python/Numba
event-cell scanner whose implementation the source attributes to Kleddamag’s release,
and a Node/BigInt checker rebuilt at replay time from Guzhou’s own R038 scanner by two
pinned byte-edit recipes.
Both compare every row minimum with the frozen ledger.
`SOURCE_PIN.json` says the functions in `src/geometry.py` were extracted unchanged from
a file with SHA-256 `038c0575…8b81`. No file with that digest is in any of the eleven
public commits of the Guzhou repository or in the retained Kleddamag releases, so that
statement cannot be checked here.

## What Is Retained, and What Is Not

**Retained byte-identical** under `n17-square-packing/`, at their upstream paths: 31
files. That is the whole `certificates/R052/` package (22 files including its
`MANIFEST.json`), `verification/R052.json`, the root `README.md`, `NOTICE.md`,
`CITATION.cff` and `R052_PUBLICATION.json`, the `R042`, `R043` and `R050` publication
records, and `.github/workflows/r052.yml`.
Every file’s `git hash-object` equals its blob at the pinned commit.
`certificates/R052/MANIFEST.json` carries CRLF line endings as published; those bytes
are part of the package identity `verify.py` checks.

**Omitted, each for a reason:**

- The rest of the upstream repository. R012 and R038 are already retained, in
  [`../n17-weighted-certificates-2026-09-20/`](../n17-weighted-certificates-2026-09-20/)
  and
  [`../external-square-certificates-2026-09-22/dependencies/`](../external-square-certificates-2026-09-22/dependencies/);
  the R042, R043 and R050 packages are inventoried below by pinned path and digest.
- The rebuilt Node checker. The source deliberately does not redistribute it, and
  neither does this packet; `receipts/` records its SHA-256, which matches the source’s
  pin. It is rebuilt offline from the R038 scanner already retained at
  `../external-square-certificates-2026-09-22/dependencies/guzhou-r038/`.
- Replay outputs: the fresh row ledgers and chunk files. `receipts/` records their
  digests and compares them with the digests the source published.

**Licensing.** The upstream repository has no repository-wide licence.
In the source’s words, Kleddamag-derived sources and edit recipes keep the upstream
MIT licence, retained verbatim as `KLED_MIT_LICENSE.txt`; the source does not list
which files those are.
The certificate, ledgers and new prose carry no general grant; `LICENSE_SCOPE.md` and
`NOTICE.md` set attribution boundaries and restrict only redistribution of the rebuilt
Node checker. This packet is retained for verification and private research use on the
same basis as the earlier Guzhou retentions. Consult the author before redistribution.

## Replay Here

Every command ran on 2026-09-25 from `n17-square-packing/`, the retained repository
root, against the retained bytes, with outputs written outside this packet.
The machine is an Apple-silicon Mac with ten cores; unrelated processes were running,
so the walls are contended readings, not benchmarks.
[`receipts/replays.json`](receipts/replays.json) records each command, interpreter,
start, wall and exit; each mode’s directory keeps the source’s own `RESULT.json`,
`INPUT.json` and console output.

The two standard-library checks, as the source’s README gives them, under the project
interpreter:

```sh
python -X utf8 -B -S certificates/R052/verify.py --output OUT/r052-records
python -X utf8 -B -S certificates/R052/verify.py --containment --output OUT/r052-containment
```

The two full sweeps, as `REPRODUCIBILITY.md` gives them, at the most workers the
machine has:

```sh
python -X utf8 -B certificates/R052/verify.py --python-full --jobs 10 --output OUT/r052-python
python -X utf8 -B -S certificates/R052/verify.py --bigint-full --jobs 10 \
  --source ../../external-square-certificates-2026-09-22/dependencies/guzhou-r038/certificates/R038/src/exact_parent_side_scan.js \
  --output OUT/r052-bigint
```

The Python sweep ran in a separate CPython 3.14.7 environment holding exactly the
pinned `numpy==2.5.3`, `numba==0.67.0` and `llvmlite==0.49.0`; the source tested
3.12.14. The BigInt sweep ran under the project interpreter with Node `v24.19.0`, and
rebuilt its checker offline from the retained R038 scanner.

| Mode | Wall | Exit | Status | What it establishes |
| --- | ---: | ---: | --- | --- |
| records | 0.16 s | 0 | `PASS_R052_RECORDS` | Package manifest, certificate identity, the frozen 123-block ledger and its per-row minima; no geometry |
| containment | 3.81 s | 0 | `PASS_R052_CONTAINMENT` | Resource closure, budget, and 62,884 endpoint containment inequalities, least margin `4613/9240040000000000000` |
| python-full | 904.45 s | 0 | `PASS_R052_PYTHON_FULL` | Fresh exact centre minimum for all 15,721 rows, each equal to the ledger |
| bigint-full | 673.60 s | 0 | `PASS_R052_BIGINT_FULL` | The same, by the rebuilt Node/BigInt checker, in 123 chunks |

Both standard-library checks report package manifest `2a74ea2e…52aa`, the digest the source’s
validation record gives for its final records check.
The fresh Python row ledger has SHA-256 `f370defb…d4b8`, byte-identical to the
`fresh_rows_sha256` of the source’s own Python sweep on Windows under 3.12.14.
The rebuilt checker has SHA-256 `82fad041…24b1`, the source’s pin, and the fresh BigInt
ledger has `ee506dfe…17d1`, byte-identical to the frozen `BIGINT_ROWS.json` the source
ships. The two fresh ledgers agree on every row’s minimum, and the global minimum
`999426274093` falls only on rows 15555 and 15556, as the source says; no other row
comes within `10^6` units of it.

What these replays do **not** establish is independence of method.
Both source checkers decide the same exact event-cell sweep of the same certificate; the
native route below is the attempt at a distinct method.

The source’s validation record notes that its own full sweeps ran on a snapshot whose
`PROOF.md` and `MANIFEST.json` predate a wording revision. The sweeps here ran on the
final published package.

## The Native Route

[`packing/devtools/verify_guzhou_r052_native.py`](../../../devtools/verify_guzhou_r052_native.py)
reads the retained certificate into this repository’s `ParentCoreCertificate` without
importing any source code, and
[`packing/tests/test_guzhou_r052_native.py`](../../../tests/test_guzhou_r052_native.py)
holds it to the counts above and to eleven refused mutations.
The structure maps directly: rows become `ParentCoreRow`s, positive point orbits become
point atoms, and positive two-of-three and three-of-five groups become `ThresholdAtom`s
whose budget `w⌊m/k⌋` is the source’s own rule.
Site indices follow the source’s definition, and the test checks that every one of the
568 group orbits, zero weight included, is the D4 image set of its first group under
that table.

**Exact premises: verified natively.** `validate_parent_core` accepts the certificate:
D4 invariance of the weighted charges, the budget `16990246659579/10^12` equal to the
declared one, the counting gap of 2 units, a contiguous folded cover ending at
`207107/500000`, and all 62,884 containment quadratics minimized over whole intervals,
interior minima included, with least numerator `4613/4613131550180000000 > 0`. This is
a different check from the source’s, which evaluates containment only at interval
endpoints and relies on monotonicity in between.
Receipt: [`receipts/native/premises.json`](receipts/native/premises.json).

**Coverage: refused by the frozen engine.** The interval engine that decided
Kleddamag’s `n = 11` certificate refuses this one before searching a box, at static
allocation ceilings that do not depend on batch size:

| Dimension | R052 | Ceiling |
| --- | ---: | ---: |
| Atom rows (6,901 point + 2,036 threshold) | 8,937 | 8,192 |
| Distinct sites | 9,261 | 8,192 |
| Padded member slots (width 5) | 44,685 | 16,384 |
| Ragged member slots, for comparison | 13,105 | — |

Receipt: [`receipts/native/pilot-refused.json`](receipts/native/pilot-refused.json),
status `PREMISES_VERIFIED_COVERAGE_REFUSED`. A refusal is not evidence against the
certificate; no native coverage decision exists.

Deciding it needs those ceilings lifted in `interval.py` and `threshold_interval.py`:
sites and atoms to at least 9,261 at a batch of at most 1,024, which keeps the 16 MiB
site mask, and member slots to at least 44,685, or a ragged member table.
Both files are proof inputs that `packing/devtools/audit_kleddamag_n11_native.py` pins to Git
blobs at `c183cc9ab`, so the change needs a new proof commit and a re-baselined audit,
which is pipeline work in its own right.

**Sizing, not a decision.** The tool’s `--sizing` mode lifts those ceilings in its own
process only and times rows serially through the unchanged search.
On the four pilot rows, the first, the two at the ledger minimum and the last, it
certified every row with no stalled box and no exhausted budget:

| Row | Boxes | Certified lower bound (units) | Seconds |
| ---: | ---: | ---: | ---: |
| 0 | 7,823 | 999430203966 | 1.91 |
| 15555 | 47,299 | 999426274093 | 11.11 |
| 15556 | 46,427 | 999426274093 | 11.09 |
| 15720 | 45,199 | 999435492325 | 9.92 |

The two tight rows certify exactly at `Γ`, so the zero-slack rows do not stall the
box search. Receipt:
[`receipts/native/sizing-pilot.json`](receipts/native/sizing-pilot.json), status
`SIZING_ONLY_RAISED_CEILINGS`. It ran a configuration nobody has reviewed and covers
four rows of 15,721, so it supports neither a coverage claim nor a confirmation rung.
It prices the work: at two to eleven seconds a row, a complete run is roughly 8 to 49
CPU-hours, an estimate from four rows, not a measurement.

## Earlier Releases Not Yet in the Record

Three releases between R038 and R052, all at the same repository and all numerically
superseded by R052. Paths are at the pinned commit `3bf1095c`; none changed after its
own publishing commit.

| Release | Published (UTC) | Claim | Certificate | Relation |
| --- | --- | --- | --- | --- |
| R042 | 2026-09-23 10:46, `b1e060ea` | `s(17) > 115325/24963 = 4.619837…` | `certificates/R042/certificate/R042_CERTIFICATE.json.gz`: gzip `ec79424e…8e28`, JSON `ad47686f…59de` | Kleddamag’s schema at `A = 24963/25000`: 1,134 point and 253 two-of-three orbits, 7,853 rows, weights `10^−9`, `17Γ − M = 11` |
| R043 | 2026-09-23 15:57, `5c6d1c16` | `s(17) > 461300/99851 = 4.619884…` | `certificates/R043/certificate/R043_CERTIFICATE.json.gz`: gzip `667ba391…a7d1`, JSON `f0995a8d…cf4b` | R042’s support with four zero-weight point orbits activated; 7,853 rows, `17Γ − M = 13` |
| R050 | 2026-09-24 19:19, `48ff059b` | `s(17) > 4613000/998509 = 4.619888…` | `certificates/R050/certificate/R050_CERTIFICATE.json.gz`: gzip `a21f7adf…f9f7`, JSON `84283b2a…f400` | R043’s resources and weights, angle rows refined to 15,706; R052’s geometry is derived from this certificate |

All three sit above the frontier’s `461300/99853 = 4.619791…` and below R052’s
`4.62002`. R050’s own README already says it is not the best known bound, citing the
reported unpublished Kleddamag `4.62001`. Each release has a green upstream CI replay on
the pinned commit; none was replayed here.

## Retrieval Hashes

Digests of this packet’s copies, which are the source’s bytes unchanged.
The package’s own `MANIFEST.json` lists every package file’s SHA-256, and `verify.py`
checks the package against it on every run.

| File | SHA-256 |
| --- | --- |
| `certificates/R052/PROOF.md` | `b6adec4abfbd9adcc48ffd996f473b51c8fc9cb6e095481adca7b4fe5f06fb53` |
| `certificates/R052/verify.py` | `1ed3da8237a67857425a36857a6d4dde64e260eb5832f58b6f6b0fe4bbba4017` |
| `certificates/R052/certificate/R052_CERTIFICATE.json.gz` | `826b3eabb8f4881ad02f6e20df890c37f19bb5f5bf4a5e343d9c34441f878756` |
| `certificates/R052/results/BIGINT_ROWS.json.gz` | `09e4b0cf53de756b290ccde3b66f33a35d8023c25379a80653dc8603b0fe18c3` |
| `certificates/R052/MANIFEST.json` | `2a74ea2efef6be4435b227746d3e48f93075160b77ee5a0563a2dc81996952aa` |
| `verification/R052.json` | `112f9a2eeea7d45264879b16392102d0cc418658c91fc79c1e9dabaa45d46c63` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
