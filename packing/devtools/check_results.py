#!/usr/bin/env python3
"""Validate structural support for the results register's declared rungs.

`epistemics.md` owns the policy. This checker derives V1 and V3 through V5 from
the cited evidence of any origin and the retained reviews, derives C0 through C5
from the confirming-origin evidence and the confirming-side reviews, requires
explanations for declared-only V0 and V2, and refuses unsupported promotion,
unexplained understatement and a confirmation above the verification. It also
resolves evidence, repository-file and `produced_by` references -- the campaign
records a result came out of, which must exist -- requires retained controls at
C3 and above, holds every review in `reviews` to a mapped, non-superseded,
dated document (two adversarial AI reviews by distinct reviewers and a human
oversight record at rung 4; human formalization reviews, an axiom receipt and
an open-review pointer at rung 5), and rejects unknown result ids in the reader
tier. It holds every `headline` to one table cell that states no
number its claim does not, dates every result of this project by `established`
and every result by others by `attribution.published`, never both, and requires
each entry's `registered` date. It requires each entry's `kind`, one of `KINDS`,
and cross-checks it against the relations the headline and the claim state and
the claims of the cited evidence (`kind_problems`). It holds a `superseded_by`, the
later results a result of a kind that is no bound declares imply it in whole or in part,
to registered results dated no earlier, on a case it shares, and refuses one on a bound,
whose supersession is derived (`superseded_by_problems`). It holds a `builds_on`, which
puts `after …` in the credit of a result of this project, to the sources the
result's own evidence cites. It refuses a rung label in a `claim`, `composition`,
`next_rung` or `significance.rationale`, or in a case record, that asserts a rung no
result the clause is about holds (`devtools.rung_prose`); a statement of what a rung
needs is not such an assertion. A result's status (recorded, reviewed, confirmed, incomplete) is
derived from its rungs by `devtools.result_status` and never stored; this holds
the one hand-recorded workflow fact, an entry's `activity`, to its fields, its
link and its age. Human review owns evidence relevance, claim
coverage, composition, significance, novelty, whether a headline says what its
claim says, and the choice between kinds the record cannot tell apart.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_results
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any

from devtools.build_bound_citations import RECENT_SINCE
from devtools.render_document_map import document_link
from devtools.result_status import STATUSES, activity_problems, latest_review, status
from devtools.rung_prose import REGISTER_FIELDS, Standing, label_problems
from devtools.verifier_registry import RANK, confirming_runs, strongest
from sqpack.assurance import EXTERNAL_ORIGINS, PROOF_METHODS
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RESULTS = ROOT / "frontier" / "results.yaml"
EVIDENCE = ROOT / "frontier" / "evidence.yaml"
BIBLIOGRAPHY = ROOT / "resources" / "bibliography.yaml"
FRONTIER = ROOT / "frontier"
#: The reader documents whose result mentions must name registered results: README, the
#: synopsis, and the site's overview, results, frontier and papers prose. Each template
#: is held for the results its own prose names: the overview's Recent Results names
#: T-060, T-093, T-065 and the three new exact values in its one paragraph, the papers
#: page T-060, and the Frontier page T-015 and T-016; README is held for its own fuller
#: account of the same progress.
READER_TIER = (
    REPO / "README.md",
    REPO / "SYNOPSIS.md",
    ROOT / "devtools" / "templates" / "overview-article.md",
    ROOT / "devtools" / "templates" / "all-results-article.md",
    ROOT / "devtools" / "templates" / "frontier-article.md",
    ROOT / "devtools" / "templates" / "papers-article.md",
)
DOCUMENT_MAP = REPO / "docs" / "project" / "document-map.yaml"
CAMPAIGN = ROOT / "campaign"
# What each `produced_by` key names, for the refusal message.
PRODUCED_BY_NOUNS = {
    "hypothesis": "hypothesis",
    "agenda_cell": "agenda commitment",
    "session": "agent session",
    "experiment": "experiment round",
}

MACHINE_METHODS = {"exact-algebraic", "interval-certified"}
FORMAL_METHOD = "proof-assistant-checked"
#: Confirmation counts work beyond the producing run: this repository's replays and
#: audits, and a third party's own replay retained here (epistemics.md, Confirmation).
CONFIRMING_ORIGINS = {"audited-here", "replayed-here", "independently-external"}
OURS_ORIGINS = CONFIRMING_ORIGINS
DECLARED_ONLY_V = {"V0", "V2"}
#: How many adversarial AI reviews, by distinct reviewers, rung 4 needs on either axis.
#: Provisional: the owner's "multiple adversarial attempts" read as two
#: (plan-2026-09-30-epistemics-ladder-review, decision 11); one edit reverses it.
ADVERSARIAL_REVIEWS = 2
#: How many human formalization reviews rung 5 needs on each axis. The owner set two at
#: C5; one at V5 is provisional (the same plan, decision 15).
FORMALIZATION_REVIEWS = {"V": 1, "C": 2}
#: What a human oversight record must say it checked (epistemics.md, Review Records).
OVERSIGHT_CHECKS = frozenset({"trust-boundary", "certificate-meaning", "ai-findings"})
#: What a human formalization review must say it checked.
FORMALIZATION_CHECKS = frozenset({"statement-fidelity", "definitions", "axioms", "build"})
ACCEPTING_VERDICTS = frozenset({"accepted", "defects-resolved"})
#: A review the result's own source performed counts toward V and never toward C.
SOURCE_RELATION = "source"
REVIEW_KINDS = frozenset({"adversarial", "confirming", "oversight", "formalization"})
# Whose result an entry is. A `previously-published` result is someone else's and names
# its source; a novel one is this project's and names none (epistemics.md, "Results by
# Others"). `common-knowledge` results owe no citation either way.
ATTRIBUTED_NOVELTY = "previously-published"
FIRST_PARTY_NOVELTY = {"apparently-novel", "confirmed-novel"}
#: A headline is one table cell in the README and `RESULTS.md`, so it has a width.
HEADLINE_LIMIT = 100
#: A number as a headline or claim writes it: an integer, or a decimal.
_NUMBER = re.compile(r"\d+(?:\.\d+)?")
#: What marks a decimal cut short of the one the claim writes.
TRUNCATION = "…"

#: The kinds of result the register holds, each named for what its claim concludes
#: (epistemics.md, Result Kinds), in the order the views list them. The schema's enum
#: is this tuple.
KINDS = (
    "lower-bound",
    "upper-bound",
    "optimality",
    "uniqueness",
    "simplification",
    "rigidity",
    "case-exclusion",
    "restricted-optimality",
    "method-limit",
    "correction",
    "audit",
)
SIMPLIFICATION = "simplification"
#: The relations on `s(n)` each bound kind states, as a headline (`≥`) and a claim (`>=`)
#: write them. These three kinds are the bounds; every other kind is no bound on `s(n)`.
KIND_RELATIONS = {
    "lower-bound": frozenset({"≥", ">=", ">"}),
    "upper-bound": frozenset({"≤", "<=", "<"}),
    "optimality": frozenset({"="}),
}
BOUND_KINDS = frozenset(KIND_RELATIONS)
#: The kinds that say nothing about `s(n)`: a property of one packing, one class of
#: configurations or the packings that attain `s(n)`, which the evidence contract types
#: as `derived-structure`.
STRUCTURE_KINDS = frozenset(
    {"uniqueness", "rigidity", "case-exclusion", "restricted-optimality"}
)
STRUCTURE_CLAIM = "derived-structure"
#: `s(n)` and the relation written after it. Several counts may share one relation,
#: `s(27), s(28) ≥ 28/5`. The lookbehind keeps `cos(x) =` from reading as `s(x) =`.
_COUNT = r"(?<![A-Za-z])s\([^)`]*\)"
_RELATION = r"\s*(≥|>=|≤|<=|>|<|=)"
_STATED_RELATION = re.compile(_COUNT + _RELATION)
_LEADING_RELATION = re.compile(rf"`{_COUNT}(?:,\s*{_COUNT})*{_RELATION}")
_RESULT_ID = re.compile(r"\bT-\d{3}\b")
#: How a refusal names the bound a headline opens with.
_OPENS_WITH = {
    "lower-bound": "a lower bound",
    "upper-bound": "an upper bound",
    "optimality": "an exact value",
}


def _rank(rung: str) -> int:
    return int(rung[1])


def _machine_proof_shaped(entry: dict) -> bool:
    """A certificate that replays: exact, interval or kernel-checked, with a replay
    command and a passing status. Rung 3's machine evidence on either axis."""
    return (
        (entry.get("method") in MACHINE_METHODS or entry.get("method") == FORMAL_METHOD)
        and bool(entry.get("certificate"))
        and bool(entry.get("replay"))
        and entry.get("replay_status") == "passed"
    )


