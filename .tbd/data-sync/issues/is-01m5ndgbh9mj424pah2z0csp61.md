---
type: is
id: is-01m5ndgbh9mj424pah2z0csp61
title: "PR #757: the gist source card (OTHER_PROJECTS accepts gist.github.com)"
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-fix-757-1023
labels: []
dependencies: []
parent_id: is-01m5mr7439b7eqzqzccqrxnkxa
hold: null
hold_until: null
created_at: 2026-10-23T22:18:34.921Z
updated_at: 2026-10-24T01:47:15.127Z
started_at: 2026-10-23T22:18:44.697Z
---

## Notes

2026-10-23 c-fix-757-1023 (moderate lane, sole committer on claude/intake-2026-10-23-755, worktree /home/user/wt-lean).

## The gist card, option (a)
- c4301bb8a: OTHER_PROJECTS (packing/devtools/site_resources.py) lists https://gist.github.com/amundsk/78f9f0e7b4669f2f509a281845081768, no revision, by Amund Kristiansen, note naming T-238. overview_sections.source_repository drops a gist's 40-hex revision (fullmatch on https://gist.github.com/<owner>/<id>/<sha>[/]); everything else is unchanged.
- Negative control first: test_a_project_card_on_an_unsupported_host_is_refused (example.com twice, github.com.example.com, gist.github.com.example.com, plain http) passed under the old host set; with the gist positive added it and test_a_gist_revision_names_the_gist_and_nothing_else_is_cut failed; after the change both pass. PROJECT_HOSTS in test_overview.py is now github.com and gist.github.com.
- test_other_projects_include_every_source_repository_the_record_reviews now reads reviewed sources through source_repository. test_site_project_tallies' oracle (_project_address) derives a gist's home itself, apart from source_repository, as its fixture docstring requires; without it three tally tests failed (the page counted T-238, the oracle did not).
- No layout, template, CSS or browser script changed. The card renders "Repository 78f9f0e7b4669f2f509a281845081768", by Amund Kristiansen, tally "1 record (at S2) - 1 result (at S2)". The hex heading is deferred to think-mwi8.

## Merge and re-pin
- 6510bca31 merges origin/main 64b316b6c (#761, #762; the brief named 77aba4c02, main had moved by #762, a 4-line test change). Conflict only in release.py: DATA_REVISION, and RELEASE_IMPACTS (explainer v0.4.22 kept ahead of main's infographics v0.7.0).
- 8a2be6a45: flip_regularization --update; 303 keeps pose 270/no flip/quadrants, only its four weights move in the fifth place.
- ea8c6f106: release_pin --update (8a2be6a4).
- 825c95959: the three papers' no-change record also names overview_sections.py and site_resources.py; re-measured at link revision ea8c6f10 against main 64b316b6c, twice from the tree and twice with main's ten candidate inputs swapped in and the profile aside: 51 files each, byte-identical. check_release_impact: every publication candidate has a reviewed disposition.

## Checks at 825c95959
- adopt_houses --check (70), upper_bound_houses check (70), select_houses --check (303 does not move), default_drawings --check-state --base-ref origin/main (0 pending), regularized_drawings --check, flip_regularization --check: pass.
- packing-validate --records: only id contiguity fails (119 s).
- 18 affected modules: 1,129 passed, 1 skipped, 12 errors, all test_site_drawing_hover.py setups where local Chromium crashed ("Page crashed") at load 17-23; same 12 crash alone; hosted suite-b passes the module at this head.
- Hosted run 40037263522: suite-b and suite-c pass; validate, suite-a and suite-d fail on id contiguity only.
- Hosted, complete at 825c95959: Packing validation 40037263522 (packing-required fails on validate, suite-a, suite-d only, all id contiguity; frontend, typecheck, geometry, sweeps, measure-verifier, suite-b, suite-c pass), Certificate page 40037263599 success, Branch mergeability 40037258662 success.
- PR #757 body updated (gist-card and flip rows, Changes by Purpose, Validation, merges, Limits, think-mwi8). Still a draft; labels intake, S2. Not merged; think-ykgh untouched; think-8r5w not registered.

2026-10-24 c-land-757-1024: the entry these notes call T-238 is T-239 since commit 045497b6a on PR #757 (renumbered when the owner gave T-237 and T-238 to #750, think-4o9c). The gist card counts T-239.
