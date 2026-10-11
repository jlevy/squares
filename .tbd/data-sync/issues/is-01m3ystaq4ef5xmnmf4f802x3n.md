---
type: is
id: is-01m3ystaq4ef5xmnmf4f802x3n
title: "Independent measure verifier, slice 2: baseline profile of the authors' checkers"
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T17:15:30.916Z
updated_at: 2026-10-02T18:05:40.345Z
closed_at: 2026-10-02T18:05:40.324Z
close_reason: "Profile committed (tool b925765f9, outputs and research note a135a140a): PROFILE_RETAINED, every complete direction reproduced its recorded nodes. Clean timings at packing/benchmarks/results/author-checker-profile-2026-10-02/timings.json; dirty attribution in attribution/ and docs/project/research/research-2026-10-02-author-checker-profile.md. Child CPU about 24 minutes for the final run, about 50 in all."
resolution: null
duplicate_of: null
---
Lane W1 (dirty side). packing/benchmarks/profile_author_measure_checkers.py builds Tokoharu's verify.cpp and wand125's mixed and linear checkers from the retained packets, regenerates inputs from the retained candidates, requires every complete direction to reproduce its recorded nodes, and writes timings.json (implementer-readable) and attribution/ (dirty: gprof and callgrind). The research note docs/project/research/research-2026-10-02-author-checker-profile.md interprets the attribution and is not an implementer input. Exit: committed outputs.
