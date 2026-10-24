---
type: is
id: is-01m5ngnmstxk6xfzjsxfqsxez5
title: Name a gist's resource card by something other than its hex id
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5mr7439b7eqzqzccqrxnkxa
created_at: 2026-10-23T23:13:53.978Z
updated_at: 2026-10-23T23:13:53.978Z
---
PR #757 (c4301bb8a) gives Amund Kristiansen's gist its card in Other Square Packing Projects, the first gist in OTHER_PROJECTS (packing/devtools/site_resources.py). site_resources.resource_records titles a repository card by the last path segment of its address, so the card's heading is '78f9f0e7b4669f2f509a281845081768', and overview_sections.project_name gives the Project filter 'amundsk/78f9f0e7b4669f2f509a281845081768' (slug amundsk-78f9f0e7b4669f2f509a281845081768). Both are correct and unique, but a reader sees a hex id. Options: a curated title for a gist (its main file, s303_amund.cert, or 'amundsk gist'), or a title column in OTHER_PROJECTS. This is card data, but it changes what the Resources page and the results page's Project control show, so the site owner should choose. Found by c-fix-757-1023 on 2026-10-23; not done in #757 because the lane's scope was the card's presence and its tests.
