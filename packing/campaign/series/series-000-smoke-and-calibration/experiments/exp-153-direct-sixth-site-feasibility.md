---
title: "exp-153 \u2014 direct complete-domain sixth-site feasibility"
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-153
  series: series-000
  title: Direct complete-domain sixth-site feasibility
  date: '2026-09-09'
  hypotheses:
  - H-151
  tier: exploratory
  subject:
    label: Exact feasible region for any added sixth site with D and owner tuple fixed
    engine: Complete-domain support extrema over exact vertical-decomposition closures, closed half-plane
      intersection, and independent polygon-union confirmation
    assurance: verified
    method: exact-algebraic
    host_system: Darwin arm64; project Python 3.14; one process
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: Support-sign extrema, all component vertices, open-domain closure and tangency, point/segment
      site-region retention, empty-prefix versus incomplete-positive semantics, shared deadline, independent
      candidate confirmation, and provenance controls; Astra Max source admission.
    candidate: Reconstruct the admitted two-core intersection. For each required direction decompose the
      original nine-obstacle D-missed domain and intersect four exact support inequalities. Stop with
      complete family refutation if empty; otherwise finish all 361 and confirm the mean of final vertices
      on all 361 directions with ten-obstacle union at ceiling1023.
    runs_per_condition: 1
    interleaved: false
    operator: GPT-6 Astra coordinator; implementation by GPT-5.6 Sol extra high; mathematical admission
      by GPT-6 Astra max
    entry_point: packing/devtools/wall_owner_sixth_site_feasibility.py
    command: cd packing && /opt/homebrew/bin/timeout --signal=TERM --kill-after=2s 300s .venv/bin/python3
      -m devtools.wall_owner_sixth_site_feasibility campaign/series/series-000-smoke-and-calibration/results/agenda-032/exp-143-four-owner-footprint-cover.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-146-wall-owner-footprints.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-149-selected-wall-tuple-cover.json
      campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-151-selected-six-dot-cover.json
      --expect-six-dot-blob 46d34b1e295d9f5178379b02780a8c598c1a73e5 --expect-six-dot-source c8cd38dad502c78840144bcae42df4294ba7f3d0
      --expect-endpoint-blob cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19 --expect-wall-blob e54fa98133db5f2135cae8875188f51b7db26e12
      --expect-wall-source 915758898a97c92793f51e62b7a6b17f846895ca --expect-selected-blob 83ec897738d6d1b228623c3ac4c10cd9170d5940
      --expect-selected-source 5600c0fb4eccf9e9dcdf82b02506d3d4340651cb --expect-git-revision "$(git rev-parse
      HEAD)" --deadline-seconds 240 --output campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-153-direct-sixth-site-feasibility.json
    budget: One300-second external process plus two-second grace and shared240-second internal guard after
      loading. No retry, per-direction clock reset or adaptive candidate loop. Initial source-slice latest
      launch19:01:38 UTC expired unrun. At19:06:09 UTC, Session122 phase2 was prospectively allocated
      through19:36:09 UTC; latest launch19:31:07 UTC fits the full302-second allowance. Preserve source
      and target evidence if it does not fit; never launch late.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/exp-153-direct-sixth-site-feasibility.json
  results: []
  verdict:
    decision: in-progress
    primary_criterion: All 361 complete-domain support constraints leave a nonempty exact site set, and
      its one canonical candidate independently passes all 361 exact zero-deficit union checks before
      the shared deadline.
    reason: Prospective and unrun. Exp152 establishes only two-witness feasibility; this complete-domain
      calculation may settle the entire fixed-D-plus-one-site family.
  lease:
    expires: '2026-09-09T19:36:09Z'
    host: local
---
# Exp153: Compute the Entire Feasible Sixth-Site Region

**Prospective and unrun.** The
[admitted design](../../../../cases/n11_five_dot_cover/direct-sixth-site-contract.md)
replaces a bounded sequence of guessed sites with one exact support pass over the
complete original-D-missed domain.
[Independent source admission](../../../../cases/n11_five_dot_cover/direct-sixth-site-source-admission.md)
is GO:33 combined controls passed independently in3.41seconds; final source and test
blobs are retained there.
Target remains unrun pending clean publication.

For each nonempty direction domain U and core axis u, enforce
`sup(u·c)−h ≤ u·p ≤ inf(u·c)+h`, and likewise for v. Extrema range over all vertices of
all positive-area component closures, not component means.
A closure attainer is not labelled as a strict escape.
Preserve zero- and one-dimensional feasible-site sets.

An empty processed-prefix intersection is a complete fixed-D-plus-one-site refutation.
A nonempty prefix is unresolved.
After all 361 constraints, check the canonical mean of distinct vertices against every
inequality and independently confirm all 361 D-plus-site union deficits are zero.
A deficit at that stage is inconsistent/invalid, not permission to choose another
candidate.

One absolute240-second internal deadline covers reconstruction, support construction,
final membership and confirmation.
Completed support-direction checkpoints are atomic records inside this one
immutable-source experiment, with no Git publication or clock reset between directions.
Confirmation rows are retained on cooperative return, but an external kill during
confirmation can leave only the last support checkpoint.
The300-second external guard plus two-second grace bounds loading and output as well.
Retain per-stage timings so decomposition cost is measured rather than guessed.

Empty intersection refutes one added site with D fixed; it does not refute weighted
additional mass below two unless a disjoint pair of actual D-missed cores is separately
proved. Any successful conditional cover leaves global owner routing open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
