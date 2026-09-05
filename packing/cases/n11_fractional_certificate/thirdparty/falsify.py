#!/usr/bin/env python3
"""Show what the verifier refuses, and by which condition.

Usage:
    python3 falsify.py [--quick] [certificate.json] [PERTURBATION ...]

A verifier that has only ever said yes has demonstrated nothing. This script
applies named perturbations to the certificate, runs verify.py's decision on
each (all conditions, never short-circuited), and prints a Markdown table of
the refusals with the actual numbers. Standard library only; it imports
verify.py from its own directory and nothing else.

It is not a general tool, and the certificate argument is not a general one.
Every perturbation below carries an oracle -- the verdict, the five condition
results and the exact least covered weight it must produce -- and those are
this directory's certificate.json and no other file's, so the script decides
rather than merely reports. A path that is not this directory's
certificate.json is refused by name instead of being measured against numbers
that are not its own. The argument stays for explicitness.

With --quick, only a negative-weight mutation is run. It stops at the
verifier's preconditions before any Condition 5 sweep, so it is cheap enough
for a required gate, and it is the one mutation whose oracle does not depend
on which certificate it is applied to.

The perturbed atom is chosen from the verifier's own witness: the first atom
covered by the least-covered placement of the unperturbed certificate, so a
lowered weight or a dropped atom is guaranteed to touch the tight cell and
show up in Condition 5, not only in the symmetry condition, Condition 1.
"""

# ruff: noqa: N803, N806, FBT003, PLR0917 -- L, D, X, Y are the theorem's own symbols, and the
# oracle table's rows are positional so that each reads as one line beside its name.

import json
import sys
import tempfile
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify

TINY = Fraction(1, 10000)
SHIPPED = Path(__file__).resolve().parent / "certificate.json"
ABSENT = object()


def expected(condition_1, condition_2, condition_3, condition_4, condition_5, minimum):
    """The complete oracle for one published perturbation of certificate.json.

    Every figure below was read off a run of this script on the shipped file,
    not copied from prose. Re-derive them by deleting an oracle and running the
    perturbation alone.
    """
    return {
        "accepted": False,
        "conditions": {
            "Condition 1": condition_1,
            "Condition 2": condition_2,
            "Condition 3": condition_3,
            "Condition 4": condition_4,
            "Condition 5": condition_5,
        },
        "minimum": minimum,
    }


# The one mutation whose oracle is certificate-independent: a negative weight
# breaks the counting step for any certificate, and P2 refuses it before the
# conditions are reached, so there is no Condition 5 minimum to compare.
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
    _k, t, X, Y = witness
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
        r["claim"] = f"s({cert['n']}) >= 4"
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

    site = f"atom {target} at ({x0}, {y0}), weight {w0}"
    return site, [
        (
            "weight of that atom lowered by 1/10000",
            weight_lowered,
            expected(False, True, True, True, False, Fraction(24999, 25000)),
        ),
        (
            "weights of its whole orbit (8 atoms) lowered by 1/10000",
            orbit_lowered,
            expected(True, True, True, True, False, Fraction(49993, 50000)),
        ),
        (
            "that atom dropped",
            atom_dropped,
            expected(False, True, True, True, False, Fraction(49189, 50000)),
        ),
        (
            "its whole orbit dropped",
            orbit_dropped,
            expected(True, True, True, True, False, Fraction(387, 400)),
        ),
        (
            "that atom shifted by +1/1000 in x",
            atom_shifted,
            expected(False, True, True, True, True, Fraction(50003, 50000)),
        ),
        (
            f"container side 4 instead of {L}, atoms unchanged",
            container_enlarged,
            expected(False, True, True, True, False, Fraction(0)),
        ),
        (
            "container side 4, atoms translated by +%s to keep the symmetry"
            % ((Fraction(4) - L) / 2),
            container_enlarged_recentred,
            expected(True, True, True, True, False, Fraction(0)),
        ),
        (
            "weights scaled so the total is exactly n",
            mass_reaching_n,
            expected(True, False, True, True, True, Fraction(1100066, 1084775)),
        ),
        (
            "angle limit 41/100, short of tan(pi/8)",
            net_short_of_pi_over_4,
            expected(True, True, False, True, False, Fraction(195849, 200000)),
        ),
        (
            "B raised to 1/(1 + D), so B(1 + D) = 1",
            shrink_touching,
            expected(True, True, True, False, True, Fraction(50003, 50000)),
        ),
    ]


def condition_result(results, prefix):
    """The PASS/FAIL of the one check whose name starts with `prefix`, or None."""
    for key, value in results.items():
        if key.startswith(prefix):
            return value[1]
    return None


