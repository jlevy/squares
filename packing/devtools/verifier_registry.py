"""The verifier registry: which verification programs stand behind each evidence entry.

`frontier/verifiers.yaml` holds one entry per verification program the evidence register
names, external or first-party, with the digests or revisions that ran and the paths that
hold its source. Each evidence entry names its programs in `verifiers`, and its existing
`relationship_to_generator` says how the code that verified it stands to the code its
result's producer used (epistemics.md, Confirmation):

- `same-implementation`, or `generator`: the producer's own code, re-run. A replay of it
  establishes reproducibility, not independence.
- `shared-components`: separately written code that reuses named parts of it, listed in
  the entry's `shared_components`.
- `independent-implementation`: code that shares none of it, written from the
  mathematics and the certificate format.

Since 2026-10-14 a first-party program that decides, and a new independent-implementation
entry, carry a structured `independence` record (epistemics.md, The Independence Record):
what the program's authors read, whether it is clean-room, the producer's components it
shares, who wrote it and whether that authorship overlaps the producer's, and, on the
entry, its coverage. Every new replay states its coverage regardless of relation.
`LADDER` names each evidence run's level, from its relation and deciding programs'
records; a sample confirms nothing whole (`sampled`).

This module loads the registry, holds the cross-record rules the JSON Schema cannot state
(`problems`, run by `devtools.validate_schemas`), and gives the views one reading of an
entry's and a result's verification code.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
REGISTRY = ROOT / "frontier" / "verifiers.yaml"

GENERATOR = "generator"
SAME = "same-implementation"
SHARED = "shared-components"
INDEPENDENT = "independent-implementation"
NOT_APPLICABLE = "not-applicable"
UNKNOWN = "unknown-historical"
#: The relations a run of code can hold to its producer's code, from closest to
#: furthest. `generator` and `same-implementation` both mean the producer's own code ran.
RANK = {GENERATOR: 0, SAME: 0, SHARED: 1, INDEPENDENT: 2}
#: The typographic apostrophe the register's prose uses, written as an escape.
APOSTROPHE = "\u2019"
#: How each relation is read beside a rung and after the word "confirmed": the legend the
#: register's views print, and the phrases the prose rule accepts.
LABELS = {
    GENERATOR: f"reproduced with the producer{APOSTROPHE}s code",
    SAME: f"reproduced with the producer{APOSTROPHE}s code",
    SHARED: f"re-implemented, sharing the producer{APOSTROPHE}s components",
    INDEPENDENT: "independently re-implemented",
    NOT_APPLICABLE: "no relation: a proof, a derivation or a report",
    UNKNOWN: "relation not recorded",
}
#: The labels in rank order, once each, for a legend.
LEGEND = tuple(dict.fromkeys(LABELS[relation] for relation in (SAME, SHARED, INDEPENDENT)))
DECIDES = "decides"
EXTERNAL = "external"
FIRST_PARTY = "first-party"
CONFIRMING_ORIGINS = frozenset({"audited-here", "replayed-here", "independently-external"})

#: The independent-implementation entries recorded before 2026-10-02, when the record of
#: what a verifying program's authors read became required, that name no program whose
#: registry entry carries one and carry none of their own. They are exempt by name: the
#: list only shrinks, as each gains a record, and a new entry is never added to it.
GRANDFATHERED_INDEPENDENCE = frozenset(
    {
        "E-basic-area-lower",
        "E-basic-grid-upper",
        "E-bentz13-figure2-audit",
        "E-bentz46-theorem8-audit",
        "E-gobel-family-upper",
        "E-gobel-offcentre-upper",
        "E-gobel-strip-upper",
        "E-lifted-q2-upper",
        "E-lifted-q7-upper",
        "E-n005-gobel-upper",
        "E-n010-gobel-upper",
        "E-n011-h236-rung0-reduction",
        "E-n011-kleddamag-3875-native-parent-core",
        "E-n011-trump-upper",
        "E-n011-wang-li-native-parent-core",
        "E-n012-evand-15680-3951-native-parent-core",
        "E-n012-monotonicity-lower",
        "E-n017-burns-control-decision",
        "E-n017-certified-endpoint",
        "E-n017-guzhou-r012-interval-decision",
        "E-n017-mira-4613-exact-replay",
        "E-n017-mira-4613-interval-decision",
        "E-n029-interval-certified-upper",
        "E-n029-kingbird-numerical",
        "E-n029-orientation-classes",
        "E-n029-schadt-numerical",
        "E-n040-gobel-upper",
        "E-n061-wand125-point-cover-evand-replay-report",
        "E-n082-gobel-l-upper",
        "E-wand125-tools-n11-row-report",
    }
)


#: What a confirming program's authors may have read, in the structured independence
#: record (epistemics.md, The Independence Record); `producer-code` is the one that rules
#: out a clean room.
READ_KINDS = (
    "mathematics",
    "proof-text",
    "specification",
    "certificate-format",
    "producer-code",
    "producer-output",
    "earlier-review",
)
PRODUCER_CODE = "producer-code"
#: The fields of a program's structured record, which an evidence entry carries itself
#: where no deciding program's registry entry carries them.
AUTHORSHIP_FIELDS = ("read", "clean_room", "shares", "written_by", "overlaps_producer")
SAMPLE = "sample"
FULL = "full"
#: The independence ladder (epistemics.md, The Independence Ladder): each level's name,
#: closest to the producer's code first, as the views print it.
LADDER = {
    "reproduced": f"reproduced with the producer{APOSTROPHE}s code",
    "shared": "re-implemented, sharing named components",
    "after-reading": (
        f"independently re-implemented after reading the producer{APOSTROPHE}s code"
    ),
    "clean-room": "independently re-implemented, clean-room",
}

#: The first-party programs that decide, registered before 2026-10-14, when the
#: structured independence record became required of every program written here that
#: decides. They are exempt by name: the list only shrinks, as each gains a record, and
#: a new program is never added to it.
UNSTRUCTURED_PROGRAMS = frozenset(
    {
        "V-assess-frontier-rigidity",
        "V-assess-n40-rigidity",
        "V-assess-n5-rigidity",
        "V-audit-clipped-corner-transfer",
        "V-audit-continuous-pose",
        "V-check-basic-bounds",
        "V-check-half-angle-area",
        "V-check-karakus-strip-measure",
        "V-check-nagamochi-lemma1-counterexample",
        "V-check-rational-witness-independent",
        "V-dilation-corollary",
        "V-five-dot-independent-union",
        "V-green17-interval-audit",
        "V-k3-n17-capture-row-checker",
        "V-k3-n17-root-isolation",
        "V-kingbird29-verify-svg",
        "V-n11-optimality-checkers",
        "V-n12-independent-verifier",
        "V-n17-catalogue-polynomial",
        "V-n17-endpoint-checkers",
        "V-n17-weighted-instrument",
        "V-optimal-moduli",
        "V-rectangle-ceiling",
        "V-replay-owner-footprint-cover",
        "V-review-trump-local-theorem",
        "V-ryxu-undilated-n51-independent",
        "V-screen-translation-escape",
        "V-sqpack-cover",
        "V-sqpack-fractional-exact",
        "V-sqpack-fractional-interval",
        "V-sqpack-parent-core-native",
        "V-sqpack-threshold-exact",
        "V-sqpack-threshold-interval",
        "V-sqpack-verify",
        "V-sqverify-fast",
        "V-trump11-fixed-angle-tree-check",
        "V-trump11-isolation-radius",
        "V-trump11-tangent-cones",
        "V-upper-bound-intervals",
        "V-upper-bound-promotion",
        "V-wall-owner-containment",
        "V-wall-owner-footprints",
    }
)

#: The independent-implementation evidence entries recorded before 2026-10-14, when the
#: structured independence record, with its coverage, became required of every new one.
#: They are exempt by name, and the list only shrinks, as GRANDFATHERED_INDEPENDENCE does.
UNSTRUCTURED_EVIDENCE = frozenset(
    {
        "E-barnett-505-exact-feasibility",
        "E-basic-area-lower",
        "E-basic-grid-upper",
        "E-bentz13-figure2-audit",
        "E-bentz46-theorem8-audit",
        "E-couzo-451-exact-feasibility",
        "E-couzo-460-followup-exact-feasibility",
        "E-couzo-476-exact-feasibility",
        "E-couzo-488-exact-feasibility",
        "E-couzo-506-exact-feasibility",
        "E-deleeuw-483-exact-feasibility",
        "E-evand-399-exact-feasibility",
        "E-evand-465-record-hunt-exact-feasibility",
        "E-evand-489-exact-feasibility",
        "E-evand-exact-ceilings-2026-10-05-exact-replay",
        "E-evand-exact-optima-2026-10-05-exact-replay",
        "E-evand-regularized-exact-feasibility",
        "E-evand-trio126-exact-feasibility",
        "E-fang-484-exact-feasibility",
        "E-franciscouzo-2026-09-27-exact-replay",
        "E-franciscouzo-2026-09-27-interval-replay",
        "E-franciscouzo-2026-10-03-exact-replay",
        "E-franciscouzo-2026-10-03-interval-replay",
        "E-gobel-family-upper",
        "E-gobel-offcentre-upper",
        "E-gobel-strip-upper",
        "E-green17-interval-audit",
        "E-gupta-438-exact-feasibility",
        "E-k2m3-wand125-valid7-independent",
        "E-k2m4-wand125-validtilt9-report",
        "E-karakus-strip-measure-interval",
        "E-lifted-q2-upper",
        "E-lifted-q7-upper",
        "E-mishapolk-470-exact-feasibility",
        "E-n005-gobel-upper",
        "E-n010-gobel-upper",
        "E-n011-five-dot-independent-union",
        "E-n011-h236-rung0-reduction",
        "E-n011-kleddamag-3875-native-parent-core",
        "E-n011-trump-local-theorem-first-clause",
        "E-n011-trump-upper",
        "E-n011-wang-li-native-parent-core",
        "E-n012-evand-15680-3951-native-parent-core",
        "E-n012-independent-verifier",
        "E-n012-levy-15680000-3949423-native-parent-core",
        "E-n012-monotonicity-lower",
        "E-n012-squarepacker-31360-7901-native-parent-core",
        "E-n012-squarepacker-7943-2000-native-parent-core",
        "E-n017-burns-control-decision",
        "E-n017-certified-endpoint",
        "E-n017-guzhou-r012-interval-decision",
        "E-n017-kleddamag-rational-upper",
        "E-n017-massaccesi-h052-agreement",
        "E-n017-mira-4613-exact-replay",
        "E-n017-mira-4613-interval-decision",
        "E-n017-overbeck-statement-root-independent",
        "E-n018-wand125-mixed-4704-sqverify-fast-replay",
        "E-n019-wand125-mixed-48229-sqverify-fast-replay",
        "E-n019-wand125-rect-48175-sqverify-fast-replay",
        "E-n020-wand125-rect-48975-sqverify-fast-replay",
        "E-n020-wand125-rect-49-sqverify-fast-replay",
        "E-n026-wand125-rect-55325-sqverify-fast-replay",
        "E-n027-wand125-rect-5635-sqverify-fast-replay",
        "E-n028-wand125-rect-57225-sqverify-fast-replay",
        "E-n029-interval-certified-upper",
        "E-n029-kingbird-numerical",
        "E-n029-orientation-classes",
        "E-n029-schadt-numerical",
        "E-n029-schadt-rational-upper",
        "E-n029-wand125-mixed-581-sqverify-fast-replay",
        "E-n029-wand125-rect-57975-sqverify-fast-replay",
        "E-n030-wand125-rect-5875-sqverify-fast-replay",
        "E-n031-wand125-rect-59525-sqverify-fast-replay",
        "E-n038-wand125-rect-6545-sqverify-fast-replay",
        "E-n039-wand125-rect-6635-sqverify-fast-replay",
        "E-n040-gobel-upper",
        "E-n040-guzhou-clipped-corner-finite-audit",
        "E-n040-guzhou-continuous-pose-crate-axis",
        "E-n040-guzhou-continuous-pose-finite-audit",
        "E-n040-wand125-rect-67-sqverify-fast-replay",
        "E-n041-wand125-rect-676-sqverify-fast-replay",
        "E-n042-wand125-mixed-68475-sqverify-fast-replay",
        "E-n042-wand125-rect-6815-sqverify-fast-replay",
        "E-n042-wand125-rect-68275-sqverify-fast-replay",
        "E-n043-wand125-mixed-69075-sqverify-fast-replay",
        "E-n043-wand125-rect-68875-sqverify-fast-replay",
        "E-n044-wand125-mixed-69725-sqverify-fast-replay",
        "E-n044-wand125-rect-69425-sqverify-fast-replay",
        "E-n051-wand125-mixed-746-sqverify-fast-replay",
        "E-n051-wand125-mixed-747-sqverify-fast-replay",
        "E-n052-wand125-mixed-755-sqverify-fast-replay",
        "E-n053-wand125-mixed-76275-sqverify-fast-replay",
        "E-n053-wand125-rect-76075-sqverify-fast-replay",
        "E-n054-wand125-mixed-7685-sqverify-fast-replay",
        "E-n054-wand125-rect-76725-sqverify-fast-replay",
        "E-n055-wand125-mixed-7728-sqverify-fast-replay",
        "E-n055-wand125-rect-77125-sqverify-fast-replay",
        "E-n056-wand125-mixed-78025-sqverify-fast-replay",
        "E-n056-wand125-rect-77825-sqverify-fast-replay",
        "E-n057-wand125-mixed-78725-sqverify-fast-replay",
        "E-n058-wand125-mixed-7905-sqverify-fast-replay",
        "E-n058-wand125-mixed-7935-sqverify-fast-replay",
        "E-n061-wand125-point-cover-evand-replay-report",
        "E-n066-wand125-mixed-843-sqverify-fast-replay",
        "E-n066-wand125-rect-8385-sqverify-fast-replay",
        "E-n067-wand125-mixed-8475-sqverify-fast-replay",
        "E-n067-wand125-mixed-848-sqverify-fast-replay",
        "E-n068-wand125-rect-851-sqverify-fast-replay",
        "E-n069-ellsworth-2026-09-exact-replay",
        "E-n069-wand125-mixed-8612-sqverify-fast-replay",
        "E-n069-wand125-mixed-862-sqverify-fast-replay",
        "E-n069-wand125-rect-8585-sqverify-fast-replay",
        "E-n070-wand125-mixed-86475-sqverify-fast-replay",
        "E-n070-wand125-mixed-86575-sqverify-fast-replay",
        "E-n070-wand125-rect-8625-sqverify-fast-replay",
        "E-n070-wand125-rect-86275-sqverify-fast-replay",
        "E-n071-wand125-mixed-8705-sqverify-fast-replay",
        "E-n071-wand125-mixed-8721-sqverify-fast-replay",
        "E-n072-wand125-mixed-876-sqverify-fast-replay",
        "E-n073-wand125-mixed-8809-sqverify-fast-replay",
        "E-n073-wand125-mixed-8813-sqverify-fast-replay",
        "E-n074-wand125-mixed-88675-sqverify-fast-replay",
        "E-n074-wand125-rect-88475-sqverify-fast-replay",
        "E-n075-wand125-mixed-892-sqverify-fast-replay",
        "E-n075-wand125-mixed-894-sqverify-fast-replay",
        "E-n075-wand125-rect-89-sqverify-fast-replay",
        "E-n076-wand125-mixed-896-sqverify-fast-replay",
        "E-n076-wand125-mixed-8965-sqverify-fast-replay",
        "E-n076-wand125-rect-8925-sqverify-fast-replay",
        "E-n082-gobel-l-upper",
        "E-n083-chang-2026-09-exact-replay",
        "E-n083-wand125-mixed-937-sqverify-fast-replay",
        "E-n084-wand125-mixed-94075-sqverify-fast-replay",
        "E-n084-wand125-mixed-9411-sqverify-fast-replay",
        "E-n085-wand125-mixed-946-sqverify-fast-replay",
        "E-n086-wand125-mixed-950-sqverify-fast-replay",
        "E-n086-wand125-mixed-9503-sqverify-fast-replay",
        "E-n086-wand125-rect-9365-sqverify-fast-replay",
        "E-n087-chang-2026-09-exact-replay",
        "E-n087-wand125-mixed-948-sqverify-fast-replay",
        "E-n087-wand125-mixed-955-sqverify-fast-replay",
        "E-n087-wand125-mixed-958-sqverify-fast-replay",
        "E-n087-wand125-rect-941-sqverify-fast-replay",
        "E-n088-wand125-mixed-960-sqverify-fast-replay",
        "E-n088-wand125-mixed-96125-sqverify-fast-replay",
        "E-n088-wand125-mixed-962-sqverify-fast-replay",
        "E-n088-wand125-rect-94775-sqverify-fast-replay",
        "E-n089-wand125-mixed-965-sqverify-fast-replay",
        "E-n089-wand125-rect-9565-sqverify-fast-replay",
        "E-n090-wand125-mixed-9725-sqverify-fast-replay",
        "E-n090-wand125-mixed-973-sqverify-fast-replay",
        "E-n090-wand125-rect-95775-sqverify-fast-replay",
        "E-n091-wand125-mixed-970-sqverify-fast-replay",
        "E-n091-wand125-mixed-975-sqverify-fast-replay",
        "E-n091-wand125-mixed-97625-sqverify-fast-replay",
        "E-n092-wand125-mixed-975-sqverify-fast-replay",
        "E-n092-wand125-mixed-977-sqverify-fast-replay",
        "E-n093-wand125-mixed-986-sqverify-fast-replay",
        "E-n093-wand125-mixed-988-sqverify-fast-replay",
        "E-n093-wand125-rect-97225-sqverify-fast-replay",
        "E-n094-wand125-mixed-992-sqverify-fast-replay",
        "E-n094-wand125-mixed-994-sqverify-fast-replay",
        "E-n094-wand125-mixed-995-sqverify-fast-replay",
        "E-n094-wand125-rect-9805-sqverify-fast-replay",
        "E-n095-wand125-mixed-996-sqverify-fast-replay",
        "E-n095-wand125-mixed-9965-sqverify-fast-replay",
        "E-n095-wand125-rect-98518-sqverify-fast-replay",
        "E-n096-wand125-mixed-996-sqverify-fast-replay",
        "E-n096-wand125-mixed-997-sqverify-fast-replay",
        "E-n211-de-winter-exact-replay",
        "E-n211-de-winter-interval-replay",
        "E-nagamochi-lemma1-counterexample",
        "E-ostashev-501-exact-feasibility",
        "E-pingyou-503-exact-feasibility",
        "E-pingyou-504-exact-feasibility",
        "E-rehwaldt-couzo-refinements-2026-10-07-exact-replay",
        "E-ryxu-432-radical-n51-feasibility",
        "E-ryxu-432-rational-feasibility",
        "E-squish-481-exact-feasibility",
        "E-squish-500-exact-feasibility",
        "E-squish-n153-2026-10-07-exact-replay",
        "E-squish-second-update-2026-10-07-exact-replay",
        "E-squish-ten-packings-2026-10-07-exact-replay",
        "E-squish-update-2026-10-07-exact-replay",
        "E-wand125-tools-ceiling-certificates",
        "E-wand125-tools-n11-row-report",
    }
)


#: Replays recorded before 2026-10-14 without coverage. Only removal is allowed.
UNCOVERED_REPLAYS = frozenset(
    {
        "E-barnett-505-exact-feasibility",
        "E-basic-area-lower",
        "E-basic-grid-upper",
        "E-bentz13-figure2-audit",
        "E-bentz46-theorem8-audit",
        "E-chelokot-square-minus-two-lean",
        "E-couzo-451-exact-feasibility",
        "E-couzo-460-followup-exact-feasibility",
        "E-couzo-476-exact-feasibility",
        "E-couzo-488-exact-feasibility",
        "E-couzo-506-exact-feasibility",
        "E-deleeuw-483-exact-feasibility",
        "E-evand-399-exact-feasibility",
        "E-evand-465-record-hunt-exact-feasibility",
        "E-evand-489-exact-feasibility",
        "E-evand-exact-ceilings-2026-10-05-exact-replay",
        "E-evand-exact-ceilings-2026-10-05-source-replay",
        "E-evand-exact-optima-2026-10-05-exact-replay",
        "E-evand-exact-optima-2026-10-05-source-replay",
        "E-evand-regularized-exact-feasibility",
        "E-evand-trio126-exact-feasibility",
        "E-fang-484-exact-feasibility",
        "E-fractional-interval-decision",
        "E-franciscouzo-2026-09-27-exact-replay",
        "E-franciscouzo-2026-09-27-interval-replay",
        "E-franciscouzo-2026-10-03-exact-replay",
        "E-franciscouzo-2026-10-03-interval-replay",
        "E-gobel-family-upper",
        "E-gobel-offcentre-upper",
        "E-gobel-strip-upper",
        "E-green17-interval-audit",
        "E-green17-sixteen-point-lower",
        "E-gupta-438-exact-feasibility",
        "E-k2m3-evand-bentz-lean-build",
        "E-k2m3-evand-valid7-qx2-replay",
        "E-k2m3-wand125-valid7-independent",
        "E-k2m4-evand-bentz4-lean-build",
        "E-karakus-strip-measure-interval",
        "E-lifted-q2-upper",
        "E-lifted-q7-upper",
        "E-mishapolk-470-exact-feasibility",
        "E-n005-fixed-side-local-rigidity",
        "E-n005-gobel-upper",
        "E-n005-second-order-rigidity",
        "E-n010-gobel-upper",
        "E-n011-corner-class-96-25-exact-decision",
        "E-n011-corner-class-96-25-interval-decision",
        "E-n011-five-dot-full-net",
        "E-n011-five-dot-independent-union",
        "E-n011-fractional-certificate",
        "E-n011-fractional-dilation-limit",
        "E-n011-fractional-net1440-certificate",
        "E-n011-fractional-net1440-dilation-limit",
        "E-n011-fractional-net1440-interval-decision",
        "E-n011-fractional-net720-certificate",
        "E-n011-fractional-net720-dilation-limit",
        "E-n011-global-optimality-independent",
        "E-n011-h236-rung0-reduction",
        "E-n011-kleddamag-3875-native-parent-core",
        "E-n011-kleddamag-3875-source-replay",
        "E-n011-lean-statement-closure-build",
        "E-n011-optimum-uniqueness",
        "E-n011-repaired-lower",
        "E-n011-threshold-certificate",
        "E-n011-threshold-interval-decision",
        "E-n011-threshold-net1440-certificate",
        "E-n011-threshold-net1440-dilation-limit",
        "E-n011-threshold-net1440-interval-decision",
        "E-n011-threshold-net2880-certificate",
        "E-n011-threshold-net2880-dilation-limit",
        "E-n011-threshold-net2880-interval-decision",
        "E-n011-threshold-net720-certificate",
        "E-n011-threshold-net720-dilation-limit",
        "E-n011-trump-isolation-radius",
        "E-n011-trump-local-rigidity",
        "E-n011-trump-local-theorem-first-clause",
        "E-n011-trump-upper",
        "E-n011-wall-owner-containment",
        "E-n011-wall-owner-footprints",
        "E-n011-wang-li-native-parent-core",
        "E-n011-wang-li-source-replay",
        "E-n012-evand-15680-3951-native-parent-core",
        "E-n012-evand-15680-3951-source-replay",
        "E-n012-fractional-certificate",
        "E-n012-independent-verifier",
        "E-n012-levy-15680000-3949423-audit",
        "E-n012-levy-15680000-3949423-generator",
        "E-n012-levy-15680000-3949423-native-parent-core",
        "E-n012-levy-15680000-3949423-source-replay",
        "E-n012-monotonicity-lower",
        "E-n012-squarepacker-31360-7901-native-parent-core",
        "E-n012-squarepacker-31360-7901-source-replay",
        "E-n012-squarepacker-7943-2000-audit",
        "E-n012-squarepacker-7943-2000-native-parent-core",
        "E-n012-squarepacker-7943-2000-source-replay",
        "E-n013-evand-casefree-cover-lean-kernel",
        "E-n013-evand-casefree-cover-zmx2-replay",
        "E-n017-anabologyco-weighted-certificate",
        "E-n017-burns-control-decision",
        "E-n017-burns-source-replay",
        "E-n017-catalogue-polynomial-identity",
        "E-n017-certified-endpoint",
        "E-n017-fort-point-certificate-replay",
        "E-n017-fractional-certificate",
        "E-n017-guzhou-r012-interval-decision",
        "E-n017-guzhou-r012-source-replay",
        "E-n017-guzhou-r052-source-replay",
        "E-n017-guzhou-r067-source-replay",
        "E-n017-guzhou-r068-source-replay",
        "E-n017-guzhou-r071-source-replay",
        "E-n017-kleddamag-461300-99853-source-replay",
        "E-n017-kleddamag-4640020-source-replay",
        "E-n017-kleddamag-466001-source-replay",
        "E-n017-kleddamag-rational-upper",
        "E-n017-massaccesi-h052-agreement",
        "E-n017-massaccesi-source-replay",
        "E-n017-mira-4613-exact-replay",
        "E-n017-mira-4613-interval-decision",
        "E-n017-mira-point-certificate-replay",
        "E-n017-overbeck-candidate-check-py-replay",
        "E-n017-overbeck-statement-root-independent",
        "E-n018-fractional-certificate",
        "E-n018-t028-fractional-certificate",
        "E-n018-t029-fractional-certificate",
        "E-n018-t030-fractional-certificate",
        "E-n018-wand125-mixed-470-source-replay",
        "E-n018-wand125-mixed-4704-source-replay",
        "E-n018-wand125-mixed-4704-sqverify-fast-replay",
        "E-n018-wand125-mixed-4705-sqverify-fast-replay",
        "E-n019-wand125-mixed-48229-sqverify-fast-replay",
        "E-n019-wand125-mixed-4825-sqverify-fast-replay",
        "E-n019-wand125-rect-48175-sqverify-fast-replay",
        "E-n020-fractional-certificate",
        "E-n020-fractional-certificate-97-20",
        "E-n020-wand125-mixed-4905-sqverify-fast-replay",
        "E-n020-wand125-rect-48975-sqverify-fast-replay",
        "E-n020-wand125-rect-49-sqverify-fast-replay",
        "E-n021-evand-5000-1001-source-replay",
        "E-n021-evand-mixed-cover-zmx2-replay",
        "E-n021-fractional-certificate-122-25",
        "E-n021-wand125-point-endpoint-source-replay",
        "E-n026-wand125-mixed-5545-sqverify-fast-replay",
        "E-n026-wand125-rect-55325-sqverify-fast-replay",
        "E-n027-wand125-mixed-56435-sqverify-fast-replay",
        "E-n027-wand125-rect-5635-sqverify-fast-replay",
        "E-n028-wand125-mixed-5735-sqverify-fast-replay",
        "E-n028-wand125-rect-57225-sqverify-fast-replay",
        "E-n029-interval-certified-upper",
        "E-n029-kingbird-numerical",
        "E-n029-orientation-classes",
        "E-n029-schadt-numerical",
        "E-n029-schadt-rational-upper",
        "E-n029-wand125-mixed-581-sqverify-fast-replay",
        "E-n029-wand125-rect-57975-sqverify-fast-replay",
        "E-n030-wand125-mixed-58835-sqverify-fast-replay",
        "E-n030-wand125-rect-5875-sqverify-fast-replay",
        "E-n031-wand125-rect-59525-sqverify-fast-replay",
        "E-n032-evand-closed-cover-source-run",
        "E-n032-evand-closed-cover-zmx2-replay",
        "E-n032-evand-zmx2-full-sym-replay",
        "E-n037-wand125-mixed-644-source-replay",
        "E-n038-wand125-rect-6545-sqverify-fast-replay",
        "E-n039-wand125-mixed-665-sqverify-fast-replay",
        "E-n039-wand125-rect-6635-sqverify-fast-replay",
        "E-n040-first-order-flexibility",
        "E-n040-gobel-upper",
        "E-n040-guzhou-clipped-corner-finite-audit",
        "E-n040-guzhou-clipped-corner-sqverify-fast-replay",
        "E-n040-guzhou-continuous-pose-crate-axis",
        "E-n040-guzhou-continuous-pose-finite-audit",
        "E-n040-guzhou-continuous-pose-kernel-replay",
        "E-n040-wand125-rect-67-sqverify-fast-replay",
        "E-n041-wand125-mixed-6775-sqverify-fast-replay",
        "E-n041-wand125-rect-676-sqverify-fast-replay",
        "E-n042-wand125-mixed-68475-sqverify-fast-replay",
        "E-n042-wand125-rect-6815-sqverify-fast-replay",
        "E-n042-wand125-rect-68275-sqverify-fast-replay",
        "E-n043-wand125-mixed-69075-sqverify-fast-replay",
        "E-n043-wand125-rect-68875-sqverify-fast-replay",
        "E-n044-wand125-mixed-69725-sqverify-fast-replay",
        "E-n044-wand125-rect-69425-sqverify-fast-replay",
        "E-n045-evand-mixed-cover-zmx2-replay",
        "E-n045-wand125-point-cover-source-replay",
        "E-n050-wand125-mixed-740-source-replay",
        "E-n051-wand125-mixed-746-sqverify-fast-replay",
        "E-n051-wand125-mixed-747-sqverify-fast-replay",
        "E-n052-wand125-mixed-755-sqverify-fast-replay",
        "E-n053-wand125-mixed-76275-sqverify-fast-replay",
        "E-n053-wand125-rect-76075-sqverify-fast-replay",
        "E-n054-wand125-mixed-7685-sqverify-fast-replay",
        "E-n054-wand125-rect-76725-sqverify-fast-replay",
        "E-n055-wand125-mixed-7728-sqverify-fast-replay",
        "E-n055-wand125-rect-77125-sqverify-fast-replay",
        "E-n056-wand125-mixed-78025-sqverify-fast-replay",
        "E-n056-wand125-rect-77825-sqverify-fast-replay",
        "E-n057-wand125-mixed-78725-sqverify-fast-replay",
        "E-n058-wand125-mixed-7905-sqverify-fast-replay",
        "E-n058-wand125-mixed-7935-sqverify-fast-replay",
        "E-n059-wand125-mixed-cover-zmx2-replay",
        "E-n060-evand-mixed-cover-zmx2-replay",
        "E-n061-wand125-point-cover-zmx2-replay",
        "E-n065-wand125-mixed-835-source-replay",
        "E-n066-wand125-mixed-842-source-replay",
        "E-n066-wand125-mixed-843-sqverify-fast-replay",
        "E-n066-wand125-rect-8385-sqverify-fast-replay",
        "E-n067-wand125-mixed-8475-sqverify-fast-replay",
        "E-n067-wand125-mixed-848-sqverify-fast-replay",
        "E-n068-wand125-rect-851-sqverify-fast-replay",
        "E-n069-ellsworth-2026-09-exact-replay",
        "E-n069-wand125-mixed-8612-sqverify-fast-replay",
        "E-n069-wand125-mixed-862-sqverify-fast-replay",
        "E-n069-wand125-rect-8585-sqverify-fast-replay",
        "E-n070-wand125-mixed-86475-sqverify-fast-replay",
        "E-n070-wand125-mixed-86575-sqverify-fast-replay",
        "E-n070-wand125-rect-8625-sqverify-fast-replay",
        "E-n070-wand125-rect-86275-sqverify-fast-replay",
        "E-n071-wand125-mixed-8705-sqverify-fast-replay",
        "E-n071-wand125-mixed-8721-sqverify-fast-replay",
        "E-n072-wand125-mixed-876-sqverify-fast-replay",
        "E-n073-wand125-mixed-8809-sqverify-fast-replay",
        "E-n073-wand125-mixed-8813-sqverify-fast-replay",
        "E-n074-wand125-mixed-88675-sqverify-fast-replay",
        "E-n074-wand125-rect-88475-sqverify-fast-replay",
        "E-n075-wand125-mixed-892-sqverify-fast-replay",
        "E-n075-wand125-mixed-894-sqverify-fast-replay",
        "E-n075-wand125-rect-89-sqverify-fast-replay",
        "E-n076-wand125-mixed-894-source-replay",
        "E-n076-wand125-mixed-896-sqverify-fast-replay",
        "E-n076-wand125-mixed-8965-sqverify-fast-replay",
        "E-n076-wand125-rect-8925-sqverify-fast-replay",
        "E-n077-wand125-mixed-cover-zmx2-replay",
        "E-n082-gobel-l-upper",
        "E-n082-wand125-linear-932-source-replay",
        "E-n083-chang-2026-09-exact-replay",
        "E-n083-wand125-linear-935-source-replay",
        "E-n083-wand125-mixed-937-source-replay",
        "E-n083-wand125-mixed-937-sqverify-fast-replay",
        "E-n084-wand125-mixed-940-source-replay",
        "E-n084-wand125-mixed-94075-sqverify-fast-replay",
        "E-n084-wand125-mixed-9411-sqverify-fast-replay",
        "E-n085-wand125-mixed-942-source-replay",
        "E-n085-wand125-mixed-946-source-replay",
        "E-n085-wand125-mixed-946-sqverify-fast-replay",
        "E-n086-wand125-mixed-950-sqverify-fast-replay",
        "E-n086-wand125-mixed-9503-sqverify-fast-replay",
        "E-n086-wand125-rect-9365-sqverify-fast-replay",
        "E-n087-chang-2026-09-exact-replay",
        "E-n087-wand125-mixed-948-source-replay",
        "E-n087-wand125-mixed-948-sqverify-fast-replay",
        "E-n087-wand125-mixed-955-sqverify-fast-replay",
        "E-n087-wand125-mixed-958-sqverify-fast-replay",
        "E-n087-wand125-rect-941-sqverify-fast-replay",
        "E-n088-wand125-mixed-960-sqverify-fast-replay",
        "E-n088-wand125-mixed-96125-sqverify-fast-replay",
        "E-n088-wand125-mixed-962-sqverify-fast-replay",
        "E-n088-wand125-rect-94775-sqverify-fast-replay",
        "E-n089-wand125-mixed-965-sqverify-fast-replay",
        "E-n089-wand125-rect-9565-sqverify-fast-replay",
        "E-n090-wand125-mixed-960-source-replay",
        "E-n090-wand125-mixed-9725-sqverify-fast-replay",
        "E-n090-wand125-mixed-973-sqverify-fast-replay",
        "E-n090-wand125-rect-95775-sqverify-fast-replay",
        "E-n091-wand125-mixed-970-source-replay",
        "E-n091-wand125-mixed-970-sqverify-fast-replay",
        "E-n091-wand125-mixed-975-sqverify-fast-replay",
        "E-n091-wand125-mixed-97625-sqverify-fast-replay",
        "E-n092-wand125-mixed-969-source-replay",
        "E-n092-wand125-mixed-975-source-replay",
        "E-n092-wand125-mixed-975-sqverify-fast-replay",
        "E-n092-wand125-mixed-977-sqverify-fast-replay",
        "E-n093-wand125-mixed-986-sqverify-fast-replay",
        "E-n093-wand125-mixed-988-sqverify-fast-replay",
        "E-n093-wand125-rect-97225-sqverify-fast-replay",
        "E-n094-wand125-mixed-992-sqverify-fast-replay",
        "E-n094-wand125-mixed-994-sqverify-fast-replay",
        "E-n094-wand125-mixed-995-sqverify-fast-replay",
        "E-n094-wand125-rect-9805-sqverify-fast-replay",
        "E-n095-wand125-mixed-996-sqverify-fast-replay",
        "E-n095-wand125-mixed-9965-sqverify-fast-replay",
        "E-n095-wand125-rect-98518-sqverify-fast-replay",
        "E-n096-wand125-mixed-996-source-replay",
        "E-n096-wand125-mixed-996-sqverify-fast-replay",
        "E-n096-wand125-mixed-997-sqverify-fast-replay",
        "E-n101-wand125-linear-1028-source-replay",
        "E-n211-de-winter-exact-replay",
        "E-n211-de-winter-interval-replay",
        "E-nagamochi-lemma1-counterexample",
        "E-ostashev-501-exact-feasibility",
        "E-perfect-square-tiling-rigid",
        "E-pingyou-503-exact-feasibility",
        "E-pingyou-504-exact-feasibility",
        "E-rehwaldt-couzo-refinements-2026-10-07-exact-replay",
        "E-rehwaldt-n68-refinement-2026-10-07-exact-replay",
        "E-ryxu-432-radical-n51-feasibility",
        "E-ryxu-432-rational-feasibility",
        "E-side2-center-lower",
        "E-squish-481-exact-feasibility",
        "E-squish-500-exact-feasibility",
        "E-squish-n153-2026-10-07-exact-replay",
        "E-squish-second-update-2026-10-07-exact-replay",
        "E-squish-ten-packings-2026-10-07-exact-replay",
        "E-squish-update-2026-10-07-exact-replay",
        "E-tokoharu-density-source-replay",
        "E-translation-escape-not-rigid",
        "E-wand125-n052-derived-lower",
        "E-wand125-n068-derived-lower",
        "E-wand125-point-source-replay",
        "E-wand125-rectangle-2026-09-28-source-replay",
        "E-wand125-rectangle-2026-10-01-source-replay",
        "E-wand125-rectangle-2026-10-02-source-replay",
        "E-wand125-rectangle-source-replay",
        "E-wand125-tools-ceiling-certificates",
        "E-wand125-tools-n11-row-replay",
    }
)


@dataclass(frozen=True)
class Verifier:
    """One registry entry, as the views read it."""

    id: str
    program: str
    author: str
    provenance: str
    role: str
    record: Mapping[str, Any]

    @property
    def decides(self) -> bool:
        return self.role == DECIDES


def load(path: Path = REGISTRY) -> dict[str, Verifier]:
    """The registry's verifiers by id, in file order."""
    document = safe_load(path.read_text(encoding="utf-8"))
    return {
        entry["id"]: Verifier(
            id=entry["id"],
            program=entry["program"],
            author=entry["author"],
            provenance=entry["provenance"],
            role=entry["role"],
            record=entry,
        )
        for entry in document["verifiers"]
    }


