"""TEMPORARY diagnostic: why WebKit reports embedded math faces as errors on CI.

Removed before the pull request. Prints one JSON object per repetition.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from devtools.check_math_loading import FIRST_PAINT_SCRIPT, HOLD_FONTS_SCRIPT, page_url
from devtools.render_explainer_pdf import PAGE, READY, SETTLED

#: Timestamp every face transition and record what the first visible formula was.
WATCH = r"""
(() => {
  globalThis.__faceLog = [];
  globalThis.__readyLog = [];
  const seen = new Map();
  const key = f => `${f.family}|${f.style}|${f.weight}|${f.unicodeRange}`;
  const tick = () => {
    for (const face of document.fonts) {
      const k = key(face);
      if (seen.get(k) !== face.status) {
        seen.set(k, face.status);
        globalThis.__faceLog.push({at: Math.round(performance.now()), face: k, status: face.status});
      }
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
  const timer = setInterval(tick, 5);
  setTimeout(() => clearInterval(timer), 20000);
  const wait = setInterval(() => {
    if (!globalThis.squaresMath) return;
    clearInterval(wait);
    globalThis.squaresMath.ready.then(
      r => globalThis.__readyLog.push({at: Math.round(performance.now()), result: r}),
      e => globalThis.__readyLog.push({at: Math.round(performance.now()), error: String(e)}));
  }, 1);
})();
"""

#: Record the first visible formula's identity, not only its text.
FIRST_NODE = FIRST_PAINT_SCRIPT.replace(
    "globalThis.__mathFirstPaint = { at: performance.now(), faces };",
    "globalThis.__mathFirstPaint = { at: performance.now(), faces,"
    " node: math.outerHTML.slice(0, 160),"
    " pendingAttr: document.documentElement.dataset.kpressMathPending ?? null,"
    " mathReady: document.documentElement.classList.contains('math-ready'),"
    " readyLog: [...(globalThis.__readyLog || [])] };",
)

PROBE = r"""async () => {
  const reloads = [];
  for (const face of document.fonts) {
    if (face.status !== 'error') continue;
    let outcome;
    try { await face.load(); outcome = 'resolved:' + face.status; }
    catch (error) { outcome = `${error.name}: ${error.message}`; }
    reloads.push({face: `${face.family} ${face.style} ${face.weight}`, outcome});
  }
  return {
    reloads,
    wait: (globalThis.kpressMathFaceWait || []).filter(e => e.outcome !== 'loaded')
      .map(e => ({request: String(e.request).slice(0, 90), outcome: e.outcome,
        detail: e.detail === undefined ? null : String(e.detail).slice(0, 200)})),
    readyLog: globalThis.__readyLog,
    faceLog: globalThis.__faceLog,
  };
}"""

#: Two identical faces, one `swap` and one `block`, loaded together. If WebKit's
#: `swap` face reports `error` while the `block` face reports `loading`, the status
#: is the zero-length block period, not a failed transfer.
FIXTURE = """<!doctype html><meta charset=utf-8>
<style>
@font-face { font-family: SwapFace; src: url("data:font/woff2;base64,%(font)s") format("woff2");
  font-display: swap; }
@font-face { font-family: BlockFace; src: url("data:font/woff2;base64,%(font)s") format("woff2");
  font-display: block; }
@font-face { font-family: AutoFace; src: url("data:font/woff2;base64,%(font)s") format("woff2"); }
</style>
<p style="font-family: SwapFace">swap</p>
<p style="font-family: BlockFace">block</p>
<p style="font-family: AutoFace">auto</p>
<script>
globalThis.__samples = [];
const record = () => {
  const row = {at: Math.round(performance.now())};
  for (const face of document.fonts) row[face.family] = face.status;
  globalThis.__samples.push(row);
};
record();
globalThis.__loads = [];
for (const face of document.fonts) {
  face.load().then(() => globalThis.__loads.push([face.family, 'resolved', Math.round(performance.now())]),
    e => globalThis.__loads.push([face.family, 'rejected: ' + e.name + ' ' + e.message, Math.round(performance.now())]));
}
record();
const t = setInterval(record, 4);
setTimeout(() => clearInterval(t), 3000);
</script>
"""


def host() -> dict[str, object]:
    meminfo: dict[str, str] = {}
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, _, value = line.partition(":")
            if key in {"MemTotal", "MemAvailable"}:
                meminfo[key] = value.strip()
    except OSError:
        pass
    return {"cpus": os.cpu_count(), "meminfo": meminfo, "loadavg": os.getloadavg()}


def fixture(browser_name: str) -> dict[str, object]:
    """Is `font-display: swap` alone enough to make WebKit report `error`?"""
    import re  # noqa: PLC0415

    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    html = PAGE.read_text(encoding="utf-8")
    match = re.search(r'url\("data:font/woff2;base64,([A-Za-z0-9+/=]+)"', html)
    assert match is not None
    font = match.group(1)
    with TemporaryDirectory(prefix="diag-fixture-") as temporary:
        path = Path(temporary) / "fixture.html"
        path.write_text(FIXTURE % {"font": font}, encoding="utf-8")
        with sync_playwright() as driver:
            browser = getattr(driver, browser_name).launch()
            try:
                page = browser.new_page()
                page.goto(path.resolve().as_uri(), wait_until="load")
                page.wait_for_timeout(1500)
                samples = page.evaluate("() => globalThis.__samples")
                seen: list[dict[str, object]] = []
                for row in samples:
                    if not seen or {k: v for k, v in row.items() if k != "at"} != {
                        k: v for k, v in seen[-1].items() if k != "at"
                    }:
                        seen.append(row)
                return {
                    "browser": browser_name,
                    "font_bytes": len(base64.b64decode(font)),
                    "transitions": seen,
                    "loads": page.evaluate("() => globalThis.__loads"),
                }
            finally:
                browser.close()


def one(browser_name: str, width: int, *, hold: bool, index: int) -> dict[str, object]:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        browser = getattr(driver, browser_name).launch()
        try:
            page = browser.new_page(viewport={"width": width, "height": 720})
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            if hold:
                page.add_init_script(HOLD_FONTS_SCRIPT)
            page.add_init_script(WATCH)
            page.add_init_script(FIRST_NODE)
            page.goto(page_url(PAGE), wait_until="domcontentloaded")
            page.wait_for_timeout(200)
            if hold:
                page.evaluate("globalThis.__mathLoadControl.release()")
            page.wait_for_selector(READY, timeout=60_000)
            page.evaluate(SETTLED)
            paint = page.evaluate("() => globalThis.__mathFirstPaint")
            probe = page.evaluate(PROBE)
            bad = (
                []
                if paint is None
                else [
                    f"{f['family']} {f['style']} {f['weight']} ({f['status']})"
                    for f in paint["faces"]
                    if f["status"] != "loaded"
                ]
            )
            return {
                "index": index,
                "browser": browser_name,
                "hold": hold,
                "first_paint_at": None if paint is None else paint["at"],
                "first_paint_node": None if paint is None else paint["node"],
                "pending_attr": None if paint is None else paint["pendingAttr"],
                "math_ready_at_paint": None if paint is None else paint["mathReady"],
                "ready_log_at_paint": None if paint is None else paint["readyLog"],
                "first_paint_bad": bad,
                "probe": probe,
                "page_errors": errors,
                "host_after": host(),
            }
        finally:
            browser.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", default="webkit")
    parser.add_argument("--width", type=int, default=390)
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--no-hold", action="store_true")
    parser.add_argument("--fixture", action="store_true")
    args = parser.parse_args(argv)
    print(json.dumps({"host_before": host()}))
    if args.fixture:
        print(json.dumps(fixture(args.browser), indent=1))
        return 0
    for index in range(args.repeat):
        result = one(args.browser, args.width, hold=not args.no_hold, index=index)
        print(json.dumps(result, indent=1))
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
