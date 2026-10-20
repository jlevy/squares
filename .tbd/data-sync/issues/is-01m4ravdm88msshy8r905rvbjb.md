---
type: is
id: is-01m4ravdm88msshy8r905rvbjb
title: Diagnose local polynomial-stack worker subprocess timeouts
kind: bug
status: open
priority: 2
version: 3
spec_path: docs/project/handoff-2026-10-10-polynomial-pr-stack.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ma117y5ygnz88exhchnjp0
hold: null
hold_until: null
created_at: 2026-10-12T15:14:13.255Z
updated_at: 2026-10-12T16:57:09.138Z
started_at: 2026-10-12T16:55:32.535Z
---
# Diagnose local polynomial-stack worker timeouts

The local parent pre-push at `1c72686eac852e05fef250bb0cd703a83dc05d75`
passed 64 prerequisites, then its reachable-test command hit the unchanged 1,800s
ceiling (1,801.03s wall). A complete call-phase companion reports
`test_a_control_command_is_green_unmutated_in_a_worker[python3 -m devtools.check_readme]`
failing because its unmutated command exceeded the unchanged 120s deadline, with
empty stdout/stderr. Neither normal nor pool completed JUnit. This does not establish
a README mismatch, scientific failure, or common host cause.

A preceding owner-stopped ten-worker retry recorded four distinct subprocess timeouts
at 60/25/45/20s. An older d0c run recorded 143 atlas outcomes without exception text;
the repaired failure-companion writer now preserves full failed-phase diagnostics.
The six-CPU run does not diagnose the ten-worker failures. Python CPU override changes
reported pool sizing, not affinity; markers, assertions and deadlines are unchanged.

Continue with the saved exact-node trace and retained worker inputs. Reproduce the
unmutated baseline under the documented task environment, distinguish source input,
subprocess scheduling and browser/tool startup, and repair a demonstrated cause.
Then rerun the affected controls and maintained parent pre-push at a clean declared
head. Do not raise timeouts, waive guards, infer lane passes from progress, or close
this from a different hosted pass alone. Existing `think-nns5` tracks broader worker
baseline input fidelity; `think-w19q` tracks two other pool annotations. Coordinate
with those owners rather than conflating their scope with this observed timeout.

Evidence root:
`/Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/upstream-refresh-20261012-0635/validation/`.
Receipts: `parent-six-cpu-first-failure-classification.json`,
`parent-companion-first-failure-classification.json`, and
`interrupted-fixture-retention.json`. The preserved d0c and six-CPU fixtures live in
`retained-interrupted-fixtures/`; verified task processes are stopped. Keep unique
failure evidence outside disposable scratch. The current refreshed source/report PRs
remain #403 and #435, formal stack447; their final CI qualification is separate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->

## Notes

# Latest Captured Diagnostics, October 12

The child pre-push at `0841b84eb7435c747d23da9d7893370af5888977` passed 68
prerequisites, then produced four complete failed call phases and was explicitly
stopped with terminal exit 143. No normal/pool JUnit or lane success was completed.
The fresh CLI worker at
`test_audit_n17_certificate_dependencies::test_fresh_cli_runs_full_contract_with_visible_route_label`
hit its unchanged 20-second subprocess deadline with empty stdout/stderr.
The unchanged CLI passed serially during the focused four-control run in 12.43 seconds;
this does not establish the earlier parallel timeout's cause. Continue this diagnosis
from the preserved exact worker input and failed-phase companion.

The other three child failures have concrete, separate repairs: obsolete historical
census assertions; obsolete n=155 browser occurrence assertions; and a signal-test
fixture whose broad Popen interception wrote the RSS sampler PID as the worker PID.
The signal repair now recognizes only the exact worker launch, runs the sampler
preflight before signaling, and keeps the original worker-absence assertion and all
three interruption modes. Those source repairs do not diagnose a timeout or supply
retrospective success for the stopped broad run.

Preserve:
`child-main25-layer-push-first-failure-classification.json`, failed-phase companions,
`child-main25-interrupted-fixture-retention.json`, and
`retained-interrupted-fixtures/child-0841-layer-pytest-15/` in the protected validation
evidence root described in the issue. Parent roots 12/14 remain protected too.
Only three independently audited inactive generated repository-copy subtrees from
pytest13 were deleted; all actual-worker siblings, unknown10/11, current17 and unique
failed evidence remain. Receipt: `admin/main-e10-generated-copies-cleanup-receipt.json`.
Observed free-space gain was 522,874,880 bytes with concurrent writers; this is not an
exclusive APFS allocation-reclamation measurement.

Disposition: leave this bug OPEN for a reproducible local timeout cause and repaired
exact-head rerun. Hosted success alone, a serial pass, changed CPU sizing or test
progress does not satisfy closure. Coordinate separately with `think-nns5` input
fidelity and `think-w19q` pool annotations. No deadline, skip or assertion waiver.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
