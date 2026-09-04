#!/usr/bin/env python3
"""Show what the verifier refuses, and by which condition.

Usage:
    python3 falsify.py [--quick] [certificate.json] [PERTURBATION ...]

A verifier that has only ever said yes has demonstrated nothing. This script
applies named perturbations to the certificate, runs verify.py's decision on
each (all conditions, never short-circuited), and prints a Markdown table of
the refusals with the actual numbers. Standard library only; it imports
verify.py from its own directory and nothing else.

With --quick, only a negative-weight mutation is run.  It stops at the
verifier's preconditions, so it is suitable for a fast required gate.

The perturbed atom is chosen from the verifier's own witness: the first atom
covered by the least-covered placement of the unperturbed certificate, so a
lowered weight or a dropped atom is guaranteed to touch the tight cell and
show up in C4, not only in the symmetry condition C0.
"""

import json
import os
import sys
import tempfile
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify  # noqa: E402

TINY = Fraction(1, 10000)
ABSENT = object()


def expected(c0, c1, c2, c3, c4, minimum):
    """The complete oracle for one published perturbation."""
    return {
        "accepted": False,
        "conditions": {"C0": c0, "C1": c1, "C2": c2, "C3": c3, "C4": c4},
        "minimum": minimum,
    }


QUICK_EXPECTATION = {
    "accepted": False,
    "conditions": {"P2": False},
    "minimum": ABSENT,
}


def covered(atom, cert, c, s, X, Y):
    x, y = atom[0], atom[1]
    half = cert["B"] / 2
    along = c * (x - X) + s * (y - Y)
    across = -s * (x - X) + c * (y - Y)
    return -half <= along <= half and -half <= across <= half


def perturbations(record, cert, witness):
    """Return each mutation together with its exact, verdict-bearing oracle."""
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
        ("weight of that atom lowered by 1/10000", weight_lowered,
         expected(False, True, True, True, False, Fraction(24999, 25000))),
        ("weights of its whole orbit (8 atoms) lowered by 1/10000", orbit_lowered,
         expected(True, True, True, True, False, Fraction(49993, 50000))),
        ("that atom dropped", atom_dropped,
         expected(False, True, True, True, False, Fraction(49189, 50000))),
        ("its whole orbit dropped", orbit_dropped,
         expected(True, True, True, True, False, Fraction(387, 400))),
        ("that atom shifted by +1/1000 in x", atom_shifted,
         expected(False, True, True, True, True, Fraction(50003, 50000))),
        ("container side 4 instead of %s, atoms unchanged" % L, container_enlarged,
         expected(False, True, True, True, False, Fraction(0))),
        ("container side 4, atoms translated by +%s to keep the symmetry" % ((Fraction(4) - L) / 2),
         container_enlarged_recentred,
         expected(True, True, True, True, False, Fraction(0))),
        ("weights scaled so the total is exactly n", mass_reaching_n,
         expected(True, False, True, True, True, Fraction(1100066, 1084775))),
        ("angle limit 41/100, short of tan(pi/8)", net_short_of_pi_over_4,
         expected(True, True, False, True, False, Fraction(195849, 200000))),
        ("B raised to 1/(1 + D), so B(1 + D) = 1", shrink_touching,
         expected(True, True, True, False, True, Fraction(50003, 50000))),
    ]


def condition_result(results, prefix):
    for key, value in results.items():
        if key.startswith(prefix):
            return value[1]
    return None


def expectation_errors(accepted, results, oracle):
    """Return every way a verifier result disagrees with a mutation oracle."""
    errors = []
    if accepted != oracle["accepted"]:
        errors.append("verdict was %s, expected %s"
                      % ("accepted" if accepted else "REFUSED",
                         "accepted" if oracle["accepted"] else "REFUSED"))
    for prefix, wanted in oracle["conditions"].items():
        actual = condition_result(results, prefix)
        if actual is None:
            errors.append("%s result is missing" % prefix)
        elif actual != wanted:
            errors.append("%s was %s, expected %s"
                          % (prefix, "PASS" if actual else "FAIL",
                             "PASS" if wanted else "FAIL"))
    wanted_minimum = oracle["minimum"]
    if wanted_minimum is ABSENT:
        if "minimum" in results:
            errors.append("minimum was %s, expected no C4 result" % results["minimum"])
    elif results.get("minimum", ABSENT) != wanted_minimum:
        actual = results.get("minimum", "missing")
        errors.append("minimum was %s, expected %s" % (actual, wanted_minimum))
    return errors


