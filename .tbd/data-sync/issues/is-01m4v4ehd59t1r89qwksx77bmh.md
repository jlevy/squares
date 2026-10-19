---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: in_progress
priority: 2
version: 30
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-final-merge
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
child_order_hints:
  - is-01m57g2khg6prcesy0fyxf32gc
  - is-01m59ev56c1da5q51t9h5jxpg7
  - is-01m59eyytph14724m9yrwe5x3e
  - is-01m59gqa1rq6jbsah86qha7xtt
  - is-01m59gsv3bsj068eq0mbhnga56
  - is-01m59jfeg786bcnxfbrm0mmjq3
  - is-01m59kfzac51p79k9q2myr0t18
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-19T08:12:20.683Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

2026-10-19 review/integration: all source work is isolated at /Volumes/spud-ext1/worktrees/squares-profiles-review-20261018, branch codex/profiles-upstream-review-20261018. Original checkout /Users/levy/.codex/worktrees/1116/squares remains clean at e1f921bf0; main checkout belongs to another active agent and was not changed. Integrated385 upstream commits through2891494ee;14 original conflicts resolved, followed by two clean small merges. Pushed34fd06feaeaa374511d9c9423ca62cb7d65291bd to draftPR578. Independent Astra architecture/design review and final patch review found defects that were fixed: source-specific identity authorization, overlapping spans, native-panel request race, bounded evidence snapshot, T174 HTML size/link audit, parser callback signature and n29 historical writer replay. Source records/numeric preservation comparisons and50screenshot/25navigation checks are retained. Latestfocused checks:89result/preview tests,6writer tests(all53adopted contracts),35release-impact tests, browserfloor341Node tests. Original local broad gate did not complete; timing diagnostics remain open underthink-j13b. Final standardCI39220334742/Pages39220334772 and fullcheckpoint39220360885 are running at34fd06fea; superseded full39218248533 canceled after8passes, not a fullpass. Next entry: resolve any finalCI failures, publish prepared ReviewB and ReviewA dispositions, close fixed childbeads, update this handoff and sync. DraftPR not merged/deployed. Remaining population underthink-m7il:354unresolved spans,146PDFs awaiting fullcredit inspection. Previewhttp://127.0.0.1:8792/profiles/index.html opened in defaultbrowser. Durable evidence /Volumes/spud-ext1/agent-evidence/squares-profiles-review-20261019/; prepared ReviewB/PRbody in external task scratch tmp. No data repin needed for final tool-only fixes.
