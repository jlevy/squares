---
type: is
id: is-01m0r281yx1mhbgh5hdg38jp4n
title: "Atlas: the fields deferred from the minimum viable store"
kind: task
status: open
priority: 2
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T19:41:02.813Z
updated_at: 2026-08-23T19:41:02.813Z
---
think-eq6l shipped the minimum viable basin store -- enough to unblock the H-011 census, deliberately not the full deliverable the original bead described. These are the fields it left out, and none of them blocks a census:

- **Algebraic degree per basin.** sqpack/closed_form.py recognises (p + q*sqrt(d))/r and declines everything else, which is a yes/no rather than a degree. Degree is the field that would separate "a higher-degree optimum, legitimately unrecognised" from "not converged" -- which is currently the sharpest open question about the n = 5 census, where every repeated basin has a closed form and every singleton does not.
- **Symmetry group per basin.** The stabilizer of the packing inside the container's D4. Cheap to compute: it falls out of d4_images, which already builds all eight images and takes the minimum -- the count of images achieving that minimum IS the stabilizer order.
- **Neighbour links with merge-delta.** Which basins are adjacent, and what side you have to climb to get from one to the other. This is the structure that makes an atlas a map rather than a list, and it is what a continuation ladder (H-013) would actually navigate.

Ordering note: symmetry group is nearly free and is the one to do first. Neighbour links need a defined perturbation-and-requench protocol and are a piece of work in their own right; do not start them before the census has told us how many basins there are to link.
