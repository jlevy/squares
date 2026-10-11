---
type: is
id: is-01m3rdcdbds5nnn4a7czrz9kra
title: "Coordinate the #247 s(11) intake with PR #246's n = 11 optimality work"
kind: task
status: closed
priority: 1
version: 12
labels:
  - packing
  - low-n
  - coordination
dependencies: []
created_at: 2026-09-30T05:42:45.356Z
updated_at: 2026-10-06T08:42:39.208Z
closed_at: 2026-10-06T08:42:39.191Z
close_reason: "Done: PR #246 merged 2026-09-30 and #249 (stack #258/#260) landed 2026-10-01 with Wang-Li as T-061 and T-060 as the optimum. The correction reply on #247 was posted 2026-10-03T18:48Z naming T-061, and #247 is closed (gh issue view 247)."
resolution: null
duplicate_of: null
---
Two lines of n = 11 work are open at once. This bead keeps them from colliding.

## The two lines

- **jlevy/squares#246**, branch `codex/wand125-tools-review`, a separate agent. It does W7 work on the confirmed global optimality of Trump's eleven-square packing (T-060, S5/V4/C5; P0 `think-3i74`). It also registers wand125's tool claims as T-058 (the `B·UB(n)` ceiling) and T-059 (all 12,028 row minima of Kleddamag's certificate reproduced by wand125's exact `general_pose_tree` checker).
- **jlevy/squares#247 intake**, session 01BwdQAcVk5jwFycxVkLGNaK on branch `claude/determined-goldberg-ura2ed`. Ke Wang and Can Li (Fudan) report `s(11) > 3875000000/999999999`, Zenodo 23038546, CC-BY-4.0. Their certificate is Kleddamag's `global-certificate.json` with 13 threshold-charge orbits reweighted and the parent and core sides scaled by 999999999/1000000000. It improves T-037's 31/8 by 31/7999999992, about 3.9e-9. The intake runs three replays (the authors' two verifiers, Kleddamag's source sweeps, and this repository's native interval parent-core checker) and an independent mathematical review.

## The rules both lines follow

- **IDs.** The current branches collide: #246 uses T-058 to T-060, while #249 uses T-058 for Wang–Li. Contiguous-register validation prevents reserving T-061 in #249 now. Whichever PR merges second renumbers its new entries to follow the first; if #249 is second, Wang–Li becomes T-061. Update every reference and regenerate dependent records.
- **Shared files.** Both lines edit these:
  - `packing/frontier/n-011.md`
  - `packing/frontier/results.yaml`, `evidence.yaml` and `source-coverage.yaml`
  - `packing/resources/README.md`
  - `README.md` and `SYNOPSIS.md`
  - `packing/src/sqpack/release.py` (`DATA_REVISION`)

  #246 also changes `packing/devtools/gate-budgets.yaml`, `run_negative_controls.py` (snapshot cap 160 → 192 MiB) and `packing/src/sqpack/cli/validate.py`, which the #247 intake does not touch. Whichever branch merges second merges main into itself and resolves conflicts there. The #247 intake keeps its `n-011.md` change to one new subsection plus the verified-lower-bound line, so the conflict stays small. `DATA_REVISION` is re-pinned after the merge, never hand-merged.
- **Mathematical overlap.**
  - T-059's `general_pose_tree` row checker is a candidate third route for the Wang–Li certificate: its histogram claims every one of the 12,028 row minima equals 1000047559. Whether that checker accepts the scaled parameters is an open question for the #247 lane's report.
  - T-060 now confirms global optimality at Trump's exact value. Preserve Wang–Li as a separately credited historical lower bound when merging the case records.
  - Preserve the exact equality from T-060 and the earned V4/C4 evidence for the Wang–Li historical bound; do not replace the confirmed optimum with the weaker historical bound during conflict resolution.
- **Tools.** #247 generalises `devtools.verify_kleddamag_n11_native` so it reads the certificate's own container and parent sides, keeping the old certificate's behaviour byte-identical (`packing/devtools/verify_n11_parent_core_native.py` in progress). #246 does not modify that tool.

## Done when

