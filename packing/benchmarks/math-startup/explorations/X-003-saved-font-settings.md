---
softschema:
  contract: squares.math-startup.exploration.v1
  schema: ../schemas/exploration.schema.yaml
  status: enforced
id: X-003
title: Prepared geometry must cover supported saved settings
proposes: [H-004]
---
# Prepared Geometry Must Cover Supported Saved Settings

Review after integrating main found a gap in the initial preparation design.
A saved sans or system setting changes the runtime profile, which correctly refuses the
default prepared markup.
Its replacement loses the measured boxes.
The original geometry probe could miss that loss by inspecting only surviving
reservations.

Prepare all four custom/system and serif/sans combinations.
Select matching fragments from the head bootstrap’s root attributes through CSS, before
paint. Deduplicate identical fragments and hydrate only the selected child, keeping
inactive copies out of layout and the accessibility tree.
A runtime-only replacement is insufficient because earlier layout may already have used
the wrong dimensions.

The guard must discover expected formulas and bases independently of their reservation
wrappers. Reject an entire missing reservation before discovery, as well as the existing
missing-width and wrong-width controls.
H-004 extends the default-only correctness matrix; the performance hypothesis still uses
its separately frozen rule.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
