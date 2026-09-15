---
type: is
id: is-01m2heyxjmw1jnjrwzpmdr19z3
title: "PR #160 review D56: the self-contained check misses SVG and script requests, and there is no CSP"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:57.523Z
updated_at: 2026-09-15T03:02:13.474Z
closed_at: 2026-09-15T02:40:56.930Z
close_reason: "Fixed on #160 at 269fefcc: SVG image/use/feImage href, script-built url( and script request calls are refused (fixtures as HTML files); build_site puts a default-src 'none' CSP first in <head>; check_frontend passes on the policy-carrying page. 'unsafe-eval' is granted for the checkers' string predicates until think-xvjf."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

The self-contained check missed SVG `<image>`/`<use>`/`<feImage>` `href`, script-built `url(`, `fetch(`/`import(`/workers, and the page had no CSP. `<img>`/`<iframe>` were fixed at 15d97a59.

Sources: #125 F21; #160 R22 (script-text item). Related: think-yz20.

Files: `packages/workbench/tools/workbench_tools/self_contained.py:8-75`; `build_site.py:239-242`; `packages/workbench/tests/test_self_contained.py`.

## Notes

2026-09-14 follow-up d4891db4: 'unsafe-eval' removed from the published policy; check_pack_panel bypasses the CSP for its one expression-string predicate, and check_page_policy (run by check_frontend) loads the page without bypass with an init-probe violation recorder and a live-recorder control.
