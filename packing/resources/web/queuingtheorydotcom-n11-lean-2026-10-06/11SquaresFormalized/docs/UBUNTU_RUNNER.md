# Run the proof on Ubuntu

The manual verification workflow lets you choose a runner label available to
this repository. It defaults to the standard GitHub-hosted `ubuntu-latest`
runner and **2 Lean workers**, so it does not depend on access to another
organization's larger runner. These defaults do not establish that a complete
replay will fit in one job; accepted-module checkpoints can resume later runs.

EvolvingPrograms performed its replay on the larger `ubuntu-heavy` runner.
Choose **runner_label: ubuntu-heavy** and **jobs: 64** only after its runner
group has granted this repository access. Access granted to
`EvolvingPrograms/11SquaresEvolving` does not by itself grant access to
`Queuingtheorydotcom/11SquaresFormalized`. A configured runner label without
repository access can leave a job queued. A persistent Ubuntu machine is another
option; see the direct-run instructions below.

## Start verification

Open **Actions → Verify simplified proof → Run workflow**. Select the reviewed
branch, choose the available **runner_label** and a suitable **jobs** count,
leave **fresh** unchecked, and keep **resume_run** set to **auto**. The defaults
are **ubuntu-latest** and **2 Lean workers**.
Modules still compile serially; workers operate inside each Lean process.
The appropriate worker count depends on the chosen runner's cores and memory;
actual speedup depends on the module and has not been benchmarked.

The live replay log reports module count, percentage, replay elapsed time, and a
rough remaining-time estimate after ten newly compiled modules. The estimate
extrapolates the average observed compilation interval, excluding cached-module
intervals, to the remaining module count. Module costs vary widely, so it can be
very inaccurate, especially early in a run. It excludes the final audit and does
not refresh continuously while a single module is compiling. A `checking` line
identifies the active module before compilation starts. Reaching 100% of modules
is not proof acceptance; the final audit must still pass. If a module fails, the
console shows a bounded compiler-error excerpt and the relative path to its
complete log; machine-specific absolute paths are redacted from the excerpt.

Increasing workers does not enable concurrent module compilation or guarantee
proportional speedup. Changes to the runner or worker count apply to new runs,
not an already running job.

The job prepares the pinned Lean environment, obtains Mathlib's cache, checks
source assembly, runs the full serial verifier, and validates the final receipts
and public axiom reports. This project's expensive numerical certificates use
`native_decide`; successful verification reports
`OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES` and
`trust_model: lean_kernel_and_native_compiler`. The geometry and checker soundness
proofs remain kernel-checked, but the final theorem additionally trusts Lean's
compiler for the explicitly recorded numerical evaluations. No admissions may
remain. `OPTIMALITY_PROVED` is reserved for a successful kernel-only audit without
native certificate dependencies. Pushes and pull requests do not automatically
start verification.

GitHub-hosted jobs have a [six-hour execution limit](https://docs.github.com/en/actions/reference/limits).
The verification command, including bootstrap and final audit, has a **4-hour-45-minute
budget**. At that cutoff it receives TERM, which stops the active compiler process
group and preserves completed receipts. A 90-second forced-stop fallback and a
290-minute step limit bound shutdown time. The incomplete module is retried on
the next run; a cutoff remains failed/interrupted, never proved.

The workflow reserves time for saving progress instead of waiting for the hard
job limit. Checkout and restoration allow 5 and 10 minutes, packaging allows
10 minutes, and the checkpoint uploads **first**, with up to **30 minutes**.
Evidence and diagnostics each allow another 5 minutes. All step limits total
355 minutes, leaving 5 minutes for overhead within the 360-minute job limit.
Only a completed `proof-checkpoint` upload is resumable. This prevents the known
six-hour cutoff from consuming the upload window; machine loss, manual cancellation,
or upload/storage failures can still prevent a new checkpoint from being saved.

## Download outputs and resume

After a run, open its **Artifacts** section:

- **proof-evidence** (90 days): run status and commit, pinned configuration,
  per-module timings, and, on full success, the final source-hash and axiom audit.
- **proof-diagnostics** (30 days): `diagnostics.tar` containing compiler and setup
  logs and module receipts, including failure details. These diagnostics follow repository artifact access rules and may contain
  machine paths; inspect before sharing publicly.
- **proof-checkpoint** (30 days): `checkpoint.tar` containing accepted `.olean`
  modules, their receipts, and the exact compiler logs required for axiom auditing.
  It excludes toolchains, dependency checkouts, Git metadata, and credentials.

Uploads run after success, failure, or the planned cutoff while job time remains.
Check that **Upload resumable compiled-module checkpoint** succeeded, then start
a **new Run workflow** on the same branch with **fresh** unchecked and
**resume_run: auto** (or that run's ID). A failed/interrupted run can still provide
a valid checkpoint; if its upload failed, use the last run whose upload succeeded.
Re-running an old job keeps its old revision and original resume inputs.
Checkpoint uploads do not overwrite an existing artifact from the same run:
a retry cannot delete its last saved checkpoint, and publishing newer progress
requires a new workflow run. Reports and diagnostics can still be refreshed.

The final evidence
is accepted only when its summary says `OPTIMALITY_PROVED` or
`OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES`, agrees with the finalized audit, and
records zero admissions. The native status preserves the compiler trust model
and exact native axiom list in both the summary and audit; it is never relabelled
kernel-only. A checkpoint, timings, or a verifier result found inside diagnostics
is not proof acceptance.

The next dispatch automatically looks through the newest 100 checkpoint artifacts
in this repository for an unexpired checkpoint from a completed manual
verification on the same branch. Alternatively, supply that workflow's numeric
run ID in **resume_run**. Checkpoint restoration uses the current repository;
do not enter a run ID from `EvolvingPrograms/11SquaresEvolving` when dispatching
in `Queuingtheorydotcom/11SquaresFormalized`. A first run in a new repository
starts without a prior same-repository checkpoint.
The restored objects are reused only after the serial verifier validates source,
compiler, configuration, object, and dependency fingerprints. Changed modules and
their affected dependents are checked again. **fresh** skips restoration and
forces replay. Artifact expiry/deletion means there is no checkpoint to resume.
Mathlib and the pinned toolchain are prepared again on each hosted machine.

To resume a downloaded checkpoint locally, unzip the artifact, then from the
repository root run:

```sh
python3 scripts/verification_artifacts.py extract --archive /path/to/checkpoint.tar
bash scripts/run_verification.sh --bootstrap --jobs 2
```

Use a matching Linux environment for reusable hosted-runner objects. The extractor
rejects non-checkpoint paths and links; it does not establish mathematical validity.
The verifier and final audit still determine acceptance.

## Direct run on a persistent Ubuntu machine

With Python 3, Git, curl, and tar installed, run from the repository root:

```sh
bash scripts/run_verification.sh --bootstrap --jobs 2
```

Choose a worker count appropriate to that machine. The script uses the pinned
`lean-toolchain` and `lake-manifest.json`. Do not invoke historical source
restoration scripts or `verify.py --setup` on this snapshot.

On a persistent machine, keep `.lake/` and `.verification/` to resume from accepted
receipts whose source and dependency fingerprints match. Ctrl-C stops a direct
run; rerun the same command to continue.

Local outputs remain under ignored `.verification/` paths. CI uploads only the
selected outputs described above; none are committed to the source tree.
Only successful full replay and final audit establish acceptance of this export;
source checks and historical component receipts do not.