def _path_problem(path: str) -> str | None:
    pure = PurePosixPath(path)
    if pure.is_absolute() or pure.as_posix() != path or ".." in pure.parts:
        return "is not a normalized repository-relative path"
    if not (REPO / pure).exists():
        return "does not exist"
    return None


def _mapping(value: Any) -> Mapping[str, Any]:
    """A structured record's mapping, or no facts while schema diagnostics are emitted."""
    return value if isinstance(value, Mapping) else {}


def sampled(entry: Mapping[str, Any]) -> bool:
    """Whether an evidence entry's run is a sample: it decides the instances it ran and
    nothing about the others, so it derives no rung. Invalid coverage is excluded too,
    leaving shape diagnostics to the schema (epistemics.md, The Independence Ladder)."""
    raw = entry.get("independence")
    if "independence" in entry and not isinstance(raw, Mapping):
        return True
    record = _mapping(raw)
    coverage = record.get("coverage")
    if "coverage" in record and not isinstance(coverage, Mapping):
        return True
    return _mapping(coverage).get("extent") == SAMPLE


def ladder_level(entry: Mapping[str, Any], verifiers: Mapping[str, Verifier]) -> str | None:
    """An evidence run's relation, using only its deciding programs' authorship."""
    relation = entry.get("relationship_to_generator")
    if relation in {SAME, GENERATOR, SHARED}:
        return "shared" if relation == SHARED else "reproduced"
    if relation != INDEPENDENT:
        return None
    own = _mapping(entry.get("independence"))
    records = [
        _mapping(verifiers[v].record.get("independence")) or own
        for v in entry.get("verifiers") or []
        if v in verifiers and verifiers[v].decides
    ]
    if own.get("shares") or any(record.get("shares") for record in records):
        return "shared"
    if (records and all(record.get("clean_room") is True for record in records)) or (
        not records and own.get("clean_room") is True
    ):
        return "clean-room"
    if any(PRODUCER_CODE in (record.get("read") or []) for record in records or [own]):
        return "after-reading"
    return None


