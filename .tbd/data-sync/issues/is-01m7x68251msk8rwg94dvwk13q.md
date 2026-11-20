---
type: is
id: is-01m7x68251msk8rwg94dvwk13q
title: "Stage 4 blind review of #1052's s(305) certificate"
kind: task
status: in_progress
priority: 1
version: 8
delegate: r1052
labels:
  - intake
  - validation
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T19:17:02.241Z
updated_at: 2026-11-20T20:36:37.354Z
started_at: 2026-11-20T19:17:10.691Z
---
R-1052: blind stage 4 review (packing/campaign/result-import.md) of Joost de Winter's s(305) <= 17.945755838742 certificate (JoostdeWinter/square-packing n305/, data db8efcb, registration 5282edd), the review lane's own bead. Clean-room exact checker (two methods sharing only the reader) and pre-stated controls frozen and pushed before any program reads the certificate; findings frozen; then custody, record at 305 (T-309), identity, option D contraction facts, credit facts, significance proposal, questions. Branch claude/intake-2026-11-20-review-1052; review docs/project/reviews/review-2026-11-20-de-winter-1052-n305.md. The import lane (think-kzwl) is not read before the findings freeze.

## Notes

R-1052 (blind review), lane r1052, 2026-11-20T19:25Z. Created and claimed think-d788 (claimed [think-d788], skipped []). Worktree scratchpad/r1052, branch claude/intake-2026-11-20-review-1052 from origin/main ee3a7fc7dd (no upstream set; push only, no PR). Issue #1052 read via REST at 19:17:22Z (opened 17:51:36Z, 0 comments, label intake). Source JoostdeWinter/square-packing via a blobless bare clone (commits and trees only, no blobs, `git ls-tree` without -l): n305/ added in db8efcb (18:50:11+01:00), REGISTRATION.md and SHA256SUMS added in 5282edd, head 20b6f0e; certificate blobs unchanged across all three: n305_exact.json 355cbe46ff685c00c1bb292443b974084dc0b9c4, n305_witness.yaml 58ab84e20c2eb6d533f59d8f3141de3d4bfbf4f1. No blob fetched. Writing the clean-room checker in packing/resources/web/de-winter-n305-1052-review-2026-11-20/programs (not yet frozen; no program has read the certificate). Disclosure: `tbd list --parent think-p02d` printed the import bead think-kzwl's title once; nothing else of it read.

R-1052 19:44Z: checker and controls plan frozen at 19:42:44Z (frozen/checker-frozen-digests.txt: the two certificate blob ids from the source tree; ten programs and the plan; the self-test receipt, PASSED 608 checks), committed 1e5214e631 and pushed to claude/intake-2026-11-20-review-1052 at 19:43Z. Before the freeze the programs ran only on synthetic packings (self-test; 18 mutations; controls on two synthetic two-form certificates, 51/51 each). Blobs fetched by id into an empty directory at 19:43:38Z: n305_exact.json 289,792 bytes sha256 e6c7d028...831f, n305_witness.yaml 1,144,100 bytes sha256 b11a6e65...1a46. Running the frozen check now; then controls, describe, findings freeze.

R-1052 20:17Z: findings frozen at 20:16:13Z (frozen/findings-frozen-digests.txt), committed c686263343 and pushed. Frozen check on the files as published: REFUSE only because the reader refuses n305_witness.yaml (softschema block has only `contract`; no Witness/v2 `claim` block, which the schema requires); form J ACCEPT by both methods. r1052_envelope_copy.py (post-checker-freeze, decides nothing) inserts `envelope: witness` and a 3-line claim block, proved to be the only difference; frozen check on J + copy: ACCEPT, twin holds 305/305, files decide alike, claim box accepted. 46,360 pairs all apart, least margin 1.715e-82 (9,12), no contacts, no wall contacts (least clearances 1.5e-82 left/bottom, 1.66e-82 right/top); claim 17.945755838742 = 12-place ceiling (4.11e-13 above S). Controls 51/51 as stated (665 CPU s). Findings: F4 minor (witness metadata), F7 note (36 near-axis squares, sines 1e-30..2.1e-11). Next: custody, record at 305, identity vs T-309, contraction/option D, credit, significance.

R-1052 20:37Z: done; branch claude/intake-2026-11-20-review-1052 head 3fc1cea071 (pushed; no PR, per brief). After the freeze: custody holds (both SHA-256 = SHA256SUMS lines; blobs unchanged db8efcb..20b6f0e; issue states no digest). Record at 305: house T-309 (#1001) exact side 17.945762359658969613927895321035..., V3/C3, S3. Identity (devtools.measure_identity): one to one with T-309 under the identity, none beyond 0.1 (largest 0.0832, 201 beyond 1e-3, 63 beyond 1e-2), one turn of 7.27 deg, no tilt reversed; against the regularized drawing 3 beyond 0.1, largest 0.178, RMS 0.018 (the issue's figures). Contraction (devtools.contraction_margin, both routes accept): T-309 margin 1.906551e-10 (pair 130,137); gain 6.520917e-6 = 34,202.7x it; certificate 6.520727e-6 below T-309 shrunk to first contact -> new result under option D; certificate's own margin 3.204267e-81 (pair 9,12). Also 6.5207e-6 below JoeGun's numerical local minimum near T-309 (17.945762359467513364), so a different local minimum. Shadoks side-only 17.94575583874176 (issue) / 17.945755838742 (JoeGun README): claim equals the 12-place value; side 1.71e-13 below the 14-place one; context only. Credit asked: de Winter as improver of the Kodaj-JoeGun arrangement; facts support it. AI tool: issue says GPT 6.2 Astra, README/REGISTRATION.md say OpenAI Codex (F12 minor). Significance proposed S2 (6.52e-6, below T-188 9.29e-6 and T-239 9.89e-6, both S2). Findings: F4 minor (witness lacks claim block and envelope keys), F12 minor (AI tool naming; stray opening paragraphs in issue body), rest notes. Validation: packing-validate --edit 71/71 selected steps pass (exit 0, 398 s wall); --records 55/55 pass (131 s); synopsis/doc-map and soft-schema rechecked after the last commit. Hosted: only Branch mergeability runs on push (success at 1e5214e and c686263). Note for coordinator: the branch adds a SYNOPSIS row and a document-map row, so a PR from it meets the synopsis HTML budget until the raise lands; origin/main was still ee3a7fc at 20:36Z, nothing merged. CPU: review ~0.35 h; with validation ~0.7 h. Import bead think-kzwl had no notes/branch when this ended.