def _formal(entry: dict) -> bool:
    """Rung 5's machine evidence: a kernel check with its axiom receipt retained."""
    return (
        entry.get("method") == FORMAL_METHOD
        and _machine_proof_shaped(entry)
        and bool(entry.get("axioms_receipt"))
    )


def _confirming_side(review: dict) -> bool:
    return review.get("relation") != SOURCE_RELATION


def _distinct_reviewers(reviews: Iterable[dict]) -> int:
    return len(
        {" ".join(str(review.get("reviewer", "")).split()).casefold() for review in reviews}
    )


def adversarially_reviewed(reviews: list[dict], *, confirming: bool = False) -> bool:
    """Rung 4's AI review: `ADVERSARIAL_REVIEWS` adversarial reviews by distinct
    reviewers, and the latest-dated review of the result accepts the claim, so every
    defect found has a disposition. On the confirming side, the source's own reviews
    do not count."""
    pool = [review for review in reviews if not confirming or _confirming_side(review)]
    adversarial = [
        review
        for review in pool
        if review.get("kind") == "adversarial" and review.get("reviewer_kind") == "ai"
    ]
    if _distinct_reviewers(adversarial) < ADVERSARIAL_REVIEWS:
        return False
    latest = latest_review(pool)
    return latest is not None and latest.get("verdict") in ACCEPTING_VERDICTS


def _human_records(reviews: Iterable[dict], kind: str, checks: frozenset[str]) -> list[dict]:
    return [
        review
        for review in reviews
        if review.get("kind") == kind
        and review.get("reviewer_kind") == "human"
        and checks <= set(review.get("checked") or [])
        and review.get("verdict") in ACCEPTING_VERDICTS
    ]


def overseen(reviews: list[dict], *, confirming: bool = False) -> bool:
    """Rung 4's human oversight: one accepting human record that checked the trust
    boundary, the certificate's meaning and the AI reviews' findings."""
    pool = [review for review in reviews if not confirming or _confirming_side(review)]
    return bool(_human_records(pool, "oversight", OVERSIGHT_CHECKS))


def formalization_reviews(reviews: list[dict], *, confirming: bool = False) -> int:
    """How many distinct human experts, none the formalization's author, reviewed the
    formal statement, definitions, axioms and build and accepted them."""
    pool = [review for review in reviews if not confirming or _confirming_side(review)]
    experts = [
        review
        for review in _human_records(pool, "formalization", FORMALIZATION_CHECKS)
        if review.get("independent_of_author") is True
    ]
    return _distinct_reviewers(experts)


def derive_confirmation(
    entries: list[dict], reviews: list[dict] | None = None, *, open_review: bool = False
) -> str:
    """The confirmation rung the confirming-origin evidence and the confirming-side
    reviews support (epistemics.md, Confirmation)."""
    reviews = list(reviews or [])
    ours = [entry for entry in entries if entry.get("origin") in CONFIRMING_ORIGINS]
    rebuilt = [
        entry for entry in ours if _formal(entry) and entry.get("origin") == "replayed-here"
    ]
    if (
        rebuilt
        and open_review
        and formalization_reviews(reviews, confirming=True) >= FORMALIZATION_REVIEWS["C"]
    ):
        return "C5"
    machine = [entry for entry in ours if _machine_proof_shaped(entry)]
    if (
        machine
        and adversarially_reviewed(reviews, confirming=True)
        and overseen(reviews, confirming=True)
    ):
        return "C4"
    if machine:
        return "C3"
    if any(entry.get("replay") and entry.get("replay_status") == "passed" for entry in ours):
        return "C2"
    if any(
        entry.get("origin") in EXTERNAL_ORIGINS
        and _qualifying_read(entry.get("external_review") or {})
        for entry in entries
    ):
        return "C1"
    return "C0"


def distinct_methods(entries: list[dict]) -> int:
    """The attribute shown beside the rung: how many distinct machine methods the
    confirming entries decide the claim by. Never a rung (epistemics.md, Confirmation)."""
    return len(
        {
            entry.get("method")
            for entry in entries
            if entry.get("origin") in CONFIRMING_ORIGINS and _machine_proof_shaped(entry)
        }
    )


