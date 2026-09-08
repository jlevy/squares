# Math Startup and Layout Stability

This W7 continuation answers `think-qcmi`: can the published page reserve the final
space of its mathematics and show the interactive parameters sooner?
The owner reports that the font swap is gone, but delayed mathematics still moves the
text after it. The control is the deployed Squares revision
`33cd47606dae223664f117945631440aa5c8ece9`, with KPress
`7b20ae702acf37020e6132265c8faa0ba74e4465`.

## Integration plan

The coordinator owns records, CI, integration, and release.
Three delegates own the startup probe, Squares preparation and scheduling, and the
shared KPress runtime.
The first integration checkpoint targets four hours from the 2026-09-08 15:49 UTC
delegation, with these slices, each at most thirty minutes:

1. Retain a frozen control, design the three disjoint changes, and prove the probe’s
   positive and negative controls.
   Run the records tier before adding records.
2. Calibrate normal startup on the control at both widths.
   Prepare the publication CI path and freeze the hypotheses before the first candidate
   measurement.
3. Integrate measured math geometry and runtime hydration.
   Review correctness of wrapping, font profiles, baseline alignment, and failure
   fallback.
4. Integrate parameter-first scheduling.
   Run the focused input, hidden-certificate, print, and no-swap checks; correct
   failures before measuring performance.
5. Efficiency slice: review instrumentation overhead and the publication dependency
   graph; remove duplicate work that does not establish a distinct contract.
6. Freeze the candidate and run the paired comparisons sequentially on an otherwise idle
   host. Record invalid and rejected experiments as well as successes.
7. Review both repositories, run the required local validation, and publish the upstream
   PR. Continue documentation and independent review while CI runs.
8. Integrate the merged upstream revision, validate and merge Squares, then verify the
   actual Pages deployment and its live rendering.

At each boundary, record elapsed work and the remaining critical path.
A long gate runs asynchronously; inspect it at the next integration boundary.
The four-hour target does not authorize skipping a failed check or abandoning unfinished
fixes.

At the first boundary, 16:19 UTC, the records tier passed in 32.93 seconds and the
eleven reporting/publication contract tests passed in 0.41 seconds.
The three delegated implementations were still in flight.
Probe controls passed, but real control pages exposed a legitimate early frame with no
certificate selected; distinguishing that initialization phase and observing the new
hydration API extended the probe slice.
The source review also found all certificate figures initially hidden, tracked as
`think-tpsi`. The next critical path is the delayed-font geometry guard, followed by an
idle-host measurement window; CI preparation and record validation can continue without
waiting on that guard.

At the 17:01 UTC boundary, the six baseline observations are retained and the startup
instrument is frozen at `f95150e4`. KPress PR 61 passed its first complete CI run, but
the independent held-transfer geometry guard found a WebKit readiness defect in the
integrated candidate: a lone relation could appear while its font request was pending.
The guard remains red while KPress is corrected; no candidate timing has run.
The efficiency review removed duplicate publication builds by sharing one prepared
artifact across browser jobs.
It also removed unused-font warmup and deferred hidden heat maps.
Their latency effect remains unmeasured.

The owner added a small downward bullet adjustment and a canonical architecture document
in KPress. The marker review found and corrected an obsolete line-height override that
stretched the new CSS square into a bar; retained negative controls now check its shape
as well as position.
Independent host review also corrected print visibility and native fallback state.
The next slice finishes the WebKit fix, then freezes the final prepared artifact for
correctness and paired timing.

## Measurement protocol

Run `python -m devtools.check_math_startup` through the frozen project environment from
`packing/`. Use its retained `--self-test` first.
Baseline calibration uses three fresh Chromium runs at each of 1280 by 720 and 390 by
720 CSS pixels. Confirmatory comparisons use twelve control/candidate pairs at each
width, with arms interleaved by the instrument.
Keep the page files fixed for the whole comparison.
Use local files for both arms; live-site checks are a separate deployment check.

Each trial starts a fresh browser.
Filesystem and OS caches are uncontrolled and are not flushed.
Do not run other browsers or heavy validation during measurements.
The probe observes normal navigation without holding fonts, changing inputs, scrolling,
resizing, or printing.
Record the real viewport, focus and visibility, selected certificate, source identity,
and instrument environment with every run.
Raw JSON belongs in `runs/`; no number is copied by hand into the generated report.

The primary latency is `parameters_ready_ms`: the first sampled frame with all fourteen
active Figure 6 math labels and readouts present and correct for the initial angle.
Adjacent-text anchors record both absolute movement and movement relative to their
containing block. A character range’s bottom is a baseline proxy, not a DOM baseline.
Movement of surrounding prose fonts can contribute to those measurements, so the
independent delayed-font geometry check must distinguish math-box movement from other
page changes.
The existing delayed-font and early-input probe remains a correctness test,
not a normal-load timing instrument.

The [idea board](ideas.md), [exploration](explorations/X-001-startup.md), and hypothesis
records preserve the alternatives and their acceptance rules.
The timing criterion is fixed before candidate measurements.
A layout fix may be accepted on correctness even if the separate latency hypothesis is
rejected; it must not then be described as a measured speed improvement.

## Reproduction and report

Run the startup probe’s `--help` for the control/candidate and viewport arguments.
Run `python -m devtools.report_math_startup` to validate the records and regenerate
`ledger.md`; `--check` verifies the generated view without writing.
This report is an engineering experiment record, not a new timing gate in CI.
Correctness controls and the fast record tests run in CI; absolute startup times do not
determine a PR’s status.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
