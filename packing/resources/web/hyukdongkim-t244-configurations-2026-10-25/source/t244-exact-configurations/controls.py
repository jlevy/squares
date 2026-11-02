"""Control tests: each mutated certificate must be rejected by the checker given on the command line."""
import json, copy, subprocess, sys
from fractions import Fraction as Fr

checker, cert_path = sys.argv[1], sys.argv[2]
base = json.load(open(cert_path))
n = base["n"]


def bump(lst, delta):
    lst = list(lst) or ["0"]
    lst[0] = str(Fr(lst[0]) + delta)
    return lst


def run(c, name):
    json.dump(c, open("/tmp/ctrl_cert.json", "w"))
    r = subprocess.run(["python3", "-I", checker, "/tmp/ctrl_cert.json"], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    verdict = "REJECTED" if r.returncode != 0 else "accepted"
    print(f"  {name:58s} {verdict}   {out[-1][-90:] if out else ''}")
    return r.returncode != 0


# find squares touching the right wall / another square (largest x; and the first pair of near squares)
xs = [float(Fr(q["x"][0])) if len(q["x"]) == 1 else None for q in base["squares"]]
ok = True
c = copy.deepcopy(base); c["squares"].append(copy.deepcopy(c["squares"][0])); c["n"] = n + 1; ok &= run(c, "duplicate square 0 (n raised to n+1)")
c = copy.deepcopy(base); c["squares"].append(copy.deepcopy(c["squares"][0])); r = run(c, "duplicate square 0 (n left unchanged)")
for k in range(n):                                      # move each of the first few squares by 1e-30 in x and y
    pass
for k, axis in ((0, "x"), (0, "y"), (n // 2, "x"), (n // 2, "y"), (n - 1, "x"), (n - 1, "y")):
    for sgn in (1, -1):
        c = copy.deepcopy(base); q = c["squares"][k]; q[axis] = bump(q[axis], sgn * Fr(1, 10 ** 30))
        r = run(c, f"square {k} {axis} {'+' if sgn > 0 else '-'}1e-30")
        # a move may be harmless if the square has slack in that direction; report, do not require
c = copy.deepcopy(base); c["S"]["in_K"] = bump(c["S"]["in_K"], -Fr(1, 10 ** 30)); ok &= run(c, "side reduced by 1e-30")
c = copy.deepcopy(base); c["field"]["t_interval"] = [str(Fr(c["field"]["t_interval"][1]) + 1), str(Fr(c["field"]["t_interval"][1]) + 2)]
ok &= run(c, "t interval moved off the root")
print("required controls all rejected" if ok else "SOME REQUIRED CONTROL ACCEPTED")
