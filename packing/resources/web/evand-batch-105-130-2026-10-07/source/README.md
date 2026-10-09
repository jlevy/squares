# square-packing

How small a square can hold *n* unit squares?  That side, `s(n)`, is known exactly for only a
handful of *n*.  This repository has two parts:

| | |
|---|---|
| [`site/`](site/) | **Square Packing Atlas**, an explorer for the record packings in David Ellsworth's catalogue: every packing drawn and analysed (angles, contacts, free squares, gaps, symmetry, rigidity), how the records changed over time, the proven lower bounds, and how the exact results are proved.  **https://evand.github.io/square-packing/** |
| [`s12/certificates/k2m3/`](s12/certificates/k2m3/) | **s(k² − 3) = k for every k ≥ 6**: one fixed-profile family of measures (corner modules, a periodic wall band, area density inside; total `k² − 3.389` for every k), whose 7 × 7 box is certified at margin zero by a single exact checker (`qx2_zm.py`; a second implementation, `zmx2` with area density, is in progress and not yet complete); the reduction from that box to every k is kernel-checked in Lean, conditional on that box's covering statement (`bentz_of_valid7 : Valid7 → …`).  The bundle's default `verify.sh` re-checks hashes, totals, structure and the run record's coverage, and re-runs the exact θ = 0 check, but does not recompute the positive-tilt leaves' mass bounds; `verify.sh --full` re-runs the checker (~81,000 CPU-s).  With k = 3 (Kearney–Shiu 2002), 4 (Bentz 2010; also our s(13) = 4) and 5 (Bentz's 2016 preprint; also our s(21) = 5) this settles the statement Bentz suggested for all k ≥ 3.  Working in public: a single-implementation exact certificate, adversarially reviewed by six independent agents with no errors found; the all-k reduction is kernel-checked in Lean. Not yet independently re-implemented, externally reviewed, or fully formalised.  Write-up: **https://evand.github.io/square-packing/k2m3/** |
| [`s12/certificates/s60/`](s12/certificates/s60/) | **s(60) = 8**: a mixed cover of `[0,8]²` (weighted points plus mass spread uniformly along the grid lines) of total `59.8587 < 60`, certified at margin zero by the same two separately written exact checkers as s(21) = 5 and s(45) = 7 (its default `verify.sh` includes a fresh run of the Rust one), hence also **s(61) = 8** (s is monotone; wand125's point-only cover, replayed here, is a second route); not in Lean yet.  Write-up: **https://evand.github.io/square-packing/s60/** |
| [`s12/certificates/s45/`](s12/certificates/s45/) | **s(45) = 7**: a mixed cover of `[0,7]²` (weighted points plus mass spread uniformly along the grid lines) of total `44.7735 < 45`, certified at margin zero by the same two separately written exact checkers as s(21) = 5; not in Lean yet.  Write-up: **https://evand.github.io/square-packing/s45/** |
| [`s12/certificates/s21/`](s12/certificates/s21/) | **s(21) = 5**: a mixed cover of `[0,5]²` (weighted points plus mass spread uniformly along the grid lines) of total `20.8947 < 21`, certified at margin zero by two separately written exact checkers (no shared code, but a shared point-test lineage: `s12/certificates/s21/README.md`), with a Lean 4 top theorem conditional on that computational hypothesis (the checkers' covering statement; segments are not yet in the kernel verifier).  Write-up: **https://evand.github.io/square-packing/s21/** |
| [`s12/certificates/s32/`](s12/certificates/s32/) | **s(32) = 6**: a weighted closed cover of `[0,6]²` of total weight `31.7135 < 32`, certified at margin zero by two separately written exact checkers, and kernel-checked in full in Lean 4 with no hypothesis (`s32_eq_6`).  Write-up: **https://evand.github.io/square-packing/s32/** |
| [`s12/`](s12/) | Machine-checked results on unit squares in a square: **s(12) ≥ 15680/3951 = 3.968616…** (still the best lower bound for s(12) we know of), **s(11) ≥ 3040/797 = 3.814304…** (since superseded by jlevy's 3.827, Kleddamag's 3.875 and Queuingtheorydotcom's proof that s(11) = 3.877084…, Trump's packing), and a **case-free proof of s(13) = 4** (one weighted closed cover, checked at margin zero by two separately written checkers sharing no code, and kernel-checked in Lean with no hypothesis; chelokot's Lean archive kernel-checked Bentz's proof earlier).  Exact weighted certificates, a Rust verifier over the full continuum of placements, an independent Python re-check.  In Lean's kernel, with no hypothesis: s(11) ≥ 3040/797, s(12) ≥ 35/9, ≥ 3920/997 and ≥ 15680/3951, s(13) = 4.  Also the research log, including a detailed record of why these methods stop short of s(12) = 4.  Write-ups: **https://evand.github.io/square-packing/s12/** (s(11), s(12)) and **https://evand.github.io/square-packing/s13/** |

[![verify](https://github.com/evand/square-packing/actions/workflows/verify.yml/badge.svg)](https://github.com/evand/square-packing/actions/workflows/verify.yml)
re-checks the `s12/` certificates (fast tier) and builds the Lean whenever `s12/` changes; the slow
sweeps run on demand (`s12/verify.sh --full`).

## Status

Nothing here has been peer reviewed.  The results are computer-assisted and meant to be
checked: `s12/verify.sh` rebuilds the verifiers and re-checks every certificate.

## Data and licence

The code is MIT-licensed (`LICENSE`).  The packings themselves are David Ellsworth's
(https://kingbird.myphotos.cc/packing/squares_in_squares.html, continuing Erich Friedman's
survey).  `site/www/data/` is derived from his SVGs and quotes his attribution text; that
material is his and is not covered by the MIT licence.  Full credits are on the site's Sources
page (`site/www/sources.html`), including the 2026 work this builds on or runs beside: Burns, Massaccesi,
Fort, Mira, jlevy (Squares Project), Kleddamag, Guzhou0806, tokoharu, wand125 and chelokot.
