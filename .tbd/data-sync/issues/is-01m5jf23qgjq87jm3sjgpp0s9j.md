---
type: is
id: is-01m5jf23qgjq87jm3sjgpp0s9j
title: Apply consistent icons to GitHub document, issue, and pull-request links
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: upstream_integration
labels: []
dependencies: []
parent_id: is-01m5jct23n8s7fj3ydf94n0yhv
hold: null
hold_until: null
created_at: 2026-10-22T18:48:02.029Z
updated_at: 2026-10-22T19:05:38.193Z
started_at: 2026-10-22T18:48:17.286Z
---
Use shared typed icons across all website contexts for GitHub blob documents, issues and pull requests. Preserve meaningful link labels, avoid duplicate existing icons, cover dynamically loaded popovers, and follow design-system sizing/accessibility.

## Notes

Implemented shared GitHub link icons without changing link labels, hrefs, nested code/math or account-handle text. Repository/doc links use the existing canonical GitHub mark; issues use Lucide circle-dot and pull requests use Lucide git-pull-request, retained from upstream 1.17.0 (ISC). KPress's retained sprite has no GitHub brand glyph, so the existing Octicons mark (MIT) remains the brand source. SVG files under devtools/overview/icons supply both inline references and the CSS masks; inline accessibility/sizing attributes are injected with whitespace-aware matching.

Publication uses site_github_links.decorate_github_links at write_site (including drift comparison) and the papers' shared link_inline_assets boundary. Its HTMLParser reuses exact GitHub thread parsing and adds only a data attribute, preserving source markup and idempotency. Query strings containing /issues/7 and owners named issues/pull retain the generic mark. All five producers declare all seven shared icon inputs. CSS paints inherited-color first-line marks without JavaScript or wrappers, so fetched result/case/profile content receives the same treatment. Existing SVG/image/card marks are excluded. The record-links delimiter moved from the next link's ::before to the previous link's ::after, preserving it while freeing the first-line icon slot. Screen-only decoration preserves PDF pagination. Updated the GitHub Links design section and retained the documentation footer; Flowmark applied.

Final focused command: uv run --frozen --all-extras --group dev python -m pytest -q tests/test_github_references.py tests/test_site_github_links.py tests/test_site_popover_controls.py --maxfail=1 --tb=short -> 37 passed in 11.70s. Includes exact route/query/owner lookalikes, inline glyph attributes and canonical geometry, static/no-JS/mobile/multiline/math links, SVG/img/card duplicate avoidance, fetched result content and nine popover control checks. Log: /Volumes/spud-ext2/agent-scratch/about-profiles-20261020/github-links-focused-final.log.

Narrow floor: Ruff passes across changed Python; Biome passes five CSS/probe files; tsconfig.probes passes; focused BasedPyright reports 0 errors, 0 warnings, 0 notes. check_no_embedded_js --since origin/main reads 2791 files with zero allowlisted sites and none added. git diff --check passes. An unnecessary repo_links expansion was interrupted after 58 passed in 101.07s when its shared pages fixture began a redundant full render; this was not a test failure. Parent owns broad gates, final preview and review. Production source frozen, no commit or push. Keep open for coordinator integration acceptance; coordinator owns handoff sync under delegated-work rules.
