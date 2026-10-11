---
type: is
id: is-01m3w2epwv3nyche0sm30s17y6
title: "Release: name the site's version v0.5.0 once the stack has landed and the deployment is verified"
kind: task
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T15:48:44.044Z
updated_at: 2026-10-02T04:49:38.800Z
closed_at: 2026-10-02T04:49:38.799Z
close_reason: "The site's version is v0.5.0: jlevy/squares#291 merged as 8aaa411dc and deployed at 2026-10-02T01:07:03Z, every page prints v0.5.0-971e5f, check_published_site passed 848 of 848 on that commit, and #297 (0848631a8) recorded the deployment above PUBLICATION_HISTORY. No tag or GitHub release: the owner said on 2026-10-01 that releases matter only for generated assets (PDFs, films), and nothing on the site needs a v0.5.0 release (the posters are served from the site; the films stay on the v0.4.2 release, think-9xvt). The scope sentence's wording is the owner's to change and is listed on think-cv22. Procedure follow-up: think-be7y."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'after all land let's make sure we update the name of the version of the site to v0.5.0', and 'Make sure everything is deployed correctly first.' Order: (1) the remaining PRs land (#266, #271, #270, the coherence fixes); (2) the live site is verified from that main (check_published_site, every page 200, the paper, films, PDFs); (3) the version becomes v0.5.0. Today the version is the git tag and GitHub release v0.4.2: render_overview.FILM_RELEASE, the explainer template's film URLs, README's release link, the atlas stamp (v0.4.2-<data revision>, from release.py), and about 20 files in all name it. Work out what the release procedure is from development.md and release.py (tag, GitHub release with the film and poster assets or the films kept at v0.4.2 and referenced there, DATA_REVISION re-pin, atlas re-stamp, changelog or release notes), propose it to the owner, and carry it out; creating the tag and the GitHub release is outward-facing and needs the owner's go at that point.

## Notes

State at 2026-10-02 02:05 UTC (19:05 PT, 1 October).

Done: the deployment of 07f014386 was verified first (check_published_site 848 of 848). jlevy/squares#291 cut v0.5.0 with `devtools.cut_release` and merged as 8aaa411dc02994635c74457bf928d5309adbb69f. That commit deployed at 2026-10-02T01:07:03Z, so the edition's date, October 2, 2026, stands. Live: the homepage, Results, Frontier, Papers and both papers print v0.5.0-971e5f, and the first paper's PDF is served. Main's Packing validation and Certificate page runs at 8aaa411dc are green.

Open: jlevy/squares#297 (branch claude/v0.5.0-deployment, worktree .claude/worktrees/v050-deployment, sparse) adds the deployment line above PUBLICATION_HISTORY. Merge it when its run is green.

Left (item 1 is done: check_published_site passed 848 of 848 on 8aaa411dc at 02:40 UTC, and #297 merged as 0848631a8):
1. The full published-site check on 8aaa411dc was not run, because the worktrees with the environment were on the detached external drive: from packing/, `uv run --frozen --all-extras --group dev python -m devtools.check_published_site --commit 8aaa411dc02994635c74457bf928d5309adbb69f` (the full id; a short one fails three checks).
2. Owner decision, not done: the tag and GitHub release. `git tag v0.5.0 8aaa411dc && git push origin v0.5.0`, then `gh release create v0.5.0 --title v0.5.0 --notes-file <notes> packing/atlas/known-best/known-best-1-*.pdf packing/atlas/known-best/known-best-1-*.png`. The films stay on the v0.4.2 release.
3. The scope sentence is the agent's wording and the owner's to reword; keep it to three lines in the first paper's version history, or the PDF goes to 23 pages and the page-count guard fails.
