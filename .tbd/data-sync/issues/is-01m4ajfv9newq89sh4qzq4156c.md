---
type: is
id: is-01m4ajfv9newq89sh4qzq4156c
title: "W7: strict SQUISH #401 import and exact dual-checker receipts"
kind: task
status: closed
priority: 1
version: 10
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4ajdxfkfqyr1yj5d4wm5npt
hold: null
hold_until: null
created_at: 2026-10-07T06:58:20.597Z
updated_at: 2026-10-07T19:08:23.758Z
started_at: 2026-10-07T06:58:30.243Z
closed_at: 2026-10-07T10:17:57.693Z
close_reason: Local engineering complete at reported 463203adf and confirmed 9ce8ac8ea; validated source, reader, cost and recovery/rebase deliverables. Parent retains pending full checkpoint and HTTP403-blocked publication.
resolution: null
duplicate_of: null
---

## Notes

Local engineering implementation and verification complete; leave in_progress pending parent publication and CI. Added bounded strict SQUISH source parser/acquisition, exact half-angle conversion via public existing adapter helpers, dual exact deciding routes, deterministic compressed derived facts and certificates, bound verification receipts, source provenance checks, and fast/replay commands. Full bound recertification: 45.990 wall seconds with 2 workers. Full deterministic replay: 76.122 wall seconds serial; all eleven n=108,126,129,130,153,154,155,180,209,238,303 and both overlap/container controls pass expected outcomes; 177440 pair decisions per checker across positive cases. Final 40 tests passed in 2.92 seconds; Ruff and BasedPyright zero findings, fast artifact check passed. Fixed reviewed duplicate roster handling, tuple/list control replay mismatch, stale checker-input evidence binding, source provenance drift, and inconsistent verdict/clearance receipt fields, each with targeted tests. Runtime cost: final certification plus replay 2.04 wall minutes; exploratory initial cert49.061s, failed replay79.676s, canonical replay138.650s, final recert45.990s, final replay76.122s = 6.49 wall minutes total engineering geometry runs (reviewer runs additional). Source producer executable absent and never claimed reproduced. Raw upstream bytes not retained; source/fact/certificate hashes protect acquisition and checker-input trust boundaries, no Git code fingerprints. Packet packing/resources/web/squish-401-2026-10-07; witnesses packing/witnesses/squish-401-2026. Registration tests test_squish_upper_bound_packets.py; confirmation artifact tests test_squish_upper_bound_receipts.py. Reproduce from packing with uv run --frozen python -m devtools.squish_upper_bound_packets certify --workers 2, then check --replay. Remote tbd sync remains known divergent/push403; preserve local notes and all beads in outbox. Parent handles separate PRs, issue comments, final bead disposition.

Follow-up after broad registration pre-push: the original gate had 33 failures and 171 errors, largely a stale HEAD-tree cache before the packet commit. On the committed reported tree, fixed genuine historical-source/current-selection interactions without bypassing old certificate verification: source_supersession guards only document/frontier ownership; historical Kingbird/Evan/Couzo source parsing and all geometric deciding tests still run. Coverage overlays preserve unowned sources and stable ordering. Generator genuinely redrafts historical inputs, then adopts owned SQUISH geometry from exact facts, normal lower lanes/prose, reviewed source/history additions and later rigidity promotion. S5 whole-record no-op removed, with reported/confirmed refresh, bound/body/lower drift, absent-declaration refusal, earlier-source ownership and integer rational regressions. Added required verified-ceiling/new-report gap prose to eleven cases; parent subsequently refreshed current-pose rigidity, case files then frozen. Source-repository/issue-comment cards and per-square color contracts follow current geometry; frozen pre-import 56-ceiling census remains explicitly audited from old receipts. Regularized generated witness snapshots pruned (about2.9MB) with192MiB cap unchanged.
Validation: implicated source/parser/generator/color/overview suite556passed plus one discovered GitHub issue website-card contract mismatch,130.44s; that defect fixed and covered by final20regression/ceiling/source-card tests passing12.14s, plus separately10 targeted tests8.00s. All11 selected SQUISH cases now regenerate with0disagreements. Prior25 residual tests passed6.91s. Ruff/BasedPyright clean for all17 engineering-owned changed/new files. Kernel /proc profiler reproduced with required escalation:1passed0.75s. Remaining worker-index issue is untracked new source/test files until parent stages them; parent owns integrity-policy and rigidity floor changes. Logs:/tmp/squish-followup-final-focused.log,/tmp/squish-followup-final-regressions.log,/tmp/squish-followup-last-fixes.log. No confirmation checkout edits, commits or feature branch pushes by this lane. Bead stays in_progress pending parent publication and CI; tbd sync again push-denied and automatically saved outbox.

