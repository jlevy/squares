---
type: is
id: is-01m4zs2fv9hfmsbpjdkxb47p94
title: "E1: bind deferred proof identity to GitHub-authored producer source tree"
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zq0njqcj232mhnhc0nwfa3
hold: null
hold_until: null
created_at: 2026-10-15T12:37:25.992Z
updated_at: 2026-10-15T12:50:15.492Z
started_at: 2026-10-15T12:42:39.164Z
closed_at: 2026-10-15T12:50:15.492Z
close_reason: Retired before activation after independent source-provenance review. GitHub metadata identifies PR HEAD but cannot authenticate which merged workflow/source executed after associations disappear. Exact six-file candidate is preserved and reverse-apply verified in deferred-worker-reuse/retired-final.patch at basefc2; 88 passing focused tests do not close E1. D1/D2/E2 fixes remain prototype evidence only, with no production speed claim. All six source paths restored; no new proof framework. Separate live fast-proof issue is actively fixed under think-3d1m.
resolution: null
duplicate_of: null
---
Independentsecurityreviewofunpublishedreusecandidate: artifactselfdeclaredtree plus display-namedsuccessstepsdoesnotauthenticateproducercode. Existingconsumerrecipecomparisonislocalonly. RequireGitHubrunhead_commit.id==head_sha andhead_commit.tree_id==requestedtree; missing/malformed/mismatchcold. Usesexistingrunresponse,nofurtherAPI. Conservativehead/mergetreedifferencelosesreuseandrunscold. Addnegativecontrols forgedartifactnamefromdifferentproducer tree and inconsistentcommit identity.
