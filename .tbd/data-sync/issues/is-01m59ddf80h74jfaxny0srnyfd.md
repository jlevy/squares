---
type: is
id: is-01m59ddf80h74jfaxny0srnyfd
title: "PR #671: integrate landed T195–199 stack, preserve census evidence, and qualify release consumers"
kind: task
status: in_progress
priority: 1
version: 4
delegate: codex-671-integration-20261018
labels: []
dependencies: []
parent_id: is-01m54ahqaf9t63nz12annpqy69
hold: null
hold_until: null
created_at: 2026-10-19T06:26:07.230Z
updated_at: 2026-10-19T06:46:48.175Z
started_at: 2026-10-19T06:26:17.042Z
---

## Notes

2026-10-18 PDT continuation, delegated engineering integration only. External source /Volumes/spud-ext1/agent-source/squares-671-retention-20261018 remains clean at reviewed89166716d492ae7e4e76f61550e80849dec7edc3. Small external scratch read/write passed with77GiBfree; required pre-edit records baseline reproduced expected oldT195 URL identity collision, then stalled at14/52 with multiple macOS uninterruptible-I/O children. Interrupted withSIGINT, exit130, confirmed child cleanup; no full records/push pass claimed. Coordinator authorized focused checks from internal source and hosted broad validation.

Own internal source checkout reused: /Users/levy/wrk/github/squares/.worktrees/review-668-math-20261018, new branch codex/671-main-reconcile at89166716d. Old codex/review-668-math branch a70bc1979 is preserved (18 commits not contained in main); no unique old source deleted. Current merge is staged and uncommitted, MERGE_HEADd167d4b86ec46f9af6fb37591794cecc3b31eb64, no unresolved paths. No remote push or PR mutation yet. Existing primary packing/.venv Python3.14.7 used read-only with explicit per-checkout PYTHONPATH/PYTHONDONTWRITEBYTECODE; external TMPDIR/CARGO_TARGET_DIR/UV_CACHE_DIR, failed/1pytestretention, no new environment/toolchain/cache/download/census.

Reconciled own18result IDs only toT200-217 (n91T211 before n90T212, n108T216V3/C3, other17V0/C0). Structural checks prove all199main result objects unchanged, own18objects unchanged except own ID/reference shift, all main evidence/verifier/source rows preserved. Retained packet+census bytes unchanged from891. Generated RESULTS/VERIFIERS/INVENTORY/SYNOPSIS217/research tables/t007audit/composite/bound citations refreshed. URL registry1037rows has historical+identity checks PASS; local full derive correctly cannot inventory absent atlas assets in sparse checkout, hosted full checkout must verify.

Focused validation: test_bound_citations selected3passed119deselected1.79s; RESULTS/VERIFIERS/SYNOPSIS driftchecks pass; release.py scoped Ruff check and format check pass; source integration diff whitespace check againstmain passes. All three unchanged papers rendered in memory against exactmain d167d4b86 (baseline checkout HEAD tree equal main; its unrelated AGENTS policy edit excluded). At common source-link revisiond167d4b86 all six outputs byte-identical: optimality HTML2200293/MD190399 chars, threshold HTML2411008/MD392963, methods HTML2097115/MD151177. Updated own no-change declarations for current surveyv0.2.3, not stale0.2.2. Comparison command /private/tmp/compare671-papers.py invokes maintained renderers, writes no site/build artifacts. Existing pinned KPress submodule515f4a08 source generator/CSS materialized minimally to satisfy sparse renderer inputs; do not stagevendor.

Coordinator reserves sitev0.7.28 for smallerPR679, so final671site must be0.7.29 after679lands; final release history/base/pins/claim-doc links/PRdescription/push/hosted CI/review remain pending. Current staged release is provisional0.7.28 againstd167 and must NOT be pushed as final. Explainer remains successorv0.4.8 overmain0.4.7. Next: receive exact679mergedmain from coordinator, complete current merge commit via normal hooks with existing env/no-sync, merge679main, reconcile site0.7.29/publication comparisons, commit data then one-line DATA_REVISION pin then publication revision/claim docs, push to existing remote head branch claude/intake-2026-10-17-lower-bounds-446, wait terminal CI, coordinate independent Astra review. No merge delegated.
