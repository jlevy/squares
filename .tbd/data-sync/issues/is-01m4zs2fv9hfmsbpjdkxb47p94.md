---
type: is
id: is-01m4zs2fv9hfmsbpjdkxb47p94
title: "E1: bind deferred proof identity to GitHub-authored producer source tree"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
labels: []
dependencies: []
parent_id: is-01m4zq0njqcj232mhnhc0nwfa3
created_at: 2026-10-15T12:37:25.992Z
updated_at: 2026-10-15T12:37:25.992Z
---
Independentsecurityreviewofunpublishedreusecandidate: artifactselfdeclaredtree plus display-namedsuccessstepsdoesnotauthenticateproducercode. Existingconsumerrecipecomparisonislocalonly. RequireGitHubrunhead_commit.id==head_sha andhead_commit.tree_id==requestedtree; missing/malformed/mismatchcold. Usesexistingrunresponse,nofurtherAPI. Conservativehead/mergetreedifferencelosesreuseandrunscold. Addnegativecontrols forgedartifactnamefromdifferentproducer tree and inconsistentcommit identity.
