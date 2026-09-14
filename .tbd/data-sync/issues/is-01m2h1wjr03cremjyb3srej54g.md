---
type: is
id: is-01m2h1wjr03cremjyb3srej54g
title: Roll only the numeral in the stage headline, holding n = still
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T22:51:29.406Z
updated_at: 2026-09-14T22:51:29.406Z
---
Owner report 2026-09-14: the headline under the stage slides and fades the whole expression 'n = <value>' between steps; only the number should move, with 'n =' fixed. Cause: facts.ts buildFacts puts the whole KaTeX html_headline ('n = 11' as one expression) into each fading numeral layer, and application.js render() fades numeral-slot-a/b and translates numeralA/B, so 'n =' rolls with the value. The CSS and measureHeadline comments still describe the earlier design where 'n =' lived outside the layers. Fix: render 'n =' once, static, and roll only the value; keep the centring on the widest value.
