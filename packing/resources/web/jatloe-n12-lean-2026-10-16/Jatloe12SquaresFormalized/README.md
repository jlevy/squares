# Jatloe: twelve-square formalization

This repository formalizes the optimal square container for twelve unit squares:

```lean
N12Compact.Final.optimality : S12.packingConstant12 = 4
```

The squares may have arbitrary orientations and translations. Their interiors
must be disjoint; boundary contact is allowed. The theorem supplies the global
lower bound and a 4-by-3 grid attaining container side 4.

**Credits:** Jatloe provided the full mathematical proof and partial Lean
formalization. Ben Gurevitch aided in formalization. **CTJLewis refactored and
compiled the formalization.**

## Verified source and evidence

The proof source is copied byte-for-byte from `EvolvingPrograms/SquaresLean`,
branch **`main`**, commit **`1f60d412707aae824b76fbaf11d4e708695451fa`**, accepted
by [run 38849916588, job 116808701733](https://github.com/EvolvingPrograms/SquaresLean/actions/runs/38849916588/job/116808701733).
That job authenticated all **5,377 project modules** against their compiled
objects and receipts and ran a fresh final theorem/type/axiom audit.
All 5,377 module objects were reused from cache; this particular job was not a
fresh compilation of every module. The publication was checked against every
source and compiler-log hash in those receipts; no local full rebuild was run.

The final theorem has no pending case hypotheses or admissions. Its axiom audit
contains the three standard axioms (`propext`, `Classical.choice`, `Quot.sound`)
and **1,624 approved native-generated axioms** from the numerical classification.
Accordingly, verification retains the documented **native compiler trust** of
`native_decide`, in addition to Lean's kernel. There is no `sorryAx` or unexpected
custom axiom in the accepted final audit.

- [Final theorem](Lean/Proofs/N12-jatloe/Compact/Assembly/Final.lean)
- [Packing definition and normalization](Lean/Proofs/N12-jatloe/source/S12/Normalization.lean)
- [Attaining construction and packing constant](Lean/Proofs/N12-jatloe/source/S12/PackingConstant.lean)
- [Publication provenance](SOURCE-PROVENANCE.json) and [verified source hashes](verification/run-38849916588/verified-source-manifest.json)
- [Accepted final report](verification/run-38849916588/github-replay.json) and [type/axiom audit](verification/run-38849916588/global-type-axiom-audit.log)
- [Original verification artifact and checksums](https://github.com/Queuingtheorydotcom/Jatloe12SquaresFormalized/releases/tag/n12-verified-2026-10-16)
- [Mathematical arguments](Lean/Proofs/N12-jatloe/mathematics/README.txt)

The release includes **all 5,377 compiled `.olean` objects** in the original
checkpoint ZIP, plus the original successful-run evidence ZIP and checksums.
The binary checkpoint comes from earlier run `38847898861`; every source,
object and compiler-log hash matches the receipts accepted in successful run
`38849916588`. Its earlier run failure does not supply the theorem evidence;
the later successful final audit does. The bundle contains project objects;
Lean and external libraries are installed separately using the pinned versions.
[Artifact details and independent hash-check instructions](verification/run-38849916588/README.txt)
describe the exact verification scope.

The project is in `Lean/Proofs/N12-jatloe`. The replay environment is pinned to
**Lean 4.35.0**, Mathlib **`56a005855ea17e0b0958f73ec801ae140b0a1679`**.
The accepted final closure has 5,377 project and 4,049 external modules;
including setup, package configurations and the final audit, the inventory is
**9,583 modules**, below the hard 10,000 cap and above the preferred 8,000 target.
Older dated handoffs, source comments and census files record earlier stages;
this README and the run-specific evidence above supersede their status claims.

## Run on GitHub

Open **Actions → Verify twelve-square proof → Run workflow**. Choose branch
**`main`**, target **`N12-jatloe`**, jobs **`auto`**, runner **`ubuntu-latest`**,
fresh unchecked, and resume_run **`auto`**.

```sh
gh workflow run verify.yml --repo Queuingtheorydotcom/Jatloe12SquaresFormalized \
  --ref main -f target=N12-jatloe -f jobs=auto -f resume_run=auto
```

Choose another runner label only if it is available to this repository.
The runner sizes CPU and memory use to the machine, stops proof work after
five hours, and saves progress with time reserved for upload. It resumes using
this repository's complete build cache, including Lean 4.35 object sidecars.
The upstream private cache is not automatically accessible here. During module
verification the console shows only `module k/total`; detailed diagnostics are
saved in artifacts. A saved checkpoint alone is not a completed theorem audit.
See [replay instructions](Lean/Proofs/N12-jatloe/handoff/GITHUB-REPLAY.txt).
