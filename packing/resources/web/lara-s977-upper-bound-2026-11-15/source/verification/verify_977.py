#!/usr/bin/env python3
"""Read the published coordinate certificate and verify the packing with Shapely.

Usage: python3 verification/verify_977.py
Does not modify the certificate or require external data beyond this repository.
"""
import csv
import json
import math
import platform
import sys
import time
from pathlib import Path

import shapely
from shapely.geometry import Polygon, box
from shapely.strtree import STRtree

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "certificates" / "n977_coordinates.csv"
CONTAINER_SIDE = 31.85
EPS = 1e-11  # numerical area tolerance; not an exact proof


def polygon(x, y, angle):
    c, s = math.cos(angle), math.sin(angle)
    return Polygon([(x + u*c - v*s, y + u*s + v*c)
                    for u,v in ((-.5,-.5),(.5,-.5),(.5,.5),(-.5,.5))])


def main():
    start = time.perf_counter()
    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 977, f"Expected 977 rows, got {len(rows)}"
    assert [int(r['id']) for r in rows] == list(range(977))
    assert [int(r['square_id']) for r in rows] == list(range(977))
    assert all(int(r['n']) == 977 for r in rows)
    angles = [float(r['angle']) for r in rows]
    middle = sum(abs(a - math.pi/4) < 1e-12 for a in angles)
    corners = sum(abs(a) < 1e-12 for a in angles)
    assert (middle, corners) == (441, 536), (middle, corners)
    poly = [polygon(float(r['x']),float(r['y']),a) for r,a in zip(rows,angles)]
    area = box(0, 0, CONTAINER_SIDE, CONTAINER_SIDE)
    outside = [i for i,p in enumerate(poly) if p.difference(area).area > EPS]
    tree = STRtree(poly)
    overlaps = []
    tested_pairs = 0
    for i,p in enumerate(poly):
        for raw_j in tree.query(p):
            j = int(raw_j)
            if j <= i: continue
            tested_pairs += 1
            intersection = p.intersection(poly[j]).area
            if intersection > EPS: overlaps.append((i,j,intersection))
    elapsed = time.perf_counter() - start
    result = {
        'n': len(rows), 'middle': middle, 'corners': corners,
        'side_checked': CONTAINER_SIDE, 'side_less_than_32': CONTAINER_SIDE < 32,
        'outside_count': len(outside), 'overlapping_pairs': len(overlaps),
        'candidate_pairs_tested': tested_pairs,
        'all_possible_pairs': len(poly)*(len(poly)-1)//2,
        'area_tolerance': EPS, 'valid_numerically': not outside and not overlaps,
        'arithmetic': 'IEEE-754 double precision with Shapely floating-point predicates',
        'python_version': platform.python_version(),
        'shapely_version': shapely.__version__,
        'platform': platform.platform(), 'elapsed_seconds': round(elapsed,6)
    }
    print(json.dumps(result, indent=2))
    return 0 if result['valid_numerically'] else 1


if __name__ == '__main__':
    sys.exit(main())
