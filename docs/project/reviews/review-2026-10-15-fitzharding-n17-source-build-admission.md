# Source-Build Admission Audit: Fitzharding’s n = 17 Lean Receipts

Audited 2026-10-15 under
[epistemics.md → Reported Formal Proofs and Source Builds](../../../epistemics.md#reported-formal-proofs-and-source-builds)
by Codex at the strong tier with xhigh reasoning, the author of the rule and of the
admission (bead `think-o6ou`), not an independent reviewer.
The audit was first written into the
[implementation plan](../specs/active/plan-2026-10-15-formal-proof-verification-rubric.md),
a transient document.
This record retains its n = 17 part.
It was written on 16 October 2026 by Claude Opus 5.5 (the addressing pass for PR #645,
acting as `user-eb-addr-645`), from the plan, from the admitted evidence entry and from
the receipt fields re-read that day.
The re-reading treated the retained packet as data; it ran no Lean, lake or source
script.

The audit admits `E-n017-fitzharding-lean-source-build` as separate external evidence
beside the source’s report, `E-n017-fitzharding-lean-report`, which stays as it was.
No Lean build was performed for the audit or for this record, no bound moves, and the
case’s verified lane does not cite the entry (`sqpack.assurance.verified_here`). This is
not a human oversight record and not a human formalization review.

**Verdict: admitted as source verification only.** The retained receipt and axiom log
record a complete producer build of `Sq17.square17_optimality` at pinned versions.
They support V3 for T-154 and supply no confirmation: C stays at the C1 the two 13
October reads give.

## What Was Inspected

The packet is
[`fitzharding-n17-lean-2026-10-13`](../../../packing/resources/web/fitzharding-n17-lean-2026-10-13/README.md),
retained from `ofitzharding/sq17-lean` release `v1.0.0`.

| Record | What it states | Checked against |
| --- | --- | --- |
| `sq17-lean/verification/clean-build-receipt.json` | `CLEAN_SOURCE_BUILD_ACCEPTED` for `Sq17.square17_optimality` at Lean 4.34.1; 4,951 project modules rebuilt with no prebuilt project objects; the pinned third-party (Mathlib) cache used; axioms `propext`, `Classical.choice`, `Quot.sound` and 13,343 `native_decide` facts, none unexpected; two control modules with exit code 0 | The theorem and statement the two 13 October reviews read; the axiom log below |
| `sq17-lean/verification/Square17Optimality.log.gz` | The final axiom report | Its SHA-256, `5e74c4af…8ac241`, equals the receipt’s `final_log_sha256` |
| `receipts/source-consistency.json` | The release manifest is complete for `Sq17Lean.Square17Optimality`: final closure 4,951, no pending module, two validation-only controls; 13,346 axioms listed, no `sorryAx`; the log digest, axiom counts and controls match the receipt | The retained checkout’s 1,215 in-tree Lean files and 12 root files, all matching the manifest |

The test `test_live_n17_source_receipt_supports_v_only_and_binds_its_axiom_log`
re-checks the receipt’s status, theorem, module count, prebuilt flag, axiom fields and
the log binding on every run.

## Assessment

The rule asks the audit to assess five things.

- **Recoverability.** The proof and its three source archives are public at the pinned
  release; the manifest lists the archives, 1,962,867,415 bytes in all.
  The record has not downloaded two of the three.
- **Build pins.** Lean 4.34.1 and Mathlib `d13f23b7`; the replay command and its
  terminal acceptance line are recorded on the evidence entry.
- **Execution completeness.** The receipt covers the theorem’s whole 4,951-module import
  closure, rebuilt without project prebuilts.
  It has no per-module logs, timing or machine specification.
- **Statement fidelity.** The theorem states this record’s `s(17) = L` exactly, by the
  [adversarial review](review-2026-10-13-fitzharding-n17-lean.md) and the
  [mathematical-correctness review](review-2026-10-13-fitzharding-n17-mathematical-correctness.md)
  of 13 October, whose findings and limitations stand; this audit did not re-read the
  mathematics.
- **Trust boundary.** Lean’s kernel, Mathlib, the compiler, native runtime, C toolchain
  and compiled checker libraries are trusted; the 13,343 `native_decide` facts make this
  more than a kernel-only check.

## Limitations

The receipt is the source’s account of its own run.
Inspecting it does not authenticate the source machine or show that the commands ran
there, which is why the entry’s origin is `external`, its actor `source-author`, and why
it cannot confirm. The ten `native_decide` facts the second review checked independently
are a sample. The two accepting adversarial reviews are AI reviews and supply no human
oversight or expert attestation.

## Dispositions on 15 October 2026

- T-154 moved from V0/C1 to V3/C1 on this entry.
  V4 waits on the owner’s oversight record; C3 on a complete build beyond the producer
  (`think-r109`).
- T-060 stayed V3/C3 on its separate exact geometric confirmation.
  Its formalization’s full build remains reported: the retained source summaries do not
  resolve which modules the private, resumed run compiled.
- The plan’s evidence matrix records the audit’s reading of the other formal entries in
  the register that day; none of their rungs moved.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
