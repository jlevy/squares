---
type: is
id: is-01m5j79r46k1ez04dzq3arz7zv
title: Fix stale Pages subpath fixtures in publication checker tests
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-test-fix
labels: []
dependencies: []
parent_id: is-01m5j10qmw6d55ghhfxg9ekww1
hold: null
hold_until: null
created_at: 2026-10-22T16:32:23.685Z
updated_at: 2026-10-22T16:32:32.331Z
started_at: 2026-10-22T16:32:32.330Z
---
CI shard C on PR #727 reports seven stale-domain failures in packing/tests/test_check_published_site.py. Evidence: https://github.com/jlevy/squares/actions/runs/39812882258/job/119943570388.

Reproduced all seven locally: the checked-pages contract still expects /squares/ and the shared head fixture writes /squares/ icon/Apple-touch URLs, producing extra head-check failures in six other tests. Update only this test file to the squaremath.org root; preserve exact failure assertions and existing negative coverage. Leave the separate plan review fix untouched. Coordinator owns commits and pushes.
