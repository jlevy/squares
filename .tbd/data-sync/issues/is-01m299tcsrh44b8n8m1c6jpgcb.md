---
type: is
id: is-01m299tcsrh44b8n8m1c6jpgcb
title: "[epic] The workbench's JavaScript and CSS come under the standard floor"
kind: epic
status: open
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
child_order_hints:
  - is-01m299vb5st0sgwphga9w6zc3j
  - is-01m299vbk4aq0mkrjfxf7hyx4s
  - is-01m299vc0er1aeg7dzkrvvx90m
  - is-01m299vcddahjev9njwnhmcq9m
  - is-01m299vctfygccsbspy01xqj97
  - is-01m29bhr1chn5zb60pd7jfy01b
  - is-01m29bhrhcs1zrcbfbhgwbb86n
created_at: 2026-09-11T22:36:10.935Z
updated_at: 2026-09-11T23:08:51.049Z
---
Phase 6D made the page's script a file. This is what reads it.

The repository has a zero-findings floor for Python -- ruff and BasedPyright over every tracked file -- and nothing at all for the 5,079 lines of JavaScript the published page runs, or the 395 lines of CSS, or the 180 probe files the checkers drive it with. That asymmetry is the whole reason a TeX escape bug reached a rendered page.

The floor is not ours to invent: `tbd guidelines typescript-lint-format-rules` defines it, Profile B is the Biome instantiation, and /Users/levy/wrk/aisw/trading/biome.json is a worked example in a sibling repository. What it asks for:

1. Everything auto-formattable is auto-formatted; the formatter owns layout.
2. The lint gate is zero-tolerance and verify-only in CI: `biome ci --error-on-warnings`.
3. Type checking is a separate strict gate -- for JavaScript, `allowJs` + `checkJs` + `noEmit`.
4. Braces mandatory on every control statement (`style.useBlockStatements`, not in the recommended preset).
5. Recommended preset plus the named floor rules.
6. Hooks auto-fix at commit; the full verify gate runs at push and in CI.
7. Exceptions are narrow and file-scoped, never a global downgrade.
8. Legacy code ratchets toward strict and never loosens the default.

One consequence to state up front: **formatting the script changes the published page's bytes.** Every check so far has been byte-identity against a baseline. That baseline moves once, deliberately, here -- and what proves the page still works afterwards is the gate, not the hash.

Five chunks: J1 the toolchain, J2 the floor over the assets and probes, J3 the type gate, J4 the wiring, J5 the HTML.

## Notes

All five chunks landed, as c8e852ca (J1, J2) and c803f848 (J3, J4); J5 declined at this Biome pin with the measurement recorded on its bead.

The floor now: Biome 2.5.11 and TypeScript 7.0.2 pinned exact, zero errors and zero warnings over 191 files, three type programs at zero, a commit hook that fixes, a pull-request step that verifies, and a contract test that proves the floor is live rather than merely configured.

What it found along the way, which is the argument for having it:
- 'use strict' had been removed from four non-module files by c8e852ca, so the published workbench and both motion-lab pages were running sloppy. Restored, rule scoped off, assembled page regenerated.
- Biome renamed four cross-file functions in the motion lab as unused, which would have broken the page. Caught before commit; the rule is scoped off for assets that are concatenated rather than imported.
- Math.SQRT1_2 replaced 0.70711 where the literal was a rounded stand-in for an exact half-diagonal.
- blind_sweep collects two fields physics() never returns (think-2c3z).
- The API is now described twice with nothing keeping the two in step (think-gxxc).

What says none of it moved the page: check_workbench.py's output is byte-identical to the baseline taken before any of today's work.
