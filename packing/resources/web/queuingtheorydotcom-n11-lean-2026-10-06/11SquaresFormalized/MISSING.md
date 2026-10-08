# Proof and verification status

No inventoried mathematical admissions remain in the integrated snapshot.
The completed [verification run](https://github.com/EvolvingPrograms/11SquaresEvolving/actions/runs/37414883750)
and its final audit accepted all 7,920 local modules at source commit
`1bf942a7af1ea330e95489d8997deebd4227ca71`. The public optimality theorem and
lower bound passed their transitive axiom audits. These exact proof sources
and build pins are incorporated here.

The result is `OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES` with trust model
`lean_kernel_and_native_compiler`. Expensive numerical certificates use the
precisely inventoried `native_decide` declarations; geometry, soundness, and
assembly retain ordinary proofs. Zero admissions does not mean kernel-only
trust. See [the evidence report](docs/VERIFICATION_20261006.md).

Future proof or dependency changes require renewed verification. The previously
stated 300,000-line simplification and 2–3 hour macOS compilation targets are
not established by this run. The successful run reused validated receipts and
must not be presented as a fresh full-build timing measurement.

The earlier six-obligation state and original assembly manifest remain in Git
history at `b237948fa44eb8876ed87eeb21329ab5577c833c`. Historical handoffs describe
older checkpoints, not outstanding admissions in the current proof.