Both PRs are merged with distinct contiguous IDs and complete source credit, `n-011.md` states both lines consistently, and each line's reply (#247 on the issue, #246 in its PR) points at the other where it matters.

## Notes

PR #246 merged first at d44ec04086cffd5498fd69e54ee58415365910c7 on 2026-09-30 at 17:41:19 UTC, after all required checks passed on 424b6be3a. PR #249 advanced to c6f51ce6b with passing pre-integration checks; it remains draft while its owner finishes the s(21)/s(45) re-sweeps. When ready, merge the new main into that branch and rename Wang–Li T-058 to T-061. Preserve T-060 equality, every provider credit and V/C assignment, the native parent-core checker, and the three-shard CI topology. Reconcile shared records, regenerate atlas/readers, repin DATA_REVISION, and run the affected integration checks and checkpoint. The earlier 36 shared paths, 39 text hunks and six binary conflicts are a planning baseline; reassess the current head. PR body and comment5916559023 now record the actual merge and why earlier green checks do not certify the combined source.

2026-09-30 integration (session_01VfxwoTFTTtYPSdNYENYKZ1, branch claude/beads-upstream-merge-vmytrm): main at 5ddb1cdae (#246, #250 to #253) merged into #249's head c6f51ce6b as 818d6cf3f, then DATA_REVISION re-pinned to it at 3d29a00f1. Wang and Li is T-061 in results.yaml, n-011.md, T-037's supersession note, the review disposition, resources/README.md and the packet README, with mapping notes in the register and review; archived receipts carried no ID. T-060's exact equality leads n-011.md; Wang-Li is kept as a historical strict bound with its credit, V4/C4 evidence and S2. No other ID namespace collided (evidence, bibliography, source-coverage, defects, sessions, experiments). Explainer takes main's T-060 solved display; run_negative_controls keeps main's in_pruned_roots; development.md keeps main's three-shard table with #249's re-based frontend/typecheck/geometry records. All generated views and the atlas regenerated from the merged records. Head pushed as d188e13cb, which adds a crate .gitignore and a snapshot PRUNE entry for main's packing/sqverify_exact/target (it left 331 MB of unignored cargo output that broke two negative-control tests under --fast). Local: --records 36/36; --edit passes after npm ci; --fast 467 s, every failure environmental: two process-group reaping tests (PID 1 here does not reap orphans; neither branch touched that code) and the Chromium step (the pinned Playwright build is not installed). Release, explainer and atlas tests: 125 passed. Remaining for done: move #249 onto this head (or open a PR from it), hosted checks on the combined tree, merge, and the #247/#246 cross-links. The s(21)/s(45) re-sweeps (think-l6la) ran in the old session's scratchpad and are not in this merge.

2026-10-01: stacked as jlevy/squares#258 (head claude/beads-upstream-merge-vmytrm, base claude/determined-goldberg-ura2ed). Owner's landing order: results first (#258 into #249's branch, then #249 to main), then #254 (math), then #255 (site). #254 is currently based on #255's branch, so it needs restacking onto main once the results land. Results not in this stack: wand125 rectangle replay batches b02/b04/b07/b08/b09 (need think-0rrj's --merge mode; b01/b03/b05/b06/b10 never pushed), the n21-point frontier-stage receipts, and think-l6la's re-sweeps.

2026-10-01 01:37Z: LANDED. #249's branch was fast-forwarded to #258's head b2f622f17 (which also took in main's #259), #258 merged into it, and stack 260 merged #249 into main as 306ae9fab with a merge commit. Main's tree equals the validated b2f622f17; data revision on main is 818d6cf3f, matching the pin. Evidence on b2f622f17: #249's packing-required and pages-required, and a dispatched full Packing validation whose post-merge-required (integration plus all nine deferred workers) passed. IDs on main: T-058/T-059 wand125, T-060 the n = 11 optimum, T-061 Wang-Li (historical). Remaining for done: the 2026-09-30 11:57Z reply on jlevy/squares#247 (comment 5910776488) still says T-058 and needs a correction pointing at T-061 and T-060; awaiting the owner's go-ahead to post it.
