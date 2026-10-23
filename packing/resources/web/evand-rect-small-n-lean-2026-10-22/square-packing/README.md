# square-packing

How small a square can hold *n* unit squares?  That side, `s(n)`, is known exactly for only a
handful of *n*.  This repository holds exact, machine-checked results on `s(n)`, the tools that
produce and check them, and the **Square Packing Atlas**, an explorer for the record packings:
**https://evand.github.io/square-packing/**

[![verify](https://github.com/evand/square-packing/actions/workflows/verify.yml/badge.svg)](https://github.com/evand/square-packing/actions/workflows/verify.yml)
spot-checks each push (hashes, the point certificates, every bundle's shipped run records, a small Lean target).  The real checks run locally:
`./verify.sh` (fresh sweeps and rejection suites, ~4 min on 16 cores), `./verify.sh --full` (slow sweeps), `cd lean && lake build` (some modules need > 16 GB).

## Results

Each result is a certificate file, an exact checker you can re-run, a write-up, and (where noted) a Lean theorem.
Status, caveats and independent checks are in each bundle's README; nothing here has been peer reviewed.

| Result | Certificate bundle | Re-check | Write-up | Lean |
|---|---|---|---|---|
| **s(k² − 3) = k** for every k ≥ 6 | [`certificates/k2m3/`](certificates/k2m3/) | `certificates/k2m3/verify.sh [--full]` | [/k2m3/](https://evand.github.io/square-packing/k2m3/) | **in the kernel with no hypothesis** (`valid7`, `bentz`; wand125's PR #6, merged 10-10; root modules built by wand125, not rebuilt here: `tasks/pr6-valid7-kernel/`); all-k reduction `bentz_of_validTilt7` |
| **s(k² − 4) = k** for every k ≥ 5 | [`certificates/k2m4/`](certificates/k2m4/) | `certificates/k2m4/verify.sh [--full]` | [/k2m4/](https://evand.github.io/square-packing/k2m4/) | all-k reduction `bentz4_of_validTilt9`, conditional on the tilted box statement (re-checked by wand125's separate exact checker, 10-06; not yet register-verified) |
| **s(60) = s(61) = 8** | [`certificates/s60/`](certificates/s60/) | `certificates/s60/verify.sh [--full]` | [/s60/](https://evand.github.io/square-packing/s60/) | — |
| **s(45) = 7** | [`certificates/s45/`](certificates/s45/) | `certificates/s45/verify.sh [--full]` | [/s45/](https://evand.github.io/square-packing/s45/) | — |
| **s(32) = 6** | [`certificates/s32/`](certificates/s32/) | `certificates/s32/verify.sh [--full]` | [/s32/](https://evand.github.io/square-packing/s32/) | `s32_eq_6`, no hypothesis (opt-in build) |
| **s(21) = 5** | [`certificates/s21/`](certificates/s21/) | `certificates/s21/verify.sh [--full]` | [/s21/](https://evand.github.io/square-packing/s21/) | `s21_eq_five_of_checker`, conditional |
| **s(13) = 4**, case-free | [`certificates/rung2/`](certificates/rung2/) | `./verify.sh` | [/s13/](https://evand.github.io/square-packing/s13/) | `s13_eq_4`, no hypothesis (opt-in build) |
| **s(12) ≥ 15680/3951** = 3.9686 (squarepacker's 3.9715 re-weights these points) | [`certificates/`](certificates/) `s12_lower_3.9686.txt` | `./verify.sh` | [/s12/](https://evand.github.io/square-packing/s12/) | `s12_ge_15680_3951`, no hypothesis (opt-in build) |
| s(11) ≥ 3040/797 (superseded: s(11) = 3.877… is now proved) | [`certificates/`](certificates/) `s11_lower_3.8143.txt` | `./verify.sh` | [/s12/](https://evand.github.io/square-packing/s12/) | `s11_ge_3040_797`, no hypothesis (opt-in build) |
| **s(n² − n + 1) < n** for every n ≥ 15 (Kevin Fang, jlevy#603) | [`certificates/fang-gluing/`](certificates/fang-gluing/) | `certificates/k2-minus-c/verify.sh --fang` | [/k2c/](https://evand.github.io/square-packing/k2c/) | `FangFinal.theorem1/2`, no hypothesis (opt-in build) |
| **c*(k) ≤ 4⌈√(2k − 7)⌉ − 1** (k ≥ 7) and **c*(k) < 18.9 k^{2/5} + 35.7 k^{1/5} + 122** (k ≥ 3·10⁵); Ryu's 8⌈√(k − 4)⌉ − 1 and his Theorem 1.2 (k ≥ 8·10⁶) | [`certificates/k2-minus-c/`](certificates/k2-minus-c/) | `certificates/k2-minus-c/verify.sh` | [/k2c/](https://evand.github.io/square-packing/k2c/) | `RyuLayers`, `RyuStairBound`, `RyuBound`; no hypothesis |
| **R₃ exactly**: three unit squares (any angles) fit in w × h iff both sides ≥ 1 and (both ≥ 2, or one ≥ 3, or ℓ + 2s ≥ 4 + 2√2 with short side s < 2: the 45° wedge). The boundary and its constructions, wedge included, are from Erich Friedman's [Math Magic, June 2010](https://erich-friedman.github.io/mathmagic/0610.html) (boundary of S₂; solvers of that problem: Morandi, Stenlund, Cantrell, Hosono); new here is the proof, the first we know of (Yang 2026 leaves part of the region open) | — | `cd lean && lake build Sqpack.Rect3` | [`search/rectfront/RECTFRONT.md`](search/rectfront/RECTFRONT.md) | `rect3_iff`, no hypothesis (also `rect2_iff`, R₂) |
| **R₄ exactly**: four unit squares (any angles) fit in w × h iff both sides ≥ 1 and (both ≥ 2, or one ≥ 4, or, with short side s < 2, ℓ ≥ L(t, s) = 2 + (1 − 2(s − k − 1) sin t)/cos t + (1 − (s − 2k) cos t)/sin t, k = (cos t + sin t)/2, for some t: two uprights in opposite corners and a tilted pair between them). The boundary and its constructions are from Erich Friedman's [Math Magic, June 2010](https://erich-friedman.github.io/mathmagic/0610.html) (boundary of S₃; its tilted piece credited there to MM, i.e. Maurizio Morandi; closed form also in wand125's `problems/rectangles` k = 4); new here is the proof (chain of shelves; the separating line of the middle pair gives t) | — | `cd lean && lake build Sqpack.Rect4` | [`search/rectfront/RECTFRONT.md`](search/rectfront/RECTFRONT.md) | `rect4_iff`, no hypothesis |
| **R₅ exactly**: five unit squares (any angles) fit in w × h iff both sides ≥ 1 and (one side ≥ 5; or both ≥ 2 and (one ≥ 3 or w + h ≥ 4 + √2, the stretched s(5) packing, so s(5) = 2 + 1/√2, Göbel 1979); or, with short side s < 2, ℓ + 4s ≥ 4 + 6√2: the 45° zigzag). The boundary and its constructions are from Erich Friedman's [Math Magic, June 2010](https://erich-friedman.github.io/mathmagic/0610.html) (pieces 4.1–4.5 of S₄, all credited there to MM, i.e. Maurizio Morandi; closed forms also in wand125's `problems/rectangles` k = 5); new here is the proof: weighted point covers for both sides ≥ 2 (incl. a 10-point 2/3–1/3 cover), four midline points for strips of height < 2√2 − 1, and the chain plus ~14k lines of generated polynomial certificates (Handelman + an exact zigzag decomposition) for 2√2 − 1 ≤ s < 2 | — | `cd lean && lake build Sqpack.Rect5Thm` (~5 min wall on 16 cores, ~70 CPU-min) | [`search/rectfront/RECTFRONT.md`](search/rectfront/RECTFRONT.md), [`r5strip/FINAL5.md`](search/rectfront/r5strip/FINAL5.md), [`r5pts/R5PTS.md`](search/rectfront/r5pts/R5PTS.md) | `rect5_iff`, no hypothesis |
| **Exact forms** of the record packings, n ≤ 324 (S* as an algebraic number; Lean `Packs n S*`; local minimality) | [`search/exact/`](search/exact/) | `search/exact/batch/verify_all.sh` | [`EXACT_FORMS.md`](search/exact/EXACT_FORMS.md) | `lean/Sqpack/Exact/` |
| New record packings: s(266), s(270), s(272) upper bounds | [`search/exact/results/sw2/`](search/exact/results/sw2/) | `search/exact/verify_cert.py` | — | — |
| Packings beating the 2×2 doublings of the s(241), s(273), s(307) records: s(964) ≤ 31.8595, s(1092) ≤ 33.8406, s(1228) ≤ 35.8474 (evidence for "tilings are never optimal") | [`search/tilings/`](search/tilings/) | `search/exact/verify_cert.py`, `verify_cert2.py` | [`search/TILINGS.md`](search/TILINGS.md) | conjecture stated: `Conjectures.TilingsNeverOptimal` |

The certificate format is [`certificates/FORMAT.md`](certificates/FORMAT.md); [`VERIFICATION.md`](VERIFICATION.md) logs
what has been verified, when, and how.  [`RESEARCH.md`](RESEARCH.md) is the long account of the s(11)/s(12)/s(13)
method, its limits, and how to reproduce (not just check) a certificate.

## Layout

| | |
|---|---|
| `certificates/` | one bundle per result (cover, run records, `SHA256SUMS`, `verify.sh`, README) |
| `verify/` | exact Rust verifier for weighted point certificates (`verify`) |
| `verify2/` | zero-margin checkers: `zmcheck` (points) and `zmx2` (mixed covers: points, segments, area) |
| `xcheck.py`, `search/zeromargin.py`, `search/zm_mixed.py` | independent Python re-checks |
| `verify.sh`, `tests/` | the whole re-check (CI runs it) and the rejection suites (mutated certificates must fail) |
| `lean/` | Lean 4 + Mathlib: `lake build`; `lean/Axioms.lean` prints each headline's axioms; `lean/LADDER.md` |
| `docs/` | the HTML write-ups served on the site |
| `site/` | the Square Packing Atlas (build: `site/build.sh`) |
| `search/` | research code and logs: one `UPPERCASE.md` log per investigation next to its scripts; `search/packer/` is the packing search engine, `search/exact/` the exact-forms pipeline |
| `notes/`, `tasks/` | working notes and per-task material (history; not curated) |
| `TODO.md`, `Completed.md` | the open research list and what's done |

Exit status of `verify` and `zmcheck`: 0 VERIFIED, 1 NOT VERIFIED, 2 malformed input, 4 partial run (no verdict).

## Data, licence, credits

The code is MIT-licensed (`LICENSE`).  The packings drawn on the site are David Ellsworth's
(https://kingbird.myphotos.cc/packing/squares_in_squares.html, continuing Erich Friedman's
survey).  `site/www/data/` is derived from his SVGs and quotes his attribution text; that
material is his and is not covered by the MIT licence.  Full credits are on the site's Sources
page (`site/www/sources.html`) and in [`CREDITS.md`](CREDITS.md), including the 2026 work this builds on or runs beside:
Burns, Massaccesi, Fort, Mira, jlevy (Squares Project), Kleddamag, Guzhou0806, tokoharu, wand125, chelokot,
Queuingtheorydotcom, Couzo, itsnaka and squarepacker.

Until 2026-10-07 everything except `site/` lived under `s12/`; old links `…/s12/X` are now `…/X`.
