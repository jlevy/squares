"""Grade a physics configuration on both halves of what it is asked to do.

    packing/.venv/bin/python3 grade_motion.py [workbench.html] [--style physics] [--anneal 3]
    packing/.venv/bin/python3 grade_motion.py --compare      # every style at every anneal level

**Neither half alone is the answer, and that is the whole design.** A run graded only on where it
ends up can thrash across the stage and still score well, because the lock-in carries whatever is
left; one graded only on the journey can glide smoothly to somewhere wrong. A configuration is good
when a viewer can follow the motion AND the run arrives, so this reports the two separately, never
collapses one into the other, and combines them only at the end with the weights written down.

**Outcome** -- did it get there, at the instant the lock-in takes over, which is the last frame the
physics owns:

  residual    the worst square's distance from its place in the record, in unit sides
  turn        the worst square's angle from its place in the record, in degrees
  mean        the same distance averaged over the squares, which says whether one square is out
              or the whole arrangement is

**Motion** -- was the journey one a viewer can follow:

  wander      the worst distance a square strays from the straight line between where it starts and
              where it ends. This is the measure that matters and it took two tries to find: distance
              from the final pose confuses travel with thrashing, since a square that legitimately
              moves 1.2 sides reads 1.2 at the start of its move
  jerk        the worst single-frame displacement, in sides -- a jump, as against a glide
  overlap     the deepest penetration of one square into another through the move, which is the
              physics failing rather than looking bad

The grade is `1 / (1 + sum(weight * value))` over both families, so it runs 0 to 1 with 1 perfect,
and the components are printed beside it. The weights are a statement about what matters, not a
measurement, and they are here to be argued with: a unit side of residual and a unit side of wander
are counted the same, a degree of turn as a fiftieth of a side, and a unit side of overlap as five,
because squares passing through each other is a different kind of wrong from squares taking a long
way round.
"""

import argparse
import json
import statistics
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
PACKING = HERE.parents[4]
DEFAULT_PAGE = PACKING / "site/workbench/index.html"

#: The n sampled by default: a spread of sizes and of rearrangement kinds, every one a matched step
#: (a static append has no motion to grade). Small enough to run while someone waits.
DEFAULT_SIZES = (11, 17, 26, 29, 37, 110, 180, 307)

#: What a unit of each measure costs the grade. See the module docstring: this is a statement about
#: what matters rather than something measured, and the components are always printed beside the
#: grade so a reader can disagree with the weights without losing the numbers.
WEIGHTS = {
    "residual": 1.0,
    "mean": 1.0,
    "turn": 0.02,
    "wander": 1.0,
    "jerk": 2.0,
    "overlap": 5.0,
}

#: Where the lock-in takes over, as a fraction of the move: `1 - PHYS.blend`. The outcome is read
#: here rather than at the end, because after this the blend is carrying the squares and what it
#: carries them from is exactly what is being graded.
LOCK_IN_AT = 0.88

MEASURE = """(args) => {
  const api = window.atlasTransitions;
  const d = api.duration(), sc = api.schedule();
  const read = () => { const o = []; for (let i = 0; ; i++) { const q = api.poseOf(i); if (!q) break; o.push(q.slice()); } return o; };
  const at = (u) => { api.seek(sc.moveStart + (sc.moveEnd - sc.moveStart) * u); return read(); };
  api.seek(d);            const end = read();
  const start = at(0);
  const path = [];
  for (let s = 1; s <= args.samples; s++) path.push(at(s / args.samples));
  const lock = at(args.lockAt);

  // Outcome: where the free run had got to when the lock-in took over.
  let residual = 0, turn = 0, sum = 0, count = 0;
  for (let i = 0; i < end.length; i++) {
    if (!lock[i]) continue;
    const r = Math.hypot(lock[i][0] - end[i][0], lock[i][1] - end[i][1]);
    if (r > residual) residual = r;
    sum += r; count++;
    let da = Math.abs(lock[i][2] - end[i][2]) % 90;
    if (da > 45) da = 90 - da;
    if (da > turn) turn = da;
  }

  // Motion: how the journey went.
  let wander = 0, jerk = 0;
  for (let i = 0; i < end.length; i++) {
    if (!start[i]) continue;
    const vx = end[i][0] - start[i][0], vy = end[i][1] - start[i][1];
    const len2 = vx * vx + vy * vy;
    let prev = start[i];
    for (const frame of path) {
      const q = frame[i];
      if (!q) continue;
      const px = q[0] - start[i][0], py = q[1] - start[i][1];
      const u = len2 > 1e-12 ? Math.max(0, Math.min(1, (px * vx + py * vy) / len2)) : 0;
      const off = Math.hypot(px - vx * u, py - vy * u);
      if (off > wander) wander = off;
      const step = Math.hypot(q[0] - prev[0], q[1] - prev[1]);
      if (step > jerk) jerk = step;
      prev = q;
    }
  }
  // The deepest overlap the run reached, which the page measures for its own readout.
  const built = api.physics(api.state().pair, args.style);
  api.seek(d);
  return {
    squares: end.length,
    residual: residual, mean: count ? sum / count : 0, turn: turn,
    wander: wander, jerk: jerk,
    overlap: built.maxPenetration === undefined ? 0 : built.maxPenetration,
    ms: built.ms === undefined ? 0 : built.ms,
  };
}"""


