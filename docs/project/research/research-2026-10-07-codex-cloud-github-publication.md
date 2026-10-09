# Research: Publishing GitHub Work from Codex Cloud

**Date:** 2026-10-07 (last updated 2026-10-07)

**Author:** Codex (Sol engineering; Astra network and source review), for the squares
project

**Status:** Publication access repaired and verified by actual pushes and draft PRs.
CI and review remain pending; no merge is recorded.

**Tracking:** `think-wzdn`, under `think-mc4u`

## Overview

The owner explicitly chose **All repositories** for the existing Codex GitHub
installation. Fresh reads then showed the target repository as accessible, and the agent
pushed both prepared branches and opened the draft stack:

- [PR #415](https://github.com/jlevy/squares/pull/415): registration,
  `codex/import-squish-401` against `main`
- [PR #416](https://github.com/jlevy/squares/pull/416): confirmation,
  `codex/confirm-squish-401` against the registration branch

These writes verified the repair through the mediated GitHub route in this session.
The authenticated elevated direct probe still failed with TCP connection refused just
before the access change.
The successful writes do not establish direct egress or which raw credential the
intermediary forwarded.

The restored environment passes all five repository bootstrap checks.
Both original source heads remain unchanged, and independent standalone recovery
verified their histories and trees.
No new task or mathematical replay was needed to publish them.
The pre-repair failures below explain the access diagnosis and remain historical
evidence, rather than the current publication status.

## Questions to Answer

1. How do ordinary Codex Cloud users connect GitHub and open a PR?
2. Which GitHub connection, CLI authentication, and network controls are separate?
3. What do this session’s failures establish, and which repair can be attempted safely?
4. How can a new task recover the completed work without assuming workspace inheritance?

## Scope

This brief covers official OpenAI and GitHub documentation available on 7 October 2026,
this repository’s scoped GitHub CLI setup recipe, and actual publication responses for
`jlevy/squares`. It distinguishes current Codex Cloud from legacy GitHub review
workflows and the ChatGPT GitHub app.
It does not change credentials, network policy, TLS verification, repository remotes,
source geometry, or validation budgets.
The observed repair was the owner’s repository-access change, followed by successful
publication in this session.
Other credential-delivery experiments were not needed.

## Findings

### Normal Cloud Publication Uses a Coding Task

The [Codex Cloud overview][cloud] gives this sequence:

1. On web or desktop, choose **Work in > Cloud > Select environment > Create
   environment**, select the GitHub repositories, and connect GitHub if prompted.
2. Let Codex prepare and test the project.
   Review setup, save changes, select **Publish**, and wait for **Environment
   published**.
3. Select **Start a new task**, describe the coding work, then review its changes and
   test results and **commit or open a pull request** when ready.

For an existing published environment, select it and start the task directly.
[Current environment documentation][environments] says an environment is reusable setup
and each task has its own workspace.
It also says: “If the fix requires changing source files, a package manifest, or a
lockfile, make that change in a coding task, then return to setup.”
The documented workflow separates setup from coding tasks; it does not guarantee that PR
controls are exposed in this setup conversation.

New tasks start from the published prepared filesystem.
Existing tasks retain their own working state.
This does not establish which unpushed Git branches survive a particular task launch or
repository refresh. Recovery must verify the prepared branch refs and source trees
explicitly before any publication attempt.

### The ChatGPT GitHub App Is a Separate Read Route

The [ChatGPT GitHub help article][github-app] explicitly says its GitHub app only reads
repositories for analysis and search, and directs users to Codex to generate, edit, and
push code. Installing or reconnecting that read app is not a documented substitute for
Codex publication.

The article describes **Settings > Plugins > GitHub**, repository-management options,
and GitHub app installation and organization approval.
Those settings can repair missing repository access; seeing a repository through them
does not prove that an agent’s GitHub write channel is authorized.
The Codex Cloud setup flow separately prompts for its GitHub connection when choosing
repositories.

The [GitHub integration guide][github-review] describes code review on an existing PR
and `@codex`-triggered legacy cloud chats.
A fix can be pushed “when it has permission to do so.”
This is useful after publication; it is not evidence that a read-only connection can
bootstrap unpublished branches.

### Destination Policy and Credential Delivery Are Separate

[Current cloud settings][environments] document **Allow Codex to access internet** and
**Allow domains > All (unrestricted)**. They explicitly say allowing a destination does
not supply credentials or grant permissions in that service.
Unrestricted destinations therefore do not prove that raw TCP can bypass the managed
proxy.

| Setting | Documented delivery | Consequence |
| --- | --- | --- |
| Environment variable | Passed directly to programs | Appropriate when `gh` must read a credential itself |
| Network secret | Programs receive a placeholder; proxy substitutes the credential for allowed HTTPS destinations on port 443 | Supports service authentication through the proxy; use a different key from a direct variable |
| Personal vault | Only requested matching keys reach a task; environment-specific values take precedence over general defaults | A saved value alone does not establish that this task requested or received it |

The [GitHub CLI manual][gh-environment] documents `GH_TOKEN` precedence over
`GITHUB_TOKEN` and stored credentials.
The current setup records a direct `GH_TOKEN` variable and no network-secret entry.
The presence of that variable was checked without exposing its value.
Successful mediated identity reads do not prove which credential reaches GitHub after
proxy handling.

The docs support adding a distinct network secret with allowed domains such as
`api.github.com` and `github.com`. They do **not** document whether that substitution
overrides platform-injected GitHub authentication.
Such a change is a possible controlled experiment, not an established repair; it must
avoid reusing a direct variable’s key and must verify actual branch publication
afterward.

### Scoped Proxy Bypass Depends on Actual Direct Egress

The repository’s `setup-github-cli` shortcut and `.codex/ensure-gh-cli.sh` describe
scoped, additive `NO_PROXY` for GitHub hosts, preserving proxy settings elsewhere and
TLS verification. The recipe only applies when a bounded direct probe reaches GitHub.
It is a repository procedure for proxy-intercepted sessions, including Claude Code cloud
examples, not an OpenAI guarantee of direct egress from every Codex Cloud VM.

[Agent Security documentation][agent-security] says a permitted and approved full
sandbox escalation can bypass the managed command proxy on supported paths; cloud
environment internet settings still apply separately.
In this session, the documented authenticated direct `gh api --include user --jq .login`
probe failed with TCP connection refused in both ordinary and elevated execution.
A further bounded read with all HTTP, HTTPS, and ALL proxy variables unset also failed.
None reached GitHub HTTP authentication, so none diagnoses an invalid token.

### Pre-Repair Publication Responses Refused Writes

Before the repair, the agent made these actual write requests.
`gh` is pinned at version 2.97.0. Mediated reads identify `jlevy`, report repository
`viewerPermission: ADMIN`, and see remote `main` at the validated public base.
At that point, neither feature branch nor a PR was published.
Tool discovery in this setup session exposed no GitHub write MCP.

| Channel | Actual result | What it establishes |
| --- | --- | --- |
| Git push of both final feature branches | Exit 128, HTTP 403, permission denied | Git channel refused these branch writes before repair |
| GraphQL `createPullRequest` | Exit 1, “Resource not accessible by integration” | GraphQL PR channel refused creation before repair |
| REST `POST /repos/jlevy/squares/git/refs` | HTTP 403, same integration message; genuine GitHub request ID | Alternate branch-reference route refused the request before repair |
| REST `POST /repos/jlevy/squares/pulls` | HTTP 403, same integration message; genuine GitHub request ID | Alternate draft-PR route refused the request before repair |
| Authenticated direct API in ordinary and elevated execution | TCP connection refused | No supported direct route was demonstrated; authentication was not evaluated by GitHub |

The branch REST response lists accepted required permissions `contents=write` or
`contents=write,workflows=write`; the PR response lists `pull_requests=write`. GitHub
documents these in [permissions required for GitHub Apps][github-permissions]. These
headers describe endpoint requirements, not permissions actually granted to the
presented credential.
They do not prove that the owner’s configured token is invalid or missing a particular
permission. At that stage, an integration restriction, credential routing, or
platform-side authorization remained possible explanations.
Those failures justified changing effective access before repeating the requests.

### Pre-Repair Reads Excluded the Target

The `jlevy` installation of `chatgpt-codex-connector` declares contents, pull-request
and workflow write permissions and initially used selected repositories.
Two separately verified authenticated reads returned `total_count: 1` with no target
match by `jlevy/squares` or repository ID. GitHub describes this as the
[repositories accessible to the authenticated user for an installation][installation-access].
This is an accessible intersection, not the installation’s unconditional full inventory;
app write permissions do not prove target inclusion in the connection’s effective
access.

A supported `PUT /user/installations/{installation_id}/repositories/{repository_id}`
attempted to add only the target, using explicit current API version `2026-03-10`. It
returned HTTP 403, “Resource not accessible by integration,” with endpoint-required
permission `installation_repositories=write`. That header describes a requirement, not
an actual grant. Readback still excluded the target.
The agent-side attempt changed no repository selection.
The owner later explicitly chose All repositories in GitHub’s settings, as recorded
below.

After the owner opened the exact installation-settings page and requested another try, a
fresh proactive-authentication push still returned HTTP 403. A current-version, no-cache
read also excluded the target.
This does not establish that the owner failed to save, or that the actual installation
inventory omits the repo: an effective credential or connection view can differ.
This retry preceded the owner’s All repositories change and the verified publication
below.

The explicit environment-token test used the official GitHub CLI helper and
[Git 2.52 proactive Basic authentication][git-auth]; a marker verified credential GET
invocation without recording credential output.
This client-level route also returned HTTP 403. Token forwarding beyond the intermediary
and raw token validity remain unknown.

### Observed Access Repair and Publication

After the owner chose All repositories, a fresh `GET /user/installations` reported
installation `100851868` with `repository_selection: all`, updated at
`2026-10-07T19:03:48Z`. A paginated, no-cache read of that installation’s accessible
repositories returned `total_count: 157`, including `jlevy/squares`, repository
`1299872453`, with `push` and `admin` true.

The agent then used the official GitHub CLI credential helper with proactive Git Basic
authentication. The registration push at `6d0546b4c8949d9775d1a99865ec4e7277251cc7`
succeeded, and `gh` created draft PR #415 against `main`. The confirmation push at
`8f3c5484b9bade9cdf5c8fe332f2d5e6c2e016ac` succeeded, and `gh` created draft PR #416
against the registration branch.
Both PRs are linked in formal stack #417. Separate remote membership queries confirm
that stack for each PR, with the exact preserved heads and the expected branch bases.
The owner’s access change and the subsequent actual writes establish that the mediated
publication route works for this repository now.
They do not establish the intermediary’s credential-forwarding details.

## Options Considered

| Option | Support and observed result | Disposition |
| --- | --- | --- |
| Installation repository-access repair | Owner chose All repositories; fresh accessible-target read and actual pushes and PR creation succeeded | Completed; preserve the owner’s chosen selection |
| Existing mediated Git and `gh` | Both prepared branches and draft PRs published after repair | Use for this stack’s publication and review |
| Normal Codex coding-task publication | Official documented workflow | Available for future coding work; task switching was unnecessary for this repair |
| Distinct network-secret delivery | Documented substitution; precedence over injected authentication remains unknown | Experiment not needed |
| Scoped direct `NO_PROXY` | Ordinary and elevated probes failed before GitHub HTTP authentication | No working direct route demonstrated |

## Recommendations

Continue review and CI on PR #415 and PR #416 using the repaired connection.
Keep the registration and confirmation stages linked as a formal stack, and obtain merge
consent separately.
The owner’s All repositories selection is the current choice; another
selection change is unnecessary for this completed repair.

For a future access failure, compare the target’s effective installation access with an
actual bounded publication request.
Read permission or declared app write permission alone did not settle this session’s
diagnosis. Avoid inferring token invalidity from a connection refusal or an
integration-denied response.

### Recover the Completed Work Explicitly

The reported ref is `codex/import-squish-401` at
`6d0546b4c8949d9775d1a99865ec4e7277251cc7`; confirmation is `codex/confirm-squish-401`
at `8f3c5484b9bade9cdf5c8fe332f2d5e6c2e016ac`. Their prepared PR descriptions are
outside the checkout and must be transferred with the recovery artifact.
The receiving agent can run:

```bash
git bundle verify /path/to/squares-401-import.bundle
git fetch /path/to/squares-401-import.bundle \
  refs/heads/codex/import-squish-401:refs/heads/codex/import-squish-401 \
  refs/heads/codex/confirm-squish-401:refs/heads/codex/confirm-squish-401
git rev-parse codex/import-squish-401 codex/confirm-squish-401
```

The compact bundle needs public base `ef79288a498b5469e6b944f7b150d83aeeab5f94`, already
in the normal repository history.
A separate standalone source bundle contains complete history with no prerequisites and
was independently restored into an empty bare repository with `fsck` and both final
trees checked. Native tracker history has a separate verified standalone bundle.
These are preservation artifacts, not evidence of remote publication or permanent
platform retention. The current environment guide describes saved VM recovery for up to
seven days by default; important artifacts must be transferred or published rather than
relying on that window.

The retained artifact filenames are `squares-401-import.bundle` (compact source),
`squares-401-source-standalone.bundle` (complete source),
`squares-401-source-standalone-receipt.json` (independent recovery evidence), and
`squares-401-native-tracker-publication-retry.bundle` (complete tracker through the
publication retry).
The original research layer is paired with the complete source backup
using `squares-401-cloud-publication-research.bundle`; the research follow-up tracker is
separately retained in `squares-401-native-tracker-research.bundle`. These remain
external recovery files rather than large committed repository assets.

The access-diagnosis update is retained separately in
`squares-401-cloud-publication-research-access-fix.bundle`, paired with the same
complete source baseline.
Latest full tracker history is retained in
`squares-401-native-tracker-installation-access.bundle`; prior bundles remain intact.

Recovery is complete, with both original heads preserved and both draft PRs published in
verified formal stack #417. Attach review evidence, wait for CI, and obtain merge
consent separately. No mathematical replay is needed merely to move the same verified
source bytes to a supported publisher.

## Next Steps

- [x] Preserve source and tracker histories and descriptions; verify independent
  standalone source restoration and unchanged original branch heads.
- [x] Restore the environment and pass all five repository bootstrap checks.
- [x] Verify the owner’s All repositories selection and fresh accessible target
  membership.
- [x] Push both original branches and create draft PR #415 and draft PR #416.
- [x] Link both PRs as formal stack #417 and verify both remote memberships and bases.
- [ ] Finish review attachments and wait for hosted CI.
- [ ] Obtain merge consent before merging or publishing the main-based author reply.

## Methodology

Read official Cloud overview/current and legacy environment guides, the ChatGPT GitHub
help article, GitHub review documentation, Agent Security guidance, GitHub CLI
environment-variable precedence, GitHub REST permissions, the repository shortcut, and
its pinned CLI setup script.
Cross-check against actual bounded reads, supported direct probes, Git pushes, and
GraphQL/REST writes.
No secret values were printed.

Current cloud docs are linked from the legacy path
`developers.openai.com/codex/cloud/environments`; the guide at that old path now
describes legacy review and integration environments.
Product settings and feature availability can differ by plan, rollout, and workspace;
the brief records the published documentation and this session’s evidence rather than
promising a UI control it cannot operate.

Local operational evidence retained outside Git includes
`publication-retry-receipt.json`, `rest-publication-receipt.json`, and
`squares-401-source-standalone-receipt.json`. The REST reference request ID is
`41EC:F6480:873007:1B8426E:6AC66C0A`; the draft-PR request ID is
`2CBA:267852:B8D837:2575E57:6AC66C10`. No large source bundle or raw response corpus is
committed with this brief.

Follow-up evidence outside Git includes `installation-access-repair-receipt.json`, the
proactive helper invocation marker, and the owner-requested retry response.
The denied single-repository repair’s request ID is `F0E6:11AB04:D98FD:2C1DB2:6AC68FF7`.
No unrelated repository identities or raw credentials are retained in this brief.

## References

- [Codex Cloud overview][cloud] (official product workflow)
- [Current cloud environments][environments] (official setup, credentials, and
  saved-state guide)
- [Legacy cloud environments][legacy] (official legacy integration guide)
- [Connecting GitHub to ChatGPT][github-app] (official read-app scope and settings)
- [Review GitHub pull requests with Codex][github-review] (official review and
  legacy-task workflow)
- [Agent Security][agent-security] (official managed-execution and network boundaries)
- [GitHub CLI environment variables][gh-environment] (official authentication
  precedence)
- [GitHub App REST permissions][github-permissions] (official endpoint permission
  requirements)
- [Installation access APIs][installation-access] (official accessible-intersection and
  single-target repair contracts)
- [Git proactive authentication][git-auth] (official first-request authentication
  setting)
- Repository GitHub CLI shortcut (`tbd shortcut setup-github-cli`, read 2026-10-07)
- [Repository CLI setup script](../../../.codex/ensure-gh-cli.sh)

[cloud]: https://developers.openai.com/codex/cloud
[environments]: https://developers.openai.com/codex/environments/cloud-environments
[legacy]: https://developers.openai.com/codex/cloud/environments
[github-app]: https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt
[github-review]: https://developers.openai.com/codex/third-party/github
[agent-security]: https://learn.chatgpt.com/docs/enterprise/agent-security
[gh-environment]: https://cli.github.com/manual/gh_help_environment
[github-permissions]: https://docs.github.com/en/rest/authentication/permissions-required-for-github-apps
[installation-access]: https://docs.github.com/en/rest/apps/installations#add-a-repository-to-an-app-installation
[git-auth]: https://git-scm.com/docs/git-config#Documentation/git-config.txt-httpproactiveAuth

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
