# Stage 4 Review Programs for Four #446 Fine-Net Certificates, 23 October

These are the programs and receipts of the stage 4 mathematical review of wand125’s
certificates `mixed_n19_L48275`, `mixed_n20_L49125`, `mixed_n26_L5555` and
`mixed_n27_L5655`, whose findings are the
[review of 23 October](../../../../../../docs/project/reviews/review-2026-10-23-wand125-446-fine-net.md).
They read this packet’s retained candidates and logs as data and the 8 October facts
packet’s records; nothing here runs a program of the source or of the maintained route.

## Independence

The programs were written by the stage 4 review lane `c-review-t233-math` (bead
`think-bwis`), a Claude (Anthropic) agent at the `tbd-strong-max` tier and maximum
reasoning, prompted separately from the records lane, from:

- the mathematics: this repository’s `packing/sqverify_fast/SOUNDNESS.md` and §1 of the
  measure verifier’s specification
  (`docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md`);
- the certificate format: the source’s `SPEC.md` and each bundle’s `README.md`;
- the source’s outputs, read to compare: the check2 and pre-publication receipts and the
  run and control logs.

Their authors did not read, before or after the programs ran, the source’s adapted crate
(pinned by digest, not opened), its `fine_net_check.sh`, this repository’s
`packing/sqverify_fast/src/`, the census driver or the maintained fine-net tools
(`devtools/fine_net_followup.py`, `devtools/audit_wand125_declared_net.py`,
`devtools/check_sqverify_fast.py`). They share no code with any of them: clean room.
Authorship overlaps the producer’s at the level of the system family.
The source’s commits carry Claude co-author trailers, and the crate the source adapted
was written by a Claude agent of this project.

They use CPython 3.14.7 (`fractions`, `hashlib`, `json`, `zlib`, `gzip`) and numpy 2.5.2
on OpenBLAS 0.3.34, run with `OPENBLAS_NUM_THREADS=1`; `crate_identity.py` also calls
`git show` on the repository it is given.

## The Programs

| Program | Role | What it does |
| --- | --- | --- |
| `programs/t233lib.py` | library | The strict reader, exact rationals, the $D_4$ expansion, the net, and the core’s capture: exact (Sutherland–Hodgman clipping of the core against each image in fractions, after a float classification with a $10^{-9}$ slack that is the exact decision) and float (for the search only) |
| `programs/premises.py` | premises | Every exact premise of each candidate: custody, the claim, the field order, the measure and its expansion, lemma N0 (a) to (e), the sharp extent, the last bin, the per-bin domains, F3’s caps, agreement with the source’s summary, the semantic digest |
| `programs/custody.py` | premises | Re-derives the retention record from the stored bytes, the asset digests against the source’s `ASSET.json` and the 8 October packet, and the source’s inventory and the subtree manifest against the retained files |
| `programs/crate_identity.py` | premises | Compares the 8 October manifest’s digests of the source’s 20 archived verifier files with this repository’s `packing/sqverify_fast` at named commits, by `git show`; reads no code |
| `programs/net_cover.py` | premises | The net’s orientation coverage by direct exact geometry at 10,363 orientations: core strictly inside the unit square, the half-turn bound, the per-bin domain’s monotonicity, and the bins’ contiguity and reach |
| `programs/geometry_selftest.py` | test, decides nothing | Eighteen analytic area fixtures for the exact clipping, and float against exact capture at 40 random poses |
| `programs/receipts_check.py` | decides poses | The source’s run and control logs as data; the exact capture at every rotated direction’s least-bound box centre (8,288) and at the four axis argmins; the 124 rotated control witnesses recomputed as fractions |
| `programs/axis_decide.py` | decides one direction | Index 0 of each certificate decided completely: exact `int64` events and overlaps on the $10^{-17}$ grid, one binary64 matrix product under an a priori bound, an exact comparison, and the 64 smallest vertices again in fractions |
| `programs/direction_sample.py` | decides poses | 32 rotated directions per certificate: an independent grid and compass search for the least capture, then exact values at every search’s end |
| `programs/controls.py` | test, decides nothing | Mutations the checks must refuse: reader, premises, the axis decision of each 99/100 mutant, four wrong conventions at the 31 control witnesses of n = 19, and the 99/100 mutant at the sample’s least points |