def ladder_label(entry: Mapping[str, Any], verifiers: Mapping[str, Verifier]) -> str:
    """The entry's ladder level, or its non-computational relation label."""
    return LADDER.get(
        ladder_level(entry, verifiers) or "",
        LABELS[INDEPENDENT]
        if entry.get("relationship_to_generator") == INDEPENDENT
        else SHORT_LABELS.get(str(entry.get("relationship_to_generator")), "-"),
    )


def coverage_line(entry: Mapping[str, Any]) -> str:
    """Coverage as a readable table cell, including sample counts and the named unit."""
    coverage = _mapping(_mapping(entry.get("independence")).get("coverage"))
    if not coverage:
        return "not recorded"
    extent = str(coverage.get("extent", "not recorded"))
    if "checked" in coverage and "of" in coverage:
        extent += f", {coverage['checked']:,} of {coverage['of']:,}"
    return extent + ": " + " ".join(str(coverage.get("unit", "")).split())


def record_problems(owner: str, record: Mapping[str, Any]) -> list[str]:
    """What contradicts itself inside one structured independence record: a clean room
    whose authors read the producer's code or that shares its components, and a coverage
    whose count does not fit its extent."""
    record = _mapping(record)
    problems: list[str] = []
    if record.get("clean_room") is True and PRODUCER_CODE in (record.get("read") or []):
        problems.append(
            f"{owner}: its independence record says clean_room, but its authors read the "
            f"producer{APOSTROPHE}s code"
        )
    if record.get("clean_room") is True and record.get("shares"):
        problems.append(
            f"{owner}: its independence record says clean_room, but it shares the "
            f"producer{APOSTROPHE}s components"
        )
    overlap = _mapping(record.get("overlaps_producer"))
    if record.get("shares") and overlap.get("separate_code") is True:
        problems.append(
            f"{owner}: its independence record says separate_code, but it shares the "
            f"producer{APOSTROPHE}s components"
        )
    if record.get("clean_room") is True and overlap.get("separate_code") is False:
        problems.append(
            f"{owner}: its independence record says clean_room, but not separate_code"
        )
    coverage = _mapping(record.get("coverage"))
    checked, of = coverage.get("checked"), coverage.get("of")
    if isinstance(checked, int) and isinstance(of, int):
        if coverage.get("extent") == SAMPLE and checked < 1:
            problems.append(f"{owner}: a sample checks at least one instance")
        if coverage.get("extent") == SAMPLE and checked >= of:
            problems.append(f"{owner}: a sample checks fewer than all, not {checked} of {of}")
        if coverage.get("extent") == FULL and checked != of:
            problems.append(f"{owner}: full coverage checks all, not {checked} of {of}")
    return problems


