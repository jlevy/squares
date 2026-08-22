---
type: is
id: is-01m0n8jvsq901ha5ms18vnm8p6
title: Supply-chain check before installing flowmark
kind: task
status: closed
priority: 0
version: 3
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
assignee: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m0n8jv4yts3mwdptj15b4gar
created_at: 2026-08-22T17:34:05.110Z
updated_at: 2026-08-22T17:35:11.927Z
closed_at: 2026-08-22T17:35:11.927Z
close_reason: "Clears the policy with no exception needed: crates.io owner is jlevy (Joshua Levy), same as this repo's owner; version 0.3.2 is not yanked; checksum e5a811a023ce3ff63a767e6e43efdc52ecf17892d73e24c8a31880f84c598e50; published 2026-07-15, i.e. 37 days old against a 14-day cool-off."
---
Verify publisher identity matches jlevy, check provenance/attestation and integrity hash, and compute the version's age against the 14-day cool-off in guidelines/supply-chain-hardening.md. If inside the window, do NOT self-approve: prepare the exception record and ask the user to sign off.
