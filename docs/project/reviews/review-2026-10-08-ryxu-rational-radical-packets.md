# Review of the ry-xu Rational and Radical Packing Packets

Reviewer: independent strong agent, GPT-6 Astra, xhigh.
Reviewed on 2026-10-08 UTC (2026-10-07 in the host’s America/Los_Angeles timezone).
Scientific checkpoint: `5abc1b327d5a3bdbf14f128ff7b176e6abdb64d0`, with the replay
normalization and source-count wording corrections described below.

## Decision and Scope

The reviewed arithmetic, complete source inputs and retained decisions support finite
feasibility for the 25 rational constructions and the separate undilated 51-square
construction. Production house construction, private-worker recovery, frontier adoption,
source-snapshot size and final assurance expression require their own integration gates.
This review does not authorize those gates to be skipped.

The source’s claim of 191 touching pairs for the undilated n=51 construction remains
unconfirmed. Both reviewed exact implementations count 119 touching pairs and 1,156
strictly separated pairs, covering all 1,275 unordered pairs.
This discrepancy does not invalidate the independently checked feasibility claim.
Neither route establishes optimality, novelty, rigidity, local minimality or the history
of the source’s search.

Credit for the constructions belongs to ry-xu.
The primary sources are [issue #432](https://github.com/jlevy/squares/issues/432) and
[the immutable source tree](https://github.com/ry-xu/square_packing/tree/8dc415296f697f5140caea27c7a0193d52deb4e6).
The source describes an LLM-assisted search.
No upstream producer or checker was executed for this review.

## Rational Source and Geometry

The complete roster is 51, 70, 84, 86, 88, 102, 103, 105, 108, 123, 126, 127, 129, 130,
131, 146, 153, 175, 179, 236, 258, 261, 263, 267 and 295. Superseded cases remain in the
packet; current frontier selection must compare exact sides independently.

The reviewer compared every retained original certificate string with the acquired file,
its pinned SHA-256 and the immutable source tree’s Git blob identity.
All 25 matched byte for byte.
The acquisition boundary is implemented in
[`ryxu_arrangement_reports.py`](../../../packing/devtools/ryxu_arrangement_reports.py),
with original factual inputs in the
[source packet](../../../packing/resources/web/ry-xu-new-packings-2026-10-08/README.md).
The parser rejects duplicate JSON keys, missing or extra fields, wrong counts,
incomplete square rosters and unsupported scalar or angle syntax.

For each exact rational half-angle parameter t, the conversion uses c=(1−t²)/(1+t²) and
u=2t/(1+t²). The denominator is positive and c²+u²=1 exactly.
Rotating each corner (±1/2, ±1/2) by this basis produces a unit square with the source
centre.
Native centre/basis materialization and the separate rational corner checker then
decide containment and every unordered pair using exact separating axes.
The half-angle conversion is shared between the two routes and was reviewed as a shared
boundary; their geometric deciding implementations are distinct.

The input uses the source’s exact rational side and all centres and half-angle values.
The source certificates already include their stated dilation.
The importer applies no further dilation.
The printed decimal ceiling does not determine the admitted side; `confirmed_bound`
computes an upward decimal rendering from the exact rational value.
The rational n=51 certificate remains separate from the undilated radical construction.

The retained batch contains 75 full-roster jobs and 150 complete native outcomes: 25
positives, 25 duplicated-square controls and 25 outside-container controls.
The receipt reports 2,078,082 pair decisions and 330.19143345800694 seconds for the
producer’s two-worker run.
The reviewer admitted all 75 jobs against reconstructed full inputs and the exact native
result contracts.
Every positive passes both routes; every control fails both routes with
the required negative pair or wall diagnostic.
The reviewer did not repeat this entire rational batch.
The underlying rational kernel was independently replayed for all three #399
certificates in its separate review.

The fast receipt check validates complete source/control input equality, exact result
field sets, both route identities, rational fields, scope limitations, full pair counts,
verdicts and diagnostic signs.
It does not recompute every diagnostic magnitude.
`check --replay` compares the full freshly computed native outcomes, excluding measured
CPU and wall times.
Git retains the reviewed complete receipts; a structural admission is
not described here as a fresh geometric execution.

## Undilated n=51 Arithmetic and Source Binding

The source root `square_packing_records.json` is 340,048 bytes, with SHA-256
`93130ffb2f9da1b15ba5e8e491e60509192d6fb21108aa2adc86d29c4f071e5d`. The entire selected
51-square record equals the retained fact, whose canonical JSON SHA-256 is
`bf744f8b9b41776cabe43eb46c2e45293fbfe3803eb47578de878c61509357e0`. The reviewer checked
both equality and the original root blob’s source-tree identity.
The full source root’s size must not be confused with the selected record’s size.

[`ryxu_radical_n51.py`](../../../packing/devtools/ryxu_radical_n51.py) uses the exact
fields for all 51 centres and accepts only angles 0 and π/4. Rounded source fields are
retained as source facts and do not decide geometry.
The closed expression parser uses rational strings and specified linear expressions in
√2; it never evaluates source code.

The independent scalar is a+b√2 with a and b rational.
Addition and multiplication use (√2)²=2. Equal-sign coefficients have that sign.
For opposite signs, comparing a² with 2b² and multiplying the comparison by sign(a)
gives the exact sign of a+b√2. No nonzero rational coefficients can make a²=2b². The
native route separately uses the irreducible polynomial x²−2 and isolating interval
(1,2), selecting the positive root.

Axis-aligned corners are the centre plus (±1/2, ±1/2). Diamond corners are the centre
plus (0, ±√2/2) and (±√2/2, 0). Their consecutive edges have squared length one and
oriented determinant one.
The independent route checks those identities, all corner wall clearances and all 1,275
pairs. For each pair it takes the maximum directional projection gap over the edges of
both squares: negative means interior overlap, zero means touching, and positive means
strict separation. Including opposite edges adds redundant axes without changing that
decision.

The admitted side is (16+5√2)/3. Substitution gives 9s²−96s+206=0. This polynomial and
the source coordinates describe a feasible construction; they do not assert equality
with the minimum packing side s(51).

## Fresh Radical Outcomes and the Contact Discrepancy

The reviewer executed the three full radical jobs and compared canonical JSON for
complete inputs and both outcomes against the retained evidence.
All bytes matched these frozen outcome SHA-256 values:

| Job | Complete outcome SHA-256 |
| --- | --- |
| positive | `2170142ecd3e1065a038ad5d1eb38c7f53951d7f9fad6851a34f729ba9b249a2` |
| duplicate-square-overlap | `65dfc3caaf99e148f0a49dfd61702c8b95397cd5e88a17d9413899f83685dc4e` |
| square-translated-outside-container | `02a31fcac9651ffbc3b0a6dab329675c1e2cdecdf263d92c5327b37331a6c0cc` |

Both controls retain 51 squares and test all 1,275 pairs in each route.
The duplicate control replaces the second square by the first.
The outside control translates the first centre by the full side plus two.
The retained number-field decimals are diagnostic renderings; the complete coefficient
pairs remain the exact deciding input.
The full outcome hashes protect every retained diagnostic and metadata field across the
private-worker custody boundary, in addition to the reconstructed input comparison.

A second native positive execution returned 119 touching pairs, 1,156 strictly separated
pairs, 1,275 tested pairs and 52 corner-coordinate incidences on container walls.
The independent rational-pair route also returned 119 touching pairs.
The 52 is a separate corner-coordinate count and does not explain 191. The source
explicitly reports 191 touching pairs and says its exact checker is available on
request, rather than in the repository.
No equivalent alternative definition has been established.

The native count is reproducible from the retained complete input with project Python
3.14, from `packing/`:

```python
from devtools import ryxu_radical_n51 as radical

side, poses = radical.inputs("positive")
_, report = radical.exact_verify(radical.witness(side, poses))
print(report.valid, report.pairs_tested, report.touching_pairs,
      report.strict_pairs, report.container_contacts)
# True 1275 119 1156 52
```

## Findings and Verification Record

**R1: replay comparison rejected valid negative outcomes.** The documented
`python -m devtools.ryxu_radical_n51 check --replay` failed at the scientific
checkpoint. Native failure entries were Python tuples; retained JSON entries were lists.
The positive compared equal directly, and both negatives compared equal under canonical
JSON with their frozen hashes unchanged.
The correction compares canonical JSON of the entire fresh and retained outcomes.
It preserves full-field comparison and source/input binding.
An actual duplicate-square replay regression covers this serialization boundary.
The corrected documented command replayed all three full jobs and exited 0.

**R2: unsupported explanation of the source contact count.** The initial packet README
called the source’s 191 a different contact statistic.
The reviewed correction states that 191 remains unconfirmed and is not used to admit
feasibility.
The record must preserve that distinction when expressing T126 or an adopted
case.

Review logs are under the external task review directory:

- `ryxu-source-custody-audit.log`: all 25 complete source inputs, immutable blob checks,
  selected radical source equality and 75 full receipt contracts; exit 0
- `ryxu-radical-replay-diff.log`: all three fresh canonical outcomes equal retained
  outcomes, full outcome hashes and native contact roster; exit 0
- `ryxu-radical-replay.log`: reproducible pre-fix tuple/list failure
- `ryxu-radical-replay-fixed.log`: documented-command verification of R1; exit 0
- `ryxu-focused-tests.log`: both scientific test modules, 40 passed in 4.23 seconds; the
  actual negative replay regression took 3.51 seconds, below the unchanged 12-second
  per-test ceiling

The producer’s recorded 18.707450165995397 seconds covers its original three radical
jobs and 7,650 pair decisions; it is not the reviewer’s wall measurement.
No claimed source search result, source program output or contact count substituted for
an independently evaluated geometric predicate.

## Exact Presentation API Review

The presentation changes were reviewed on the working patch over
`e49f3417a7eea2fe89b6f29b862677f76a33105d`, before the production-adoption freeze.
`materialize_exact_witness` exposes the existing exact parser and pose expansion.
It performs no packing predicate and assigns no assurance.
The atlas renderer keeps rational coordinates as `Fraction` identities.
For number-field coordinates and the side, it retains the reduced coefficient vector and
the entire declared field polynomial and root-isolating interval as the exact identity;
the field’s decimal projection is used only for drawing.
This is an appropriate separation between exact source representation and display.
The materializer docstring records that boundary, and callers that decide feasibility
still use the exact verifier.

The reviewer independently compared every corner of the complete n=51 input against a
direct rational-pair axis/diamond construction and every corner of the complete n=70
input against direct `Fraction` pose expansion.
The test also checked that changing the selected algebraic root changes both the exact
identity and projection, that the numerical n=52 route remains numerical, and that none
of the three input dictionaries changes.
Packing predicates and margin computation were replaced with immediate failures during
this reproduction; none was called.
The reproduction passed in 0.181 seconds, recorded in `ryxu-presentation-api-review.log`
in the external review directory.

Three source tests were independently run with project Python 3.14.7:
`test_exact_radical_projection_keeps_all_coefficient_geometry`,
`test_rational_center_basis_corners_remain_exact`, and
`test_radical_upward_display_is_strictly_outward`. **All three passed in 1.10 seconds.**
The first also checks that low ambient Decimal and mpmath precision neither changes the
rendering nor leaks a changed precision context.
The third proves the displayed radical ceiling is outward by exact order and is the
smallest decimal at the selected precision with that property.
The log is `ryxu-presentation-tests.log` in the external review directory.

No presentation defect was found in this reviewed scope.
This acceptance does not close production adoption: complete metadata for all eighteen
selected houses, actual private-worker admission and mutation refusals, preservation of
earlier source packets, final storage admission and the final record expressions remain
separate gates. The new worker regression must retain a bounded subprocess and check the
unchanged storage ceiling before copying; that pre-freeze feedback was sent to its
owner.

## Production Integration Findings

**R3, Medium, open: historical custody is saved after case mutations.** In
`register_ryxu_reports.record_cases`, each frontier file is saved before the remaining
roster is checked and before the complete original history is archived.
An independent isolated reproduction supplied a valid first case, n=51, followed by a
non-improving n=70 bound.
The function refused n=70 after changing n=51, while the history file did not exist.
A subsequent run would skip the already selected n=51 case.
The existing-history refusal also occurs after these writes.
This is an importer recovery defect; no corruption of the currently retained eighteen
historical records was observed.

**Fix:** build and validate the complete adoption plan and history custody boundary
before changing any frontier file, retain the complete original history before the first
case write, and allow an interrupted run to resume from that immutable history.
A later-case refusal should leave every frontier byte unchanged.
The confirmed reproduction is retained as
`ryxu-adoption-history-preflight-confirmed.log` in the external review directory.
The first reproduction stopped at the fixture’s output guard; the confirmed run
correctly rooted that guard in the fixture and reached the stated failure.

The reviewer also requested a fresh refusal after corrupting a private scientific input
inside the actual production worker, using the same clone as its positive and producer
checks. The fixture mutation tests alone do not demonstrate that final copier boundary.
The worker test now has a 45-second subprocess ceiling and checks the unchanged storage
cap before and after copying; those two corrections were inspected.
Final custody acceptance remains pending the complete worker result and correction of
R3.

## Full Production Integration

**Decision: accepted.** This acceptance covers source checkpoint
`609038af757cf364bac38467d861b1ac7061d9a7`: the eighteen complete house views, private
scientific custody, guarded production outputs and recoverable adoption.
The scientific modules and deciding inputs remain those reviewed above; this checkpoint
adds production integration rather than a new geometric assertion.
Final confirmation records and their reader-facing expression require a separate check.

The current house roster is 51, 70, 84, 86, 102, 103, 105, 108, 123, 126, 127, 129, 131,
146, 175, 261, 267 and 295. Each complete house is reconstructed from admitted source
facts and actual native results, including its entire side, pose, field declaration,
source, claim and certificate metadata.
The n=51 unit coefficient pair is normalized to the schema’s literal unit; its field,
side and all source poses remain exact.
Only the public house identifier changes in its retained native positive result.
The rational n=51 construction remains separately retained.

**R3, closed:** the reviewed repair validates the complete original history and all
remaining case transformations before any frontier write.
It writes the complete immutable original history before the first case mutation and
resumes an interrupted adoption against that same history.
It refuses an incomplete history, a selected prefix without its original history, and a
changed unadopted original.
The reviewer independently ran the later-case preflight refusal, interrupted-write and
retry, and incomplete-history controls at the frozen checkpoint.
All three passed in 93.35 seconds under external-volume I/O contention; their test calls
took 4.25, 8.81 and 0.02 seconds respectively.
The remaining wall time included fixture setup and teardown.
The receipt is `ryxu-adoption-history-fix-review.log` in the external review directory.

The reviewer inspected the actual production-worker regression and its completed
receipt, `actual-private-worker-v6.log`, under the writer’s external production task
directory. The writer ran that test at the frozen checkpoint: one passed, 62 deselected,
in 406.23 seconds. The preserved worker contains all eight required private inputs as
ordinary files with byte-for-byte source equality: rational facts and all 75 deciding
jobs, radical facts, all three complete radical job receipts, house metadata and
original frontier history.
The child process admitted all eighteen current houses, the earlier #425 thirteen-job
custody index and all nine earlier #422 constructions.
It refused both selected and whole-atlas producers without changing their output
manifests. It then corrupted a rational pair count and a radical deciding gap in the
copied receipts, refused each mutation, restored the original bytes and admitted the
houses again. This was the actual production clone, not only a fixture approximation.

The child retained its 45-second timeout, and the complete clone regression passed the
unchanged source-size ceiling before and after copying.
The writer’s post-test, review-document-inclusive measurement was 200,722,177 bytes
against 201,326,592 bytes, leaving 604,415 bytes before this closure addendum.
After adding this closure, the reviewer independently compared all eight
preserved-worker inputs with the source: every file was ordinary and byte-identical.
The same command measured the current working snapshot, including the confirmation
draft, at 200,745,688 bytes, leaving 580,904 bytes.
The owner must remeasure the final checkpoint if later integration changes its contents.
The 406.23-second whole-test wall time is not evidence that the test meets the fast
lane’s 12-second per-call ceiling; final test selection and CI results remain separate
operational gates. No cap, deadline or acceptance criterion was raised for this review.

This closes the production prerequisites for finite-feasibility confirmation at V3/C3
only. It does not establish the source’s 191-touching-pair assertion, optimality, local
minimality, rigidity, novelty, human review or a C4 claim.

## Final Presentation and Record Review

A separately prompted strong reviewer accepted the final presentation and record changes
at `fb5309b258e10e5f56201620dbc06f0afc633380` on 8 October 2026 UTC. This is a scoped
follow-up to the scientific, API and production decisions above.
Those decisions and their limits remain unchanged.

The contact census and workbench expand the complete exact poses before projecting them
for display. Workbench matching keys retain the scalar declaration, algebraic field and
selected root, coordinate convention, side and source pose.
Rational regularization uses the exact expanded corners; number-field regularization
refuses before attempting a rational parse.
The existing numeric and rational-corner workbench paths remain in place.

An independent read-only audit loaded all eighteen selected workbench constructions and
checked their complete square and key counts.
Exactly seventeen are rational and one is the separate undilated radical n=51
construction. Each source override points to the reported construction evidence; each
verified upper lane points to the separate feasibility evidence.
Their upward ceilings agree, and every case remains open.
All twenty-five rational source certificates remain retained, including the eight not
selected in the current atlas.

The review found and closed three expression issues: stale final-selection counts,
historical prose referring to displaced frontmatter values, and five obsolete
certificate-gap blockers.
The corrected text distinguishes the eighteen rational improvements over the pre-intake
frontier from the final seventeen rational selections alongside radical n=51.

The blocker correction removes only the earlier Evan Daniel certificate-print gap after
mapped ry-xu confirming evidence and matching reported/verified upper values and exact
forms are present. An independent comparison against the complete original history found
exactly five such dispositions, at n=127, 175, 261, 267 and 295. All eighteen reported
and verified lower lanes and all other blockers were unchanged, including the separate
missing Green lower-proof blocker at n=261. The old complete records remain in the
immutable history.

The reviewer ran the exact-pose and historical-prose controls: two passed in 1.21
seconds, with the pose call taking 0.15 seconds.
After the blocker correction, the historical and real-history n=261 controls both passed
in 1.19 seconds; the blocker call took 0.18 seconds.
The complete workbench/routing audit took 0.97 seconds, and the final history/blocker
audit took 0.556 seconds.
The writer separately ran the full n=51/n=70 workbench projection, alternate-root
identity and unchanged n=52 numeric-path control; that recorded run passed in 1.27
seconds.

`git diff --exit-code 609038af757cf364bac38467d861b1ac7061d9a7` over the
rational/radical scientific modules, house-binding module, full source facts and actual
`receipts/` directory returned 0. This follow-up did not repeat the geometric batch or
the actual private-worker run accepted above.
Final source-size and exact-head CI checks remain integration gates.
The source’s 191-touching-pair assertion remains unconfirmed; the review establishes no
optimality, local-minimum, rigidity or novelty claim.

## Consumer Integration Review

A separately prompted strong reviewer accepted the consumer changes in `f0c28d610`,
their normal integration at `fc0cc69e206bf7785561751f80005a253bb077cf`, and the
subsequent reported-stage fixture correction.
This review covers source routing, diagnostic projection, generated consumer records,
and presentation. It does not repeat the native source campaign.

The diagnostic pose reader materializes complete rational and number-field centre-basis
witnesses before converting them to floating poses.
It preserves the declared field and root through the maintained materializer and makes
no feasibility decision.
Independent n51 and n70 controls compare every projected centre and angle with the exact
source and forbid the geometry decider.
Existing corner and angle representations remain supported.

Historical generator and citation controls now read the complete pre-intake records.
The displaced n105 refinement fixture also retains its complete old house and private
metadata. The Göbel strip checker compares n84 with that strip’s historical side; its
exact five-size construction and negative controls remain the subject of the check.
It does not relabel the smaller selected n84 packing as Göbel’s construction.

The revised #422 worker control first refuses the current n108 house against the old
#422 receipt. It then writes the complete retained historical house to an ordinary
private path and runs the unchanged whole-house reader over all nine old constructions.
It restores the path selector before checking other artifact reads and producer output
guards. Complete input coverage, native-result binding, mutant/restoration controls, and
the worker’s existing deadlines remain required.

An independent bounded audit admitted all 27 #422 deciding inputs and eight current
houses with every geometry decider forbidden.
It refused current n108 and schema-loaded the complete historical n108 house, whose full
geometry and private metadata exactly matched the admitted old source.
This audit did not create the production worker clone; the revised actual-worker control
still requires hosted execution.

The frontier table uses one closed-form display predicate for both lines.
Long rational bounds use compact decimal presentation while preserving the complete raw
fraction in a title and leaving the source record unchanged.
Integers, radicals and polynomial-root forms keep their prior semantics.
The n51, n70 and n108 rows are now included in the four-width browser sample.

Source cards and citations retain finite construction scope.
The chunk, family, contact and evidence-profile records reflect the selected houses,
including the radical n51 interior tilted components.
Their sensitivity and outlier information remains present; the descriptive diagnostics
grant no exact rigidity or optimality claim.
The slow-marker roster names the previously measured full-worker and confirmation
transactions without raising the fast-call or child-process ceilings.

Independent controls passed: three rendering checks in 7.09 seconds; nine exact
projection, historical refinement, refusal and taxonomy checks in 6.66 seconds; and
three profile regeneration, sensitivity and contact-gallery checks in 1.20 seconds.
The final three-line fixture correction resets only the simulated reported-stage
rigidity to `None`; the confirmation’s no-promotion, lower-lane, complete-history and
idempotence assertions remain intact.
The writer’s explicit bounded transaction passed in 19.56 seconds, with a 17.95-second
call, recorded in `ryxu-432-gate-evidence/confirmation-hosted-failure-control-v25.log`.

The ry-xu rational, radical and house-binding modules and complete ry-xu packet have no
diff from the accepted `dc8f15cf3` scope; source facts and deciding receipts remain
unchanged from `609038af757cf364bac38467d861b1ac7061d9a7`. Final hosted fast/full checks
and the post-integration private-copy size remain release gates.
This closure does not confirm the source’s 191-contact assertion or promote optimality,
local minimality, novelty, human review, or C4 assurance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
