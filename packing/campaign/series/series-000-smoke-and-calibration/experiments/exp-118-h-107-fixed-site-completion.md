---
title: exp-118 — one fixed-site scalar row completion
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-118
  series: series-000
  title: Complete the retained scalar rows without changing sites
  date: '2026-09-07'
  hypotheses: [H-107]
  tier: confirmatory
  subject:
    label: Terminal exp-116 fixed sites and exact rows at 61/16
    engine: Single row-completion adapter with retained failure and candidate receipts
    engine_commit: 46f38ab4
    assurance: numerically-checked
    method: numerical-f64
    precision: {binary_bits: 64, rounding: nearest ties-to-even in the numerical LP; exact rational snapping and candidate construction}
    tolerance: No floating value accepts the claim; every positive outcome requires all declared exact decisions.
    host_system: macOS arm64, Python 3.14.7, one numerical worker on a shared host
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Nine independent source-free adapter controls pass, including a verified
      side-two cover, mass/deadline refusal, vector-prefix retention and net
      identity. The complete proof-chain controls passed in the 99a3ad42 full
      gate; all sqpack source, source-certificate files, standalone verifiers,
      decide_certificate.py and locked dependencies are unchanged through
      2707ea39 and the 46f38ab4 instrument commit. The later full gate at
      2707ea39 passed in 1496.68 seconds.
    candidate: >-
      The 24,653 sites and 11,885 initial rows from terminal exp-116; 181 uniform
      half-angle parameters ending at 207107/500000; eight additional row rounds,
      three rows per direction, an 1800-second cooperative row deadline, bridge
      snapping denominator 1000000 and rationalization scale 4000000.
    runs_per_condition: 1
    interleaved: false
    operator: Codex coordinator, max mathematical reasoning, Session 090 BC-252
    commit: 46f38ab4
    dirty: false
    entry_point: packing/devtools/run_fixed_site_completion.py
    command: >-
      /usr/bin/time -p /opt/homebrew/bin/timeout --signal=KILL 2100s
      env PYTHONPATH=src OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
      VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
      /Users/levy/wrk/github/squares/packing/.venv/bin/python3
      -m devtools.run_fixed_site_completion
      --state /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01-state.json
      --output /Users/levy/wrk/github/squares/packing/campaign/series/series-000-smoke-and-calibration/results/exp-118-h-107-fixed-site-completion/attempt
      --n 11 --side 61/16 --core 9977/10000 --angle-limit 207107/500000 --steps 180
      --rows-rounds 8 --rows-per-direction 3 --deadline-seconds 1800 --scale 4000000
    budget: >-
      One 2100-second external whole-process cap including startup and tail;
      the 1800-second cooperative row clock starts after reconstruction. No
      intermediate objective threshold stop, retry, site change or extra rounds.
      One conditional verification sequence shares 1200 seconds externally across
      declaration, full production decision and independent standalone replay.
      The Session 090 launch cutoff was 03:16 UTC to preserve the 20-minute closing
      reserve. Future launch requires a fresh sufficient allocation and renewed
      operational lease after passing record checks.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/exp-118-h-107-fixed-site-completion/attempt/receipt.json
  effort:
    timebox: One 2100-second target allowance and one 1200-second verification allowance, both unspent
    wall_seconds: 0
    stopped_by: dependency
  results:
  - shape: determination
    role: guard
    question: Did all launch prerequisites pass before the 03:16 UTC cutoff?
    outcome: criterion_missed
    checked_by: The selected launch cutoff passed before the record gate; no target or verification process was invoked and no scientific output exists.
  verdict:
    decision: blocked
    primary_criterion: Exact complete fixed-site covering measure of mass below eleven.
    reason: The prospective record gate was not complete by the 03:16 UTC launch cutoff; no target or verification process ran and both allowances remain unspent.
---
# exp-118 — Fixed-Site Row Completion

This is the unlaunched protocol for
[H-107](../../../hypotheses/H-107-fixed-site-scalar-completion.md), not an unchanged
exp-116 retry. The record gate was incomplete at the selected 03:16 UTC launch boundary,
so the coordinator did not dispatch the target or borrow the closing reserve.
Neither process allowance was consumed.
The new full gate subsequently passed on `2707ea39` in 1496.68 seconds; the nine new
adapter controls passed separately.
A fresh sufficient allocation may activate this unspent protocol after record checks and
a renewed operational lease.
The failed launch guard records a scheduling block; H-107 was not tested and remains
unresolved.

The command, source and receipt path above describe the proposed invocation; no target
receipt or scientific output exists.
Commit the protocol and pass record checks before any future launch.
Run from a clean detached `46f38ab4` checkout’s `packing/` directory with its source
selected by `PYTHONPATH=src` and the existing project interpreter supplying
dependencies. All output paths must be absent.
The adapter exclusively creates its `attempt/` directory.

The legacy state and summary are committed in [exp-116](exp-116-h-093-scalar-61-16.md).
Before the sole invocation, compare its side, core, 24,653 sites and 11,885 rows with
the declared metadata; the adapter checks exact containment, D4 closure and the supplied
uniform net. Preserve the input bytes in the attempt receipt directory, without adding a
redundant digest.

The adapter’s independent review completed at 03:13:19 UTC with nine passing controls,
clean Ruff and formatting checks, and zero BasedPyright findings.
It retains the complete available primal and dual vectors and identifies the exact row
prefix to which each dual belongs.
The existing proof-chain source controls may be reused:
[Session 089](../../../agent-sessions/session-089-agenda024-next-phases.md) records the
complete `99a3ad42` gate passing in 1487.51 seconds, and read-only Git comparison shows
no change to any `sqpack` source, source-certificate files, standalone verifiers,
`decide_certificate.py`, `pyproject.toml` or `uv.lock` through this instrument commit.
This is reused completed evidence, not a fresh 3.81 CLI run or zero historical cost.
The new full gate at `2707ea39` was still in flight at the launch cutoff and was not
assumed to have passed then.
Its subsequent completion provides additional validation; it does not retroactively
satisfy the missed launch cutoff.

Keep the earlier proposed 2700-second target price as planning history.
The selected 2100-second external cap is shorter; reconstruction or the unsnapped round
may consume its tail and leave only a started receipt.
That is unresolved, never convergence.
The cooperative clock does not stop a running LP or cover final rationalization.
No objective-at-eleven stop was added.
A scientific cap cannot be reset by interruption.

An actual exit zero and `candidate-unverified` permit the separately bounded proof
sequence. Preserve pre-declaration candidate bytes, then run `declare_least_cell_mass`,
full `decide_certificate` (not `--quick`) and `minimal_verify.py --unpinned` on the
declared file. These sequential commands share one 1200-second external deadline,
including orchestration, rather than receiving 1200 seconds each.
Keep one worker. The production 4096-atom and 8 MiB ceilings remain unchanged; no atom
pruning is allowed. The unpinned minimal verifier has no 2000-atom ceiling, but remains
within the shared cap.

Accept only if both production routes and the standalone reader agree on frozen bytes,
instance, nonnegative D4 weights, mass below eleven, the net/shrink premises and minimum
coverage at least one; the production interval enclosure must have width zero and equal
the sweep’s exact minimum.
A failed declaration leaves its input unchanged.
Any other result is unresolved, including oversized output, numerical mass at least
eleven, nonconvergence, timeout or missing publication.
No finite-site dual rejection is implemented.
Record actual process exits and outer wall/CPU costs separately from the adapter’s
internal timing and operator allocation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