def registry_problems(verifiers: Mapping[str, Verifier], ids: Sequence[str]) -> list[str]:
    """What is wrong with the registry by itself: duplicate ids; source, version and
    independence-record paths that do not resolve; a structured independence record that
    contradicts itself; and a first-party program that decides with no structured record,
    unless it is exempt by name."""
    problems = [
        f"verifiers: duplicate id {verifier_id}"
        for verifier_id in sorted({i for i in ids if ids.count(i) > 1})
    ]
    for verifier in verifiers.values():
        record = verifier.record
        if structured := record.get("independence"):
            problems.extend(record_problems(f"verifiers: {verifier.id}", structured))
        elif (
            verifier.provenance == FIRST_PARTY
            and verifier.decides
            and verifier.id not in UNSTRUCTURED_PROGRAMS
        ):
            problems.append(
                f"verifiers: {verifier.id} is a first-party program that decides, and "
                "carries no structured independence record (epistemics.md, The "
                "Independence Record)"
            )
        paths = [
            *record.get("source", []),
            *(version["path"] for version in record.get("versions", []) if "path" in version),
        ]
        if "independence_record" in record:
            paths.append(record["independence_record"])
        problems.extend(
            f"verifiers: {verifier.id} names {path}, which {problem}"
            for path in paths
            if (problem := _path_problem(path))
        )
    return problems


