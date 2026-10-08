> Historical checkpoint notes. The integrated proof has since passed its full
> replay and final audit; see [the current report](docs/VERIFICATION_20261006.md)
> and [README.md](README.md) for current commands and trust assumptions.

# Resume the unverified simplification checkpoint

Branch: `codex/native-numerical-certificates-20261004`.

This is one project. Its generated numerical certificate proofs now use
`native_decide`, while geometry, soundness proofs, and assembly use ordinary
Lean proofs. Continue with `python3 scripts/verify.py --jobs 1`. No separate
numerical project or manual proof assumptions are needed. The axiom audit
permits only the exact native declaration owners in the source inventory.
The final theorem inherits compiler trust from these numerical results.

Expect `OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES` after a successful full
replay with zero admissions. No full replay or speedup has yet been measured
for this change. `checking MODULE` now identifies active work; `cached MODULE`
means that module has already been reused successfully. Existing unchanged
receipts remain reusable; changed sources and their dependents are rechecked.

The measurements and older source manifests below describe the preceding
checkpoint. New source hashes and inverse hashes are in
`verification/native-certificates.json`.

**This is a source candidate, not a verified full proof.** The full `ElevenSquare.Verification` target has not been run on this checkpoint. The imported bundle commit is `dac90e2f02d4afe8482096e13b9dcf546d871fde`, based on `c82cff63e48b2d3f2da60cb998bbab48e557c012`.

## Current size and scope

The refreshed `ElevenSquare.Optimality` census contains **365,392 physical Lean lines, 4,257 local modules and 1,051,109,682 bytes**. It includes every reached local certificate source and excludes pinned Lean/Mathlib dependencies. No missing local imports, import cycles or symlinked sources were found. File hashes and import edges are recorded in `simplification/checkpoint-census.json` and `simplification/source-manifest.json`.

The prior checkpoint contained 394,204 lines in 6,326 modules: the structural simplifications remove **28,812 lines and 2,069 reachable modules**. Module bundling accounts for **2,032** of the removed modules: 1,301 T07 modules and 731 Sqpack modules. Additional dependency pruning accounts for the remaining net reduction. **The 300,000-line target remains unfinished.** Subsequent certificate trimming removes another **34,739,375 bytes**, leaving roughly 1.05 GB of active source.

## Implemented source reductions

- Across 459 T07 stages, remove 5,964,331 trailing zero Farkas weights and clear 20,152 collision-core lists where the collision-region list is empty. The existing checker and all packing conclusions remain unchanged. `simplification/t07-certificate-trimming.json` retains exact inverse edits; the older bundling audit first inverts this layer. The frozen S135 pruning fixture passes, but this is not a corpus replay.

- Conditional coverage uses indexed triangle/target tables across 267 cases, retaining 6,688 triangle entries and 6,421 target entries and checking 20,343 consumer references. This saves 14,991 lines; removing 652 redundant root aliases saves another 1,304 while preserving public statements and proof bodies.
- T07's 842 certificate shards and 459 auxiliary proof modules are bundled into their 459 stage modules. All 26,033 moved public declaration blocks are preserved. Sqpack bypasses intermediate import facades and combines selected small modules with their sole consumer, removing another 731 modules from the active closure. Old import paths remain compatibility reexports. The ledgers reconstruct exact predecessor source bytes.
- Four collision bounds use rational coordinate boxes and a shared distance argument. Label/view/mask data is separated from historical geometry, removing unused dependencies.
- The common local cone shares fixed-row and parallel-row arguments, retaining its 40 rows and 66 dual certificates. Bundled field proofs share option and majority arguments, retaining 187 cover calls and 147 majority certificates.
- T07 shares repeated tree spines and generates the original width-eight finite goals within stage proofs. Source audits cover 22,931 transformed trees and 3,303 regrouped checking blocks. T06, inventory, singleton ownership and endpoint helpers retain the earlier shared arguments.

Module bundling avoids **2,032 compiler launches in a cold final-theorem replay**. It does not remove certificate data or finite checks. Retained compatibility and historical modules still run under `--all`, so that broader audit does not receive this startup reduction.

## Excluded experiments and timing limits

The new `DirectSupport` and `DirectTree` modules are optional and are not imported by the active theorem. Lean accepted their soundness proofs with only the three permitted standard axioms. Their S135 benchmark retains the same `ExtStep` conclusion: two mirrored comparisons measured median CPU time of 51.775641 seconds for the original and 36.3148995 for direct support checking with unused-core removal. This is a 29.9% component improvement, not a full-build estimate. The active zero-tail/unused-core pass uses the original checker; its separate single-trial scout was 42.135205 CPU seconds versus 49.700244 originally. See `simplification/T07_DATA_PROFILE_20261003.md` for reproducible commands and remaining rollout work.

