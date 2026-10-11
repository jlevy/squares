---
type: is
id: is-01m4ma117y5ygnz88exhchnjp0
title: Synchronize polynomial PR stack and audit Git history size
kind: task
status: in_progress
priority: 1
version: 2
delegate: codex@spud10
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-11T01:42:50.877Z
updated_at: 2026-10-11T01:42:51.830Z
started_at: 2026-10-11T01:42:51.829Z
---
Use the upstream merge shortcut to synchronize the existing formal stack main → PR403 →
PR435 with freshly fetched origin/main, resolve textual and semantic conflicts, validate
and push the updated stack, and wait for CI. Audit final diffs plus every unique
branch-history blob and per-commit size; remove or rewrite any excessive generated/bulk
files so the PRs remain reviewable and Git stays manageable.
Preserve scientific data and certainty distinctions, all existing review/issue evidence
and the unrelated primary checkout.
The polynomial paper is strictly web-only; no PDF may be generated or published.
Root owns Git mutations, PR publication and this bead.
Three bounded parallel lanes cover Git storage, upstream semantic integration and PR/CI
administration. Scratch stays on the mounted external volume; use existing Python
3.14.7/runtime/cache, no new environments or internal fallback.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
