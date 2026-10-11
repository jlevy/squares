---
type: is
id: is-01m47d1ey7r49t9x8zdj5yarqw
title: "sqverify-fast: the crate in the tree is not the reviewed source; re-review the declared-net diff or pin the replay build"
kind: task
status: closed
priority: 1
version: 5
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m47hea1vkqx8h5wzdzcyqs5k
hold: null
hold_until: null
created_at: 2026-10-06T01:25:23.015Z
updated_at: 2026-10-06T04:39:56.232Z
started_at: 2026-10-06T02:45:49.713Z
closed_at: 2026-10-06T04:39:56.232Z
close_reason: Re-review accepted main's crate d97758bb for declared nets (307d934aa, ae2c8e452); DR-1 to DR-3 fixed and confirmed; merged at f342dff82
resolution: null
duplicate_of: null
---
f007d7afd and 910b6b12c (the declared-net change, lemma N0; 910b6b12c never reviewed) mean a build of packing/sqverify_fast/ today has a source_sha256 outside REVIEWED_SOURCES, so the census --evidence template ('cargo build --release in sqverify_fast/') and T-094's replay entries describe a build the route review did not accept. T-097's replay ran the reviewed binary (af0871c0, source 7c49cf79, as at e020eb1e2). Either: a soundness re-review of the declared-net diff that adds its source digest to REVIEWED_SOURCES, or make the replay command name a build of the reviewed source (e.g. a git worktree at e020eb1e2). Until then every further carry of the route (T-082, T-090, T-091) must use a reviewed-source build.

## Notes

2026-10-06 04:50Z, lane R1, done on claude/ecstatic-pascal-pothtx-r1 (not pushed).

Diff: crate e020eb1e2 (src byte-identical to 4ddf37d9c) -> main 34e87a86b = f007d7afd + 910b6b12c; src changes only in certificate.rs (+98 -8), lib.rs (+3), rotated_tests.rs (+1); Cargo.toml/Cargo.lock/build.rs/toolchain unchanged. build.rs digests: 4ddf37d9c 9985c465, e020eb1e2 7c49cf79, f007d7afd 73959cae, 910b6b12c = main d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88 (devtools.check_sqverify_fast.crate_source_sha256, census --source-digest).

Review (claude -p tbd-strong opus-5-5, executing): review-2026-10-06-sqverify-fast-declared-net-soundness.md (307d934aa, sha256 787e6b03): accept d97758bb for standard nets; declared nets once DR-1 (mixed_exact on the standard step) and DR-3 fixed and DR-1's fix read. DR-2/DR-3 evidence text. Fixed at 36b52538a (also fixes think-q9gu). Re-check review-2026-10-06-sqverify-fast-declared-net-fix-check.md (ae2c8e452, sha256 c1cf89df): accepts fixes and the declared_nets flip; FC-2..FC-5, FC-7 folded in. 11f0a8d24: link checker skips fenced code (the re-check quotes a SYNOPSIS row). 8c29ed626 re-pin.

Open: think-0uia (FC-1, control's 99/100 at one direction; mixed_n18_L470 CONTROL_FAILED, R2 reports its two pass), think-dtun (DR-4), think-2uc1 (DR-7).

Validation: measure verifier Rust, ruff, basedpyright, --records pass; census pytest 28 passed; reachable tests 4553 passed, 7 failed (2 known container, 5 browser floor: typescript-eslint missing from node_modules).
