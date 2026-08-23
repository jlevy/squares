---
type: is
id: is-01m0pnjq24x1x9nnch6xn1s3yk
title: Decide whether the cell/instance-cell rule binds outside SYNOPSIS.md
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
created_at: 2026-08-23T06:40:26.179Z
updated_at: 2026-08-23T06:40:26.179Z
---
SYNOPSIS.md's Terminology section states: bare "cell" means a cell of configuration space; a position in the sweep is an "instance cell". conventions.md section 8 now points at that as binding on artifacts, beads and reviews.

But only SYNOPSIS.md was actually brought into line. Everything else -- campaign/README.md, the hypothesis artifacts, exp-001..010, defects.yaml, tools/controls.yaml -- still uses bare "cell" for the sweep sense, including in generated output ("a cell of the sweep whose answer is known in advance").

So conventions.md currently asserts a rule the directory mostly does not follow. Resolve it one way:

1. Apply the rule everywhere. Mechanical but touches dated round artifacts, which conventions section 6 says are corrected by annotation rather than rewriting -- so this may mean leaving rounds alone and fixing only living documents.
2. Or scope the rule to living documents explicitly, and say in conventions.md that dated artifacts predate it.

Option 2 is probably right and is cheap. Option 1 without thinking about section 6 would violate a different convention. Subsumed by think-8vhj if that is done first.