def third_party_replayed(entries: list[dict]) -> bool:
    """The attribute shown beside the rung: a third party's own replay is retained."""
    return any(
        entry.get("origin") == "independently-external" and _machine_proof_shaped(entry)
        for entry in entries
    )


#: The claims that carry each half of an exact value.
_LOWER_CLAIMS = frozenset({"lower-bound", "exact-value"})
_UPPER_CLAIMS = frozenset({"upper-bound", "exact-value"})


def confirmation_code(
    record: Mapping[str, Any], entries: Sequence[Mapping[str, Any]]
) -> str | None:
    """The attribute shown beside the rung: how the code of the result's confirming runs
    stands to the code its producer used, as a `relationship_to_generator` value, or
    nothing where no confirming run is recorded. Never a rung (epistemics.md,
    Confirmation).

    The runs are the confirming-origin entries with a passing replay, the machine-shaped
    ones where there are any. Each part of the claim takes the relation furthest from the
    producer's code among the runs that confirm it, and the result takes the part closest
    to it: an optimality result is as independent as the less independent of its halves,
    so the grid replay of an upper half never makes a lower half re-run with the source's
    own checker read as re-implemented. A bound reads its own runs, and any other kind
    reads all of them.
    """
    runs = confirming_runs(entries)
    machine = [entry for entry in runs if _machine_proof_shaped(dict(entry))]
    pool = machine or runs
    if not pool:
        return None
    kind = record.get("kind")
    if kind in {"lower-bound", "upper-bound"}:
        own = [entry for entry in pool if entry.get("claim") in {kind, "exact-value"}]
        return strongest(own or pool)
    lower = strongest(entry for entry in pool if entry.get("claim") in _LOWER_CLAIMS)
    upper = strongest(entry for entry in pool if entry.get("claim") in _UPPER_CLAIMS)
    if lower and upper:
        return min((lower, upper), key=RANK.__getitem__)
    return strongest(pool)


#: The word whose kind the prose rule asks for, as a verb or a participle; a novelty label
#: or a status in code is not the word.
_CONFIRMED = re.compile(r"(?<![\w`])confirmed(?![\w`-])", re.IGNORECASE)
#: The phrases that say which kind of confirmation a sentence means (epistemics.md,
#: Confirmation): the producer's own code re-run, a re-implementation sharing its named
#: components, or an independent re-implementation.
CONFIRMATION_KINDS = re.compile(
    r"producer[\u2019']s (?:own )?(?:verification )?code"
    r"|independent(?:ly)?[ -]re-?implement|independent implementation"
    r"|shar(?:es|ing|ed) (?:the producer[\u2019']s )?(?:named )?components",
    re.IGNORECASE,
)
_SENTENCE_END = re.compile(r"(?<=[.;:])\s+(?=[A-Z`(\[])")


def confirmation_prose_problems(record: Mapping[str, Any]) -> list[str]:
    """Sentences of a result's `claim`, `composition` or `next_rung` that say "confirmed"
    without saying which kind of confirmation: the producer's code re-run, shared
    components, or an independent re-implementation. `notes` is history and exempt."""
    return [
        f"{record['id']}: {name} says confirmed without saying how: {sentence[:90]}"
        for name in ("claim", "composition", "next_rung")
        for sentence in _SENTENCE_END.split(" ".join(str(record.get(name) or "").split()))
        if _CONFIRMED.search(sentence) and not CONFIRMATION_KINDS.search(sentence)
    ]


def review_problems(record: dict, document_map: dict) -> list[str]:
    """What is wrong with a result's `reviews` and `open_review`, structurally: each
    review exists, is mapped as a non-superseded review, names its reviewer and date,
    covers this result when it names what it covers; a human reviewer states a
    relation; the open-review pointer's retained copy exists."""
    rid = record["id"]
    problems: list[str] = []
    for review in record.get("reviews") or []:
        path = str(review.get("path", ""))
        if problem := repository_file_problem(path):
            problems.append(f"{rid}: review path {problem}: {path}")
        entry = _document_map_entry(path, document_map)
        if not (
            entry and entry.get("role") == "review" and entry.get("lifecycle") != "superseded"
        ):
            problems.append(
                f"{rid}: review is not a non-superseded review in the document map: {path}"
            )
        if review.get("kind") not in REVIEW_KINDS:
            problems.append(f"{rid}: review {path} has no kind")
        if _iso_date(review.get("date")) is None:
            problems.append(f"{rid}: review {path} is not dated")
        if review.get("reviewer_kind") == "human" and not review.get("relation"):
            problems.append(f"{rid}: human review {path} states no relation to the project")
        covers = review.get("covers")
        if covers and rid not in covers:
            problems.append(f"{rid}: review {path} covers {covers}, not this result")
    if open_review := record.get("open_review"):
        retained = str(open_review.get("retained", ""))
        pure = PurePosixPath(retained)
        if pure.is_absolute() or ".." in pure.parts or not (REPO / pure).exists():
            problems.append(
                f"{rid}: open_review.retained does not name a retained path: {retained}"
            )
    return problems


def _qualifying_read(review: dict) -> bool:
    return (
        review.get("state") in {"informally-verified", "defect-found"}
        and bool(review.get("date"))
        and bool(review.get("reviewed_by"))
        and bool(review.get("note"))
    )


def _document_map_entry(path: str, document_map: dict) -> dict | None:
    for document in document_map["documents"]:
        if path == document["path"]:
            return document
    pure = PurePosixPath(path)
    return next(
        (
            collection
            for collection in document_map["collections"]
            if pure.match(collection["pattern"])
        ),
        None,
    )


def repository_file_problem(path: str) -> str | None:
    pure = PurePosixPath(path)
    if pure.is_absolute() or pure.as_posix() != path or ".." in pure.parts:
        return "must be a normalized repository-relative path"
    target = (REPO / pure).resolve()
    try:
        target.relative_to(REPO.resolve())
    except ValueError:
        return linked_repository_file_problem(path)
    if not target.is_file():
        return "does not name a file"
    return None


