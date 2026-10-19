# Continuous-pose measure certificate: n=28, s(28) > 1149/200 (5.745)

**Claim.** No packing of 28 closed unit squares (interiors disjoint) fits in the closed square of side 1149/200 = 5.745,
so s(28) > 5.745. This replaces our earlier lower bound 5.7425 (`mixed_n28_L57425`). It is a lower bound, not a claim of optimality.

## Method

The certificate is a nonnegative measure of total mass 2799999/100000 < 28 on the container of side L = 573351/100000 (5.73351),
given by 884 axis-parallel rectangles with masses (each averaged over the 8 images of the container's
symmetry group, mass/8 per image). The checks prove that every square of side B = 499/500 placed anywhere in the container of
side L, at **any** orientation, carries mass at least 1 (threshold 1, with a counting margin). Then 28 disjoint such squares would
need mass 28 > 2799999/100000. Scaling by 1/B = 500/499 turns the container of side L into the container of side
L/B = 1149/200 and the core squares into unit squares, which gives the claim.

Unlike our fine-net certificates (a finite net of directions plus a shrunken core), orientations are covered **continuously**:
the half-angle t = tan(theta/2) in [0, sqrt(2)-1] is split into intervals and each interval is proved with interval
arithmetic and translation-derivative bounds, together with an exact check of the near-axis region.

## Checks (two independent systems, both VERIFIED; both negative controls REFUSED)

| | verifier | result | work |
|---|---|---|---|
| first system | sqverify-fast `--continuous` v4 (source 619b3c00) | VERIFIED `s(28) > 1149/200`, 86/86 roots | 1,265,052,068 nodes, 4183 s on 10 threads |
| second system | contpose_check3 v1.2 (source f3629c29) | VERIFIED `s(28) > 1149/200`, 43/43 slabs | 1,912,948,689 nodes, 8506 s with 16 workers |
| control (masses x 0.985) | both | REFUSED | first system: refused roots; second system: axis coverage refused |

## What is in this bundle

- `candidate.json` — the measure (`n`, `L`, the search core `B`=0.9977 and the search net, which the checks do not use).
- `control/candidate-mass0985.json` — the same measure with every mass x 985/1000 (negative control).
- `check1/` — first system: `summary.json` (final summary), `run.jsonl.gz` (per-root log), the control's summary and log, and
  `src/sqverify_continuous_v4.tgz`, the verifier source (also in wand125/square-packing `tools/sqverify_continuous`, commit d4a1981).
- `check2/` — second system: `receipt.json` (per-slab results), `manifest.json` and the derived inputs (`*.txt.gz`) it checked,
  the control's receipt, and `src/` (the checker and its C++ kernels; `kernel/LICENSE` is the MIT licence of the reused kernel).
- `provenance/search-notes.md` — how the candidate was found (numerical search; not an input to the checks).
- `REPRODUCE.md` — commands to rerun both checks.
- `bundle.json`, `files-sha256.json` — metadata and hashes of every file.

## Independence

The two verifiers share no code. The second system reuses the continuous-pose kernel of Guzhou0806/n40-square-packing (commit 71c97d0, MIT) with the changes listed in check2/src/CHANGES.md; the first system was written separately (it extends sqverify-fast). The second-system kernel was read during a review of that repository, so the two are independent in code, not in authorship of ideas.

## Check (first system)

```sh
tar xzf check1/src/sqverify_continuous_v4.tgz
(cd sqverify_continuous/sqverify_fast && cargo build --release --locked)
sqverify_continuous/sqverify_fast/target/release/sqverify-fast --candidate candidate.json --n 28 --continuous --core 499/500 --tau 1 --threads 8 --max-nodes 200000000 | tail -1
```

The last line must show `"status":"VERIFIED"` and `"claim":"s(28) > 1149/200"`. The second system and the control are in REPRODUCE.md.

## Pre-publication check

Before publication the first system was rebuilt from `check1/src/` and run again on a fresh Ubuntu 24.04.5 LTS (x86_64), Rust 1.98.0 machine: VERIFIED `s(28) > 1149/200` with 86/86 roots in 3714 s on 30 threads (source digest `619b3c00bd91`), and the control (masses x 985/1000) was REFUSED. The tarball's SHA-256 and all its file hashes were checked first. The receipt is `verification/prepublication-receipt.json`.