The active proof uses **original literal T07 witness data**. Compact witness recipes were removed after the complete S135 scout measured **54.126 CPU seconds for literals versus 132.407 for compact recipes**. These are single observations, not a general speed ratio or a full-proof benchmark. Only S137's experimental certificate/consumer inputs were restored; all module mergers remain. Its older compact-certificate acceptance is marked historical, and the bundling ledger preserves the exclusion history.

All four conditions in the full S135 pruning benchmark fixtures passed Lean. This is fixture evidence, not acceptance of the assembled production stage. Runtime-checker equality/soundness helpers and the LCM helper have focused Lean acceptance. The **LCM runtime comparison was not run**; its optional `--lcm-only` benchmark path is prepared for the larger computer. The prototype is **not enabled in the active proof**. There is no supported 2–3 hour full-build estimate. Do not enable experimental routes merely because their helpers compile.

## Check on the larger computer

Install Git, Python 3 and elan. For a fresh clone:

```sh
git clone --branch codex/simplification-unverified-20261003 https://github.com/Queuingtheorydotcom/11SquaresFormalized.git
cd 11SquaresFormalized
```

For an existing clone, fetch and switch to this branch while preserving local changes. Keep the pinned **Lean 4.34.1** toolchain and Mathlib revision **d13f23b723b8a846827a245b89c10fc7d3f11612**. Restore the dependency cache, then run the main verification command:

```sh
lake exe cache get
python3 scripts/verify.py --jobs 1
```

This checks **`ElevenSquare.Verification` and its dependency closure, including the final public axiom audit**. Require `OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES`, zero admissions and only the standard axioms plus the exact inventoried numerical native axioms. The result must disclose compiler trust. No `--all` step is required for that final-theorem check. Historical reports under `verification/` or `simplification/accepted-components.json` do not certify current source.

The verifier compiles modules serially; `--jobs` controls worker threads inside each Lean process. Ctrl-C stops a run. Rerun the same command to reuse matching accepted receipts; changed sources or dependencies require new checks. Inspect `.verification/incomplete-result.json` and the named module logs after failures. A fresh clone does not include local compiled objects or machine-local receipts. On Windows use `python` or `py` instead of `python3`.

**Do not run `verify.py --setup` or `materialize_wand125.py` on this branch:** they restore the older generated source layout.

For optional source-preservation checks:

```sh
python3 scripts/check_sources.py
python3 scripts/simplification_census.py
python3 scripts/simplify_indexed_stages.py --check
python3 scripts/simplify_stage_aliases.py --check
python3 scripts/bundle_t07_stages.py --check
python3 scripts/flatten_stage_bundles.py --check
python3 scripts/trim_t07_zero_tails.py --check simplification/t07-certificate-trimming.json
```

## Optional entire-repository audit

To additionally check every retained auxiliary, historical and compatibility module, use:

```sh
python3 scripts/verify.py --all --jobs 1
python3 scripts/finalize_verification.py
```

The finalizer requires that broader `--all` result. After it succeeds, `python3 scripts/finalize_verification.py --write` records portable whole-repository evidence. This optional audit does **not** benefit from the 2,032 removed theorem-closure startups, because the compatibility files still exist.

## What remains

Focused checks cover selected cones, collision bounds, shared adapters and helpers. The selected `P2.S0` / `P2.S1` replay was deliberately stopped with exit 130 when free disk space fell to approximately 123 MiB and the machine was swapping heavily. Both verifier and Lean processes were confirmed stopped; free space recovered to approximately 1.6 GiB.

Dependencies through `P2.S1D` passed. **`P2.S0` was not accepted, and `P2.S1` was not attempted. No complete merged-stage kernel pass is claimed.** All checkpoint source audits pass, but they and the S135 fixture results do not replace the unrun final target. **Do not restart the full history replay on this Mac in this state; continue on the larger computer.** The later bounded certificate fixtures are separate evidence.

Run the final-target command, fix any failures, and inspect its public axiom result before claiming the proof complete. If source changes, refresh the census with `python3 scripts/simplification_census.py --write`. Preserve the packing model, final statements, strict owned interiors, legal touching and closed split boundaries. Keep this checkpoint on its branch until the final-theorem replay and axiom audit pass.
