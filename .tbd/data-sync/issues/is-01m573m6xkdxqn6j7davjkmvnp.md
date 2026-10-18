---
type: is
id: is-01m573m6xkdxqn6j7davjkmvnp
title: "PR671 review A1/A5: retain certificates without overwrite and replace manifests atomically"
kind: bug
status: closed
priority: 1
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m572ssbx1x412zpvsw1sb6je
hold: null
hold_until: null
created_at: 2026-10-18T08:56:33.457Z
updated_at: 2026-10-18T13:31:13.093Z
started_at: 2026-10-18T09:42:48.172Z
closed_at: 2026-10-18T13:31:13.093Z
close_reason: PR671 fixes published at89166716d with terminal green Packing/Pages CI and marked A/B/C dispositions; census/C1 remains open in protected think-f40c
resolution: null
duplicate_of: null
---
Review https://github.com/jlevy/squares/pull/671#pullrequestreview-5562187918 at32d47d3214ec28f2a82b89689cd8bb8f63f98e02 reproduced silent overwrite/deletion of an existing plain candidate with exit0. Fix collision refusal before any write; manifest replacement must be atomic. Add fail-closed regression controls. No new expensive census is required. Preserve digest-only adapted source archive custody.

## Notes

2026-10-18 continuation: A1/A5 fixed and pushed on PR #671 at 1b2cf7cfe15c4eec90d447bf3977a683d96dec1d. Source commits be93e8ea3a2e41916ce226f741dfae9d2d9ff7a0 and 13fcf887f48dce4c128499504b22ac63c002cde5, both with normal hooks and coordinator source review. Full destination preflight refuses existing plain counterparts (matching or conflicting), nonregular/symlink manifests and symlink targets; private gzip staging keeps gzip -9n bytes; os.link publishes members without clobber; strif atomic manifest replacement preserves prior complete records. Initial controls reproduced 5 failures; final focused retention tests 33 passed in 6.67 s, broader acquisition/retention group 232 passed in 32.98 s. Scoped Ruff/format and configured BasedPyright pass. Unique receipts retained outside scratch at /Volumes/spud-ext1/agent-source/squares-671-retention-evidence-20261018/. Hosted CI pending; unrelated publication/page-size findings remain open. No source verifier archive fetched or opened.

Final PR671 disposition, 2026-10-18: published clean head 89166716d492ae7e4e76f61550e80849dec7edc3 on existing owner branch; PR remains draft, no merge/deployment/author message. Required local --push passed all69 selected steps in1266.55s real (1264.98/1800s tier), quick19,016passed55skipped1xfailed plus10pooltests. Normal hooks and unchanged ceilings.
Final exact-head hosted CI: Packing https://github.com/jlevy/squares/actions/runs/39130821839 SUCCESS; Pages https://github.com/jlevy/squares/actions/runs/39130821886 SUCCESS; mergeability https://github.com/jlevy/squares/actions/runs/39130818998 SUCCESS.31successful/28conditional-skipped checks; optional deferred run39130821909 correctly skipped without deep-gate label. No pending/failing check. Post-CI discovery found only original formal A/B/C, no inline or other review comments/issues.
Marked dispositions: A https://github.com/jlevy/squares/pull/671#issuecomment-6250490436 ; B https://github.com/jlevy/squares/pull/671#issuecomment-6250491767 ; C https://github.com/jlevy/squares/pull/671#issuecomment-6250493618 . A1-A6 fixed; B bounded integration complete; C1 deferred in open think-f40c for stage7 upstream author README correction/question. Source archive README/digest unchanged; no author message claimed. Only n108 V3/C3; other17 V0/C0; no fresh native coverage replay.
Final publication follow-up: ccb2 hosted Packing passed but Pages exposed23 PDFpages vs inherited22 expectation.34fd8b33f00623b0e8ad24c760f17a8072dc057b fixes expectation/comment;101 PDF/exporter controls pass20.68s and artifact reproduction passes869,900bytes/23pages/19embeddedfonts.89166716d492ae7e4e76f61550e80849dec7edc3 scopes three unchanged-paper decisions to exact helper path after six byte-identical HTML/MD comparisons; release-impact18tests pass6.70s/errors[]. Final hosted PDF/math/font/artifact/saved-print-geometry checks all pass.
Merge-order caveats remain: #661 retainsT195, this draft renumbers; sitev0.7.26 provisional against #676, explainerv0.4.8 and data pin reconcile after incoming changes. Separate open efficiency follow-up think-y3pe tracks fresh per-run external TMPDIR/nested pytest isolation. Durable receipts: /Volumes/spud-ext1/agent-source/squares-671-retention-evidence-20261018 .
A1/A5 fixed by be93e8ea and13fcf887: no-clobber candidates, invalid-manifest preflight, atomic manifest,33focused regression controls. Adapted archive remains digest-only/unopened/unretained.
