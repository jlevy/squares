---
type: is
id: is-01m24pamfvfh7z9k8j20qxr2rk
title: Write the StrategyPlan schema and Python executor
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-10T03:38:33.847Z
updated_at: 2026-09-10T03:52:55.662Z
---
Phase 1 of the strategy-plan spec. Write packing/schemas/strategy-plan.schema.yaml as a draft 2020-12 contract (packing.squares:StrategyPlan/v1) with oneOf on the stage's strategy field so each stage validates against its own parameters, and the structure-ladder rung as an enum: partition, contact-graph, contact-graph-with-types, with-wall-contacts.

Then devtools/strategy_plan.py: load, validate, execute, record a trace, emit a run record naming the plan, the rung, the side reached and the excess over the record. The strategy registry is the only place that knows how to run a stage -- that is the seam a Rust backend slots into later.

The four stages that exist today are assemble (devtools/known_structure.assemble_from_faces), project and ratchet (devtools/run_projection_ratchet), and relax (project with constraints released). solve() already has a trace hook and ratchet() already accepts start_from/start_side.

Not Pydantic: the repo already validates softschema contracts with jsonschema and ships jsonschema-rs for the Rust side, so a third convention would be a Python-first bias for a document whose point is being language-neutral.
