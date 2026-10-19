# wand125 Tools: Mathematical and Admission Review

The new repository publishes search machinery around Tokoharu’s rectangle-density
certificates, plus a separate exact point-and-threshold checker.
Its source supports reusing the existing rectangle proof contract.
Two claims need qualification before we adopt the tooling: the general
$B\thinspace UB(n)$ ceiling omits an orientation condition, and `scale_and_verify.py`
can announce a packing bound without checking the target count’s mass budget.

The disputed ceiling is tracked as **T-058**. The separately reported equality of the
n11 row scans is **T-059**.

## Assigned Result Classifications

The [result register](../../../packing/frontier/results.yaml) assigns each imported
claim the same
[verification, confirmation and significance scales](../../../epistemics.md) used for
this project’s results.
Verification describes the evidence supporting the whole claim; confirmation describes
this repository’s recorded work.
Significance is a separate judgment and does not raise either evidence level.

| Claim | Significance | Verification | Confirmation | What remains |
| --- | --- | --- | --- | --- |
| T-058: unrestricted $B\thinspace UB(n)$ ceiling | S2: a tooling limit whose premises affect safe search, with no new packing bound | V0: the unrestricted claim is unestablished | C1: source-level review found a missing premise | Discharge angular alignment and exact upper-witness assumptions, or use the reviewed sufficient correction; think-xgjo. |
| T-059: equality of all 12,028 n11 row minima | S2: a citable row-checking result that changes no existing theorem | V0: no retained complete replay supports the equality claim | C1: source-level review found journal-admission defects | Replay all unique rows with exact witness comparisons and retain the full journal; think-11z6 under think-190a. |

Both are attributed to the published wand125 source and classified
`previously-published`. The register retains each significance rationale, assessment
date and scorer. The three sampled row replays do not confirm the full equality, and the
existing complete native proof of the n11 bound is a different claim.
Search speedups and alternative verifier implementations remain implementation
obligations in the component table below; no measured speedup or independent full-domain
acceptance is inferred from these two ratings.

