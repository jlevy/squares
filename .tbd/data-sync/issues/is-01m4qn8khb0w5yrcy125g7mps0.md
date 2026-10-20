---
type: is
id: is-01m4qn8khb0w5yrcy125g7mps0
title: "Read wand125/square-packing d4a1981 (sqverify_continuous v4, --resume), stream-verify and evand PR 7: nothing to import (no issue)"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-12T08:56:56.618Z
updated_at: 2026-10-12T08:56:56.618Z
---
Watched-repository read for lane W of the 2026-10-12 intake (think-mq0k); nothing on GitHub asked. Not an issue.

**Range.** wand125/square-packing main, one commit past the f30cc2c read (b4c030f11, think-xzob): d4a19815e2b0cca5faa562f00c7a80b93d3402ef (2026-10-12T01:29:29Z, Hiroaki Hosono, co-authored by Claude Opus 5.5), "tools/sqverify_continuous: v4, --resume for interrupted runs". Still the head at 08:46Z (git ls-remote). 7 files, all under tools/sqverify_continuous/: PROVENANCE.md, README.md, CONTINUOUS.md, patches/continuous.diff, src/main.rs, src/slab.rs, src/slab_tests.rs.

**What it changes.** v4, source_sha256 619b3c00bd918b329b4141c24ee30b027af7f88b86bcf2886e3c18855a61c7f5 (v3 was 1266a8b9...). Root lines are written as each root range ends and carry run_key, a SHA-256 over the input's digest, n, L, the build's source_sha256, --core, --tau, --eps, --last-t, the axis side, the cuts and --max-nodes. --resume PREVIOUS.jsonl takes over only verified root lines whose run_key, index and t range match, copies them with inherited_from, and always recomputes the axis patch; the summary reports inherited_roots, resumed_from and missing_roots. The author states the search and every verdict are unchanged from v3; a new test, resume_takes_over_only_matching_verified_roots. No certificate, density or n = 40 receipt changes.

**Map.** Nothing to import; new evidence for the tool think-xzob (#533) owns evaluating. For think-xzob: a review and replay now has v3 and v4 to choose between; since run_key binds the build, a v4 run cannot inherit v3 roots; a replay here should not use --resume on output it did not produce (the README says trusting a taken-over line means trusting the earlier run). The README's n = 40 receipts are v3's; the 4.4 CPU-hour price in think-xzob is unchanged, and --resume would let it run in interruptible slices.

**Also read, not on the default branch** (the sweep reads HEAD only, so nothing records these):
- origin/stream-verify (2b31528, five commits of 10 October from 22a23c8): a PASS-only streaming mode with classic fallback for tools/n17_bb_verifier, its receipt-equality tests on 3 fixtures and 17 mutants, and a large-certificate memory measurement. n = 17 verifier tooling under the n = 17 hold (think-x4v4); no certificate, nothing to import.
- evand/square-packing PR #7, open since 2026-10-11T05:59Z from wand125/square-packing-1 (valid7-followup): ValidTilt7 from the pose tree without Face, a LebMassBridge.lean, cost figures (Lean). Unmerged follow-up to PR #6 (060c1a1), the Valid7 kernel route to T-064's finite premise that think-0ayk owns; nothing to import until it merges.

Other wand125 repositories: square-packing-bounds, square-packing-density-bounds, valid7-independent-check, n17-bb-verifier, n17-certificates, square-packing-tools and the polygon-container repositories are archived (7 October); wand125/square-packing-1 is the fork behind evand PR #6 and #7.

Already tracked and not duplicated: #532 (T-142..T-144 replays), #534 (s(31) >= 2391/400), #536 (Lean s(59) = 8), #446 (think-eth9), #533 (think-xzob).

**Proposed intake-watch.yaml read** (for the records lane): read_through d4a19815e2b0cca5faa562f00c7a80b93d3402ef, read_on 2026-10-12, bead think-xzob (the tool is unretained and think-xzob owns it). Text in lane W's scratch file intake-watch-reads.yaml.

Close when the records lane lands the read.
