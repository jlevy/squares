---
type: is
id: is-01m23kzyzcgy2618y4g80fet03
title: Make the font-loading browser install survive a bad upstream apt repository
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T17:38:32.556Z
updated_at: 2026-09-09T17:38:32.556Z
---
The two `font-loading` jobs of the Certificate page workflow failed on `1950968b`
(run 34383162197, attempts 2, 3 and 4, 17:34-17:37Z on 2026-09-09) and the cause is
entirely outside this repository.

Playwright's browser install runs with `--with-deps`, which runs `apt-get update` on a
runner whose sources include Google's Chrome repository. That repository was serving a
`Release` file created at 17:16:59Z against a `dists/stable/main/binary-amd64/Packages.gz`
still reporting a 09:41:12Z modification, so apt refused it:

    E: Failed to fetch https://dl.google.com/linux/chrome-stable/deb/dists/stable/main/binary-amd64/Packages.gz  Hash Sum mismatch
    Failed to install browsers
    Error: Installation process exited with code: 100

The expected and received SHA-256 pair was byte-identical across all three attempts, which
is the signature of a stale CDN object rather than anything that varies per run. The job
fails before any repository code executes.

Not caused by the branch: the parent commit `0443a193` passed both jobs at 16:37Z, and
`codex/n11-independent-owner-audit` passed the same workflow at 17:00Z -- both before
Google published the mismatching Release at 17:16:59Z. The commits under test (`0e05bbd4`,
`1950968b`) touch only Markdown and YAML records.

The project-side question is that this workflow has no defence against it. Options,
cheapest first: install browsers without `--with-deps`, since the ubuntu-latest runner
image may already carry the system libraries firefox and webkit need; or drop Google's list
file before the install (`sudo rm -f /etc/apt/sources.list.d/google-chrome.list`), since
neither browser under test needs it; or retry the install step. The first two remove the
dependency rather than paper over it, which is the shape this repository prefers.

Done when a transient inconsistency in a third-party apt repository this project does not
use cannot fail the font-loading jobs, with the reason recorded where the workflow declares
the install.
