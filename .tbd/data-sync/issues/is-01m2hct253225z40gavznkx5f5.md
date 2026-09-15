---
type: is
id: is-01m2hct253225z40gavznkx5f5
title: "PR #125 review D76: tooling and count drift (.npmrc, Makefile, lefthook, TUTORIAL, README)"
kind: bug
status: closed
priority: 3
version: 4
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:21.218Z
updated_at: 2026-09-15T02:13:11.564Z
closed_at: 2026-09-15T02:13:11.563Z
close_reason: "Fixed in 4b930870: .npmrc names make hooks-install, obsolete Makefile paragraph removed, lefthook.yml install line corrected, TUTORIAL says twenty-eight strategies, README's unchecked report counts dropped (check_readme pins the remaining one)."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F39 (Low); triage row D76. The Biome hook glob item is fixed in #160 at f9099096.

Tooling and count drift: .npmrc:7 says `npm run prepare` installs the hooks but package.json has no prepare script; Makefile :26-35 keeps the obsolete npx lefthook@2.1.10 paragraph above the hooks-install text; lefthook.yml:2 still says `npx lefthook install`; TUTORIAL.md:1129 "Twenty search strategies" (28); README.md :263 and :644 give eleven and twelve research reports (the count changed again with the main merge).
