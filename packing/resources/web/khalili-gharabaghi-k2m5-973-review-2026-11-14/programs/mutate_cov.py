"""Control M-4 (review of #973, L144): a copy of the coverage dumps with one box widened just outside the domain.

usage: python -I mutate_cov.py COVDIR OUTDIR
Takes, in file order, the first box that lies in the main domain (u0 = 1/4000) and in none of the five ranges
certified at u0 = 1/2000, and rewrites its u upper end to 1/4000 + 2^-40 (exact).  The other files are
symlinked.  Prints the file and the box.  (The plan's first choice, the first box of the first dump, lies in a
u0 = 1/2000 range, where the widened box is genuinely covered; see the README.)
"""
import os
import re
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2m5_coverage import in_domain  # noqa: E402

covd, outd = sys.argv[1:3]
os.makedirs(outd, exist_ok=True)
pat = re.compile(r"^(UNCERT \d+ pass \d+ box )(\S+)( .*)$")
done = False
for name in sorted(os.listdir(covd)):
    src = os.path.join(covd, name)
    dst = os.path.join(outd, name)
    if os.path.lexists(dst):
        os.remove(dst)
    if done:
        os.symlink(src, dst)
        continue
    lines = open(src).read().split("\n")
    for k, ln in enumerate(lines):
        m = pat.match(ln)
        if not m:
            continue
        box = [F(t) for t in m.group(2).split(",")]
        if in_domain(box) and in_domain(box)[0] == "main":
            nb = list(box)
            nb[5] = F(1, 4000) + F(1, 2 ** 40)
            if in_domain(nb) is None:
                parts = m.group(2).split(",")
                parts[5] = f"{nb[5].numerator}/{nb[5].denominator}"
                lines[k] = m.group(1) + ",".join(parts) + m.group(3)
                print("mutated", name, "line", k, "box", m.group(2), "->", ",".join(parts))
                done = True
                break
    if done:
        open(dst, "w").write("\n".join(lines))
    else:
        os.symlink(src, dst)
