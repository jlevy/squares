"""Recognise a packing side as a simple algebraic expression, or decline to.

Several known packing optima have short forms such as `2 + 1/2 sqrt(2)`,
`1 1/2 + sqrt(2)`, and `2 + 2/3 sqrt(2)`. Matching one is useful for recognizing a
known control value and for proposing an exact-reconstruction hypothesis.
It is not a convergence or local-optimality oracle.

The search is bounded: `r*v = p + q*sqrt(d)` for `d in {2, 3, 5, 6}`, `r <= 12`, and
`|p|, |q| <= 40`. That finite family makes the result interpretable, but it does not
make a distribution-free coincidence probability available. Optimizer outputs are
structured, a censored endpoint can lie near a short form, and a positive-dimensional
stationary component may have an exactly recognized side.

## What it does not claim

A match is **not a proof** that the side equals the form and is not evidence by itself
that the configuration is a genuine optimum rather than a stopping point. Promotion of
any value to `exact` routes through [`sqpack.verify`](verify.py) over the packing's own
number field, and local-optimum claims require separate stationarity and isolation
evidence.

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
