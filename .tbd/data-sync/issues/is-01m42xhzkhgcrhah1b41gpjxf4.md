---
type: is
id: is-01m42xhzkhgcrhah1b41gpjxf4
title: "kpress: host-generated assets in the asset manifest (phase 2)"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m42xfwp06kzm2b390dx1cw17
created_at: 2026-10-04T07:37:49.425Z
updated_at: 2026-10-04T07:37:49.425Z
---
Upstream the generic part of devtools/site_assets.py into kpress: AssetRef kind=generated with host bytes, content-hashed output paths for host CSS/JS/fonts, a CSS url rewriter that emits faces as hashed files, materialize for generated assets, public link/script/preload tag helpers, a depth-relative prefix, and inline_assets (put a linked page back whole). A stacked squares PR then bumps vendor/kpress and deletes the squares copy. Related: think-iy3l, think-mtov, think-vnph.
