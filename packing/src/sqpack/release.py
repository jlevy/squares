"""The version this project's site and data carry, the rule that keeps it true, and the
papers' own versions beside it.

Every site page prints the site's version in its footer, the workbench shows it on its
stage, and the atlas posters and the films carry it too, so a release is stamped in one
place and all of them follow. This is the publication's version, not the package's:
`pyproject.toml` versions the code, and the two move for different reasons.

**The papers do not carry it.** Each paper has a version of its own, declared at the foot
of this module (`EXPLAINER_HISTORY`, `OPTIMALITY_REVIEW_EDITION`), and its front prints
that (`devtools.paper_front`); the site's version and the data hash appear nowhere on a
paper page, its Markdown edition or its PDF (the owner, 2026-10-01: "the repository
version should not go on the papers anymore. Papers should be individually versioned").

It is written `v0.4.1-f5e113` (the owner, 2026-09-22): the edition's semver core, then
the first six characters of the last commit that changed the evidence and data. Two
artifacts drawn from the same data carry the same version, whatever code commit built
them. The rule that keeps that true without any artifact chasing its own hash:

1. **Every site page prints `PUBLICATION_EDITION`, whose hash is the pinned
   `DATA_REVISION`.** Nothing reads git to stamp a version, so a render needs no history
   -- the deploy's shallow checkout and a source tarball stamp the same string as a full
   clone.
2. **`DATA_REVISION` must be what git says** -- `data_revision`, the last commit that
   changed `DATA_PATHS`. `tests/test_release.py` fails when the two differ, wherever git
   can answer; the pull-request behavioral shards check out full history, so every pull
   request asks.
3. **A commit that changes the data is followed by one that re-pins, and a re-pin is one
   line**: `DATA_REVISION` set to the hash the failing test names, which
   `python -m devtools.release_pin --update` writes. No commit can contain its own hash,
   so the pin trails the data by one commit. Only a branch's head has to agree: merges
   here are merge commits, so the data commit a branch pinned is still the last one on
   `main` after it lands. If `main`'s data also moved meanwhile, the merge is itself the
   new data commit, so the pull request's merge ref fails the check until the branch
   merges `main` and re-pins. **Nothing is rebuilt for a re-pin.**
4. **A drawn release asset states the data it was drawn from, and is never re-stamped.**
   The atlas posters and the films are expensive to draw, so each is stamped once, with
   the edition as it read when the asset was drawn (`edition_at`), and redrawn at a
   version bump or on demand. A poster records the data commit and its date in its own
   metadata (`devtools.build_known_best_atlas.CompositeIdentity`), so the stamp in its
   footer is held to the poster's own record and not to the pin. Until 2026-10-01 the
   posters printed the pin itself, and every data commit rewrote eight binaries to
   change six characters: thirty re-pins in a row, 13.6 MB of blobs each, and not one
   changed a card (`devtools.measure_release_assets --history`).
5. **A poster may trail the data until the next version bump** (`COMPOSITES_MAY_TRAIL`;
   the owner, 2026-10-01). While a poster's data revision is the pin, every claim on it
   must agree with the current record. Once the pin has moved, the cards that differ
   are listed by every check and fail none. A version bump redraws: a poster whose
   stamp does not carry `PUBLICATION_VERSION` fails.
6. **The re-pinning commit is not itself a data commit, and neither is a redraw.** The
   artifacts that carry a stamp are excluded from the data (`DATA_EXCLUDED`); counting
   them would make each redraw a new data commit, and the pin would chase its own hash
   forever. A test fails when a text file inside the data paths carries the stamp
   without being excluded.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import NamedTuple


class PublicationHistoryEntry(NamedTuple):
    """One public edition, when it was first published, and what it changed: an edition
    of the site and its data in `PUBLICATION_HISTORY`, or of one paper in that paper's
    own history."""

    version: str
    first_published: str
    result_scope: str


#: Every edition this publication, the site and its data, has had, newest first, and NONE
#: is ever removed. It is the site's record: the posters and the films are stamped from
#: it, the claim documents are regenerated at each entry, and `development.md` (Cutting
#: an edition) is where a reader finds it. It is not a paper's history: a paper lists its
#: own editions (`EXPLAINER_HISTORY`, below), which are the ones in which that paper
#: changed. Until 2026-10-02 the explainer listed this whole record and called it its
#: version history, so a site-only edition read as an edition of the paper.
#:
#: It used to be "the two editions retained in the explainer's short public history", and
#: under that rule adding v0.4.1 on 2026-09-22 dropped v0.3.0 -- the first edition, and the
#: proof of s(11) >= 381/100 the whole publication began with. A history that keeps the
#: last two is a changelog of the last two; a reader who wants to know when the result was
#: first put in front of anyone needs the first one most. `test_release` holds the list to
#: its oldest entry being that edition.
#:
#: Dates are when each edition's content was **first published** -- first live on the
#: public page -- read from the repository's GitHub Pages deployments, in UTC. They used to
#: be when each version *label* first appeared in Git, which is a different date whenever
#: an edition went live before it was named or was named before it went live, and both
#: happened (the owner, 2026-09-22: "accurately record the date of when that was first
#: published"). The deployment and commit behind each date, so it can be re-read:
#:
#:   v0.5.0  2026-10-02T01:07:03Z  8aaa411dc  the merge of PR 291, label and content together
#:   v0.4.2  2026-09-28T06:11:35Z  c19e6c0e2  the merge of PR 239, label and content together
#:   v0.4.1  2026-09-22T23:12:36Z  d5b1c2e1b  the merge of PR 218, label and content together
#:   v0.4.0  2026-09-13T22:12:47Z  f2e24e07b  T-025's 191/50 and the v0.4.0 label first live;
#:                                            the label was cut on a branch on September 10
#:   v0.3.0  2026-09-05T08:06:30Z  f060b1d78  the first Pages deployment of all, headlining
#:                                            s(11) >= 381/100; "v0.3.0" was only put on it
#:                                            on September 8 (`ce3b1ab56`)
#:
#: Reproduce with `gh api "repos/jlevy/squares/deployments?environment=github-pages"` and,
#: for each deployment's commit, what the page it built stated.
PUBLICATION_HISTORY = (
    PublicationHistoryEntry(
        version="v0.5.0",
        first_published="October 2, 2026",
        result_scope=(
            "The website edition: the project gets its own site, with a rated table of "
            "results and a frontier survey to $n = 324$, and a second paper reviews the "
            "proof that $s(11) = 3.8770835…$ (T-060)."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.2",
        first_published="September 28, 2026",
        result_scope=(
            "The recent-results edition: the atlas takes in $s(32) = 6$ and raises the "
            "lower bound for 22 more cases, among them $s(11) ≥ 3.875$ and "
            "$s(17) \\gt 4.66001$, from outside certificates the register verifies, and "
            "its star now marks every recent result, credited case by case."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.1",
        first_published="September 22, 2026",
        result_scope=(
            "The shared-version edition: the page and the atlas carry one version, "
            "named for the last commit that changed the data, and the atlas adds "
            "T-030's $s(18) ≥ 4679/1000$."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.0",
        first_published="September 13, 2026",
        result_scope=(
            "The T-025/T-026 proof edition: T-025 proves "
            "$s(11) ≥ 191/50 = 3.82$, and T-026 proves "
            "$s(11) ≥ 3.8264474…$."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.3.0",
        first_published="September 5, 2026",
        result_scope=(
            "The first edition: T-018's point certificate proves $s(11) ≥ 381/100 = 3.81$."
        ),
    ),
)

#: The edition the site's pages, the posters and the films state. Choose at most one
#: version bump per merge, and keep it fixed while revising that pull request.
PUBLICATION_VERSION = PUBLICATION_HISTORY[0].version

#: Where the edition stands, said ahead of the version. Empty once it is final; the
#: join below then drops it and the stray space with it, so going final is one edit.
PUBLICATION_STATUS = ""

#: What the shared version's hash names (the owner, 2026-09-22): the last commit that
#: changed the evidence and data every artifact is drawn from. Repository-relative, as
#: every declared path here is.
DATA_PATHS: tuple[str, ...] = ("packing/frontier", "packing/atlas/known-best")

#: What inside `DATA_PATHS` is not evidence and data, and so never moves the version, as
#: git pathspecs. The atlas composites and their raster and PDF exports carry the stamp
#: and are drawn from the data rather than being it; counting them would make the commit
#: that re-stamps them a data commit (rule 4 above). The video spikes are the players'
#: code, and the videos themselves are release assets, never committed.
#:
#: The registers' own READMEs join them on 2026-09-22, on the same grounds: they document
#: how a record is written, and nothing is drawn from them. `e560571f2` edited
#: `frontier/README.md` alone -- the prose on registration evidence, no packing record and
#: no bound -- and under the old list that moved the version every artifact prints, which
#: would have restamped the atlas and dated a cut whose every frame was identical. A
#: version that changes when the instructions change is not naming the evidence.
#:
#: The figure playbook joins them on 2026-09-28 for the same reason: it says how the atlas
#: is drawn and how to check it, and nothing is drawn from it. `6f6bc89ec` edited only its
#: legend counts and moved the version every artifact prints; the atlas's new citations
#: line then needed a one-word playbook edit that would have done it again.
DATA_EXCLUDED: tuple[str, ...] = (
    "packing/atlas/known-best/known-best-1-*",
    "packing/atlas/known-best/video",
    "packing/frontier/README.md",
    "packing/atlas/known-best/README.md",
    "packing/atlas/known-best/FIGURE-PLAYBOOK.md",
)

#: How many characters of that commit the version carries (the owner, 2026-09-22).
DATA_REVISION_LENGTH = 6

#: Whether an atlas poster may show data older than the pin between version bumps (rule
#: 5; the owner, 2026-10-01: the large assets are regenerated "whenever we do an official
#: site version number bump", and on demand). `True`: a card that differs from the
#: current record is listed and fails nothing, once the pin has moved past the poster's
#: own data revision. `False`: it fails, and the poster is redrawn whenever a card
#: changes -- as 26 commits did in September 2026, at 13.6 MB of blobs each.
COMPOSITES_MAY_TRAIL = True

#: The last data commit, pinned in full: what `data_revision` returned when it was last
#: re-pinned. Full rather than six characters so the drift check compares a commit, not
#: a prefix.
DATA_REVISION = "ea13726693246e03c22392048d44b32e00c3d38d"

#: The version, written the one way it is ever written: `v0.4.1-f5e113`. Semver core,
#: then the data revision, in the shape a build identifier takes everywhere else.
#:
#: This is the value to reach for. It exists because the artifacts that stamp an edition
#: used to compose their own strings from the parts, in two files and two languages, and
#: the page named a different commit from the atlas. Hand-assembled spellings of one fact
#: are how they come to disagree.
PUBLICATION_STAMP = f"{PUBLICATION_VERSION}-{DATA_REVISION[:DATA_REVISION_LENGTH]}"


def edition_at(revision: str) -> str:
    """The edition as an artifact drawn from the data commit `revision` writes it.

    `PUBLICATION_EDITION` is this at the pin. A drawn release asset keeps the one it
    was drawn with (rule 4), so its stamp is this at its own data revision.
    """
    stamp = f"{PUBLICATION_VERSION}-{revision[:DATA_REVISION_LENGTH]}"
    return " ".join(part for part in (PUBLICATION_STATUS, stamp) if part)


#: How the version is written wherever it is stamped: the stamp, with the status ahead
#: of it while there is one. The site's footer and the workbench take this string whole,
#: so neither can disagree about whether the reader is holding a draft, nor about how
#: the version is spelled. A paper's footer leaves it out (`render_overview.colophon_lines`).
PUBLICATION_EDITION = edition_at(DATA_REVISION)

#: When the current edition was first published, written the way a reader reads it.
PUBLICATION_DATE = PUBLICATION_HISTORY[0].first_published

#: When the publication itself was first published: its oldest edition's date. The site
#: began as the explainer, so this is also that paper's first day (`EXPLAINER_FIRST_PUBLISHED`,
#: which is what the paper's front prints).
FIRST_PUBLISHED = PUBLICATION_HISTORY[-1].first_published

# ---------------------------------------------------------------------------
# The papers' own versions.
#
# Each paper is versioned on its own (the owner, 2026-10-01), and its version line and
# version history reflect versions of the paper, not of the site or anything else. A
# published number under which the paper changed stays exactly as published, number and
# date, and is never renumbered; an edition under which the paper did not change is not
# a version of the paper and is not in its history. `devtools.paper_front` writes the
# front of both papers from these, and `tests/test_release.py` holds the rules.
# ---------------------------------------------------------------------------

#: The first paper's own editions, newest first. Through v0.5.0 the paper carried the
#: site's number, so the entries up to v0.4.2 are the editions of the publication in
#: which the paper itself changed, with the site's own number and date for each; v0.4.3
#: is the paper's first number of its own. What changed in the paper under each, read
#: from the article's history between the deployments listed above `PUBLICATION_HISTORY`
#: on 2026-10-02:
#:
#:   v0.4.4  the paper becomes Part I of the n = 11 series: the frontier update names
#:           T-037 and links Parts II and III, and Further Reading lists the series
#:   v0.4.3  the frontier update of September 30 records T-060's proof that s(11) is
#:           Trump's side, the T-026 rating moves from V4/C5 to V3/C3 under the ladder
#:           of 2026-09-30, Figure 3 marks the settled endpoint, and a footnote records
#:           the n = 12 and n = 17 bounds others have since raised (249d42c37,
#:           d205561f0, 7862dc3e8, a6f630dd7); a patch revision of the paper (the owner,
#:           2026-10-01), published under the v0.4.2 label until it was numbered
#:   v0.4.2  the frontier update of September 22 records Kleddamag's verified
#:           s(11) >= 3.875, built on T-026's certificate, and the paper presents T-026's
#:           bound as historical; Figure 2's star marks every recent result
#:   v0.4.0  the article rewritten around T-025 and T-026, the 381/100 proof kept as the
#:           worked example
#:   v0.3.0  the first edition
#:
#: Not versions of the paper: v0.4.1, under which the article did not change at all (the
#: shared version stamp and the atlas's T-030), and v0.5.0, the website edition, which
#: changed nothing in either paper. A new version of the paper goes on the front with its
#: own number and the day it is first published; `EXPLAINER_REVISED` moves with the
#: article either way.
#:
#: v0.4.3 is dated by the deployment that first served the article in its present
#: substance, the last substantive change being the V3/C3 regrade (d205561f0):
#:
#:   v0.4.3  2026-10-01T08:01:58Z  f9a3409f0  the first deployment holding d205561f0;
#:                                            the T-060 update was live from d44ec0408,
#:                                            2026-09-30T17:44:28Z, and the cosmetic
#:                                            changes after it (the slug, the credits
#:                                            form, 9b459da65 and 97e4069d5) went live
#:                                            on October 1 and 2, so the substantive
#:                                            day is the one recorded
EXPLAINER_HISTORY = (
    PublicationHistoryEntry(
        version="v0.4.4",
        first_published="October 5, 2026",
        result_scope=(
            "The series revision: the paper is Part I of three; its frontier update and "
            "Further Reading link Part II, on Kleddamag's T-037, and Part III, on T-060."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.3",
        first_published="October 1, 2026",
        result_scope=(
            "The settled-case revision: the frontier update records T-060's proof that "
            "$s(11)$ is Trump's side, Figure 3 marks the endpoint, T-026 is rated V3/C3, "
            "and the raised $n = 12$ and $17$ bounds are noted."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.2",
        first_published="September 28, 2026",
        result_scope=(
            "The recent-results edition: a frontier update records Kleddamag's verified "
            "$s(11) ≥ 3.875$, built on the T-026 certificate, so the paper presents "
            "T-026's bound as historical, and the star on the atlas in Figure 2 marks "
            "every recent result."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.4.0",
        first_published="September 13, 2026",
        result_scope=(
            "The T-025/T-026 proof edition: T-025 proves "
            "$s(11) ≥ 191/50 = 3.82$, and T-026 proves "
            "$s(11) ≥ 3.8264474…$."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.3.0",
        first_published="September 5, 2026",
        result_scope=(
            "The first edition: T-018's point certificate proves $s(11) ≥ 381/100 = 3.81$."
        ),
    ),
)

#: The first paper's version, plain, which its version line prints and links to its
#: history: its newest edition's number, with no status ahead of it and no data hash.
EXPLAINER_VERSION = EXPLAINER_HISTORY[0].version

#: When the first paper was first published: its oldest edition's day, which its front
#: puts beside the day it was last revised, so a reader sees both how old the result is
#: and how recently it was revised.
EXPLAINER_FIRST_PUBLISHED = EXPLAINER_HISTORY[-1].first_published

#: When the explainer's own text last changed: the date its "Last revised" line prints.
#: It is the author date of the last commit that changed the article
#: (`devtools.artifact_dates` names the file and holds this to git), and it used to be
#: `PUBLICATION_DATE`, the day the edition was first published, which stood still while
#: the article changed under it: merging is the whole publish, so the text a reader sees
#: moves between editions. Change it in the commit that changes the article.
EXPLAINER_REVISED = "October 5, 2026"

#: The optimality review's own editions, newest first, each with the day it was first
#: published and what changed in the paper: the review's history, as `EXPLAINER_HISTORY`
#: is the explainer's, linked from its front (`PaperFront.history`). v0.1.0 is dated by
#: the commit that published it (620ffff54); the day it first went live is not recorded
#: (think-2cqu).
OPTIMALITY_REVIEW_HISTORY = (
    PublicationHistoryEntry(
        version="v0.1.6",
        first_published="October 6, 2026",
        result_scope=(
            "The uniqueness corollary is registered as T-112 and no longer called "
            "unreviewed, with its prior art: Trump's rigidity claim is local, and "
            "Stromquist's three optimal packings of ten squares show uniqueness is not "
            "automatic; and Queuingtheorydotcom's report of a complete Lean 4 "
            "formalization of October 6 is cited, with its native-compiler trust base "
            "and the project's statement audit."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.5",
        first_published="October 5, 2026",
        result_scope=(
            "The series revision: the paper is Part III of three, its lineage names Part "
            "II's three changes from T-026 and draws the series bound ladder as Figure 3, "
            "Charge Budgets contrasts capacity one with "
            "$\\lfloor m/k\\rfloor$, a test holds every term to a definition before its "
            "first use, and the notation follows the series: $L_0$, $\\Gamma_i$, "
            "$\\operatorname{rot}$, $\\mathbf{D}_4$ and $(191/50)/U$."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.4",
        first_published="October 4, 2026",
        result_scope=(
            "wand125's comment of October 4 is answered: the in-progress Lean 4 "
            "formalizations are named, with their status as wand125 reports it; the root "
            "node completes thirteen further updates, not fourteen; Figure 8 and the text "
            "agree that the symmetry lemma rests on the exhaustive search; and the "
            "1,931-case premise of cases 2175 and 2176 is stated as a premise of their "
            "accepted certificates, beside wand125's report of a Lean proof of all 76 "
            "prior-family cases that does not use it."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.3",
        first_published="October 3, 2026",
        result_scope=(
            "The closing section explains what a receipt is, the three depths at which "
            "a reader can verify the retained evidence, and the four checked components "
            "the reviews of October 3 added beside the accepted ones; the receipts "
            "register is linked."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.2",
        first_published="October 3, 2026",
        result_scope=(
            "The second reviewed revision: GPT-6 Pro's unified adversarial review of "
            "October 3 is applied. The invariant is stated row by row with ownership "
            "quantified over valid packings, the field citation names the original's "
            "§12 and a worked mask-0 certificate, the separation features are written "
            "as a disjunction of conjunctions, the isolation lemma carries the weighted "
            "residual, the five-site charge gains its ten-hull form, the root is "
            "certified unique on its interval, the uniqueness corollary is stated "
            "conditionally, and the frames, roles, radii and cover sites are tabulated."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.1",
        first_published="October 3, 2026",
        result_scope=(
            "The reviewed revision: the adversarial review of October 3 is applied, every "
            "term is defined before its first use, the transfer rule states the half-turn, "
            "the final deduction names the symmetry image, and the paper explains the tilt "
            "$u=\\tan(a/2)$, the polynomial as one contact and the four survivors as the "
            "construction under the eight symmetries."
        ),
    ),
    PublicationHistoryEntry(
        version="v0.1.0",
        first_published="September 30, 2026",
        result_scope="The first edition: the explainer of T-060's proof, with its figures.",
    ),
)

#: Where the review stands, and its version line: a draft, written on the two papers'
#: one credits form (`devtools.paper_front`; the owner, 2026-10-01: "Draft v0.1.0", not
#: bold). It is the review's version and not the site's, which was the first of #289's
#: questions on think-cv22 and is settled: the site's edition goes on no paper. Joined as
#: `edition_at` joins the publication's status and stamp, so going final is one edit
#: here too.
OPTIMALITY_REVIEW_STATUS = "Draft"
OPTIMALITY_REVIEW_VERSION = OPTIMALITY_REVIEW_HISTORY[0].version
OPTIMALITY_REVIEW_EDITION = " ".join(
    part for part in (OPTIMALITY_REVIEW_STATUS, OPTIMALITY_REVIEW_VERSION) if part
)

#: When the optimality review's own text last changed: the date its "Last revised" line
#: prints, by the rule `EXPLAINER_REVISED` follows -- the author date of the last commit
#: that changed its article, `n11-optimality-review-article.md`, held to git by
#: `devtools.artifact_dates`. Change it in the commit that changes the article.
OPTIMALITY_REVIEW_REVISED = "October 6, 2026"

#: The day the proof the review explains was published by its source, which the review's
#: "Original proof" date prints. A fact about someone else's work, so it is typed, and
#: held by `devtools.artifact_dates` to the day the register records for T-060.
OPTIMALITY_PROOF_PUBLISHED = "September 29, 2026"

#: Every edition of Part II, the review of Kleddamag's certified lower bound
#: `s(11) > 31/8` (T-037), newest first, as `OPTIMALITY_REVIEW_HISTORY` is Part III's.
THRESHOLD_REVIEW_HISTORY = (
    PublicationHistoryEntry(
        version="v0.1.0",
        first_published="October 5, 2026",
        result_scope=(
            "The first edition: Part II of the series, the review of T-037's proof, with "
            "its figures."
        ),
    ),
)

#: Part II's status and version line, on the papers' one credits form, as
#: `OPTIMALITY_REVIEW_EDITION` is Part III's.
THRESHOLD_REVIEW_STATUS = "Draft"
THRESHOLD_REVIEW_VERSION = THRESHOLD_REVIEW_HISTORY[0].version
THRESHOLD_REVIEW_EDITION = " ".join(
    part for part in (THRESHOLD_REVIEW_STATUS, THRESHOLD_REVIEW_VERSION) if part
)

#: When Part II's text last changed, by the rule `OPTIMALITY_REVIEW_REVISED` follows: the
#: author date of the last commit that changed `n11-threshold-bound-review-article.md`,
#: held to git by `devtools.artifact_dates`.
THRESHOLD_REVIEW_REVISED = "October 5, 2026"

#: The day Kleddamag published the proof Part II reviews (v1.0.2 of
#: 11-squares-certified-bound), which its "Original proof" date prints.
THRESHOLD_PROOF_PUBLISHED = "September 22, 2026"

#: The commit the committed claim documents link to
#: (`render_n11_lower_bounds_explainer.edition_file`), at this repository's short length. It is
#: pinned for the reason `DATA_REVISION` is: those documents are compared byte for byte with a
#: fresh render, so a link naming the build commit would fail their drift check forever. It is
#: in no version string. It moves when the claim documents are regenerated for an edition. It
#: must be a commit on `main`; the site's own links name `main` itself (`devtools.repo_links`).
PUBLICATION_REVISION = "07f01438"


def data_pathspec() -> tuple[str, ...]:
    """`DATA_PATHS` less `DATA_EXCLUDED`, as the arguments git takes after `--`."""
    return (*DATA_PATHS, *(f":(exclude){path}" for path in DATA_EXCLUDED))


def _shallow_boundary(repo: Path) -> frozenset[str]:
    """The commits a shallow clone's history is cut at; none in a complete clone."""
    found = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-path", "shallow"],
        capture_output=True,
        text=True,
        check=False,
    )
    if found.returncode != 0:
        return frozenset()
    shallow = Path(found.stdout.strip())
    shallow = shallow if shallow.is_absolute() else repo / shallow
    return frozenset(shallow.read_text().split()) if shallow.is_file() else frozenset()


