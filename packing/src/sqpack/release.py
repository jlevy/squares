"""What this project calls the edition its reader-facing artifacts belong to.

The atlas draws it under its title and the explainer prints it in its credits, so a
release is stamped in one place and both follow. This is the publication's version, not
the package's: `pyproject.toml` versions the code, and the two move for different
reasons.
"""

from __future__ import annotations

#: The edition the figures and the explainer state. Bump it when they are republished.
PUBLICATION_VERSION = "v0.1.0"

#: Where the edition stands, said ahead of the version. Empty once it is final; the
#: join below then drops it and the stray space with it, so going final is one edit.
PUBLICATION_STATUS = "DRAFT"

#: How the edition is written wherever it is stamped. The atlas footer and the
#: explainer's credits both take this string, so the two artifacts cannot disagree
#: about whether the reader is holding a draft.
PUBLICATION_EDITION = " ".join(
    part for part in (PUBLICATION_STATUS, PUBLICATION_VERSION) if part
)

#: The date that edition carries, written the way a reader reads it.
PUBLICATION_DATE = "September 5, 2026"

#: The commit the edition was cut from. Pinned rather than read from git at build time:
#: the atlas SVG is compared byte for byte against a fresh render, and a live revision
#: would differ from the committed one the moment it was committed, failing that gate
#: forever. Bump it with the version when republishing.
PUBLICATION_REVISION = "3bd273e6"
