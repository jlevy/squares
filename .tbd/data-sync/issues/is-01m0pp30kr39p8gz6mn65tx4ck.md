---
type: is
id: is-01m0pp30kr39p8gz6mn65tx4ck
title: Apply the formatting rules from common-doc-guidelines to README and SYNOPSIS
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pp24qsn326dyxy9na7wc50
created_at: 2026-08-23T06:49:20.248Z
updated_at: 2026-08-23T07:01:15.778Z
closed_at: 2026-08-23T07:01:15.778Z
close_reason: Verified flowmark does not normalise em-dash spacing, so these were real. Closed 71 spaced em dashes in SYNOPSIS, 14 in README, 21 in conventions.md, leaving the 9 table cells where an em dash is a not-applicable placeholder. Where an em dash was not the best punctuation it became a colon, comma or full stop rather than just tightening -- the references block was rewritten outright, since a citation followed by an em-dash gloss read badly closed up. H2 headings retitled to Title Case in README (What Has Gone Wrong Here, Exact Verification) and conventions.md (four). 'papers + web' now reads 'papers and web'. The one pedantic use of 'canonical', about a document, is gone; the technical uses (canonical basin identity) stay.
resolution: null
duplicate_of: null
---
Verified that flowmark does not normalise em-dash spacing, so these are real and fixable. (1) Spaced em dashes: 14 in README, 76 in SYNOPSIS. The guideline is American style, no spaces, and also 'use em dashes only when they are the best punctuation' -- so reduce the count where a comma, colon or full stop is better rather than only closing the spaces. (2) H2 headings must be Title Case: README has 'What has gone wrong here' and 'Exact verification'. (3) Write 'and', not '+', in prose: the layout tree says 'papers + web sources'. (4) common-doc-guidelines names calling a document 'canonical' as pedantry; SYNOPSIS uses it that way once, about the registry artifact. The other uses are the technical sense (canonical basin identity) and are fine.
