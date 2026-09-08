#!/usr/bin/env python3
"""Exercise and sweep revision 5's block matching. Run with packing/.venv/bin/python3.

    experiment_block_matching.py 100 110 307          # per-pair block report for the pairs named
    experiment_block_matching.py --sweep               # the discount and the tolerances over all 158 assignment pairs

The per-pair report lists every block the assignment kept (size, turn, pivots, residual),
the squares moving alone, the new square with its rule and tie set, and the arrival overlap
count. The sweep re-matches every assignment pair at each setting and tabulates how many
moving squares ride in blocks, the residuals, the crossings and the new-square choices, so
the constants in build_candidate.py are a measured choice.
"""

from __future__ import annotations

import argparse
import json
import sys
import time

import build_candidate as bc


def load_all() -> tuple[dict, dict, dict]:
    manifest = {e["n"]: e for e in json.loads(bc.MANIFEST.read_text())["atlas"]["entries"]}
    witnesses = {n: bc.load_witness(n) for n in range(1, bc.N_MAX + 1)}
    renderings = {n: bc.load_rendering(n) for n in range(1, bc.N_MAX + 1)}
    return manifest, witnesses, renderings


def report(n: int, manifest: dict, witnesses: dict, renderings: dict) -> None:
    a, b = witnesses[n], witnesses[n + 1]
    started = time.perf_counter()
    match = bc.match_pair(a, b, renderings[n], renderings[n + 1], manifest[n + 1])
    s = bc.pair_stats(a, b, match)
    elapsed = time.perf_counter() - started
    print(
        f"{n}->{n + 1} {s['kind']}: clusters {s['clusters_from']}/{s['clusters_to']}, links {s['links_found']}, "
        f"blocks {s['block_count']}; moving {s['moving']} = {s['moving_in_block']} in blocks + {s['moving_individually']} alone, "
        f"stationary {s['stationary']}; residual mean {s['block_residual_mean']} max {s['block_residual_max']}; "
        f"max displacement {s['max_displacement']}, {s['crossings']} close passes; new square {s['new_index']} "
        f"(revision 4 left {s['new_index_hungarian']}), {s['new_tied']} tied, by {s['new_rule']}; "
        f"{s['arrival_overlaps']} squares under it at arrival; {elapsed * 1000:.0f} ms"
    )
    for blk in s["blocks"]:
        print(
            f"    block of {len(blk['members']):3d}: turn {blk['turn']:7.2f} deg, pivot {blk['from']} -> {blk['to']}, "
            f"residual mean {blk['residual_mean']} max {blk['residual_max']}"
        )
    alone = [i for i in range(n) if s["block_of"][i] < 0]
    moving_alone = []
    for i in alone:
        x0, y0, a0 = a["squares"][i]
        x1, y1, a1 = b["squares"][s["map"][i]]
        d = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        if d > bc.MOVE_TOLERANCE or abs(bc.angle_delta(a0, a1)) > bc.ROTATION_TOLERANCE_DEG:
            moving_alone.append((i, round(d, 2), round(bc.angle_delta(a0, a1), 1)))
    if moving_alone:
        print(f"    moving alone (index, travel, turn): {moving_alone[:20]}{' ...' if len(moving_alone) > 20 else ''}")


SWEEP_KEYS = ("BLOCK_DISCOUNT", "INDIVIDUAL_PENALTY", "BLOCK_RESIDUAL_TOL", "CLUSTER_ANGLE_TOL", "CLUSTER_GAP_TOL", "BLOCK_SLIDE_MAX")


