# Predeclared Geometry and Controls

These controls were specified and implemented before the first run.
The frozen source and original plan identities are recorded in
[freeze.json](frozen/freeze.json).
The portable verifier preserves them.

The rows are centers `[cx,cy]` measured from the container’s lower-left origin and
signed counterclockwise `t = tan(theta/2)`. Put `u=((1-t²)/(1+t²),2t/(1+t²))` and
`v=(-u_y,u_x)`. Each unit square has vertices `center ± u/2 ± v/2`. The check verifies
exact unit lengths and orthogonality, all four wall inequalities at every vertex, and
every unordered pair.
A strict separation of coordinate projections certifies a pair; every remaining pair
receives all four square-edge-axis checks.
Nonnegative maximum separation margin accepts disjoint interiors, including contact.
A negative maximum rejects an interior overlap.
All arithmetic uses rational numbers.

Before checking the submitted witness, a synthetic pair with `t=1/3` must accept exact
edge contact, reject a center displacement multiplied by `1-10^-80`, and accept the
corresponding `1+10^-80` displacement.
A synthetic right wall must accept exact contact and reject an inward step of `10^-80`.

After the submitted checks, the source pair with the least maximum edge-axis margin is
moved along its center displacement to the exact first-contact scale.
Its inward and outward displacements must respectively reject and accept.
All submitted wall and pair equalities are recorded separately from these constructed
control equalities. The enclosing side is reduced to the largest submitted top/right
extent minus `10^-80`; at least one wall inequality must fail.

The [mathematical receipt](results/independent-feasibility.json) records the measured
outcomes, including the actual source contact `(123,124)` at scale exactly `1`. The
computation relies on Python’s rational arithmetic and execution, without a proof
assistant. It establishes finite feasibility of these coordinates, with no priority or
minimality claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
