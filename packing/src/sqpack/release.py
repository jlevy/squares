"""What this project calls the edition its reader-facing artifacts belong to.

The atlas draws it under its title and the explainer prints it in its credits, so a
release is stamped in one place and both follow. This is the publication's version, not
the package's: `pyproject.toml` versions the code, and the two move for different
reasons.
"""

from __future__ import annotations

#: The edition the figures and the explainer state. Bump it when they are republished.
PUBLICATION_VERSION = "v0.2.1"

#: Where the edition stands, said ahead of the version. Empty once it is final; the
#: join below then drops it and the stray space with it, so going final is one edit.
PUBLICATION_STATUS = "DRAFT"

#: The commit the committed artifacts are stamped with, at this repository's own short
#: length -- the eight characters `git rev-parse --short` prints here -- so the hash a
#: reader sees in the atlas footer is one they can paste into `git show` and have
#: resolve.
#:
#: Pinned rather than read from git at build time, because the artifacts that carry it
#: are checked in: the atlas SVG is compared byte for byte against a fresh render, and
#: the claim documents' links name it, so a live revision would differ from the
#: committed one the moment it was committed and fail those gates forever. The page is
#: the exception, and deliberately: it is rendered on every deploy and stamps the commit
#: it is built from (`render_explainer.page_edition`), so its hash moves with every push
#: while this one moves when an edition is cut.
PUBLICATION_REVISION = "9307172a"

#: The version, written the one way it is ever written: `v0.1.0-3bd273e6`. Semver core,
#: then the revision, in the shape a build identifier takes everywhere else.
#:
#: This is the value to reach for. It exists because the two artifacts that stamp an
#: edition -- the atlas footer and the explainer's credits -- each used to compose their
#: own string from the parts, in two files and two languages, joined by a literal
#: ", revision ". Two hand-assembled spellings of one fact is how they come to disagree,
#: and neither could be changed without remembering the other.
PUBLICATION_STAMP = f"{PUBLICATION_VERSION}-{PUBLICATION_REVISION}"

#: How the edition is written wherever it is stamped: the stamp, with the status ahead
#: of it while there is one. The atlas footer and the explainer's credits both take this
#: string whole, so the two artifacts cannot disagree about whether the reader is holding
#: a draft, nor about how the version is spelled.
PUBLICATION_EDITION = " ".join(part for part in (PUBLICATION_STATUS, PUBLICATION_STAMP) if part)

#: The date that edition carries, written the way a reader reads it.
PUBLICATION_DATE = "September 6, 2026"
