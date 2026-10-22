---
type: is
id: is-01m5j79r46k1ez04dzq3arz7zv
title: Fix stale Pages subpath fixtures in publication checker tests
kind: bug
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-test-fix
labels: []
dependencies: []
parent_id: is-01m5j10qmw6d55ghhfxg9ekww1
hold: null
hold_until: null
created_at: 2026-10-22T16:32:23.685Z
updated_at: 2026-10-22T17:39:27.591Z
started_at: 2026-10-22T16:32:32.330Z
closed_at: 2026-10-22T17:39:27.591Z
close_reason: "Implemented and pushed in PR727 at73a28c47fb0499999fb1a9b9e8baad78a6589215. Senior review A and follow-up B complete; A1 fixed and disposition posted https://github.com/jlevy/squares/pull/727#issuecomment-6347206000. Final hosted CI green: packing39815232494, Pages39815232525 attempt2. Local corrected file133passed and pool23passed. Live cutover separately tracked think-juq7."
resolution: null
duplicate_of: null
---
CI shard C on PR #727 reports seven stale-domain failures in packing/tests/test_check_published_site.py. Evidence: https://github.com/jlevy/squares/actions/runs/39812882258/job/119943570388.

Reproduced all seven locally: the checked-pages contract still expects /squares/ and the shared head fixture writes /squares/ icon/Apple-touch URLs, producing extra head-check failures in six other tests. Update only this test file to the squaremath.org root; preserve exact failure assertions and existing negative coverage. Leave the separate plan review fix untouched. Coordinator owns commits and pushes.

## Notes

Confirmed the CI root cause with the exact seven failing tests: 7 failed, 126 deselected in 4.38s before editing. Updated only packing/tests/test_check_published_site.py: shared fixture icon/Apple-touch root now /, and three checked-page URL expectations assert exact squaremath.org root addresses. Preserved all negative failure assertions. Full focused file: 133 passed in 55.76s. Ruff check/format and git diff --check pass; BasedPyright 0 errors/warnings/notes. Existing plan review diff untouched. No commit/push. Awaiting coordinator commit and hosted CI; coordinator reports the separate pool-complement phase was skipped on the earlier suite failure and still needs its follow-up check.