def data_revision(repo: Path) -> str:
    """The full hash of the last commit in `repo` that changed the data, as git says.

    Raises where git cannot say: outside a repository, and in a shallow clone whose cut
    falls before the answer. git reports the commit a shallow history is cut at as
    changing every path, since it cannot see that commit's parent, so the boundary is
    refused rather than returned: a version stamped from it would name the wrong data.
    """
    found = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--format=%H", "--", *data_pathspec()],
        capture_output=True,
        text=True,
        check=False,
    )
    revision = found.stdout.strip()
    if found.returncode != 0 or not revision:
        raise RuntimeError(
            f"git cannot name the last data commit in {repo}: "
            f"{found.stderr.strip() or 'no commit touches ' + ', '.join(DATA_PATHS)}"
        )
    if revision in _shallow_boundary(repo):
        raise RuntimeError(
            f"git cannot name the last data commit in {repo}: its shallow history is cut "
            f"at {revision[:12]}, so whether that commit changed the data cannot be seen"
        )
    return revision


def commit_date(repo: Path, revision: str) -> str:
    """The ISO date of the commit `revision` in `repo`: its author date, on the author's
    own calendar, which is the day a reader would say the change was made.

    The commit records its own offset, so the answer is the same on every machine. Raises
    where git cannot say: outside a repository, or for a commit this clone does not have.
    """
    found = subprocess.run(
        ["git", "-C", str(repo), "show", "-s", "--format=%as", f"{revision}^{{commit}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    day = found.stdout.strip()
    if found.returncode != 0 or not day:
        raise RuntimeError(
            f"git cannot date {revision[:12]} in {repo}: "
            f"{found.stderr.strip() or 'no such commit'}"
        )
    return day


def last_change_date(repo: Path, *paths: str) -> str:
    """The ISO date of the last change to any of `paths`: the latest author date among
    the commits that changed one, merges excluded.

    A merge is excluded because it is not when anyone wrote the text, and the latest date
    is taken, not the first commit `git log` lists, because two branches merged out of
    order list the earlier change first. Raises where git cannot say, and in a shallow
    clone, where a change below the cut cannot be seen.
    """
    found = subprocess.run(
        ["git", "-C", str(repo), "log", "--no-merges", "--format=%H %as", "--", *paths],
        capture_output=True,
        text=True,
        check=False,
    )
    changes = [line.split() for line in found.stdout.splitlines() if line.strip()]
    if found.returncode != 0 or not changes:
        raise RuntimeError(
            f"git cannot date the last change to {', '.join(paths)} in {repo}: "
            f"{found.stderr.strip() or 'no commit changes it'}"
        )
    if _shallow_boundary(repo):
        raise RuntimeError(
            f"git cannot date the last change to {', '.join(paths)} in {repo}: its "
            "history is shallow, so a later change may lie below the cut"
        )
    return max(day for _commit, day in changes)


def data_version(repo: Path) -> str:
    """The shared version as git says it is now, which the pinned one must equal.

    Artifacts print `PUBLICATION_EDITION` rather than this, so that a render needs no
    history; this is what the drift check holds that pin to.
    """
    return f"{PUBLICATION_VERSION}-{data_revision(repo)[:DATA_REVISION_LENGTH]}"
