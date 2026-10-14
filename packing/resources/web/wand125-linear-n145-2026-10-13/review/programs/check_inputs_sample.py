"""The proof bundle's inputs at chosen angles, enclosed by the exact candidate, checked here.

Usage::

    python3 -I check_inputs_sample.py BUNDLE_DIR CANDIDATE_SHA256 CERTIFICATE.json \\
        RETAINED_CHECKER.cpp ANGLE [ANGLE ...]

``BUNDLE_DIR`` is the unpacked proof bundle, holding ``candidate.json``, ``certificate.json``,
``manifest.json`` and one ``netNNN/`` folder per angle. For each angle this reads
``input.txt`` and ``result.json`` as data and prints, as JSON: the input's digest against
the record's, the stored result (verified, empty frontier, no witness, the record's node
count), the result's manifest against the facts recomputed here, the six header
enclosures (``L``, ``B``, ``E``, ``cos``, ``sin`` and ``gamma`` exactly one), and every
rectangle, point and segment line enclosing, in the source's order, the D4 image recomputed
here with its density or weight, with the widest enclosure met in units in the last place.
It also hashes every ``netNNN/verify.cpp`` against the retained checker. It decides no coverage.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import linear_exact as exact


def interval(low_token: str, high_token: str) -> tuple[Fraction, Fraction, float]:
    """The enclosure a pair of hexadecimal floats states, and its width in ulps."""
    low, high = float.fromhex(low_token), float.fromhex(high_token)
    ulps = 0.0 if low == high else (high - low) / math.ulp(low)
    return Fraction(low), Fraction(high), ulps


def encloses(tokens: list[str], values: list[Fraction]) -> tuple[bool, float]:
    if len(tokens) != 2 * len(values):
        return False, math.inf
    widest = 0.0
    for k, value in enumerate(values):
        low, high, ulps = interval(tokens[2 * k], tokens[2 * k + 1])
        if not low <= value <= high:
            return False, math.inf
        widest = max(widest, ulps)
    return True, widest


def main(argv: list[str]) -> int:
    bundle, expected = Path(argv[1]), argv[2]
    certificate = exact.load_json(Path(argv[3]).read_bytes())
    checker = exact.sha256(Path(argv[4]).read_bytes())
    angles = [int(value) for value in argv[5:]]
    candidate_bytes = (bundle / "candidate.json").read_bytes()
    if exact.sha256(candidate_bytes) != expected:
        msg = "the bundle's candidate is not the asset's"
        raise SystemExit(msg)
    candidate = exact.load_json(candidate_bytes)
    measure = exact.read_measure(candidate)
    digest = exact.semantic_digest(candidate)
    rows = {
        "rectangle": [
            (*g, w / ((g[2] - g[0]) * (g[3] - g[1]))) for g, w in measure.images["rectangle"]
        ],
        "point": [(*g, w) for g, w in measure.images["point"]],
        "segment": [(*g, w) for g, w in measure.images["segment"]],
    }
    verify_copies = sorted(bundle.glob("net*/verify.cpp"))
    checked = []
    for index in angles:
        folder = bundle / f"net{index:03}"
        raw = (folder / "input.txt").read_bytes()
        result = json.loads(
            (folder / "result.json").read_bytes(), object_pairs_hook=exact.refuse_duplicates
        )
        record = certificate["results"][str(index)]
        spec = result["manifest"]
        c, s = exact.direction(measure.step, index)
        width = exact.half_width(measure, index)
        lines = raw.decode("ascii").splitlines()
        header = [measure.side, measure.core, width, c, s, Fraction(1)]
        header_ok, header_ulps = True, 0.0
        for line, value in zip(lines[:6], header, strict=True):
            ok, ulps = encloses(line.split(), [value])
            header_ok, header_ulps = header_ok and ok, max(header_ulps, ulps)
        gamma_low, gamma_high, _ = interval(*lines[5].split())
        at, lines_ok, widest, counts_ok = 6, True, 0.0, True
        for kind in exact.KINDS:
            counts_ok = counts_ok and int(lines[at]) == len(rows[kind])
            for line, values in zip(
                lines[at + 1 : at + 1 + len(rows[kind])], rows[kind], strict=True
            ):
                ok, ulps = encloses(line.split(), list(values))
                lines_ok, widest = lines_ok and ok, max(widest, ulps)
            at += 1 + len(rows[kind])
        checked.append(
            {
                "angle": index,
                "input_sha256_is_recorded": exact.sha256(raw)
                == spec["input_sha256"]
                == record["input_sha256"],
                "result_verified_with_empty_frontier_and_no_witness": result["status"]
                == "ANGLE_VERIFIED"
                and result["frontier"] == []
                and not result["exact_witnesses"],
                "result_nodes_are_recorded": result["nodes"] == record["nodes"],
                "manifest_is_ours": spec["index"] == index
                and Fraction(spec["t"]) == index * measure.step
                and Fraction(spec["E"]) == width
                and Fraction(spec["L"]) == measure.side
                and Fraction(spec["B"]) == measure.core
                and spec["gamma"] == "1"
                and Fraction(spec["mass"]) == measure.total
                and spec["candidate_digest"] == digest
                and spec["source_sha256"] == checker,
                "header_encloses": header_ok,
                "gamma_is_exactly_one": (gamma_low, gamma_high) == (1, 1),
                "counts_are_ours": counts_ok,
                "every_line_encloses_its_image": lines_ok,
                "no_extra_lines": at == len(lines),
                "widest_header_enclosure_ulps": header_ulps,
                "widest_line_enclosure_ulps": widest,
                "lower_bound_stored": result.get("lower"),
                "verify_cpp_is_retained_checker": exact.sha256(
                    (folder / "verify.cpp").read_bytes()
                )
                == checker,
            }
        )
    report = {
        "bundle_candidate_sha256": expected,
        "semantic_digest": digest,
        "images": {kind: len(rows[kind]) for kind in exact.KINDS},
        "verify_cpp_copies": len(verify_copies),
        "verify_cpp_copies_all_retained_checker": all(
            exact.sha256(copy.read_bytes()) == checker for copy in verify_copies
        ),
        "angles": checked,
    }
    sys.stdout.write(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
