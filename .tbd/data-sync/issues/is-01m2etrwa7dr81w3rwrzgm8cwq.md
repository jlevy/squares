---
type: is
id: is-01m2etrwa7dr81w3rwrzgm8cwq
title: "Owner decision: land the n11 stack before any BC329 or exp-158 scientific result"
kind: task
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - decision
  - landing
dependencies: []
parent_id: is-01m2etr75jfh3t3ry7kj1ccqrb
created_at: 2026-09-14T02:08:39.238Z
updated_at: 2026-09-14T02:26:55.021Z
closed_at: 2026-09-14T02:26:42.833Z
close_reason: "Owner decision, 2026-09-14 (~02:35 UTC, Claude Code session on claude/n11-stack-ci-stabilization): land all the machinery now and be explicit about its limitations and what the scientific results are. Heavy computer-assisted proof efforts for very small improvements are on hold; the program pivots to a holistic strategy for significant n=11 improvements or a significantly simpler proof of s(11) >= 3.82. PR descriptions must state: established bound unchanged at T-026 s(11) >= 3.8264474; H-159 and H-161 are scoped negatives; BC329, exp-158 and H-162 are unexecuted instruments/registrations."
resolution: null
duplicate_of: null
---
Owner decision required: may #156 and the #161–#166 chain merge to main before any scientific run (the three BC329 calibration profiles, the BC329 target, or the H-160/exp-158 C/S charge target)?

What would land: the BC329 runner, source-distinct reader, run-set verifier and calibration producer (never run on a full-shape profile); two scoped negatives (H-159 at one local parent, H-161 literal parent union); the target-free C/S reader and H-160/exp-158 registration; X-030/X-031 strategy drafts. No bound changes; T-026 `s(11) >= 3.8264474` remains the established result.

For: OR-6 ("Instrument readiness is pipeline progress, not a mathematical result"; "Checkpoints may close before this chain is complete") and OR-9 (explicit no-result statement, present in every PR body) permit it; the negatives are finished results; the BC329 wait is open-ended while the stack keeps growing (#167) and needs back-merges at every change.

Against: the #156 review comment (issuecomment-5657094528, 2026-09-13T23:39Z) recommended keeping #156 draft, citing BC329 operational admission rather than merge policy; #156 was marked ready at 00:44Z by the jlevy account, so no owner decision is recorded. main would carry runner tooling never exercised end to end; the published SYNOPSIS would show the prospective S_c ≈ 3.826721 (labelled conditional); no PR has a formal review; CI time grows for unexercised code.

Coupling: yes enables calibrating on main (think-zwlf, option B); no forces calibration on an open PR head first.

Record the decision, who made it, and when, as a note here and a comment on #156, then close.
