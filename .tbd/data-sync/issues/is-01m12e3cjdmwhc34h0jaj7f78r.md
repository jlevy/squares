---
type: is
id: is-01m12e3cjdmwhc34h0jaj7f78r
title: Make the commitment-to-phase join machine-checkable
kind: feature
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m127tej32njy532m2q642418
created_at: 2026-08-27T20:20:37.067Z
updated_at: 2026-08-28T01:36:56.392Z
closed_at: 2026-08-28T01:36:56.391Z
close_reason: Optional commitment and bead fields on a workflow phase, optional workflows list on a commitment, all populated for real. A cross-file schema $ref does not resolve for these loaders (measured, not assumed), so the workflow enum is duplicated and guarded by a check comparing the two lists. Both new checks verified to fire and pinned by negative controls.
resolution: null
duplicate_of: null
---
The layer where work actually happens has no structured link to the layer that planned it. Measured across 29 sessions and 171 phases:

  - workflow phases have no bead field and no commitment field
  - only 39 percent of phases name a BC id at all, and only 13 of 40 commitments ever appear in phase text
  - a session declares a single primary_bead, but 16 of 20 sessions that name beads in phase text name beads other than that one (session-029: primary think-kdil, phases also served think-1s0h, think-75ll, think-oyn9, think-uzmh)
  - the session-to-commitment link is recovered by regex over next_action prose in check_synopsis
  - agenda items have no workflow field; the intended W-sequence is prose inside the budget string, e.g. 'one 105-minute W3-W6-W2-W3 mini-cycle'

Two fields would close it: an optional workflows enum array on agenda items, and an optional bead (and/or commitment) field on workflow_phases.

Then packing-ledger check could verify that a session's phases actually served the commitments it claims, which is currently unverifiable. Same defect family as the guard failures: the model is sound but the joins are not machine-checkable, so drift is invisible.

Keep both fields optional so no terminal session record needs rewriting.