This is a W2 factual review of
[wand125/square-packing-tools at `0d33ab61726c2ab03e3eb8f457dabaf22db8571f`](https://github.com/wand125/square-packing-tools/tree/0d33ab61726c2ab03e3eb8f457dabaf22db8571f),
retrieved on 2026-09-29. The admission defect was reproduced with the unchanged upstream
checker, and three n11 row scans were replayed.
The ceiling findings are source inspection and mathematical derivations.
The
[PR review comment](https://github.com/jlevy/squares/pull/246#issuecomment-5886292553)
records the intake findings and their initial dispositions.
No complete replay of the 12,028-row claim or reproduced speed measurement is claimed.
The [existing rectangle review](review-2026-09-22-tokoharu-density-mathematics.md)
supplies the detailed continuous coverage argument.

## What the New Claims Establish

| Component | Claim and proof obligation | Review disposition |
| --- | --- | --- |
| Transfer to another $n$ or $L$ | Reuse support and re-optimize weights, then prove coverage and the new exact budget | Valid architecture; transferring support alone proves nothing about the new target |
| Budget recovery | Add or move rectangle columns and repair screened violations before final verification | Search operation; requires a fresh proof at the final geometry and mass |
| Weight rescaling | Multiply nonnegative weights by an exact positive factor; coverage and mass scale linearly | Valid identity; final budget and coverage must both be checked |
| $B\thinspace UB(n)$ ceiling | Pack $n$ disjoint checked cores into the container and sum their coverage | Valid for a packing whose orientations belong to the checked net; unrestricted statement has a missing premise |
| Working rows, cached bases, batched screens | Produce useful candidates faster | Outside the proof path when final full verification is mandatory |
| Cached-axis C++ checker and lazy zmx2 | Preserve verifier behavior while changing evaluation work | Separate implementation claims; source provenance and full-domain comparison required |
| General pose tree | Reproduce 12,028 n11 per-row minima with exact arithmetic | Reported upstream result; global counting argument and local replay remain separate obligations |

The source’s
[provenance table](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/solver/PROVENANCE.md)
identifies Tokoharu’s upstream commit `84bebef51856d46a19c145b035664324ba9572d3`. We
also compared Git blob identities of `solver/verify.cpp` and the previously retained
Tokoharu source: both are `9a64c606d9dd76843d06b4f120038df7d167606b`. This establishes
source identity for the checker, not a new replay result.

## Ceiling: Account for the Angular Net

[`l_cap.py:17–23`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/transfer/l_cap.py#L17-L23)
argues that a packing of unit squares at side $U=UB(n)$, scaled by $B=9977/10000$,
provides $n$ disjoint cores each charged at least one.
The checker establishes that coverage for side-`B` squares at the 201 angles
$\theta_r=2\arctan(83r/40000)$, modulo container symmetries.
Its extension to arbitrary orientations applies to *unit* squares, through containment
of a nearby net core.
It does not establish the same coverage for arbitrary orientations of side-`B` squares.

Thus the stated argument proves a ceiling at $BU$ when the witness packing’s
orientations belong to that net, modulo $D_4$. Axis-aligned grid packings satisfy this
condition. A general freely rotated packing needs an additional containment allowance.
This is a gap in the stated ceiling argument; it is not a counterexample to a published
rectangle certificate.

A sufficient general ceiling follows from the existing nearest-angle calculation.
Put $D=83/40000$ and

$$
\alpha=B(1+D)=\frac{399908091}{400000000}=0.9997702275.
$$

For every orientation, a nearest checked angle has discrepancy $|\delta|\le\arctan D$. A
concentric side-`B` core at that angle fits inside a square of the original orientation
and side $\alpha$, since $B(\cos|\delta|+\sin|\delta|)\le B(1+D)=\alpha$. Scale a
certified packing at side $U$ by $\alpha$, and place this net core inside each scaled
square. Their interiors remain disjoint, and each core is contained in the container.
For a nonnegative rectangle density, boundaries have zero mass, so checked coverage
implies

$$
M\ge \sum_{i=1}^{n}\int_{Q_i}g\ge n.
$$

Consequently a mass budget below $n$ is impossible at $L\ge\alpha U$. This bound is
sufficient, not necessarily sharp.
If the exact witness orientations are available, their individual net discrepancies can
give a smaller common scaling factor.
The checker’s stronger threshold $10001/10000$ only strengthens the mass contradiction.
Smoothing is unnecessary for this argument about the unsmoothed rectangle density.

The numerical table is another limitation.
The
[UB data](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/transfer/data/ub.json)
contains rounded display values, and `l_cap.py` uses only those floats.
For example, the n26 value $5.62132$ is below $7/2+(3/2)\sqrt2$, and the n29 value
$5.933833$ is below the rational witness side recorded in the same table.
These values are not certified outward bounds.
Some `ubExact` entries instead contain coarser integer bounds.
Treat the current three-decimal output as a search suggestion.
A proved ceiling needs a validated witness, its exact side or outward enclosure, and the
appropriate orientation allowance; rounding the answer down does not establish
impossibility above that rounded value.

## Rescaling: Coverage Acceptance Does Not Check the Budget

[`scale_and_verify.py:27–39`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/transfer/scale_and_verify.py#L27-L39)
defaults to target mass $28.9$, verifies only that the old mass is smaller, and rescales
the weights exactly.
It calls `certify.py`, then
[prints a bound for the candidate’s `n`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/transfer/scale_and_verify.py#L63-L79).
It never requires the new mass to be below that $n$.

The called
[`certify.py`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/solver/certify.py)
checks the support, nonnegative weights, angular margin, interval input, and all 201
coverage cases. It records exact mass but does not compare it with a target count.
Therefore its successful coverage result cannot supply the missing budget premise.
For a candidate whose $n$ is below the requested target mass, the wrapper can announce a
bound unsupported by its own checks.
An executed negative control confirms the defect.
We supplied $n=1$, $L=1.5$, $B=0.9977$, and a rectangle on $[0.001,1.499]^2$ with
initial mass $1/2$. The wrapper scaled its mass to the default $289/10$, the unchanged
C++ checker verified all 201 directions in 209 nodes, and the wrapper exited
successfully while announcing `certificate for s(1) >= 1.5`. This bound is false because
$s(1)=1$. The coverage result is valid; the missing mass-budget premise invalidates the
announced packing bound.

The
[receipt](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/admission-control.json)
retains the exact mass, source revision, verifier identity, and complete direction
count. The
[run log](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/admission-control.log)
retains the false announcement.
Reproduce it with the durable
[audit tool](../../../packing/devtools/audit_wand125_tools.py), from `packing/` with the
task’s external scratch environment configured:

```bash
uv run --frozen python -m devtools.audit_wand125_tools \
  /path/to/pinned/square-packing-tools \
  --scratch "$TMPDIR/wand125-admission-control" \
  --out resources/web/wand125-tools-2026-09-29/receipts \
  --timeout 60
```

The scratch directory must be new or empty.
The tool requires the pinned source revision with no tracked modifications and records
the upstream output as a negative control, never as a packing certificate.

The separate
[`rectangle_rescue.py`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/solver/rectangle_rescue.py)
does check $0<M<n$, binds geometry and candidate bytes to the proof artifacts, checks
all 201 direction records, and compares the resulting verifier source with its selected
snapshot. `ladder/rung.py` calls that guarded path.
The finding is specific to the unprotected scaling wrapper; it does not establish that
the ladder admits the same mistake.

Required integration controls are an explicit integer target count, exact recomputation
of mass, a strict $M<n$ check, equality of admitted and proved $L$ and $B$, complete
direction coverage, and source-bound replay artifacts.
Test a wrong count, an over-budget rescaling, stale geometry, a missing angle, and a
substituted checker.
A successful process exit or a `VERIFIED_CONTINUOUS_DENSITY` label alone is
insufficient.

## Independent Verification and Follow-Up

For rectangle certificates, the existing independent rational preflight verifies the
data conversion, mass, support, symmetry multiplicities, angular containment margin, and
axis event set. The retained external-certificate replays still depend on Tokoharu’s C++
checker for complete nonzero-angle coverage.
Replaying identical C++ through another wrapper is independent of the search, but not
independent of that checker’s implementation.

An independent rectangle checker must enclose every translated overlap over the full
legal centre domain at every net angle, or check a complete subdivision certificate with
independently derived leaf bounds.
It also needs exact input binding, outward arithmetic, termination that refuses
unresolved cells, and the same final continuous-angle and mass argument.
Agreement on sampled centres cannot replace that coverage proof.
Retain the present C++ replay while developing this second route; do not label the
existing preflight a complete independent rectangle replay.
The new [native prototype](../../../packing/src/sqpack/rectangle_density.py) implements
that separate route using exact clipping and common-core bounds, under its
[reviewed contract](review-2026-09-29-native-rectangle-contract.md).
It has completed an analytic control, but its retained n11 probe is inconclusive.

The new
[`general_pose_tree` report](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/general_pose_tree/README.md)
concerns points and threshold charges.
It reports matching all 12,028 row minima of Kleddamag’s n11 certificate and explicitly
leaves the global counting argument with Kleddamag.
That is a useful separate cross-check claim.
Our production-bound
[three-row journal](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/n11-bound-sample-portable.jsonl)
and its
[summary](../../../packing/resources/web/wand125-tools-2026-09-29/receipts/n11-bound-sample-portable-summary.json)
cover rows 0, 6014, and 12027. The pinned source search returned minima matching the
reference values, and a separate exact evaluator confirmed all three attaining
witnesses. Minimality remains evidence from the source search; witness attainment alone
does not prove it. These probes establish agreement on those three rows; **T-059’s full
12,028-row census remains reported**. The identical certificate already has a
[complete native parent-core verification](review-2026-09-22-native-n11-parent-core.md),
including exact enclosures, $D_4$ folding, threshold budget and $11\Gamma>M$. Those
global premises are established evidence for the existing `V4/C4` bound $s(11) > 31/8$;
they are not missing merely because wand125 supplies a new checker.
The native threshold decision need not equal each exact row minimum, so the full wand125
minimum-equality claim still requires its own replay and exact census.
It does not verify rectangle densities or remove their current C++ dependency.

Source review found no defect in the threshold-charge boundary argument, exact four-axis
separation test, leaf enumeration, witness reconstruction, or endpoint wall enclosure
for well-formed pinned inputs.
The upstream replay harness still needs admission controls:
[`run_n11.py`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/general_pose_tree/run_n11.py)
resumes by row number without binding previous results to the certificate and checker,
while
[`summarize_n11.py`](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/general_pose_tree/summarize_n11.py)
counts duplicate rows and does not establish the exact `0..12027` census.
A complete local replay must reject duplicate, missing, stale or mixed-source rows
before it compares minima.
Our
[first-party census wrapper](../../../packing/devtools/check_general_pose_tree_census.py)
now enforces those identity and census checks, with explicit partial and complete
verdicts. Its completed local replay still covers only the three rows above.
The generic
[`Measure` interface](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/general_pose_tree/measure.py)
also silently converts coordinates with `int()` after checking duplicates; strict
exact-integer validation is needed there.
The pinned Kleddamag loader asserts integer coordinates, so this conversion concern does
not invalidate the three ordinary row probes.

The
[cached-axis checker instructions](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/performance/verifiers/README.md)
require full replay with the unchanged verifier before publication.
The
[lazy zmx2 instructions](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/performance/point_verifier_lazy/README.md)
require a whole-domain census with zero uncertified or capped roots and describe their
timings as private reported measurements.
Maintain those distinctions in our synopsis: candidate search, source replay,
independent preflight, and a second complete verifier are separate evidence levels.

## Accelerated Verifiers: Static Review

The cached-axis variant preserves the canonical rectangle summation order and the
parenthesization of interval products; nonzero-direction code is unchanged.
Its adapter pins the source and runner identities and requires fresh logs.
The existing tests check activation, hashes and freshness, but do not establish compiled
output equality. Before integration, compare the canonical and cached axis checks at
tangencies and near the acceptance threshold, retain an equality receipt, and keep the
required canonical 201-angle publication replay.

The lazy point-verifier patch leaves the pair-bound endpoint calculation in place and
avoids computing endpoints only where zero line density makes the continuum term zero.
Static inspection found no mathematical change in that optimization.
Its
[`verify.py` wrapper](https://github.com/wand125/square-packing-tools/blob/0d33ab61726c2ab03e3eb8f457dabaf22db8571f/performance/point_verifier_lazy/verify.py)
needs stronger admission checks:

- The binary digest is compared with a supplied receipt, but the receipt’s source, patch
  and builder identities are not checked against the pinned build constants.
- Expected root count and reference census are optional.
  An empty root log passes the universal zero-uncertified/zero-capped check, so the
  wrapper does not independently establish a positive complete census.
- Final acceptance uses Python `assert`; an optimized interpreter removes the exit,
  unchanged-input, whole-cover verdict, root-count and reference-equality assertions.

These are static findings, not an executed counterexample to a retained lazy-verifier
run. Integration should enforce the pinned build identities, a positive expected census
and exact reference agreement with explicit refusal branches, and test counterfeit
receipts, empty or incomplete logs, input mutation and optimized-Python execution.
The reported private n32/n45 timings and full censuses remain unreplayed here.
The follow-up is tracked in `think-xgjo`.

A subsequent GPT-6 Astra review at max thinking applied tbd’s Rust review and testing
rules to the retained `zmx2` source and lazy patch.
The patch introduces no unsafe code or FFI; each `OnceCell` belongs to one
`family_bound` call, and the pair calculation still initializes both endpoint bounds.
The zero-density singleton branch removes only an identically zero continuum term.
This remains a static equivalence review; the standalone Rust source was not compiled by
the first-party `sqsearch` Cargo gate.

The same review found a **High** integration risk in retained shell build wrappers:
[`zmx2_run.sh`](../../../packing/resources/web/evand-square-packing-2026-09-28/square-packing/s12/search/zmx2_run.sh)
pipes a build through `tail` under `set -eu` without preserving the build status, while
[`zmx2_tests.sh`](../../../packing/resources/web/evand-square-packing-2026-09-28/square-packing/s12/search/zmx2_tests.sh)
uses a text match to decide whether the build failed.
A build failure can therefore reach an old executable.
Integration under **think-xgjo** must inspect the actual compiler exit code, use a fresh
output location and bind the executable to reviewed source bytes.
The archived wrappers remain unchanged; this finding alone does not refute a retained
run whose independent provenance checks established the binary it used.

One **Medium** input-admission hardening gap also remains outside the retained input
sizes: `zmx2.rs` stores point indices with `i as u32` without bounding the surviving
point count. Above $2^{32}$ distinct points, indices can alias and the candidate sum can
count an aliased weight twice.
This is a static path analysis requiring enormous input and memory, not an executed
counterexample or a finding against the retained certificates.
A first-party importer must cap the point count or use checked index conversion before
claiming support for arbitrary parser-admitted files; **think-xgjo** tracks this
integration requirement.

## Frozen-Source Scope Audit

A further GPT-6 Astra review at max thinking checked the synopsis, verification
overview, plan, retained receipt contents, and Git identities at `03efb3702`. It found
no unsupported mathematical promotion.
The analytic 201-angle result, inconclusive external probe, 15/67 diagnostic refinement,
and 3/12,028 partial minimum replay agree with their stated scopes.
All 19 existing T-037 proof-input paths match `c183cc9`. This audit did not rerun
coverage or premise checks and does not certify the subsequent upstream merge.

A follow-up Astra-max preservation review at `cb7bc3998` confirmed the canonical claim
mapping, unchanged wand125 acceptance logic and archived evidence, and all 19 T-037
proof-input paths still matching `c183cc9`. It found no collision, lost premise, or
mathematical promotion.
This narrow merge check did not re-assess the imported Couzo/de Winter proofs or certify
the atlas regeneration.

The provisional wand125 labels T-056/T-057 in archived receipts map to T-058/T-059 after
that merge; published Couzo/de Winter claims retain T-056/T-057.

## Updated Source and Equivalence Audit

The separately retained
[source update](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/source-provenance.json)
pins `3eb08e6c675d8d5aa953cb93da049a3f3cdc6123`. Its unchanged `verify.cpp` remains the
coverage authority; the new wrapper refuses target mass outside $(0,n)$ and defaults
below n. The revised ceiling calculation uses $B(1+D)$ generally and $B$ only for
matching integer-grid upper-bound records.
All 64 current matching records satisfy the required `n <= k^2`; the selection function
should enforce that condition before accepting future records.
Rounded upper-bound inputs still make the displayed ceiling guidance heuristic.

Four focused upstream controls passed.
The retained
[wrapper control](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/fix-control-result.json)
reproduces the old admission path and the corrected refusal with a synthetic certifier.
It checks wrapper behavior only, not C++ geometry or performance.
This update does not alter the original counterexample receipt or erase its historical
finding.

An Astra review at max thinking found no new flaw in the reviewed continuum-coverage
argument at this pin.
The
[process map](../guides/verification-tooling.md#wand125-verification-process-and-independent-equivalence)
separates exact admission, interval geometry, translation-domain subdivision, the
201-direction net, strict packing budget and artifact publication.
Its arithmetic dependencies include binary64 interval operations, the rounding mode, and
compiler flags excluding unsafe floating-point transformations.
The generic certifier checks coverage without supplying the separate `mass < n` packing
premise. It also rereads the source candidate at publication, so a first-party replay
must bind an immutable candidate and verify the final artifact against the input that
was checked.

Our exact rational verifier implements different geometric bounds.
C++ combines center-area enclosures with signed derivative bounds; common-core and
per-rectangle corner minima do not exploit the same derivative cancellation.
Equivalent complete coverage and comparable speed therefore remain separate obligations.
The matched benchmark uses the exact rational value of the C++ effective binary64
cutoff, records the nominal $10001/10000$ target, and distinguishes complete, partial
and unresolved outcomes.
Neither an incomplete probe nor a complete analytic control establishes performance
parity on external certificates.
This audit concerns rectangle-density certificates; it does not confirm the T-060
global-optimality capture proof.

The paired benchmark at source SHA
`a31a41c0d87126883bc28e6ad68e96b2571c8a944b5d012afa05200b2a11c2f6` passed a separate
Astra-max review of exact threshold conversion, D4/input/domain binding, complete unique
angle census, unresolved-work refusal, source rechecks and timeout handling.
Three portable benchmark tests and two production-path refusal tests pass.
The retained
[analytic comparison](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/parity/analytic-control/result.json)
accepts all 201 directions in both engines.
The
[external angle-1 probe](../../../packing/resources/web/wand125-tools-2026-09-29/update-3eb08e6/parity/n11-angle1-feasibility/result.json)
finishes in C++ but is inconclusive in native after its 13-second internal budget.
These establish a working comparison and a specific performance gap; they do not
establish independent full external coverage or speed parity.
The process map retains the measured costs and the open effectiveness obligations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