def independence_recorded(entry: Mapping[str, Any], verifiers: Mapping[str, Verifier]) -> bool:
    """Whether an independent implementation names the record of what its authors read:
    its own `independence_record`, or a deciding program's in the registry."""
    if entry.get("independence_record"):
        return True
    return any(
        verifiers[v].decides and "independence_record" in verifiers[v].record
        for v in entry.get("verifiers") or []
        if v in verifiers
    )


def evidence_problems(
    evidence: Iterable[Mapping[str, Any]], verifiers: Mapping[str, Verifier]
) -> list[str]:
    """What is wrong with the evidence entries' verifier fields, given the registry: every
    id resolves; a replay names a program that decides, since a premise check never
    decides alone, unless the entry claims no relation to the producer's decision
    (`not-applicable`), which is what a premise check recorded on its own is; an
    independent implementation names the record of what its authors
    read, unless it is grandfathered; an entry's own independence record resolves."""
    problems: list[str] = []
    for entry in evidence:
        eid = str(entry.get("id", "<unknown evidence>"))
        named = list(entry.get("verifiers") or [])
        unknown = [verifier_id for verifier_id in named if verifier_id not in verifiers]
        problems.extend(f"{eid}: names unknown verifier {v}" for v in unknown)
        record = entry.get("independence_record")
        if record and (problem := _path_problem(str(record))):
            problems.append(f"{eid}: independence_record {record} {problem}")
        if unknown:
            continue
        if (
            entry.get("replay")
            and named
            and entry.get("relationship_to_generator") != NOT_APPLICABLE
            and not any(verifiers[v].decides for v in named)
        ):
            problems.append(
                f"{eid}: its replay names no program that decides; a premise check never "
                "decides a claim alone"
            )
        if (
            entry.get("relationship_to_generator") == INDEPENDENT
            and eid not in GRANDFATHERED_INDEPENDENCE
            and not independence_recorded(entry, verifiers)
        ):
            problems.append(
                f"{eid}: an independent implementation names the record of what its "
                "authors read: an independence_record, or a deciding program whose "
                "registry entry carries one"
            )
        structured = _mapping(entry.get("independence"))
        if structured:
            problems.extend(record_problems(eid, structured))
        needs_coverage = (entry.get("replay") and eid not in UNCOVERED_REPLAYS) or (
            entry.get("relationship_to_generator") == INDEPENDENT
            and eid not in UNSTRUCTURED_EVIDENCE
        )
        if needs_coverage and "coverage" not in structured:
            owner = "a replay" if entry.get("replay") else "an independent implementation"
            problems.append(f"{eid}: {owner} states its coverage in its independence record")
        deciders = [verifiers[v] for v in named if verifiers[v].decides]
        records = [_mapping(verifier.record.get("independence")) for verifier in deciders]
        if structured.get("clean_room") is True and any(
            record and record.get("clean_room") is not True for record in records
        ):
            problems.append(f"{eid}: clean_room contradicts a deciding program's record")
        if (
            entry.get("relationship_to_generator") == SHARED
            and records
            and all(record and not record.get("shares") for record in records)
            and not structured.get("shares")
        ):
            problems.append(f"{eid}: shared-components names no shared deciding component")
        if (
            entry.get("relationship_to_generator") == INDEPENDENT
            and eid not in UNSTRUCTURED_EVIDENCE
        ):
            problems.extend(structured_independence_problems(eid, entry, named, verifiers))
    return problems


