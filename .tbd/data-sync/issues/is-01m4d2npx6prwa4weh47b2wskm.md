---
type: is
id: is-01m4d2npx6prwa4weh47b2wskm
title: A7 Retain homepage fragment destinations for registered withdrawn results
kind: bug
status: open
priority: 1
version: 1
assignee: codex
delegate: moderate-site
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
created_at: 2026-10-08T06:19:38.789Z
updated_at: 2026-10-08T06:19:38.789Z
---
Independent Astra review found that the known-only homepage result-fragment guard excludes withdrawn T-117 and T-118 although their permanent URL registry tombstones are retained. Derive exact retired aliases from the registry and route those old homepage fragments, including encoded forms and actual link clicks, to the explanatory tombstones. Keep live-result query filtering and unknown-ID refusal, with no numeric-range guesses or primary content fetch.
