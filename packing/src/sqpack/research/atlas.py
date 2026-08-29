"""The provisional atlas: a deduplicated store of numerical quench endpoints.

One file per `n`, append-only, keyed by
[canonical basin identity](canonical.py). It answers the two questions a census exists to
answer — *how many endpoint clusters were observed* and *how often did each key turn
up* — and it is the current artifact behind the cartography strategy.
It does not yet identify connected terminal components, so its row count is not an
authoritative basin count; see F-18 in the PR #14 review.

## Append-only, and why that is not merely tidiness

An observation, once seen, remains part of the record; a later run that fails to
rediscover it does not erase it. So `add` only ever raises a frequency or introduces a
row, and nothing here deletes. That makes the endpoint-cluster discovery curve monotone
by construction. A plateau suggests saturation only for this key, proposer, quench,
and numerical regime.

It also makes the file mergeable: two runs of the same census on different machines
produce stores that combine by summing frequencies, with no reconciliation.

## What a row does and does not claim

`side` is a binary64 LP endpoint with a measured scalar side-error floor of about
`1e-11` ([D-021](../defects.md)). It is numerically checked, not exact.
`closest_pair` records only the smallest side gap. It cannot
decide endpoint or basin identity: distinct configurations may have equal sides, and a
connected terminal component may contain many geometric keys. Nothing here is entitled
to formal assurance; promotion requires an exact witness or rigorous certificate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import pairwise
from pathlib import Path
from typing import Any

import yaml

from sqpack.research.canonical import DEFAULT_QUANTUM, BasinKey

CONTRACT = "packing.squares:BasinAtlas/v1"


@dataclass
class Basin:
    """One endpoint-key cluster, and how often the proposer produced that key."""

    geometric: str
    contact: str
    side: float
    angle_signature: tuple[int, ...]
    contact_count: int
    quench_frequency: int = 1
    first_seen_seed: int | None = None
    # How many of the quenches that landed here actually proved they had converged.
    # Kept per basin rather than only in the header: a basin nothing ever converged to
    # is a different kind of object from one everything converges to, and the census
    # needs to be able to tell them apart without re-running anything.
    converged_frequency: int = 0

    @property
    def identity(self) -> tuple[str, str]:
        return (self.geometric, self.contact)


@dataclass
class Atlas:
    """Every endpoint-key cluster observed at one `n`."""

    n: int
    quantum: float = DEFAULT_QUANTUM
    contact_tol: float = 1e-9
    proposals: int = 0
    # Proposals whose quench never proved convergence. Retained as observations, but not
    # entitled to promotion as stationary components or local optima. A census where
    # most quenches stopped on a sweep limit is measuring the limit rather than the
    # landscape, and that has to be impossible to overlook.
    non_converged: int = 0
    basins: list[Basin] = field(default_factory=list)

    # --- building ---------------------------------------------------------------

    def add(self, key: BasinKey, *, seed: int | None = None, converged: bool) -> bool:
        """Record one quench endpoint key. Returns True when that key was new.

        Counting Trues against `proposals` gives a key-discovery curve. It becomes a
        basin/component discovery curve only after the component and promotion
        contracts described in F-18/F-19 are implemented.

        `converged` is required rather than defaulted, because defaulting it is how a
        census records a sweep limit as a discovery. Measured 2026-08-23 at `n = 5`: 11
        of 12 uniform multistarts hit the quench's sweep cap, and the store recorded all
        twelve stopping points as twelve distinct basins while every structural check
        passed. A caller that has to type the word has to know the answer.
        """
        self.proposals += 1
        if not converged:
            self.non_converged += 1
        for basin in self.basins:
            if basin.identity == (key.geometric, key.contact):
                basin.quench_frequency += 1
                basin.converged_frequency += int(converged)
                # Keep the best side seen for this basin. Two quenches of one basin can
                # differ by the solver floor, and the lower is the better estimate.
                basin.side = min(basin.side, key.side)
                return False
        self.basins.append(
            Basin(
                geometric=key.geometric,
                contact=key.contact,
                side=key.side,
                angle_signature=key.angle_signature,
                contact_count=key.contact_count,
                first_seen_seed=seed,
                converged_frequency=int(converged),
            )
        )
        return True

    @property
    def closest_pair(self) -> float | None:
        """The smallest side gap between two rows; never an identity decision.

        D-021 bounds error in this scalar objective only. Pose distance, active/contact
        structure, repeatability, and interval separation are required to resolve two
        endpoint candidates. The legacy field name is retained for schema compatibility.
        """
        sides = sorted(b.side for b in self.basins)
        if len(sides) < 2:
            return None
        return min(b - a for a, b in pairwise(sides))

    # --- persistence ------------------------------------------------------------

    def _sorted(self) -> list[Basin]:
        """Best side first, then by key. Deterministic, so the file is diffable and the
        drift check compares content rather than insertion order."""
        return sorted(self.basins, key=lambda b: (b.side, b.geometric, b.contact))

    def to_document(self) -> dict[str, Any]:
        return {
            "softschema": {
                "contract": CONTRACT,
                "schema": "atlas.schema.yaml",
                "envelope": "atlas",
                "status": "enforced",
            },
            "atlas": {
                "n": self.n,
                "quantum": self.quantum,
                "contact_tol": self.contact_tol,
                "proposals": self.proposals,
                "non_converged": self.non_converged,
                "distinct_basins": len(self.basins),
                "closest_pair": self.closest_pair,
                "basins": [
                    {
                        "geometric": b.geometric,
                        "contact": b.contact,
                        "side": b.side,
                        "angle_signature": list(b.angle_signature),
                        "contact_count": b.contact_count,
                        "quench_frequency": b.quench_frequency,
                        "converged_frequency": b.converged_frequency,
                        "first_seen_seed": b.first_seen_seed,
                    }
                    for b in self._sorted()
                ],
            },
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "# GENERATED by sqpack.research.atlas. "
            "Append-only: edit the census, not this file.\n"
            + yaml.safe_dump(self.to_document(), sort_keys=False, width=100)
        )

    @classmethod
    def load(cls, path: Path) -> Atlas:
        if not path.exists():
            raise FileNotFoundError(path)
        doc = yaml.safe_load(path.read_text())
        a = doc["atlas"]
        return cls(
            n=a["n"],
            quantum=a.get("quantum", DEFAULT_QUANTUM),
            contact_tol=a.get("contact_tol", 1e-9),
            proposals=a.get("proposals", 0),
            non_converged=a.get("non_converged", 0),
            basins=[
                Basin(
                    geometric=b["geometric"],
                    contact=b["contact"],
                    side=b["side"],
                    angle_signature=tuple(b["angle_signature"]),
                    contact_count=b["contact_count"],
                    quench_frequency=b["quench_frequency"],
                    converged_frequency=b.get("converged_frequency", 0),
                    first_seen_seed=b.get("first_seen_seed"),
                )
                for b in a.get("basins", [])
            ],
        )

    @classmethod
    def load_or_new(cls, path: Path, n: int) -> Atlas:
        return cls.load(path) if path.exists() else cls(n=n)

    def merge(self, other: Atlas) -> None:
        """Fold another store of the same `n` into this one.

        Frequencies add and basin sets union, which is what append-only buys: two
        machines running the same census need no reconciliation beyond this.
        """
        if other.n != self.n:
            raise ValueError(f"cannot merge n={other.n} into n={self.n}")
        self.proposals += other.proposals
        self.non_converged += other.non_converged
        index = {b.identity: b for b in self.basins}
        for incoming in other.basins:
            if (mine := index.get(incoming.identity)) is not None:
                mine.quench_frequency += incoming.quench_frequency
                mine.converged_frequency += incoming.converged_frequency
                mine.side = min(mine.side, incoming.side)
            else:
                self.basins.append(incoming)