Adopted-state integration follow-up: made the confirmation display regression fixture valid from both reported and confirmed case records by replacing the source display exactly once, removing an existing verified-display declaration, and injecting exactly one deliberately stale declaration. Production code unchanged; missing-display refusal assertion retained. Reported6affectedtests pass4.06s; confirmation8SQUISH/adoptiontests pass3.65s,91deselected. Copied only this test file into confirmation at parent explicit instruction. Ruff clean. Logs /tmp/squish-fixture-reported-final.log and /tmp/squish-fixture-confirmation-final.log. Parent owns commit/publication and bead disposition.

Final gate follow-up: repaired confirmation local Node dependencies with repo-prescribed npm ci --no-audit --no-fund (96packages2s), because root-package links omitted packages/workbench/node_modules/typescript-eslint8.68.0. No tracked manifests/lockfiles changed. Browser-floor rerun passed2selectedsteps103.84s; liveness56passed44.68s (/tmp/squish-confirmation-browser-floor-repaired.log).
Reported broad progress isolated two genuine result-overview failures: T-114 canonical issue401 comment citation misclassified as a repository file requiring blob/tree/main. Shared strict exact host/repository numbered issue/discussion+correctly typed comment predicate now classifies these source reports as external citations. Arbitrary IDs, mismatched comment types, host/repository impostors, query/path extensions and file links cannot use exemption. Existing branch/hash-pin/tree-path checks unchanged; meaningful combined negative-control test retains their refusal outputs. Four changed files devtools/repo_links.py,devtools/result_overview.py,tests/test_repo_links.py,tests/test_result_overview.py, copied only code/tests into confirmation as parent directed. Senior static acceptance and independent18tests passed2.39s; reported full affected56tests passed46.07s, confirmation56tests passed65.24s. Ruff/BasedPyright clean. Initial failed two-test reproduction24.83s retained /tmp/squish-reported-result-link-reproduction.log; fixed logs /tmp/squish-reported-result-link-fixed.log and /tmp/squish-confirmation-result-link-fixed.log.
Third broad failure was pre-existing paper-test expectation drift: REVIEW_FIGURES[PAPER] expected11 while current n11-optimality-review article has12 figures. Endpoint figure body blamed to e37362ff9b Sept30, explicit Figure12 caption to d7a55fa324 Oct5, before SQUISH import. Read-only standalone reproduction1failed74.42s (/tmp/squish-reported-glyph-reproduction.log). Parent authorized two-literal test-only correction to12 and explanatory twelve drawings in tests/test_site_glyphs.py, copied to confirmation. Full original figure assertion now exercises every styling/centering/caption requirement and passes: reported1test53.56s, confirmation1test52.44s. Ruff clean; paper/glyph/layout/geometry code unchanged. Logs /tmp/squish-reported-glyph-count-fixed.log and /tmp/squish-confirmation-glyph-count-fixed.log. Source/test freeze delivered; parent owns common-source commits, rebase, incremental pre-push against d48bcd365 and final CI/publication/bead disposition.

