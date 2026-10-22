---
type: is
id: is-01m5jgjmwqthz66kpksgjh3aav
title: Diagnose presentation pre-push behavioral suite timeout
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: presentation-validation
labels: []
dependencies: []
parent_id: is-01m5jct23n8s7fj3ydf94n0yhv
hold: null
hold_until: null
created_at: 2026-10-22T19:14:32.468Z
updated_at: 2026-10-22T21:04:21.745Z
started_at: 2026-10-22T20:19:38.497Z
---
Presentation branch codex/profile-naming-and-tally-order: all 67 non-behavioral push checks passed, but reachable behavioral tests exceeded 1800 seconds (1917s total). Final edit tier 68/68 passed, GitHub icon focused tests 37/37 passed, full rebuilt-site audit 7341/7341 passed, senior review clean. Diagnose selection/runtime and finish required pre-push validation before commit/push/PR; do not treat timeout as a test assertion failure. Log: /Volumes/spud-ext2/agent-scratch/about-profiles-20261020/tmp/presentation-push-complete.log. Existing presentation parent think-zpzg.

## Notes

Diagnosis and retained evidence:
- Initial presentation push selected331/834 files. An unavailable .gate-running reservation forced the conservative fallback: one normal pytest worker despite10 available CPUs. The reachable step hit its1800s deadline (1801.02s;1917.20s overall), with25 F symbols before termination. No per-node progress/JUnit artifacts had been enabled, so those historical F symbols cannot be attributed reliably; the old lastfailed cache was not evidence for that run. Preserve tmp/presentation-push-complete.log.
- Supported rerun used --push --jobs3 --inner-jobs1, NODE_OPTIONS=--max-old-space-size=8192, short tracebacks and PACKING_VALIDATION_ARTIFACT_DIR. It selected332 files and confirmed8 normal xdist workers; all67 prerequisite checks passed. I omitted --timeout-seconds1800 on that invocation, so the proper-subset step inherited the900s default and timed out at901.03s (1110.89s overall). It retained8,013 completed test records and13 distinct failed nodes. This was not a passing full push gate. Artifacts: /Volumes/spud-ext2/agent-scratch/about-profiles-20261020/presentation-main-e44a51f4-push-artifacts, run383d76f1058a41ba9638544bf59f23a9, command13585eade340492abf85b143771f3ca7. Child source receipt0296712242241a67990a6c1c010c7fef141faad9. Main log tmp/presentation-main-e44a51f4-push.log.

Dispositions of all13 captured failures:
- One workbench navigation assertion: the icon SVG spans lines, which the old regex skipped. Initial DOTALL repair passed1test in6.94s; domain_finterm owns its final semantic refactor.
- Eight overview assertions: replaced exact SVG/panel serialization with parsed roles, destinations, decorative attributes and accessible GitHub labeling; accepted attribute-order variation; required full names in narrative context; retained shared sizing tokens without pinning a former CSS selector; verified header/footer result destinations instead of obsolete one-link counts. Claim, scope, record context and destination coverage remain. All8 repaired nodes passed in306.99s; log tmp/presentation-overview-all-fixes.log. Earlier3-node subset passed110.14s. Ruff clean. No production edits by this lane.
- One case-popover exact serialization assertion: root owns semantic repair and reported1passed169s.
- Two real Pages workflow input omissions: root added site_github_links.py, site_popovers.py and templates/github-links.css; root reported all3 workflow/input focused checks passed13.9s.
- One suite-file cost roster failure: measured and admitted only the2new whole test modules with the existing admit-local tool. Successful unfiltered/unsharded run:16passed40.31s; github-links7tests14.146 reported seconds, popover-controls9tests18.784 seconds. Raw report retained in packing/devtools/suite-file-cost-admissions/presentation-2026-10-22/popover-github-links.json; local historical record/provenance and10% threshold unchanged. All shard unrecorded shares now9.5/9.3/9.7/9.4%. Exact prior failure test_suite_files.py::test_check_passes_on_the_real_tree passes1test in1.52s. Root pushed admissions as5f3f626f3 and semantic/workflow fixes as e3c1bcb3f.

Current229-result browser artifact, for reuse without rendering: /Volumes/spud-ext2/agent-scratch/about-profiles-20261020/tmp/pytest-of-levy/pytest-29/popen-gw0/site0/results.html (1,327,838bytes,229rows,13CSS assets alongside). Performance reviewer routing goes through coordinator because its agent path is not visible from this lane.

Handoff: at the coordinator's explicit direction, do not restart the whole local gate while matching-source hosted distributed CI is running each push. No timeout/coverage/threshold was relaxed and no validation CLI patch was made. A future local retry can use the already-supported --timeout-seconds1800 option explicitly. Coordinator owns final upstream integration, CI acceptance, review and merge; this bead stays open pending that acceptance. No commit/push by this delegated lane. Coordinator owns handoff sync.

PR733 CI follow-up at 064b2bc5ab6e8c124aff329210eec5ee5417901a:
- Diagnosed all8 assertion failures in hosted run39852077730 from individual job logs while the run was ongoing. suite-a4: Markdown paper credits retained shortened labels after HTML expanded names; suite-b1: two exact scientific-term registry anchors retained Overbeck/Trump after narrative names expanded; suite-d2: a class-prefix popover count included the new controls wrapper and a single-line list-item regex omitted multiline SVG; frontend1: intrinsic Atlas table width1170 exceeded a former1150±10 snapshot although desktop fit, local narrow scrolling and zero page overflow remained correct.
- Coordinator repaired paper_front.py/profile_links.py and structure fixtures, preserving short technical-label defaults via keyword-only full_names=False. Full test_paper_structure.py + test_profile_links.py:46passed9.34s; coordinator log tmp/presentation-paper-structure-parity-fixed.log.
- This lane updated only the2 term anchor names, replaced popover serialization counting with the native-popover id/role/accessible-label roster, parsed credit list items and asserted source/registration URLs stay with their result, and replaced the fixed intrinsic-width snapshot with stable narrow width bounded by the desktop track. No scientific definition, forward allowance, assertion coverage, timeout, gate or size threshold was relaxed.
- Four previously failing focused nodes passed45.47s, including real Chromium at1280/1024/768/390. Log tmp/pr733-ci-semantic-focused.log. Ruff, formatting and git diff --check passed. Precommit review found no further actionable issues; native attribute and destination semantics preserve the contracts under SVG/layout serialization changes. Normal lefthook completed2.45s, including paper-title agreement.
- Combined7file repair committed and pushed directly with coordinator authorization as064b2bc5ab6e8c124aff329210eec5ee5417901a; remote ref read back identical and source tree clean. The prior historical no-commit statement describes only the earlier handoff. Hosted CI and final review/merge acceptance remain coordinator-owned; this bead stays open pending that acceptance.
