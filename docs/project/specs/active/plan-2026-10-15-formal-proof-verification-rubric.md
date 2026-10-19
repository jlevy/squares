# Plan and Audit: Verification of Reported Formal Proofs

**Date:** 2026-10-15

**Author:** Codex, strong tier, xhigh reasoning; implementation author, not an
independent reviewer

**Status:** Implemented; independent review and publication pending

**Workflow:** W4 process review, followed by a bounded records and validator change

**Bead:** `think-o6ou`

## Decision

Credit an inspected, retained record of a complete producer build toward verification
(`V`) without calling it an independent confirmation (`C`). The existing ladders in
[epistemics.md](../../../../epistemics.md) already allow this.
The import instructions and the explanations attached to formal reports had instead made
a build here or by a third party a prerequisite for both axes.

`T-154`, Fitzharding’s seventeen-square formalization, qualifies for **V3/C1** on the
retained source build and its statement and receipt audits.
Its original report stays separate from the source-build evidence.
No build was performed in this audit, and no bound is adopted through this change.
Its two adversarial AI reviews do not supply the human oversight required for V4. No
human expert formalization review is on file for V5.

`T-060`, Ahmed’s eleven-square optimality result, stays **V3/C3** on its existing exact
geometric confirmation.
Its formalization’s full build remains reported: the retained source summaries do not
resolve which modules were compiled in the private, resumed run.
The statement closure and upper construction built here establish only those components.

## Evidence Matrix

This inventory covers all nine `proof-assistant-checked` methods or reported methods in
`packing/frontier/evidence.yaml` before the additional source-build entry.
The dispositions concern the retained pins, not later upstream revisions.
No rating depends on an author’s reputation or on the absence of a discovered defect.

| Result and formal evidence | Retained execution and inspection | Scope and trust boundary | Disposition |
| --- | --- | --- | --- |
| `T-154`, `E-n017-fitzharding-lean-report` | Public source receipt states `CLEAN_SOURCE_BUILD_ACCEPTED`, 4,951 project modules rebuilt without prebuilt project objects; final axiom log and two control logs retained. Source-consistency receipt matches log digest and manifest closure count. Two separately prompted AI reviews examine the statement and soundness chain; no local Lean run. | Full seventeen-square optimality, including attainment; no geometric premise remains in the stated theorem. Standard axioms plus 13,343 `native_decide` facts; compiler, native runtime and C toolchain are trusted. Missing per-module build logs, timing and machine details remain qualifications. | Add separate source-build entry; V3/C1. Human oversight or expert review can raise V under the existing rubric; C needs a complete confirming execution. |
| `T-060`, `E-n011-lean-formalization-report` | Retained source summary, provenance, integration review and final audit; private run 37414883750, resumed from earlier receipts, with no retained full build logs or project objects. `verification/admissions.json` still says `SOURCE_COMPLETE_REPLAY_PENDING`; integration review says no independent Lean recompilation. | Full optimality is the reported theorem. Standard axioms plus 13,308 native auxiliary axioms; compilation and runtime are trusted. The provenance gap concerns full execution, not the theorem’s intended statement. | Keep report. T-060 remains V3/C3 from separate exact geometry, not from this full formalization. A complete source execution record could establish formal V3 support; independent execution is necessary for formal C3 support. |
| n = 11, `E-n011-lean-statement-closure-build` | Eighteen project modules and a statement probe built here, with full command output retained; non-vacuity controls and an `Iff.rfl` statement check. | Construction at T and elaboration of the statement; standard axioms only, no native evaluation. No lower bound. | Existing V3/C3-quality component evidence; does not establish the whole formal optimality claim. |
| `T-064`, `E-k2m3-evand-bentz-lean-build` | Retained successful build and axiom receipt for the ten-module reduction closure. | `Valid7` implies the family equality; standard axioms. Separate complete exact replay discharges `Valid7`. | Keep whole result V3/C3; formal component plus discharged premise. |
| `T-081`, `E-k2m4-evand-lean-report` | Source reports a reduction; its local build is separately retained below. | The hypothesis `ValidTilt9` is not proved by this formal reduction. | Report adds no whole-claim rung. |
| `T-081`, `E-k2m4-evand-bentz4-lean-build` | Sixteen-module closure built here with retained stage, build and axiom receipts. | Conditional reduction, standard axioms. No complete confirming run for `ValidTilt9` in the cited record. | Keep whole result V0/C1. The implication is checked; the unconditional family claim has an unconfirmed premise. |
| `T-086`, `E-chelokot-square-minus-two-lean` | Retained replay receipt and 79 axiom assertions; four modules rebuilt over the same session’s source build of the other 273. | Full family theorem; standard axioms. Sources recoverable at their public pin rather than retained locally; no fresh single-command rebuild of all modules. | Keep V3/C3 with existing source-retention and build-assembly qualifications. |
| `T-006`, `E-n013-evand-casefree-cover-lean-kernel` | Full generated cover build here, 6,255 seconds; retained axiom log named in limitations but missing from the structured `axioms_receipt` field. | `s(13) = 4`, standard axioms only. Later common-specification bridges were retained but not built. | Keep V3/C3; add the existing axiom-log pointer. No expert review exists to raise V5. |
| `T-124`, `E-evand-local-minima-178-report` | Retained source and theorem roster; no inspected full execution receipt or pinned replay establishing all bindings. | Non-strict local minima under the source’s matched-index convention, not global optimality, uniqueness or rigidity. | Keep V0/C0; proof source and a plausible report are not a complete run. |

