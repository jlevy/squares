---
type: is
id: is-01m4padkz7c8b0chp1f85vmfy8
title: "Import BuddenPing: s(207) <= 14.880960373044 (#503)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T20:28:12.135Z
updated_at: 2026-10-11T21:13:32.635Z
started_at: 2026-10-11T20:28:24.948Z
---
https://github.com/jlevy/squares/issues/503 (2026-10-11T10:27Z). BuddenPing/square-packing-certificates 9dc93b6ac2f8fefe038062a74c9a75bf05afdba6, n207.cert.json (SHA-256 1c334f31...) and pingyou-n207-rational.yaml Witness/v2; zip 01-squares-project.zip. Below SQUISH #481's n207 (T-136) by 4.55e-3. Stages 1-4 replay through devtools.upper_bound_reports.

## Notes

2026-10-11 import lane C (stages 1, 2 and the stage 4 replay), worktree /home/user/squares/.claude/worktrees/agent-a083f5edf89079571, branch worktree-agent-a083f5edf89079571, commit 7ad4fc95f (not pushed). Packet packing/resources/web/pingyou-n207-certificate-2026-10-11.

## Stage 1 triage

- **Pin:** BuddenPing/square-packing-certificates 9dc93b6ac2f8fefe038062a74c9a75bf05afdba6, committed 2026-10-11T10:30:57Z (tree 14d56776), the revision the issue names. The repository (created 10:25:46Z) has three commits: 0d8b9c1 (10:26:22Z) first published all seven files, with the certificate and witness blobs unchanged since; 9dc93b6 "Correct attribution in submission materials" changed only the zip, README.md and SHA256SUMS; bc328a7 (10:39:06Z, head at retrieval 20:33Z) is #504's n153 release and leaves the n207 files unchanged. The issue was opened at 10:27:00Z citing 0d8b9c1 and edited at 10:31:52Z to cite 9dc93b6.
- **Author and credit, from the source's files:** README headed "Square-packing certificates — PingYou Ltd"; credit asked for PingYou Ltd (the n207 assembly), Ryan Xu (the n70 construction, #432), Evan Daniel (exact retention of the n70, his regularized n-070.cert.gz at 7dfca4e), and SQUISH's #481 n207 only as the comparison. Commits authored "BuddenPing" from a pingyou.com address; no individual is named, and the packet names none. The record's "PINGYOU LTD" Fibonacci-torus abstract (think-aj43) has the same company name; nothing in this release refers to it, and it is not linked.
- **Licence:** none (no file, GitHub detects none; the README grants nothing for the source's own files). Derived-only custody.
- **AI assistance:** the pinned source states none. 0d8b9c1's README and the issue as first posted said OpenAI Codex assisted the verification, the comparison review and the package; 9dc93b6 removed that sentence from README.md and from the zip's ISSUE_BODY.txt (and "Codex-assisted workflow" became "workflow"), and the issue was edited to match. No reason given. Open question for the owner and the records lane: which account the register carries (the plan's credit text states the history factually).
- **Every claim in the release:** one bound, s(207) <= 148809603730436756319360591381170501178639/10^40 = 14.8809603730436756319360591381170501178639 (requested). Author reports beside it: its three exact Fraction checkers accept 21,321 pairs and every wall; reproduce.py rebuilds all 207 poses from the n70 parent; this repository's exact_verify and check_rational_witness_independent at 5b0eb012 accept its Witness/v2. No optimality claim. The zip also carries SQUISH's #481 n207 certificate (byte-identical, da36d750) and the n70 parent (cites the digest 65b1c469 the T-146 packet records for n-070.cert.gz; its side equals T-146's n70 exactly); neither is a claim of this release.
- **Register map:** a bound the record does not hold, one in-horizon count: a new entry (stage 1 table, row 1).
- **Who else holds 207:** the case, T-127 (Gupta after SQUISH), 14887992258302657381304248932763/10^30: this is 7.03e-3 below (exactly 70318852589817493681897946459498821361/10^40). Pending T-136 (#481, SQUISH), 14.88550630884167768...: 4.5459357980020505e-3 below, the margin the issue states. T-056, T-098 and T-116 are older entries the case supersedes. Other 2026-10-11 reports: none at 207 (#500, #501, #504, #505, #506).
- **Priced validation plan:** both maintained exact routes on the derived fact, 3 jobs, priced at minutes and run (below). New tools: pingyou-json and witness-corners adapters, and derive comparing a derived fact's same_packing files from the checkout; added and tested. The source's own programs are not needed: the routes decide the certificate itself; all were read, none ran. Third route (check_half_angle_area) belongs to its own review lane, not run. Then a mapped AI review, as precedents.

## Stage 2 and the replay

- **Packet:** the whole tree at the pin, 7 files, 485,671 bytes, all pinned only, including 01-squares-project.zip (d3b65052...). The README lists all 33 zip members with digests (each equals the zip's own manifest.json); nothing retained. Fact facts/n-207.yaml.gz (stored SHA-256 8a561c4c...).
- **Why two packets:** each issue pins its own revision (9dc93b6, bc328a7); each import has its own issue, bead and register entry, and a report.json declares one issue. bc328a7 contains the n207 files unchanged, so the n153 packet pins only the paths bc328a7 changed.
- **derive:** read n207.cert.json (1c334f31...) and, as the row's same_packing file, pingyou-n207-rational.yaml (09e6d0df...) from the checkout: the witness states all 207 poses and the side exactly; admitted at the issue's exact fraction. derive --check passes.
- **compare:** below the case and T-136; smallest: this certificate (claims.json frozen at main 3a5a91a90).
- **certify --workers 1:** 3 jobs; the positive passes both routes and both controls are refused; 127,926 pair decisions, 54.66 route CPU s, 103.49 job wall s, longest 40.08 s; run 20:48:22Z to 20:50:15Z. Both routes: least wall clearance 1/20000000000, least pair gap 19999999989999999999016010000001601/2e44, equal to the source's native-replay.json. check --replay: exit 0, 2 min 10 s.
- **The issue's 5b0eb012 claim reproduced:** packing-witness verify --json and check_rational_witness_independent (unchanged 5b0eb012 to 3a5a91a90; the seven checker files the package's manifest names have its digests) on the pinned witness bytes: both pass, 207 squares, 21,321 pairs, same margins, about 13 s and 6 s. Outputs not retained.
- **register-plan:** printed, T-NNN at V0/C0, proposed significance 3, credit "PingYou Ltd after Xu, Daniel, Levy", lineage builds-on-project. Shared records not edited.

## Draft acknowledgement (2026-10-11, not posted; the owner posts it)

@BuddenPing, thank you. We received the n = 207 certificate and pinned BuddenPing/square-packing-certificates at 9dc93b6ac2f8fefe038062a74c9a75bf05afdba6; `n207.cert.json`, `pingyou-n207-rational.yaml` and `01-squares-project.zip` have the SHA-256 digests you give. The certificate's exact side is the one you state, and your Witness/v2 states exactly the same 207 poses and side. It is below the ceiling the n = 207 case holds today, and below SQUISH's pending #481 certificate by the margin you give; no other report names n = 207. The repository states no licence, so we keep digests and an exact fact derived from the certificate rather than your files. Next we will replay the certificate exactly by this repository's two maintained routes, with duplicate-square and outside-container controls, and review the replay; your scripts are not needed for that and will not be run. Credit will read PingYou Ltd for the n207 assembly, after Ryan Xu's n70 construction and Evan Daniel's exact n70 certificate, as you ask. One question: the first version of this issue and commit 0d8b9c1 said OpenAI Codex assisted the verification, the comparison review and the package, and commit 9dc93b6 removed that sentence. The issue template asks for the author's own account of AI assistance; which account should the record carry?
