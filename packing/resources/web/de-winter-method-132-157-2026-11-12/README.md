# Joost de Winter’s Method for 132 and 157 at 57de046

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/57de0465c07f7ba94bbd1fd2a317ee3f08cfedca)
at `57de0465c07f7ba94bbd1fd2a317ee3f08cfedca` (committed 2026-11-12T08:30:46Z), the head
of `main` when it was read at 08:56Z and again at 09:02Z.
It is the one commit after `6617869`, the pin of the
[s132](../de-winter-s132-upper-bound-2026-11-11/README.md) and
[s157](../de-winter-s157-upper-bound-2026-11-11/README.md) packets, and the author’s
answers on [issue #958](https://github.com/jlevy/squares/issues/958)
([issuecomment-6818738203](https://github.com/jlevy/squares/issues/958#issuecomment-6818738203),
08:31:55Z, 69 seconds later) name it.
By the result-import runbook a later revision is a new packet, so this one keeps the
commit and the s132 and s157 packets stay at `6617869`.

The commit publishes the method behind T-292 (132) and T-293 (157) and adds the schema
envelope to both witness files.
It adds no packing and no bound, and the record’s entries, rungs and houses at 132 and
157 do not change.
Intake lane L136 (think-c3p2) retained it on 12 November 2026.

## What the Source Claims

- **The method.** `method_n132_n157/README.md` says the folder holds the code that
  produced both packings and the high-precision solutions behind both certificates, in
  four steps:
  - a growth step (`grow.py`, `surgery.py`) that cuts the packing along one vertical and
    one horizontal line, moves the parts about 1.15 apart and copies every square in the
    layer next to a cut once across it: axis-aligned squares by one unit, tilted squares
    by 1/cos θ along the cut’s normal. A copy that overlaps another square by more than
    0.15 is dropped;
  - an optimization (`slp.py`, `nlp.py`) that removes overlaps with linear programs at a
    fixed side, then minimizes the side with IPOPT through CasADi, with one
    separating-axis constraint per corner of each pair of nearby squares;
  - a high-precision solution (`newton.py`) of the contact equations by Newton’s method at
    900 bits with python-flint. It writes one equation for each corner within 10⁻⁶ of the
    edge line of a neighbouring square, on a separating axis, and one for each corner
    within 10⁻⁶ of a wall: 1,407 at 132 and 2,024 at 157;
  - a certificate (`package.py`, `mkcert.py`) that scales the solution by 1 + 10⁻⁶⁰,
    shifts it by 10⁻⁶⁰, writes it as exact rationals and checks it in rational
    arithmetic.
- **Reproduction.** Run from the seed, the 109-square packing of `best_fit_101_500.csv`
  at `Samanyu-dev/squares_in_squares` `53551d7`, with cuts at x = 3.48, y = 8.61 and
  then x = 9.71, y = 3.33, the scripts print the sides 11.976048386602 and
  12.993302615406 after the two growth steps. They then write `n132_exact.json` and
  `n157_exact.json` byte for byte equal to the published files.
  The README names Python 3.10 or later with numpy, scipy, casadi, python-flint, mpmath
  and matplotlib, and shapely for the second check.
  The seed is not in the repository.
- **The solutions.** `n132_solution_250_digits.txt` and `n157_solution_250_digits.txt`
  state the side and each square’s x, y and angle in radians to 250 places.
- **Two checks.** `check_binary64.py` is a separating-axis test over all pairs in
  binary64; the README gives a least separation of about −2 × 10⁻¹⁵ at 132 and
  −4 × 10⁻¹⁵ at 157, rounding error on gaps of 10⁻⁶⁰. `check_shapely.py` gives the area
  of the union with Shapely as 132.0000000000 and 157.0000000000. The README says both
  were written for the folder and repeat the checks reported with the packings, and
  that the perturbation trials and the force-balance check are outside it.
- **The witness files.** `n132/n132_witness.yaml` and `n157/n157_witness.yaml` gain a
  `softschema` header naming `packing.squares:Witness/v2` and this repository’s
  `witness.schema.yaml`, a `claim` block (`coordinate_provenance: verified`,
  `method: exact-algebraic`) and the lowercase ids `W-n132-de-winter` and
  `W-n157-de-winter`. The commit message says the squares and the sides are unchanged.
- **AI assistance.** The method README says the code was written with Claude Fable 5.2
  (Anthropic) under Joost de Winter’s direction.

## What Was Checked Here

- **Custody.** Every file is bound to its Git blob at the pin, and both `SHA256SUMS`
  files match the five other files of their folders.
  `n132_exact.json`, `n157_exact.json` and `verify_exact.py` are byte-identical to the
  copies the `6617869` packets retain.
- **The squares and sides are unchanged.** `git diff 6617869 57de046` adds 10 lines to
  each witness file and removes 1: the header’s five, the claim block’s four and the new
  id, for the old one. No line of a square or of the side changes, so both packings are
  the ones T-292 and T-293 record.
- **The schema.** `packing-witness inspect` reads both files past the JSON-schema stage
  and then refuses each, `FAILED [semantic-invalid]: verified claims require a
  replayable certificate record`, exit 2.
  The files validate against `witness.schema.yaml`, as the answer says.
  This repository’s loader adds one rule the schema cannot state: a claim of
  `coordinate_provenance: verified` must carry a replayable `certificate` record.
  The record keeps its own witnesses at 132 and 157, so this blocks nothing.
- **The reproduction was not run.** CasADi (with IPOPT), python-flint, matplotlib and
  Shapely are not in the project environment, and adding them is not a cheap check.
  The seed is in a repository the project does not watch and does not retain.
  The growth step’s re-optimization also stops on a wall-clock budget
  (`nlp.compact(..., tmax=120)` in `grow.py`), so its binary64 result can depend on
  the machine; the 900-bit Newton step then solves the contact equations that result
  selects. That the scripts reproduce both exact JSON files byte for byte is the
  author’s claim, unchecked here.
- **No program from the folder ran here.** The scripts and both checks are retained as
  data.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json). The scope is the licence,
the root README, `method_n132_n157/`, `n132/` and `n157/`: 26 files, 19 retained under
[source/](source/) and 7 pinned by digest only.
The pinned seven are `LICENSE`, against the copy the
[227, 229 and 260 packet](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
retains; the two exact JSON files and both copies of `verify_exact.py`, against the
s132 and s157 packets’ copies; and the two figures.
Retained are the root README, the twelve files of `method_n132_n157/`, and the README,
`SHA256SUMS` and witness of each count.

## What Is Not Established

- **The reproduction from the seed**, as above.
- **The 250-digit solutions as local optima**, and any optimality: not replayed here.
- **Human oversight**: no record is retained.

## Credit and Licence

The method is Joost de Winter’s, after Samanyu-dev’s pinwheel at 109, the seed, which
his READMEs credit. The README says the code was written with Claude Fable 5.2
(Anthropic) under his direction. The bibliography key is
**[de Winter method 132 157 2026-11-12]**.

Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter,
by `LICENSE` at the pin, which the root README says covers all files.
The seed’s licence is the owner’s question on think-71uq; the author’s answer says he
used the public file as published at `53551d7`, credited it, did not contact
Samanyu-dev, and cannot say what “MIT-style” covers beyond the code.
Retaining a file grants no licence and relicenses nothing.

## Commands

From `packing/`, with the project interpreter:

```bash
P=de-winter-method-132-157-2026-11-12
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
packing-witness inspect resources/web/$P/source/n132/n132_witness.yaml
packing-witness inspect resources/web/$P/source/n157/n157_witness.yaml
git -C CHECKOUT diff --numstat 6617869 57de046 -- n132/n132_witness.yaml n157/n157_witness.yaml
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
