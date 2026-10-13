# Evan Daniel’s Regularizer, Vendored

This directory is a subset of Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing), copied unmodified at
one commit: the exact solver and its two exact checkers under `search/exact/`, the
display regularizer under `search/regularize/`, and the inputs and lists they read.
It is the generator behind this project’s regularized drawing layer.
It decides nothing here: every view it produces is decided by this project’s exact
checkers, and a view the checkers refuse is refused whatever the generator reported.

Evan Daniel wrote the code and holds its copyright.
Upstream’s [CREDITS.md](CREDITS.md) says, under “Provenance of this work”, that the work
was produced by Claude (Anthropic) under his direction.
The code is under the MIT licence, whose notice is kept with this copy in
[LICENSE](LICENSE).

This README and [vendored.yaml](vendored.yaml) are this project’s own files; everything
else here is upstream’s.
`vendored.yaml` is the machine-readable manifest: the pin, the licence and every file’s
size, SHA-256 and executable bit.
`devtools.check_vendored_evand` holds the directory to the manifest in the edit tier and
on every pull request, and its `--upstream` mode holds the manifest to upstream
([Checking the Copy](#checking-the-copy)).

## Source and Pin

| Field | Value |
| --- | --- |
| Repository | https://github.com/evand/square-packing |
| Commit | `675a5eaa8712542daac8b4515b0f69ad7044df44` |
| Committed | 2026-10-11T10:34:02-06:00 (16:34:02Z) |
| Subject | Site: a record drawing identical to a catalogue drawing is listed once |
| Tree | `fc24671215a46a239fcb8f30d2c16773b095cceb` |
| Retrieved | 2026-10-11 |
| Licence | MIT, “Copyright (c) 2026 Evan Daniel” |
| Files | 351, 2,089,912 bytes |

Every file keeps its upstream path relative to the repository root, so the code’s own
`sys.path` insertions and relative paths (`reg.py` reads `../exact/batch/results.json`,
`write_cert` imports `../exact/verify_cert.py`) work unchanged.
Upstream’s
[root README](https://github.com/evand/square-packing/blob/675a5eaa8712542daac8b4515b0f69ad7044df44/README.md)
is not vendored; its “Data, licence, credits” section is where upstream states the MIT
grant and carves David Ellsworth’s drawings under `site/www/data/` out of it.
Nothing from `site/` is vendored either, but the alternates lists quote the same
catalogue (see [Credit](#credit)).

The
[regularization assessment](../../docs/project/research/research-2026-10-11-evand-regularization-assessment.md)
read upstream at `060c1a1`. Between that commit and this pin, the vendored paths changed
only by the addition of `search/regularize/posted_cert.py`; the rest of what changed
under `search/` there was raw posted certificates and a Lean log, none of it vendored.

## Credit

A drawing or record made with this code credits Evan Daniel’s method and code beside the
credit it already gives the packing’s finders, which regularization does not change.
Two forms, because [conventions.md](../../conventions.md#6-provenance) keeps commit ids
out of reader prose:

- **In structured fields** -- a regularization’s `method`, a run receipt, an evidence
  entry -- write the pin:
  `regularized with Evan Daniel's search/regularize (MIT), evand/square-packing@675a5ea`.
- **In reader prose** -- register prose, the README, case records, site text -- link it
  and leave the pin in the link target:
  `regularized with Evan Daniel’s [search/regularize](https://github.com/evand/square-packing/tree/675a5eaa8712542daac8b4515b0f69ad7044df44/search/regularize) (MIT)`.

Upstream’s lists and batch inputs are derived from this project’s known-best witnesses
(CC BY 4.0, Joshua Levy, the squares project) and from Evan Daniel’s packing store;
`search/exact/batch/README.md` and `search/regularize/REGULARIZE.md` say which.
The alternates lists also draw on David Ellsworth’s
[catalogue of squares in squares](https://kingbird.myphotos.cc/packing/squares_in_squares.html):
70 of the 74 rows of `search/regularize/lists/alternates.json`, `.csv` and `.md` name a
catalogue drawing as their source, and 64 of them quote its attribution text.
Upstream’s README says of the same material in its `site/www/data/`, derived from his
drawings and quoting his attribution text, that it is his and not covered by the MIT
licence. The root [LICENSE](../../LICENSE) treats these rows the same way.

## What Each File Is For

The pipeline this project runs, per count, is the assessment’s adaptation plan (section
5): an `n S` then `x y degrees` input written from this project’s witness, the exact
solve, then the regularizer, then this project’s checkers.

| Path | Role |
| --- | --- |
| `LICENSE` | The MIT notice, which stays with every copy |
| `CREDITS.md` | Upstream’s credits and its provenance disclosure |
| `search/exact/exactsolve.py` | The exact solve: the 80-digit KKT point of *min S subject to non-overlap* near an input packing, its contacts and free squares, and a dilated rational certificate |
| `search/exact/geom.py` | The contact geometry `exactsolve.py` imports |
| `search/exact/verify_cert.py` | Upstream’s first exact checker (separating axes over `Fraction`); `exactsolve.py` and `reg.write_cert` call it |
| `search/exact/verify_cert2.py` | Upstream’s second exact checker (vertex-in-polygon and edge intersection), sharing no geometry code with the first |
| `search/exact/README.md` | The exact-forms log |
| `search/exact/batch/inputs/n-N.txt` | The 324 inputs upstream solved, one per count, from this project’s witnesses (17 polished by upstream’s SLP); 272 rows of the best-choice list rest on them, the other 52 on Evan Daniel’s store |
| `search/exact/batch/results.json` | The batch’s per-count status; `reg.load` reads each count’s `from_`, `status`, `by` and `register` from it |
| `search/exact/batch/README.md` | The batch’s method, results and data credit |
| `search/exact/batch/register.py` | How upstream read this register; it reads upstream’s `site/data/`, which is not vendored |
| `search/exact/batch/reproduce.sh` | Upstream’s re-solve-and-compare script; it compares with `certs/`, which is not vendored, so here it reports every count as different |
| `search/regularize/reg.py` | The regularizer: orientation, angle groups, the translation LP at fixed side, refinement at 80 digits, verification, and `write_cert` |
| `search/regularize/atlas.py` | The driver: `compute --policy conservative --style coincide` regularizes each count into `runs/regularize/`; `draw` needs matplotlib |
| `search/regularize/REGULARIZE.md` | The method log |
| `search/regularize/samepacking.py` | The same-packing path test and the KKT re-solve of a regularized output |
| `search/regularize/lists.py` | Builds the best-choice and alternates lists from `runs/` |
| `search/regularize/lists/` | Upstream’s lists at the pin, as JSON, CSV and Markdown; `devtools.compare_evand_regularization` reads `best.json` by default |
| `search/regularize/census.py` | The tie-break census over gravity, symmetry and orientation variants |
| `search/regularize/gallery.py` | Side-by-side PNG galleries; imports matplotlib at load |
| `search/regularize/refresh.py` | Refreshes inputs from Evan Daniel’s store; needs `search/packer/`, which is not vendored |
| `search/regularize/register_cert.py`, `posted_cert.py` | Certificates converted from register witnesses and from posted certificates; they read paths outside this copy |

**Dependencies.** numpy, scipy (HiGHS `linprog` and `milp`, `linear_sum_assignment`) and
mpmath, all in `packing/uv.lock`, carry the solve and the regularizer; PyYAML, also
locked, is read only by `register_cert.py` and `batch/register.py`. sympy is imported in
one place, lazily, in `exactsolve.identify`, which runs only when `--algdeg` is above
its default of 0; the conservative and coincide path never imports it, and sympy 1.14.0
is locked anyway through the `symbolic` extra and the `dev` group.
matplotlib is imported by `gallery.py` at load and by `atlas.py draw`; it is not in the
lockfile and `atlas.py compute` does not need it.
This project runs neither.
If a drawing path ever needs them, matplotlib enters through `packing/uv.lock` under the
dependency cool-off (`tbd guidelines supply-chain-hardening`), never through an ad-hoc
`pip install` or an unpinned `uvx`.

## How This Project Runs It

Run the code from a scratch replica outside the checkout, as the assessment’s plan does,
with `python -I` from outside that tree; never write run outputs into this directory.
The check refuses any file the manifest does not list, so a stray `runs/` or
`search/exact/batch/work/` here fails it.

The copy sits outside this project’s own floors, each exclusion saying why where it is
made: Ruff and BasedPyright do not reach `vendor/`, the lint-floor contract names this
directory, the integrity-ceremony scan skips `vendor/`, flowmark and Biome ignore
`vendor/`, and the document map and the retained-JSON layout exempt it.
The embedded-JavaScript scan reads its Python like any other and finds none.

## Checking the Copy

There are two checks, because the offline one cannot see upstream.

- **Offline**: `python -m devtools.check_vendored_evand` from `packing/`, in the edit
  tier and on every pull request.
  It holds the copy to `vendored.yaml`: every pinned file’s size, SHA-256 and executable
  bit, each recorded local change, and no other file in the directory.
  It refuses a symbolic link anywhere in the copy.
  It also refuses a module file named after a standard-library module, a dependency the
  scripts import, such as a `numpy.py`, or a module a dependency looks up as it loads,
  such as a `gmpy2.py`, which mpmath tries at import and falls back from silently: five
  of the scripts put `search/regularize/` first on `sys.path` and two put
  `search/exact/` there, so such a file would be imported in that module’s place.
  The last group is measured by a test, with the optional modules installed and with
  them hidden; what it cannot measure is named by hand, and anything a dependency
  imports only later, at call time, is left to `--upstream`, which refuses any file
  upstream’s tree does not hold.
  **It catches accidental edits only.** Its expected values come from the manifest, so
  a change that edits a vendored file and that file’s manifest line together passes it.
- **Upstream**: the same command with `--upstream`.
  It first fetches the commits of every upstream branch and tag, without trees or
  blobs, and refuses a pin none of them holds: GitHub serves a pull request’s head by
  id through upstream’s own URL, so a third party’s unmerged commit would otherwise
  pass as upstream’s.
  It then fetches the pinned commit’s trees, without blobs, into a temporary bare
  repository, and deletes both afterwards.
  It requires the commit’s tree, date and subject to be the manifest’s, every pristine
  file’s Git blob id and mode to be upstream’s at the pin, and every file here to be in
  upstream’s tree unless it is a recorded addition, and it names the branches and tags
  that hold the pin.
  It fetches only from `https://github.com/evand/square-packing`, and refuses a
  manifest that names another source.
  It needs the network, so no offline tier runs it.
  Run it at every re-pin and before merging any change to `vendored.yaml` or to a
  vendored file.

No gate runs `--upstream` yet, so the person reviewing a change to this directory runs
it; `think-vwlm` tracks a networked gate that would.

## Forking

The copy may be adjusted, and every adjustment is a reviewed patch:

1. Change the file in a commit of its own, with the reason in the message.
2. Add an entry to `local_changes` in `vendored.yaml`: `path`, `kind` (`modified`,
   `added` or `removed`), `date`, `bead` and `reason`. A modified file keeps its pinned
   entry, so the pristine bytes stay reconstructible from the upstream pin.
3. A modified or added `.py` or `.sh` file says so in a header comment, within its first
   20 lines, naming `vendor/evand-regularize/README.md` and the bead.
   A pristine file carries no such comment.
4. Describe the change under Local Changes below, by path.

`LICENSE` is never changed.
The check refuses an edit with no entry, an entry whose file is still the pinned bytes,
a patched script with no header comment, and an entry Local Changes does not name.
Only that section counts: the role table above names every file.

### Local Changes

None. Every file is byte-identical to the pin.

## Re-pinning

1. Bring an upstream checkout to the new commit, for example
   `git -C attic/evand-square-packing fetch` and `checkout <commit>`, and read the
   upstream diff over every vendored path.
2. If local changes are recorded, restore the pristine files first; they are re-applied
   at the end.
3. Replace each vendored file with its bytes at the new commit
   (`git -C <checkout> show <commit>:<path>`), add any file the pipeline newly needs,
   and delete any the new commit no longer has.
4. From `packing/`, run
   `uv run --frozen --all-extras --group dev python -m devtools.check_vendored_evand --write --checkout ../attic/evand-square-packing --commit <commit> --retrieved <date>`,
   with the full 40-digit commit id.
   It compares every vendored file with the checkout’s blob at the commit, byte for
   byte and mode for mode, refuses on any difference or symbolic link, and rewrites
   `vendored.yaml`.
   It needs the network: it refuses a checkout whose `origin` is not upstream, and a
   commit none of upstream’s branches or tags holds, such as a pull request’s head.
5. Run the check with `--upstream`, which holds the rewritten manifest to upstream
   itself rather than to the local checkout.
6. Update Source and Pin and the credit lines above.
   Records made at the old pin keep naming it as their provenance.
7. Re-apply and re-record any local changes, then run the check, `--upstream` again,
   and the edit tier.
   A re-pin invalidates nothing the exact checkers have already decided.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
