---
type: is
id: is-01m3tdpv3xq6bcg89z9mdfvf57
title: "README and homepage intro: n = 11 is a central case, not the central case; one intro, shared by both"
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T00:26:55.995Z
updated_at: 2026-10-01T04:50:49.479Z
closed_at: 2026-10-01T04:50:49.478Z
close_reason: Done in ab7ae05e6, 15ef20b81 and c266798d9 on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. README's intro no longer calls n = 11 the central case and is one marked block the homepage renders (site_documents.intro_block); results.yaml rationales say 'a central open case' or 'a central case' (T-017, T-019, T-020, T-023, T-027 to T-031, T-018, T-037, T-060, T-061), no rating changed; a test forbids 'the/its central case'.
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: the README says n = 11 is 'the central case' of the Squares Project. That is not true and the project should not be framed that way: its purpose is to cover square packing at every n, going into depth at the values of n where there has been deeper recent progress. Rewrite the README intro without that framing (T-060 stays as a recent major result, stated within its rungs). The README intro is then reused properly as the intro of the site's overview page: one source, rendered on both, and the overview intro rewritten to be more focused and closer to the README's. Also remove 'the project's central case' from paper-design.md and render_overview's docstring. The significance rubric's S5 anchor ('movement on a central open case', epistemics.md) and the result rationales that call n = 11 the central open case are listed for the owner, not changed here.

## Notes

Owner correction, 2026-09-30: 'n = 11 is a central case, it is not the central case.' So prose may call n = 11 a central case but never the central case, and the project is not framed around it. The rubric's S5 anchor (a central open case) stays; the result rationales in results.yaml that say 'the central open case' change to 'a central open case' (wording only, no rating change), with RESULTS.md regenerated and DATA_REVISION re-pinned.