def structured_independence_problems(
    eid: str, entry: Mapping[str, Any], named: Sequence[str], verifiers: Mapping[str, Verifier]
) -> list[str]:
    """What a new independent-implementation entry's structured record lacks: its
    coverage, always its own; who wrote the deciding code and what they read, its own or
    on every deciding program; and no component shared with the producer, which would
    make the relation shared-components (epistemics.md, The Independence Record)."""
    structured = _mapping(entry.get("independence"))
    problems: list[str] = []
    deciders = [verifiers[v] for v in named if verifiers[v].decides]
    carried = [verifier for verifier in deciders if "independence" in verifier.record]
    if "read" not in structured and (not deciders or len(carried) < len(deciders)):
        problems.append(
            f"{eid}: an independent implementation says who wrote its deciding code and "
            "what they read: in its own independence record, or in a structured record on "
            "every deciding program"
        )
    sharing = [
        verifier.id
        for verifier in carried
        if (_mapping(verifier.record.get("independence"))).get("shares")
    ]
    if structured.get("shares"):
        sharing.append(eid)
    problems.extend(
        f"{eid}: an independent implementation, but {owner}'s record shares the "
        f"producer{APOSTROPHE}s components, which makes the relation shared-components"
        for owner in sharing
    )
    return problems


def problems(evidence: Sequence[Mapping[str, Any]], path: Path = REGISTRY) -> list[str]:
    """Every cross-record problem of the registry and the evidence's verifier fields."""
    document = safe_load(path.read_text(encoding="utf-8"))
    ids = [entry["id"] for entry in document["verifiers"]]
    verifiers = load(path)
    stale = sorted(
        eid
        for eid in GRANDFATHERED_INDEPENDENCE
        if not any(
            entry.get("id") == eid and entry.get("relationship_to_generator") == INDEPENDENT
            for entry in evidence
        )
    )
    unstructured = {
        str(entry.get("id"))
        for entry in evidence
        if entry.get("relationship_to_generator") == INDEPENDENT
        and not entry.get("independence")
    }
    stale_programs = sorted(
        vid
        for vid in UNSTRUCTURED_PROGRAMS
        if vid not in verifiers
        or verifiers[vid].provenance != FIRST_PARTY
        or not verifiers[vid].decides
        or "independence" in verifiers[vid].record
    )
    uncovered = {
        str(entry.get("id"))
        for entry in evidence
        if entry.get("replay") and not _mapping(entry.get("independence")).get("coverage")
    }
    return [
        *(
            f"{eid}: coverage exemption is stale; remove it from UNCOVERED_REPLAYS"
            for eid in sorted(UNCOVERED_REPLAYS - uncovered)
        ),
        *registry_problems(verifiers, ids),
        *evidence_problems(evidence, verifiers),
        *(
            f"{eid}: grandfathered for its independence record, but no longer an "
            "independent-implementation entry; remove it from GRANDFATHERED_INDEPENDENCE"
            for eid in stale
        ),
        *(
            f"{vid}: exempt from the structured independence record, but no longer a "
            "first-party program that decides without one; remove it from "
            "UNSTRUCTURED_PROGRAMS"
            for vid in stale_programs
        ),
        *(
            f"{eid}: exempt from the structured independence record, but no longer an "
            "independent-implementation entry without one; remove it from "
            "UNSTRUCTURED_EVIDENCE"
            for eid in sorted(UNSTRUCTURED_EVIDENCE - unstructured)
        ),
    ]