The primary retained packets are
[Fitzharding n17](../../../../packing/resources/web/fitzharding-n17-lean-2026-10-13/README.md),
[Ahmed n11](../../../../packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/README.md),
and the evidence entries’ execution receipts and scoped proof blocks.
The
[n11 adversarial review](../../reviews/review-2026-10-06-n11-lean-formalization-adversarial.md)
identifies the private run’s conflicting metadata; that remains a substantive reason to
withhold formal execution credit.
Its broader reading that any source run must wait for an independent replay is replaced
by this decision. Dated reviews remain unchanged.
The n17
[statement and trust audit](../../reviews/review-2026-10-13-fitzharding-n17-lean.md) and
[mathematical audit](../../reviews/review-2026-10-13-fitzharding-n17-mathematical-correctness.md)
remain the source of their findings and limitations; this audit does not replace them.

## Admission and Ratings

### Incoming n = 19 Packet

[PR #642](https://github.com/jlevy/squares/pull/642), inspected read-only at
`71f6a413eb5f15b501554c3017e8cf317b23707e`, is an unmerged source intake, not a
registered result in this audit’s baseline.
It retains Fitzharding’s `sq19` v1.0.0 at `34fb2b7bc39465db368c45cb48d4db58829d3051` and
reports `Sq19.square19_optimality`, with 4,320 native certificate facts.
The
[retained kernel-replay receipt](https://github.com/jlevy/squares/blob/71f6a413eb5f15b501554c3017e8cf317b23707e/packing/resources/web/fitzharding-n19-lean-2026-10-16/sq19/verification/kernel-replay.json)
records zero failures over 13,144 compiled research objects, including the report
module, and a second smoke check of the theorem’s 13,143-module closure.
Kernel replay accepts the native facts as axioms; it does not recompute them.
The
[packet](https://github.com/jlevy/squares/blob/71f6a413eb5f15b501554c3017e8cf317b23707e/packing/resources/web/fitzharding-n19-lean-2026-10-16/README.md)
explicitly says the complete public-script rebuild has not run.

Do not encode this receipt as a complete source rebuild or assume it establishes the
native evaluations’ provenance.
Its registration needs a statement and execution audit that distinguishes the research
objects, their source bindings, the native facts and the kernel replay.
An adequate complete producer execution record can earn V under the same rule as n17; a
fresh independent build is not a prerequisite for source V. No n19 rating or scientific
bound changes in this slice.
The author estimates several hours on 64 cores and 512 GB for a complete build; no such
run was launched. `think-nqnl` owns its replay and `think-o40t` its mathematical review
in the incoming intake.

### Applicable Rungs

| Evidence available | V treatment | C treatment |
| --- | --- | --- |
| Credible announcement or readable formal source, without an adequate execution record | No formal execution rung; normally V0, or V2 only when the proof itself is unavailable | C0, or C1 after a qualifying read |
| Inspected, complete producer build with public recoverable proof, pinned toolchain, retained build and axiom receipts, scoped statement audit and disclosed trust assumptions | V3; use `origin: external`, `performed_by: source-author` | No confirming execution; qualifying read can support C1 |
| Complete build here or retained from a third party beyond the producer, covering every load-bearing part | V3 | C3, with controls and the implementation relationship recorded |
| Complete machine evidence plus two distinct accepting adversarial AI reviews and a named human oversight record | V4 | C4 only when execution and reviews qualify on the confirming side |
| Complete formal evidence plus a named human expert’s formalization review independent of its author | V5 | C5 additionally needs full replay here, public replay instructions and two distinct qualifying experts |

An internal team can earn a high V when its records meet the rung’s requirements.
AI review does not substitute for the human records already required by the rubric.
A native-evaluated formal proof can qualify within its disclosed trust boundary; neither
V3 nor V5 silently makes it a kernel-only computation.
Mathematical premises and partial coverage still limit the derived whole-claim rung.

The source receipt is evidence of what the source says it executed.
It does not independently authenticate the source machine or prove that the stated
commands actually ran there.
That is why the origin is displayed and C stays separate.
Review must judge the consistency and completeness of the source packet, including
conflicting status files; the schema cannot establish the truth of a receipt.

## Implementation

One slice changes the maintained rubric and import guidance, admits the n17 source build
as a separate evidence entry and corrects T-154’s rating and next steps.
`build_receipt` is a repository-relative evidence path.
An external formal entry must also carry its axiom receipt, scoped proof and audit,
explicit full coverage, qualifying dated read and the producer’s passing execution.
The schema gate refuses a missing receipt file; rung derivation refuses incomplete
source formal support.
Result detail links expose the build and axiom receipts.
The existing meaning of `origin`, the human review requirements and every scientific
bound remain unchanged.

Independent review found two admission gaps, corrected before publication: an unresolved
conditional theorem could supply an unconditional rung, and changing only a producer
run’s origin could give it confirming status.
Rung derivation now follows complete, scope-covering premise chains on each axis,
rejects cycles and takes the weakest proof rung in the chain.
Actor/origin validation and confirmation consumers both exclude producer executions from
confirming status; run labels preserve the stated actor.
An unresolved implication remains a legal evidence record and its qualifying read still
counts as C1. Source verification does not require a confirming premise run.

- [x] Audit every existing formal evidence entry and distinguish whole claims from
  components.
- [x] Add source-build admission controls and maintain the V/C separation.
- [x] Apply the n17 correction and the n13 axiom-pointer completion.
- [x] Complete focused admission, derivation and display checks; refresh generated
  records.
- [ ] Independent senior and correctness review, coordinated by the parent task.
- [ ] Publish the separate PR and coordinate its site edition after the News change.

## Tests and Replay Follow-Up

Focused controls distinguish a bare report, a full producer build, missing receipts,
unread receipts, partial coverage, conditional implications, human-reviewed high V and
unchanged low C. Live-record controls verify n17’s receipt/axiom binding, its rendered
links and rungs. A comparison against the baseline confirms that n11 and n17’s case
frontmatter and the original n17 reported evidence are unchanged.

The focused assurance and result-register suite passed 118 tests.
The final source-build admission and rendered-link controls passed 11 tests, including
receipt paths escaping the repository through symlinks.
The changed Python files pass Ruff and BasedPyright.
The URL compatibility check passes with an explicit T-154 evidence-identity amendment;
the previous identity is retained.
The full records gate and release-impact disposition remain part of the coordinated
publication check, not a claimed green release here.

No foreign Lean build belongs to this slice.
The n17 release archives total 1,962,867,415 bytes and expand to 6,986,311,712 bytes of
Lean source, before Mathlib, generated objects and native libraries.
Its source says tens of gigabytes of disk and memory and gives no execution time; the
available external volume had 5.7 GiB free at intake.
`think-r109` owns the complete replay; `think-s7s4` the cheaper statement/endpoint
build; `think-c1kz` the remaining archive scans.
Those component checks do not replace the full lower-bound execution.
n11’s complete formal build and human reviews remain in T-060’s next steps; no replay is
claimed by this policy correction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
