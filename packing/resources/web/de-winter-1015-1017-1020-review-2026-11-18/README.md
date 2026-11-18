# Stage 4 Review of #1015, #1017 and #1020: Programs, Sources, Frozen Files and Receipts

This directory keeps the programs, the retained sources and the receipts of lane
r127-1118’s blind stage 4 review of three reports of 17 November 2026 by Joost de
Winter, each an upper bound on $s(127)$: issue
[#1015](https://github.com/jlevy/squares/issues/1015), issue
[#1017](https://github.com/jlevy/squares/issues/1017) and issue
[#1020](https://github.com/jlevy/squares/issues/1020). The review is
[`docs/project/reviews/review-2026-11-18-de-winter-1015-1017-1020.md`](../../../../docs/project/reviews/review-2026-11-18-de-winter-1015-1017-1020.md).

## Sources

The six certificate files of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing) at the
three commits the issues pin, fetched twice (a blobless Git fetch of each pin, and the
contents API at each pin) with equal bytes, and retained here byte for byte: the centre
files plain, the witness files as deterministic gzip
([Compressed Files](#compressed-files)). This review retains them so that its digest
lists check from this directory alone; the import lane retains its own copies.

| Report | Pin | File here | Git blob | SHA-256 of the bytes |
| --- | --- | --- | --- | --- |
| #1015 | `35b576a355297942bca9c195bee5cd74f0b27f40` | `source/i1015-35b576a/n127/n127_exact.json` | `369badb291372aa883340ff9b0460cf64086ae82` | `a4c9beb8b7b656072fa60150c70d2ea685907bc0e10e19e77963464c0f946772` |
| #1015 | the same | `source/i1015-35b576a/n127/n127_witness.yaml.gz` | `ec517cd53432ad4c0058f9f9ab9fbc375b100051` | `c1d4ee460abe4cbcd0479af32b0b28c4ad1793786120dc0111b892c2bfb65bb0` |
| #1017 | `cc20a26845789c2502950041c26709eda8a71081` | `source/i1017-cc20a26/n127/n127_exact.json` | `a9d633fcf6b3b166217802af9eef4d3c0c9b9563` | `bb883631dc01343198a07826d2a84faf029789b13beb88403478db736ac27c9b` |
| #1017 | the same | `source/i1017-cc20a26/n127/n127_witness.yaml.gz` | `b0fe7cbdeefcf79888d2f73fbf855f66594c282d` | `8245da32e92e9780a22a5cf9cd42911674e3be4d816c235fe42743f9a90a085d` |
| #1020 | `a1ba5019e787e407646293d7bef81d63c9951b32` | `source/i1020-a1ba501/n127/n127_exact.json` | `722628c9e12e5a7097db426e809aa25fa53eabc5` | `3a66f38276be9e986fc46fa1f859de54754ec77fc4694b3442de58381056a835` |
| #1020 | the same | `source/i1020-a1ba501/n127/n127_witness.yaml.gz` | `c5e0dec86b7caeb84980aafef1b5290641cb5ae2` | `19597239cdf162cbac5c12a6e60547ce0771f0b02078446517ad3e5d3dabb31e` |

The Git blobs and SHA-256 are of the uncompressed bytes; the blobs equal the pinned
trees’. The issues state no digest.
The authors’ `n127/SHA256SUMS` at `35b576a` lists the first two digests; at `cc20a26` it
is the same file, and at `a1ba501` it lists the two `cc20a26` digests (the review’s F9).
The author’s next commits, `67fb815` and `838c5ea`, pushed with `cc20a26` and `a1ba501`
respectively, update it to the digests of the files beside it, so it was stale only at
the intermediate commits the issues pin (the review’s addendum after review A).

T-305, the house at 127, is read from its retained copy in
[`../joegun-upper-bounds-2026-11-16/source/n-127-candidate.yaml`](../joegun-upper-bounds-2026-11-16/source/n-127-candidate.yaml)
(SHA-256 `9bde48b76afce9ab7d20d6d180650d0a6bbe46b7f106573f8155dfe9ed9d06f0`).

## Layout

- `source/`: the six retained certificate files.
- `programs/`: the review’s programs and its controls plan.
- `frozen/`: the checker freeze (`checker-frozen.txt`, `checker-frozen.sha256`), the
  findings freeze (`findings-frozen.txt`, `findings-frozen.sha256`) and the frozen
  review text.
- `out/`: the receipts of this review’s programs; `out/maintained/` the receipts of the
  repository’s maintained tools run as a second route.

## Programs

Every program is lane r127-1118’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the sources, and reuses no
code of any earlier review.
Each was run with CPython 3.14.7 (the project interpreter) as `python -I -B`, under
`nice -n 19`, at most two at a time; the entry points put their own directory on the
module path, since `-I` leaves it off.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `r127_read.py` | the reading: a centre file (exactly `n`, `side`, `square_size`, the `format` sentence, `squares`; no float, constant or duplicate key) or a Witness/v2 corners record as YAML (one block-style document without anchors, aliases, tags, directives, flow collections, block scalars or duplicate keys, built from the parser’s events, plain scalars resolved here, every corner scalar read a second time line by line); every scalar `p` or `p/q`; lowest terms recorded; a stored `X.gz` read decompressed | a certificate | nothing (a module); it also holds the writers the controls use |
| `r127_axes.py` | method A: unit squares, wall clearances and pair margins by separating axes on the corners, each square over one integer denominator, in Python integers | rationals from the reader | nothing (a module) |
| `r127_area.py` | method B: unit squares (sides, diagonals and shoelace), pairs and walls by the exact intersection, enumerated vertex by vertex and measured by its hull, containment by area, in `gmpy2.mpq` | points only | nothing (a module) |
| `r127_frame.py` | nothing by itself: the closed form by centres and directions, $M - T$ with one threshold $T$ on all four axes, for the controls, the contraction and control C0 | fractions | nothing (a module) |
| `r127_decide.py` | a packing by both methods, every square, wall and pair, and their agreement; a patched decision for a packing that differs in named squares or the side | the reader’s values | nothing (a module) |
| `r127_check.py` | a certificate by both methods, and the claim’s arithmetic (the claim against the side, its 12-place ceiling, and a stated exact fraction or decimal) | a certificate and its claim | `out/check-*.json` |
| `r127_twin.py` | nothing about a bound: whether two files hold one packing, square by square as sets of four corners | two files | `out/twin-*.json` |
| `r127_contract.py` | the uniform-contraction margin of each packing ($\lambda^* = \max T/M$, the contracted packing boxed at $L'$, decided by both methods, and $\lambda^* - 10^{-30}$ refused), and every report-order step’s gain against the predecessor’s margin | certificates in order | `out/contract.json` |
| `r127_identity.py` | nothing: the tilts of each packing, and each later packing against each earlier under the box’s eight symmetries, by nearest centres and an optimal assignment (binary64) | certificates in order | `out/identity.json`, `out/identity.txt` |
| `r127_controls.py` | the controls of the plan, by both methods or the reader; with `--checker always-accept` or `always-refuse`, which controls a constant checker fails | a certificate, its twin, the plan | `out/controls-*.json`, `out/controls-*.log` |
| `r127_synth.py` | nothing: synthetic packings for the self-test and for pricing | nothing | nothing (a module) |
| `r127_selftest.py` | the readers, both methods, the closed form, the decision, the twin comparison and the contraction against 10,486 checks with hand-derived answers | nothing | `out/selftest.json` |
| `r127_mutants.py` | that each of 18 broken copies of the programs fails the self-test, and the unmutated copy passes | the programs | `out/mutants.json` |
| `r127_bands.py` | nothing: the near pairs and near walls of each packing by method A, and the issues’ stated differences, exactly; written after the checker freeze | certificates | `out/bands.json` |
| `r127_compare.py` | nothing: this review’s contraction receipt against the maintained tool’s, exactly; written after the checker freeze | receipts | `out/compare-maintained.json` |

`programs/controls-plan.json` is the plan, written and hashed before any program read a
certificate; its outcomes are rules over each certificate’s exact facts.
Each report’s centre file runs every control and its witness file the ones the plan
marks for twins; the twin runs also carry S0 and S1b, which the plan lists for the first
files only (the review’s F12).

## Running It

From this directory, with the project interpreter:

```bash
PY="nice -n 19 ../../../.venv/bin/python3 -I -B"
T305=../joegun-upper-bounds-2026-11-16/source/n-127-candidate.yaml
$PY programs/r127_selftest.py --out out/selftest.json
$PY programs/r127_mutants.py --work "$(mktemp -d)" --out out/mutants.json
$PY programs/r127_check.py source/i1015-35b576a/n127/n127_exact.json --claim 11.800795682214 \
  --out out/check-1015-exact.json
$PY programs/r127_check.py source/i1017-cc20a26/n127/n127_exact.json --claim 11.800793726616 \
  --claim-exact 5900396863307571/500000000000000 --claim-decimal-exact 11.800793726615142 \
  --out out/check-1017-exact.json
$PY programs/r127_check.py source/i1020-a1ba501/n127/n127_exact.json --claim 11.800793726615 \
  --out out/check-1020-exact.json
$PY programs/r127_check.py $T305 --claim 11.801753890487 --out out/check-t305.json
# the same three checks on each n127_witness.yaml.gz, with out/check-NNNN-witness.json
for k in 1015:i1015-35b576a 1017:i1017-cc20a26 1020:i1020-a1ba501; do
  d=source/${k#*:}/n127
  $PY programs/r127_twin.py $d/n127_exact.json $d/n127_witness.yaml.gz --out out/twin-${k%%:*}.json
done
S="T-305=$T305 #1015=source/i1015-35b576a/n127/n127_exact.json"
S="$S #1017=source/i1017-cc20a26/n127/n127_exact.json #1020=source/i1020-a1ba501/n127/n127_exact.json"
$PY programs/r127_contract.py $S --out out/contract.json
$PY programs/r127_identity.py $S --out out/identity.json
$PY programs/r127_bands.py $S --out out/bands.json
# controls: each centre file (real, always-accept, always-refuse) and each witness file
$PY programs/r127_controls.py source/i1015-35b576a/n127/n127_exact.json --tier first \
  --twin source/i1015-35b576a/n127/n127_witness.yaml.gz --claim 11.800795682214 \
  --out out/controls-1015-exact.json
$PY programs/r127_controls.py source/i1015-35b576a/n127/n127_witness.yaml.gz --tier twin \
  --twin source/i1015-35b576a/n127/n127_exact.json --claim 11.800795682214 \
  --out out/controls-1015-witness.json
# likewise for 1017 (claim 11.800793726616) and 1020 (claim 11.800793726615), and with
# --checker always-accept and --checker always-refuse on each centre file
$PY programs/r127_compare.py --ours out/contract.json --identity out/identity.json \
  --maintained out/maintained --out out/compare-maintained.json
```

The maintained tools ran from `packing/`, as the brief allows, as a second route:

```bash
R=resources/web/de-winter-1015-1017-1020-review-2026-11-18
T305='T-305=packet:joegun-upper-bounds-2026-11-16'
C15="#1015=center-direction-json:$R/source/i1015-35b576a/n127/n127_exact.json"
C17="#1017=center-direction-json:$R/source/i1017-cc20a26/n127/n127_exact.json"
C20="#1020=center-direction-json:$R/source/i1020-a1ba501/n127/n127_exact.json"
.venv/bin/python3 -m devtools.contraction_margin --n 127 "$T305" --against "$C15" \
  --out $R/out/maintained/contraction-t305-1015.json   # and the five other steps
.venv/bin/python3 -m devtools.measure_identity --n 127 "$C20" "$T305" \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' "$C15" "$C17" \
  --out $R/out/maintained/identity-1020.json            # and #1015, #1017 likewise
```

## What They Printed

Each program printed one line a run (the receipts hold the rest):

| Receipt | What it says |
| --- | --- |
| `out/selftest.json` | `PASSED`: 10,486 checks, no failure |
| `out/mutants.json` | `ALL_MUTANTS_FAIL`: each of the 18 broken copies fails 1 to 2,483 checks; the unmutated copy passes |
| `out/check-1015-exact.json`, `out/check-1015-witness.json` | `ACCEPT`: 8,001 pairs apart, least $3.73044 \times 10^{-70}$ (31, 34); no wall touched; the claim the 12-place ceiling |
| `out/check-1017-exact.json`, `out/check-1017-witness.json` | `ACCEPT`: least $3.84839 \times 10^{-15}$ (35, 88); left 52 and bottom 43, 48, 54, 67 touched; the stated fraction and decimal equal the side; the title the ceiling |
| `out/check-1020-exact.json`, `out/check-1020-witness.json` | `ACCEPT`: least $1.64827 \times 10^{-59}$ (84, 99); no wall touched; the claim the ceiling |
| `out/check-t305.json` | `ACCEPT`: T-305 at its side, least $1.12027 \times 10^{-11}$ (50, 54) |
| `out/twin-1015.json`, `out/twin-1017.json`, `out/twin-1020.json` | `SAME_PACKING`: each witness lists the centre file’s corners from $c + (u + v)/2$ |
| `out/contract.json` | margins $1.20994 \times 10^{-10}$ (T-305), $7.73937 \times 10^{-63}$ (#1015), $4.19030 \times 10^{-14}$ (#1017), $1.82026 \times 10^{-58}$ (#1020); every step beats its predecessor’s, the least by 4.29 (#1017 to #1020) |
| `out/identity.json`, `out/identity.txt` | the tilts; no symmetry matches any report to T-305; each later report one to one with the earlier |
| `out/controls-1015-exact.json`, `out/controls-1017-exact.json` | `EVERY_CONTROL_AS_STATED`, 49 of 49 |
| `out/controls-1015-witness.json`, `out/controls-1017-witness.json` | 31 of 31 as stated; the verdict string `SOME_CONTROL_NOT_AS_STATED` because S0 and S1b ran outside the plan’s twin tier |
| `out/controls-1020-exact.json`, `out/controls-1020-witness.json` | 41 of 46 and 25 of 28: W1 had no subject at three walls, and W2p at the right and top crossed more than the nearest squares |
| `out/controls-*-exact-always-accept.json`, `-always-refuse.json` | `SOME_CONTROL_NOT_AS_STATED`: every must-refuse (always-accept) or must-accept (always-refuse) control that ran fails |
| `out/tables.json` | the controls tabulated against the plan: 226 of 234 as stated; the constant checkers’ statement holds in all six runs |
| `out/bands.json` | the near pairs and near walls, and the issues’ stated differences |
| `out/compare-maintained.json` | all six contraction steps equal the maintained tool’s, exactly |
| `out/maintained/contraction-*.json` | the maintained tool: the same margins and gains, none within the margin, both maintained routes accepting |
| `out/maintained/identity-*.json` | the maintained tool: the same moves; against T-174 farther still |

The `out/controls-*.log` files are the controls’ one-line prints.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/i1015-35b576a/n127/n127_witness.yaml.gz` | upstream | `ec517cd53432ad4c0058f9f9ab9fbc375b100051` | `c1d4ee460abe4cbcd0479af32b0b28c4ad1793786120dc0111b892c2bfb65bb0` |
| `source/i1017-cc20a26/n127/n127_witness.yaml.gz` | upstream | `b0fe7cbdeefcf79888d2f73fbf855f66594c282d` | `8245da32e92e9780a22a5cf9cd42911674e3be4d816c235fe42743f9a90a085d` |
| `source/i1020-a1ba501/n127/n127_witness.yaml.gz` | upstream | `c5e0dec86b7caeb84980aafef1b5290641cb5ae2` | `19597239cdf162cbac5c12a6e60547ce0771f0b02078446517ad3e5d3dabb31e` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
