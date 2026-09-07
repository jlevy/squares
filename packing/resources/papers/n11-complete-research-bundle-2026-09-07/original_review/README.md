# Eleven-square research review

The report reviews the supplied September 6, 2026 research snapshot, develops
new structural deductions and proposed proof architectures, and includes an
exact finite-support result relevant to the next density experiment.

- `n11_research_review.pdf`: typeset technical report.
- `n11_research_review.md`: editable report source.
- `certificate/`: standard-library exact checker, tests, retained results, and
  a separate README specifying the proof scope.
- `report_header.tex`, `table_widths.lua`, and `trump_cover.png`: PDF build assets.
  The image is rendered from the user-supplied file 18; it is not new geometry.

To rebuild the PDF with Pandoc and a LaTeX installation:

```sh
pandoc n11_research_review.md -s --number-sections --toc --toc-depth=1 \
  --lua-filter=table_widths.lua -H report_header.tex \
  --pdf-engine=pdflatex -o n11_research_review.pdf
```

The report contains no new global lower bound for s(11) and does not assert
Trump optimality. Its newly established fixed-support result and structural
lemmas have the scopes stated in their sections. See the report for proposed
research directions, first unresolved implications, and success/stop conditions.
