---
type: is
id: is-01m4pd6dbc6j1wyjg6n62dv8ag
title: "Intake announcement: generate a one-line-per-result summary with X handles where self-declared, names otherwise"
kind: feature
status: closed
priority: 2
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T21:16:41.708Z
updated_at: 2026-10-23T06:12:23.242Z
started_at: 2026-10-11T21:16:45.790Z
closed_at: 2026-10-23T06:12:23.242Z
close_reason: "Tracker audit 2026-10-23 (c-audit-a-1023, think-s4ld), checked by coord-intake-1023: DONE; STALE-CLAIM. packing/devtools/render_announcement.py; result-import.md line 74"
resolution: null
duplicate_of: null
---
Owner request 2026-10-11: as part of the intake process, a very brief, clean, tweet-style summary of the new results, one per line, using Twitter/X handles when we have them, otherwise people's names, for the owner to announce from; included in the intake PRs and on the top PR of the stack. Handles only from evidence: a GitHub profile's self-declared twitter_username (today: ry-xu -> small_LM, jlevy -> ojoshe), a handle the record already cites (n-011.md: Ahmed -> ManassehA06), and the contributor profiles of draft PR #490 (packing/contributors/*.md links kind twitter) once they land. Build it as a devtool (OR-1) and add the step to result-import.md, Running an Intake Pass.

## Notes

2026-10-11 (lane T): built devtools.render_announcement with tests (packing/tests/test_render_announcement.py, 26 pass) and added step 6 "Render the announcement" to result-import.md, Running an Intake Pass, and step 7 to its prompt. Commit aaf3e1796 on worktree branch worktree-agent-a86d4098c7e60167c (not pushed).

Usage, from packing/: uv run --frozen --all-extras --group dev python -m devtools.render_announcement (--ids T-NNN ... | --since YYYY-MM-DD) [--github] [--min-significance 3] [--all] [--date YYYY-MM-DD]. --since reads `registered`.

Wording rules: "New best known" only at V3+ where nothing on record (case record both lanes, every other entry) is better or equal-and-earlier; a regularization of the entry's own packing does not count against it. Below V3: "Reported ... not yet verified (Vn/Cn)". Upper bounds rounded up, lower down; margins cut to 2 significant figures; previous holders not named. Credit: the register's whole credit line in order, plus the finders of regularized packings.

Handles found 2026-10-11: @ojoshe for Levy (GitHub jlevy twitter_username, tied as the requests record's owner = PROJECT_AUTHOR); @small_LM for ry-xu (GitHub ry-xu, login equals the credited name) — appears only where the register credits "ry-xu" (T-125, T-126), not "Xu"; @ManassehA06 for Ahmed (record: n-011.md). No other issue author declares twitter_username.

Open: (1) "Xu" in credit lines is not tied to ry-xu by any record evidence; adding `Ryan Xu: Xu` to bibliography credited_names (records lane) or a #490 profile with alias Xu would tie it. (2) T-128..T-146 were registered 2026-10-08..10, none on 10-11. (3) Contributor profiles (#490) are read when packing/contributors exists; format checked against PR head 068de55.

2026-10-11, revision at the coordinator's request: commit 07cc09f2e makes lines brief (at most 140 characters before the link): finders only, by full name or evidenced X handle; the owner (Levy/@ojoshe) is never credited or tagged; "(verified)"/"(reported)" tags; --lineage and --margins opt in. Sample over T-128..T-146: 12 lines, longest 92 characters before its link. 29 tests pass; records tier passes.

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): the alias decision (tie "Xu" in credit lines to ry-xu / X handle small_LM via bibliography credited_names or a #490 profile) is on https://github.com/jlevy/squares/issues/543. Tracker https://github.com/jlevy/squares/issues/544.