def expectation_errors(accepted, results, oracle):
    """Every way one decision disagrees with the mutation's oracle."""
    errors = []
    if accepted != oracle["accepted"]:
        errors.append(
            "verdict was {}, expected {}".format(
                "accepted" if accepted else "REFUSED",
                "accepted" if oracle["accepted"] else "REFUSED",
            )
        )
    for prefix, wanted in oracle["conditions"].items():
        actual = condition_result(results, prefix)
        if actual is None:
            errors.append(f"{prefix} result is missing")
        elif actual != wanted:
            errors.append(
                "{} was {}, expected {}".format(
                    prefix, "PASS" if actual else "FAIL", "PASS" if wanted else "FAIL"
                )
            )
    wanted_minimum = oracle["minimum"]
    if wanted_minimum is ABSENT:
        if results.get("minimum", ABSENT) is not ABSENT:
            errors.append(
                "minimum was {}, expected no Condition 5 result".format(results["minimum"])
            )
    elif results.get("minimum", ABSENT) != wanted_minimum:
        errors.append(
            "minimum was {}, expected {}".format(
                results.get("minimum", "missing"), wanted_minimum
            )
        )
    return errors


def run(record, name, oracle):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "perturbed.json"
        with path.open("w") as handle:
            json.dump(record, handle)
        cert = verify.load(str(path))
        accepted, results = verify.decide(cert, log=lambda *_args: None)

    def mark(prefix):
        value = condition_result(results, prefix)
        return "-" if value is None else ("PASS" if value else "FAIL")

    total = sum((w for _, _, w in cert["atoms"]), Fraction(0))
    last = cert["tangents"][-1]
    product = cert["B"] * (1 + verify.largest_half_gap_tangent(cert["tangents"]))
    minimum = results.get("minimum")
    shown = "-" if minimum is None else f"{minimum} = {float(minimum):.6f}"
    row = "| {} | {} ({}) | {} ({}) | {} ({}) | {} ({:.9f}) | {} ({}) | {} |".format(
        name,
        mark("Condition 1"),
        f"{len(cert['atoms'])} atoms",
        mark("Condition 2"),
        total,
        mark("Condition 3"),
        last * last + 2 * last - 1,
        mark("Condition 4"),
        float(product),
        mark("Condition 5"),
        shown,
        "accepted" if accepted else "REFUSED",
    )
    return row, expectation_errors(accepted, results, oracle)


def negative_weight(record):
    """The one cheap mutation: atom 0 given weight -1, refused by P2."""
    changed = json.loads(json.dumps(record))
    atoms = changed.get("atoms")
    if not isinstance(atoms, list) or not atoms:
        raise ValueError("the quick control needs a non-empty atoms array")
    if not isinstance(atoms[0], list) or len(atoms[0]) != 3:
        raise ValueError("the quick control needs atom 0 to be a triple")
    atoms[0][2] = "-1"
    return changed


def print_table_header():
    print(
        "| perturbation | Condition 1 | Condition 2 total | Condition 3 slack"
        " | Condition 4 B(1+D) | Condition 5 least covered weight | verdict |"
    )
    print("| --- | --- | --- | --- | --- | --- | --- |")


def main(argv: Sequence[str] | None = None) -> int:  # noqa: PLR0911 - each usage error returns 2 where it is found
    args = list(sys.argv[1:] if argv is None else argv)
    quick = "--quick" in args
    while quick and "--quick" in args:
        args.remove("--quick")
    path = args.pop(0) if args else SHIPPED
    try:
        selected = [int(argument) for argument in args]
    except ValueError:
        print(__doc__)
        return 2
    if quick and selected:
        print("--quick does not take perturbation numbers")
        return 2
    if Path(path).resolve() != SHIPPED:
        # The oracles below are this file's numbers. Measuring another
        # certificate against them would report failures that are the script's
        # and not the file's, which is worse than declining.
        print(f"this script only decides this directory's certificate.json; {path} is not it")
        return 2
    with Path(path).open() as handle:
        record = json.load(handle)

    if quick:
        print("quick negative-weight control: atom 0 weight replaced by -1")
        print_table_header()
        row, errors = run(negative_weight(record), "negative weight", QUICK_EXPECTATION)
        print(row)
        for error in errors:
            print(f"EXPECTATION FAILED: {error}", file=sys.stderr)
        if errors:
            return 1
        print("quick negative control: expected refusal and P2 result confirmed")
        return 0

    cert = verify.load(path)
    print("baseline: deciding the unperturbed certificate to locate its tight placement")
    accepted, results = verify.decide(cert, log=lambda *_args: None)
    if not accepted:
        print("the unperturbed certificate is refused; nothing to falsify")
        return 1
    k, _t, X, Y = results["witness"]
    print(f"least covered weight {results['minimum']} at direction {k}, centre ({X}, {Y})")
    site, table = perturbations(record, cert, results["witness"])
    unknown = sorted(set(selected) - set(range(len(table))))
    if unknown:
        print("unknown perturbation number(s): {}".format(", ".join(map(str, unknown))))
        return 2
    print(f"perturbed site: {site}")
    print()
    print_table_header()
    failures = 0
    for index, (name, make, oracle) in enumerate(table):
        if selected and index not in selected:
            continue
        row, errors = run(make(), name, oracle)
        print(row, flush=True)
        for error in errors:
            print(f"EXPECTATION FAILED [{index} {name}]: {error}", file=sys.stderr)
        failures += len(errors)
    if failures:
        print(f"falsify.py: {failures} expectation failure(s)", file=sys.stderr)
        return 1
    print("falsify.py: every mutation run matched its refusal oracle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