def run(record, name, oracle):
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, "perturbed.json")
        with open(path, "w") as handle:
            json.dump(record, handle)
        cert = verify.load(path)
        accepted, results = verify.decide(cert, log=lambda *args: None)

    def mark(prefix):
        value = condition_result(results, prefix)
        return "-" if value is None else ("PASS" if value else "FAIL")

    total = sum((w for _, _, w in cert["atoms"]), Fraction(0))
    last = cert["tangents"][-1]
    product = cert["B"] * (1 + verify.largest_half_gap_tangent(cert["tangents"]))
    minimum = results.get("minimum", ABSENT)
    minimum_text = "-" if minimum is ABSENT or minimum is None else "%s = %.6f" % (
        minimum, float(minimum))
    row = "| %s | %s (%s) | %s (%s) | %s (%s) | %s (%.9f) | %s (%s) | %s |" % (
        name,
        mark("C0"), "%d atoms" % len(cert["atoms"]),
        mark("C1"), total,
        mark("C2"), last * last + 2 * last - 1,
        mark("C3"), float(product),
        mark("C4"), minimum_text,
        "accepted" if accepted else "REFUSED",
    )
    return row, expectation_errors(accepted, results, oracle)


def quick_negative_weight(record):
    """A cheap mutation that must be refused by P2 before the C4 sweep."""
    changed = json.loads(json.dumps(record))
    atoms = changed.get("atoms")
    if not isinstance(atoms, list) or not atoms:
        raise ValueError("quick control needs a non-empty atoms array")
    if not isinstance(atoms[0], list) or len(atoms[0]) != 3:
        raise ValueError("quick control needs atom 0 to be a triple")
    atoms[0][2] = "-1"
    return changed


def print_table_header():
    print("| perturbation | C0 | C1 total | C2 slack | C3 B(1+D) | C4 least covered weight | verdict |")
    print("| --- | --- | --- | --- | --- | --- | --- |")


def main(argv):
    args = list(argv[1:])
    quick = "--quick" in args
    if quick:
        args.remove("--quick")
        if "--quick" in args:
            print("--quick may be specified only once")
            return 2
    path = args.pop(0) if args else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "certificate.json")
    try:
        selected = [int(a) for a in args]
    except ValueError:
        print(__doc__)
        return 2
    if quick and selected:
        print("--quick does not take perturbation numbers")
        return 2
    with open(path) as handle:
        record = json.load(handle)

    if quick:
        print("quick negative-weight control: atom 0 weight replaced by -1")
        print_table_header()
        row, errors = run(quick_negative_weight(record), "negative weight", QUICK_EXPECTATION)
        print(row)
        for error in errors:
            print("EXPECTATION FAILED: %s" % error, file=sys.stderr)
        if errors:
            return 1
        print("quick negative control: expected refusal and P2 result confirmed")
        return 0

    cert = verify.load(path)
    print("baseline: deciding the unperturbed certificate to locate its tight placement")
    accepted, results = verify.decide(cert, log=lambda *args: None)
    if not accepted:
        print("the unperturbed certificate is refused; nothing to falsify")
        return 1
    k, t, X, Y = results["witness"]
    print("least covered weight %s at direction %d, centre (%s, %s)" % (results["minimum"], k, X, Y))
    site, table = perturbations(record, cert, results["witness"])
    invalid = sorted(set(selected) - set(range(len(table))))
    if invalid:
        print("unknown perturbation number(s): %s" % ", ".join(map(str, invalid)))
        return 2
    print("perturbed site: %s" % site)
    print()
    print_table_header()
    failures = 0
    for index, (name, make, oracle) in enumerate(table):
        if selected and index not in selected:
            continue
        row, errors = run(make(), name, oracle)
        print(row, flush=True)
        for error in errors:
            print("EXPECTATION FAILED [%d %s]: %s" % (index, name, error), file=sys.stderr)
        failures += len(errors)
    if failures:
        print("falsify.py: %d expectation failure(s)" % failures, file=sys.stderr)
        return 1
    print("falsify.py: every selected mutation matched its refusal oracle")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
