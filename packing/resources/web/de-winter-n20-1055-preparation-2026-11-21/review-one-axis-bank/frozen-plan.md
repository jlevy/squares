# Frozen Plan: One-Axis Polynomial Bank

This slice checks the 576 conditional polynomial contradictions in the one-aligned-tile
route for `0 < tan(theta/2) <= 1/24`. It does not check bridge enumeration, signs,
symmetry reduction, separation-graph coverage, or the unrestricted theorem.
The `theta = 0` endpoint remains the separate aligned-grid argument.

This is an independent arithmetic implementation after reading the contributor’s
statements, rule formulas, positivity routine and representative certificate records.
It is not a blind review.
No contributor module will be imported or executed.

## Immutable Input and Expected Census

The exact source is `proofs/one_axis_24.json.gz` from the retained stronger #1055 ZIP:

- ZIP: 1,425,895 bytes; SHA-256
  `475d7ef50e21ce4a83cfb4c8415c9e9852d619beeade5c4c8745c2c963d6c867`.
- Compressed member: 26,877 bytes; SHA-256
  `451b1116cf5b6eaa78ecc8233ee4e4c931537e6dfd3bd4fba2a6d91b1922d257`.
- Expanded JSON: 427,596 bytes; SHA-256
  `774cf1ffc704886c9ff3802600dc7d112ef87b25024d7147176bc2af4f14ee9f`.
- Expected bank: 576 rows, 9,777 rule uses, at most 28 rules per row, multiplier degree
  at most 12, margin degree at most 18, integer coefficient magnitude at most 13 bits.
- Rule-use census: same 5,458; wall 2,521; wall0 201; zero_favored 202; zero_straight
  475; rank 302; zero_flat 25; mixedstraight 491; mixdiag 102.

These are literal-data counts, not completed certificate checks.
The contributor source pin is `dad9c3fd3443bcb9f8950bc302445bdf1e3fbbcc`.
[Submission](https://github.com/jlevy/squares/issues/1055#issuecomment-7058955337).

## Mathematical Acceptance Condition

For each row, require exact integer-coefficient multipliers nonnegative on the whole
closed interval `[0, 1/24]`; exact cancellation of all 50 center coefficients; and the
stated margin equal to minus the weighted right-hand side.
Require the margin strictly positive on `(0, 1/24]`. All 576 rows and all predeclared
controls must pass.

The checker reconstructs a rule as a physical separating-axis, wall or rank inequality
using exact rational `c = (1-t²)/(1+t²)`, `s = 2t/(1+t²)`, `u = c+s`, and `d = u(u-1)`.
Its variables are `X = 2(1+t²)² x` and `Y = 2(1+t²)² y`. Multiplication of the physical
inequality by `2(1+t²)³` gives the bank’s integer polynomial row.
The semantic premise permitting that rule in a graph is outside this slice.

The physical rule formulas used in the independent reconstruction are below.
For a pair, the displacement is the first center minus the second; let `H = (1+u)/2`. In
a same-sign rule, the projected sign equals the recorded sign for the horizontal axis
and its negative for the vertical axis.
Diagonal rule signs are already projected signs.

| Rule | Physical left-hand side | Physical right-hand side |
| --- | --- | --- |
| same | `c dx + sigma s dy` | `-1` |
| mixdiag | `c dx + sigma s dy` | `-c u` |
| mixedstraight | `c dx` | `-c u + 4s d` |
| zero_favored | `c dx + sigma s dy` | `-H` |
| zero_flat | `c dx` | `-c H` |
| zero_straight | `c dx` | `-c H + 4s d` |
| aligned | `c dx` | `-c` |
| wall or wall0, lower | `-c x` | `-c w/2`, with width `w = u` or `1` |
| wall or wall0, upper | `c x` | `c(5-w/2)` |
| rank, sign epsilon | `epsilon c x` | `c(epsilon(g+1/2) + n d)`, with `n = 4-g` for upper and `g` for lower |

In this table, `dx` denotes the forward coordinate difference and `dy` the transverse
difference, regardless of axis.
In the transformed variables, each center coefficient is its physical normal multiplied
by `D = 1+t²`. The right-hand side is multiplied by `2D³`. With `C = 1-t²` and `S = 2t`,
`d = (C+S)(C+S-D)/D²`, so every listed cleared right-hand side has degree at most 6 and
every cleared center coefficient degree at most 2. The unused aligned rule is supported
as part of the rule vocabulary but has zero occurrences in the immutable bank.

Instead of copying the producer’s coefficient-convolution checker, exact identity
testing evaluates the independently reconstructed row at every integer node
`0, ..., M+6`, where `M` is the largest multiplier degree in that certificate.
A rule’s center coefficients have degree at most 2 and its right-hand side at most 6. A
residual has degree at most `M+6`; that many plus one distinct zeroes proves it
identically zero. A declared margin above that degree bound is refused.
Nodes outside the geometric angle interval are used only for algebraic identity.

For nonnegativity, convert an integer power polynomial `p(t)` to normalized Bernstein
coefficients on `[0, 1/24]` using exact fractions:
`b[k] = sum(p[i] * binom(k,i) / (24^i * binom(n,i)), i=0..k)`. All coefficients must be
nonnegative. Strict positivity on the interval open at zero follows from a strictly
positive final coefficient, including when the constant coefficient is zero.
This is a sufficient certificate criterion, not a complete decision procedure for all
nonnegative polynomials.

## Controls Frozen Before Execution

Six arithmetic controls:

1. Accept zero as nonnegative.
2. Refuse zero as a strict margin.
3. Accept `2 - 24t` as a strict margin.
4. Refuse `1 - 48t` as nonnegative.
5. Accept `t` as a strict margin on the interval open at zero.
6. Refuse `t - 24t²` as strict: its right endpoint is zero.

Six bank controls, based on the first literal certificate:

1. Accept the unchanged first row.
2. Refuse adding one to its declared margin constant: right-hand-side identity.
3. Refuse changing the first multiplier’s constant to minus one: multiplier sign.
4. Refuse adding one to the first multiplier: center-coefficient cancellation.
5. Refuse flipping the first same-rule sign: transverse cancellation.
6. Refuse a nonzero margin coefficient above the justified degree bound.

Four independently calculated rule-value fixtures at `t = 1/2` check the scaling and
vertical-axis sign: an upper tilted wall, a rank upper bound, a favorable aligned/tilted
diagonal and a same-orientation vertical pair.
These are algebraic fixtures, not geometric assertions at that angle.

The receipt must distinguish the 16 controls from the 576 original bank rows.
A refusal, unexpected exception, incomplete row count or unexpected control result is
failure, even if a partial output exists.

## Execution Boundary

Preparation only: do not execute, import, compile, syntax-check or run the new checker
until the coordinator clears the serialized memory-guard slot.
Only reading source data, writing these artifacts and hashing the frozen files is
authorized now.

Proposed eventual run: one Python 3.14.7 process, standard library only, `-I -B`, no
source imports, solver, network, repository writes or dependency installation.
Target under 20 seconds of wall time and under 0.10 GiB peak RSS; hard ceiling 60
seconds, 0.25 GiB sampled process-tree footprint, and stop at memory pressure 2. The
coordinator may choose a stricter ceiling before launch.
Use the memory-guard skill with a dedicated owned process group, external
temporary/cache paths, and retain the guard journal and process exit separately from the
checker result.

The output is one JSON receipt with complete per-row outcomes, control outcomes, input
binding, wall/CPU time and peak RSS. The checker publishes the receipt only after
complete success, using a same-directory temporary file and replacement.
Do not infer graph coverage or a Stage 4 theorem verdict from bank success.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
