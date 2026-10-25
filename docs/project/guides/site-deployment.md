# Site Deployment

The Squares website is a static publication built by GitHub Actions and hosted on GitHub
Pages. Its canonical address is **https://squaremath.org/**. The source repository and
repository links in PDFs remain **https://github.com/jlevy/squares**.

**Deployment status (2026-10-22):** The domain is bound to GitHub Pages, its certificate
covers apex and `www`, and HTTPS enforcement is enabled.
HTTP upgrades to HTTPS and `www` redirects to the bare host.
The hosted audit passed all 5,459 checks; ordinary browser access and legacy
path/query/fragment redirects were verified.
Evidence is recorded in the
[domain migration plan](../specs/active/plan-2026-10-22-squaremath-domain.md).

## Ownership and Configuration

| Concern | Authoritative location |
| --- | --- |
| Source, reviews, and publication branch | `jlevy/squares`, branch `main` |
| Build, assembly, deployment, and live verification | [pages.yml](../../../.github/workflows/pages.yml), displayed as “Certificate page” |
| GitHub Pages hosting and domain binding | Repository Settings → Pages, source GitHub Actions |
| Domain ownership verification | Owner account Settings → Pages |
| Authoritative DNS | Registrar DNS for `squaremath.org`; currently Namecheap nameservers |
| Public website root | `SITE_URL` in [render_overview.py](../../../packing/devtools/render_overview.py) |
| Published paths and compatibility forwarders | [site-urls.yaml](../../../packing/site-urls.yaml) and [site_urls.py](../../../packing/devtools/site_urls.py) |
| Repository links | [repo_links.py](../../../packing/devtools/repo_links.py) |
| Publication design and metadata | [paper-design.md](../../../packing/devtools/templates/paper-design.md) |

DNS and GitHub settings are external state.
Inspect them before an operation; a source checkout cannot prove their current values.
Keep credentials out of source, build output, and deployment receipts.
Record the workflow run ID, deployed source revision, artifact identity, and verified
URL for a cutover.
The visible edition stamp identifies publication data, not necessarily
the deployment revision.

## Packaging and Build Flow

The Python build root is `packing/`, using the pinned Python version, `uv.lock`, and the
checked-out KPress submodule.
Browser tooling uses the root Node lockfile; workbench source lives under
`packages/workbench/`. Follow [development prerequisites](../../../development.md) and
`AGENTS.md` rather than introducing an independent deployment toolchain.

The workflow builds ordinary site pages, papers and their PDF editions, and the
workbench in parallel where dependencies allow.
The prepared historical explainer is shared by its PDF, typography, screen, geometry,
font-loading, and browser checks.
The publish job assembles the outputs into `packing/site`, checks the combined page
heads and shared assets, and uploads the Pages artifact on the publication branch.
The deploy job publishes that artifact; the verification job audits the resulting live
site.

The artifact includes HTML, downloadable Markdown and PDFs, hashed shared assets,
compatibility pages, sitemap output, and workbench code and data.
There is no runtime application server or database for this publication.
The browser loads static resources from the site.
Bulk media hosted as GitHub release assets retain their release URLs.