def confirming_runs(entries: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """The entries that confirm by running code: a confirming origin and a passing replay,
    with a relation to the producer's code recorded, and not a sample, which confirms
    nothing whole."""
    return [
        entry
        for entry in entries
        if entry.get("origin") in CONFIRMING_ORIGINS
        and entry.get("replay")
        and entry.get("replay_status") == "passed"
        and entry.get("relationship_to_generator") in RANK
        and not sampled(entry)
    ]


def strongest(entries: Iterable[Mapping[str, Any]]) -> str | None:
    """The relation furthest from the producer's code among `entries`, or none."""
    relations = [str(entry["relationship_to_generator"]) for entry in entries]
    return max(relations, key=RANK.__getitem__, default=None)


def independence_line(record: Mapping[str, Any]) -> str:
    """A program's read, shared-component and authorship facts for the views.

    Each evidence run's ladder level is derived separately by `ladder_level`.
    """
    shares = record.get("shares") or []
    authors = "; ".join(
        str(author.get("name") or author.get("system"))
        + (f" ({author['setting']})" if author.get("setting") else "")
        for author in record.get("written_by") or []
    )
    overlap = _mapping(record.get("overlaps_producer"))
    apart = [
        label
        for label, key in (("prompt", "separate_prompt"), ("code", "separate_code"))
        if overlap.get(key) is True
    ]
    return (
        f"its authors read {', '.join(record.get('read') or [])}; "
        + (
            f"it shares {', '.join(shares)}"
            if shares
            else f"it shares none of the producer{APOSTROPHE}s code"
        )
        + f"; written by {authors}"
        + (f", with its own {' and '.join(apart)}" if apart else "")
        + f"; authorship in common with the producer{APOSTROPHE}s: "
        + f"{overlap.get('extent', 'not recorded')}, "
        + " ".join(str(overlap.get("note", "")).split())
    )


def provenance_label(verifier: Verifier) -> str:
    """A program's provenance as a view prints it, with its role where it only checks
    premises: `external`, `first-party`, `first-party, premises`."""
    return verifier.provenance if verifier.decides else f"{verifier.provenance}, premises"


def result_programs(
    cited: Iterable[Mapping[str, Any]], verifiers: Mapping[str, Verifier]
) -> list[Verifier]:
    """Every program behind a result's cited evidence, each once: deciders first, external
    before first-party, then in registry order."""
    named = {v for entry in cited for v in entry.get("verifiers") or [] if v in verifiers}
    order = {verifier_id: index for index, verifier_id in enumerate(verifiers)}
    return sorted(
        (verifiers[v] for v in named),
        key=lambda verifier: (
            not verifier.decides,
            verifier.provenance != EXTERNAL,
            order[verifier.id],
        ),
    )


#: The relations as a narrow table cell prints them.
SHORT_LABELS = {
    GENERATOR: f"producer{APOSTROPHE}s code",
    SAME: f"producer{APOSTROPHE}s code",
    SHARED: "shared components",
    INDEPENDENT: "independent",
    NOT_APPLICABLE: "no code",
    UNKNOWN: "unknown",
}
#: The order a list of programs is grouped in: deciders before premise checks, external
#: before first-party.
_GROUPS = ((EXTERNAL, True), (FIRST_PARTY, True), (EXTERNAL, False), (FIRST_PARTY, False))
_CODE_METHODS = frozenset(
    {
        "numerical-f64",
        "numerical-multiprecision",
        "interval-certified",
        "exact-algebraic",
        "proof-assistant-checked",
    }
)
_PROOFS = frozenset({"published-proof", "proof-audited"})


def runs_code(entry: Mapping[str, Any]) -> bool:
    """Whether an entry's verification is a program run: a computational method, as
    performed or as reported, or a replay."""
    method = entry.get("method") or entry.get("reported_method")
    return method in _CODE_METHODS or bool(entry.get("replay"))


#: Who ran a third party's check that this repository holds only as their report: its
#: origin is `external`, not `independently-external`, so it confirms nothing here. Until
#: 2026-10-06 it read "a third party's run", and the line in `RESULTS.md` went on to say
#: how the third party's code stood to the producer's, "independently re-implemented",
#: the words a confirmed result's mark uses (`E-k2m4-wand125-validtilt9-report`, T-081).
THIRD_PARTY_REPORT = "reported by a third party, not replayed here"


def run_label(entry: Mapping[str, Any]) -> str:
    """Who ran an entry's verification, in a few words."""
    labels = {
        "replayed-here": "replayed here",
        "audited-here": "audited here",
        "independently-external": "replayed by a third party",
    }
    if (origin := entry.get("origin")) in labels:
        return labels[str(origin)]
    if entry.get("performed_by") == "independent-external":
        return THIRD_PARTY_REPORT
    if (entry.get("method") or entry.get("reported_method")) in _PROOFS:
        return "a published proof"
    return f"the source{APOSTROPHE}s own run"


def programs_text(entry: Mapping[str, Any], verifiers: Mapping[str, Verifier]) -> str:
    """An entry's programs, grouped by provenance and role:
    `` `V-a`, `V-b` (external); `V-c` (first-party, premises) ``, or why it names none."""
    named = [verifiers[v] for v in entry.get("verifiers") or [] if v in verifiers]
    if not named:
        return "no program held" if runs_code(entry) else "no verification code"
    parts = []
    for provenance, decides in _GROUPS:
        group = [v for v in named if v.provenance == provenance and v.decides == decides]
        if group:
            label = provenance if decides else f"{provenance}, premises"
            parts.append(", ".join(f"`{v.id}`" for v in group) + f" ({label})")
    return "; ".join(parts)


def entry_line(entry: Mapping[str, Any], verifiers: Mapping[str, Verifier]) -> str:
    """One evidence entry's verification code in a line: who ran it, how its code stands
    to the producer's where a confirming run went beyond the source's own, and its
    programs. A third party's run held only as their report confirms nothing here, so
    its line names no relation, whose labels are the words a confirmation is read in
    (`THIRD_PARTY_REPORT`); `VERIFIERS.md` keeps its code relation in a column of its own."""
    beyond = entry.get("origin") in CONFIRMING_ORIGINS
    how = (
        f", {ladder_label(entry, verifiers)}"
        if beyond and entry.get("relationship_to_generator") in RANK
        else ""
    )
    coverage = (
        f"; {coverage_line(entry)}"
        if _mapping(entry.get("independence")).get("coverage")
        else ""
    )
    return (
        f"`{entry['id']}`, {run_label(entry)}{how}{coverage}: {programs_text(entry, verifiers)}"
    )
