---
type: is
id: is-01m5jn36mh8x87f540ps2bc4jr
title: "Gate: every registered result at S4 or S5 has a News item (records tier + CI), and the runbook makes it a same-PR step"
kind: task
status: open
priority: 0
version: 2
labels:
  - process
dependencies: []
parent_id: is-01m5jn336nm6erpp0ygedhgpva
created_at: 2026-10-22T20:33:29.233Z
updated_at: 2026-10-22T20:52:22.233Z
---
c-lane-announce-1022, branch claude/news-gate-s4-s5. Includes T-194's News item and the decision on the 13 September S4/S5 results. Epic think-s38d.

## Notes

2026-10-22T20:50Z, c-lane-announce-1022: pushed claude/news-gate-s4-s5 at 2260fb10f (gate + T-194 item + runbook), on main 59b1ec594 (#729 merged in).

ROOT CAUSE (for think-jlra). A News entry in packing/site-changelog.yaml can name only merged PRs: render_changelog.validate requires a retained delivery (merged_at, merge_commit) for every PR an entry lists, and the entry's date must equal the latest merge date of those PRs. So a result's News item can never land in the PR that registers it, only in a follow-up after the merge. The runbook (result-import.md, Label the PR and Prepare News; Verify the Published Result step 6) said to draft the item before merge and "complete the prepared News/changelog disposition in the next change", and nothing checked that the next change happened. For T-194 it never did. Its PR #651 (labelled S5, merged 2026-10-16T17:49:19Z, merge 26d8bb335) was never imported into `deliveries` at all, and the coverage audit (coverage.pull_requests) covers only PRs someone imports, so an un-imported PR is invisible to every check. Meanwhile the home page box (S5 only) kept showing the 13 October item.

GATE. render_changelog.check_announcements, run by `render_changelog --check --baseline-ref origin/main --announcement-base REF` in the records tier's "synopsis agrees with the artifacts" step (fast, so PR CI runs it). REF is origin/main on a branch and HEAD^1 on main. Every registered result at S4/S5 needs a News entry that News shows (score >= 3, no news_exclusion), scored at least the result's score, with the result in result_ids. Grace: a result new or raised since the merge base is printed as owed and does not fail. Once on main, every later check fails, naming the result, its score, the merged PR (from first-parent history), the import_changelog command and who scored it. ANNOUNCEMENT_EXEMPT lists 15 results with exempt scores, citing 6279bd0e6. Stale exemptions fail.

T-194 ITEM: id fitzharding-n19-reported-proof, dated 2026-10-16 (#651's merge day), S5, with the result page and publication evidence from the Pages verify-deployment job of #651's merge (run 38942623017, job 117129620456: result/t-194.html HTTP 200, 4533 of 4533 checks).

EXEMPTION: 15 results, the 13 September ones plus T-064 and T-081 (S4, landed 1 and 3 Oct, named only by the S2 entry evan-daniel-attribution-corrections, which News does not show). The archive was created 13 October (6279bd0e6); T-060's 30 September item was a 15 October backfill.

FOR think-2252: of the 28 PRs labelled S3+ and merged into main since 2026-10-13 (gh pr list, label S3/S4/S5), 11 are not in site-changelog.yaml `deliveries`, all S3: #578, #620, #621, #644, #645, #657, #671, #688, #692, #699, #708. #651 (S5) was the twelfth, and is imported on this branch. Unlabelled PRs were not counted.

OTHER PRs: #725 at 3d43e15da (T-226/T-227 S2->S3) and #731 at ef005f489 (T-230 S3) give no failures and no owed notes, on their branch or on main.