def linked_repository_file_problem(path: str) -> str | None:
    """Only separately admitted exact proof and atlas leaves may link outside."""
    from devtools import evand_arrangement_houses as evand  # noqa: PLC0415
    from devtools import refinement_house_links as refinements  # noqa: PLC0415
    from devtools import squish_second_update_confirmation as second  # noqa: PLC0415
    from devtools import squish_second_update_house_links as house  # noqa: PLC0415
    from devtools.squish_followup_packets import linked_certificate_problem  # noqa: PLC0415

    # Route by lexical repository names. Each owner then checks its repository and
    # custody; unrelated private fixtures must not inherit another owner's live root.
    proofs = {
        f"packing/witnesses/squish-422-second-update-2026/n-{n:03d}-rational.yaml.gz"
        for n in second.NUMBERS
    }
    houses = {f"packing/witnesses/known-best/n-{n:03d}.yaml" for n in house.LINK_NUMBERS}
    if path in proofs:
        return second.linked_certificate_problem(path, repository=REPO)
    if path in houses:
        return house.linked_house_problem(path, repository=REPO)
    if path in {f"packing/witnesses/known-best/n-{n:03d}.yaml" for n in refinements.NUMBERS}:
        return refinements.linked_house_problem(path, repository=REPO)
    if path in {f"packing/witnesses/known-best/n-{n:03d}.yaml" for n in evand.NUMBERS}:
        return evand.linked_house_problem(path, repository=REPO)
    return linked_certificate_problem(path, repository=REPO)


def repository_file_problems(paths: Iterable[str]) -> dict[str, str | None]:
    """Check one register invocation, sharing each packet's complete linked-proof admission."""
    from devtools import squish_followup_packets as first  # noqa: PLC0415
    from devtools.squish_second_update_packets import NUMBERS  # noqa: PLC0415

    selected = dict.fromkeys(paths)
    declared = {
        f"packing/witnesses/squish-422-second-update-2026/n-{n:03d}-rational.yaml.gz"
        for n in NUMBERS
    }
    linked = [
        path
        for path in selected
        if path in declared and not (REPO / path).resolve().is_relative_to(REPO.resolve())
    ]
    problems: dict[str, str | None] = {}
    if linked:
        from devtools import squish_second_update_confirmation as second  # noqa: PLC0415

        problems.update(second.linked_certificate_problems(linked, repository=REPO))
    first_declared = {
        f"packing/witnesses/squish-401-update-2026/n-{n:03d}-rational.yaml.gz"
        for n in first.RESULT_NUMBERS
    }
    first_linked = [
        path
        for path in selected
        if path in first_declared and not (REPO / path).resolve().is_relative_to(REPO.resolve())
    ]
    if first_linked:
        problems.update(first.linked_certificate_problems(first_linked, repository=REPO))
    problems.update(
        (path, repository_file_problem(path)) for path in selected if path not in problems
    )
    return problems


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    return safe_load(text[4 : text.index("\n---", 4)]) or {}


def campaign_ids() -> dict[str, set[str]]:
    """The ids a `produced_by` entry may name, read from the campaign record.

    Hypotheses, sessions and rounds carry their id as the filename prefix, which is the
    naming rule `packing-ledger check` enforces, so the prefix is read rather than every
    frontmatter parsed. Agenda commitments live inside their agenda's frontmatter and
    are read from there.
    """

    def prefixes(paths: Iterable[Path], pattern: str) -> set[str]:
        return {match.group() for path in paths if (match := re.match(pattern, path.name))}

    cells: set[str] = set()
    for path in sorted((CAMPAIGN / "agendas").glob("agenda-*.md")):
        agenda = _frontmatter(path).get("agenda") or {}
        cells.update(item["id"] for item in agenda.get("items") or [])
    return {
        "hypothesis": prefixes((CAMPAIGN / "hypotheses").glob("H-*.md"), r"H-\d{3}"),
        "agenda_cell": cells,
        "session": prefixes(
            (CAMPAIGN / "agent-sessions").glob("session-*.md"), r"session-\d{3}"
        ),
        "experiment": prefixes(CAMPAIGN.glob("series/*/experiments/exp-*.md"), r"exp-\d{3}"),
    }


LOWER_BOUND_FIELDS = ("reported_lower_bound", "verified_lower_bound")
BOUND_FIELDS = (*LOWER_BOUND_FIELDS, "reported_upper_bound", "verified_upper_bound")


def case_bound_evidence(
    frontier: Path = FRONTIER, fields: tuple[str, ...] = LOWER_BOUND_FIELDS
) -> dict[int, set[str]]:
    """The evidence each case's bound fields cite, by `n`; the lower bounds by default.

    Both lanes, because a reported bound is a result the record acts on as surely as a
    verified one: it is registered when the source is taken in and waits on a replay.
    """
    cited: dict[int, set[str]] = {}
    for path in sorted(frontier.glob("n-*.md")):
        case = _frontmatter(path).get("packing") or {}
        ids: set[str] = set()
        for field in fields:
            ids.update((case.get(field) or {}).get("evidence") or [])
        cited[int(case["n"])] = ids
    return cited


def scope_values(scope: dict) -> set[int]:
    if "n_values" in scope:
        return set(scope["n_values"])
    return set(range(scope["n_min"], scope["n_max"] + 1))


def _dated(source: Mapping[str, Any] | None) -> str | None:
    return str(source["dated"]) if source and source.get("dated") else None


def attribution_problems(record: dict, sources: dict[str, dict]) -> list[str]:
    """What is wrong with a result's `attribution`, given the bibliography."""
    rid, novelty = record["id"], record["novelty"]
    attribution = record.get("attribution")
    if novelty == ATTRIBUTED_NOVELTY and not attribution:
        return [f"{rid}: a previously-published result names its source in attribution"]
    if novelty in FIRST_PARTY_NOVELTY and attribution:
        return [f"{rid}: an {novelty} result is this project's and carries no attribution"]
    if not attribution:
        return []
    problems: list[str] = []
    recent = attribution["published"] >= RECENT_SINCE.isoformat()
    for key in attribution["source_keys"]:
        source = sources.get(key)
        if source is None:
            problems.append(f"{rid}: attribution names {key}, which bibliography.yaml lacks")
        elif recent and not source.get("lineage"):
            problems.append(
                f"{rid}: {key} has no lineage, which a result by others published since "
                f"{RECENT_SINCE.isoformat()} needs"
            )
    return problems


