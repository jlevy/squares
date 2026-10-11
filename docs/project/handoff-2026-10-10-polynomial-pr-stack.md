# Polynomial PR stack: publication checkpoint and remaining work

This is a checkpoint for the next agent, not a merge approval.
The owner requested publication of the committed work and an explicit handoff while
validation continues.
The polynomial article is strictly web-only: preserve its HTML/Markdown, equations,
coefficients and no-JavaScript access; do not generate, sample or publish a PDF.

## Branches and entry point

The existing formal GitHub stack is 447: main →
[PR403](https://github.com/jlevy/squares/pull/403) →
[PR435](https://github.com/jlevy/squares/pull/435). Both PRs remain open.
Use `tbd shortcut merge-upstream` and the official gh-stack workflow; synchronize the
chain by rebasing, without a merge commit in a stack layer.
Landing the PRs still requires the owner’s session confirmation.

Upstream was fetched again on 2026-10-11 UTC and remained
`6038af33cc6c4b5b7121eeca4d7c1ad528cfecc0`. The parent is `claude/friendly-sagan-jk7qzy`
at `240299aad79562574cfb31d37298003374423fc6`; the reviewed child code is
`codex/exact-polynomial-coverage` at `2bbf52400e6cb1ff04a28763900ff588f83f89f7`. This
checkpoint adds the handoff/map and two independent title-check expectations above that
production code. Resolve the final published heads from GitHub before work.

Working checkouts are on the external volume:

- Parent: `/Volumes/spud-ext1/agent-source/polynomial-parent-01a118e4`.
- Child: `/Volumes/spud-ext1/agent-source/polynomial-catalogue-01a118e4`.

Preserve the unrelated primary checkout at `/Users/levy/wrk/github/squares`, branch
`codex/n17-state-review`, and its untracked research/coordination files.

## Completed work

Native stack rebases resolved the reachable-test, browser font/layout, Papers roster,
shared navigation, generated URL and forwarder conflicts.
All upstream production behavior and scientific/source/frontier/witness records were
retained. The storage-migration commit was reworded to describe its gzip/replay changes.
The navigation repair was amended into `dacfdb43d`; its five-file change is +41/−3,
followed by the separate one-line acquisition pin.
No regression/fix commit pair was added.
Production code and scientific files equal the reviewed and tested repair.
The checkpoint additionally registers this handoff in the document map/SYNOPSIS and
updates two stale four-paper title expectations for the fifth exact-side report.

The parent represents 324 cases with 320 exact identities and degree-only n=83. The
child supplies n=83’s complete degree-672 polynomial, giving 321 exact identities.
Both retain 77 proved cases.
Numeric n=29/55/71 remain research gaps.
The canonical corpus keeps 538 records, including 214 historical records, 560
coefficient vectors and 6,378 integer strings.
Public reports keep 324 current and 28 useful source records, omitting 186 superseded
rows and 22 redundant notes while preserving the canonical record and every retained
coefficient. Source occurrences, exact identities, equivalent geometry, adopted records
and optimality remain distinct.
No solver, geometry/Lean or frontier-adoption work ran in this synchronization slice.

The browser retains shared theme/navigation/headroom and its native MathML client.
The full article retains the KPress article client and rating tooltips.
Loading those article-only programs on the browser initially failed the unchanged 10%
startup criterion: 404,158/3,212,387 = 12.5812%. The corrected browser removes 100,600
unneeded automatic bytes and passes at 303,558/3,212,387 = 9.4496%. The rejected
measurement remains archived.
Neither the criterion nor physical caps were raised.

## Validation and Git size

At reviewed child code 2bbf:

- 127 focused renderer, header, script, measurement and Pages tests passed in 137.04s.
- Fresh clean web consumer checks passed 5,661/5,661; script inventory approved 12
  declarations; responsive checks passed eight views.
- Startup acceptance passed with a clean provenance receipt; all 352 projected records
  and 2,128 coefficient strings compared exactly.
- Complete HTML is 1,959,996 bytes, below the unchanged 2,000,000-byte cap; executable
  inline limits remain 4,096 bytes.
  No polynomial PDF was generated.
- Earlier URL checks passed 1,634/1,634; five paper titles/ten references agreed.
- Independent semantic and precommit reviews found no remaining code finding after the
  route-specific startup repair.

The audited code stack has 18 parent and 32 child commits.
Its streamed union pack is 3,683,176 bytes thin / 5,605,962 bytes non-thin; its largest
new historical blob is 2,629,925 bytes.
All 67 historical scientific blobs survived unchanged, with zero new PDF blobs.
The additional checkpoint changes only documentation and two title assertions.
Final published sizes belong in the PR descriptions and tracking checkpoint.
The diffs are substantial but organized as two review units: source/storage/backfills in
PR403, and catalogue/web publication in PR435. Thirteen acquired PDFs totaling
198,944,687 bytes were inherited from main and moved to the source release; they are not
new branch payloads.

PR435 Packing [38105909051](https://github.com/jlevy/squares/actions/runs/38105909051)
found two stale title assertions (4,145 other tests passed) and an unmapped handoff
document. The title expectations and documentation-map/SYNOPSIS entry are corrected in
this checkpoint.
Both exact failed title tests passed locally (2/2 in 48.88s); softschema
repair/validation and the 2,007-document coverage/link/footer check passed.
Fresh hosted qualification still remains.

**Fresh broad validation is unfinished.** Parent `packing-validate --push` passed 66
prerequisites but its reachable suite hit the actual 900-second command timeout at 55%;
this is a failed run, not a pass or a waived gate.
The parent is being retried through `--push --only 'lint floor' --timeout-seconds 1800`,
selecting Ruff plus the same full reachable selection under the repository’s existing
broad-suite budget. Progress receipts and the original failed log are retained.
The first attempt to select the dynamically added reachable step by name was a usage
error and ran no checks.
Child broad local pre-push remains to be run.

Earlier full hosted checks qualified only parent e5892db7 and child 7fd2074c:
[38088753256](https://github.com/jlevy/squares/actions/runs/38088753256) and
[38093278580](https://github.com/jlevy/squares/actions/runs/38093278580). They do not
qualify the new rebased heads.
The updated PR bodies record new checks and deferred-checkpoint run URLs when
dispatched. Inspect every check, including non-required checks, at each exact published
head before declaring it ready.
All 14 historical review-disposition links remain in both PR descriptions.

## Resume sequence

1. Run `tbd prime`, `tbd policy show` and inspect `think-e7sr`. Pull/re-read, claim and
   synchronize before changing its notes.
   Preserve other owners and delegates.
2. Verify the external volume is mounted and writable.
   Source
   `/Volumes/spud-ext1/agent-scratch/polynomial-catalogue-01a118e4/upstream-refresh-20261011-0142/env.sh`
   and add its venv and the selected worktree’s `node_modules/.bin` to PATH. Use Python
   3.14.7; keep TMPDIR, UV_CACHE_DIR and each worktree’s CARGO_TARGET_DIR external.
   The parent also needs parent-specific PACKING_PROJECT_ROOT/PYTHONPATH and
   CARGO_TARGET_DIR_PARENT overrides, shown in its command receipts.
3. Inspect the live parent retry and saved worker JSONL before starting another full
   validator. Allow it to finish; record its real verdict.
   Do not edit a worktree while its gate is running.
   If it fails, fix the concrete finding and rerun.
4. Run the child `packing-validate --push` from its packing directory, with external
   artifact output and an explicit 1,800-second broad-suite command cap.
   Keep the prior failed/not-run scopes distinct.
   No new environments or internal fallback.
5. Watch ALL checks and full `deep-gate.yml` checkpoints at the published PR heads.
   Fix failures, repeat native stack sync/submit if needed, and update both PRs and this
   tracking record with the new heads and terminal evidence.
   Re-fetch before final integration; reconcile any newly changed records rather than
   assuming the current corpus is still newest.
6. Obtain the requested next-agent review before landing.
   Close `think-e7sr` only after its synchronization/validation scope is complete.
   The science and broader engineering follow-ups below are not closed by this
   checkpoint.

## Remaining owners

| Work | Tracking |
| --- | --- |
| Numeric n=29/55/71 | think-je8y / think-phh8 / think-1blg OPEN |
| Daniel T-131 n=132 adoption/atlas; import/reply | think-kkj2 OPEN; think-iyij IN_PROGRESS |
| Couzo T-128/T-130 replay/adoption/atlas; custody | think-lhtz OPEN; think-0mlq IN_PROGRESS |
| Reported n=106/152/177 geometry/Lean | #419 / think-8sm2 IN_PROGRESS |
| n=83 ordinal count; Rehwaldt n=68 multivariate binding | think-chsu OPEN; think-nv5o IN_PROGRESS |
| Ideal n=68/105/292 prerequisites | think-056g / think-gl59 / think-w622 OPEN |
| Snapshot headroom and startup attribution | think-t1lk; think-jygq / think-5jr5 / think-rxyl IN_PROGRESS |
| W7 exporter/independent n=11 control, then bounded n=102 | think-s6np / think-ohhz OPEN |
| Broader W6 high-precision lane | think-eu89 IN_PROGRESS |
| pool_heavy annotation debt; full-CI wall reporting | think-w19q OPEN; think-0atx IN_PROGRESS |
| Controlled shared-CI timing baseline | think-9dhb OPEN under active think-ht59 |

The selected research entry remains W7 exporter/independent n=11 control, followed by
the current n=102 protocol with a confirmed seed.
Source acquisition think-88r0 is closed for acquisition only.
Later Couzo n=375/378 reports are outside 1..324. The six engineering beads
think-jygq/wuol/ja78/z3qh/okxn/wiu3 retain their prior IN_PROGRESS state and ownership;
do not infer full closure from a passing sub-check.

## Evidence, cost and cleanup

Durable evidence root:
`/Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/upstream-refresh-20261011-0142`.
It holds the baseline, preserved failure logs, command/worker receipts, source and
storage reviews, clean web metrics/layout, PR drafts and tracking snapshots.
Bulk logs and generated publications are excluded from Git.

This slice’s observed clock began at 2026-10-11T01:42:49Z; earlier preparation is
unmeasured.
The final observation belongs in the PR/bead checkpoint, not a claimed solver
or CPU cost.
The previous slice closed at 411.2 minutes at 2026-10-11T00:06:42Z, distinct
from its 391.2-minute interim observation and the separate earlier 141.3-minute slice.

Three verified inactive older pytest roots were permanently removed after process,
open-handle, containment and worktree checks.
Global free space rose from 555,328 to 15,793,332 KiB during cleanup; concurrent writers
prevent assigning the entire change to this task.
Source, evidence, live preview, environments, current active test fixtures and unrelated
chats were preserved.
Recheck activity before any more cleanup.
The live preview remains at http://127.0.0.1:60649 and has not been updated to this new
code head; use the freshly checked scratch publication or rebuild the owned preview
before showing it as current.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
