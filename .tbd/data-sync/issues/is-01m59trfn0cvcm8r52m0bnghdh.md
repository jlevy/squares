---
type: is
id: is-01m59trfn0cvcm8r52m0bnghdh
title: "PR #578 F1: detach cached articles from response shells locally"
kind: task
status: closed
priority: 3
version: 5
delegate: codex-578-f1-fix-20261019
labels: []
dependencies: []
parent_id: is-01m59tb83e779xjn19g896fa78
child_order_hints:
  - is-01m59v8t4axh5110qn5f89364m
hold: null
hold_until: null
created_at: 2026-10-19T10:19:19.582Z
updated_at: 2026-10-19T10:28:14.601Z
started_at: 2026-10-19T10:19:51.499Z
closed_at: 2026-10-19T10:24:41.957Z
close_reason: F1 fixed locally in9812f19afba96325547ec02644cab03d138c4b67 with red-green ownership regression and29passing Node tests; coordinator owns integration/CI/disposition publication.
resolution: null
duplicate_of: null
---
Address published Review F F1 (Low) at PR578 head b76a24fd29bdab28b5c946adeff88313fd28eb47, review5570079896. Sole committer in existing full checkout intake-review-20261018, new local branch codex/578-cache-fix-20261019; preserve all existing branches and never touch the external owner checkout. Detach article only after awaited math-style discovery. Add a red-green ownership regression for detached cached article, distinct clones and one fetch while preserving style discovery/promise caching/ID scope. Run focused existing Node/article-loader tests and changed-file floor, normal-hook local commit only. No push, comments, PR edits, CI dispatch, prospective671 merge, downloads, environments or broader performance/research/build work. Root coordinates actual671main, final integration/review/CI/publication.

## Notes

F1 fixed locally in commit 9812f19afba96325547ec02644cab03d138c4b67 on codex/578-cache-fix-20261019, clean existing full checkout .worktrees/intake-review-20261018. Parent is exact reviewed PR578 head b76a24fd29bdab28b5c946adeff88313fd28eb47; no prospective671 merge. The checkout was clean/detached at f319 before the explicitly requested new branch was created, preserving all existing branches. No other checkout or external-owner chat was touched or messaged.

Trust verified live before execution: gh pr view578 and gh api pulls/578 report author jlevy, isCrossRepository false, author_association OWNER, head b76a24fd29bdab28b5c946adeff88313fd28eb47, base e952755bcad005738785ab8bab0d0b7176f34fed. Read root .codex/intake-resume-20261019/578-performance-F.md, formal Review F https://github.com/jlevy/squares/pull/578#pullrequestreview-5570079896, F1 Low only. Workflow entry tbd shortcut address-pr-review; explicit coordinator local-only scope overrides push/comment/CI steps. Own fresh child claimed as codex-578-f1-fix-20261019 with claimed=[think-rkkb],skipped=[]; re-read before final update confirms already-yours and same delegate. No existing owner bead was taken.

Minimal change in packing/devtools/overview/article-loader.js: article.remove() immediately after await loadMathStyles(parsed.content,responseUrl), before returning the cached canonical article. Existing promise cache, pristine cloning and ID scoping remain. The existing Node row/article-loader fixture now retains original parsed shells/articles, and the cached-heading regression verifies attachment while stylesheet load is pending, original parent null after load, no article left in shell, distinct consumer clones, pristine cached heading and per-consumer scoped IDs, one parse/fetch. Only this source and packing/tests/node/overview_rows/row-popover.test.mjs changed, 24 insertions/3 deletions; no broader performance work.

Red-green evidence: node --test --test-name-pattern='cached articles detach' packing/tests/node/overview_rows/row-popover.test.mjs failed1/1 before the fix at 'the cache retains no response shell', actual fragment parent versus null. After the one-line fix, node --test packing/tests/node/overview_rows/row-popover.test.mjs passes29/29, zero skipped/failed, Node v24.19.0. Changed-file Biome ci --error-on-warnings passes2files; tsc -p tsconfig.overview.json and tsc -p tsconfig.devtools-node.json pass without diagnostics; changed-file promise ESLint with packages/workbench/eslint.config.js and --max-warnings0 passes. git diff --check passes. Normal lefthook passed in2.67s, Biome2files/no fixes; Markdown hook correctly skipped because no matching staged files. No bypass.

Durable test receipt /Volumes/spud-ext1/agent-source/squares-pr578-f1-20261019/receipt.json, with red.log and green-suite.log beside it. Temporary/cache env explicitly set to mounted external scratch: TMPDIR task/tmp, own cargo-intake-review-20261018 target, existing UV_CACHE_DIR, pytest failed/1 retention. Existing external node_modules reused; no downloads/new environment/clone/worktree/build/PDF/browser/geometry replay. No heap-byte, GC or latency improvement measurement is claimed; this fixes static DOM ownership.

Disposition fixed, LOCAL ONLY. No push, PR edit/comment, disposition reply or CI dispatch; no new-head CI runs or reply URLs exist. Root owns actual671main, subsequent integration, release/pins, follow-up review, fresh CI and final marked F1 disposition publication. Await root's next instruction before integrating actual main. Original review parent think-j39i remains untouched/closed by its owner; no other review finding was addressed outside the named brief, and no additional publication discovery sweep was claimed.
