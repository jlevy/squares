---
type: is
id: is-01m4f8yza6a07tq8cm0xcsgn3s
title: Fix no-JavaScript CSS test hang in current intake frontend
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
hold: null
hold_until: null
created_at: 2026-10-09T02:48:02.617Z
updated_at: 2026-10-09T03:00:43.754Z
started_at: 2026-10-09T02:48:46.858Z
---
Exact442 frontend run37873984207/job113638192725 timed out its unchanged900s site-table command with205collected,202reported(196PASS6skip),3remaining and noJUnit; frontendwall958s exceeds165 as consequence. Independent Astra pinnedPlaywright source identifies new noJS page.add_style_tag awaiting JavaScript style.onload/onerror promise with no timeout, which noJS context cannot execute. Sol bounded4parameter diagnostic underway; minimally replace only test stylesheet toggle with CDP CSS.createStyleSheet/setStyleSheetText/reset, retain noJS/print/completeMathML/AX/copy/visual assertions and all productioncontent/limits. Actual scopedcontrols, normal main integration, Astra review, exactcurrenthostedgates and owning442merge required.

## Notes

The disabled-script stylesheet test repair is committed on its owning PR #442 as fe498df7ca302e77f589bc7b5fcf92707514081b. Ordinary latest-main integration is 830cd91d903cf57b7177017aaa510011878827a5, with parent d43ea686d555efe3d866e88b960f60c9d2e0a7d1. Both normal hook invocations completed; final tree 683ecf06542edb74feb5280423e557b967408ad8 exactly matches independent Astra source acceptance. Only packing/tests/test_site_rendering.py changed; inspector stylesheet text replaces page.add_style_tag without enabling page scripts or altering production content. All 24 other module nodes, seven existing test assertions, parameter matrix, and semantic helper assertions remain unchanged.

The bounded original diagnostic passed 390px with JavaScript, then hung on 390px without JavaScript until the maintained runner terminated the group at 60 seconds. Pinned Playwright waits for disabled page-script style-load callbacks; source and real-child evidence are preserved. The corrected four Chromium parameters all passed, zero failures/errors/skips, JUnit 12.168 seconds; configured type checking and Ruff/format have zero findings. The preformat green source was reconstructed from formatter-only hunks and retained as exact Git blob 8eb7fd8779dbe2d396373d5f1bfcccdf2351dc3e; this is owner-verified evidence, not an independently reproduced Astra formatting bridge.

Maintained release pin update/check passes unchanged at e42d9d6da02b560842318c44fc127d68104f6d70; no empty pin commit. Git-selected source projection is 200904044 bytes under the unchanged 201326592 cap. Final immutable qualification is Git receipt f754eebd51437ba3c373519fc686ee45af6450b7, also review-notes/pr442-hpif-final-source-main-composition.json. ROOT owns publication, fresh exact-head hosted gates, upper cascade and merge. This bead stays open pending those current gates and the owning PR landing; local scoped results do not qualify a full or hosted gate.