def builds_on_problems(
    record: dict, sources: Mapping[str, Mapping[str, Any]], cited: Sequence[Mapping[str, Any]]
) -> list[str]:
    """What is wrong with a result's `builds_on`: whose work this project's result rests on.

    The field is what puts `after …` in a result's credit, so it may say only what the
    record already holds. It belongs to a result of this project, since a result by
    others takes its whole credit line from the bibliography. Each source it names is
    one an evidence entry the result cites already names as its `source_key`, and each
    credited name is an author of one of those sources.
    """
    builds_on = record.get("builds_on")
    if not builds_on:
        return []
    rid = record["id"]
    if record.get("attribution"):
        return [
            f"{rid}: a result by others takes its credit from the bibliography, not builds_on"
        ]
    problems: list[str] = []
    evidenced = {entry.get("source_key") for entry in cited}
    authors: set[str] = set()
    for key in builds_on["source_keys"]:
        source = sources.get(key)
        if source is None:
            problems.append(f"{rid}: builds_on names {key}, which bibliography.yaml lacks")
            continue
        authors.update(source["authors"])
        if key not in evidenced:
            problems.append(
                f"{rid}: builds_on names {key}, which no evidence entry the result cites "
                "carries as its source_key"
            )
    problems.extend(
        f"{rid}: builds_on credits {name}, who is not an author of "
        f"{', '.join(builds_on['source_keys'])}"
        for name in builds_on["credit"]
        if name not in authors
    )
    return problems


def corrects_problems(
    record: dict,
    sources: Mapping[str, Mapping[str, Any]],
    records: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    """What is wrong with a result's `corrects`: the published work it stands in for.

    The field names outside work, so a page can say which publication a bound corrects.
    Its source is in the bibliography, its result is the register's record of that same
    publication, and that record is not itself sound any more: a result standing in for a
    published one that still holds would be a stronger bound, not a correction.
    """
    corrects = record.get("corrects")
    if not corrects:
        return []
    rid = record["id"]
    key, target = corrects["source_key"], corrects["result"]
    problems: list[str] = []
    if key not in sources:
        problems.append(f"{rid}: corrects names {key}, which bibliography.yaml lacks")
    corrected = records.get(target)
    if corrected is None:
        return [*problems, f"{rid}: corrects names {target}, which is not a registered result"]
    if target == rid:
        problems.append(f"{rid}: a result does not correct itself")
    keys = set((corrected.get("attribution") or {}).get("source_keys") or [])
    if keys and key not in keys:
        problems.append(
            f"{rid}: corrects {target} as {key}, but {target} credits {sorted(keys)}"
        )
    if corrected.get("verification") != "V0":
        problems.append(
            f"{rid}: corrects {target}, which still stands at {corrected.get('verification')}"
        )
    return problems


def recent_evidence(entry: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]]) -> bool:
    """Whether an evidence entry carries a result the register must hold: this project's
    own new result, or another's from a source dated on or after `RECENT_SINCE`."""
    if entry.get("novelty") in FIRST_PARTY_NOVELTY:
        return True
    if entry.get("novelty") == ATTRIBUTED_NOVELTY:
        dated = _dated(sources.get(str(entry.get("source_key"))))
        return dated is not None and dated >= RECENT_SINCE.isoformat()
    return False


def headline_problems(record: dict) -> list[str]:
    """What is wrong with a result's `headline`, read against its own claim.

    The headline is what a table shows in place of the claim, so it may shorten the claim
    but not add to it: every number it writes is one the claim writes, or a decimal the
    claim writes cut short and marked with an ellipsis. Whether the words say what the
    claim says, and keep its relation, is review's.
    """
    rid = record["id"]
    headline = record.get("headline")
    if not isinstance(headline, str) or not headline.strip():
        return [f"{rid}: states no headline"]
    problems: list[str] = []
    if len(headline) > HEADLINE_LIMIT:
        problems.append(
            f"{rid}: headline is {len(headline)} characters, over the {HEADLINE_LIMIT} "
            "a table cell takes"
        )
    if headline != headline.strip() or "\n" in headline:
        problems.append(f"{rid}: headline is not one trimmed line")
    claimed = set(_NUMBER.findall(str(record.get("claim", ""))))
    for match in _NUMBER.finditer(headline):
        number = match.group()
        truncated = headline[match.end() : match.end() + 1] == TRUNCATION and any(
            "." in number and written.startswith(number) for written in claimed
        )
        if number not in claimed and not truncated:
            problems.append(f"{rid}: headline states {number}, which its claim does not")
    return problems


def kind_label(kind: str) -> str:
    """A kind as a reader sees it: `case-exclusion` is "case exclusion"."""
    return kind.replace("-", " ")


def stated_relations(text: str) -> set[str]:
    """Every relation `text` writes directly after an `s(n)`."""
    return set(_STATED_RELATION.findall(text))


def headline_kind(headline: str) -> str | None:
    """The bound a headline states where it opens with one: `` `s(17) ≥ …` `` is a
    lower bound, `` `s(29) ≤ …` `` an upper bound and `` `s(13) = 4` `` optimality.
    A headline that opens with words derives nothing."""
    match = _LEADING_RELATION.match(headline)
    if not match:
        return None
    return next(kind for kind, relations in KIND_RELATIONS.items() if match[1] in relations)


def _relation_problems(kind: str, headline: str, claim: str) -> list[str]:
    """Where the relations a headline and a claim write disagree with a declared kind."""
    label = kind_label(kind)
    opens = headline_kind(headline)
    if opens is not None and kind not in {opens, SIMPLIFICATION}:
        return [f"kind is {label}, but its headline opens with {_OPENS_WITH[opens]}"]
    in_headline, in_claim = stated_relations(headline), stated_relations(claim)
    if kind == "optimality":
        if "=" not in in_headline | in_claim:
            return ["an optimality result states an exact value, s(n) = v"]
        return []
    if kind in BOUND_KINDS:
        relations = KIND_RELATIONS[kind]
        problems = [
            f"kind is {label}, but its headline states s(n) {relation}"
            for relation in sorted(in_headline - relations)
        ]
        if in_claim and not in_claim & relations:
            problems.append(
                f"kind is {label}, but its claim states only s(n) {', '.join(sorted(in_claim))}"
            )
        return problems
    if kind in STRUCTURE_KINDS and in_headline:
        relation = min(in_headline)
        return [f"a {label} is no bound on s(n), but its headline states s(n) {relation}"]
    return []


def _evidence_needed(kind: str, claims: set[str]) -> str | None:
    """What a kind's cited evidence must claim and does not, or nothing."""
    if kind == "optimality":
        if "exact-value" in claims or {"lower-bound", "upper-bound"} <= claims:
            return None
        return "`exact-value`, or both `lower-bound` and `upper-bound`"
    if kind in BOUND_KINDS:
        return None if claims & {kind, "exact-value"} else f"`{kind}` or `exact-value`"
    if kind in STRUCTURE_KINDS and STRUCTURE_CLAIM not in claims:
        return f"`{STRUCTURE_CLAIM}`"
    return None


