---
type: is
id: is-01m3xf4hnsxw1tpssvxspgd8sa
title: "Release procedure: a site version bump needs no tag or GitHub release; a release is cut only to host new generated assets"
kind: task
status: closed
priority: 3
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T04:49:36.950Z
updated_at: 2026-10-02T05:41:52.625Z
closed_at: 2026-10-02T05:41:52.624Z
close_reason: "Merged in jlevy/squares#301: cut_release no longer prints a tag or gh release create and no longer moves a paper; development.md, Cutting an edition, says a release is cut only to host generated assets that need a download address (the films, FILM_RELEASE), and gives the procedure for bumping a paper's own version. tests/test_cut_release.py holds the printed text."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'The GitHub releases are not so important for the website. They are only important for the assets that are generated, like the PDFs or the videos.' Today development.md (Cutting an edition) and the text devtools.cut_release prints both end with 'tag the merge and create the GitHub release with the poster PDFs and PNGs attached' as steps left for the owner at every version bump. Bring both in line: the site's version is complete when the merge deploys and check_published_site passes; a release is made when there are assets that need a download address (the films, linked through render_overview.FILM_RELEASE, currently v0.4.2; the posters are served from the site itself). Update the printed steps, the paragraph in development.md and any test that pins the printed text (tests/test_cut_release.py).

## Notes

State, 2026-10-02 (PR #301, branch claude/paper-versions, draft): done in code and prose; not closed.

- `devtools.cut_release`: what it prints for the owner ends at the deployment check (`check_published_site`); no `git tag` and no `gh release create` as routine steps. It says a release is cut only to host generated assets that need a download address, the films (`render_overview.FILM_RELEASE`, currently v0.4.2), and that the posters are served from the site. It also says no paper's version moved: a site bump adds no entry to any paper.
- `tests/test_cut_release.py` pins the printed text (no "git tag", no "gh release create"; the release rule; "Neither paper's version changed") and that a bump leaves `EXPLAINER_HISTORY`, `EXPLAINER_VERSION` and `OPTIMALITY_REVIEW_EDITION` as they are.
- `development.md`: "A release is cut only to host generated assets" replaces "A release tag carries the version alone"; Cutting an edition no longer lists the tag and release; a new "Bumping a paper's version" section states the paper-side procedure (where the version is declared, what `artifact_dates` and the tests then require, the PDF page count).

Left: the owner's review of the wording; the PR's merge.
