# squarepack-certs

Exact certificates, checkers and the gluing program behind the note *Packing n² − n + 1 unit
squares in a square of side less than n, for every n ≥ 15* (Kevin Fang, draft v0.9,
2026-10-18, https://doi.org/10.5281/zenodo.23463481; text in `note/fang-2026-n2-n-1.md`). Lean 4 formalisation of Theorem 1 and the unmixed bounds of Theorem 2:
https://github.com/TheSnakeFang/squarepack-lean. Every packing the proof uses is here as a rational certificate, or, for the one
piece without a licence, fetched by a script from a pinned commit and checked by hash. Three
independently written exact checkers run on every certificate; `VERIFICATION.md` has the outcome.

Write s(n) for the side of the smallest square containing n unit squares with pairwise disjoint
interiors. The note proves:

**Theorem 1.** $s(n^2 - n + 1) < n$ for every integer $n \ge 15$.

**Theorem 2.** Let $n \ge 15$ and let $p, q \ge 0$ be integers with $16p + 21q \le n - 15$. Then $n^2 - n + 1 + p + 2q$ unit squares pack in a square of side less than $n$. In particular $s(n^2 - n + F(n)) < n$ with $F(n) = 1 + \max\{p + 2q : 16p + 21q \le n - 15\}$.

The proof glues a squeezable 17 × 16 rectangle R onto a square packing (Lemma 3 of the note) and
inducts on n in steps of 16, starting from finitely many certificates. Where each one lives:

| ingredient in the note | file(s) |
|---|---|
| R: 257 squares in (17 − δ) × (16 − δ), δ ≥ 7.436 · 10⁻⁴ (Proposition 4) | `rectangles/r17x16_n0257/` |
| n = 15: de Winter's 211 squares in side < 15 | not copied; `third_party/fetch_unlicensed.sh` |
| n = 16, 17: 241 and 273 squares (Arslanov, Mustafin, Shangitbayev; Ellsworth, Stead) | `third_party/daniel/n-241.cert`, `n-273.cert` |
| n = 18: 307 squares in side < 18 | implied by `n0308/` (308 squares in side < 18) |
| n = 19, …, 26: n² − n + 1 squares in side < n (Section 3) | `n0343/`, `n0381/`, `n0421/`, `n0463/`, `n0507/`, `n0553/`, `n0601/`, `n0651/` |
| m² − m squares in side < m for m = 11, …, 15 (Proposition 5) | `third_party/daniel/n-110.cert`, `n-132`, `n-156`, `n-182`, `n-210` |
| the four further rectangles with waste b − 1 (Section 4) | `rectangles/r18x17_n0290/`, `r19x18_n0325/`, `r21x20_n0401/`, `r22x21_n0442/` |
| the 22 × 21 rectangle with waste b − 2 = 19 (443 squares, d ≥ 0.0094; added 2026-10-13) | `rectangles/r22x21_n0443/` |
| the 230 composites of Section 5, best j for 27 ≤ n ≤ 64 | `composites/` |
| the theorem inventory: for every 15 ≤ n ≤ 64 the certificate of n² − n + F(n) squares in side n − 1/20000 built by the proof (uniform squeeze 1/10000), plus 26 best-excess certificates | `theorem/` (see `theorem/README.md`) |

## Direct square packings

| folder | n | form | S, rounded up (exact value in the certificate) |
|---|---|---|---|
| `n0308/` | 308 | 18² − 18 + 2 | 17.999309855162748 |
| `n0343/` | 343 | 19² − 19 + 1 | 18.994903529220497 |
| `n0344/` | 344 | 19² − 19 + 2 | 18.995489275430816 |
| `n0380/` | 380 | 20² − 20 | 19.976775433974195 |
| `n0381/` | 381 | 20² − 20 + 1 | 19.976969740405508 |
| `n0421/` | 421 | 21² − 21 + 1 | 20.986150316947159 |
| `n0463/` | 463 | 22² − 22 + 1 | 21.986880406196935 |
| `n0507/` | 507 | 23² − 23 + 1 | 22.997807183348823 |
| `n0553/` | 553 | 24² − 24 + 1 | 23.998811020144984 |
| `n0601/` | 601 | 25² − 25 + 1 | 24.998914572427130 |
| `n0651/` | 651 | 26² − 26 + 1 | 25.991547815274380 |
| `n0382/` | 382 | 20² − 20 + 2 | 19.989479729399675 |
| `n0422/` | 422 | 21² − 21 + 2 | 20.988436524095744 |
| `n0464/` | 464 | 22² − 22 + 2 | 21.991709536768996 |
| `n0508/` | 508 | 23² − 23 + 2 | 22.994733849702143 |
| `n0758/` | 758 | 28² − 28 + 2 | 27.996346242823117 |
| `n0814/` | 814 | 29² − 29 + 2 | 28.999873603982716 |

308, 343 and 344 were published here on 2026-10-09 and submitted to the Squares Project
(jlevy/squares#484), whose exact implementations confirmed them; Evan Daniel has since improved
all three by local search from them (`third_party/daniel/hunt3_n*.cert`, jlevy/squares#489).

## Layout

```
README.md, ATTRIBUTION.md, CHANGELOG.md, VERIFICATION.md, LICENSE, MANIFEST.sha256
verify.py                     exact checker for square certificates (stdlib only)
tools/
  rectcheck.py                exact checker for square and rectangle certificates (stdlib only)
  verify_cert_daniel.py       Evan Daniel's exact checker, unchanged (MIT, NOTICE-verify_cert_daniel)
  glue.py                     Lemma 3 of the note in exact arithmetic (stdlib only)
theorem/                      theorem inventory n = 15..64 (README.md, inventory.tsv, best.tsv, PIECES.md, best/)
nNNNN/                        one direct square packing per folder:
  nNNNN.cert                  certificate, Daniel's text format
  nNNNN.cert.json             the same, SQUISH json
  nNNNN.txt                   David Ellsworth's centre-origin decimal format, 40 digits
  nNNNN.svg                   drawing (blue: tilted by 1 degree or more)
  verify_output.txt           squarepack.verify --strict (research repo; same code as verify.py)
  check_packing_output.txt    Ellsworth's check_packing.py on nNNNN.txt
  NOTES.md, SHA256SUMS        seed and date; hashes of the folder
rectangles/rAxB_nNNNN/        one squeezable rectangle per folder: .cert (header n W H), .cert.json
                              (W, H keys), .svg, verify_output.txt, rectcheck_output.txt,
                              NOTES.md (box, count, waste, exact squeeze d), SHA256SUMS
composites/
  nNNN_jJ_COUNT.cert          38 composites: the largest j for each n, 27 <= n <= 64
  TABLE.md, table.csv         all 230 composites: n, count, j, side, A, B, sha256, shipped or not
  REPRODUCE.md, reproduce.sh  how to regenerate all 230 and check their hashes
  inputs/                     two B pieces used only by the composites
third_party/
  daniel/                     Daniel's certificates used as B pieces, plus hunt3_n308/343/344,
                              LICENSE (MIT) and NOTICE
  SOURCES.md                  pinned URL and SHA-256 of every third-party file
  fetch_unlicensed.sh         downloads de Winter's 211 and Daniel's n-211.cert, checks SHA-256
```

The folders `n0308/`, `n0343/`, `n0344/` are as published on 2026-10-09 and are never edited; a
new packing for an n already here would go in a new dated folder `nNNNN-YYYY-MM-DD/`.

## Certificates

A certificate is a text file: line 1 `n S` for a square container (`n W H` for a rectangle),
then one line `x y t` per unit square, all exact rationals: centre (x, y), rotation θ with
t = tan(θ/2), so cos θ = (1 − t²)/(1 + t²) and sin θ = 2t/(1 + t²) are rational. Lines starting
with `#` are comments. A certificate is valid when every square lies in the open box (all wall
margins > 0) and every pair of squares is strictly separated along one of the four edge normals
of the two squares (pairs with centres more than √2 apart are disjoint anyway). That is the strict
convention of Daniel's checker; every certificate here meets it.

## Checking

Three exact programs, written separately, all Python 3.8+ with the standard library only:

| checker | reads | checks |
|---|---|---|
| `verify.py` | square certificates (text or json) | walls and close pairs by separating axes; `--strict` for positive margins |
| `tools/verify_cert_daniel.py` | square certificates | the same test, strict; on a rectangle it reads only `n W` and checks the W × W square |
| `tools/rectcheck.py` | square and rectangle certificates | all four walls against W and H, pairs by separating axes, strict |

They share the method (rational half-angle representation, separating axes) but not code. To run
all of them on everything (seconds for the small files; the 38 composites take about an hour per
checker):

```bash
for f in n0*/n0*.cert third_party/daniel/*.cert composites/inputs/*.cert composites/n0*.cert; do
  python3 verify.py "$f" --strict >/dev/null && python3 tools/verify_cert_daniel.py "$f" >/dev/null \
    && python3 tools/rectcheck.py "$f" >/dev/null && echo "ok   $f" || echo "FAIL $f"
done
for f in rectangles/*/*.cert; do python3 tools/rectcheck.py "$f" | tail -1; done
shasum -a 256 -c MANIFEST.sha256 --quiet && echo "manifest ok"
```

Single files: `python3 verify.py n0381/n0381.cert --strict` (exit 0 iff valid),
`python3 tools/verify_cert_daniel.py n0381/n0381.cert`, `python3 tools/rectcheck.py
rectangles/r17x16_n0257/r17x16_n0257.cert`. The square folders also carry the output of
Ellsworth's decimal checker (https://github.com/Davidebyzero/packing_squares_in_squares__tools,
`check_packing.py`) on the 40-digit `.txt` file.

## Reproducing

- Composites: `sh composites/reproduce.sh` regenerates all 230 with `tools/glue.py` from the files
  here and checks every SHA-256 against `composites/table.csv`. Details and single-file commands in
  `composites/REPRODUCE.md`. A composite is `python3 tools/glue.py --rect A.cert --second B.cert
  --out C.cert`: A in the top-left corner, two integer blocks, B in the bottom-right corner, all
  squeezed by d = min(d_A, d_B, 1/2), then scaled by 1 + 2⁻⁶⁴ so every margin is positive.
- n = 15 base case: `sh third_party/fetch_unlicensed.sh`, then `python3 verify.py
  third_party/unlicensed/n-211.cert --strict`.
- Direct packings and rectangles: found by a time-budgeted penalty search from two-wedge seeds
  (Section 6 of the note); the search is not bit-reproducible, which is why the certificates are
  shipped and checked on their own. Seeds and dates are in each folder's `NOTES.md`.

## Licences

- Code (`verify.py`, `tools/glue.py`, `tools/rectcheck.py`, the shell scripts): MIT, see `LICENSE`.
- Our certificates, text files, tables and drawings (`nNNNN/`, `rectangles/`, `composites/`): CC0 1.0.
- `third_party/daniel/` and `tools/verify_cert_daniel.py`: Evan Daniel's, MIT, unchanged; licence
  and notice in `third_party/daniel/` and `tools/NOTICE-verify_cert_daniel`.
- De Winter's n = 211 packing and Daniel's certificate of it: no licence, not copied; fetched by
  `third_party/fetch_unlicensed.sh` from pinned commits and checked by hash.

Credit for the construction, seeds, format and checkers: `ATTRIBUTION.md`.

Search, verifier and this bundle were written and run with Claude (Anthropic) as a coding and research agent, directed and reviewed by Kevin Fang.
