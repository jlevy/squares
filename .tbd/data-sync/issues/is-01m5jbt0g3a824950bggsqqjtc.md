---
type: is
id: is-01m5jbt0g3a824950bggsqqjtc
title: "Site: continuous deployment identified by its git revision; drop site editions and DATA_REVISION (papers and art keep versions)"
kind: feature
status: open
priority: 1
version: 3
labels:
  - release
dependencies: []
created_at: 2026-10-22T17:51:10.847Z
updated_at: 2026-10-22T18:27:18.830Z
---
Owner decision, 22 October 2026 (in conversation with the coordinator coord-intake-1021b):

"We don't have any real value in committing a synthetic version for the site. Paper and art artifacts should have versions, but the site itself should have continuous deployment and potentially just the git revision of the current site."

So:
- The site has no edition numbers. It deploys continuously from main and identifies itself by the git revision it was built from (injected by the deploy workflow, e.g. GITHUB_SHA; no Git read at render time; local renders say so).
- Papers (the n11 explainer and the three review papers) keep editions, cut in the PR that changes them.
- Art (atlas posters/infographics, films) keeps versions.
- DATA_REVISION and the site's PUBLICATION_HISTORY / RELEASE_IMPACTS / no-change records for the site go away; the existing site history stays as history.

Evidence for the change: scratchpad/release-design/proposal-release-pins-after-merge.md (11 PRs: 85 of 210 commits were release bookkeeping, 30 re-pins, 6 re-cuts, 12 site cuts; #722 and #724 both cut site v0.9.1; 26 claim-document records exist only because site cuts moved PUBLICATION_REVISION).

Coordinator's proposed defaults (owner may override): claim documents link at their paper's current edition commit and move only when that paper is cut (keeps think-lci1/F8); News groups by date; footer shows short SHA linked to GitHub plus build date; `landed` unchanged for now.

Next: an implementation spec (c-design-release-1022), then a writer lane. In-flight PRs (#722, #724, #725, #726, #406) merge under the current rules first.

## Notes

2026-10-22 18:00Z coord-intake-1021b: the owner refined the decision in conversation: "Going through the needless ceremony of assigning a version number to every deployment of the site is going to slow down all work, and that's not necessary. Let's remove that going forward." and "We should have a process for whenever we're releasing a snapshot of PDFs, the video, and so on. Since those are distributed, they need a version."
Reading: versions are assigned when a snapshot of distributed artifacts (paper PDFs, videos, posters) is deliberately released, by one defined release process; not in ordinary PRs, and not per content change. The site (including the papers' web pages) deploys continuously and shows its build commit. Claim documents' link commit moves at snapshot release time.

2026-10-22 18:35Z c-lane-release-pr1-1022 (for coord-intake-1021b): PR 1 of the implementation spec, "Stop cutting site editions", is open as draft https://github.com/jlevy/squares/pull/729 (branch claude/release-stop-site-editions, head 1d35cd517, based on main 78dc902c1). check_release_impact never selects the site and refuses any edit to the frozen PUBLICATION_HISTORY or PUBLICATION_REVISION, or a fresh site release-impact decision, with one message naming this bead; cut_release --component site refuses with the same message; release.py gets a docstring freeze note and freeze comments only; test_release pins the history at v0.9.1. Docs: development.md (Cutting an edition, Merging a Pull Request bullet 1, the changelog's release-impact paragraphs, Publishing the Explainer), result-import.md stage 5, and packages/workbench/README.md step 2. DATA_REVISION, release_pin, the footer, landed and paper/poster rules are untouched (PRs 2 and 3). Local: ruff/basedpyright 0 findings on changed files; 144 tests passed; records tier 52/52 at --jobs 2. If #722 (or another PR) lands a later site edition first, merging main into #729 moves FINAL_SITE_EDITION in test_release to it; open PRs still carrying a site cut must otherwise drop it.