def grade(row: dict[str, float]) -> float:
    """One number from both families, 0 to 1, with 1 perfect. Components stay printed beside it."""
    penalty = sum(weight * float(row.get(name, 0.0)) for name, weight in WEIGHTS.items())
    return 1.0 / (1.0 + penalty)


def measure(page, sizes: tuple[int, ...], style: str, samples: int) -> list[dict]:
    """One row per step, at the configuration the page is currently in."""
    pairs = page.evaluate("window.atlasTransitions.pairs()")
    rows = []
    for n in sizes:
        found = [p for p in pairs if p["n"] + 1 == n]
        if not found:
            continue
        page.evaluate(f"window.atlasTransitions.select({found[0]['index']})")
        row = page.evaluate(MEASURE, {"samples": samples, "lockAt": LOCK_IN_AT, "style": style})
        row["n"] = n
        row["kind"] = found[0]["kind"]
        row["grade"] = grade(row)
        rows.append(row)
    return rows


def report(label: str, rows: list[dict]) -> dict:
    """Print the rows and their medians, and return the summary."""
    print(f"\n== {label} ==")
    head = f"{'n':>5} {'residual':>9} {'mean':>7} {'turn':>7} {'wander':>8} {'jerk':>7} {'overlap':>8} {'grade':>7}"
    print(head)
    for row in rows:
        print(
            f"{row['n']:>5} {row['residual']:>9.3f} {row['mean']:>7.3f} {row['turn']:>7.2f} "
            f"{row['wander']:>8.3f} {row['jerk']:>7.3f} {row['overlap']:>8.4f} {row['grade']:>7.3f}"
        )
    if not rows:
        return {}
    summary = {
        name: round(statistics.median(row[name] for row in rows), 4)
        for name in ("residual", "mean", "turn", "wander", "jerk", "overlap", "grade")
    }
    print(
        f"{'med':>5} {summary['residual']:>9.3f} {summary['mean']:>7.3f} {summary['turn']:>7.2f} "
        f"{summary['wander']:>8.3f} {summary['jerk']:>7.3f} {summary['overlap']:>8.4f} "
        f"{summary['grade']:>7.3f}"
    )
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("page", nargs="?", type=Path, default=DEFAULT_PAGE)
    ap.add_argument("--style", default="physics", choices=("physics", "bodies"))
    ap.add_argument("--anneal", type=int, default=None, help="the annealing dial, 0 to 10")
    ap.add_argument("--sizes", type=int, nargs="*", default=list(DEFAULT_SIZES))
    ap.add_argument("--samples", type=int, default=24, help="frames sampled across the move")
    ap.add_argument("--compare", action="store_true", help="both styles at three anneal levels")
    ap.add_argument("--json", type=Path, help="write the rows here as well")
    o = ap.parse_args()

    if not o.page.exists():
        raise SystemExit(f"{o.page} is not built: run `python -m devtools.build_workbench_site`")
    sizes = tuple(o.sizes)
    out: dict[str, dict] = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(o.page.resolve().as_uri(), wait_until="load")
        page.evaluate("document.fonts.ready")
        page.evaluate("window.atlasTransitions.setMode('animate')")
        page.evaluate("window.atlasTransitions.setCapture(true)")
        settings = (
            [(style, level) for style in ("physics", "bodies") for level in (0, 3, 8)]
            if o.compare
            else [(o.style, o.anneal)]
        )
        everything = []
        for style, level in settings:
            page.evaluate(f"window.atlasTransitions.setStyle({json.dumps(style)})")
            if level is not None:
                page.evaluate(f"window.atlasTransitions.setAnneal({level})")
            label = f"{style}, anneal {level if level is not None else 'as set'}"
            rows = measure(page, sizes, style, o.samples)
            out[label] = report(label, rows)
            everything.extend({**row, "style": style, "anneal": level} for row in rows)
        browser.close()

    if len(out) > 1:
        print("\n== by grade ==")
        for label, summary in sorted(out.items(), key=lambda kv: -kv[1].get("grade", 0)):
            print(f"  {summary.get('grade', 0):.3f}  {label}")
    if o.json:
        o.json.write_text(
            json.dumps({"weights": WEIGHTS, "lock_in_at": LOCK_IN_AT, "rows": everything}, indent=2),
            encoding="utf-8",
        )
        print(f"\nwrote {o.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