Use the workflow as the source of exact job dependencies, pinned actions, concurrency,
timeouts, artifact guards, and retention periods.
Do not deploy an independently rebuilt partial tree in place of its checked artifact.
See [Publishing the Explainer](../../../development.md#publishing-the-explainer) for PDF
reproducibility, source receipts, artifact handoff, and diagnostic retention.

## Local Preview and Validation

Use external scratch storage as required by `AGENTS.md`. Verify the volume is mounted
and writable; set `TMPDIR`, `UV_CACHE_DIR`, `CARGO_TARGET_DIR`, and pytest retention
before builds. Each worktree needs its own Cargo target.
Run commands from `packing/` with the project interpreter.
Set `SITE_PREVIEW_DIR` to a directory beneath the task’s external scratch root before
running the preview.

```bash
uv run --frozen --all-extras --group dev python -m devtools.preview_site --output "${SITE_PREVIEW_DIR:?Set SITE_PREVIEW_DIR under external scratch}" --serve
```

The preview builds the site, including the lower-bounds PDF, and runs its local metadata
and asset audit. It does not replace the workflow’s independent PDF, typography, and
browser gates. The default server address is `http://127.0.0.1:8765/`.

```bash
uv run --frozen --all-extras --group dev python -m devtools.check_published_site \
  --site http://127.0.0.1:8765/ --commit <built-commit> --deadline-minutes 25
```

The placeholder must be the revision used for the build.
Follow [Validation Loops](../../../development.md#validation-tiers) for edit, push, PR,
and checkpoint gates.
A local preview cannot validate public DNS, certificate issuance, or GitHub’s host
redirects.

## Routine Deployment

Merge reviewed publication changes into `main` and monitor the “Certificate page”
workflow. Its source filters determine whether an automatic build runs; declared
render-input tests guard those filters.
Inspect workflow dispatch inputs before using a manual run, since candidate infographic
runs intentionally retain outputs without deployment.

Deployment uses GitHub’s Pages artifact and deployment actions with the workflow’s Pages
and identity-token permissions.
Keep the repository configured for Actions publication.
Avoid adding a second deployment service or long-lived deployment credential unless the
hosting design changes.

Inspect the current configuration without changing it:

```bash
gh api repos/jlevy/squares/pages
gh run list --repo jlevy/squares --workflow pages.yml --limit 5
```

PR runs select content scopes from changed inputs and may skip whole-site assembly for
partial scope. Main and ordinary manual runs select all scopes.
The deployment requires both assembled output and the aggregate Pages gate.
A manual `gh workflow run pages.yml --ref main` can deploy; it is not a
verification-only operation.

The workflow grants read access by default and gives the deployment job `pages: write`
and `id-token: write` in the `github-pages` environment.
Most producer and diagnostic artifacts retain seven days; rendering measurements retain
thirty days. The final Pages artifact has no repository-specific retention override.
Download required evidence by run ID before rerunning.

Wait for the live verification job as well as deployment.
A failed post-deployment check does not automatically roll back publication.
From the checkout at the deployed revision, run:

```bash
uv run --frozen --all-extras --group dev python -m devtools.check_published_site \
  --site https://squaremath.org/ --commit <deployed-commit> --deadline-minutes 25
```

During the migration, use the actual configured production address.
The checker verifies publication identity, linked resources, repository targets, paper
receipts, and workbench behavior.
A completed deploy with a failed live audit is incomplete publication verification.
Retain the failure output, diagnose the response, and repeat verification rather than
assuming another deployment will fix it.

## Domain Cutover

The target is `https://squaremath.org/` with `www.squaremath.org` redirecting to it.
GitHub’s
[custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
and
[ownership verification instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
govern the provider steps.

1. Record the current Pages configuration, DNS records, and last healthy deployment.
   Prepare and review the source migration, including canonical metadata, profile URL
   recognition, and current changelog artifact links.
2. Add `squaremath.org` in the owner account’s Pages verification settings.
   Publish the exact TXT value GitHub supplies at
   `_github-pages-challenge-jlevy.squaremath.org`, then verify ownership.
   Keep this record after migration.
3. Coordinate publication with setting the repository’s custom domain to
   `squaremath.org`. Keep source set to GitHub Actions.
   GitHub instructs configuring the custom domain before routing DNS to Pages; this
   setting may affect the old host immediately, so proceed with DNS edits in the same
   attended cutover.
4. Replace parking or conflicting web-routing records with the table below.
   Preserve MX, mail-related TXT, the verification TXT, and unrelated service records.
   Do not add wildcard routing.
5. Wait for DNS checks and certificate provisioning, then confirm Enforce HTTPS is
   enabled. GitHub notes HTTPS availability can take up to 24 hours; record actual
   readiness instead of assuming it follows immediately from DNS resolution.
6. Run the checks below and record the deployed revision, workflow run, and observed
   redirects in the migration plan.
   Update this guide’s deployment status only after successful verification.

| Type | Name in Namecheap | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `jlevy.github.io` |

The CNAME is a hostname, without a scheme or `/squares` path.
IPv6 is optional; if configured, use all four current GitHub Pages AAAA addresses from
the provider instructions and remove incompatible old AAAA records.
Review any CAA restriction if certificate issuance fails.

A `CNAME` file in the artifact does not configure a custom Actions deployment.
The domain binding belongs in Pages settings.
Do not add client-side host redirects to every page: those pages are also served on the
canonical host.

### Acceptance checks

Check DNS from authoritative and public resolvers, then verify TLS without bypassing
certificate checks. Verify apex HTTPS, HTTP-to-HTTPS, www-to-apex, and old project-host
routing. Include the root, `news.html`, `profiles/index.html`, a deep profile, a paper
and PDF, workbench assets, and a results URL with a query string.
Confirm that an anchor still selects its heading in a browser.

```bash
dig +short squaremath.org A
dig +short www.squaremath.org CNAME
curl -IL https://squaremath.org/
curl -IL https://www.squaremath.org/news.html
curl -IL 'https://jlevy.github.io/squares/results.html?s=5'
```

Record the actual old-host response chain and final destination; it must preserve the
page and query rather than send all visitors to the homepage.
HTTP requests do not carry URL fragments, so use a browser for fragment checks.
Existing path forwarders must continue to work on the new host.
Run the full live publication audit against the deployed revision after these transport
checks.

## Recovery and Maintenance

For a content regression, revert the offending source change through the normal reviewed
workflow and publish a fresh checked artifact.
Do not assume a prior Actions artifact is still downloadable: retention and reruns can
make it unavailable.
Preserve diagnostic artifacts before rerunning failed jobs, as described in the
publication contract.

For a domain incident, inspect authoritative DNS, Pages domain state, and certificate
state separately. Restore accidental DNS changes from the recorded values without
touching mail. If returning publication to the original GitHub Pages URL is necessary,
coordinate removal of the custom-domain setting with restoring the matching public root
in source and deploying a checked artifact.
Domain rollback affects both canonical metadata and redirects; changing only DNS does
not restore the old hosting behavior.

Keep the domain ownership TXT record.
When retiring a hosting binding permanently, remove or repoint its DNS before abandoning
control of the hosted resource, following GitHub’s domain-takeover guidance.
Keep the registrar account and domain renewal under the owner’s control.

Changes to the host, public root, artifact layout, or deployment workflow require
updates to this guide and its linked source contracts.
Record migration-specific observations in the plan; retain routine deployment evidence
in GitHub workflow and deployment records.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
