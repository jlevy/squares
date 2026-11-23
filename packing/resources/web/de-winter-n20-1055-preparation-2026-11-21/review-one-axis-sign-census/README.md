# Independent one-axis sign census and D4 audit

The independent checker completes the finite sign/vacancy census implied by the accepted
paired-bridge conditions for `0 < tan(theta/2) <= 1/24`. It checks all 120 vacancy
permutations and twenty aligned-square positions, retains 29,368 sign assignments, and
checks all 234,944 D4 images.
They form exactly 3,671 orbits, each of size eight.
All twelve predeclared controls pass.

This is a necessary-condition roster for one aligned square and nineteen independently
signed equal-magnitude tilts in a hypothetical board `S < 5`. It does not assert that
any retained assignment is geometrically feasible.
The reviewed near-grid reduction and the geometric paired-bridge implication remain
premises of this finite check.

## What was checked

The checker constructs each horizontal and vertical chain directly from their shared
diagonal cells. It enumerates the chain’s local sign vectors and computes their integer
costs. For every bridge, at least one chain must have zero cost by the
[accepted local exclusions](../review-one-axis-bridges/README.md).
A finite constraint search retains every assignment satisfying those disjunctions, fills
all remaining free signs and independently checks the resulting assignments against the
direct cost formula.
It visits 3,624 search nodes and emits 29,368 assignments.

The D4 audit reconstructs four quarter-turns with and without reflection.
Rotations preserve tilt signs; reflections negate them.
The aligned cell and every occupied-cell index are transported explicitly.
Every image must belong to the complete roster, and every representative must regenerate
its orbit. The paired-bridge counts also match: 92 vacancy permutations have four
bridges, 24 have five, and four have six.

The receipt retains all 2,400 case counts, all 29,368 assignments and all 3,671
representatives. Its canonical roster SHA-256 is
`b7203bf5e99c7df4e72819440a72b1487e84bac5478686ca7fe2e639bd142e5d`. The checker binds
the original accepted bridge receipt by digest; it does not rerun that polynomial check.

The reviewer had read the producer’s proof and sign/path programs.
The direct bridge construction, local truth tables, constraint search and
rotation/reflection implementation were written separately, without importing or
executing contributor programs.
This is an independent implementation with disclosed exposure.

## Frozen inputs and completed runs

Use the [specification](census-spec.json), [frozen plan](frozen-plan.md),
[freeze](freeze.json), [checker](checker.py.txt), and retained
[bridge input](bridge-verification.json.gz).
The freeze’s prepared-only status describes the moment before execution.
The original checker name was `check_one_axis_sign_census.py`; its bytes are unchanged
under `checker.py.txt`.

Two runs are retained.
The coordinator first launched the ordinary invocation, then repeated the frozen `-I -B`
invocation. The [isolated receipt](sign-census-isolated.json.gz) and
[first receipt](sign-census.json.gz) are byte-identical after omitting only the three
root fields `wall_seconds`, `cpu_seconds` and `peak_rss_bytes`. The
[equivalence audit](receipt-equivalence.json) records both original identities, the
exact comparison rule and the common substantive digest.

| Run | Supervised wall | Internal wall | Worker peak RSS | Worker exit | Observer exit |
| --- | ---: | ---: | ---: | ---: | ---: |
| First invocation | 4.893 s | 4.303 s | 57,671,680 bytes (55.0 MiB) | 0 | 0 |
| Isolated invocation | 5.396 s | 4.951 s | 56,147,968 bytes (53.5 MiB) | 0 | -2 |

The isolated run’s observer returned `-2` during shutdown after the worker exited zero.
Its retained stderr reports the observed process exited and zero interventions; the five
samples have maximum memory pressure 1. The first run also has five samples at maximum
pressure 1. Their maximum sampled process-tree costs are respectively 0.03 and 0.02 GiB,
separate from worker peak RSS. The supervisor reports both workers completed; neither
reached a cap. The isolated observer exit is not reported as zero.

Retained execution evidence: [first supervisor](execution.run.json),
[first preflight](execution.preflight.json), [first journal](execution.jsonl),
[first observer log](execution.guard.stderr);
[isolated supervisor](execution-isolated.run.json),
[isolated preflight](execution-isolated.preflight.json),
[isolated journal](execution-isolated.jsonl),
[isolated observer log](execution-isolated.guard.stderr).
These files accompany the receipts; transient scratch is not needed to inspect them.

From this directory, with the project Python 3.14 interpreter and an external
supervisor:

```bash
"$PYTHON" -I -B checker.py.txt --spec census-spec.json \
  --bridge-receipt bridge-verification.json.gz --output "$OUT/sign-census.json"
```

The output must be new.
Use one worker, external scratch/cache directories and the frozen limits: 60 seconds,
0.25 GiB sampled process-tree cost, stop at memory pressure level 2. The checker also
imposes its declared search, emission, roster and 55-second internal bounds.

## Remaining obligations

This census depends only on the paired-bridge necessary conditions.
It does not use general-path clauses or the
[576-certificate polynomial bank](../review-one-axis-bank/README.md).

The separate [general-path review](../review-one-axis-general-paths/README.md) now
classifies all 29,008 local profiles, excluding 23,286 and leaving 5,722 not certified.
The [path covariance audit](../review-one-axis-path-covariance/README.md) checks all
occupied paths and their D4 maps.
The [case-to-clause audit](../review-one-axis-case-clauses/README.md) applies the local
decisions to all 3,671 canonical cases and binds their orbits to all 29,368 assignments.
Complete separation-graph enumeration, geometric rule extraction and graph-to-bank
coverage remain open.
The source’s 273,584 graphs and 566 used certificates remain producer reports.
The one-axis theorem has not cleared Stage 4, and neither the angular-diversity theorem
nor an unrestricted lower bound is accepted by this finite census.

## Compressed Files

| Stored path | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `sign-census.json.gz` | receipt | `ddda8efa9ec50b03d75cf444dcacc6547642dd93` | `45d16648622df9321d4ca3105bf3b2014b049e3774f3b89b3955fbd8ddd4654a` |
| `sign-census-isolated.json.gz` | receipt | `3cd64b80b74221bfbd0302d5b1ac5af3ef1033a0` | `fc75c5853c16cc99e3cbdda6661ddcfb5a0d6d2b0698c47c9f7747351ccd96fe` |
| `bridge-verification.json.gz` | receipt | `69f62be84b71b713500296344d8a6f8c629d8ccc` | `a8b48b5cff9b0b101174e3eb513bb3ed502c05bbfb825e1f8b376fb0c017d286` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