def kind_problems(
    record: dict, cited: Iterable[Mapping[str, Any]], scopes: Mapping[str, set[int]]
) -> list[str]:
    """What is wrong with a result's `kind`, read against its own record.

    The kind is declared, and three things the record already holds check it.

    - **The relations written.** A headline that opens with a relation on `s(n)` states
      its kind, and only a simplification, a second proof of a result the record holds,
      may restate one under another kind. A bound's headline writes no relation of
      another direction, its claim writes one of its own if it writes any, and an
      optimality result writes its `=`. A kind that says nothing about `s(n)` has a
      headline that writes none.
    - **The cited evidence.** It claims what the kind needs: the bound for a bound, an
      exact value or both halves for optimality, and `derived-structure` for the kinds
      that say nothing about `s(n)`.
    - **The results the claim names.** A simplification's claim names the registered
      result it proves again, on a case they share. `scopes` is every result's cases.

    Method limit, correction and audit are told apart by review alone.
    """
    rid = record["id"]
    kind = record.get("kind")
    if kind is None:
        return [f"{rid}: states no kind"]
    if kind not in KINDS:
        return [f"{rid}: kind {kind} is not one of {', '.join(KINDS)}"]
    headline = str(record.get("headline", ""))
    claim = " ".join(str(record.get("claim", "")).split())
    problems = _relation_problems(kind, headline, claim)
    needed = _evidence_needed(kind, {str(entry.get("claim")) for entry in cited})
    if needed is not None:
        problems.append(f"kind is {kind_label(kind)}, and no cited evidence claims {needed}")
    if kind == SIMPLIFICATION:
        cases = scopes.get(rid, set())
        named = {other for other in _RESULT_ID.findall(claim) if other != rid}
        if not any(cases & scopes.get(other, set()) for other in named):
            problems.append(
                "a simplification's claim names the registered result it proves again, "
                "on a case they share"
            )
    return [f"{rid}: {problem}" for problem in problems]


def result_date(record: Mapping[str, Any]) -> str:
    """The date a result is of: its source's `attribution.published` for a result by
    others, which may be a year alone, else the day this project `established` it."""
    attribution = record.get("attribution") or {}
    return str(attribution.get("published") or record.get("established") or "")


def _earlier(date_of: str, than: str) -> bool:
    """Whether one result's date is strictly before another's, at the precision both
    give: `1979` is before `2026-09-24`, and `2026` is not before `2026-09-24`."""
    shared = min(len(date_of), len(than))
    return date_of[:shared] < than[:shared]


def superseded_by_problems(
    record: dict,
    dated: Mapping[str, str],
    scopes: Mapping[str, set[int]],
    holding: frozenset[str] = frozenset(),
) -> list[str]:
    """What is wrong with a result's `superseded_by`, the later results it declares
    imply it in whole or in part.

    Only a result whose kind is no bound declares it: a bound's supersession is derived
    from the case records (`render_recent_results.superseding`), and a declaration
    beside it would be a second account that could disagree. Each named result is in
    the register, is not this one, appears once, is dated no earlier than this one
    (`result_date`: when its source published it or this project established it, not
    when it was registered), and shares a case with it. A result a case bound still
    rests on is not superseded as a whole, whatever implies it, since the tables would
    hide the row a case's bound cites; it may be superseded in part. `dated` and
    `scopes` are every result's date and cases, and `holding` the results a case bound
    rests on now (`holding_results`).
    """
    rid = record["id"]
    declared = record.get("superseded_by") or []
    if not declared:
        return []
    if record.get("kind") in BOUND_KINDS:
        return [
            (
                f"{rid}: declares superseded_by, but its kind is "
                f"{kind_label(record['kind'])}, whose supersession is derived from the "
                "case records and never declared"
            )
        ]
    problems: list[str] = []
    seen: set[str] = set()
    for item in declared:
        other = str(item["result"])
        if other == rid:
            problems.append(f"{rid}: superseded_by names the result itself")
            continue
        if other in seen:
            problems.append(f"{rid}: superseded_by names {other} twice")
            continue
        seen.add(other)
        if other not in dated:
            problems.append(f"{rid}: superseded_by names {other}, which is not registered")
            continue
        if _earlier(dated[other], dated[rid]):
            problems.append(
                f"{rid}: superseded_by names {other}, dated {dated[other]}, before this "
                f"result's {dated[rid]}"
            )
        if not scopes.get(rid, set()) & scopes.get(other, set()):
            problems.append(f"{rid}: superseded_by names {other}, which shares no case with it")
        if item.get("extent") == "whole" and rid in holding:
            problems.append(
                f"{rid}: superseded_by names {other} as superseding all of it, but a case "
                "bound still rests on it"
            )
    return problems


def superseded_by_cycles(results: Iterable[Mapping[str, Any]]) -> list[str]:
    """The declared supersessions that lead back to where they start. A result is
    superseded only by one dated no earlier than itself (`superseded_by_problems`), so
    two results of one day could each declare the other, and both rows would be hidden
    for a supersession neither has. Each cycle is named once, from its first result in
    the register, and a result that names itself is `superseded_by_problems`' to say."""
    later = {
        str(record["id"]): [str(item["result"]) for item in record.get("superseded_by") or []]
        for record in results
    }
    problems: list[str] = []
    found: set[frozenset[str]] = set()
    for start in later:
        paths: list[tuple[str, ...]] = [(start,)]
        while paths:
            path = paths.pop()
            for other in later.get(path[-1], []):
                if other == start and len(path) > 1 and frozenset(path) not in found:
                    found.add(frozenset(path))
                    problems.append(
                        f"{start}: superseded_by leads back to it, "
                        f"{' to '.join((*path, start))}"
                    )
                elif other not in path:
                    paths.append((*path, other))
    return problems


def holding_results() -> frozenset[str]:
    """Every result a case bound rests on now, lower or upper, verified or reported:
    `render_recent_results.held` over every case record. Raises `ValueError` where a
    case's own lower-bound evidence is carried by no registered result, or by more than
    one (`render_recent_results.project_result`)."""
    from devtools.render_recent_results import held, load_records  # noqa: PLC0415

    records = load_records()
    holders: set[str] = set()
    for n in records.cases:
        case = held(n, records)
        holders |= case.lower_holders | case.upper_holders
    return frozenset(holders)


