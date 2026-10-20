---
type: is
id: is-01m577zabh9gk6ck6vqn70m9qp
title: "PR671 A3: restore hosted overview page-size budgets"
kind: bug
status: closed
priority: 1
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m573m7c33z407xbx74ytf0jt
hold: null
hold_until: null
created_at: 2026-10-18T10:12:31.728Z
updated_at: 2026-10-18T13:31:13.083Z
started_at: 2026-10-18T10:12:50.998Z
closed_at: 2026-10-18T13:31:13.083Z
close_reason: PR671 fixes published at89166716d with terminal green Packing/Pages CI and marked A/B/C dispositions; census/C1 remains open in protected think-f40c
resolution: null
duplicate_of: null
---
Own the A3 hosted page-size failure at PR #671 head 1b2cf7cfe15c4eec90d447bf3977a683d96dec1d: results.html 1,141,207 bytes exceeds 1,100,000 and result/t-174.html 305,917 exceeds 300,000. Scope is site rendering/budget surface with evidence, no frontier or release records, local commit only for coordinator integration. Separate external checkout squares-671-pages-20261018; reduce accidental repetition where possible and preserve content/accessibility.

## Notes

Local-only fix prepared at cd64e8b40365f44850c8007da6167461f0d5875b on codex/671-page-budgets in /Volumes/spud-ext1/agent-source/squares-671-pages-20261018; parent approved measured exceptions after strict browser evidence. Results table: 212 rows, 1141207 bytes, ceiling1250000; T174: 68 cases and89 unique history steps,305917 bytes, ceiling350000. No renderer/content changes; global2000000 ceiling retained. RED existing overview test fails1 in27.68s; RED producer6292/6294 with exactly these two failures. GREEN focused modules362 passed149.61s, overview producer6295/6295, URL history1032 rows0failures, Ruff and BasedPyright0findings; normal precommit hooks passed1.55s. Strict browser three runs at1280/390 light/dark plus noJS:24 JS+8static navigations, nofailures/no timing exceedances; allsample maxima CLS0.000673684,LCP576ms,longesttask153ms,blocking123ms. Raw evidence: /Volumes/spud-ext1/agent-source/squares-671-pages-evidence-20261018. Remains open pending coordinator cherry-pick and hosted CI; stage4 record adoption changes emitted bytes and requires final fresh measurements. No push, comment or merge from this lane.

Final PR671 disposition, 2026-10-18: published clean head 89166716d492ae7e4e76f61550e80849dec7edc3 on existing owner branch; PR remains draft, no merge/deployment/author message. Required local --push passed all69 selected steps in1266.55s real (1264.98/1800s tier), quick19,016passed55skipped1xfailed plus10pooltests. Normal hooks and unchanged ceilings.
Final exact-head hosted CI: Packing https://github.com/jlevy/squares/actions/runs/39130821839 SUCCESS; Pages https://github.com/jlevy/squares/actions/runs/39130821886 SUCCESS; mergeability https://github.com/jlevy/squares/actions/runs/39130818998 SUCCESS.31successful/28conditional-skipped checks; optional deferred run39130821909 correctly skipped without deep-gate label. No pending/failing check. Post-CI discovery found only original formal A/B/C, no inline or other review comments/issues.
Marked dispositions: A https://github.com/jlevy/squares/pull/671#issuecomment-6250490436 ; B https://github.com/jlevy/squares/pull/671#issuecomment-6250491767 ; C https://github.com/jlevy/squares/pull/671#issuecomment-6250493618 . A1-A6 fixed; B bounded integration complete; C1 deferred in open think-f40c for stage7 upstream author README correction/question. Source archive README/digest unchanged; no author message claimed. Only n108 V3/C3; other17 V0/C0; no fresh native coverage replay.
Final publication follow-up: ccb2 hosted Packing passed but Pages exposed23 PDFpages vs inherited22 expectation.34fd8b33f00623b0e8ad24c760f17a8072dc057b fixes expectation/comment;101 PDF/exporter controls pass20.68s and artifact reproduction passes869,900bytes/23pages/19embeddedfonts.89166716d492ae7e4e76f61550e80849dec7edc3 scopes three unchanged-paper decisions to exact helper path after six byte-identical HTML/MD comparisons; release-impact18tests pass6.70s/errors[]. Final hosted PDF/math/font/artifact/saved-print-geometry checks all pass.
Merge-order caveats remain: #661 retainsT195, this draft renumbers; sitev0.7.26 provisional against #676, explainerv0.4.8 and data pin reconcile after incoming changes. Separate open efficiency follow-up think-y3pe tracks fresh per-run external TMPDIR/nested pytest isolation. Durable receipts: /Volumes/spud-ext1/agent-source/squares-671-retention-evidence-20261018 .
A3 hosted overview gate restored by de9c57d85 (original cd64e8b403): prior362focused tests,24JS/8no-JS browser cases. Final local overview6327/6327; results1,141,460/1,250,000bytes, T174306,199/350,000, n108detail101,522/300,000, case148,574/300,000. Hosted final overview and Pages aggregate green.
