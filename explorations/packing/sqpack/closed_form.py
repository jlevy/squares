"""Recognise a packing side as a simple algebraic number, or decline to.

A local optimum of this problem is where contact constraints meet, so its side is an
algebraic number of modest height — `2 + ½√2`, `1½ + √2`, `2 + ⅔√2`. A configuration
that merely *stopped* is not: it lands wherever the budget ran out, and that is a
number with no short description.

That asymmetry is an **oracle**, and it is the one this project most needs. Every other
check available here — schema, dedup, determinism, round trip — verifies that a value
was handled consistently. None of them can tell a converged optimum from an interrupted
descent, which is exactly the confusion that produced [D-030](../defects.md): twelve
sweep-limit stopping points recorded as twelve basins with every structural invariant
green.

## Why a match is evidence rather than numerology

The search is bounded: `r·v = p + q√d` for `d ∈ {2, 3, 5, 6}`, `r ≤ 12`, `|p|, |q| ≤ 40`.
That is about `4 * 12 * 81 * 81 ≈ 3.1e5` candidate expressions. A value unrelated to any
of them matches within `1e-11` with probability of order `3.1e5 * 1e-11 ≈ 3e-6`.

So a match at that residual is roughly a one-in-300,000 coincidence, and a *table* of
matches — several basins in one census each landing on a short form — is not a
coincidence at all. The residual is always reported alongside, so a reader can apply
their own bar rather than inheriting this one.

## What it does not claim

A match is **not a proof** that the side equals the form. It is evidence that the
configuration is a genuine optimum rather than a stopping point. Promotion of any value
to `exact` routes through [`sqpack.verify`](verify.py) over the packing's own number
field, and nothing here is entitled to that word.

Declining is the common case and is not a failure: `s(11)` is a degree-8 algebraic
number and will never be recognised by this. `None` means "no short form in this family",
never "not a real optimum".
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Surds a packing side plausibly lives in. 45-degree structure gives sqrt(2), and the
# oblique records give higher degrees this deliberately does not reach for -- a family
# wide enough to match anything is not an oracle.
SURDS: tuple[int, ...] = (2, 3, 5, 6)

MAX_DENOM = 12
MAX_COEFF = 40
DEFAULT_TOL = 1e-11


@dataclass(frozen=True)
class ClosedForm:
    """`value == (p + q*sqrt(d)) / r`, to within `residual`."""

    p: int
    q: int
    d: int
    r: int
    residual: float

    def __str__(self) -> str:
        if self.q == 0:
            return f"{self.p}" if self.r == 1 else f"{self.p}/{self.r}"
        surd = f"√{self.d}"
        coeff = "" if self.q == 1 else ("-" if self.q == -1 else str(self.q))
        term = f"{coeff}{surd}"
        head = "" if self.p == 0 else f"{self.p} {'+' if self.q > 0 else '-'} "
        body = f"{head}{term if self.p == 0 else term.lstrip('-')}"
        return body if self.r == 1 else f"({body})/{self.r}"

    @property
    def value(self) -> float:
        return (self.p + self.q * math.sqrt(self.d)) / self.r


def _height(p: int, q: int, r: int) -> int:
    """How complicated the expression is. Ties break toward the simpler form, so
    `2√2` is preferred over an equal-residual `(16√2)/8` saying the same thing."""
    return abs(p) + abs(q) + r


def recognise(value: float, *, tol: float = DEFAULT_TOL) -> ClosedForm | None:
    """The simplest `(p + q√d)/r` matching `value`, or None.

    Bounded exhaustive search rather than a lattice method: the space is small enough
    that being able to state its exact size — and therefore the coincidence probability
    above — is worth more than the speed.
    """
    best: ClosedForm | None = None
    for d in SURDS:
        root = math.sqrt(d)
        for r in range(1, MAX_DENOM + 1):
            target = value * r
            for q in range(-MAX_COEFF, MAX_COEFF + 1):
                p_real = target - q * root
                p = round(p_real)
                if abs(p) > MAX_COEFF:
                    continue
                residual = abs((p + q * root) / r - value)
                if residual > tol:
                    continue
                cand = ClosedForm(p=p, q=q, d=d, r=r, residual=residual)
                if best is None or (
                    _height(p, q, r),
                    residual,
                ) < (_height(best.p, best.q, best.r), best.residual):
                    best = cand
    return best


def describe(value: float, *, tol: float = DEFAULT_TOL) -> str:
    """`recognise`, rendered for a report. Never raises, always says something true."""
    form = recognise(value, tol=tol)
    return "unrecognised" if form is None else f"{form} (residual {form.residual:.2e})"
