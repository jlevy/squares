# Handoff — 2026-09-04, close of the fractional-certificate block

Everything a session resuming from [PR #78](https://github.com/jlevy/squares/pull/78)
needs. Branch `claude/agenda-017-plan-and-run`, head `88a45915`.

## What moved

| Result | Bound | Was | Score |
| --- | --- | --- | --- |
| `T-018` | `s(11) ≥ 19/5 = 3.8` | `2 + 4/√5 = 3.788854`, Stromquist 2003 | `S5` |
| `T-017` | `s(12) ≥ 393/100 = 3.93` | `3.788854`, inherited by monotonicity | `S4` |

And a corollary neither had: **`s(12) > s(11)` strictly**, since
`3.93 > 3.877084 ≥ s(11)` by Trump’s 1979 packing.

Both are `V4/C3`. They are *not* `C4`: the two exact decisions share a method family,
and an interval-certified decision is what would move that rung.

## The instrument

`packing/src/sqpack/fractional/` — `certificate.py` (five conditions `C0`–`C4`, the
verifier and the only thing that decides), `sweep.py` (the exact event-cell reduction),
`model.py`, `generate.py` (covering LP by row generation), `colgen.py` (dual-driven
column generation), `ceiling.py` (the fractional packing dual, built and tested, no
ceiling proved).

Certificates live under `packing/cases/n11_fractional_certificate/` and
`packing/cases/n12_fractional_certificate/`, each with a replay gate:

```shell
cd packing && uv run --frozen --all-extras python -m cases.n11_fractional_certificate
```

`cases/n12_fractional_certificate/independent_verify.py` is the second verifier, written
from the theorem statement with the implementation withheld.
It reproduces Massaccesi’s published `n = 17` bound as its own control, which is what
makes it worth anything.

## Where the next rungs are

- **`n = 11` above `3.8`.** Two column-generation runs were live at block close and are
  checkpointed under `scratchpad/laneB/` (`cg2-381_100.pkl`, `cg2-383_100.pkl`). `3.81`
  sat at exactly `11.000` on a degenerate plateau with 32 negative-reduced-cost columns
  entering per round; `3.83` plateaued near `11.104` with the dual close to feasible, so
  `τ*(3.83) ≥ 11` may be real.
  The slope between them is about `0.10` per `0.01` of side.
  `3.81` is plausible with more columns; `3.85` and above look closed.
- **`n = 12` above `3.93`.** Only `0.06` of headroom remains: the shrink caps this
  method at `B_max · s(12) = 3.99082` with the 181-direction net.
  A further rung needs a finer net *and* a finer site set; 361 directions raise the cap
  only to `3.99540`.
- **`C3 → C4` on either result.** An interval-certified decision, not another
  exact-algebraic pass.
- **The ceiling route** (`ceiling.py`) is built and unused.
  It would discharge `H-061`’s pre-registered rejection branch, but the integral
  packings it needs at the interesting sides are themselves open problems.

## What not to repeat

- `D-434`: the search’s separation oracle scored fewer placements than the verifier
  decides. Fixed, and it is what unlocked every rung above `77/20`. If a future candidate
  converges below `n` and is then refused by `C4` narrowly, suspect this shape first.
- `D-433`: `rationalise` floored while its docstring said it rounded up.
- Four “negatives” recorded in this block were fixed-grid restricted optima, not `τ*`.
  Round values (`18.0`, `25.0`, `200/11`) are the signature.
  `τ*` depends on the side alone, never on `n`; check any negative against the bounds
  already in the record before believing it.
- Do not sweep `(grid count, inset)` as a product: those site sets are incomparable.
  Take unions, which are monotone.
- Do not stop column generation at a round cap.

## How to run the block

[`three-lane-research-method.md`](three-lane-research-method.md) is the method, written
so it can be followed rather than reconstructed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
