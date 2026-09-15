---
type: is
id: is-01m2hez16qm2y57ppeabmewzjr
title: "PR #160 review D90: publishing details: checkout credentials, Chromium download, no retry"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:40:01.239Z
updated_at: 2026-09-15T02:40:59.775Z
closed_at: 2026-09-15T02:40:59.774Z
close_reason: "Fixed on #160 at 2782c27e: frontend checkout persist-credentials false; verify-deployment installs --only-shell chromium to match its cache key; check_published_site retries transient answers with 2/4/8/16 s backoff and returns the last answer."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Publishing details: the new `frontend` checkout lacked `persist-credentials: false`; `verify-deployment` re-downloaded Chromium on every deploy; `check_published_site` fetched once with no retry.

Source: #160 R26 (non-inputs items). Related: think-9x0m.

Files: `.github/workflows/packing-validation.yml` (~`:396`); `.github/workflows/pages.yml` `verify-deployment`; `packing/devtools/check_published_site.py`.
