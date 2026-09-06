---
title: Validation Efficiency Implementation Review
date: 2026-09-06
---
# Validation Efficiency Implementation Review

The W5 candidates preserve the checks inspected here.
Two artifact failure-path bugs found during review are fixed with bounded regressions.
Performance acceptance remains the
[campaign report’s](../../../packing/benchmarks/validation-efficiency/README.md)
decision after all preregistered trials; this review does not certify a speedup.

This review covers the working implementation based on main
`6b21d14b64c19003d597ed3c993c051b64336b0c` and the retained control and candidate
patches. The reviewer authored the float lookup and bridge inventory changes, so their
assessment below is an implementation audit, not an independent author review.
The gate timing code and certificate worker cap received independent inspection.

## Coverage and Source Equality

The [float helper](../../../packing/tests/test_fractional_generate.py) still computes
the exact minimum and independently enumerates reference cells with `reduce_to_cells`.
Precomputed axis maps preserve Fraction midpoint construction, float conversion, and
left-search tie handling.
The same configurations, directions, tolerances, and all-reference-cell assertion
remain. Added guards compare coincident float events with the scalar mapping and require
an empty reachable grid to report every missing cell.

The [bridge](../../../packing/devtools/check_minus_w_bridge.py) builds one
invocation-local `RowJetInventory`. Each owner calculation receives fresh active rows;
both scale calculations reuse the immutable inventory.
All fifteen scale routes, three owner checks, coefficient comparisons, and
direction-refusal checks remain.
The existing bridge success test also verifies that each stratum’s row jets are built
once. Acceptance still requires the campaign’s output-equivalence check.

At the first completed control/candidate pair for each experiment, retained JUnit
identities matched: one float-oracle test and all three bridge tests.
Selected test source hashes matched their live frozen checkouts, including the next
control start.
A follow-up audit on 2026-09-06 found that all four then-completed control
receipts matched the retained control patch’s normalized digest, but none of the four
candidate receipts matched the retained candidate patch’s digest.
Other documentation and instrumentation edits continued after that patch was captured.
The retained patch therefore does not reconstruct the candidate’s whole working tree at
measurement time.

For the affected sources, applying the retained candidate patch in memory to the stated
base reconstructed `test_fractional_generate.py`, `test_minus_w_bridge.py`, and
`check_minus_w_bridge.py` byte-for-byte against their current contents.
The reconstructed test hashes also match every completed candidate receipt available at
that audit. The bridge implementation reconstructs to SHA-256
`606ce2c6df76c13d89959989b09beffc932250984485422ef8e3c41d83dd3c04`; it was held
unchanged during trials but is not directly hashed by the receipts.
This supports the affected-source comparison, not a clean-tree or
complete-source-snapshot claim.
Both arms use the same Python 3.14.7 interpreter, one pytest process, one inner worker,
and one native thread.
Explicit `PYTHONPATH` selects each arm’s checkout.
The control also carries the certificate worker cap and exhaustive-duration
instrumentation, preventing those shared changes from becoming experimental variables.

The [certificate cap](../../../packing/src/sqpack/fractional/certificate.py) adds the
shared worker policy to the existing direction, memory, and absolute caps.
It changes concurrency without removing directions or changing serial/parallel
computation.

## Artifact Failure Paths

The [negative-control runner](../../../packing/devtools/run_negative_controls.py) now
returns a borrowed snapshot to its queue even when writing the control-start journal
fails. Previously that write occurred outside the cleanup block, potentially leaving
another control waiting forever.
The regression uses one control and a tracked queue to demonstrate the leak without
creating a hanging test.

Mutation children now receive no `PACKING_VALIDATION_ARTIFACT_DIR`. The parent retains
its unique journal. This matters because a registered control invokes a nested gate
inside a snapshot without Git metadata: inherited capture would fail during provenance
collection before exercising the intended refusal.
A test-first regression checks the actual `main`/`run_one` route with a tiny snapshot
and mocked command, verifies the child environment, and confirms the parent journal
completes.

The [gate recorder](../../../packing/src/sqpack/cli/validate.py) retains command-start
receipts before launch and streams output to files.
End receipts distinguish passing, failure, timeout, cancellation, and skip through
explicit exception types.
Hard kills can leave unmatched starts; those are incomplete observations.
A shared run ID links run, command, and step artifacts.
Provenance hashes exact tracked diff bytes and untracked files, and CI uploads artifacts
even after a failed job.
File-backed output still feeds existing gate checks after subprocess completion.

## Remaining Limits and Follow-up

The
[original benchmark instrument](../../../packing/benchmarks/validation-efficiency/runs/instrument-v1.py.txt)
strips leading/trailing whitespace when calculating its Git diff digest and directly
hashes only selected target files.
Imported untracked modules are not automatically covered, and source hashes are
collected before execution rather than verified afterward.
Frozen affected sources and retained patches support this campaign’s audit.
After all twelve trials finished, the maintained instrument was corrected to hash exact
diff bytes and untracked inputs.
It still captures source provenance before execution; it does not certify that sources
remained unchanged throughout a run.
Original receipts retain their original limitations and are not a general
source-integrity guarantee.
Allocated worker-seconds remain a scheduling proxy, not measured process-tree CPU. Warm
caches and lightweight concurrent agent work limit broader timing claims.

The worker-cap correction can increase checkpoint wall time before any pytest-level
parallel scheduling is adopted.
The main integration and deep deferred jobs use `--jobs 2 --inner-jobs 2`; both
exhaustive jobs use `--jobs 1 --inner-jobs 2`. Large default-worker `verify()` calls
therefore now respect a two-worker cap.
Previously they could use up to four workers when the host exposed enough CPUs and the
other caps permitted it.
On a two-CPU runner, that correction need not reduce their pool size.
Quick jobs use an inner cap of one, but those settings do not describe the expensive
full-verification jobs.
Exposed tests include the full retained certificate, retained n=12, n=11 acceptance and
calibration, n=17, and n=20 acceptance in `test_fractional_certificate.py`, plus the
slow n=17 verification test in `test_fractional_sweep_integer.py`. Retain the cap as a
worker-budget correctness fix, but measure the full checkpoint after these isolated
trials and evaluate any parallel rollout separately.
The planned local checkpoint uses two outer jobs and two inner workers to match the main
integration limits, on a host exposing ten CPUs; it is not a two-CPU host replica.
The float and bridge comparisons hold the cap constant, so their results cannot
establish that the whole checkpoint improved.

Keep n=40 duplicate-replay removal as a separate follow-up.
Replacing `test_the_record_round_trips` with cheap CLI equality/drift/missing-output
contracts could preserve the full gate’s real `assess_n40_rigidity --check` replay.
It would change standalone exhaustive pytest coverage and failure routing, however.
That policy change needs its own disposition and a guard proving the full gate still
invokes the complete assessor.
The expensive test and named step remain in this block.

## Validation

Focused candidate checks passed: four bridge/midpoint checks and two
midpoint/missing-cell checks.
The journal queue regression was observed failing before its fix.
The artifact inheritance regression likewise failed before its fix; four timing/artifact
checks then passed in 0.38 seconds.
Ruff, formatting, and BasedPyright checks passed for the modified negative-control
files. These short correctness runs are not benchmark observations.
No full negative-control run or gate was launched by this review while campaign trials
were active; final integration evidence belongs to the coordinating checkpoint.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
