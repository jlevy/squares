#!/usr/bin/env python3
"""Show what the verifier refuses, and by which condition.

Usage:
    python3 falsify.py [certificate.json] [PERTURBATION ...]

A verifier that has only ever said yes has demonstrated nothing. This script
applies named perturbations to the certificate, runs verify.py's decision on
each (all conditions, never short-circuited), and prints a Markdown table of
the refusals with the actual numbers. Standard library only; it imports
verify.py from its own directory and nothing else.

The perturbed atom is chosen from the verifier's own witness: the first atom
covered by the least-covered placement of the unperturbed certificate, so a
lowered weight or a dropped atom is guaranteed to touch the tight cell and
show up in Condition 5, not only in the symmetry condition, Condition 1.
"""

import json
import os
import sys
import tempfile
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify  # noqa: E402

TINY = Fraction(1, 10000)


def covered(atom, cert, c, s, X, Y):
    x, y = atom[0], atom[1]
    half = cert["B"] / 2
    along = c * (x - X) + s * (y - Y)
    across = -s * (x - X) + c * (y - Y)
    return -half <= along <= half and -half <= across <= half


def perturbations(record, cert, witness):
    """Each entry maps a name to a function that returns a modified JSON record."""
    k, t, X, Y = witness
    c, s = verify.direction(t)
    L = cert["L"]
    target = next(i for i, atom in enumerate(cert["atoms"]) if covered(atom, cert, c, s, X, Y))
    x0, y0, w0 = cert["atoms"][target]
    orbit = set(verify.symmetry_images(x0, y0, L))

    def copy():
        return json.loads(json.dumps(record))

    def in_orbit(atom):
        return (Fraction(atom[0]), Fraction(atom[1])) in orbit

    def weight_lowered():
        r = copy()
        r["atoms"][target][2] = str(Fraction(w0) - TINY)
        return r

    def orbit_lowered():
        r = copy()
        for atom in r["atoms"]:
            if in_orbit(atom):
                atom[2] = str(Fraction(atom[2]) - TINY)
        return r

    def atom_dropped():
        r = copy()
        del r["atoms"][target]
        return r

    def orbit_dropped():
        r = copy()
        r["atoms"] = [atom for atom in r["atoms"] if not in_orbit(atom)]
        return r

    def atom_shifted():
        r = copy()
        r["atoms"][target][0] = str(x0 + Fraction(1, 1000))
        return r

    def container_enlarged():
        r = copy()
        r["outer_side"] = "4"
        r["claim"] = "s(%d) >= 4" % cert["n"]
        return r

    def container_enlarged_recentred():
        r = container_enlarged()
        shift = (Fraction(4) - L) / 2
        for atom in r["atoms"]:
            atom[0] = str(Fraction(atom[0]) + shift)
            atom[1] = str(Fraction(atom[1]) + shift)
        return r

    def mass_reaching_n():
        r = copy()
        total = sum(Fraction(atom[2]) for atom in r["atoms"])
        for atom in r["atoms"]:
            atom[2] = str(Fraction(atom[2]) * cert["n"] / total)
        return r

    def net_short_of_pi_over_4():
        r = copy()
        r["angle_limit"] = "41/100"
        return r

    def shrink_touching():
        r = copy()
        D = verify.largest_half_gap_tangent(cert["tangents"])
        r["square_side"] = str(1 / (1 + D))
        return r

    site = "atom %d at (%s, %s), weight %s" % (target, x0, y0, w0)
    return site, [
        ("weight of that atom lowered by 1/10000", weight_lowered),
        ("weights of its whole orbit (8 atoms) lowered by 1/10000", orbit_lowered),
        ("that atom dropped", atom_dropped),
        ("its whole orbit dropped", orbit_dropped),
        ("that atom shifted by +1/1000 in x", atom_shifted),
        ("container side 4 instead of %s, atoms unchanged" % L, container_enlarged),
        ("container side 4, atoms translated by +%s to keep the symmetry" % ((Fraction(4) - L) / 2),
         container_enlarged_recentred),
        ("weights scaled so the total is exactly n", mass_reaching_n),
        ("angle limit 41/100, short of tan(pi/8)", net_short_of_pi_over_4),
        ("B raised to 1/(1 + D), so B(1 + D) = 1", shrink_touching),
    ]


def run(record, name):
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "perturbed.json")
        with open(path, "w") as handle:
            json.dump(record, handle)
        cert = verify.load(path)
        accepted, results = verify.decide(cert, log=lambda *args: None)
    def mark(prefix):
        for key, value in results.items():
            if key.startswith(prefix):
                return "PASS" if value[1] else "FAIL"
        return "-"
    total = sum((w for _, _, w in cert["atoms"]), Fraction(0))
    last = cert["tangents"][-1]
    product = cert["B"] * (1 + verify.largest_half_gap_tangent(cert["tangents"]))
    minimum = results.get("minimum")
    return "| %s | %s (%s) | %s (%s) | %s (%s) | %s (%.9f) | %s (%s = %.6f) | %s |" % (
        name,
        mark("Condition 1"), "%d atoms" % len(cert["atoms"]),
        mark("Condition 2"), total,
        mark("Condition 3"), last * last + 2 * last - 1,
        mark("Condition 4"), float(product),
        mark("Condition 5"), minimum, float(minimum),
        "accepted" if accepted else "REFUSED",
    )


def main(argv):
    path = argv[1] if len(argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      "certificate.json")
    selected = [int(a) for a in argv[2:]]
    with open(path) as handle:
        record = json.load(handle)
    cert = verify.load(path)
    print("baseline: deciding the unperturbed certificate to locate its tight placement")
    accepted, results = verify.decide(cert, log=lambda *args: None)
    if not accepted:
        print("the unperturbed certificate is refused; nothing to falsify")
        return 1
    k, t, X, Y = results["witness"]
    print("least covered weight %s at direction %d, centre (%s, %s)" % (results["minimum"], k, X, Y))
    site, table = perturbations(record, cert, results["witness"])
    print("perturbed site: %s" % site)
    print()
    print("| perturbation | Condition 1 | Condition 2 total | Condition 3 slack"
          " | Condition 4 B(1+D) | Condition 5 least covered weight | verdict |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for index, (name, make) in enumerate(table):
        if selected and index not in selected:
            continue
        print(run(make(), name), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
