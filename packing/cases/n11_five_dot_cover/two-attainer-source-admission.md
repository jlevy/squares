# Fixed Two-Attainer Obstruction: Source Admission

**2026-09-10. GO for the frozen instrument’s stated finite construction.** This is
completed source preparation.
No target attainer reconstruction, separation gap, perturbation, or strict target replay
has been evaluated. A future scientific outcome still needs a separately registered and
prospectively allocated run.

## Reviewed Bytes and Synthetic Evidence

| Artifact | Git blob of the reviewed private file |
| --- | --- |
| [wall_owner_two_attainer_obstruction.py](../../devtools/wall_owner_two_attainer_obstruction.py) | `80fa1343a412ac92fe0fa7587dc4d60702c6a020` |
| [test_wall_owner_two_attainer_obstruction.py](../../tests/test_wall_owner_two_attainer_obstruction.py) | `cfe4a4716bc9d776565cfc7cd36fead96846e4fa` |

Both hashes were checked against Sol’s final freeze.
The independent review ran only the twelve synthetic tests, using the project Python
3.14 environment from `packing/`:

```text
.venv/bin/python3 -m pytest -q /private/tmp/n11-two-attainer-prep/test_wall_owner_two_attainer_obstruction.py
12 passed in 4.44s
```

Sol separately reported twelve controls passing in 0.33 seconds, Ruff check and
format-check clean, and BasedPyright with zero errors or warnings.
This review inspected the complete module, focused tests, and the reused strict-dot,
polygon-SAT, square-SAT, corner-selection, source-binding, and atomic-output interfaces.
No shared file changed.

## Mathematical and Source Contract

The CLI accepts only the endpoint, wall, and exp153 receipts, with expected source/blob
arguments, its own clean revision, a fresh output path, and one deadline.
The endpoint authority is fixed to the retained exp143 blob; the existing loaders
validate the complete geometry and wall provenance.
The exp153 parser binds its authority chain, selected tuple, scale, complete 188-row
first-empty prefix, axes and labels, and the two fixed component/vertex identities.
Earlier exp149/151 references are retained as exp153 source-chain fields; the new proof
does not claim to reload their geometry.

Only two original-D domains are reconstructed: right row 0, u_max, component 0, vertex
1; and left row 187, u_min, component 0, vertex 0, also its v_max attainer.
Reconstruction uses the four selected wall patches and five original dots.
It checks component counts, exact vertices, projected extrema, the shared left attainer,
and positive-area component means.
There is no sixth dot, alternative axis selection, attainer sweep, or second candidate.

The x-radius formula `h*(abs(u.x)+abs(u.y))` has the correct orientation dependence.
The limit gap is right minimum x minus left maximum x and is independently compared with
explicit core vertices.
A nonpositive gap completes only the negative branch for this frozen positive-limit-gap
x-axis construction.
It does not test other separating axes or other pairs.

For a positive gap g, the source uses the contracted single common coefficient:
`epsilon=1/2` when horizontal movement bound M is zero, otherwise `min(1/2,g/(2*M))`.
Full-dimensional convex component means are interior, so the positive interpolation is
interior; the bound preserves gap at least g/2. Independent replay then checks the open
container, every original closed dot, every selected closed patch, and strict
square-square SAT. These final geometric replays are necessary even though the
perturbation has an analytic margin argument.
A failed replay or inconsistent radius/extremum is invalid, not a scientific refutation.

## Controls and Corrected Receipt Semantics

The focused controls cover the oblique `(3/5,4/5)` radius and positive pair, real strict
replay through the selected patch path, zero and negative gaps, M=0, both positive-M
coefficient branches, exact attainer reconstruction, closed dot and patch tangencies,
changed source chain and prefix, pre-replay expiry, replay failure, and expiry after
successful SAT.

The consequential review correction is present: constructed candidates no longer count
as verified strict escapes.
In partial or invalid results their centres are labelled `candidate_centre`,
`strict_replay_verified` is false, and the summary’s verified escape count is zero.
Complete acceptance alone sets the strict-obstruction flags.
The post-SAT expiry retains the computed gap and separator while withholding acceptance.
These semantics are conservative even when some geometric checks completed before
expiry.

## Deadline and Output Scope

One internal clock begins after input loading and covers patch preparation, both domain
reconstructions, gap construction, the single perturbation, strict replay, and the
terminal acceptance check.
Its default is 90 seconds.
Checks occur around the coarse geometry calls; a long individual decomposition is
cooperatively checked when it returns.
The external 120-second process guard plus two-second termination grace must therefore
remain part of any future protocol, covering input loading and serialization as well.

Atomic JSON is written after the computation returns, including cooperative partial
returns. There are no incremental target checkpoints.
An external kill can leave no receipt; process status and absent output must be retained
honestly. No deadline or invalid path acquires an accepted mathematical result.

## Claim Limit and Adoption

A positive future result would establish two disjoint strict D-missed cores in the
selected four-patch relaxation.
Analytically, every nonnegative added measure covering both must supply at least two
units of mass.
With all five original unit atoms retained, this forces nominal total mass
at least seven. The receipt explicitly leaves the available-mass conclusion after
occupied-union banking conditional on a separate original-site outside-union premise.
It does not claim realizable unit parents, joint physical owners, a packing, a global
bound, or any change to T023.

The receipt phrases the elementary unit-dot special case as requiring distinct
additional unit atoms; fractional added measures are governed by the mass statement
above. It does not require arbitrary fractional covers to consist of unit atoms.

No consequential source blocker remains.
Adoption should retain the reviewed bytes and normal repository validation.
If the private test import is adjusted to the repository module path during adoption,
record that mechanical change and rerun the focused controls; this GO does not certify
an unreviewed geometry change.
The target remains **unrun**.

### Repository Adoption

The adopted module retains blob `80fa1343a412ac92fe0fa7587dc4d60702c6a020`. The test
imports the module through `devtools`, with imports sorted by Ruff; its adopted blob is
`eec38c51f5af55241800fe0040f90f1449145791`. This is the only change from the reviewed
private pair. The twelve focused controls passed in 2.21 seconds after the import
adjustment. Ruff check and format-check pass, and BasedPyright reports zero errors,
warnings or notes.
These checks concern the instrument and synthetic controls; the target
remains unrun and no new numbered experiment has been registered.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