def sweep(manifest: dict, witnesses: dict, renderings: dict, quick: bool = False) -> None:
    matched = [n for n in range(1, bc.N_MAX) if bc.match_pair(witnesses[n], witnesses[n + 1], renderings[n], renderings[n + 1], manifest[n + 1])["kind"] == "matched"]
    baseline = {key: getattr(bc, key) for key in SWEEP_KEYS}
    settings = [("baseline", {})]
    settings += [(f"discount {v}", {"BLOCK_DISCOUNT": v}) for v in (0.0, 0.25, 0.5, 1.0)]
    settings += [(f"individual penalty {v}", {"INDIVIDUAL_PENALTY": v}) for v in (0.0, 0.5, 2.0, 4.0)]
    if not quick:
        settings += [(f"residual tol {v}", {"BLOCK_RESIDUAL_TOL": v}) for v in (0.2, 0.5)]
        settings += [(f"cluster angle tol {v}", {"CLUSTER_ANGLE_TOL": v}) for v in (2.0, 8.0)]
        settings += [(f"cluster gap tol {v}", {"CLUSTER_GAP_TOL": v}) for v in (0.08, 0.4)]
        settings += [(f"slide max {v}", {"BLOCK_SLIDE_MAX": v}) for v in (1.0, 3.0)]
    print("| setting | moving in blocks | of moving | pairs at least half in blocks | pairs all in blocks | hops (alone, no turn) | mean residual | max residual | crossings | max of max disp | new differs from rev 4 | seconds |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, overrides in settings:
        for key, value in baseline.items():
            setattr(bc, key, overrides.get(key, value))
        started = time.perf_counter()
        rows = []
        for n in matched:
            match = bc.match_pair(witnesses[n], witnesses[n + 1], renderings[n], renderings[n + 1], manifest[n + 1])
            rows.append(bc.pair_stats(witnesses[n], witnesses[n + 1], match))
        elapsed = time.perf_counter() - started
        moving = sum(r["moving"] for r in rows)
        in_block = sum(r["moving_in_block"] for r in rows)
        members = sum(r["in_block"] for r in rows)
        mean_res = sum(r["block_residual_mean"] * r["in_block"] for r in rows) / max(1, members)
        print(
            f"| {name} | {in_block} | {moving} | {sum(1 for r in rows if r['moving'] and r['moving_in_block'] >= 0.5 * r['moving'])} | "
            f"{sum(1 for r in rows if r['moving'] and r['moving_individually'] == 0)} | {sum(r['alone_hops'] for r in rows)} | {mean_res:.3f} | "
            f"{max(r['block_residual_max'] for r in rows):.3f} | {sum(r['crossings'] for r in rows)} | "
            f"{max(r['max_displacement'] for r in rows):.2f} | {sum(1 for r in rows if r['new_choice_differs'])} | {elapsed:.1f} |"
        )
    for key, value in baseline.items():
        setattr(bc, key, value)


PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#17becf", "#bcbd22", "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173", "#3182bd", "#e6550d", "#31a354", "#756bb1", "#636363", "#6baed6"]


def draw(n: int, manifest: dict, witnesses: dict, renderings: dict, out_dir) -> None:
    """Frames n and n+1 side by side, squares coloured by the block that carries them (grey
    for a square moving alone, pale for one that stays, scarlet for the new square), numbered
    by index; written to frames/blocks-NNN.png through the headless shell."""
    import os  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415

    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    a, b = witnesses[n], witnesses[n + 1]
    match = bc.match_pair(a, b, renderings[n], renderings[n + 1], manifest[n + 1])
    s = bc.pair_stats(a, b, match)
    side = max(a["side"], b["side"])

    def colour(i: int, moving: bool) -> str:
        k = s["block_of"][i]
        if k >= 0:
            return PALETTE[k % len(PALETTE)]
        return "#9a9a9a" if moving else "#e4e4e4"

    def frame_svg(w: dict, fills: list[str], labels: list[str], title: str) -> str:
        parts = [f'<svg viewBox="-0.6 -0.6 {side + 1.2} {side + 1.4}" width="700" height="712"><g transform="translate(0 {side}) scale(1 -1)">']
        parts.append(f'<rect x="0" y="0" width="{w["side"]}" height="{w["side"]}" fill="none" stroke="#000" stroke-width="0.04"/>')
        for (x, y, ang), fill, label in zip(w["squares"], fills, labels, strict=True):
            parts.append(f'<g transform="translate({x} {y}) rotate({ang})"><rect x="-0.5" y="-0.5" width="1" height="1" fill="{fill}" stroke="#000" stroke-width="0.03"/>'
                         f'<text transform="scale(1 -1)" font-size="0.34" text-anchor="middle" y="0.12" font-family="sans-serif" fill="#000">{label}</text></g>')
        parts.append(f'</g><text x="0" y="{side + 0.7}" font-size="0.45" font-family="sans-serif">{title}</text></svg>')
        return "".join(parts)

    moving = set()
    for i in range(n):
        x0, y0, a0 = a["squares"][i]
        x1, y1, a1 = b["squares"][s["map"][i]]
        if ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 > bc.MOVE_TOLERANCE or abs(bc.angle_delta(a0, a1)) > bc.ROTATION_TOLERANCE_DEG:
            moving.add(i)
    fills_a = [colour(i, i in moving) for i in range(n)]
    labels_a = [str(i) for i in range(n)]
    fills_b = ["#a3123f"] * (n + 1)
    labels_b = ["new"] * (n + 1)
    for i, j in enumerate(s["map"]):
        fills_b[j] = fills_a[i]
        labels_b[j] = str(i)
    html = (
        "<html><body style='margin:0;background:#fff;display:flex;gap:20px;font-family:sans-serif'>"
        + frame_svg(a, fills_a, labels_a, f"n = {n}: blocks coloured, alone grey, stationary pale")
        + frame_svg(b, fills_b, labels_b, f"n = {n + 1}: same colours by source index; new square scarlet ({s['new_index']}, {s['new_rule']})")
        + f"<div style='position:absolute;left:8px;top:{712 + 6}px;font-size:14px'>{s['block_count']} blocks; moving {s['moving']} = {s['moving_in_block']} in blocks + {s['moving_individually']} alone ({s['alone_hops']} hops); residual mean {s['block_residual_mean']} max {s['block_residual_max']}; max displacement {s['max_displacement']}; {s['crossings']} close passes; {s['arrival_overlaps']} under the new square at arrival</div>"
        + "</body></html>"
    )
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    page_path = out_dir / f"blocks-{n:03d}.html"
    page_path.write_text(html)
    with sync_playwright() as driver:
        browser = driver.chromium.launch(executable_path=os.environ.get("SQPACK_CHROMIUM"))
        page = browser.new_page(viewport={"width": 1440, "height": 760}, device_scale_factor=1)
        page.goto(page_path.resolve().as_uri(), wait_until="load")
        page.screenshot(path=str(out_dir / f"blocks-{n:03d}.png"), type="png")
        browser.close()
    page_path.unlink()
    print("wrote", out_dir / f"blocks-{n:03d}.png")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pairs", nargs="*", type=int, help="n of each pair n -> n+1 to report")
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument("--quick", action="store_true", help="sweep only the discount and the penalty")
    parser.add_argument("--draw", action="store_true", help="also draw each named pair to frames/blocks-NNN.png")
    parser.add_argument("--out", default=str(bc.HERE / "frames"))
    args = parser.parse_args()
    manifest, witnesses, renderings = load_all()
    for n in args.pairs:
        report(n, manifest, witnesses, renderings)
        if args.draw:
            draw(n, manifest, witnesses, renderings, args.out)
    if args.sweep:
        sweep(manifest, witnesses, renderings, quick=args.quick)
    return 0


if __name__ == "__main__":
    sys.exit(main())
