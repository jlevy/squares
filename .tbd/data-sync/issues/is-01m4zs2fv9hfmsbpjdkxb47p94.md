---
type: is
id: is-01m4zs2fv9hfmsbpjdkxb47p94
title: "E1: bind deferred proof identity to GitHub-authored producer source tree"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zq0njqcj232mhnhc0nwfa3
hold: null
hold_until: null
created_at: 2026-10-15T12:37:25.992Z
updated_at: 2026-10-15T12:42:39.165Z
started_at: 2026-10-15T12:42:39.164Z
---
Independentsecurityreviewofunpublishedreusecandidate: artifactselfdeclaredtree plus display-namedsuccessstepsdoesnotauthenticateproducercode. Existingconsumerrecipecomparisonislocalonly. RequireGitHubrunhead_commit.id==head_sha andhead_commit.tree_id==requestedtree; missing/malformed/mismatchcold. Usesexistingrunresponse,nofurtherAPI. Conservativehead/mergetreedifferencelosesreuseandrunscold. Addnegativecontrols forgedartifactnamefromdifferentproducer tree and inconsistentcommit identity.
