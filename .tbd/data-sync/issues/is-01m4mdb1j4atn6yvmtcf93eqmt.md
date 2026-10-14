---
type: is
id: is-01m4mdb1j4atn6yvmtcf93eqmt
title: "Regularization: a typed credit in the register, and every packing n = 1..324 regularized (stacked on PR #487)"
kind: epic
status: in_progress
priority: 1
version: 21
labels:
  - regularization
dependencies: []
child_order_hints:
  - is-01m4mdbdkx61v53br8cp4cmght
  - is-01m4mdbe5pjzjb684fqbedg5p0
  - is-01m4mdbq6bhkv71fxeeckawsbt
  - is-01m4mdbqsgkdz008e42ffjx4ej
  - is-01m4p42ssedcwc2x97vnphnq2p
  - is-01m4p42tpvh49yd1p9cj3t320s
  - is-01m4p42vm11zqf83e657ycs66q
  - is-01m4p42wedbt2e9e3r7fhmphxa
  - is-01m4p42xe0xsyrkr48g6dxhkcj
  - is-01m4p42yjaz3qj1kd5n86hsj8n
  - is-01m4p92a2pdcph8m8v99zt2tzd
  - is-01m4pcp6ensk4j6gd1afb67cbr
  - is-01m4pcp8d9d59rd5btj6xcmxeh
  - is-01m4pcp9t15wsdbwb9kdhw58eq
  - is-01m4pcpb29v0db74jb4pg37yk6
  - is-01m4pfc1r22b6vh9n4dyv23sg2
  - is-01m4q7v1t6qmvrvzsf8qxn4dvq
  - is-01m4w9w2vc4p0j983wvvx8pybw
created_at: 2026-10-11T02:40:44.612Z
updated_at: 2026-10-14T04:14:04.131Z
---
Owner decisions of 2026-10-11, in the session continuing PR https://github.com/jlevy/squares/pull/487 (session_012VZZQseec5xK8Zu4ah5BjG):

1. Regularization is tracked as a specific credit and detail in the records, because the project has further processes for it.
2. Its home is an optional per-count `regularizations` list on register entries (packing/frontier/results.schema.yaml), chosen over a separate regularization register and over a case-record field (PR #403 rewrites every case record). Each item: `n`; `of`, the register result whose packing at n was regularized (its finder keeps the packing's credit through that result's attribution); `by`, the regularizer's bibliography key, or `project`; `method`, the regularizer's own name for the variant; `side`, `same` or `solved` (solved to an exact side first, then regularized at that side); `changes` (merged_rotation_groups_deg, straightened, ...); `identity` (`basis` source-claim or measured, with one_to_one, moved, max_move, max_turn_deg as measured here). check_results resolves every id; the field replaces the hard-coded `CREDITED` map in devtools/check_half_angle_area.py; RESULTS.md and the result pages print it.
3. T-146 (Evan Daniel's regularized certificates at 15 counts) is the first entry to carry it. Credit at n = 70 is Ryan Xu alone; T-137 (Deleeuw) is named only as the previous smallest side. The bibliography credit of [Daniel regularized lists 2026-10-10] becomes "Daniel after Xu, Chaoweeraprasit, Mishapolk, Levy" (review RG-2).
4. Check out evand/square-packing in full into attic/ and examine search/regularize (https://github.com/evand/square-packing/tree/main/search/regularize); adapt it as needed and regularize every packing the record holds, n = 1..324. That is a separate process and a separate pull request, stacked on PR #487, begun once the imports of the 2026-10-10 pass are in good shape.
5. The expensive wand125 confirmation runs (think-r333, think-i85v, think-nd7g: T-132, T-142, T-143, T-144, about 23 to 35 CPU-hours) wait until the regularization is done: clean graphics and pretty diagrams come first.

What the record held on 2026-10-11 (read-only survey of the branch):
- No schema typed regularization. The finder/improver split is per case record (`found_by`, `improved_by`), and `improved_by` is already overloaded for optimizers and exact solvers (devtools/generate_frontier_case.py).
- The project's own regularizer: devtools/regularize_axis_components.py (algorithm regularize_axis_components/2) writes packing/atlas/known-best/regularized/n-NNN-regularized.yaml.gz and index.json (contract packing.squares:RegularizedAtlasIndex/v1, no softschema block; 68 regularized, 182 unchanged, 74 refused). devtools/render_regularized_atlas.py draws regularized/rendering/n-NNN.svg. Validation steps: "regularized atlas views match their index" (records tier) and "regularized atlas views re-derive exactly" (CI job regularized-views). overview_sections.atlas_regularized draws a regularized case from its view (think-k8x9). Policy in index.json: a derived drawing layer, never a witness; it changes no side, frontier value or evidence tier, and every drawing made from it is labelled regularized. The view witnesses' `certificate` block (derived_from, regularization) is unvalidated (witness.schema.yaml additionalProperties: true).
- Evan Daniel's process (packet packing/resources/web/evand-regularized-2026-10-10/, pin ea1a2f2; search/regularize/ added 346c6ed, lists refreshed 122d0ba): each count's best packing refreshed from his store, solved by exactsolve to an 80-digit KKT point S_exact, then translated by an LP toward the bottom-left corner and the walls with symmetries and coincident faces imposed and angles grouped; variants `conservative` (moves only free squares' angles) and `fewest` (also merges determined rotation groups, which his round-5 log first called "a different packing at the same side"); each classed "level 2, same packing traversable without expansion" by a path test sampled in 0.01 degree steps that REGULARIZE.md says is not a continuous proof. 324 rational certificates (n = 1..324) with 50-digit JSON; checkers verify_cert.py and verify_cert2.py (byte-identical to the issue-399 copies). MIT licence; CREDITS.md says the work was produced by Claude under human direction.
- The T-146 stage 4 review (docs/project/reviews/review-2026-10-10-evand-regularized-certificates.md, accepted for finite feasibility only, RG-1..RG-11) measured each regularized view against its credited packing: 10 to 239 squares moved beyond 1e-3, merges of 0.03 to 2.96 degrees under `fewest`, and at 123, 129 and 292 no symmetry matches nearest centres one to one.

## Notes

2026-10-11 (session_017JNnKDwL74rnktr9s8BdjP), state at hand-off. Stack #498: #497 (planning: assessment, policy; main merged twice, DATA_REVISION re-pinned, the stale grid-ceiling premise amended, VENDORED.md references fixed, the owner's reporting vocabulary recorded in the policy) -> #509 (vendor) -> #511 (tools: driver, same-side re-solve, gallery, research doc; draft). #497 and #509 green and mergeable; #511 CI running. Pilots: 25 counts, gallery https://claude.ai/artifact/GGkxS3NBJzodZcJzaUb1qX; 4 admitted (26, 66, 126, 292), 8 held, 1 refused (295), 9 no change, 3 no view. Owner decisions this session: (1) report decisions as no view / no change / held / refused / review / admitted (applied); (2) track every regularization's provenance in the schema, in the register's terms (driver record done; contract and admission think-k35c, a blocker of the full run); (3) an explainer paper in the project's own kpress format, citing Evan Daniel and summarizing our changes, as a later phase after the full run (think-scua). Open for the owner: think-pn0e (row 4 'bound' would admit n = 206; row 7 regressions with improved totals to review; row 5 tolerance; conservative only; adopt T-146 as witnesses; batch-register printed-side packings). Next: think-pn0e answers, think-cb34, think-k35c, then batch 1 (think-ux1v).
