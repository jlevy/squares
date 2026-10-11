---
type: is
id: is-01m2bmgc6v2dx391qsg393hw2m
title: "N11 BC327 stage 4: paired instrument and exact common manifests"
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research-tooling
dependencies: []
parent_id: is-01m26697w7prvp4mdkme3cspdc
created_at: 2026-09-12T20:21:25.850Z
updated_at: 2026-10-06T08:38:24.601Z
closed_at: 2026-10-06T08:38:24.601Z
close_reason: "Superseded by T-060: s(11) equals Trump's side, registered 2026-09-29 at V3/C3 and on main since PR #246 (merged 2026-09-30). This n = 11 lower-bound certificate work has no target left; the owner's 2026-09-14 strategy reset had already paused it, and the post-optimality plan (plan-2026-10-01) uses n = 11 only as a control."
resolution: canceled
duplicate_of: null
---
Stage 4 of the weighted five-site atom admission review, blocked on stage 3. Build the maintained paired-program producer and its exact common row and point manifests: the same matrix on common columns, treatment-only additions, exact orbit costs, all-one multiplicities reproducing legacy rows, and cap, deadline, partial-result and forged-witness refusals passing. A scouting pass established that a common row and point manifest has NO precedent in this repository -- it is named as missing evidence in two documents and CertificateManifest does not exist in code -- so this stage builds it rather than extending anything. Take the manifest idiom from devtools/owner_footprints.py (frozen slotted dataclass, validated once) and the row-by-site content from sqpack.fractional.cutting, but in exact arithmetic: cutting.py is float and that is what the review tells us to stop doing. No finite scientific comparison may be registered until this passes.
