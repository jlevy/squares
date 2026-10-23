---
type: is
id: is-01m5jn36mh8x87f540ps2bc4jr
title: "Gate: every registered result at S4 or S5 has a News item (records tier + CI), and the runbook makes it a same-PR step"
kind: task
status: open
priority: 0
version: 6
labels:
  - process
dependencies: []
parent_id: is-01m5jn336nm6erpp0ygedhgpva
created_at: 2026-10-22T20:33:29.233Z
updated_at: 2026-10-23T00:44:34.658Z
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

2026-10-22 20:55Z coord-intake-1021b: PR #735 (https://github.com/jlevy/squares/pull/735, branch claude/news-gate-s4-s5, head 2260fb10f on main 59b1ec594): gate (records-tier synopsis step, render_changelog --announcement-base), T-194's News item with #651's delivery imported, 15-result pre-archive exemption (6279bd0e6), stage 7 'Announce a Significant Result'. Senior review A launched (c-review-735-A). Merge as soon as reviewed and green.

2026-10-22T21:07Z, c-lane-announce-1022: PR #735 (draft), head 652a06b43, merges main ffd0f4af7 (#724). Added since the first push: the gate prints a summary line ("announcements: 21 registered S4 and S5 results, 15 exempt from before the News archive, 0 owed after this merge, 0 missing"); tests for the postmortem's two rules (S2/hidden entries don't count; a raise to S4 is owed on its branch and fails once on main, exactly as a registration) in 13d7bec6d; the home box's tests now pin T-194/T-154/T-153, since T-194's item moved Ahmed's 30 Sept item off the S5 box. think-jlra's postmortem is committed as e593ac0c7 and mapped; one row is corrected to say what this PR delivers. Records tier at 652a06b43: 52/52 selected steps, 144 s. Hosted CI pending at the time of writing.

2026-10-22T22:05Z, c-lane-announce-1022: jlevy merged #735 at 21:31:58Z (bfc04b659) at head 652a06b43, before Review A's fixes; this lane did not merge it. The fixes are on follow-up draft PR #738 (claude/news-gate-review-a, cherry-picked onto bfc04b659), head 7907ec361, labelled S2. A1 option (b): an owed S4/S5 item fails only a change that edits results.yaml or site-changelog.yaml, and warns elsewhere; option (a) is think-n51k. A2: 10 gate tests, 26 of 26 mutants killed. A3: the exemption is frozen and may only shrink, and any score mismatch is stale. A5: a fresh release record (#735's record kept as history). A6: the C toolchain. A7 and the nit. Dispositions are posted on #735: https://github.com/jlevy/squares/pull/735#issuecomment-6352159306. Hosted CI on #738 was 29 pass and 1 pending at posting.

2026-10-23T01:20Z, c-lane-announce-1022: #738's own review A is addressed in 8d29be1dc, and the branch merges main e929137a8 (#725): head 633662a2a, hosted CI 31 pass / 28 skip / 0 fail (packing-required and pages-required pass). A1: on main (--announcement-base HEAD^1, MAIN_DELIVERY_BASE) an owed item only warns, even after a raced records merge; PR CI enforces. A2: the committed-edit test; 40 of 40 mutants killed. A3: the postmortem credits #738. Nits: reflow and re-render; release wording. Dispositions: https://github.com/jlevy/squares/pull/738#issuecomment-6354618978