def established_problems(record: dict, last_reviewed: str) -> list[str]:
    """What is wrong with the date a result carries, given whose result it is.

    A result of this project is dated by `established`, the day its certificate or proof
    first passed here, which cannot precede the project's start or follow the register's
    last review. A result by others is dated by its source in `attribution.published`,
    and a second date beside that one would be a second answer to one question.
    """
    established = record.get("established")
    if record.get("attribution"):
        problem = (
            "a result by others is dated by attribution.published and carries no established"
            if established is not None
            else None
        )
    elif established is None:
        problem = "a result of this project names the day it was established"
    else:
        problem = _established_date_problem(str(established), str(last_reviewed))
    return [f"{record['id']}: {problem}"] if problem else []


def _established_date_problem(established: str, last_reviewed: str) -> str | None:
    try:
        day = date.fromisoformat(established)
    except ValueError:
        return f"established {established} is not a date"
    if day < RECENT_SINCE:
        return (
            f"established {established} is before {RECENT_SINCE.isoformat()}, "
            "when this project's work began"
        )
    if day > date.fromisoformat(last_reviewed):
        return f"established {established} is after the register's last review, {last_reviewed}"
    return None


def coverage_problems(
    results: list[dict],
    evidence_index: dict[str, dict],
    sources: dict[str, dict],
    cases: dict[int, set[str]],
) -> list[str]:
    """Case lower bounds from recent sources that no register entry covers.

    The rule the register keeps (plan-2026-09-29-third-party-results-register): every
    result of this project, and every result by others published since the project
    began that the record acts on. A case's lower bound, reported or verified, is the
    record acting on it; the entry that covers it must cite the same evidence and name
    that `n` in its scope.
    """
    covered: dict[str, set[int]] = {}
    for record in results:
        for ref in record["evidence"]:
            covered.setdefault(ref, set()).update(scope_values(record["scope"]))
    problems: list[str] = []
    for n, ids in sorted(cases.items()):
        for ref in sorted(ids):
            recent = recent_evidence(evidence_index.get(ref) or {}, sources)
            if recent and n not in covered.get(ref, set()):
                problems.append(
                    f"n-{n:03d}: its lower bound cites {ref}, and no registered result "
                    f"citing it covers n = {n}"
                )
    return problems


def _iso_date(value: object) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def registered_problems(record: dict, last_reviewed: str) -> list[str]:
    """What is wrong with a result's `registered` date.

    A registration is a real calendar date no later than the register's own
    `last_reviewed`, since a result cannot enter a record reviewed before it existed.
    """
    rid = record["id"]
    registered = record.get("registered")
    if registered is None:
        return [f"{rid}: registered is required"]
    if (when := _iso_date(registered)) is None:
        return [f"{rid}: registered is not a calendar date: {registered}"]
    if (reviewed := _iso_date(last_reviewed)) is not None and when > reviewed:
        return [
            (
                f"{rid}: registered {when.isoformat()} is after the register's "
                f"last_reviewed {reviewed.isoformat()}"
            )
        ]
    return []


def derive_verification(entries: list[dict], reviews: list[dict] | None = None) -> str:
    """The verification rung the cited evidence, of any origin, and the retained
    reviews support (epistemics.md, Verification)."""
    reviews = list(reviews or [])
    if any(_formal(entry) for entry in entries) and (
        formalization_reviews(reviews) >= FORMALIZATION_REVIEWS["V"]
    ):
        return "V5"
    machine = any(_machine_proof_shaped(entry) for entry in entries)
    if machine and adversarially_reviewed(reviews) and overseen(reviews):
        return "V4"
    if machine:
        return "V3"
    if any(entry.get("method") in PROOF_METHODS and entry.get("proof") for entry in entries):
        return "V3"
    if any(
        str(entry.get("method", "")).startswith("numerical") and entry.get("precision")
        for entry in entries
    ):
        return "V1"
    return "V0"


def rung_label_problems(
    results: Sequence[Mapping[str, Any]],
    standings: Mapping[str, Standing],
    cases: Iterable[Path] | None = None,
) -> list[str]:
    """Rung labels the register's prose and the case records assert that no result they
    are about holds: the prose copy of a derived rung, gone stale (`devtools.rung_prose`).
    """
    problems = [
        f"{record['id']}: {field} {problem}"
        for record in results
        for field in REGISTER_FIELDS
        for problem in label_problems(record.get(field) or "", standings, own=record["id"])
    ]
    # A significance rationale is a dated judgment of the claim, and it may say what a
    # rung would need; it may not say what rung the result stands at, which goes stale as
    # the rungs move. T-064's said "V0/C1 says how far it stands" for two days after the
    # result reached V3/C3 (lane R9, 2026-10-06).
    problems.extend(
        f"{record['id']}: significance.rationale {problem}"
        for record in results
        for problem in label_problems(
            str((record.get("significance") or {}).get("rationale") or ""),
            standings,
            own=record["id"],
        )
    )
    by_n: dict[int, set[str]] = {}
    for record in results:
        for n in scope_values(record["scope"]):
            by_n.setdefault(n, set()).add(record["id"])
    for path in sorted(FRONTIER.glob("n-*.md")) if cases is None else cases:
        scoped = by_n.get(int(path.stem.removeprefix("n-")), set())
        problems.extend(
            f"{path.name}: {problem}"
            for problem in label_problems(
                path.read_text(encoding="utf-8"), standings, fallback=scoped
            )
        )
    return problems


def verification_relation(declared: str, derived: str) -> str:
    if declared == "V2" and _rank(derived) <= 1:
        return "supported"
    if _rank(declared) > _rank(derived):
        return "inflated"
    if _rank(declared) < _rank(derived):
        return "understated"
    return "supported"


def record_links(document_map: Mapping[str, Any]) -> tuple[str, ...]:
    """The document map's links to dated records, each written with the record's own title.

    The synopsis's document map links each document by its own H1
    (`devtools.render_document_map`). A document of `record` authority, such as a review
    stored as its reviewer wrote it, keeps the result ids it was written with and is never
    edited to follow a renumbering. When a provisional id is renumbered at a merge, as
    T-118 became T-101 on 6 October 2026, the record's title still names the old id, so
    these links are left out of the reader-tier mention check; the renumbered entry's
    notes say which id the record means.
    """
    return tuple(
        document_link(document["path"])
        for document in document_map.get("documents", ())
        if document.get("authority") == "record"
    )


