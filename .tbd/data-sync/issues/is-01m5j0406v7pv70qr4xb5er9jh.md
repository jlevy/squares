---
type: is
id: is-01m5j0406v7pv70qr4xb5er9jh
title: Review squaremath.org hosting options and domain migration
kind: task
status: closed
priority: 2
version: 4
delegate: domain-coordinator
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-22T14:26:55.322Z
updated_at: 2026-10-22T14:31:30.845Z
started_at: 2026-10-22T14:27:36.135Z
closed_at: 2026-10-22T14:31:30.843Z
close_reason: "Options review complete: recommend GitHub Pages custom domain; Render tradeoffs, Finterm comparison, DNS state and migration edit map recorded. Hosting choice and implementation remain a subsequent decision; no deployment changes made."
resolution: null
duplicate_of: null
---

## Notes

Reviewed hosting options on clean codex/squaremath-domain at main76496462b. Existing Pages is custom Actions publication with no custom domain. Live DNS: Namecheap NS, apex192.64.119.119, www parkingpage.namecheap.com; existing MX forwarding must remain. Recommendation: retain Pages for squaremath.org apex plus www redirect; preserves current seven-producer build/gates and artifact deployment. Render static sites are viable if explicit cache/security headers, HTTP redirect rules or hosted PR previews justify migration. Finterm render.yaml uses runtime static, Astro/Python/KPress, commit-triggered independent rebuild rather than CI artifact promotion. Migration requires SITE_URL, profile_links hardcoded host/path, validated changelog artifact destinations, live authored links and URL tests; regenerate site/PDFs/crawl files and verify legacy links/query/fragment preservation. Do not replace archived source evidence globally. Current official docs checked for both services: Pages custom workflow ignores CNAME file; verify domain TXT, configure repository before DNS, enable HTTPS. Render offers managed TLS and bandwidth/pipeline usage billing. No DNS or hosting settings changed; no source edits. Review reports from Sol inventories and independent Astra recommendation retained in conversation.
