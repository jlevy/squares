---
type: is
id: is-01m0n8jwjv8a08tzaj6y0fk7dv
title: Install flowmark as an agent skill in this repo
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n8jv4yts3mwdptj15b4gar
created_at: 2026-08-22T17:34:05.914Z
updated_at: 2026-08-22T17:39:00.428Z
closed_at: 2026-08-22T17:39:00.427Z
close_reason: Installed via flowmark's own --install-skill, writing .agents/skills/flowmark, .claude/skills/flowmark, and an AGENTS.md block -- the same convention tbd and softschema use.
---
Set up flowmark as a skill so agents discover it: prefer the tool's own installer if it has one (as tbd and softschema do); otherwise write a SKILL.md to the portable .agents/skills/ location and the .claude/skills/ mirror, matching the existing convention.