## How to Run Them

From the repository root, with the project interpreter:

```bash
PKT=packing/resources/web/wand125-fine-net-lower-bounds-446-release-2026-10-08
R=$PKT/review/review-2026-10-23
FACTS=packing/resources/web/wand125-fine-net-lower-bounds-2026-10-08
export OPENBLAS_NUM_THREADS=1
PY="packing/.venv/bin/python3 -I"
$PY $R/programs/premises.py --packet $PKT --out $R/outputs/premises.json
$PY $R/programs/custody.py --packet $PKT --facts $FACTS --out $R/outputs/custody.json
$PY $R/programs/crate_identity.py --manifest $FACTS/source-manifest.json --repo . \
  --commit e020eb1e2 --commit 910b6b12c --out $R/outputs/crate-identity.json
$PY $R/programs/net_cover.py --out $R/outputs/net-cover.json
$PY $R/programs/geometry_selftest.py --packet $PKT --out $R/outputs/geometry-selftest.json
$PY $R/programs/receipts_check.py --packet $PKT --out $R/outputs/receipts-check.json
$PY $R/programs/axis_decide.py --packet $PKT --out $R/outputs/axis-decision.json
$PY $R/programs/direction_sample.py --packet $PKT --receipts $R/outputs/receipts-check.json \
  --out $R/outputs/direction-sample.json
$PY $R/programs/controls.py --packet $PKT --sample $R/outputs/direction-sample.json \
  --scratch "${TMPDIR:-/tmp}" --out $R/outputs/controls.json
```

`--only N` limits `receipts_check.py`, `axis_decide.py` and `direction_sample.py` to one
count. Each program overwrites its output and exits 0 only on its passing verdict.

## What They Printed

Final runs on 23 October 2026, at `nice -n 19`, one at a time; the CPU is each program’s
own `getrusage`, children excluded.

| Program | Receipt | Printed | CPU (s) |
| --- | --- | --- | ---: |
| `premises.py` | `outputs/premises.json` | `ALL_PREMISES_HOLD`; 2,776, 3,768, 4,916 and 5,696 distinct images; $B(1 + D) = 25009997/25010000$; gains $1/400$, $3/400$, $1/100$, $23/2000$; the semantic digest reproduced by sorted compact JSON | 1.1 |
| `custody.py` | `outputs/custody.json` | `ALL_CUSTODY_HOLDS`; the source’s inventory differs from the retained files only in `README.md` | 0.1 |
| `crate_identity.py` | `outputs/crate-identity.json` | at `e020eb1e2`, 16 of 20 identical; differ `README.md`, `SOUNDNESS.md`, `src/certificate.rs` (30,446 here, 31,964 archived), `tests/adversarial.rs`; at `910b6b12c`, 12 of 20 | under 1 |
| `net_cover.py` | `outputs/net-cover.json` | `NET_COVERS`, 10,363 orientations, least clearance $6.9967 \times 10^{-8}$ at node 0, $u = 1/10004$ | 1.0 |
| `geometry_selftest.py` | `outputs/geometry-selftest.json` | `PASS`, 18 of 18 fixtures; float within $1.12 \times 10^{-11}$ of exact at 40 poses | 0.9 |
| `receipts_check.py` | `outputs/receipts-check.json` | `RECEIPTS_CONSISTENT` at each count, `ALL_CONSISTENT`; 31 of 31 control fractions equal at each; least exact margin at the least-bound centres $7.45 \times 10^{-4}$, $7.24 \times 10^{-4}$, $3.38 \times 10^{-4}$, $6.41 \times 10^{-4}$ | 61.6 |
| `axis_decide.py` | `outputs/axis-decision.json` | `decided` at each count, `AXIS_DIRECTION_DECIDED`; rigorous least captures $1.0015172217$, $1.0010018544$, $1.0009906901$, $1.0009178105$ | 16.3 |
| `direction_sample.py` | `outputs/direction-sample.json` | 32 directions per count, least exact $1.000676$, $1.000651$, $1.000308$, $1.000495$; 32 of 32 mutant witnesses at each; `NO_COUNTEREXAMPLE_IN_SAMPLE` | 471.4 |
| `controls.py` | `outputs/controls.json` | every control `refused`; the right conventions reproduce 31 of 31 fractions; `EVERY_CONTROL_REFUSED` | 25.8 |

