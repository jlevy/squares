# Fibonacci Torus Confirmation Checks

This case retains W2 checks of the mathematics visible in an owner-supplied abstract.
The
[W3 assessment](../../campaign/explorations/X-050-fibonacci-torus-and-boundary-information.md)
distinguishes reconstructed results from the missing manuscript’s claims.

| Instrument | Evidence | Scope |
| --- | --- | --- |
| [algebra.py](algebra.py) | [algebra-result.json](algebra-result.json) | Exact quotient arithmetic, pair actions, return model, bundle and modular calculations, and degree-eight Galois certificate |
| [geometry.py](geometry.py) | [geometry-result.json](geometry-result.json) | A fully defined two-parameter contact family on $u\in[9/25,37/100]$, $L\in[387/100,389/100]$, all walls and pair alternatives, endpoint and cusp bound, contact-graph asymmetry |
| [periodic.py](periodic.py) | [periodic-result.json](periodic-result.json) | Explicit axis-parallel periodic packings at $N=11,S=11/3$ and $N=17,S=17/4$, checked by wrapped distances and neighboring lifts; exact cyclic-gap and endpoint checks certify the absence of empty straight seams |

From `packing/`, using the project’s Python 3.14 environment:

```bash
uv run --frozen --all-extras --group dev python -m cases.fibonacci_torus.algebra
uv run --frozen --all-extras --group dev python -m cases.fibonacci_torus.geometry
uv run --frozen --all-extras --group dev python -m cases.fibonacci_torus.periodic
uv run --frozen --all-extras --group dev pytest tests/test_fibonacci_torus.py
```

Each CLI prints a complete deterministic JSON receipt.
The tests compare fresh calculations to the retained mathematical payload and exercise
controls that reject changed polynomials, false group actions, interior-negative
Bernstein polynomials, denominator poles, duplicated squares, and wrapped overlaps.
These are confirmation checks, not numerical searches or performance benchmarks.
The periodic audit also checks seam gaps below, at and above the unit threshold,
singleton wraparound, and malformed-input refusal.

The geometry proof uses rational Bernstein coefficients on a stated interval, not
sampling. Its source constants come from the retained Trump construction.
The graph comes from the existing exact-algebraic atlas entry; this pass checks graph
asymmetry and does not rerun the atlas’s original contact-verification pipeline.
The finite algebra sweep does not replace the all-index proof in the algebra review.

The torus-to-packing inverse, cell congruence, manuscript’s full parameter domain and
its particular Erdős #106 counterexample are not verified.
No global lower bound or unrestricted capture theorem is claimed by these tools.

The checks were authored and run under the
[research plan](../../../docs/project/specs/active/plan-2026-10-07-fibonacci-torus.md).
Algebra and geometry had separate authors; the algebra reviewer subsequently checked the
geometry and synthesis.
The source reviewer independently replayed the periodic examples.
Review notes retain limitations instead of treating that separation as a formal proof
kernel.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
