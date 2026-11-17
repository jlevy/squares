# Programs of the 5 November 2026 Review of #895

These programs belong to the stage 4 mathematical review of Kaelan Yim’s certificate for
s(260) ([jlevy/squares#895](https://github.com/jlevy/squares/issues/895)), written up in
`docs/project/reviews/review-2026-11-05-yim-895-260.md`. Claude (AI review) wrote and
ran them at the strong tier (`tbd-strong-max`), at maximum reasoning.
The review lane was prompted separately and shared no context with the import lane.

## What the Authors Read

The programs were written from these sources:

- the mathematics: separating axes for convex polygons, Sutherland–Hodgman clipping, the
  shoelace formula and the half-angle substitution;
- the certificate format as #895 and the packet README state it;
- the rotation sense, measured against the n-260 house witness and T-257’s certificate.

They read no producer code:

- not the author’s conversion or search code, neither of which is published;
- not `devtools.check_rational_witness_independent`, the program the author ran;
- not `sqpack`’s witness verifier, nor `devtools.upper_bound_reports`;
- not Evan Daniel’s `verify_cert.py` or `verify_cert2.py`.

They import nothing from this repository.
They are a clean room and share nothing.

## The Programs

Each receipt records the SHA-256 of the program that wrote it.
All but `custody.json` also record that of `certcheck.py`, which is
`0890eea39e3c622f8a3d5d4d4d8a7e79eb2ceb162a6551ecfc0c00bd2464ce5c` in each.
CPU is the receipt’s `cpu_seconds_total`.

| Program | Role | Receipt and result | CPU s |
| --- | --- | --- | --- |
| `certcheck.py` | Decides every wall and all 33,670 pairs by method A (separating axes, `Fraction`) and method B (exact clipped areas), no distance filter | `check-yim-n260-ccw.json`: accepted by both. `check-yim-n260-cw.json`, the reversed sense: refused, 159 pairs by both. `check-t257-s260-ccw.json`: accepted. `check-t257-s260-cw.json`: refused, 152 pairs | 16.5, 16.2, 9.2, 9.5 |
| `selftest.py` | Holds both methods to 23 hand cases with known answers and 400 random pairs taken exactly to contact, then $10^{-30}$ either side (1,200 probes) | `selftest.json`: passed, no disagreement | 1.2 |
| `controls.py` | 17 sharp and gross controls on `n260.cert`, each decided in full by both methods | `controls.json`: all as expected | 302.2 |
| `side.py` | The header against #895’s fraction, the prints, the extents, and each certificate’s exact contact scale about the corner | `side.json` | 6.3 |
| `identity.py` | The house witness against T-257’s certificate; identity under the eight symmetries; moves, turns, tilts and contacts | `identity.json` | 22.7 |
| `upright.py` | The 146 tiny-turned squares set upright, decided at #895’s side, and the exact contact dilation of that variant at contact and $10^{-30}$ below; a similarity fit | `upright.json` | 46.0 |
| `rowsback.py` | In the upright variant, whole rows put back at T-257’s abscissae, decided at #895’s side | `rowsback.json` | 108.8 |
| `movers.py` | Movers beyond 0.1, 0.01 and 0.001 exchanged between the packings, decided by both methods | `movers.json` | 84.0 |
| `slides.py` | Each mover beyond 0.1 slid back alone, then those accepted together | `slides.json` | 40.2 |
| `custody.py` | Read-only git plumbing on a bare clone of vitamoon/vitamoon, against the packet | `custody.json`: custody holds | 0.07 |
| `run_all.sh` | Runs all of the above | `run-part1.log`, `run-part2.log` |  |

The final runs took 662.8 CPU-seconds, about 11 CPU-minutes, at `nice -n 19` with at
most two processes. With the development runs, the review used about 23 CPU-minutes.

## What They Printed

- **Feasibility.** The least pair gap is $1.336398719863592 \times 10^{-15}$, at rows
  203 and 210. Row 253 touches the right wall exactly, the only zero clearance.
  The top wall clears by $4.3232 \times 10^{-13}$ (row 236), the left by
  $7.216449644 \times 10^{-16}$ (row 133) and the bottom by
  $7.216449650 \times 10^{-16}$ (row 7). Methods A and B agree on every pair and wall.
- **The side.** The header equals #895’s fraction verbatim.
  - T-257’s side minus #895’s is $1.99269842703378 \times 10^{-10}$.
  - T-257’s own poses reach contact at scale $1 - 1.2016 \times 10^{-12}$, which is
    $1.9988 \times 10^{-11}$ below its side.
  - #895’s side lies $1.7928 \times 10^{-10}$ below that contact side.
- **Identity.** The packings are one to one under the identity only, row for row.
  - 26, 64, 96 and 114 squares move beyond 0.1, 0.01, $10^{-3}$ and $10^{-6}$; the
    largest move is 0.382307.
  - 14 squares turn beyond $10^{-6}$ radians, by up to 1.4984°.
  - 105 squares are tilted against T-257’s 104.
  - T-257 has 139 squares exactly upright: 112 with $t = 0$ and 27 with $t = 1$.
- **Contacts.** With contact taken as a gap within $10^{-9}$:
  - pairs: 520 in #895 and 528 in T-257, 504 in both;
  - walls: 50 and 51, 49 in both.
- **The tiny turn.** It is not needed.
  - Upright, the variant packs at #895’s side.
  - Its contact dilation, at $16.6339825019080413$ (pair 205, 208), is accepted at
    contact and refused $10^{-30}$ below.
- **The rows.** In the upright variant, three sets of rows can go back where T-257 has
  them at #895’s side: the bottom row (rows 1–16), the top row (rows 236–251) and the
  pair at $y \approx 10.13$ (rows 138, 232). The others collide with squares of the
  tilted island.
- **The exchanges.** `movers.py` and `slides.py` are inconclusive by design.
  Moves that run along rows collide with neighbours left in place, and a box-centred
  carry puts wall-touching squares about $10^{-10}$ outside.
  They are kept because they ran, and `rowsback.py` is the test the review relies on.

## What Decides What

`certcheck.py`’s run on `n260.cert` is the review’s exact-feasibility evidence, with
full coverage: every wall and all 33,670 pairs.
`selftest.py` and `controls.py` are its controls.
The other programs decide nothing about the bound:

- `side.py`, `identity.py`, `upright.py`, `rowsback.py`, `movers.py` and `slides.py` are
  measurements;
- `custody.py` is a premise check.

`upright.py` and `rowsback.py` decide packings derived here, which are not the claim and
are cited by no evidence entry.

## How to Run

Run from the repository root with the project interpreter, after placing a bare clone of
vitamoon/vitamoon at `CLONE` for the custody part:

```bash
D=packing/resources/web/yim-s260-upper-bound-2026-11-05/review/review-2026-11-05
bash $D/programs/run_all.sh packing/.venv/bin/python3 $D/programs $D/out all
bash $D/programs/run_all.sh packing/.venv/bin/python3 $D/programs $D/out custody CLONE
```

Each program runs alone under the same interpreter with `-I`, as its docstring shows.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
