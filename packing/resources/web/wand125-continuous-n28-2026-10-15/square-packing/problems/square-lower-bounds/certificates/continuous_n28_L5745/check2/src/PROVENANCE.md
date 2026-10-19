# Provenance

The supplied `upstream/` snapshot is Guzhou0806/n40-square-packing, commit
`71c97d0`, licensed under MIT. It has not been edited. The upstream copyright
and licence are retained in `upstream/LICENSE` and copied to `kernel/LICENSE`.

The interval arithmetic, continuous half-tangent parameterization, rectangle
classification, concave-section area lower bound, translation derivative
bounds, binary subdivision, and exact integer hinge-grid algorithm are reused
from `upstream/verifier/continuous_pose.cpp` and `axis_integer_grid.cpp`.
The existing angle-loss splitting heuristic is unchanged.

`CHANGES.md` documents the cap increases and receipt identity instrumentation,
with the complete unified diff. `kernel/identity.h` is a new standard C++ SHA-256
implementation. `generator.py`, `check.py`, `make_control.py`, and `tests/` are
new independently written orchestration, exact parsing, generation, and tests.
The generator follows the mathematical conventions of the supplied `exact.py`;
frozen-input hashes test exact regression compatibility.

No sibling checker or other files outside this folder were opened or copied.
This is independent orchestration and input handling around a shared upstream
mathematical kernel, not an independently derived numerical proof algorithm.
The upstream proof explains its own earlier mathematical/code lineage.
