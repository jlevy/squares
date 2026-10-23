---
type: is
id: is-01m4pan85d4sartjf3m3h3p1b6
title: "Lean-backed claims: what V4/V5 and C4/C5 would need for T-060 (n = 11, Ahmed's 11SquaresOptimal and 11SquaresFormalized), T-084, T-055 and T-120..T-124 (#419)"
kind: task
status: open
priority: 1
version: 6
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T20:32:22.189Z
updated_at: 2026-10-23T06:15:48.725Z
started_at: 2026-10-11T20:32:26.032Z
---
Owner request 2026-10-11: check whether the n = 11 repositories by Ahmed are linked and whether the Lean formalization is linked; a proof-assistant formalization might merit V4 or V5, but not C4/C5 until replayed here. Establish for each Lean-backed entry what is retained (pins, statement audit, axiom receipt, native_decide count, builds here), what each rung's predicate in epistemics.md requires that is missing (adversarial AI reviews, human oversight record, human expert formalization review, a replay here at a pinned toolchain), and the price of a Lean replay here.

## Notes

Lane R2 findings, 2026-10-11 (review: docs/project/reviews/review-2026-10-11-lean-backed-rungs.md; worktree branch worktree-agent-a071451124e9c1977).

Upstream (read-only, gh api, 20:38-20:52Z): 11SquaresFormalized unchanged at the pin cdc746ed (pushed 2026-10-06T05:23:46Z, no licence, 16 branches and 21 tags all before the pin). 11SquaresOptimal main 4262f07 (2026-10-09), three commits past f9e0de7, paper/ only, already in intake-watch under think-3i74. The author has no other repository. EvolvingPrograms/11SquaresEvolving (now SquaresLean) is private but visible to the owner's token with admin permission; run 37414883750 is inspectable (success on 1bf942a7, 04:41 to 05:00Z on 6 Oct) and its artifacts are unexpired (proof-checkpoint 7.94 GB until 2026-11-05, proof-diagnostics 7.4 MB until 2026-11-05, proof-evidence 2.0 MB until 2027-01-04); the repository is active (n = 12 formalization, an n11 comparator workflow, a run in progress at 19:21Z). Nothing downloaded; owner decision on retention and terms (think-8spq). evand 6bbae379 commits 258 Packs modules (decide +kernel, standard axioms; n = 102 has one, 125 s at the source; 106, 152, 177 have none at field degree > 20); think-63vx. wand125/square-packing-bounds archived 7 Oct, moved to wand125/square-packing; the hypothesis-free n21pts_eq_5 (77636c63, zero-margin/, five files) is not retained here; think-f2bm. chelokot head e1e9ef5, Apache-2.0, NagamochiPackingTheorem.lean blob unchanged; squareMinusOne compiled here 2 Oct on standard axioms (build.log line 218), unregistered; think-5i1z.

Rungs: every entry stays where it is. T-060 V4/C4 lacks only (a) the second adversarial review *entry* (GPT-6 Pro 2026-10-03 exists, recorded on T-112 as accepted) and (b) the owner's oversight record. V5 lacks a passing build the record holds (the formal entry is reported; routes: third party's retained build, a fork-dispatched Actions run of the public pin, or the owner's ruling that his inspection of the source's run counts toward V) plus a human expert formalization review. C5 also lacks a licence on 11SquaresFormalized (open_review.terms) and a second expert. native_decide: 13,308 compiler-trusted axioms, disclosed everywhere, unregulated by epistemics.md; owner decision whether compiler trust may hold V5/C5 or becomes an attribute beside the rung. Checker gap: formalization reviews are not tied to a formalization (propose formalization_of). Full n11 build infeasible here (7,920 modules, 7.94 GB objects, no cold-build time on record); the statement closure was rebuilt today at v4.34.1 / Mathlib d13f23b7 (toolchain 54 s, restricted cache 1 m 44 s; build receipt in the packet as receipts/lean/build-statement-closure-2026-10-11.log).

Owner decisions: D1 count the source's own run toward V once read; D2 oversight record; D3 the human expert (and one or two at V5); D4 compiler-trusting proofs at V5/C5; D5 retention from the private repo and a licence request to Ahmed; D6 whether and where to pay for the full build.

Build 2026-10-11: the statement closure built again here (devtools.audit_n11_lean stage + build, Lean v4.34.1, Mathlib d13f23b7 cache for the 22 imports only): 18 modules exit 0, probe elaborates, six theorems on [propext, Classical.choice, Quot.sound]; 20:56:37 to 21:15:44Z, 19 min 7 s wall, 9 min 22 s CPU, host load 8 to 13 (7.6 min on 6 Oct). Receipt: packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/build-statement-closure-2026-10-11.log. Checks: packing-validate --records passes except the expected stale SYNOPSIS document-map step; check_documentation the same.

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): owner decisions D1-D6 are on https://github.com/jlevy/squares/issues/543; the section 8 record changes and LR-7 are in https://github.com/jlevy/squares/issues/542 (bead think-npvi). Tracker https://github.com/jlevy/squares/issues/544.
