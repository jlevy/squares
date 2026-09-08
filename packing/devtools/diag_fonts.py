"""TEMPORARY diagnostic: why WebKit reports embedded math faces as errors on CI.

Removed before the pull request. Prints one JSON object per repetition.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from devtools.check_math_loading import FIRST_PAINT_SCRIPT, HOLD_FONTS_SCRIPT, page_url
from devtools.render_explainer_pdf import PAGE, READY, SETTLED

PROBE = r"""async () => {
  const faces = [...document.fonts].map(face => ({
    family: face.family, style: face.style, weight: face.weight, status: face.status
  }));
  const wait = (globalThis.kpressMathFaceWait || []).map(entry => ({
    request: String(entry.request).slice(0, 120), outcome: entry.outcome,
    detail: entry.detail === undefined ? null : String(entry.detail).slice(0, 300)
  }));
  const reloads = [];
  for (const face of document.fonts) {
    if (face.status !== 'error') continue;
    let outcome;
    try { await face.load(); outcome = 'resolved:' + face.status; }
    catch (error) { outcome = `${error.name}: ${error.message}`; }
    reloads.push({face: `${face.family} ${face.style} ${face.weight}`, outcome});
  }
  return {
    faces, wait, reloads, setStatus: document.fonts.status,
    ready_at: performance.now(),
    nav: performance.getEntriesByType('navigation').map(e => ({
      domContentLoaded: e.domContentLoadedEventEnd, load: e.loadEventEnd
    })),
    hardware: {cores: navigator.hardwareConcurrency, memory: navigator.deviceMemory ?? null},
  };
}"""


def host() -> dict[str, object]:
    meminfo: dict[str, str] = {}
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, _, value = line.partition(":")
            if key in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}:
                meminfo[key] = value.strip()
    except OSError:
        pass
    return {"cpus": os.cpu_count(), "meminfo": meminfo, "loadavg": os.getloadavg()}


def one(browser_name: str, width: int, *, hold: bool, index: int) -> dict[str, object]:
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as driver:
        browser = getattr(driver, browser_name).launch()
        try:
            page = browser.new_page(viewport={"width": width, "height": 720})
            errors: list[str] = []
            console: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on(
                "console",
                lambda message: console.append(f"{message.type}: {message.text}"[:300]),
            )
            if hold:
                page.add_init_script(HOLD_FONTS_SCRIPT)
            page.add_init_script(FIRST_PAINT_SCRIPT)
            page.goto(page_url(PAGE), wait_until="domcontentloaded")
            page.wait_for_timeout(200)
            if hold:
                page.evaluate("globalThis.__mathLoadControl.release()")
            page.wait_for_selector(READY, timeout=60_000)
            page.evaluate(SETTLED)
            paint = page.evaluate("() => globalThis.__mathFirstPaint")
            probe = page.evaluate(PROBE)
            readout = page.evaluate(
                "() => { const el = document.getElementById('kval-19-5');"
                " return el ? [el.innerText, el.textContent.length, el.children.length] : null; }"
            )
            return {
                "index": index,
                "browser": browser_name,
                "hold": hold,
                "first_paint_at": None if paint is None else paint["at"],
                "first_paint_bad": []
                if paint is None
                else [
                    f"{f['family']} {f['style']} {f['weight']} ({f['status']})"
                    for f in paint["faces"]
                    if f["status"] != "loaded"
                ],
                "probe": probe,
                "kval": readout,
                "page_errors": errors,
                "console": console[-20:],
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
    args = parser.parse_args(argv)
    print(json.dumps({"host_before": host()}))
    print(json.dumps({"page_bytes": PAGE.stat().st_size}))
    try:
        free = subprocess.run(["free", "-m"], capture_output=True, text=True, check=False)
        print(json.dumps({"free": free.stdout}))
    except OSError:
        pass
    for index in range(args.repeat):
        result = one(args.browser, args.width, hold=not args.no_hold, index=index)
        print(json.dumps(result, indent=1))
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
