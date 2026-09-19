---
title: exp-161 — Route S T-025 fixed-support compression to at most 23 orbits
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-161
  series: series-000
  title: Route S T-025 fixed-support compression to at most 23 D4 orbits
  date: '2026-09-18'
  hypotheses: [H-163]
  tier: confirmatory
  subject:
    label: >-
      T-025 exact 119-orbit support universe U025 at L=191/50, B=9977/10000, 181
      directions, closed cores
    engine: >-
      sqpack.fractional.threshold_compression decompressor and
      devtools.compress_threshold_certificate producer; coverage by
      devtools.decide_threshold_certificate
    assurance: verified
    method: exact-algebraic
    host_system: Cloud agent; project Python 3.14; encode-only timed out; no --search
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Frozen T-025 certificate.json at Git revision
      5ce2839f17b2f5a337260dc3f649e05ab974bd25, inventory catalog SHA-256
      8de1d9646efef5c49367b679a78ff20961f7f5c1d43b11ff28b5f9a6b41f0e75, N+=119,
      exact budget 685457679/62500000. T-026 720- and 1440-step certificates are
      provenance sentinels only. Before any optimizer, recompute the admission
      receipt with `python -m devtools.admit_threshold_compression --check` and
      refuse on mismatch. A retained receipt JSON is not a live check. Refuse a
      changed source, catalog, or failed mutation control before constructing a
      candidate. The three admission-control manifests cannot confirm H-163:
      full T-025 control
      53fbe28bd6dd022600515663ea1e3609ed2bd36a83e69e350b4bb3b45d7b7176,
      synthetic 23-orbit decompressor control
      007b394f48b0b11565ca87d09ad961258534c426bfd623a3e9bfc15aa6495e8a, and
      rejected 24-orbit policy control
      194f1f9f47fc94e7f945920c38a4efdb43476719eba025ea446a1d7b91fde27e.
    candidate: >-
      A D4-symmetric nonnegative rational reweighting of U025 with N+ <= 23 strictly
      positive orbit representatives, produced only by the admitted deterministic
      decompressor from a canonical nonempty selection manifest whose SHA-256 is
      none of the three admission-control manifests above. Weights may be zero
      by omission; every coordinate, threshold triple, symmetry image, domain
      parameter, and budget coefficient stays fixed. The all-zero family is outside
      the manifest language. The receipt must carry generating_account (X-032
      clause 5: a short generating account of the retained orbit pattern, not a
      restatement of N+) and selected_orbits equal to N+.
    runs_per_condition: 1
    interleaved: false
    operator: Cursor session-139 Lane C
    entry_point: packing/devtools/compress_threshold_certificate.py
    command: >-
      cd packing && uv run --frozen --all-extras --group dev python -m
      devtools.admit_threshold_compression --check && uv run --frozen --all-extras
      --group dev python -m devtools.compress_threshold_certificate
      --authorize-target exp-161
      --source cases/n11_threshold_certificate/certificate.json
      --expect-source-revision 5ce2839f17b2f5a337260dc3f649e05ab974bd25
      --expect-catalog-sha256 8de1d9646efef5c49367b679a78ff20961f7f5c1d43b11ff28b5f9a6b41f0e75
      --max-orbits 23 --budget-below 11 --least-charge 1
      --output campaign/series/series-000-smoke-and-calibration/results/agenda-036/exp-161-route-s-threshold-compression.json
    budget: >-
      One overnight target attempt after this registration. The scientific wall is
      three hours once the producer exists; the lease to 18:40Z is the
      owner-extended overnight claim, not that wall. Independent source-distinct
      replay is inside the three-hour cap. No second attempt without a new
      experiment id.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-036/exp-161-route-s-threshold-compression.json
  effort:
    timebox: 3h
    wall_seconds: 10806
    stopped_by: timebox
  results:
  - shape: determination
    role: outcome
    question: >-
      Does encode-only coverage of U025 under --authorize-target exp-161 emit a
      candidate with N+ <= 23 before the three-hour scientific wall?
    outcome: no_progress
    checked_by: >-
      timeout 10800 exited 2026-09-18T15:24:31Z with no JSON; the producer log
      was empty; --search did not run
  - shape: record
    role: outcome
    metric: source U025 N+ (encode-only produced no JSON)
    direction: lower
    score: 119
    standing_best: 23
    standing_best_source: H-163 registered N+ <= 23 criterion
    beat_record: false
    runs: 1
  verdict:
    decision: unresolved
    primary_criterion: >-
      Confirm H-163 only at N+ <= 23 with total budget < 11, least charge >= 1 from
      agreeing exact event-cell and interval routes, source-distinct manifest
      replay, a generating_account, selected_orbits equal to N+, and a manifest
      SHA-256 that is not an admission-control; refute only by exact infeasibility
      of those constraints for every N+ <= 23 family member
    reason: >-
      Encode-only hit timeout 10800 at 15:24:31Z with no JSON and no candidate.
      Timeout is unresolved, never rejected. No --search.
    resume_from: >-
      Re-run encode-only under a new lease; no partial encoding was written.
