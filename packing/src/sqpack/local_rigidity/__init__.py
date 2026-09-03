"""Exact local-rigidity instrument for a fixed-side square packing.

`H-060` asks whether Goebel's exact `n = 5` optimum is *isolated* in the fixed-side
feasible set. `T-012` settles the first two orders -- the infinitesimal cone is one line
and a self-stress obstructs it -- and cannot settle isolation, because an arc whose first
nonzero Puiseux coefficient sits above order one is invisible to both.

This package builds the object that argument needs and does not yet have: one intrinsic,
locally injective chart in which the *entire* local feasible set is a finite polynomial
system with exactly known active and inactive margins, so that the curve-selection and
coefficient argument has something exact to run on.

- `polynomial` -- sparse multivariate polynomials over `sqpack.field`, no floats;
- `chart` -- the tangent half-angle substitution, with its own injectivity, orthogonality
  and denominator-positivity certificates;
- `system` -- every wall and separating-axis inequality with exact base margins, and the
  neighborhood expressed as strict conditions rather than as a radius;
- `binding` -- the exact transfer of chart gradients and second jets onto `T-012`'s `A`
  and `q`;
- `controls` -- the refusals, each of which must reject;
- `receipt` -- the replayable, byte-stable certificate.

Nothing on the certified path uses floating point.
"""

from __future__ import annotations
