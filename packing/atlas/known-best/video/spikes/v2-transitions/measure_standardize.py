"""How coarse the angle grouping has to be, and whether an open-ended run ever goes still.

Two questions the revision-10 colour model turns on, both measured against the page's own data
rather than guessed:

  --classes   how many angle classes the retained packings hold at a range of tolerances,
              and which angles two packings share. Too coarse and a frame is one colour;
              too fine and a settled physics run wraps the palette. Reads the atlas JSON
              out of the built page.
  --still     the greatest speed a square carries late in an open-ended run, per simulated
              second, which is what a "the picture has stopped" threshold has to sit
              above.

    packing/.venv/bin/python3 measure_standardize.py [--classes] [--still] [page.html]
"""

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent


def fold(angle: float) -> float:
    return ((angle % 90.0) + 90.0) % 90.0


def gap(a: float, b: float) -> float:
    d = abs(a - b)
    return min(d, 90.0 - d)


def classes(angles: list[float], tolerance: float) -> list[list[float]]:
    """The repository's own seeded greedy grouping (sqpack/render/color.py::_angle_classes)."""
    reps: list[float] = []
    groups: list[list[float]] = []
    for angle in (fold(a) for a in angles):
        hit = next((k for k, rep in enumerate(reps) if gap(angle, rep) <= tolerance), None)
        if hit is None:
            reps.append(angle)
            groups.append([angle])
        else:
            groups[hit].append(angle)
    return groups


def representative(members: list[float]) -> float:
    anchor = members[0]
    total = 0.0
    for value in members:
        offset = value - anchor
        if offset > 45.0:
            offset -= 90.0
        elif offset < -45.0:
            offset += 90.0
        total += offset
    return (anchor + total / len(members)) % 90.0


def slots(reps: list[float], tolerance: float, palette: int = 20) -> list[int]:
    """The revision-10 standardized map: slot 0 pinned to right angles, slot 1 to 45
    degree tilts, the rest by angle ascending from slot 2 up, wrapping over the palette."""
    pinned: list[int | None] = []
    for rep in reps:
        if gap(rep, 0.0) <= tolerance:
            pinned.append(0)
        elif gap(rep, 45.0) <= tolerance:
            pinned.append(1)
        else:
            pinned.append(None)
    rest = sorted((k for k, pin in enumerate(pinned) if pin is None), key=lambda k: reps[k])
    out = [0 if pin is None else pin for pin in pinned]
    span = max(1, palette - 2)
    for position, k in enumerate(rest):
        out[k] = 2 + position % span
    return out


def slot_of(frames: dict, n: int, angle: float, tolerance: float) -> int | None:
    groups = classes([s[2] for s in frames[str(n)]["squares"]], tolerance)
    reps = [representative(g) for g in groups]
    assigned = slots(reps, tolerance)
    for k, rep in enumerate(reps):
        if gap(rep, angle) <= tolerance:
            return assigned[k]
    return None


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not flags:
        flags = {"--classes", "--still"}
    page_path = (HERE / args[0]) if args else HERE / "workbench.html"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(f"file://{page_path}")
        page.wait_for_timeout(700)

        if "--classes" in flags:
            frames = json.loads(
                page.evaluate("document.getElementById('atlas-data').textContent")
            )["frames"]
            probes = [
                n for n in (5, 10, 11, 17, 26, 29, 100, 110, 272, 324) if str(n) in frames
            ]
            print("tolerance (deg) |" + "".join(f"{n:>7}" for n in probes))
            for tol in (0.0001, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0):
                counts = [
                    len(classes([s[2] for s in frames[str(n)]["squares"]], tol)) for n in probes
                ]
                print(f"{tol:>15.4f} |" + "".join(f"{c:>7}" for c in counts))
            tol = 0.5
            print()
            for n in probes:
                groups = classes([s[2] for s in frames[str(n)]["squares"]], tol)
                reps = sorted((representative(g), len(g)) for g in groups)
                shown = ", ".join(f"{r:.2f}deg x{k}" for r, k in reps[:12])
                print(f"n = {n:>3}: {len(groups):>3} classes at {tol} deg: {shown}")
            # Which non-trivial angles two retained packings actually share.
            table = {}
            for n in [int(k) for k in frames if k.isdigit()]:
                for group in classes([s[2] for s in frames[str(n)]["squares"]], tol):
                    table.setdefault(round(representative(group), 1), []).append(n)
            shared = {
                a: v
                for a, v in table.items()
                if len(v) > 1 and 0.6 < a < 89.4 and abs(a - 45) > 0.6
            }
            top = sorted(shared.items(), key=lambda kv: -len(kv[1]))[:8]
            print(
                "\nnon-pinned angles shared by several n (rounded to 0.1 deg),"
                " and the slot each takes:"
            )
            for angle, ns in top:
                slots = {n: slot_of(frames, n, angle, tol) for n in sorted(ns)[:8]}
                agree = len(set(slots.values())) == 1
                print(f"  {angle:>6.1f} deg in {len(ns)} packings: slots {slots}"
                      f" {'(agree)' if agree else '(DISAGREE)'}")

        if "--still" in flags:
            print(
                "\nlate motion in an open-ended run: the greatest square speed over a"
                " tenth of a"
            )
            print("simulated second, and the greatest turn over a whole one, which is what a")
            print("'the orientations have stopped' threshold has to sit above.")
            print(
                "   n  start   anneal  steps        max speed   mean speed   max turn/s (deg)"
            )
            for n in (17, 29, 100):
                for kind in ("grid", "random"):
                    for level in (0, 3, 10):
                        out = page.evaluate(
                            """([n, kind, level]) => {
                              const A = window.atlasTransitions;
                              A.setStepN(n); A.setAnneal(level); A.setInitial(kind);
                              A.optimizeStep(3600);
                              const before = A.optimizeState();
                              const poseOf = () =>
                                Array.from(document.querySelectorAll('#squares g'))
                                .filter(g => g.style.display !== 'none')
                                .map(g => g.getAttribute('transform'));
                              const a = poseOf();
                              A.optimizeStep(12);   // a tenth of a simulated second
                              const b = poseOf();
                              A.optimizeStep(108);  // out to a whole one
                              const c = poseOf();
                              const num = (s) =>
                                (s.match(/-?\\d+\\.?\\d*(e-?\\d+)?/g) || []).map(Number);
                              let max = 0, sum = 0, count = 0, turn = 0;
                              for (let i = 0; i < a.length; i++) {
                                const p = num(a[i]), q = num(b[i]), r = num(c[i]);
                                if (p.length < 2 || q.length < 2) continue;
                                const d = Math.hypot(q[0] - p[0], q[1] - p[1]) * 10;
                                if (d > max) max = d;
                                sum += d; count++;
                                if (p.length >= 3 && r.length >= 3) {
                                  const g = Math.abs(r[2] - p[2]) % 90;
                                  const f = Math.min(g, 90 - g);
                                  if (f > turn) turn = f;
                                }
                              }
                              return {steps: before.steps, max,
                                      mean: count ? sum / count : 0, turn};
                            }""",
                            [n, kind, level],
                        )
                        print(
                            f"{n:>5}  {kind:<7} {level:>5}  {out['steps']:>6}   "
                            f"{out['max']:>14.5f}   {out['mean']:>10.5f}   "
                            f"{out['turn']:>16.4f}"
                        )

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
