---
type: is
id: is-01m4ajfv9newq89sh4qzq4156c
title: "W7: strict SQUISH #401 import and exact dual-checker receipts"
kind: task
status: in_progress
priority: 1
version: 5
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4ajdxfkfqyr1yj5d4wm5npt
hold: null
hold_until: null
created_at: 2026-10-07T06:58:20.597Z
updated_at: 2026-10-07T08:24:47.737Z
started_at: 2026-10-07T06:58:30.243Z
---
## Notes

Local engineering implementation and verification complete; leave in_progress pending
parent publication and CI. Added bounded strict SQUISH source parser/acquisition, exact
half-angle conversion via public existing adapter helpers, dual exact deciding routes,
deterministic compressed derived facts and certificates, bound verification receipts,
source provenance checks, and fast/replay commands.
Full bound recertification: 45.990 wall seconds with 2 workers.
Full deterministic replay: 76.122 wall seconds serial; all eleven
n=108,126,129,130,153,154,155,180,209,238,303 and both overlap/container controls pass
expected outcomes; 177440 pair decisions per checker across positive cases.
Final 40 tests passed in 2.92 seconds; Ruff and BasedPyright zero findings, fast
artifact check passed.
Fixed reviewed duplicate roster handling, tuple/list control replay mismatch, stale
checker-input evidence binding, source provenance drift, and inconsistent
verdict/clearance receipt fields, each with targeted tests.
Runtime cost: final certification plus replay 2.04 wall minutes; exploratory initial
cert49.061s, failed replay79.676s, canonical replay138.650s, final recert45.990s, final
replay76.122s = 6.49 wall minutes total engineering geometry runs (reviewer runs
additional). Source producer executable absent and never claimed reproduced.
Raw upstream bytes not retained; source/fact/certificate hashes protect acquisition and
checker-input trust boundaries, no Git code fingerprints.
Packet packing/resources/web/squish-401-2026-10-07; witnesses
packing/witnesses/squish-401-2026. Registration tests
test_squish_upper_bound_packets.py; confirmation artifact tests
test_squish_upper_bound_receipts.py.
Reproduce from packing with uv run --frozen python -m
devtools.squish_upper_bound_packets certify --workers 2, then check --replay.
Remote tbd sync remains known divergent/push403; preserve local notes and all beads in
outbox. Parent handles separate PRs, issue comments, final bead disposition.

Follow-up after broad registration pre-push: the original gate had 33 failures and 171
errors, largely a stale HEAD-tree cache before the packet commit.
On the committed reported tree, fixed genuine historical-source/current-selection
interactions without bypassing old certificate verification: source_supersession guards
only document/frontier ownership; historical Kingbird/Evan/Couzo source parsing and all
geometric deciding tests still run.
Coverage overlays preserve unowned sources and stable ordering.
Generator genuinely redrafts historical inputs, then adopts owned SQUISH geometry from
exact facts, normal lower lanes/prose, reviewed source/history additions and later
rigidity promotion. S5 whole-record no-op removed, with reported/confirmed refresh,
bound/body/lower drift, absent-declaration refusal, earlier-source ownership and integer
rational regressions.
Added required verified-ceiling/new-report gap prose to eleven cases; parent
subsequently refreshed current-pose rigidity, case files then frozen.
Source-repository/issue-comment cards and per-square color contracts follow current
geometry; frozen pre-import 56-ceiling census remains explicitly audited from old
receipts. Regularized generated witness snapshots pruned (about2.9MB) with192MiB cap
unchanged. Validation: implicated source/parser/generator/color/overview suite556passed
plus one discovered GitHub issue website-card contract mismatch,130.44s; that defect
fixed and covered by final20regression/ceiling/source-card tests passing12.14s, plus
separately10 targeted tests8.00s. All11 selected SQUISH cases now regenerate
with0disagreements. Prior25 residual tests passed6.91s. Ruff/BasedPyright clean for
all17 engineering-owned changed/new files.
Kernel /proc profiler reproduced with required escalation:1passed0.75s. Remaining
worker-index issue is untracked new source/test files until parent stages them; parent
owns integrity-policy and rigidity floor changes.
Logs:/tmp/squish-followup-final-focused.log,/tmp/squish-followup-final-regressions.log,/tmp/squish-followup-last-fixes.log.
No confirmation checkout edits, commits or feature branch pushes by this lane.
Bead stays in_progress pending parent publication and CI; tbd sync again push-denied and
automatically saved outbox.

Adopted-state integration follow-up: made the confirmation display regression fixture
valid from both reported and confirmed case records by replacing the source display
exactly once, removing an existing verified-display declaration, and injecting exactly
one deliberately stale declaration.
Production code unchanged; missing-display refusal assertion retained.
Reported6affectedtests pass4.06s; confirmation8SQUISH/adoptiontests
pass3.65s,91deselected. Copied only this test file into confirmation at parent explicit
instruction. Ruff clean.
Logs /tmp/squish-fixture-reported-final.log and
/tmp/squish-fixture-confirmation-final.log.
Parent owns commit/publication and bead disposition.
