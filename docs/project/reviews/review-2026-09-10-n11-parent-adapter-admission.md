# Independent Review of the Adopted Parent Adapter

**September 10, 2026. Verdict: PASS for the two library modules and their focused
tests.** No blocking defect was found in this bounded review.
BC326 still needs a production command, frozen source identities, a result schema,
process deadlines, and independent readback before its scientific target can run.
This review establishes no new packing bound and reports no target result.

The reviewed branch is `codex/n11-daytime-strategy`, based on merged PR139 at
`3a18a05a6af75e3800612549d5a3c5fe419b96f2`. The reviewed files are:

- `packing/devtools/wall_owner_parent_compatibility.py`;
- `packing/devtools/wall_owner_parent_inputs.py`;
- `packing/tests/test_wall_owner_parent_compatibility.py`;
- `packing/tests/test_wall_owner_parent_inputs.py`.

The independent review used 28 focused tests and 18 separate adversarial controls.
It ran no retained scientific input through the proposed target.

## What the Adapter Represents

For a retained unit core direction `r`, put

```text
S = |r.x| + |r.y|,
T = ||r.x| - |r.y||.
```

The adapter computes the exact necessary coordinate half-extent

```text
e = max((B/2)*S, 1/2, (S-T*D)/(2+D^2)).
```

The third term bounds every unit parent whose principal angular mismatch from `r`
satisfies `tan(|delta|) <= D`. The old strict-core containment term remains in the
maximum. Production use accepts only the frozen values `B=9977/10000`, `q=96/25`,
`D=207107/90000000`, and the rule that selects a nearest retained direction before owner
routing.

The bound restricts a parent centre to a closed square.
It is necessary, not sufficient: a surviving centre need not realize a permitted unit
parent angle, coexist with the other selected owners, or extend to an eleven-square
packing.

## Domain and Quantifier Checks

The implementation reconstructs each original anchored owner-centre domain from its mark
and signed frame before intersecting the parent box.
It checks the original polygon, dimension, support values, and common rectangle rather
than accepting cached derivatives.
After intersection it recomputes every consumed field.

Empty, point, segment, and area domains remain distinct.
An all-empty class is recorded as impossible without inventing a numerical margin.
A mixed class retains its empty frame identities while taking extrema over every
nonempty frame. Missing or unfinished frames remain unresolved.

For each of the eight signed owner/residual axes, the separation calculation uses the
minimum owner-centre projection and subtracts both square support radii.
The maximum over axes and allowed centres decides whether a fixed residual pose has an
individually separated strict-core witness in that frame.
An exhaustive nonpositive maximum excludes strict-core coexistence for that fixed pose
and complete class manifest.
Zero is enough for this fixed-pose exclusion because selected cores lie strictly inside
their disjoint parents, but zero gives no neighbourhood radius.

The result does not decide simultaneous compatibility of four owners.
One positive frame is an individual witness only.
The residual core uses its own direction and source provenance; it does not inherit an
owner mark or displacement box.

## Source and Symmetry Checks

The input wrapper binds four retained receipts by repository-relative path, Git blob,
producer revision where exposed, and one checkout revision.
It reconstructs the full 361-orientation residual manifest, the sixteen local owner
classes, and all 181 expected frames for each selected physical owner.
Both existing strict-escape replays must pass before the wrapper returns admitted
inputs.

The physical corner maps are exactly identity, horizontal reflection, vertical
reflection, and half-turn for bottom-left, bottom-right, top-left, and top-right.
The review checked their coefficients, translations, corner permutations, signed-frame
transport, and displacement-coordinate exchange.
The symmetric parent box commutes with all four maps.
No diagonal class involution is substituted.

The universal replay requires one unique extremum index for every nonempty expected
frame and no extras.
It compares each saved extremum with an exact recomputation and then checks the literal
global maximum separately.
Expiry leaves an unresolved partial result and never promotes the largest value seen so
far into an exhaustive negative.

## Independent Controls

The project Python 3.14 checks returned:

| Check | Result |
| --- | --- |
| Adopted focused test files | 28 passed |
| Independent adversarial geometry, source, and replay controls | 18 passed |
| Ruff over the four adopted files | Passed |
| BasedPyright over the four adopted files | 0 errors, 0 warnings, 0 notes |

The adversarial controls include old-domain substitution, duplicate extrema, a shared
false slack that literal geometry rejects, source-provenance loss with unchanged
cardinality, changed unprocessed residual rows, both strict-replay failures,
root-versus-`packing/` invocation, invalid pins, and a symlink escape.
Additional exact controls compare the rational extent with explicitly rotated unit
parents and transport area, segment, and point domains through all four physical maps.

These controls support adoption of the pure modules.
They do not replace the universal analytic argument or admit the target path that does
not yet exist.

## Remaining Admission Work

Before BC326 runs:

1. Commit the reviewed modules and freeze the clean implementation revision plus all
   four receipt identities.
   Verify the complete implementation dependency graph is clean in that checkout.
2. Add a production command that calls the full load-and-replay wrapper before starting
   the scientific clock.
   Rebind the independent manifests during result readback; a result’s own frame count
   is not source authority.
3. Register the fixed exp151 residual, tuple `(0,0,0,7)`, physical owner order, B-only
   control, and global-D treatment.
   Test residual self-exclusion first.
4. Attribute an owner-domain gain only if the matched B-only control has a positive
   witness and the parent-restricted class is completely nonpositive.
5. Enforce the planned 90-second internal target allowance, 120-second external bound,
   and two-second termination grace.
   Preserve partial and error outcomes.
6. Write a schema-checked result atomically, retaining complete source identities,
   manifests, maps, frame dispositions, exact extrema, and completion state.
   Bind and independently replay that file before interpreting it.

The adopted modules make this a bounded implementation task rather than an open formula
question. Until the six steps pass, BC326 remains source admission and its scientific
question is unrun.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