---
# Exp-161: Route S Fixed-Support Compression Target

This is the first scientific round of
[H-163](../../../hypotheses/H-163-route-s-threshold-compression.md).
[X-032](../../../explorations/X-032-route-s-threshold-compression.md) froze the family;
Sessions [134](../../../agent-sessions/session-134-n11-route-s-admission.md) and
[135](../../../agent-sessions/session-135-n11-route-s-guard-discharge.md) admitted the
target-blind instrument; PR 182 merged it as `1d9c49c4` from reviewed head `609d7d62`.
Until this artifact existed, no optimizer, candidate, or coverage target was allowed.
Session 139 ran encode-only; `timeout` 10800 exited at 15:24:31Z with no JSON.
That timeout is unresolved. `--search` did not run. The record-shape row scores
source U025 `N+=119`, not a post-encode measurement.

## Source

The control is
[`certificate.json`](../../../../cases/n11_threshold_certificate/certificate.json) at
revision `5ce2839f17b2f5a337260dc3f649e05ab974bd25`. The admitted inventory catalog
SHA-256 is `8de1d9646efef5c49367b679a78ff20961f7f5c1d43b11ff28b5f9a6b41f0e75` (119
orbits, 904 atoms, budget `685457679/62500000`). T-026’s 720- and 1440-step certificates
check support identity and the documented uniform rescaling only.
They are not controls, targets, or a promise that a compressed certificate keeps the
dilation-limit bound.

## Target

Search the frozen U025 reweighting family for one nonempty canonical selection with
`N+ <= 23` that decompresses to a certificate the existing two coverage routes both
accept at least charge one, with exact budget strictly below eleven.
The producer may not move sites, change threshold triples, add atom classes, or change
the net or shrink.

## Accept, stop, refuse

The N+ <= 23 metric, budget < 11 rule, and least-charge >= 1 rule are unchanged.
What follows operationalizes X-032’s five confirmation clauses and the statement that
admission controls cannot resolve H-163.

- **Accept H-163** only when all five X-032 confirmation clauses hold, including
  source-distinct replay of the manifest, reconstructed certificate, and both coverage
  routes; the live `admit_threshold_compression --check` passed immediately before the
  target; the receipt carries `generating_account` and `selected_orbits` equal to `N+`;
  and the candidate manifest SHA-256 is none of
  `53fbe28bd6dd022600515663ea1e3609ed2bd36a83e69e350b4bb3b45d7b7176`,
  `007b394f48b0b11565ca87d09ad961258534c426bfd623a3e9bfc15aa6495e8a`, or
  `194f1f9f47fc94e7f945920c38a4efdb43476719eba025ea446a1d7b91fde27e`.
  Smaller files, simpler denominators, or fewer distinct weights do not meet `N+`.
  Decompressing, coverage-checking, and scoring an admission-control manifest is not
  confirmation.
- **Refute H-163** (`rejected`) only with an exact infeasibility certificate that no
  family member with `N+ <= 23` meets the frozen budget and coverage constraints.
- **Unresolved** if the three-hour scientific wall expires, the overnight lease expires
  first, the search saturates without a candidate, or a coverage route disagrees.
  Park only this frozen family. Timeout is never `rejected`.
- **Blocked** (no scientific verdict) if the live `--check` fails, the source, catalog,
  mutation controls, or decompressor fail, `--authorize-target exp-161` is missing, a
  candidate is built by any path other than the admitted decompressor, or the candidate
  manifest is one of the three admission-control SHA-256 values.

A bounded unsuccessful search is not a negative.
A failed control is not a negative.

## Independent-review boundary

A source-distinct reader must reconstruct the candidate from its canonical manifest and
re-run both coverage routes without trusting the optimizer’s summary.
The reviewer may not share the producer’s working set.
T-025 and T-026 `verify_claim.py` are not this round’s reader and must not be edited.

## Retained evidence paths

- This experiment artifact.
- Producer receipt:
  `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-036/exp-161-route-s-threshold-compression.json`
- Canonical selection manifest beside that receipt, once one exists.
- Admission receipt already retained at
  `packing/cases/n11_threshold_certificate/route-s-compression-admission-receipt.json`
  (historical: `experiment_created: false` at admission; this round is the later
  allocation).

The named producer `devtools.compress_threshold_certificate` is part of this round and
must exist before the target half of the command runs.
Building it is not a target.
Running it under `--authorize-target exp-161` after a live `--check` is.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
