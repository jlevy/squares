"""Compare two zmx2 outputs root for root: the census ("done in" line minus timings, or ROOT lines) and the set
of UNCERT boxes (exact rational strings).  Written for the review of #973 (L144).

usage: python -I compare_uncert.py MINE THEIRS
prints a JSON verdict: equal box sets, counts, census fields of each.
"""
import json
import re
import sys

pat = re.compile(r"^UNCERT (\d+) pass (\d+) box (\S+) ")


def read(path):
    boxes = set()
    n = 0
    census = None
    header = None
    for line in open(path):
        m = pat.match(line)
        if m:
            boxes.add((int(m.group(1)), int(m.group(2)), m.group(3)))
            n += 1
        elif line.startswith("done in"):
            census = re.sub(r"done in \S+ wall: ", "", line.strip())
            census = re.sub(r", cpu \S+$", "", census)
        elif line.startswith("# zmx2 cert"):
            header = line.strip()
    return boxes, n, census, header


a, b = read(sys.argv[1]), read(sys.argv[2])
res = dict(mine=sys.argv[1].split("/")[-1], theirs=sys.argv[2].split("/")[-1],
           uncert_lines=[a[1], b[1]], distinct_boxes=[len(a[0]), len(b[0])],
           box_sets_equal=a[0] == b[0], census=[a[2], b[2]], census_equal=a[2] == b[2],
           header_equal=a[3] == b[3], headers=[a[3], b[3]])
print(json.dumps(res))
