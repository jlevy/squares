---
type: is
id: is-01m15219m6eh8fww5pm9sc2sqd
title: Reorganize the repository around the packing project
kind: epic
status: open
priority: 1
version: 19
labels: []
dependencies: []
child_order_hints:
  - is-01m154398w2dzawws1aasewmg9
  - is-01m15441mc3v07taypnqeycjqc
  - is-01m15441zgw9e4ez6g7v8d1mrm
  - is-01m15442akdex5khfn7z8hrarb
  - is-01m15442nxmwj32dq2kgrxgk4t
  - is-01m1544315q4s96kgexe71qybx
  - is-01m15443cdzm4pyh7nkgbwgrd8
  - is-01m15443qrx72drzbbdpc6eqrk
  - is-01m1544433qhzbbx73s6kjh9gn
  - is-01m15444eff52e4tcfv8qthya7
  - is-01m15444sqtndc8k38h7bd5k6w
  - is-01m15b677wgahayme0bp99y2fn
  - is-01m15b67k65dz0mcqmdcwq1812
  - is-01m15b67y6cz730v40emet4x84
  - is-01m15b6893dkxa2qncvjhgtdp2
  - is-01m15b68m8zw92zf42gy1xvjv0
  - is-01m15b68zcgvpqmyb1gad46xav
  - is-01m15b69acbnaetfj9f895en85
created_at: 2026-08-28T20:47:28.901Z
updated_at: 2026-08-28T23:27:29.611Z
---
Hoist the reader-facing documents of `explorations/packing/` to the repository root and
collapse the remaining two levels to a single `packing/` container. `explorations/`
disappears; it only ever held packing.

Target layout:

    squares/
      README.md SYNOPSIS.md TUTORIAL.md conventions.md development.md defects.md
      docs/project/{research,reviews,specs,...}
      AGENTS.md CLAUDE.md Makefile lefthook.yml package.json package-lock.json
      .github/ .agents/ .claude/ .codex/ .tbd/ .flowmarkignore .gitattributes .gitignore
      packing/
        atlas/ benchmarks/ campaign/ cases/ devtools/ frankensim-probe/ frontier/
        golden/ resources/ src/ sqsearch/ tests/ witnesses/
        defects.yaml defects.schema.yaml pyproject.toml uv.lock .python-version

Why the split lands there: every prose document a reader wants is at eye level, and
everything that is code, data, or research record is one level down, so the root stays
about fifteen visible entries.

What makes this tractable: nearly every path constant in the codebase is file-relative
and counts parents up to the packing project directory, and `src/sqpack/project.py`
finds the project by marker discovery (`pyproject.toml`, `campaign`, `cases`,
`devtools`, `frontier`) rather than by a fixed path. All five markers stay together
inside `packing/`, so the whole `sqpack` runtime keeps working untouched. `sqsearch/`
has no upward references at all and is a pure directory move.

What breaks is exactly the set of things that reach ABOVE the packing directory, plus
every link that now crosses the new docs/code boundary. The child beads enumerate it.

Deliberately NOT rewritten: roughly 100 campaign session logs, experiment artifacts,
reviews and handoffs mention `explorations/packing` as historical record of commands as
actually run, as do 7 entries in defects.yaml and 595 beads. Nothing executes them
(`check_declared_commands.py` parses only the arguments after `packing-validate` /
`packing-ledger`; the `regression:` field in defects.yaml is only ever compared against
the literal "none"). Rewriting them would falsify the record for no gain.

Scale: 1,160 files move. Exactly one name collision, README.md.

Sequencing note: the move commit is rename-only so Git records renames and
`git log --follow` survives; the tree is knowingly broken at that commit and repaired by
the ones after it, inside a single PR.
