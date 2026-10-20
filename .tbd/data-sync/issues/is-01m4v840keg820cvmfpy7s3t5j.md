---
type: is
id: is-01m4v840keg820cvmfpy7s3t5j
title: "Answer #565: Fitzharding's registration request (draft; post only on the owner's word)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: coordinator-stoic-clarke
labels: []
dependencies: []
parent_id: is-01m4v5ne8b1dq1gyybx5mj689d
hold: null
hold_until: null
created_at: 2026-10-13T18:24:12.396Z
updated_at: 2026-10-14T01:30:19.512Z
started_at: 2026-10-14T01:30:14.110Z
---
Draft reply for https://github.com/jlevy/squares/issues/565. Post only on the owner's word (result-import.md, stage 7), and only after the follow-up pull request that adds the `formalization` kind and the mathematical-correctness review has merged, so that every link below resolves on `main`. T-154 is on `main` (#588).

Revised 2026-10-14: T-154's kind is `formalization` by the owner's decision of 13 October (was "simplification"); the second, mathematical-correctness review is added, and its questions are merged with the first review's.

---

Thank you for the release, and for stating the trust boundary so plainly.

**What we did.** We retained sq17-lean at `e6ee548` with the three v1.0.0 archives, pinned by size and SHA-256 (they match your `manifest.json` and GitHub's asset digests), and your announcement post. Two reviews then read it, separately:

- [An adversarial review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-13-fitzharding-n17-lean.md) of the statement, the endpoint, the axiom report and the assembly of the main theorem.
- [A mathematical-correctness review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-13-fitzharding-n17-mathematical-correctness.md), which read the hand-written development in full (about 140 modules, the checker-soundness modules included) and re-derived with its own code what the claims turn on: the endpoint root and frame margins, the D4 action, the 43,593 orbit representatives, the 346,104 census rows, the 35 patterns and 2,781 rosters, the cell cover and wall capacities, and the 93-box dual certificate of the 52-row local model. It re-implemented the compiled trace checker from the Lean text and replayed one branch node, six chunk runs of the capture, two degree-44 table checks and the terminal summary check; every replay agreed with the recorded fact, and corrupted inputs were rejected.

Both reviews accept the proof. Neither found a blocking or major defect: the statement says s(17) = L in this record's sense, `EndpointGeometry.side` is the record's L by identity of definition, everything above the 13,343 `native_decide` facts is kernel-checked, and no premise is left. No Lean was run here, so the build and most of the native checks have not been replayed.

**How it is registered.** As [T-154](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), under your name, Oscar Fitzharding, as a *formalization*: a machine-checked proof, by a route of its own, of s(17) = L, the value Marc Leonard Overbeck's candidate proof (T-153) first reported about six hours earlier on 12 October, as your README says. The record states both dates. T-154 stands at `V0`/`C1` (reported and read) until the build is replayed here or by a third party whose replay we can retain; the n = 17 page links it.

**Questions, to make the credit and the record complete.**

Credit:

1. The proof uses this project's published components and data: the 24-cell cover (`ExactCellCoverData.lean` matches exp-247's `UNIQUE_24` cell for cell, with its D4 tables), the cap 1169/250 and the orbit census, the endpoint chart (the H-255 polynomials and exp-237's root box) and the H-256 layout, the 45-coordinate, 52-row local model of exp-248, and 32 of the 35 excluded patterns, which equal entries of `certified-sub-patterns.yaml`, among them closures that wand125 contributed through #472. Were these taken from the project, and would you name them specifically in the README and `CITATION.cff`? If any were derived independently, saying so is just as useful.
2. #565 names Mannaseh Ahmed's s(11) proof (11SquaresOptimal) as a methodological reference; the README credits only his formalization. Would you add it there too?

Reproducibility:

3. Could you publish the generators and inputs the data files name (`export_lean_cell_cover.py`, `build_tree_dispatch.py`, `cells.txt`, `root_chart_data.json`, `full_cases.tsv`)?
4. What machine, CPU time and peak memory did the clean rebuild take?
5. Does `scripts/reproduce.py` check, by digest, that the five shared libraries it loads with `--load-dynlib` were compiled from the pinned sources of the same build?

Clarity (none of these affects correctness):

6. Several module docstrings still call the development conditional (for example `HalfPlaneAssemblySkeleton.lean:7`, `HalfPlaneFinalAssembly.lean:13`, `HalfPlaneLastTwo.lean:5-6`, `WallCapacityBounds.lean:5`); the theorem's own docstring is right. Could they be brought up to date?
7. `CaptureOpenBridge`, `CaptureTerminalLocalChart`, `CaptureTerminalStateData`, `CaptureTerminalSummaryData` and `HalfPlanePrototype` are built but outside the theorem's dependency closure. Are they kept on purpose, and could they be marked as outside the proof?
8. `rowCheck` in `CaptureSummaryFast.lean:14-18` returns `true` for a row whose entry index is outside the table. `summaryCheck_sound` covers it, but returning `false` would shrink the acceptance set at no cost.
9. Why does square 5 not appear among the 45 chart coordinates: is it the square whose pose the contacts do not pin, and is that stated in the sources?
10. Is there a reason the capture tables keep angle rows outside [−π/4, π/4] after splits, rather than clipping children at the parent's interval?

We will post on #405 with the link once this is merged.
