# Completed verification and integration audit — 2026-10-06

The integrated proof passed the full repository verification and final audit in
[EvolvingPrograms run 37414883750](https://github.com/EvolvingPrograms/11SquaresEvolving/actions/runs/37414883750),
at source commit `1bf942a7af1ea330e95489d8997deebd4227ca71` (attempt 1).
The run completed successfully with a clean source checkout. Its proof sources
and build configuration are imported unchanged into 11SquaresFormalized.

## Result and trust

| Check | Result |
| --- | --- |
| Accepted local Lean modules | 7,920 |
| Inventoried admissions / `sorryAx` | 0 |
| Audited theorem targets | 2,234 |
| Approved numerical declarations | 10,464 in 1,839 source files |
| Generated native certificate axiom dependencies | 13,308 |
| Final status | `OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES` |
| Trust model | `lean_kernel_and_native_compiler` |
| Lean | `leanprover/lean4:v4.34.1` |
| Mathlib | `d13f23b723b8a846827a245b89c10fc7d3f11612` |

The final `ElevenSquare.optimality`, `ElevenSquare.optimal_side_lower_bound`, and
`ElevenSquare.Pending.global_lower_bound` axiom reports each contain exactly the
13,308 approved native dependencies plus `propext`, `Classical.choice`, and
`Quot.sound`. No admitted goal or unapproved custom axiom is accepted.
The baseline, prior, and returned certificate targets also pass their audits.

Numerical certificate evaluation uses `native_decide` under an exact
source-bound declaration inventory. Geometry, checker soundness, and assembly
retain ordinary Lean proofs, but the final theorem inherits compiler trust
from its numerical inputs. The result is not a kernel-only verification.

## Evidence review

The integration review downloaded the completed run's evidence and diagnostics,
verified their GitHub artifact SHA-256 digests, and checked their agreement.
It reconciled all 7,920 accepted module receipts, their source hashes, compiler
and configuration pins, and 17,744 recorded dependency edges. It independently
parsed the successful compiler logs and matched their 2,234-target axiom map
against the final report and exact approved native declaration owners.

The successful runner's finalizer validates compiled object hashes against the
receipts, dependency inputs, source hashes, and axiom reports before declaring
success. This integration review did not download the approximately 7.94 GB
compiled checkpoint or perform an additional local Lean replay/object rehash.
It audits the successful run's evidence rather than claiming a second independent
compilation. The successful run reused validated receipts; its elapsed duration
is not a cold full-build benchmark or a macOS runtime guarantee.

Portable evidence is retained here, even after Actions artifacts expire:

- [Summary and Git object identities](../verification/completed-run-20261006/summary.json).
- [Independent source, log, and receipt review](../verification/completed-run-20261006/independent-review.json).
- [Original run provenance](../verification/completed-run-20261006/provenance.json).
- [Complete final audit, gzip-compressed](../verification/completed-run-20261006/final-audit.json.gz): the exact original JSON with all source SHA-256 values and axiom maps. Decompress with `gzip -dc` or Python's `gzip` module.

The summary records SHA-256 digests for the downloaded artifacts and uncompressed
final audit. Raw compiler logs and machine paths are intentionally excluded from
the portable publication. Repository permissions may be required to view the
original Actions run and its downloadable artifacts.

## Integration boundaries

The integration is based on 11SquaresFormalized main
`b237948fa44eb8876ed87eeb21329ab5577c833c` and preserves its Git history. Both Lean
source trees, both root Lean modules, and the three pinned build files match the
verified source commit byte-for-byte. T03 has the same tree hash in the old main,
verified source, and integration: `59311c5ece4160ae3004cb5aa2b764f63fc5775a`.
`ElevenSquare/Optimality.lean` is also unchanged from the old main.

Changes outside the verified proof consist of documentation, credits, portable
evidence, and manual workflow portability. The workflow permits a repository-
available runner label and defaults to `ubuntu-latest` with two workers. It
retains the replay, finalizer, pinned actions, read-only permissions, and resumable
checkpoint behavior. No new workflow was launched as part of this integration.
The integration commit itself has not been run in Actions; its proof acceptance
comes from exact correspondence with the successful source run.

The earlier partial assembly manifest and six-obligation documentation remain
available in the previous main commit. Older simplification and component-audit
files describe their original checkpoints and are not fresh full-proof evidence.
Use [README.md](../README.md) and [MISSING.md](../MISSING.md) for current status.
