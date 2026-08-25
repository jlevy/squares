---
type: is
id: is-01m0vhjwpg55jj6jt0g96qpr87
title: Standardize campaign, session, workflow phase, experiment, round, and run
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - terminology
dependencies:
  - type: blocks
    target: is-01m0v06qf4hksmdqc2rga0vr4x
parent_id: is-01m0typjn7s866m042zsemybj6
created_at: 2026-08-25T04:06:49.790Z
updated_at: 2026-08-25T04:06:59.707Z
---
Audit the packing documentation, schemas, generated views, campaign artifacts, and agent entry instructions against one work-unit vocabulary: a campaign is the durable multi-session scientific effort; a series is its tooling and comparability boundary; an agent session is one bounded interval of orchestrated work; a workflow phase is one contiguous focus inside a session; an experiment is the durable artifact for one preregistered round; a round is the bounded research work recorded by that experiment; and a run is one invocation or trial. Make SYNOPSIS the authoritative definition, keep README compact, require orchestrators to declare phase switches, and remove conflicting uses without rewriting source-faithful archives.