Digests of the programs as they ran (SHA-256):

| Program | SHA-256 |
| --- | --- |
| `t233lib.py` | `4466ef0298916750e64600c4e04bd54ee2547e9736cf9af61a7c64e8f8961582` |
| `premises.py` | `ab4657fb6832af60bcbebc6a6adc364aeedfb95838b90bce863549fe37a04685` |
| `custody.py` | `8d6ff7d9147f0bfcb6bec568c90d296ea3da0acba5f35d6c6b0879f19891d923` |
| `crate_identity.py` | `b393ffbe9679ba960a3f50e43934972048f6abb81134e4a98bc41c109a3246df` |
| `net_cover.py` | `f3bca65b8144f795d073155a8a603f7d98044c7c01c5074f90c9b07bf22202b4` |
| `geometry_selftest.py` | `ea2ee4fa4ba734264e9b5827d04f356d7ab363ee1dd96c4b4cc447a82544d615` |
| `receipts_check.py` | `c77cf2a429ad5fd513c3c92cca8fc5f873b3ca14380b6c3ca56161fbaf3568a5` |
| `axis_decide.py` | `c8c49cdc265ebc2e72c62f7edb18cf4fc55206dd155bcf52d40b811d4985c9b9` |
| `direction_sample.py` | `cf4e8007c612cf49dffb78dd99d90d7e8af5176856ebe0a7b1ebcc64443a3ff9` |
| `controls.py` | `d5ece9a704ff51a2749c836607803d483185c5079d8abf8179971d8c2b70a4d0` |

## What Failed Along the Way

- The first run of `geometry_selftest.py` stopped writing its receipt because numpy
  scalars are not JSON values; the float capture now returns a Python float.
  The fixtures had passed.
- `axis_decide.py` first assumed every coordinate’s denominator divides $10^{16}$, and
  refused at n = 19, where some divide only $10^{17}$; it now uses $Q = 10^{17}$, which
  `int64` holds with room to spare ($6Q < 2^{63}$).
- The first search in `direction_sample.py` (a $33 \times 33$ grid, six starts at the
  best grid points) ended at the same corner value, $1.0015354745832443$, at half the
  directions of n = 19, while starts at the source’s boxes went lower.
  It was replaced by a $49 \times 49$ grid with one start in each of 16 blocks, and the
  sample widened from 12 to 28 strata.
  The trial receipts were deleted; the numbers above are the final runs’.
- `premises.py`, `net_cover.py` and `axis_decide.py` were run again after the library’s
  float fix and the axis program’s control option, so every receipt here is of the
  programs as retained.
- The host has 4 cores and its load stood at 17 to 37 throughout, so wall times are
  several times the CPU times; every program ran at `nice -n 19`, one at a time.

## What Cites Them

The review proposes, in its record changes, three evidence entries: the premises
(`premises.py`, `custody.py`, `crate_identity.py`, `net_cover.py`), the axis direction
(`axis_decide.py`), and the captures (`receipts_check.py`, `direction_sample.py`). Each
is cited by the case records at n = 19, 20, 26 and 27 and not by the result, since a
sample derives no rung.
`geometry_selftest.py` and `controls.py` decide nothing and are cited by no evidence
entry.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
