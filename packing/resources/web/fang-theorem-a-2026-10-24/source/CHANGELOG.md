# Changelog

## 2026-10-24 (v0.2 of the Theorem A note)

`theorem-a/note/` is v0.2 (https://doi.org/10.5281/zenodo.23624565). It credits Evan Daniel's earlier proof of c*(k) ≤ 4⌈√(2k − 7)⌉ − 1, which we had missed. It also drops the v0.1 claim that Theorem A was the smallest explicit bound known. README.md, theorem-a/README.md and ATTRIBUTION.md say the same. Code and certificates unchanged.

## 2026-10-24 (later)

The Theorem A note is on Zenodo, https://doi.org/10.5281/zenodo.23624412. `theorem-a/note/` now has the version with the DOI and the bundle commit b1b3f6b in the front matter, the same text as the Zenodo files. The DOI is also in the README files.

## 2026-10-24

`theorem-a/`: code, certificates and note for Theorem A (c*(k) < 4√(2k) + 1 for every k ≥ 6).
- `lband.py`: the construction in exact rationals, stdlib only.
- `windowed_check.py`: both exact checkers, unchanged, on overlapping windows.
- 36 strict certificates (k = 6..40 and 101), plus hashes and `regenerate.sh` for k = 300 and 600.
- The note as PDF and LaTeX.

No existing file changed apart from README.md, ATTRIBUTION.md, VERIFICATION.md and this file.

## 2026-10-12

Bundle for the note "Packing n² − n + 1 unit squares in a square of side less than n, for every
n ≥ 15" (draft v0.3).

- Eight more direct square packings: n = 380, 381, 421, 463, 507, 553, 601, 651 (`nNNNN/`), in the
  same layout as the 2026-10-09 folders.
- Five squeezable rectangles, 17 × 16 / 257, 18 × 17 / 290, 19 × 18 / 325, 21 × 20 / 401,
  22 × 21 / 442 (`rectangles/`).
- Composites (`composites/`): the largest-j composite for each n with 27 ≤ n ≤ 64 (38 files), the
  table of all 230 composites with hashes, and `reproduce.sh`, which regenerates all 230.
- Evan Daniel's certificates used as B pieces and his n = 308, 343, 344 improvements, pinned to
  commits and hashed (`third_party/daniel/`, `third_party/SOURCES.md`); de Winter's n = 211 is
  fetched by `third_party/fetch_unlicensed.sh`, not copied.
- Tools: `tools/glue.py` (Lemma 3, standalone), `tools/rectcheck.py`, `tools/verify_cert_daniel.py`.
- `VERIFICATION.md` (three checkers on every certificate), `MANIFEST.sha256`, rewritten README and
  ATTRIBUTION. `verify.py` and the folders `n0308/`, `n0343/`, `n0344/` are unchanged.

## 2026-10-09

Certificates for s(308) < 18, s(343) < 19 and s(344) < 19 (`n0308/`, `n0343/`, `n0344/`), with the
standalone exact verifier `verify.py`. Submitted to the Squares Project as jlevy/squares#484.

## 2026-10-13

- Added six direct packings of n² − n + 2 squares below side n: `n0382/` (seeded from Evan Daniel's improved 343), `n0422/`, `n0464/`, `n0508/`, `n0758/`, `n0814/` (parametric seeds).
- Added `rectangles/r22x21_n0443/`: 443 squares strictly inside (22 − d) × (21 − d), d ≥ 0.0094, waste 19 = b − 2. With Lemma 3 this gives the step j(n) ≥ j(n − 21) + 2.
- Every new file passes verify.py (strict), tools/rectcheck.py and Daniel's verify_cert.py (width only for the rectangle); see VERIFICATION.md.

## 2026-10-13 (second entry)

- Added `theorem/`: for every n = 15..64 the certificate of n² − n + F(n) squares in side n − 1/20000 built by the proof of Theorem 2 (uniform squeeze d0 = 1/10000 at every gluing step, one strictification at the end), with `inventory.tsv`, `PIECES.md` (every input piece, squeeze, hash, provenance) and 26 best-excess certificates (`best/`, `best.tsv`).
- `tools/glue.py` gained `--d` (use a given common squeeze instead of min(d_A, d_B, 1/2)).
- All 76 new certificates pass `verify.py --strict` / `squarepack.verify --strict`, `tools/rectcheck.py` and Daniel's `verify_cert.py`; see VERIFICATION.md.

