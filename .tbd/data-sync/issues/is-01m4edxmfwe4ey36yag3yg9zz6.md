---
type: is
id: is-01m4edxmfwe4ey36yag3yg9zz6
title: "PR #456: bound artifact polling and honor GitHub quota retries"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e2d5gyj7m218hm9f5g01xd
hold: null
hold_until: null
created_at: 2026-10-08T18:55:27.219Z
updated_at: 2026-10-08T18:57:07.161Z
started_at: 2026-10-08T18:57:07.159Z
---
PR456 head3d266f8cc81efb54826d80f3d9921d2d26c5d529 Pages run37821312270: screen, typography and PDF failed while joining prepared-page because GitHub returned an installation API quota HTTP403. Producer prepare was still queued; queued jobs had started_at placeholders, causing needless artifact queries. Moderate addressing agent owns wait_for_run_artifact.py and its tests. Require fewer pending requests, bounded explicit-quota retry handling within unchanged600s timeout, exact attempt/artifact binding and ordinary403 refusal. Targeted19 tests and lint/types pass; final independent review, hosted CI and deployed proof remain under rollout think-7wlz.
