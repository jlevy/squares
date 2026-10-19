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
