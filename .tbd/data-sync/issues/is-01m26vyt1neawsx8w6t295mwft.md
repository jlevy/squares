---
type: is
id: is-01m26vyt1neawsx8w6t295mwft
title: A JavaScript mechanism registry, and a conformance check against Python
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-10T23:55:26.644Z
updated_at: 2026-09-10T23:55:26.644Z
---
GitHub Pages serves static files and runs no backend, so a hosted workbench that lets a visitor change a setting and see what happens must execute the mechanisms in the browser. The v2 prototype already does -- optimizeStep, annealState and the force law are JavaScript in template.html -- so nothing needs inventing, but it means two implementations of the same mechanisms in two languages, and they will drift.

That is what the shared contract is for. Build a JavaScript mechanism registry mirroring MECHANISMS in devtools/packing_strategy.py, reading the same packing-strategy.schema.yaml, so the hosted workbench executes strategy documents rather than its own hard-coded modes.

Then a conformance check: run one strategy document through both implementations and compare the two PackingAnimation outputs within a declared tolerance. Without it, two implementations of 'the physics' is a liability; with it, it is a testable agreement. It is also the test that keeps a Rust backend honest later, for the same reason -- a mechanism is a different implementation of the same phase, selected by a field.

Note the asymmetry that makes this tractable: only the hosted workbench runs mechanisms. The embedded animation and the video both replay a finished PackingAnimation with no mechanism executed, so a drift in the JS implementation cannot corrupt either of those outputs.
