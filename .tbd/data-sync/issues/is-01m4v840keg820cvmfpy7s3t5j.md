---
type: is
id: is-01m4v840keg820cvmfpy7s3t5j
title: "Answer #565: Fitzharding's registration request (draft; post only on the owner's word)"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4v5ne8b1dq1gyybx5mj689d
created_at: 2026-10-13T18:24:12.396Z
updated_at: 2026-10-13T18:24:12.396Z
---
Draft reply for https://github.com/jlevy/squares/issues/565. Post after the import merges, and only on the owner's word (result-import.md, stage 7). Replace <T-NNN> with the result id once it is on main; quote no id before then.

---

Thank you for the release and for the clear statement of the trust boundary.

**What we did.** We retained sq17-lean at e6ee548 (the v1.0.0 archives by size and SHA-256, which match your manifest.json and GitHub's asset digests) with your announcement post, and an adversarial review read the statement, the endpoint, the axiom report and the assembly of the main theorem. It found no mathematical defect in what it read: `PlainPacking L ↔ EndpointGeometry.side ≤ L` says s(17) = L in this record's sense, `EndpointGeometry.side` is the record's L by identity of definition, the statement and the upper half are kernel-only, and no certificate-acceptance or case-exclusion premise is left. Nothing has been compiled here yet, so the 13,343 native checks have not been replayed.

**How it is registered.** As <T-NNN>, under your name, Oscar Fitzharding: a second, independent proof of s(17) = L by a different route, beside Marc Leonard Overbeck's candidate proof (T-153), which was public about six hours earlier on 12 October, as your README says. The record states both dates. It stands at V0/C1 until the build is replayed here or by a third party whose replay we can retain, and the n = 17 case page links it.

**Questions, to make the credit and the record complete:**
1. The review found that the proof uses this project's published components and data: the 24-cell cover (ExactCellCoverData.lean matches exp-247's UNIQUE_24 cell for cell), the cap 1169/250 and the orbit census, the endpoint chart (the H-255 polynomials and exp-237's box) and the H-256 layout, the 52-row local recipe, and 32 of the 35 excluded patterns, which equal entries of certified-sub-patterns.yaml, among them closures wand125 contributed through #472. Would you credit these specifically in the README and CITATION.cff?
2. #565 names Mannaseh Ahmed's s(11) proof (11SquaresOptimal) as a methodological reference; the README credits only his formalization. Would you add it there too?
3. Could you publish the generators and inputs the data files name (export_lean_cell_cover.py, build_tree_dispatch.py, cells.txt, root_chart_data.json, full_cases.tsv)?
4. For the replay: what machine, CPU time and peak memory did the clean rebuild take?
5. Several docstrings still describe an earlier conditional state (for example HalfPlaneAssemblySkeleton.lean lines 7–9); a cleanup would help readers.

We will post on #405 with the link once it is merged.
