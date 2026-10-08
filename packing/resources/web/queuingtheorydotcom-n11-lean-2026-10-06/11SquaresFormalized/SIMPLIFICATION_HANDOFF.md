> Historical checkpoint notes. The integrated proof has since passed its full
> replay and final audit; see [the current report](docs/VERIFICATION_20261006.md)
> and [README.md](README.md) for current commands and trust assumptions.

# PC continuation: recovered eleven-square simplification

> Historical handoff for the imported `dac90e2f` checkpoint. The current branch is `codex/simplification-unverified-20261003`, with 394,204 reachable lines and further unverified simplifications. Use [PC_RESUME.md](PC_RESUME.md) for current commands and status. The following original counts and acceptance notes describe the earlier bundle.

This branch starts from `c82cff63e48b2d3f2da60cb998bbab48e557c012` and preserves a complete, hash-bound candidate source closure for `ElevenSquare.Optimality`.

**494,346 physical Lean lines, 7,514 local modules, zero missing local imports. Full assembled Lean acceptance is pending.** The 2,681,349-line original theorem closure is the comparison baseline. The earlier ~504,000 figure was an intermediate source proposal. The bounded stage-context pass brings this delivered checkpoint below 500,000; it preserves each theorem statement and proof body, rather than removing geometric obligations.

This is a normal Git branch containing the complete source files. The downloadable Git bundle uses `c82cff63e48b2d3f2da60cb998bbab48e557c012` as its prerequisite. From your existing repository, import it with:

```sh
git fetch origin c82cff63e48b2d3f2da60cb998bbab48e557c012
git bundle verify /path/to/eleven-squares-simplification.bundle
git fetch /path/to/eleven-squares-simplification.bundle simplification-recovered-20261003:simplification-recovered-20261003
git switch simplification-recovered-20261003
lake exe cache get
python3 scripts/verify.py --module ElevenSquare.Optimality --jobs 1 --keep-going
```

After inspection, push the branch from your PC:

```sh
git push -u origin simplification-recovered-20261003
```

On Windows, use `python` or `py` in place of `python3`. The unchanged repository verifier handles platform paths. The toolchain is Lean **4.34.1**; Mathlib is pinned to **d13f23b723b8a846827a245b89c10fc7d3f11612**. Preserve `lake-manifest.json`. Do not run the historical `--setup` or `materialize_wand125.py` on this source checkpoint: those restore the old generated sources.

Start with one Lean worker per module. The recovered environment had an 8 GiB memory limit, and several finite evaluations exhausted it. More memory on your PC may help; kernel checking of large exact certificates can still take substantial time. Matching accepted verifier receipts are reusable on repeated runs. This checkpoint includes source and portable evidence, without compiler binaries or objects.

## What was actually accepted

- The concrete common forty-row local-isolation argument.
- The full four-collision symmetry bridge.
- The complete physical case-2135 exclusion through all seventeen reduced stages.
- Actual complementary-capture and correlated-wall pilots, plus their generic soundness rules.
- Generic unconditional and conditional ownership-trace interpreters.

See `simplification/accepted-components.json` for the recorded target receipts and whether the target source bytes match this checkpoint. These component results do not certify the complete assembled dependency graph.

## First remaining checks and repairs

- Compile the source inventory classifier and the bounded selected-field dispatcher. A previous dispatcher run passed its finite block computations but failed at its final inferred-parameter join. The delivered source includes the later explicit-parameter repair and its split check module; acceptance of that repair was still pending when this checkpoint was frozen.
- Replay the complete generated stage bundles, conditional ownership programs, and U5 capture route. The U5 step-137 monolithic and width-eight pilot checks previously exceeded available memory. Further bounded row checks may be required.
- Replay the multi-option finite pilots. Their generic logical theorem was accepted; the first monolithic concrete evaluation exhausted memory. Fast or further chunked representations remain to check.
- Finish `ElevenSquare.Optimality` and inspect all printed axiom reports. Accepted targets may use only `propext`, `Classical.choice`, and `Quot.sound`; never accept `sorryAx`, custom axioms, or `native_decide` as proof completion.

The branch includes the unchanged serial verifier and its historical verification metadata. Source hashes, Git bundle integrity, an empty admission inventory, and Python certificate checks are distinct from Lean kernel acceptance. No complete optimality or full-family acceptance claim accompanies this branch.

## Reading the recovered work

[ALL_SIMPLIFICATIONS.md](simplification/ALL_SIMPLIFICATIONS.md) records the geometric, local, ownership, symmetry, and certificate reductions. `[PREVIOUS_ROUNDS.md](simplification/PREVIOUS_ROUNDS.md)` preserves the earlier T03 and geometric rounds. `simplification/source-manifest.json` authenticates the delivered Lean files; `simplification/source-preflight.json` records the actual import/admission preflight. The two one-line package entrypoints add two lines outside the counted final theorem closure.
