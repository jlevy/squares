# Eleven-square packing in Lean

**The complete optimality proof passed verification with native numerical certificates.**
The completed [EvolvingPrograms verification run](https://github.com/EvolvingPrograms/11SquaresEvolving/actions/runs/37414883750)
accepted all **7,920 local Lean modules**, and its final audit reports **zero
admissions**. This repository imports those exact proof sources and pinned
build configuration from commit `1bf942a7af1ea330e95489d8997deebd4227ca71`.
See the [verification report](docs/VERIFICATION_20261006.md) for evidence and scope.

Selected expensive, exact numerical certificate checks use `native_decide`.
Geometry, checker soundness, and proof assembly retain ordinary Lean proofs.
Consequently the final theorem trusts **Lean's kernel and native compiler**;
this is not a kernel-only verification claim. The approved numerical declarations
and their exact source hashes are recorded in
[verification/native-certificates.json](verification/native-certificates.json).

The optimal side length is

\[
T = \frac{6u+4}{1+2u-u^2},
\]

where `u` is the unique root in `(9/25,37/100)` of

\[
5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1=0.
\]

The construction attains approximately `3.8770835900228141773`. The model allows
arbitrary orientations, legal boundary contact, and disjoint open interiors.
The public statements in `ElevenSquare/Optimality.lean` and the complete T03
source tree are unchanged from this repository's previous main branch.

## Entry points

| File | Purpose |
| --- | --- |
| `ElevenSquare/Foundations.lean` | Geometry, exact endpoint, attaining construction, closed-cell cover, and finite case reduction. |
| `ElevenSquare/Pending/` | Original public interfaces, now discharged by the integrated proof. The directory name is historical. |
| `ElevenSquare/Interop/Wand125/` | Connections to the incorporated upstream certificate results. |
| `ElevenSquare/Tasks/` | Geometric arguments, checkers, certificate data, and local analytic proofs. |
| `Sqpack/` | Incorporated certificate checkers, generated proofs, and simplifications. |
| `ElevenSquare/Optimality.lean` | Unconditional optimality and side-length lower-bound theorems. |
| `ElevenSquare/Verification.lean` | Axiom queries for the public proof targets. |

## Reproduce verification

The project pins **Lean 4.34.1** and Mathlib revision
`d13f23b723b8a846827a245b89c10fc7d3f11612`. Keep `lake-manifest.json` unchanged.
On Linux with Python 3, Git, curl, and tar:

```sh
bash scripts/run_verification.sh --bootstrap --jobs 2
```

On macOS, first install the `elan` launcher, then use the same command. The
bootstrap can prepare the pinned toolchain and dependency cache when `elan` is
already installed. Choose a worker count appropriate to the machine; modules
are compiled serially. Existing valid receipts are reusable. Add `--fresh` to
force a complete replay; Ctrl-C stops the runner cleanly.

The command checks every local module and performs the final source, receipt,
dependency, and axiom audit. Require `OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES`,
zero admissions, and `trust_model: lean_kernel_and_native_compiler` in the final
result. Reaching 100% of compiled modules alone is not sufficient.

A source-only check, without Lean, is:

```sh
python3 scripts/check_sources.py
```

The [manual workflow and Ubuntu instructions](docs/UBUNTU_RUNNER.md) also support
resumable verification. Pushes do not start a workflow. The successful source
run used EvolvingPrograms' larger runner; it does not establish a cold-build
runtime or a 2–3 hour macOS guarantee.

Do not run historical materialization commands or `verify.py --setup` on this
snapshot: they restore superseded generated sources. Build objects and logs
belong in ignored `.lake/` and `.verification/` directories.

## Credits and provenance

We thank **[EvolvingPrograms](https://github.com/EvolvingPrograms),
[@ctjlewis](https://github.com/ctjlewis), and every project contributor** for the
formalization and verification work. See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md)
for individual and upstream credits, [PROVENANCE.md](PROVENANCE.md) for source
history, and [integrations/wand125](integrations/wand125/) for retained notices.
Historical simplification notes and partial-audit records are preserved; their
old unfinished-status statements are superseded by the completed-run report.