def reader_tier_text(path: Path, links: Iterable[str]) -> str:
    """A reader-tier file's text, less `record_links`; every other mention is checked."""
    text = path.read_text(encoding="utf-8")
    for link in links:
        text = text.replace(link, "")
    return text


def main() -> int:
    problems: list[str] = []
    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    document_map = safe_load(DOCUMENT_MAP.read_text(encoding="utf-8"))
    evidence_index = {
        entry["id"]: entry
        for entry in safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    }
    results = register["results"]
    known_ids = campaign_ids()
    sources = {
        source["key"]: source
        for source in safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))["sources"]
    }

    expected_ids = [f"T-{index:03d}" for index in range(1, len(results) + 1)]
    actual_ids = [record["id"] for record in results]
    if actual_ids != expected_ids:
        problems.append(f"register ids are not contiguous T-001..: {actual_ids}")
    scopes = {record["id"]: scope_values(record["scope"]) for record in results}
    by_id = {record["id"]: record for record in results}
    dated = {record["id"]: result_date(record) for record in results}
    try:
        holding = holding_results()
    except ValueError as error:
        # A case bound that no registered result carries, or that several do, is named
        # here and the checks go on, the whole-supersession check without holders, so
        # every other problem in the register is still reported.
        holding = frozenset()
        problems.append(f"which results hold a case bound could not be read: {error}")
    problems.extend(superseded_by_cycles(results))

    standings: dict[str, Standing] = {}
    artifact_problems = repository_file_problems(
        path
        for record in results
        for field in ("artifacts", "controls")
        for path in record.get(field) or []
    )
    for record in results:
        rid = record["id"]
        scope = record["scope"]
        if "n_min" in scope and scope["n_min"] > scope["n_max"]:
            problems.append(
                f"{rid}: scope range is reversed: {scope['n_min']} > {scope['n_max']}"
            )
        cited: list[dict] = []
        for ref in record["evidence"]:
            entry = evidence_index.get(ref)
            if entry is None:
                problems.append(f"{rid}: cites unknown evidence {ref}")
                continue
            cited.append(entry)

        for field in ("artifacts", "controls"):
            problems.extend(
                f"{rid}: {field} path {problem}: {path}"
                for path in record.get(field) or []
                if (problem := artifact_problems[path])
            )

        problems.extend(attribution_problems(record, sources))
        problems.extend(builds_on_problems(record, sources, cited))
        problems.extend(corrects_problems(record, sources, by_id))
        problems.extend(registered_problems(record, str(register["last_reviewed"])))
        problems.extend(headline_problems(record))
        problems.extend(kind_problems(record, cited, scopes))
        problems.extend(superseded_by_problems(record, dated, scopes, holding))
        problems.extend(established_problems(record, register["last_reviewed"]))
        problems.extend(activity_problems(record, str(register["last_reviewed"])))
        problems.extend(confirmation_prose_problems(record))

        for kind, value in (record.get("produced_by") or {}).items():
            if value not in known_ids.get(kind, set()):
                problems.append(
                    f"{rid}: produced_by.{kind} names {value}, which is not a recorded "
                    f"{PRODUCED_BY_NOUNS.get(kind, kind)}"
                )

        declared_c = record["confirmation"]
        declared_v = record["verification"]
        review_faults = review_problems(record, document_map)
        problems.extend(review_faults)
        # A review with a structural fault earns nothing until it is fixed.
        reviews = [] if review_faults else list(record.get("reviews") or [])
        derived_c = derive_confirmation(
            cited, reviews, open_review=bool(record.get("open_review")) and not review_faults
        )
        has_composition = bool(record.get("composition"))
        # A replay, rebuild or review record is also verification evidence, so C never
        # exceeds V from C2 up; a read (C1) of a recorded claim is the one exception,
        # reading being no kind of verification (epistemics.md, Scope and Composition).
        if _rank(declared_c) >= 2 and _rank(declared_c) > _rank(declared_v):
            problems.append(
                f"{rid}: confirmation {declared_c} exceeds verification {declared_v}; "
                "a confirmation is also verification evidence"
            )
        if _rank(declared_c) > _rank(derived_c):
            problems.append(
                f"{rid}: declares {declared_c} but the cited atoms support only {derived_c}"
            )
        elif _rank(declared_c) < _rank(derived_c) and not has_composition:
            problems.append(
                f"{rid}: understates {derived_c} as {declared_c} with no "
                "composition note claiming the minimum over parts"
            )

        if declared_v in DECLARED_ONLY_V and not record.get("notes"):
            problems.append(
                f"{rid}: {declared_v} is declared-only and needs a notes field saying why"
            )
        derived_v = derive_verification(cited, reviews)
        relation = verification_relation(declared_v, derived_v)
        if relation == "inflated":
            problems.append(
                f"{rid}: declares {declared_v} but the cited atoms support only {derived_v}"
            )
        elif relation == "understated" and not has_composition:
            problems.append(
                f"{rid}: understates {derived_v} as {declared_v} with no "
                "composition note claiming the minimum over parts"
            )

        if _rank(declared_c) >= 3 and not record.get("controls"):
            problems.append(f"{rid}: a {declared_c} rung names at least one control file")
        standings[rid] = Standing(declared_v, declared_c, derived_v, derived_c)

    problems.extend(coverage_problems(results, evidence_index, sources, case_bound_evidence()))
    problems.extend(rung_label_problems(results, standings))

    known = set(actual_ids)
    links = record_links(document_map)
    for path in READER_TIER:
        text = reader_tier_text(path, links)
        problems.extend(
            f"{path.name}: mentions unknown result {mention}"
            for mention in sorted(set(re.findall(r"\bT-\d{3}\b", text)))
            if mention not in known
        )

    if problems:
        print(f"{len(problems)} results-register problems:")
        for line in problems:
            print(f"  {line}")
        return 1

    held = [status(record, evidence_index) for record in results]
    print(
        f"{len(results)} registered results: every declared rung passes its "
        "structural checks, every path, source and produced_by id resolves, every "
        "headline and date holds, every kind agrees with its claim and evidence, every "
        "declared supersession names a result no earlier on a shared case, never "
        "supersedes all of a result a case bound rests on and never leads back, every "
        "recent case lower bound is covered, every reader-tier mention exists; by status, "
        + ", ".join(f"{held.count(name)} {name}" for name in STATUSES)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
