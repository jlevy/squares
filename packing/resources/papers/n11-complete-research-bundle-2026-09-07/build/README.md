# Rebuilding the PDF reports

The delivered PDFs are ready to read. Rebuilding is optional and requires
Pandoc, a LaTeX installation containing `pdflatex`, and Python with `pypdf`.
The mathematical checkers do not require any of these PDF dependencies.

From the bundle root:

```sh
python build/rebuild_reports.py
```

The command writes to `rebuild/`, preserving the original delivered report bytes.
It rebuilds each report in the appropriate working directory, then combines the
new addendum followed by the original review. The editable `complete_review.md`
is a convenience concatenation; the two original Markdown sources and their
headers are the authoritative PDF build inputs.

PDF timestamps and renderer versions can change PDF byte hashes on rebuilding.
The checksum manifest attests to the delivered files, not every future rebuild.
No font files are included in this distribution.
