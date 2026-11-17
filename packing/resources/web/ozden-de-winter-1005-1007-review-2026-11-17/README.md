# Stage 4 Review of #1005, #1006 and #1007: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane R1’s blind stage 4 review of
three reports of 16 November 2026: issue
[#1005](https://github.com/jlevy/squares/issues/1005), Doğa Özden’s upper bound
$s(292)$; issue [#1006](https://github.com/jlevy/squares/issues/1006), Joost de Winter’s
upper bound $s(292)$; and issue [#1007](https://github.com/jlevy/squares/issues/1007),
Joost de Winter’s upper bounds $s(262)$ and $s(295)$:
[`docs/project/reviews/review-2026-11-17-ozden-de-winter-1005-1007.md`](../../../../docs/project/reviews/review-2026-11-17-ozden-de-winter-1005-1007.md).

The sources are files of
[kenaznia-doga/s292-upper-bound](https://github.com/kenaznia-doga/s292-upper-bound) at
`dec930bdaa5f58077af6c05bc13c0fca0a58a3ed` and of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing) at
`796ff3b76e7816f9df24bf4f6ef0bb3b9cacef24` (#1006) and
`853b92ee2236f418160782dd2871d38ea75271a4` (#1007), not retained here; an import lane
would retain them in its own packet.
This directory is review-only.

| Label | File | SHA-256 |
| --- | --- | --- |
| `1005-n292-yaml` | `n-292-candidate.yaml` at `dec930b` | `90a0e30681821da567835ce1c9e81cf52aa899985587a953eafa0701b1829a8a` |
| `1005-n292-json` | `n292-witness.json` at `dec930b` | `07b86d44562acf8cd3bbff45ed2f7e6a9573af2f099009cfa1bf320fdfcbd720` |
| `1006-n292-exact` | `n292/n292_exact.json` at `796ff3b` | `3d6fb90c9b79bc9dee984ec0e4b6ecc89bb1306afb266d0b75dcecea4a972b4a` |
| `1006-n292-witness` | `n292/n292_witness.yaml` at `796ff3b` | `6d8a1264e3ddb014fc4ffbd55b53fa4889e6fcf00eba9458a3da8544ee3b6c3e` |
| `1007-n262-exact` | `n262/n262_exact.json` at `853b92e` | `95875def0a2784e980ff92cacbe0508d84cc1ee03d6104130d9db4007a0ffa04` |
| `1007-n262-witness` | `n262/n262_witness.yaml` at `853b92e` | `7dccee9a115cd7b056637fa3f70a208c3b35da9b5d8f0bfca4ae57d7fd86ec87` |
| `1007-n295-exact` | `n295/n295_exact.json` at `853b92e` | `9a0b4bc14803a43fb46e0370a3ad25faaa5a1f7f47186248455c90fae91b13a0` |
| `1007-n295-witness` | `n295/n295_witness.yaml` at `853b92e` | `412a6d526bda6bbde6d8edc10f0ef6df39d9bcca2aa58f83579923711490337e` |

#1005 states the first digest, which is the file’s; the issues state no other.
The two 292 files of #1006 are the same blobs at `853b92e`.

## Layout

- `programs/`: the review’s programs and the two controls plans.
- `frozen/`: the checker’s and plan’s digests at their freeze, the findings’ digest at
  their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane R1’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the sources, and reuses no
code of any earlier review.
The review of #1001 (lane L186) was the model; its text, its packet’s README and its
frozen digest lists were read, and its programs were not opened.
Each was run with CPython 3.14.7 (the project interpreter) as `python -I -B`, under
`nice -n 19`; the entry points put their own directory on the module path, since `-I`
leaves it off.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `r1_read.py` | the reading, in three forms: a Witness/v2 corners record as YAML (one block-style document without anchors, aliases, tags, directives, flow collections or duplicate keys, built from the parser’s events, every corner scalar read a second time line by line) or as JSON, and a centre file (`n`, `side`, `square_size`, the `format` sentence, `squares`); every scalar `p` or `p/q`; lowest terms recorded | a certificate | nothing (a module); it also holds the writers the controls use |
| `r1_axes.py` | method A: unit squares, wall clearances and pair margins by separating axes on the corners, each square over one integer denominator, in Python integers | rationals from the reader | nothing (a module) |
| `r1_area.py` | method B: unit squares (sides and diagonals), pairs and walls by the exact intersection, enumerated vertex by vertex and measured by its hull, containment by area, in `gmpy2.mpq` | points only | nothing (a module) |
| `r1_decide.py` | a packing by both methods, every square, wall and pair, and their agreement; a patched decision for a packing that differs in named squares | the reader’s values | nothing (a module) |
| `r1_check.py` | a certificate against its stated digest, and the claim’s 12-place arithmetic | a certificate, its digest, the claim | `out/check-*.json` |
| `r1_twin.py` | nothing about a bound: whether two files hold one packing, square by square as sets of four corners | two files | `out/twin-*.json` |
| `r1_frame.py` | nothing: the closed form by centres and half-extents, closing moves and wall moves, for the self-test and the controls | fractions | nothing (a module) |
| `r1_fmt.py` | nothing: exact and truncated prints, and the receipts’ JSON | fractions | nothing (a module) |
| `r1_selftest.py` | the readers, both methods, the closed form, the decision and the twin comparison against 24,389 checks with hand-derived answers, and 14 broken copies | nothing | `out/selftest.json` |
| `r1_controls.py` | the controls of a plan, by both methods or the reader | a certificate, its twin, the plan | `out/controls-*.json` |
| `r1_describe.py` | nothing: the tilts, the blocks of tilted squares, how each wall contact is made, the number forms | a certificate | `out/describe-*.json` |

`programs/controls-plan.json` is the plan, written and hashed before any program read a
certificate; its outcomes are rules over each certificate’s exact facts.
It states 51 controls; each report’s first file runs all of them and its twin the 34
the plan marks `on_twins`.

From `packing/` of this repository, with `PIN` a directory holding the three pinned
trees as `ozden-dec930b/`, `dewinter-796ff3b/` and `dewinter-853b92e/`, and `R` this
directory:

```bash
PY="nice -n 19 .venv/bin/python3 -I -B"
$PY $R/programs/r1_selftest.py $R/out/selftest.json
$PY $R/programs/r1_check.py $PIN/ozden-dec930b/n-292-candidate.yaml witness-yaml \
  90a0e30681821da567835ce1c9e81cf52aa899985587a953eafa0701b1829a8a 17.590104218682 \
  $R/out/check-1005-n292-yaml.json
$PY $R/programs/r1_check.py $PIN/ozden-dec930b/n292-witness.json witness-json - \
  17.590104218682 $R/out/check-1005-n292-json.json
$PY $R/programs/r1_check.py $PIN/dewinter-796ff3b/n292/n292_exact.json centre-json - \
  17.590016442847 $R/out/check-1006-n292-exact.json
$PY $R/programs/r1_check.py $PIN/dewinter-796ff3b/n292/n292_witness.yaml witness-yaml - \
  17.590016442847 $R/out/check-1006-n292-witness.json
# likewise 262 (16.699693441904) and 295 (17.699693441716) under dewinter-853b92e
$PY $R/programs/r1_twin.py $PIN/dewinter-853b92e/n262/n262_exact.json centre-json \
  $PIN/dewinter-853b92e/n262/n262_witness.yaml witness-yaml $R/out/twin-1007-n262.json
$PY $R/programs/r1_controls.py $R/programs/controls-plan.json 1007-n262-exact $PIN \
  $R/out/controls-1007-n262-exact.json
$PY $R/programs/r1_describe.py $PIN/dewinter-853b92e/n262/n262_exact.json centre-json \
  $R/out/describe-1007-n262-exact.json
```

## What They Printed

- `r1_selftest.py`: `PASSED 24389 checks 0 failed`; the 14 broken copies fail 1,636,
  357, 2,988, 1, 647, 2,234, 2,695, 2, 527, 527, 4,039, 1, 3 and 6 checks.
- `r1_check.py`: `ACCEPT` in all eight files, every pair apart by both methods (42,486,
  42,486, 34,191 and 43,365 pairs in the four packings), least margins
  $2.01869 \times 10^{-13}$, $3.03125 \times 10^{-12}$, $4.47681 \times 10^{-12}$ and
  $1.52004 \times 10^{-12}$; each claim the side’s 12-place ceiling.
- `r1_twin.py`: `SAME_PACKING` for each report’s two files.
- `r1_controls.py`: `EVERY_CONTROL_AS_STATED`, 51 of 51 on each first file and 34 of 34
  on each twin, 340 in all.
- `r1_describe.py`: the tilts, the blocks, the wall contacts and the number forms.

## After the Checker Was Frozen

Written after the checker and the plan were frozen at 03:46:57Z and before the findings
were frozen; none is in the checker’s digest list.

| Program | What it does | Reads | Writes |
| --- | --- | --- | --- |
| `r1_inner.py` | takes the 295 file’s squares that are not in its border (the squares within 1 of the two walls of the corner that leaves the least extent), as a packing in the box of their own larger extent, and hands it to the frozen `r1_decide.py`; compares those squares with the 262 file’s; with a directory, writes the derived packing in both forms | the 295 and 262 exact files | `out/inner-1007-n295.json` |
| `r1_tilts.py` | nothing: lists the tilts below and beyond 1° | a certificate | `out/tilts-*.json` |
| `r1_tables.py` | nothing: prints the review’s tables from the receipts | `out/` | standard output |

`programs/controls-plan-derived.json` is the frozen plan’s controls, unchanged, with the
derived packing’s two files as its subjects.

```bash
mkdir -p $D/n262-from-n295
$PY $R/programs/r1_inner.py $PIN/dewinter-853b92e/n295/n295_exact.json centre-json \
  $PIN/dewinter-853b92e/n262/n262_exact.json centre-json $R/out/inner-1007-n295.json \
  $D/n262-from-n295
$PY $R/programs/r1_check.py $D/n262-from-n295/derived_exact.json centre-json \
  bc4d9ce6589215d4549917c7465cef38738157c88f5a4d118c667420c4dd802d 16.699693441713 \
  $R/out/check-derived-n262-exact.json
$PY $R/programs/r1_check.py $D/n262-from-n295/derived_witness.yaml witness-yaml \
  af81ea01ada9520bca9d14497af53a806d93154106eb2b090d0f3a6036175767 16.699693441713 \
  $R/out/check-derived-n262-witness.json
$PY $R/programs/r1_twin.py $D/n262-from-n295/derived_exact.json centre-json \
  $D/n262-from-n295/derived_witness.yaml witness-yaml $R/out/twin-derived-n262.json
$PY $R/programs/r1_controls.py $R/programs/controls-plan-derived.json derived-n262-exact \
  $D $R/out/controls-derived-n262-exact.json
$PY $R/programs/r1_tilts.py $PIN/dewinter-796ff3b/n292/n292_exact.json centre-json \
  $R/out/tilts-1006-n292-exact.json
$PY $R/programs/r1_tables.py $R/out
```

They printed:

- `r1_inner.py`: `ACCEPT right-top inner 262`: the 295 file’s first 262 squares, as they
  stand, in the box of side $166996934417125687/10^{16}$, $1.90949 \times 10^{-10}$
  below the 262 file’s side.
  The derived files are not kept: `derived_exact.json` (29,076 bytes, SHA-256
  `bc4d9ce6…`) is the 295 file’s first 262 entries with `n` and the side changed, and
  `derived_witness.yaml` (116,619 bytes, `af81ea01…`) its corners.
- `r1_check.py` on both derived files: `ACCEPT`; `r1_twin.py`: `SAME_PACKING`;
  `r1_controls.py`: `EVERY_CONTROL_AS_STATED`, 51 of 51 and 34 of 34.
- `r1_tilts.py`: #1005 has 56 squares exactly upright, 172 turned by less than 1° (the
  largest by 0.39°) and 64 beyond; #1006 has 17, 216 (the largest by 0.049°) and 59;
  262 and 295 have 190 and 223 exactly upright and 72 beyond.
