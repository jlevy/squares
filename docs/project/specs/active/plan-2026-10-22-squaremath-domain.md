---
title: Square Math Domain and Deployment
description: Publish the existing static site at squaremath.org and retain legacy address compatibility
author: Codex, for the repository owner
---
# Feature: Square Math Domain and Deployment

**Date:** 2026-10-22

**Status:** Source migration merged in
[PR #727](https://github.com/jlevy/squares/pull/727). Domain ownership, DNS routing, the
apex Pages binding, and HTTPS enforcement are complete.
The hosted publication audit and local-browser DNS/fragment acceptance passed.

**Tracking:** `think-igk4` (epic), `think-m1j6` (documentation), `think-v4ab` (site
migration), `think-juq7` (production cutover).

## Overview

Publish the existing static website at `https://squaremath.org/` using its GitHub
Actions and GitHub Pages pipeline.
Configure `www.squaremath.org` as an alias and verify that the old
`https://jlevy.github.io/squares/` addresses reach the corresponding pages.
Preserve the repository identity and the `https://github.com/jlevy/squares` links used
in PDFs.

The ongoing operational reference is [Site Deployment](../../guides/site-deployment.md).
This plan owns migration tasks and acceptance evidence; the guide owns packaging,
deployment, DNS, verification, and recovery procedures.

## Goals

- Use the apex HTTPS domain in page metadata, social cards, sitemap entries, and
  generated public-site links.
- Retain page paths, query parameters, anchors, and existing path forwarders across the
  host migration.
- Preserve the checked artifact assembly and publication gates already used by Pages.
- Give maintainers a durable operational guide, with source links instead of copied
  workflow implementation.

## Non-Goals

Changing hosting providers, renaming repository or paper branding, rewriting archived
citations, changing repository links in PDFs, and changing mail service are outside this
migration.

## Background

The site is a static publication with generated HTML, Markdown, PDFs, browser code,
assets, and workbench data.
The existing workflow assembles and checks these outputs before deployment.
A custom domain does not require an application server or a new build platform.
Render remains an option if future requirements need configurable response headers or a
different preview system; it is not required for this domain change.

At planning time, Pages uses the Actions workflow with no custom domain.
The apex domain points to Namecheap parking, `www` points to its parking hostname, and
the domain has mail-forwarding MX records.
Confirm these observations immediately before cutover.

## Design

### Public addresses and repository addresses

The canonical website root is `https://squaremath.org/`. The repository root remains
`https://github.com/jlevy/squares`. Keep these concepts separate in code and
documentation. Do not perform a global URL substitution across historical documents or
PDFs.

Review `SITE_URL` in
[render_overview.py](../../../../packing/devtools/render_overview.py), its dependent
paper metadata, sitemap and 404 generation, and current authored website links.
Preserve relative internal navigation so the same artifact works in local previews.
Retain GitHub release URLs for externally hosted bulk assets.

[profile_links.py](../../../../packing/devtools/profile_links.py) independently
recognizes the old host and project prefix.
Update identity parsing and link auditing to recognize the new origin and explicit
legacy aliases without treating arbitrary external hosts as local profiles.
Test root-relative, relative, canonical absolute, and legacy absolute links.

[render_changelog.py](../../../../packing/devtools/render_changelog.py) validates live
artifact targets against the site root.
Reconcile current targets in
[site-changelog.yaml](../../../../packing/site-changelog.yaml) with the new root while
preserving historical source evidence.

### Hosting and redirects

Keep Pages configured with `build_type: workflow`. Set the repository custom domain
through Pages settings; a committed `CNAME` file does not configure a custom Actions
deployment. Verify domain ownership at the account level before changing routing.
Preserve the existing path forwarders within the published tree.

Treat the original project-host redirect as a live acceptance requirement: test both the
root and deep URLs after configuration.
Do not assume a successful apex request proves legacy compatibility.
Do not add unconditional browser redirects to pages that are also served on the
canonical host.

## Implementation Plan

### Phase 1: Prepare and validate the site

- [x] Choose GitHub Pages and the apex canonical domain.
- [x] Create the plan, deployment guide, and linked beads.
- [x] Update generated canonical URLs, current live links, profile URL recognition, and
  changelog targets (`think-v4ab`).
- [x] Add regressions for canonical and legacy URLs, rejected external hosts, and
  changelog validation.
- [x] Build the complete site, inspect local output, and run the required validation
  tier and PR checks.
- [x] Review the migration diff, including PDF repository-link preservation.

### Phase 2: Coordinate production cutover

- [x] Record current DNS, Pages configuration, and the last healthy deployment.
- [x] Complete GitHub account domain verification while retaining its TXT record.
- [x] Coordinate the reviewed deployment with custom-domain configuration and DNS
  changes (`think-juq7`).
- [x] Verify DNS, certificate provisioning, HTTPS enforcement, apex and www behavior,
  and old-host deep redirects.
- [x] Run the publication checker against the deployed commit and canonical domain.
- [x] Record deployment run, revision, redirect evidence, and any remaining follow-up in
  this spec; update the guide’s deployment status.

The source migration is one reviewable PR. DNS and repository settings are operational
changes tracked in the cutover bead; they are not represented by a Git diff.

## Testing Strategy

Exercise page-head metadata, sitemap and 404 generation, profile URL recognition,
changelog target validation, and the existing absolute-link checks.
Build the assembled artifact and use the existing local publication audit.
Check a deep profile, results filters, news, a paper HTML/PDF pair, assets, and the
workbench.

After deployment, run `devtools.check_published_site` from the deployed revision.
Separately test HTTPS and HTTP entry points for apex, www, and the old project host.
Record redirect status and destination, query retention, and browser anchor behavior.
The HTTP server cannot observe a fragment; anchor preservation needs a browser check.
A passing build alone does not establish successful DNS or redirects.

## Rollout and Recovery

Follow [Site Deployment](../../guides/site-deployment.md#domain-cutover).
The custom-domain setting can change old-host behavior before DNS and TLS are ready, so
coordinate these changes in an attended cutover.
Preserve mail and unrelated DNS records.
Use the guide’s recovery procedure if the site or deep links fail; do not delete
ownership verification as a shortcut.

## Cutover Evidence: 2026-10-22

PR #727 merged at `78dc902c19d814fa021432f66ed476b0fb1a4266` after senior reviews and 31
applicable checks passed.
The owner retained verification TXT and mail records and saved the four GitHub Pages A
records plus the `www` CNAME. Authoritative DNS and Google public DNS returned the
expected records.

GitHub approved a certificate covering both hosts, expiring 2027-01-20. Pages now
reports `https_enforced: true` and `https://squaremath.org/` as its public URL. Normal
TLS checks against the authoritative serving address succeeded: apex HTTP returns 301 to
HTTPS with the results query retained, and `www` HTTPS returns 301 to the bare host.
A deep profile returns 200. Some cached old-host responses still point first to HTTP;
the apex then upgrades them to HTTPS while retaining the path and query.

[Production workflow](https://github.com/jlevy/squares/actions/runs/39825552463) attempt
1 published before the certificate existed, so the HTTPS-only live audit correctly
refused its HTTP deployment URL. Attempt 2 repeated artifact assembly and produced two
`github-pages` artifacts, preventing deployment.
The original artifact was downloaded and verified before its duplicate was removed.
Attempt 3 redeployed successfully; its hosted audit passed all 5,459 checks at 18:39
UTC. The separate post-merge packing workflow passed.
Do not weaken the HTTPS audit or repeat artifact assembly merely to refresh an existing
deployment URL.

Ordinary local DNS access subsequently returned 200 over HTTPS. The built-in browser
followed `https://jlevy.github.io/squares/results.html?s=5#all-results` to
`https://squaremath.org/results.html?s=5#all-results`: the S5 filter displayed ten
results and the Browse Results heading landed below the navigation bar.
This verifies both query behavior and browser fragment retention.
The cutover monitor is disabled.

## Follow-up

The migration acceptance is complete.
Browser-install timeout hardening remains tracked separately in `think-fqhc`; it does
not block domain operation.
Future deployment changes follow the lasting guide rather than repeating the one-time
domain cutover.

## References

- [Publication workflow](../../../../.github/workflows/pages.yml)
- [Development and publication contracts](../../../../development.md#the-published-site)
- [GitHub custom-domain setup](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
