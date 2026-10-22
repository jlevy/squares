---
type: is
id: is-01m5jbt0g3a824950bggsqqjtc
title: "Site: continuous deployment identified by its git revision; drop site editions and DATA_REVISION (papers and art keep versions)"
kind: feature
status: open
priority: 1
version: 2
labels:
  - release
dependencies: []
created_at: 2026-10-22T17:51:10.847Z
updated_at: 2026-10-22T17:52:53.411Z
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
