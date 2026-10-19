# Reproducing the composites

Every composite is a deterministic function of two certificates in this repository, computed in
exact rational arithmetic by `tools/glue.py` (Lemma 3 of the note). Nothing is random and nothing
depends on the platform, so the files and their SHA-256 are reproducible bit for bit.

## All 230 at once

From the repository root, with any Python 3.8 or later:

```bash
sh composites/reproduce.sh                  # writes composites/regenerated/ (git-ignored)
sh composites/reproduce.sh /tmp/composites  # or anywhere else
```

The script runs the 230 `glue.py` commands of `table.csv` in table order, then checks that every
output has the SHA-256 listed in `table.csv` and that the 38 shipped files are byte-identical to
their rows. It takes well under a minute; it does not run the checkers (see below).

## One composite

Each row of `table.csv` names A (always `rectangles/<A>/<A>.cert`) and B (`B_path`). For example
the shipped `n050_j4_2454.cert`, 2454 = 50² − 50 + 4 squares in side < 50:

```bash
python3 tools/glue.py --rect rectangles/r17x16_n0257/r17x16_n0257.cert \
    --second composites/n034_j3_1125.cert --out n050.cert
python3 verify.py n050.cert --strict
python3 tools/verify_cert_daniel.py n050.cert
python3 tools/rectcheck.py n050.cert
```

`glue.py` puts the input file names into the certificate's `#` comment line, so the hash matches
`table.csv` only when the inputs have the basenames used there; the squares do not depend on it.

Level-2 rows (B = `composites/nNNN_jJ_COUNT.cert`) need the shipped level-1 composite for that n,
which is itself the output of a level-1 row. To rebuild without the shipped files, regenerate the
level-1 rows, save the ones marked shipped under their `nNNN_jJ_COUNT.cert` names, then run the
level-2 rows; `reproduce.sh` instead reads the shipped files and checks them against their
level-1 rows.

## Inputs that exist only for the composites

`composites/inputs/` holds the two B pieces that are not elsewhere in the repository:

- `one-square.cert`: a single unit square in a square of side 3/2, used as the 2 × 2 box in the
  level-1 rows with j = 0. Trivial; included so that every row reproduces.
- `n0463-superseded.cert`: our earlier certificate for n = 463 (side 21.996141230021…, grown from the
  n = 421 packing), replaced in `n0463/` by the parametric one (side 21.986880…) after the
  composites were computed. The 145 level-1 composites were generated with it, and the shipped
  composites for n = 42, 43 and, through them, 62, 63, 64 contain it. It is a valid certificate
  in its own right (it passes all three checkers, see VERIFICATION.md).

## Composites from de Winter's n = 211 packing

Gluing the 17 × 16 rectangle onto de Winter's 211 = 15² − 15 + 1 gives 932 = 31² − 31 + 2, and
twice more gives 2165 = 47² − 47 + 3 and 3910 = 63² − 63 + 4. They are not in the table and not
shipped, because the 211 packing has no licence. To build them:

```bash
sh third_party/fetch_unlicensed.sh
R=rectangles/r17x16_n0257/r17x16_n0257.cert
python3 tools/glue.py --rect $R --second third_party/unlicensed/n-211.cert --out n031_from_211.cert
python3 tools/glue.py --rect $R --second n031_from_211.cert --out n047_from_211.cert
python3 tools/glue.py --rect $R --second n047_from_211.cert --out n063_from_211.cert
```

These match the research repository's files (identical after the comment line); check them with
the three checkers as above.

## How the 230 came about

Level 1 glued each of the five rectangles with every B available on 2026-10-10: Daniel's exact
certificates for n = 5, …, 273 (plus the single square), our squares n = 308, 343, 344, 380, 381,
421 and the then-current 463, and the five rectangles themselves; 5 × 29 = 145 composites. Level 2
glued each rectangle onto the best level-1 composite for n = 27, …, 43 (5 × 17 = 85). Rows where
Lemma 3's hypotheses fail do not occur. The research repository's `squarepack.glue` produced them;
`tools/glue.py` is a standalone rewrite that gives the same squares and side on all 230 (checked by
regenerating every one and comparing with comment lines dropped). The only difference from
`squarepack.glue` is that `glue.py` takes d = min(d_A, d_B, 1/2) as in the note, where
`squarepack.glue` takes min(d_A, d_B); these agree whenever d_A ≤ 1/2, which holds for every
rectangle here (d_A < 0.012).
