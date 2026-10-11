---
type: is
id: is-01m45jyta2e4skrjhc0g6f1h0a
title: "Import squarepacker: s(12) >= 7943/2000 at 98ffe37, v1.1 (no issue)"
kind: task
status: closed
priority: 1
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
created_at: 2026-10-05T08:30:18.946Z
updated_at: 2026-10-05T17:00:50.237Z
closed_at: 2026-10-05T17:00:50.237Z
close_reason: Superseded by think-3kd9 (#363 is the same v1.1 claim, now reported as an issue)
resolution: null
duplicate_of: null
---
squarepacker/s12-lower-bound 98ffe37334c63df8ab209f1f43f4c5642d5d2ee2 (2026-10-05T08:26:42Z, 'Add v1.1: s(12) >= 7943/2000'; Zenodo DOI 10.5281/zenodo.23106581) reports s(12) >= 7943/2000 = 3.9715 by a weighted point certificate s12_lower_3.9715.txt in Daniel's format: Evan Daniel's 1736 points of s12_lower_3.9686.txt (evand/square-packing 7d6f46d) dilated to the larger container and rounded to the grid 1/4000000 with D4 orbits rebuilt exactly, and new weights from linear programming (this project's Route B with a full exact scan in every cycle), total weight 11.9974808. The source reports it accepted by Daniel's verify at N = 96000 (min covered weight 1.000005) and by its own independent checker at N = 24000 to 192000, with two negative controls, a paper (paper/s12_lower_3.9715.tex/.pdf) and SHA256SUMS. It is above the verified 15680000/3949423 (T-079) by 10266889/7898846000, about 0.0013, and above the source's v1.0 31360/7901 (packet squarepacker-s12-lower-bound-2026-10-02). No issue on jlevy/squares asks for it; the intake sweep found it as one commit past the v1.0 pin. Stage 1 to 3: claim map, packet at 98ffe37 (new key), reported evidence, coverage, a register entry at V0, the n-012 reported lane. Replay price from the source's own .time files: Daniel's verifier about 49 minutes on two threads at N = 96000 (about 1.6 CPU-hours), the independent checker about 8 minutes on one core; T-079's replay tooling may decide it without the source's code. Held in packing/campaign/intake-watch.yaml as a read of 98ffe37 naming this bead.

## Notes

2026-10-05 08:40Z: the head moved to 7a96bec36bc6811c3715ef581598f22ff9b7ba3a (2026-10-05T08:31:05Z), which adds only .zenodo.json; the intake-watch read now names that head. Pin the packet there.