Final column-layout integration follow-up: reproduced confirmation result-table failure on index.html at1280 with result cuts=[]/stranded=[]/broken=['562949953421312,'] (1failed51.05s, /tmp/squish-result-columns-diagnosis.log). Exact cause: plain Unicode ≤ in T-114 headline meant ASCII-oriented prose math recognition rendered only bare s(153), leaving long rational denominator as ordinary breakable text. Parent approved data-only canonical inline-code math presentation for exact unchanged T-113/T-114 expressions in both results.yaml files. Records confirmed existing convention; senior Astra semantic review accepted that removing delimiters recovers prior text exactly, n153 fraction matches retained fact.side, and existing converter emits numerator\mathbin{/}denominator. No bounds, claims, case/source quotations, count scopes, rungs, styles, layout guards or geometry changed. RESULTS regenerated but byte-identical; SYNOPSIS/research outputs likewise unchanged. Registry checks pass both; prose3tests pass both1.19/1.23s; math-markup checks pass both2.01/1.62s. All six original failing width/page assertions now pass with legal-break, no broken-word and no stranded-punctuation constraints intact: confirmation6passed51.38s, reported6passed43.33s (73deselected each). Logs /tmp/squish-confirmation-columns-fixed.log and /tmp/squish-reported-columns-fixed.log. Source/data freeze sent parent; parent owns commits/pins/rebase and serialized gates.
Read-only suite cost-record failure also diagnosed:625files44unrecorded, shard4=15/149=10.1% over unchanged10% threshold. Existing suite_files lacks additive merge; admission must use actual successful measurements, not manual invented weights or fabricated hosted cohorts. Scope/validation findings and six-new-module roster handed to records agent, who owns reusable local admission tool/tests/dataset and fresh measurements. No suite tool/data edits by this lane. Engineering bead stays open pending parent disposition and CI.

Local engineering completion (7 October 2026)

The engineering source, reader integration, recovery/rebase, and measured-cost
handoff are complete. Reported source is committed at
463203adf56ecb347f9abc83ee1295158efe7c32. Confirmation is committed at
9ce8ac8eaf16b2bd0f25ef2d5f50b803bfcc3eb0, with the same source ancestry,
complete exact-replay evidence, accepted mathematical reviews, confirmed V3/C3
claims, and six genuinely measured module-cost admissions. Current receipt
binding uses bounded exact semantic geometry; generated-file self-hashes are
not the integrity boundary. No source-producer executable was available or
claimed replayed.

The final reported broad gate ran 973.31 seconds: 6,652 passed, 30 skipped and
one expected failure, with one failure from the stale four-entry long-quotient
test roster. T-114's 31-digit fraction correctly rendered a binary solidus and
clean semantic MathML. The three-line roster/comment correction in 463203adf
passed Ruff and whitespace checks. The subsequent incremental push gate
completed all 61 steps, with 3,348 passed and 19 skipped, in 493.86 seconds.
No style, geometry, layout floor, collection threshold, or timeout was loosened.

Confirmation was backed up and rebased twice without scientific drift. All 50
confirmation scientific/editorial/cost paths remain byte-identical to the
pre-final-rebase tree; only the test roster and refreshed release pin changed.
The final release-pin check passes (last data commit cbc03234e548). Recovery
retains a complete 831 MiB Git bundle, incremental bundles, binary patches,
raw indices, pending outbox/native notes, and named stashes outside checkouts.
Backups are /workspace/squares-401-confirmation-backup-20261007T091449Z,
/workspace/squares-401-confirmation-final-backup-20261007, and
/workspace/squares-401-confirmation-quotient-backup-20261007.

Close this child for completed local engineering at the parent's instruction.
The parent bead owns the still-running full confirmation checkpoint and remote
publication. Feature push was denied HTTP 403; no PR or issue comment was
published. The full checkpoint is monitored read-only, with no extra browser,
proof, or test processes started by this lane. Preserve this distinction when
reporting completion.
