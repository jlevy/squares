#!/usr/bin/env python3
"""Sweep the matching's angle weight and report what it changes.

    packing/.venv/bin/python3 experiment_angle_weight.py [weights...]

For each weight the 158 matched pairs are re-matched and the table reports the mean
and maximum of the per-pair maximum displacement, the total squares that move more than
one unit, the total squares that rotate, the total rotation in degrees, and what the
4->5 pair does (whether a corner square of n=4 is sent to the centre of n=5).
"""

from __future__ import annotations

import json
import sys

import build_candidate as bc


def main(argv: list[str]) -> int:
    weights = [float(w) for w in argv] or [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
    manifest = {e["n"]: e for e in json.loads(bc.MANIFEST.read_text())["atlas"]["entries"]}
    witnesses = {n: bc.load_witness(n) for n in range(1, bc.N_MAX + 1)}
    print(
        "| angle weight | mean of max disp | max of max disp | squares moving >1 |"
        " squares rotating | total rotation (deg) | pairs with crossings |"
        " 4→5 keeps corners |"
    )
    print("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |")
    for weight in weights:
        bc.ANGLE_WEIGHT = weight
        maxima = []
        over_one = 0
        rotating = 0
        total_rotation = 0.0
        crossing_pairs = 0
        corners = None
        for n in range(1, bc.N_MAX):
            match = bc.match_pair(witnesses[n], witnesses[n + 1], manifest[n + 1])
            if match["kind"] != "matched":
                continue
            stats = bc.pair_stats(witnesses[n], witnesses[n + 1], match)
            maxima.append(stats["max_displacement"])
            over_one += stats["moved_over_1_0"]
            rotating += stats["rotated"]
            crossing_pairs += 1 if stats["crossings"] else 0
            for i, j in enumerate(match["map"]):
                here = witnesses[n]["squares"][i][2]
                there = witnesses[n + 1]["squares"][j][2]
                total_rotation += abs(bc.angle_delta(here, there))
            if n == 4:
                corners = (
                    "yes"
                    if match["new"] == 4
                    else f"no (new square is index {match['new']:d})"
                )
        print(
            f"| {weight:g} | {sum(maxima) / len(maxima):.3f} | {max(maxima):.3f} | "
            f"{over_one} | {rotating} | "
            f"{total_rotation:.0f} | {crossing_pairs} | {corners} |"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
