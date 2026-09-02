# Review: Agenda 015 Second-Wave Efficiency

**Date:** 2026-09-02

**Author:** Codex, for the project maintainers

**Status:** Complete BC-144 W5 receipt; decision is `no-change`

This is agenda-015’s second W5 `efficiency-loop` slice.
It applies the predeclared change-admission rule at frozen evidence revision
`313624cc08650bb9054e969da9cfd91ad83e2125` and changes no scientific instrument, result,
criterion, threshold, route or review flag.

## Verdict

Record **`no-change`**.

The registered wave-efficiency renderer cannot produce an admissible second-wave table
while the ten-hour coordinator is active.
Normal and optimized Python both refuse because session-078 is `in_progress`.
Session-082 also declares the coordinator’s shared parent task-tree receipt rather than
a lane-isolated interval: the retained snapshot ends before session-082 began, and
treating it as the lane would double-count the coordinator rather than measure BC-141.
No table is retained or reconstructed by hand.

## Frozen Evidence

| Artifact | SHA-256 |
| --- | --- |
| `packing/devtools/render_wave_efficiency.py` | `edb68a2a6f082695320be752e10279c843fc85a2ee7b49e5f46773cb2e763877` |
| session-078 at the evidence revision | `0eaba23e7b7afe45aadd484c55703c609ceff331978cf07049cae04b613f4f3a` |
| session-082 at the evidence revision | `858c5a76396f8244e0861c61bc996cc4abd05c7850f3bf1683a48ee5beb2a0ad` |
| shared session-078 task-tree receipt | `5b88d3ad915f2f8df3ec2aecfe6de752ea80a164b12944c2b4bf303e7e881cc3` |
| BC-143 W5 receipt | `af5f977657233ea1142b9bc04ef9999c52913a01db238734934d75cd4bc3ab25` |

Session-082 is the only separate wave-two AgentSession.
Session-079 owns BC-137’s wave-one instrument preparation but explicitly assigns the
long process and observations to session-078. Sessions 080 and 081 are wave-one lanes
already covered by BC-143.

## Registered Renderer Outcome

From `packing/`, normal and optimized Python ran the same registered arguments once:

```text
uv run --frozen --all-extras --group dev python -m devtools.render_wave_efficiency --lanes session-082 --coordinator session-078 --format json
uv run --frozen --all-extras --group dev python -O -m devtools.render_wave_efficiency --lanes session-082 --coordinator session-078 --format json
```

Both exit 2 and emit the same 59 bytes, whose SHA-256 is
`7687158e83453b7adb873845dd861d9243bf3c6c11408fa97ed26f3fc020c82e`:

```text
refused: session-078: status 'in_progress' is not terminal
```

The refusal is different from BC-143’s D-421 mixed-harness refusal.
Session-082 declares a Codex receipt, but it is the shared parent receipt and is not an
isolated BC-141 measurement.
Omitting the coordinator would mislabel that parent aggregate as the lane; later using
the same receipt for both rows would duplicate the interval and yield a meaningless zero
residual.

## Change-Admission Test

| Candidate | Profile | Frozen before/after input | Equivalence | Rollback | Positive remaining-wall repayment | Disjoint | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BC-142 reachable-test map | 13 of 115 files; no commensurate baseline | checkpoint frozen; no valid pair | **fail** — no exact-set oracle | pass — map-only seam | **fail** — no like-for-like timing pair | pass | no-change |
| Mixed-harness efficiency adapter | D-421 refusal only | no implementation or pair | **fail** — no tested common schema | absent | **fail** — no measured candidate | pass | future W7 |
| BC-141 zero-proof memoization | bounded reproducer and post-repair equivalence | same parser fixture | pass for correctness | pass — parser-local cache | **fail** — no prospective repayment contract | **fail** — repaired inside the active lane | no-change |

Agenda-015 requires all six guards to pass.
None of the candidates qualifies, and the unavailable lane-isolated receipt supplies no
new candidate.

## Boundary

This W5 decision changes no experiment verdict, hypothesis disposition, instrument
state, review flag or route.
Exp-056 remains unresolved and review-pending with a 170-row agreeing prefix; exp-057
remains unresolved before target access; BC-141 is complete as synthetic-only
instrumentation and H-055 remains instrument-unready.
The missing isolated receipt and the mixed-harness adapter remain future W7 work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
