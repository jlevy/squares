---
type: is
id: is-01m5jr2d9y616b6b95kt3dpmry
title: "headroom.js root scroll-padding write: confirm the restyle on current browsers before changing it"
kind: bug
status: open
priority: 3
version: 3
assignee: null
delegate: claude-kind-mccarthy
labels: []
dependencies: []
parent_id: is-01m5jr2cr74kbbn71j05pqsgkd
hold: null
hold_until: null
created_at: 2026-10-22T21:25:29.022Z
updated_at: 2026-10-22T21:30:43.747Z
started_at: 2026-10-22T21:25:36.536Z
---
headroom.js sets root.style.scrollPaddingBlockStart on <html> after first layout on every page. Any change to the root's computed style makes Chromium restyle the whole document: ~350 ms on results and atlas, ~136 ms on the index (trace, UpdateLayoutTree after headroom measure). Tested alternatives that do NOT help: a <style> textContent rewrite, a CSSOM :root rule edit; an unrelated root inline property (outline-offset) costs the same. Fix: declare the expected padding in site-nav.css (61.19px at >=660px wide, 81.59px below) and write only when the measurement differs by more than 1px. Measured index->results click-to-settled ~1,240 -> ~800 ms.

## Notes

2026-10-22, deferred from the first PR. The ~350 ms whole-document restyle was measured only on Chromium 141 (the container's /opt/pw-browsers build). test_site_headroom.py::test_header_measurement_does_not_restyle_the_native_math_document, added in f5effa3dc with this very write, fails identically on main under Chromium 141 (9,073 elements restyled) and is expected to pass on the pinned Playwright 1.62 Chromium, so current Chrome probably does not pay this cost. A tested fix exists (CSS default under @media (scripting: enabled): 81.59375px, 61.1875px at width >= 40rem; headroom.js writes only when its measurement differs by more than 0.5px; a test that the static shell leaves root.style unwritten at 1280/768/390px). Re-measure on the pinned Chromium, Safari and Firefox; land the fix only if one of them reproduces the restyle.
