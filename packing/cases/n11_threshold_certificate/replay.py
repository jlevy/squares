"""Load the retained threshold certificate and bind it to the bytes that were decided.

Nothing here decides anything. The verdict comes from
`devtools.decide_threshold_certificate`, which reads the frozen file itself; this module
only names the file, states the digest the record was registered against, and reports what
the file declares about itself so a replay can compare.

The digest is part of the package rather than a note in prose because the identity of an
accepted certificate is its bytes: a replay that passed on some other file would be a
replay of some other claim.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from pathlib import Path

from devtools.decide_threshold_certificate import load
from sqpack.fractional.threshold import ThresholdCertificate

CERTIFICATE_PATH = Path(__file__).with_name("certificate.json")

FROZEN_SHA256 = "3935651af614eb3e9a1926179925f98643beb17ed1764a323fe83a527f4bad5c"
"""The SHA-256 of the bytes T-025 was registered against.

Identical to the candidate frozen by lane B of agenda-033 at
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-b-threshold-candidate-191-50.json`;
the copy here is what the frontier record cites.
"""


def digest(path: Path = CERTIFICATE_PATH) -> str:
    """The SHA-256 of the certificate's bytes, as the gate prints it."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certificate(path: Path = CERTIFICATE_PATH) -> ThresholdCertificate:
    """Rebuild the retained certificate exactly as it was accepted."""
    return load(path.read_bytes())[0]


def declared(path: Path = CERTIFICATE_PATH) -> dict[str, str]:
    """What the record claims about itself, for a replay to compare against."""
    record = load(path.read_bytes())[1]
    return {
        key: str(record[key])
        for key in ("claim", "variant", "total_budget", "least_cell_charge")
        if key in record
    }


def budget(path: Path = CERTIFICATE_PATH) -> Fraction:
    """The total budget recomputed from the atoms, never read from the summary field."""
    return certificate(path).total_budget
